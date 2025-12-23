"""Agent (Voice Bot) model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Agent(Base):
    """Agent (Voice Bot) configuration model."""
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")  # ACTIVE, INACTIVE, etc.
    languages = Column(ARRAY(String), default=list)  # ["hi-IN", "en-IN"]
    voice = Column(JSON, default=dict)  # {"provider": "google", "voice_id": "...", "speaking_rate": 1.0}
    stt = Column(JSON, default=dict)  # {"provider": "google", "model": "...", "punctuate": true}
    llm = Column(JSON, default=dict)  # {"provider": "openai", "model": "...", "temperature": 0.3}
    routing = Column(JSON, default=dict)  # {"human_transfer": {"enabled": true, ...}}
    policies = Column(JSON, default=dict)  # {"no_medical_advice": true, ...}
    tools_enabled = Column(ARRAY(String), default=list)  # ["woo.products.search", ...]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", backref="agents")
    
    __table_args__ = (
        Index("idx_agents_tenant_status", "tenant_id", "status"),
    )

