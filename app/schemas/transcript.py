"""Transcript schemas per API_CONTRACTS.md."""
from typing import Optional
from pydantic import BaseModel, Field

class TurnItem(BaseModel):
    """Turn item in transcript."""
    turn_id: str = Field(..., description="Turn ID")
    speaker: str = Field(..., description="Speaker (USER/ASSISTANT)")
    text: str = Field(..., description="Turn text")
    language: Optional[str] = Field(None, description="Language")
    ts: str = Field(..., description="ISO timestamp")
    confidence: Optional[float] = Field(None, description="Confidence score")

class TranscriptResponse(BaseModel):
    """GET /tenants/{tenant_id}/calls/{call_id}/transcript response data."""
    call_id: str = Field(..., description="Call ID")
    turns: list[TurnItem] = Field(..., description="Ordered turns")

