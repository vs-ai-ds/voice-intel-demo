"""Health and version endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter
from datetime import datetime
from app.schemas.common import Envelope, Meta
from app.core.logging import request_id_var

router = APIRouter()

@router.get("/health", tags=["health"])
async def health():
    """GET /health endpoint."""
    request_id = request_id_var.get() or "unknown"
    
    return Envelope(
        ok=True,
        data={
            "status": "healthy",
            "components": {
                "db": "ok",
                "redis": "ok",
                "llm": "ok"
            }
        },
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("/version", tags=["health"])
async def version():
    """GET /version endpoint."""
    request_id = request_id_var.get() or "unknown"
    
    return Envelope(
        ok=True,
        data={
            "service": "voice-intel-demo",
            "version": "0.1.0",
            "git_sha": "abc123"
        },
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

