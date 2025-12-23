"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database (required)
    DATABASE_URL: str = "postgresql://user:password@localhost/voice_intel"
    
    # Application
    DEBUG: bool = False
    
    # LLM Provider (optional for Phase 1)
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()

