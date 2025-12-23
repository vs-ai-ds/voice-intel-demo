"""KB endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from typing import Optional
from app.db.session import get_db
from app.schemas.kb import (
    KBDocumentCreate, KBDocumentResponse, KBDocumentListItem,
    KBSearchRequest, KBSearchResponse, KBSearchHit
)
from app.schemas.common import Envelope, PaginatedEnvelope, Meta, PaginationMeta
from app.services.kb_service import KBService
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants/{tenant_id}/kb", tags=["kb"])

@router.post("/documents")
async def create_document(
    request: KBDocumentCreate,
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """POST /tenants/{tenant_id}/kb/documents - Ingest document."""
    request_id = request_id_var.get() or "unknown"
    
    service = KBService(db)
    document = service.ingest_document(
        tenant_id=tenant_id,
        source_type=request.source_type,
        title=request.title,
        content=request.content or "",
        tags=request.tags or []
    )
    
    # Count chunks - reload document to get chunks relationship
    db.refresh(document)
    chunks_count = len(document.chunks) if document.chunks else 0
    
    return Envelope(
        ok=True,
        data=KBDocumentResponse(
            document_id=str(document.id),
            status=document.status,
            chunks_created=chunks_count
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("/documents")
async def list_documents(
    tenant_id: UUID = Path(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/kb/documents - List documents."""
    request_id = request_id_var.get() or "unknown"
    
    service = KBService(db)
    repo = service.kb_repo
    
    skip = (page - 1) * page_size
    documents, total = repo.list_documents_by_tenant(tenant_id, skip=skip, limit=page_size)
    
    has_more = (skip + len(documents)) < total
    
    return PaginatedEnvelope(
        ok=True,
        data=[
            KBDocumentListItem(
                document_id=str(d.id),
                title=d.title,
                source_type=d.source_type or "TEXT",
                tags=d.tags or [],
                status=d.status,
                created_at=d.created_at.isoformat() + "Z"
            ).model_dump()
            for d in documents
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

@router.post("/search")
async def search(
    request: KBSearchRequest,
    tenant_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """POST /tenants/{tenant_id}/kb/search - Semantic search."""
    request_id = request_id_var.get() or "unknown"
    
    service = KBService(db)
    results = service.search(
        tenant_id=tenant_id,
        query=request.query,
        top_k=request.top_k,
        filters=request.filters
    )
    
    # Build response
    hits = []
    for chunk, score in results:
        hits.append(
            KBSearchHit(
                chunk_id=str(chunk.id),
                score=round(score, 2),  # Round to 2 decimal places
                text=chunk.text,
                document={
                    "document_id": str(chunk.document.id),
                    "title": chunk.document.title
                }
            ).model_dump()
        )
    
    return Envelope(
        ok=True,
        data=KBSearchResponse(hits=hits).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

