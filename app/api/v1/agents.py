"""Agent endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.db.session import get_db
from app.schemas.agents import AgentCreate, AgentUpdate, AgentResponse
from app.schemas.common import Envelope, PaginatedEnvelope, Meta, PaginationMeta
from app.repositories.agent import AgentRepository
from app.repositories.tenant import TenantRepository
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants/{tenant_id}/agents", tags=["agents"])

@router.post("")
async def create_agent(
    request: AgentCreate,
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """POST /tenants/{tenant_id}/agents."""
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
    
    from app.db.models.agent import Agent
    agent = Agent(
        tenant_id=tenant_id,
        name=request.name,
        status=request.status,
        languages=request.languages,
        voice=request.voice,
        stt=request.stt,
        llm=request.llm,
        routing=request.routing,
        policies=request.policies,
        tools_enabled=request.tools_enabled
    )
    
    repo = AgentRepository(db)
    agent = repo.create(agent)
    
    return Envelope(
        ok=True,
        data=AgentResponse(
            id=str(agent.id),
            tenant_id=str(agent.tenant_id),
            name=agent.name,
            status=agent.status,
            languages=agent.languages or [],
            voice=agent.voice or {},
            stt=agent.stt or {},
            llm=agent.llm or {},
            routing=agent.routing or {},
            policies=agent.policies or {},
            tools_enabled=agent.tools_enabled or [],
            created_at=agent.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("")
async def list_agents(
    tenant_id: UUID = Path(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/agents."""
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
    
    repo = AgentRepository(db)
    skip = (page - 1) * page_size
    agents = repo.list_by_tenant(tenant_id, skip=skip, limit=page_size)
    
    # Get total count
    from app.db.models.agent import Agent
    total = db.query(Agent).filter(Agent.tenant_id == tenant_id).count()
    has_more = (skip + len(agents)) < total
    
    return PaginatedEnvelope(
        ok=True,
        data=[
            AgentResponse(
                id=str(a.id),
                tenant_id=str(a.tenant_id),
                name=a.name,
                status=a.status,
                languages=a.languages or [],
                voice=a.voice or {},
                stt=a.stt or {},
                llm=a.llm or {},
                routing=a.routing or {},
                policies=a.policies or {},
                tools_enabled=a.tools_enabled or [],
                created_at=a.created_at.isoformat() + "Z"
            ).model_dump()
            for a in agents
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

@router.get("/{agent_id}")
async def get_agent(
    tenant_id: UUID = Path(...),
    agent_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/agents/{agent_id}."""
    request_id = request_id_var.get() or "unknown"
    
    repo = AgentRepository(db)
    agent = repo.get_by_tenant(tenant_id, agent_id)
    if not agent:
        raise APIError(
            code="NOT_FOUND",
            message=f"Agent {agent_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    return Envelope(
        ok=True,
        data=AgentResponse(
            id=str(agent.id),
            tenant_id=str(agent.tenant_id),
            name=agent.name,
            status=agent.status,
            languages=agent.languages or [],
            voice=agent.voice or {},
            stt=agent.stt or {},
            llm=agent.llm or {},
            routing=agent.routing or {},
            policies=agent.policies or {},
            tools_enabled=agent.tools_enabled or [],
            created_at=agent.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.patch("/{agent_id}")
async def update_agent(
    request: AgentUpdate,
    tenant_id: UUID = Path(...),
    agent_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """PATCH /tenants/{tenant_id}/agents/{agent_id}."""
    request_id = request_id_var.get() or "unknown"
    
    repo = AgentRepository(db)
    agent = repo.get_by_tenant(tenant_id, agent_id)
    if not agent:
        raise APIError(
            code="NOT_FOUND",
            message=f"Agent {agent_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    # Update fields
    if request.name is not None:
        agent.name = request.name
    if request.status is not None:
        agent.status = request.status
    if request.languages is not None:
        agent.languages = request.languages
    if request.voice is not None:
        agent.voice = request.voice
    if request.stt is not None:
        agent.stt = request.stt
    if request.llm is not None:
        agent.llm = request.llm
    if request.routing is not None:
        agent.routing = request.routing
    if request.policies is not None:
        agent.policies = request.policies
    if request.tools_enabled is not None:
        agent.tools_enabled = request.tools_enabled
    
    agent = repo.update(agent)
    
    return Envelope(
        ok=True,
        data=AgentResponse(
            id=str(agent.id),
            tenant_id=str(agent.tenant_id),
            name=agent.name,
            status=agent.status,
            languages=agent.languages or [],
            voice=agent.voice or {},
            stt=agent.stt or {},
            llm=agent.llm or {},
            routing=agent.routing or {},
            policies=agent.policies or {},
            tools_enabled=agent.tools_enabled or [],
            created_at=agent.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

