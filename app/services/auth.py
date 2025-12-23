"""Auth service."""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.db.models.user import User
from app.core.errors import APIError
from app.schemas.auth import LoginResponse, UserResponse
import jwt

# Demo JWT secret - in production use env var
JWT_SECRET = "demo-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 3600  # 1 hour
REFRESH_TOKEN_EXPIRE = 86400 * 7  # 7 days

class AuthService:
    """Authentication service."""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.db = db
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verify password (demo: simple comparison)."""
        # For Phase 1 demo: simple hash comparison
        # In production: use bcrypt or similar
        return hashlib.sha256(plain.encode()).hexdigest() == hashed
    
    def hash_password(self, password: str) -> str:
        """Hash password (demo)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_token(self, user_id: str, expires_delta: int) -> str:
        """Create JWT token."""
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return user_id."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise APIError(
                    code="UNAUTHORIZED",
                    message="Invalid token payload",
                    status_code=401
                )
            return user_id
        except jwt.ExpiredSignatureError:
            raise APIError(
                code="UNAUTHORIZED",
                message="Token expired",
                status_code=401
            )
        except jwt.InvalidTokenError:
            raise APIError(
                code="UNAUTHORIZED",
                message="Invalid token",
                status_code=401
            )
    
    def login(self, email: str, password: str) -> LoginResponse:
        """Authenticate user and return tokens."""
        user = self.user_repo.get_by_email(email)
        if not user:
            raise APIError(
                code="UNAUTHORIZED",
                message="Invalid email or password",
                status_code=401
            )
        
        # For demo: accept any password if user has no hash, or verify hash
        if user.password_hash:
            if not self.verify_password(password, user.password_hash):
                raise APIError(
                    code="UNAUTHORIZED",
                    message="Invalid email or password",
                    status_code=401
                )
        # Demo mode: allow login without password hash
        
        access_token = self.create_token(str(user.id), ACCESS_TOKEN_EXPIRE)
        refresh_token = self.create_token(str(user.id), REFRESH_TOKEN_EXPIRE)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                roles=user.roles or [],
                tenant_id=str(user.tenant_id)
            )
        )
    
    def refresh(self, refresh_token: str) -> LoginResponse:
        """Refresh access token."""
        user_id = self.verify_token(refresh_token)
        user = self.user_repo.get(user_id)
        if not user:
            raise APIError(
                code="UNAUTHORIZED",
                message="User not found",
                status_code=401
            )
        
        access_token = self.create_token(str(user.id), ACCESS_TOKEN_EXPIRE)
        new_refresh_token = self.create_token(str(user.id), REFRESH_TOKEN_EXPIRE)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                roles=user.roles or [],
                tenant_id=str(user.tenant_id)
            )
        )
    
    def get_current_user(self, token: str) -> User:
        """Get current user from token."""
        from uuid import UUID
        user_id = self.verify_token(token)
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise APIError(
                code="UNAUTHORIZED",
                message="Invalid user ID in token",
                status_code=401
            )
        user = self.user_repo.get(user_uuid)
        if not user:
            raise APIError(
                code="UNAUTHORIZED",
                message="User not found",
                status_code=401
            )
        return user

