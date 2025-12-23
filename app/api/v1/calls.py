"""Call endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.db.session import get_db
from app.schemas.calls import CallCreate, CallResponse, CallListItem, CallDetail
from app.schemas.common import Envelope, PaginatedEnvelope, Meta, PaginationMeta
from app.repositories.call import CallRepository
from app.repositories.tenant import TenantRepository
from app.repositories.agent import AgentRepository
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants/{tenant_id}/calls", tags=["calls"])

@router.post("")
async def create_call(
    request: CallCreate,
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """POST /tenants/{tenant_id}/calls."""
    request_id = request_id_var.get() or "unknown"
    
    # Verify tenant exists
    tenant_repo = TenantRepository(db)
    tenant = tenant_repo.get(tenant_id)
    if not tenant:
        raise APIError(
            code="NOT_FOUND",
            message=f"Tenant {tenant_id} not found",
            status_code=404
        )
    
    # Verify agent exists and belongs to tenant
    agent_repo = AgentRepository(db)
    agent = agent_repo.get_by_tenant(tenant_id, UUID(request.agent_id))
    if not agent:
        raise APIError(
            code="NOT_FOUND",
            message=f"Agent {request.agent_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    from app.db.models.call import Call
    call = Call(
        tenant_id=tenant_id,
        agent_id=UUID(request.agent_id),
        provider=request.provider,
        provider_call_id=request.provider_call_id,
        from_phone=request.from_phone,
        to_phone=request.to_phone,
        direction=request.direction,
        status="INITIATED",
        language=request.locale_hint
    )
    
    repo = CallRepository(db)
    call = repo.create(call)
    
    return Envelope(
        ok=True,
        data=CallResponse(
            id=str(call.id),
            tenant_id=str(call.tenant_id),
            provider=call.provider,
            provider_call_id=call.provider_call_id,
            from_phone=call.from_phone,
            to_phone=call.to_phone,
            direction=call.direction,
            agent_id=str(call.agent_id),
            status=call.status,
            started_at=call.started_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("")
async def list_calls(
    tenant_id: UUID = Path(...),
    status: Optional[str] = Query(None),
    from_phone: Optional[str] = Query(None),
    to_phone: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/calls."""
    request_id = request_id_var.get() or "unknown"
    
    # Verify tenant exists
    tenant_repo = TenantRepository(db)
    tenant = tenant_repo.get(tenant_id)
    if not tenant:
        raise APIError(
            code="NOT_FOUND",
            message=f"Tenant {tenant_id} not found",
            status_code=404
        )
    
    # Parse dates
    date_from_dt = None
    date_to_dt = None
    if date_from:
        try:
            date_from_dt = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
        except ValueError:
            raise APIError(
                code="VALIDATION_ERROR",
                message="Invalid date_from format (use ISO 8601)",
                status_code=400
            )
    if date_to:
        try:
            date_to_dt = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
        except ValueError:
            raise APIError(
                code="VALIDATION_ERROR",
                message="Invalid date_to format (use ISO 8601)",
                status_code=400
            )
    
    repo = CallRepository(db)
    skip = (page - 1) * page_size
    calls, total = repo.list_by_tenant(
        tenant_id=tenant_id,
        status=status,
        from_phone=from_phone,
        to_phone=to_phone,
        date_from=date_from_dt,
        date_to=date_to_dt,
        skip=skip,
        limit=page_size
    )
    
    has_more = (skip + len(calls)) < total
    
    # Calculate duration_sec
    def calc_duration(call):
        if call.ended_at and call.started_at:
            return int((call.ended_at - call.started_at).total_seconds())
        return None
    
    return PaginatedEnvelope(
        ok=True,
        data=[
            CallListItem(
                id=str(c.id),
                provider_call_id=c.provider_call_id,
                from_phone=c.from_phone,
                status=c.status,
                started_at=c.started_at.isoformat() + "Z",
                ended_at=c.ended_at.isoformat() + "Z" if c.ended_at else None,
                duration_sec=calc_duration(c),
                language=c.language,
                handoff=c.handoff
            ).model_dump()
            for c in calls
        ],
        meta=PaginationMeta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
            page=page,
            page_size=page_size,
            total=total,
            has_more=has_more
        )
    ).model_dump()

@router.get("/{call_id}")
async def get_call(
    tenant_id: UUID = Path(...),
    call_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/calls/{call_id}."""
    request_id = request_id_var.get() or "unknown"
    
    repo = CallRepository(db)
    call = repo.get_by_tenant(tenant_id, call_id)
    if not call:
        raise APIError(
            code="NOT_FOUND",
            message=f"Call {call_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    return Envelope(
        ok=True,
        data=CallDetail(
            id=str(call.id),
            agent_id=str(call.agent_id) if call.agent_id else None,
            status=call.status,
            from_phone=call.from_phone,
            language=call.language,
            summary=call.summary,
            metrics=call.metrics
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

