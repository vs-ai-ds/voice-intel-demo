"""Tenant schemas per API_CONTRACTS.md."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TenantCreate(BaseModel):
    """POST /tenants request."""
    name: str = Field(..., description="Tenant name")
    slug: str = Field(..., description="Tenant slug")
    timezone: str = Field("UTC", description="Timezone")
    default_language: str = Field("en-US", description="Default language")
    features: Dict[str, Any] = Field(default_factory=dict, description="Feature flags")

class TenantUpdate(BaseModel):
    """PATCH /tenants/{tenant_id} request."""
    name: Optional[str] = None
    slug: Optional[str] = None
    timezone: Optional[str] = None
    default_language: Optional[str] = None
    features: Optional[Dict[str, Any]] = None

class TenantResponse(BaseModel):
    """Tenant response data."""
    id: str = Field(..., description="Tenant ID")
    name: str = Field(..., description="Tenant name")
    slug: str = Field(..., description="Tenant slug")
    timezone: str = Field(..., description="Timezone")
    default_language: str = Field(..., description="Default language")
    features: Dict[str, Any] = Field(..., description="Feature flags")
    created_at: str = Field(..., description="ISO timestamp")

