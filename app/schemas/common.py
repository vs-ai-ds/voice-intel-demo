"""Common schemas for API envelope and pagination."""
from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class Meta(BaseModel):
    """Response metadata per API_CONTRACTS.md."""
    request_id: str = Field(..., description="Request ID")
    timestamp: str = Field(..., description="ISO timestamp")

class PaginationMeta(Meta):
    """Pagination metadata per API_CONTRACTS.md."""
    page: int = Field(..., ge=1, description="Current page (1-based)")
    page_size: int = Field(..., ge=1, le=200, description="Page size")
    total: int = Field(..., ge=0, description="Total count")
    has_more: bool = Field(..., description="Whether more pages exist")

class Envelope(BaseModel, Generic[T]):
    """Standard success response envelope per API_CONTRACTS.md."""
    ok: bool = Field(True, description="Success indicator")
    data: T = Field(..., description="Response data")
    meta: Meta = Field(..., description="Response metadata")

class PaginatedEnvelope(BaseModel, Generic[T]):
    """Paginated response envelope per API_CONTRACTS.md."""
    ok: bool = Field(True, description="Success indicator")
    data: List[T] = Field(..., description="Response data list")
    meta: PaginationMeta = Field(..., description="Pagination metadata")

class ErrorDetail(BaseModel):
    """Error detail per API_CONTRACTS.md."""
    field: Optional[str] = Field(None, description="Field name if applicable")
    reason: str = Field(..., description="Error reason")

class ErrorEnvelope(BaseModel):
    """Error response envelope per API_CONTRACTS.md."""
    ok: bool = Field(False, description="Error indicator")
    error: Dict[str, Any] = Field(..., description="Error details")
    meta: Meta = Field(..., description="Response metadata")

