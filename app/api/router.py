"""Main API router that includes all v1 routers."""
from fastapi import APIRouter
from app.api.v1 import health, auth, tenants, agents, calls, transcript, events, kb

api_router = APIRouter()

# Include all v1 routers
api_router.include_router(health.router, prefix="/api/v1")
api_router.include_router(auth.router, prefix="/api/v1")
api_router.include_router(tenants.router, prefix="/api/v1")
api_router.include_router(agents.router, prefix="/api/v1")
api_router.include_router(calls.router, prefix="/api/v1")
api_router.include_router(transcript.router, prefix="/api/v1")
api_router.include_router(events.router, prefix="/api/v1")
api_router.include_router(kb.router, prefix="/api/v1")

