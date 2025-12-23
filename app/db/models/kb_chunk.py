"""Knowledge Base Chunk model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from app.db.base import Base

class KBChunk(Base):
    """Knowledge Base chunk model with embedding."""
    __tablename__ = "kb_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("kb_documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)  # Order within document
    text = Column(String, nullable=False)
    embedding = Column(Vector(384))  # Using 384-dim vectors (sentence-transformers default)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    document = relationship("KBDocument", backref="chunks")
    
    __table_args__ = (
        Index("idx_kb_chunks_doc", "document_id", "chunk_index"),
        # Note: Vector index created in migration, not here (Alembic handles it)
    )

