"""Turn (transcript) model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Turn(Base):
    """Turn model for call transcripts."""
    __tablename__ = "turns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    turn_id = Column(String, unique=True)  # External turn ID like "t_001"
    speaker = Column(String, nullable=False)  # "USER", "ASSISTANT", "CUSTOMER", "AGENT"
    text = Column(String, nullable=False)
    language = Column(String)  # Detected language
    ts = Column(DateTime, nullable=False)  # Timestamp
    confidence = Column(Float)  # STT confidence score
    seq_num = Column(Integer)  # Sequence number for ordering
    intent_label = Column(String)  # Intent classification
    sentiment_score = Column(Float)  # Sentiment score
    escalation_score = Column(Float)  # Escalation risk score
    flags = Column(JSON, default=dict)  # {"pii_detected": true, ...}
    raw_provider_payload = Column(JSON)  # Raw provider data
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    call = relationship("Call", backref="turns")
    
    __table_args__ = (
        Index("idx_turns_call_seq", "call_id", "seq_num"),
        Index("idx_turns_intent", "intent_label"),
    )

