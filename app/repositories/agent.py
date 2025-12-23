"""Agent repository."""
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.agent import Agent
from app.repositories.base import BaseRepository

class AgentRepository(BaseRepository[Agent]):
    """Repository for agent operations."""
    
    def __init__(self, db: Session):
        super().__init__(Agent, db)
    
    def get_by_tenant(self, tenant_id: UUID, agent_id: UUID) -> Optional[Agent]:
        """Get agent by tenant and agent ID (tenant-scoped)."""
        return self.db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.tenant_id == tenant_id
        ).first()
    
    def list_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agent]:
        """List agents by tenant."""
        return self.db.query(Agent).filter(
            Agent.tenant_id == tenant_id
        ).order_by(Agent.created_at.desc()).offset(skip).limit(limit).all()

