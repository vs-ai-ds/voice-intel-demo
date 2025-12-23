"""
Application settings and configuration.
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost/voice_intel"
    
    # LLM Provider
    llm_provider: str = "mock"  # Options: "mock", "openai", etc.
    openai_api_key: Optional[str] = None
    
    # Application
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

