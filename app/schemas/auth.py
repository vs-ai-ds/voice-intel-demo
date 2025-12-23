"""Auth schemas per API_CONTRACTS.md."""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """POST /auth/login request."""
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    """POST /auth/refresh request."""
    refresh_token: str

class LogoutRequest(BaseModel):
    """POST /auth/logout request."""
    refresh_token: str

class UserResponse(BaseModel):
    """User data in auth responses."""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    roles: List[str] = Field(default_factory=list, description="User roles")
    tenant_id: str = Field(..., description="Tenant ID")

class LoginResponse(BaseModel):
    """POST /auth/login response data."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(3600, description="Token expiration in seconds")
    user: UserResponse = Field(..., description="User data")

class LogoutResponse(BaseModel):
    """POST /auth/logout response data."""
    revoked: bool = Field(True, description="Token revoked")

