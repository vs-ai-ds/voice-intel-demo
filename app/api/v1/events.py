"""Event endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path, Header
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.db.session import get_db
from app.schemas.events import EventCreate, EventStoredResponse
from app.schemas.common import Envelope, Meta
from app.repositories.call import CallRepository
from app.repositories.event import EventRepository
from app.core.logging import request_id_var, correlation_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants/{tenant_id}/calls/{call_id}/events", tags=["events"])

@router.post("")
async def create_event(
    request: EventCreate,
    tenant_id: UUID = Path(...),
    call_id: UUID = Path(...),
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
    db: Session = Depends(get_db)
):
    """POST /tenants/{tenant_id}/calls/{call_id}/events."""
    request_id = request_id_var.get() or "unknown"
    
    # Verify call exists and belongs to tenant
    call_repo = CallRepository(db)
    call = call_repo.get_by_tenant(tenant_id, call_id)
    if not call:
        raise APIError(
            code="NOT_FOUND",
            message=f"Call {call_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    # Use correlation_id from request or header
    correlation_id = request.correlation_id or x_correlation_id or correlation_id_var.get()
    
    from app.db.models.event import Event
    event = Event(
        call_id=call_id,
        type=request.type,
        correlation_id=correlation_id,
        payload=request.payload
    )
    
    repo = EventRepository(db)
    event = repo.create(event)
    
    return Envelope(
        ok=True,
        data=EventStoredResponse(stored=True).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

