"""UI configuration."""
import os
from typing import Optional

def get_api_base_url() -> str:
    """
    Get API base URL from environment or default.
    
    Priority:
    1. STREAMLIT_API_BASE_URL environment variable (preferred for UI)
    2. API_BASE_URL environment variable (fallback, common name)
    3. Default to localhost for local development
    """
    # Check for STREAMLIT_API_BASE_URL first (preferred)
    api_url = os.getenv("STREAMLIT_API_BASE_URL")
    if api_url:
        return api_url.rstrip('/')  # Remove trailing slash if present
    
    # Fallback to API_BASE_URL (common name)
    api_url = os.getenv("API_BASE_URL")
    if api_url:
        return api_url.rstrip('/')  # Remove trailing slash if present
    
    # Default for local development
    return "http://localhost:8000"

API_BASE_URL = get_api_base_url()

