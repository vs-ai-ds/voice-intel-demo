"""Agent schemas per API_CONTRACTS.md."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentCreate(BaseModel):
    """POST /tenants/{tenant_id}/agents request."""
    name: str = Field(..., description="Agent name")
    status: str = Field("ACTIVE", description="Agent status")
    languages: List[str] = Field(default_factory=list, description="Supported languages")
    voice: Dict[str, Any] = Field(default_factory=dict, description="Voice configuration")
    stt: Dict[str, Any] = Field(default_factory=dict, description="STT configuration")
    llm: Dict[str, Any] = Field(default_factory=dict, description="LLM configuration")
    routing: Dict[str, Any] = Field(default_factory=dict, description="Routing configuration")
    policies: Dict[str, Any] = Field(default_factory=dict, description="Policies")
    tools_enabled: List[str] = Field(default_factory=list, description="Enabled tools")

class AgentUpdate(BaseModel):
    """PATCH /tenants/{tenant_id}/agents/{agent_id} request."""
    name: Optional[str] = None
    status: Optional[str] = None
    languages: Optional[List[str]] = None
    voice: Optional[Dict[str, Any]] = None
    stt: Optional[Dict[str, Any]] = None
    llm: Optional[Dict[str, Any]] = None
    routing: Optional[Dict[str, Any]] = None
    policies: Optional[Dict[str, Any]] = None
    tools_enabled: Optional[List[str]] = None

class AgentResponse(BaseModel):
    """Agent response data."""
    id: str = Field(..., description="Agent ID")
    tenant_id: str = Field(..., description="Tenant ID")
    name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Agent status")
    languages: List[str] = Field(..., description="Supported languages")
    voice: Dict[str, Any] = Field(..., description="Voice configuration")
    stt: Dict[str, Any] = Field(..., description="STT configuration")
    llm: Dict[str, Any] = Field(..., description="LLM configuration")
    routing: Dict[str, Any] = Field(..., description="Routing configuration")
    policies: Dict[str, Any] = Field(..., description="Policies")
    tools_enabled: List[str] = Field(..., description="Enabled tools")
    created_at: str = Field(..., description="ISO timestamp")

