"""FastAPI dependencies for database, auth, and tenant context."""
from typing import Optional
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.tenant import Tenant
from app.core.errors import APIError

def get_database() -> Session:
    """Dependency for database session."""
    return Depends(get_db)

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    from app.services.auth import AuthService
    
    if not authorization or not authorization.startswith("Bearer "):
        raise APIError(
            code="UNAUTHORIZED",
            message="Missing or invalid authorization header",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    return auth_service.get_current_user(token)

async def get_tenant_context(
    tenant_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
) -> Tenant:
    """Get tenant and verify access."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise APIError(
            code="NOT_FOUND",
            message=f"Tenant {tenant_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Verify user has access to this tenant
    if current_user and current_user.tenant_id != tenant.id:
        raise APIError(
            code="FORBIDDEN",
            message="Access denied to this tenant",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    return tenant

async def get_tenant_from_header(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-Id"),
    db: Session = Depends(get_db)
) -> Optional[Tenant]:
    """Get tenant from X-Tenant-Id header if present."""
    if not x_tenant_id:
        return None
    
    tenant = db.query(Tenant).filter(Tenant.id == x_tenant_id).first()
    return tenant

