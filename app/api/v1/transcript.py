"""Transcript endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from app.db.session import get_db
from app.schemas.transcript import TranscriptResponse, TurnItem
from app.schemas.common import Envelope, Meta
from app.repositories.call import CallRepository
from app.repositories.turn import TurnRepository
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/tenants/{tenant_id}/calls/{call_id}/transcript", tags=["transcript"])

@router.get("")
async def get_transcript(
    tenant_id: UUID = Path(...),
    call_id: UUID = Path(...),
    db: Session = Depends(get_db)
):
    """GET /tenants/{tenant_id}/calls/{call_id}/transcript."""
    request_id = request_id_var.get() or "unknown"
    
    # Verify call exists and belongs to tenant
    call_repo = CallRepository(db)
    call = call_repo.get_by_tenant(tenant_id, call_id)
    if not call:
        raise APIError(
            code="NOT_FOUND",
            message=f"Call {call_id} not found in tenant {tenant_id}",
            status_code=404
        )
    
    # Get turns
    turn_repo = TurnRepository(db)
    turns = turn_repo.get_by_call(call_id)
    
    return Envelope(
        ok=True,
        data=TranscriptResponse(
            call_id=str(call_id),
            turns=[
                TurnItem(
                    turn_id=t.turn_id or str(t.id),
                    speaker=t.speaker,
                    text=t.text,
                    language=t.language,
                    ts=t.ts.isoformat() + "Z",
                    confidence=t.confidence
                ).model_dump()
                for t in turns
            ]
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

