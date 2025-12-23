"""Event schemas per API_CONTRACTS.md."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    """POST /tenants/{tenant_id}/calls/{call_id}/events request."""
    type: str = Field(..., description="Event type")
    correlation_id: Optional[str] = Field(None, description="Correlation ID")
    payload: Dict[str, Any] = Field(..., description="Event payload")

class EventStoredResponse(BaseModel):
    """POST /tenants/{tenant_id}/calls/{call_id}/events response data."""
    stored: bool = Field(True, description="Event stored")

