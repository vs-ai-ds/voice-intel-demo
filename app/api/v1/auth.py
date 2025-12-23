"""Auth endpoints per API_CONTRACTS.md."""
from fastapi import APIRouter, Depends, Header
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest, RefreshRequest, LogoutRequest,
    LoginResponse, UserResponse, LogoutResponse
)
from app.schemas.common import Envelope, Meta
from app.services.auth import AuthService
from app.core.logging import request_id_var
from app.core.errors import APIError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """POST /auth/login."""
    request_id = request_id_var.get() or "unknown"
    
    auth_service = AuthService(db)
    login_response = auth_service.login(request.email, request.password)
    
    return Envelope(
        ok=True,
        data=login_response.model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.post("/refresh")
async def refresh(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    """POST /auth/refresh."""
    request_id = request_id_var.get() or "unknown"
    
    auth_service = AuthService(db)
    login_response = auth_service.refresh(request.refresh_token)
    
    return Envelope(
        ok=True,
        data=login_response.model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.post("/logout")
async def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db)
):
    """POST /auth/logout."""
    request_id = request_id_var.get() or "unknown"
    
    # For Phase 1: simple acknowledgment
    # In production: invalidate refresh token in DB/Redis
    
    return Envelope(
        ok=True,
        data=LogoutResponse(revoked=True).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

@router.get("/users/me")
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """GET /users/me."""
    request_id = request_id_var.get() or "unknown"
    
    if not authorization or not authorization.startswith("Bearer "):
        raise APIError(
            code="UNAUTHORIZED",
            message="Missing or invalid authorization header",
            status_code=401
        )
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    user = auth_service.get_current_user(token)
    
    return Envelope(
        ok=True,
        data=UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            roles=user.roles or [],
            tenant_id=str(user.tenant_id)
        ).model_dump(),
        meta=Meta(
            request_id=request_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    ).model_dump()

