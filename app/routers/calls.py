"""
API routes for call management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.services.calls import CallService

router = APIRouter()

@router.post("/")
async def create_call(
    scenario: str = "order_inquiry",
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Create a new call."""
    service = CallService(db)
    call = await service.create_call(scenario, language)
    return call

@router.get("/")
async def list_calls(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all calls."""
    service = CallService(db)
    calls = await service.get_calls(limit=limit)
    return {"calls": calls}

@router.get("/{call_id}")
async def get_call(
    call_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific call."""
    service = CallService(db)
    call = await service.get_call(call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.post("/{call_id}/segments")
async def add_segment(
    call_id: str,
    t_ms: int,
    speaker: str,
    text: str,
    db: Session = Depends(get_db)
):
    """Add a segment to a call."""
    service = CallService(db)
    await service.add_segment(call_id, t_ms, speaker, text)
    return {"status": "ok"}

@router.post("/{call_id}/end")
async def end_call(
    call_id: str,
    db: Session = Depends(get_db)
):
    """End a call and generate summary."""
    service = CallService(db)
    result = await service.end_call(call_id)
    return result

@router.get("/search/{query}")
async def search_calls(
    query: str,
    db: Session = Depends(get_db)
):
    """Search calls by keyword."""
    service = CallService(db)
    calls = await service.search_calls(query)
    return {"calls": calls}

