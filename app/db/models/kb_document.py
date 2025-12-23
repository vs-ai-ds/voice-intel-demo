"""Knowledge Base Document model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class KBDocument(Base):
    """Knowledge Base document model."""
    __tablename__ = "kb_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    source_type = Column(String)  # "TEXT", "URL", "FILE"
    title = Column(String, nullable=False)
    tags = Column(ARRAY(String), default=list)
    content = Column(String)  # Full content
    status = Column(String, default="PENDING")  # PENDING, INGESTED, FAILED
    doc_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", backref="kb_documents")
    
    __table_args__ = (
        Index("idx_kb_docs_tenant", "tenant_id"),
    )

