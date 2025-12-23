"""Event repository."""
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models.event import Event

class EventRepository:
    """Repository for event operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event: Event) -> Event:
        """Create new event (append-only)."""
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def get_by_call(self, call_id: UUID) -> List[Event]:
        """Get all events for a call."""
        return self.db.query(Event).filter(
            Event.call_id == call_id
        ).order_by(Event.created_at.asc()).all()

