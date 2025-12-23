"""Embedding model for generic entity embeddings."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Embedding(Base):
    """Generic embedding storage for segments/summaries."""
    __tablename__ = "embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String, nullable=False)  # "segment", "summary", "turn"
    entity_id = Column(UUID(as_uuid=True), nullable=False)  # Reference to entity (no FK for flexibility)
    embedding = Column(Vector(384))  # 384-dim vector
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_embeddings_entity", "entity_type", "entity_id"),
        # Note: Vector index created in migration, not here (Alembic handles it)
    )

