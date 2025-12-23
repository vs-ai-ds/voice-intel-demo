"""Call model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Call(Base):
    """Call session model."""
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    provider = Column(String)  # "twilio", "simulated"
    provider_call_id = Column(String)  # External provider's call ID
    from_phone = Column(String)
    to_phone = Column(String)
    direction = Column(String)  # "INBOUND", "OUTBOUND"
    status = Column(String, default="INITIATED")  # INITIATED, IN_PROGRESS, COMPLETED, FAILED
    language = Column(String)  # Detected language
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    call_metadata = Column(JSON, default=dict)  # Additional metadata
    summary = Column(JSON, nullable=True)  # {"intent": "...", "entities": {...}, "resolution": "..."}
    metrics = Column(JSON, nullable=True)  # {"llm_tokens_in": 1200, "latency_ms": {...}}
    handoff = Column(JSON, nullable=True)  # {"occurred": false}
    
    tenant = relationship("Tenant", backref="calls")
    agent = relationship("Agent", backref="calls")
    
    __table_args__ = (
        Index("idx_calls_tenant_started", "tenant_id", "started_at"),
        Index("idx_calls_status", "status"),
    )

