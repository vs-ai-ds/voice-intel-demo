"""User repository."""
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for user operations."""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_tenant(self, tenant_id: UUID) -> list[User]:
        """Get users by tenant."""
        return self.db.query(User).filter(User.tenant_id == tenant_id).all()

