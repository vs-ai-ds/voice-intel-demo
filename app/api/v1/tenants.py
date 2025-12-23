"""Tenant endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.db.session import get_db
from app.schemas.tenants import TenantCreate, TenantUpdate, TenantResponse
from app.schemas.common import Envelope, PaginatedEnvelope, Meta, PaginationMeta
from app.repositories.tenant import TenantRepository
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.post("")
async def create_tenant(
    request: TenantCreate,
    db: Session = Depends(get_db)
):
    """POST /tenants - Create tenant."""
    request_id = request_id_var.get() or "unknown"
    
    repo = TenantRepository(db)
    
    # Check slug uniqueness
    existing = repo.get_by_slug(request.slug)
    if existing:
        raise APIError(
            code="CONFLICT",
            message=f"Tenant with slug '{request.slug}' already exists",
            status_code=409
        )
    
    from app.db.models.tenant import Tenant
    tenant = Tenant(
        name=request.name,
        slug=request.slug,
        timezone=request.timezone,
        default_language=request.default_language,
        features=request.features
    )
    tenant = repo.create(tenant)
    
    return Envelope(
        ok=True,
        data=TenantResponse(
            id=str(tenant.id),
            name=tenant.name,
            slug=tenant.slug,
            timezone=tenant.timezone,
            default_language=tenant.default_language,
            features=tenant.features or {},
            created_at=tenant.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("")
async def list_tenants(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """GET /tenants - List tenants."""
    request_id = request_id_var.get() or "unknown"
    
    repo = TenantRepository(db)
    skip = (page - 1) * page_size
    tenants = repo.list_all(skip=skip, limit=page_size)
    
    # Get total count
    total = db.query(repo.model).count()
    has_more = (skip + len(tenants)) < total
    
    return PaginatedEnvelope(
        ok=True,
        data=[
            TenantResponse(
                id=str(t.id),
                name=t.name,
                slug=t.slug,
                timezone=t.timezone,
                default_language=t.default_language,
                features=t.features or {},
                created_at=t.created_at.isoformat() + "Z"
            ).model_dump()
            for t in tenants
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

@router.get("/{tenant_id}")
async def get_tenant(
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}."""
    request_id = request_id_var.get() or "unknown"
    
    repo = TenantRepository(db)
    tenant = repo.get(tenant_id)
    if not tenant:
        raise APIError(
            code="NOT_FOUND",
            message=f"Tenant {tenant_id} not found",
            status_code=404
        )
    
    return Envelope(
        ok=True,
        data=TenantResponse(
            id=str(tenant.id),
            name=tenant.name,
            slug=tenant.slug,
            timezone=tenant.timezone,
            default_language=tenant.default_language,
            features=tenant.features or {},
            created_at=tenant.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.patch("/{tenant_id}")
async def update_tenant(
    request: TenantUpdate,
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """PATCH /tenants/{tenant_id}."""
    request_id = request_id_var.get() or "unknown"
    
    repo = TenantRepository(db)
    tenant = repo.get(tenant_id)
    if not tenant:
        raise APIError(
            code="NOT_FOUND",
            message=f"Tenant {tenant_id} not found",
            status_code=404
        )
    
    # Update fields
    if request.name is not None:
        tenant.name = request.name
    if request.slug is not None:
        # Check slug uniqueness
        existing = repo.get_by_slug(request.slug)
        if existing and existing.id != tenant.id:
            raise APIError(
                code="CONFLICT",
                message=f"Tenant with slug '{request.slug}' already exists",
                status_code=409
            )
        tenant.slug = request.slug
    if request.timezone is not None:
        tenant.timezone = request.timezone
    if request.default_language is not None:
        tenant.default_language = request.default_language
    if request.features is not None:
        tenant.features = request.features
    
    tenant = repo.update(tenant)
    
    return Envelope(
        ok=True,
        data=TenantResponse(
            id=str(tenant.id),
            name=tenant.name,
            slug=tenant.slug,
            timezone=tenant.timezone,
            default_language=tenant.default_language,
            features=tenant.features or {},
            created_at=tenant.created_at.isoformat() + "Z"
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

