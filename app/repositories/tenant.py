"""Tenant repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.tenant import Tenant
from app.repositories.base import BaseRepository

class TenantRepository(BaseRepository[Tenant]):
    """Repository for tenant operations."""
    
    def __init__(self, db: Session):
        super().__init__(Tenant, db)
    
    def get_by_slug(self, slug: str) -> Optional[Tenant]:
        """Get tenant by slug."""
        return self.db.query(Tenant).filter(Tenant.slug == slug).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[Tenant]:
        """List all tenants with pagination."""
        return self.get_multi(skip=skip, limit=limit, order_by="created_at")

