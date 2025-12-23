"""Call repository."""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID
from app.db.models.call import Call
from app.repositories.base import BaseRepository

class CallRepository(BaseRepository[Call]):
    """Repository for call operations."""
    
    def __init__(self, db: Session):
        super().__init__(Call, db)
    
    def get_by_tenant(self, tenant_id: UUID, call_id: UUID) -> Optional[Call]:
        """Get call by tenant and call ID (tenant-scoped)."""
        return self.db.query(Call).filter(
            Call.id == call_id,
            Call.tenant_id == tenant_id
        ).first()
    
    def list_by_tenant(
        self,
        tenant_id: UUID,
        status: Optional[str] = None,
        from_phone: Optional[str] = None,
        to_phone: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Call], int]:
        """List calls by tenant with filters."""
        query = self.db.query(Call).filter(Call.tenant_id == tenant_id)
        
        if status:
            query = query.filter(Call.status == status)
        if from_phone:
            query = query.filter(Call.from_phone == from_phone)
        if to_phone:
            query = query.filter(Call.to_phone == to_phone)
        if date_from:
            query = query.filter(Call.started_at >= date_from)
        if date_to:
            query = query.filter(Call.started_at <= date_to)
        
        total = query.count()
        calls = query.order_by(Call.started_at.desc()).offset(skip).limit(limit).all()
        
        return calls, total

