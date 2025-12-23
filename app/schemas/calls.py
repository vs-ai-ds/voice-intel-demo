"""Call schemas per API_CONTRACTS.md."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class CallCreate(BaseModel):
    """POST /tenants/{tenant_id}/calls request."""
    provider: str = Field(..., description="Provider name")
    provider_call_id: str = Field(..., description="Provider call ID")
    from_phone: str = Field(..., description="From phone number")
    to_phone: str = Field(..., description="To phone number")
    direction: str = Field(..., description="Call direction")
    agent_id: str = Field(..., description="Agent ID")
    locale_hint: Optional[str] = Field(None, description="Locale hint")

class CallListItem(BaseModel):
    """Call item in list response."""
    id: str = Field(..., description="Call ID")
    provider_call_id: Optional[str] = Field(None, description="Provider call ID")
    from_phone: Optional[str] = Field(None, description="From phone number")
    status: str = Field(..., description="Call status")
    started_at: str = Field(..., description="ISO timestamp")
    ended_at: Optional[str] = Field(None, description="ISO timestamp")
    duration_sec: Optional[int] = Field(None, description="Duration in seconds")
    language: Optional[str] = Field(None, description="Language")
    handoff: Optional[Dict[str, Any]] = Field(None, description="Handoff info")

class CallDetail(BaseModel):
    """Call detail response."""
    id: str = Field(..., description="Call ID")
    agent_id: Optional[str] = Field(None, description="Agent ID")
    status: str = Field(..., description="Call status")
    from_phone: Optional[str] = Field(None, description="From phone number")
    language: Optional[str] = Field(None, description="Language")
    summary: Optional[Dict[str, Any]] = Field(None, description="Call summary")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Call metrics")

class CallResponse(BaseModel):
    """POST /tenants/{tenant_id}/calls response data."""
    id: str = Field(..., description="Call ID")
    tenant_id: str = Field(..., description="Tenant ID")
    provider: str = Field(..., description="Provider name")
    provider_call_id: str = Field(..., description="Provider call ID")
    from_phone: str = Field(..., description="From phone number")
    to_phone: str = Field(..., description="To phone number")
    direction: str = Field(..., description="Call direction")
    agent_id: str = Field(..., description="Agent ID")
    status: str = Field(..., description="Call status")
    started_at: str = Field(..., description="ISO timestamp")

