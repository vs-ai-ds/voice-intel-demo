"""Base repository with common CRUD operations."""
from typing import Generic, TypeVar, Optional, List, Type
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository with common operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: UUID) -> Optional[ModelType]:
        """Get by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get multiple with pagination."""
        query = self.db.query(self.model)
        if order_by:
            query = query.order_by(desc(getattr(self.model, order_by)))
        return query.offset(skip).limit(limit).all()
    
    def create(self, obj: ModelType) -> ModelType:
        """Create new record."""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: ModelType) -> ModelType:
        """Update existing record."""
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: UUID) -> bool:
        """Delete by ID."""
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

