"""Turn repository."""
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.turn import Turn

class TurnRepository:
    """Repository for turn operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_call(self, call_id: UUID) -> List[Turn]:
        """Get all turns for a call, ordered by sequence."""
        return self.db.query(Turn).filter(
            Turn.call_id == call_id
        ).order_by(Turn.seq_num.asc(), Turn.ts.asc()).all()

