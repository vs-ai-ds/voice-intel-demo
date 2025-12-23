"""UI configuration."""
import os
from typing import Optional

def get_api_base_url() -> str:
    """Get API base URL from environment or default."""
    return os.getenv("STREAMLIT_API_BASE_URL", "http://localhost:8000")

API_BASE_URL = get_api_base_url()

