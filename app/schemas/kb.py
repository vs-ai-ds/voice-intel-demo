"""KB schemas matching API_CONTRACTS.md exactly."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class KBDocumentCreate(BaseModel):
    """POST /tenants/{tenant_id}/kb/documents request."""
    source_type: str = Field(..., description="TEXT, URL, or FILE")
    title: str
    tags: Optional[List[str]] = Field(default_factory=list)
    content: Optional[str] = None

class KBDocumentResponse(BaseModel):
    """POST /tenants/{tenant_id}/kb/documents response."""
    document_id: str
    status: str  # INGESTED, PENDING, FAILED
    chunks_created: int

class KBDocumentListItem(BaseModel):
    """List item for GET /tenants/{tenant_id}/kb/documents."""
    document_id: str
    title: str
    source_type: str
    tags: List[str]
    status: str
    created_at: str

class KBSearchRequest(BaseModel):
    """POST /tenants/{tenant_id}/kb/search request."""
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class KBSearchHit(BaseModel):
    """Search hit in response."""
    chunk_id: str
    score: float  # Similarity score (higher is better)
    text: str
    document: Dict[str, str]  # {"document_id": "...", "title": "..."}

class KBSearchResponse(BaseModel):
    """POST /tenants/{tenant_id}/kb/search response."""
    hits: List[KBSearchHit]

