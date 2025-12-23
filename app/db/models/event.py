"""Event model for observability."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Event(Base):
    """Append-only event log for observability and replay."""
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=True)
    type = Column(String, nullable=False)  # "TOOL_CALL", "segment_received", "summary_generated", etc.
    correlation_id = Column(String)  # For correlating related events
    payload = Column(JSON, nullable=False)  # Event payload
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    call = relationship("Call", backref="events")
    
    __table_args__ = (
        Index("idx_events_call_created", "call_id", "created_at"),
        Index("idx_events_type", "type"),
    )

