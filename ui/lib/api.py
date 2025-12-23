"""API client wrapper for backend API calls."""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List
from lib.config import API_BASE_URL
from lib.state import ACCESS_TOKEN, REFRESH_TOKEN, init_session_state

class APIError(Exception):
    """API error exception."""
    def __init__(self, message: str, code: str = None, status_code: int = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

def request(
    method: str,
    path: str,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make API request with authentication.
    
    Args:
        method: HTTP method (GET, POST, PATCH, etc.)
        path: API path (e.g., "/api/v1/auth/login")
        json: Request body (for POST/PATCH)
        params: Query parameters
        headers: Additional headers
    
    Returns:
        Response data from API envelope
    """
    init_session_state()
    
    # Build URL
    url = f"{API_BASE_URL}{path}"
    
    # Build headers
    request_headers = headers or {}
    if st.session_state.get(ACCESS_TOKEN):
        request_headers["Authorization"] = f"Bearer {st.session_state[ACCESS_TOKEN]}"
    
    # Make request
    try:
        response = requests.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=request_headers,
            timeout=30
        )
        
        # Handle 401 - unauthorized
        if response.status_code == 401:
            st.session_state[ACCESS_TOKEN] = None
            st.session_state[REFRESH_TOKEN] = None
            raise APIError(
                message="Unauthorized. Please login again.",
                code="UNAUTHORIZED",
                status_code=401
            )
        
        # Parse response
        if response.status_code == 204:
            return {}
        
        data = response.json()
        
        # Check for error envelope
        if not data.get("ok", True):
            error = data.get("error", {})
            raise APIError(
                message=error.get("message", "API error"),
                code=error.get("code"),
                status_code=response.status_code
            )
        
        # For paginated responses, return full structure (data + meta)
        # For single responses, return just data
        response_data = data.get("data", data)
        if isinstance(response_data, list) and "meta" in data:
            # Paginated response - return dict with data and meta
            return {
                "data": response_data,
                "meta": data.get("meta", {})
            }
        
        # Single response - return just data
        return response_data
        
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}")
    except ValueError as e:
        raise APIError(f"Invalid JSON response: {str(e)}")

# Auth methods
def login(email: str, password: str) -> Dict[str, Any]:
    """POST /api/v1/auth/login"""
    return request("POST", "/api/v1/auth/login", json={"email": email, "password": password})

def get_current_user() -> Dict[str, Any]:
    """GET /api/v1/users/me"""
    return request("GET", "/api/v1/users/me")

def logout(refresh_token: str) -> Dict[str, Any]:
    """POST /api/v1/auth/logout"""
    return request("POST", "/api/v1/auth/logout", json={"refresh_token": refresh_token})

# Tenant methods
def list_tenants(page: int = 1, page_size: int = 25) -> Dict[str, Any]:
    """GET /api/v1/tenants - Returns paginated envelope with data array and meta"""
    result = request("GET", "/api/v1/tenants", params={"page": page, "page_size": page_size})
    # For paginated endpoints, the full response includes data array and meta
    # But request() already extracts data, so we need to handle this differently
    # Actually, paginated responses have data as array, so result should be the full envelope
    # Let me check the actual response structure...
    return result

def create_tenant(data: Dict[str, Any]) -> Dict[str, Any]:
    """POST /api/v1/tenants"""
    return request("POST", "/api/v1/tenants", json=data)

def get_tenant(tenant_id: str) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}"""
    return request("GET", f"/api/v1/tenants/{tenant_id}")

# Agent methods
def list_agents(tenant_id: str, page: int = 1, page_size: int = 25) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}/agents"""
    return request("GET", f"/api/v1/tenants/{tenant_id}/agents", params={"page": page, "page_size": page_size})

def create_agent(tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """POST /api/v1/tenants/{tenant_id}/agents"""
    return request("POST", f"/api/v1/tenants/{tenant_id}/agents", json=data)

def get_agent(tenant_id: str, agent_id: str) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}/agents/{agent_id}"""
    return request("GET", f"/api/v1/tenants/{tenant_id}/agents/{agent_id}")

def update_agent(tenant_id: str, agent_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """PATCH /api/v1/tenants/{tenant_id}/agents/{agent_id}"""
    return request("PATCH", f"/api/v1/tenants/{tenant_id}/agents/{agent_id}", json=data)

# Call methods
def list_calls(
    tenant_id: str,
    page: int = 1,
    page_size: int = 25,
    status: Optional[str] = None,
    from_phone: Optional[str] = None,
    to_phone: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}/calls"""
    params = {"page": page, "page_size": page_size}
    if status:
        params["status"] = status
    if from_phone:
        params["from_phone"] = from_phone
    if to_phone:
        params["to_phone"] = to_phone
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    return request("GET", f"/api/v1/tenants/{tenant_id}/calls", params=params)

def create_call(tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """POST /api/v1/tenants/{tenant_id}/calls"""
    return request("POST", f"/api/v1/tenants/{tenant_id}/calls", json=data)

def get_call(tenant_id: str, call_id: str) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}/calls/{call_id}"""
    return request("GET", f"/api/v1/tenants/{tenant_id}/calls/{call_id}")

# Transcript methods
def get_transcript(tenant_id: str, call_id: str) -> Dict[str, Any]:
    """GET /api/v1/tenants/{tenant_id}/calls/{call_id}/transcript"""
    return request("GET", f"/api/v1/tenants/{tenant_id}/calls/{call_id}/transcript")

# Event methods
def post_event(tenant_id: str, call_id: str, data: Dict[str, Any], correlation_id: Optional[str] = None) -> Dict[str, Any]:
    """POST /api/v1/tenants/{tenant_id}/calls/{call_id}/events"""
    headers = {}
    if correlation_id:
        headers["X-Correlation-ID"] = correlation_id
    return request("POST", f"/api/v1/tenants/{tenant_id}/calls/{call_id}/events", json=data, headers=headers)

