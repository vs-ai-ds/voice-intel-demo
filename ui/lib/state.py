"""Streamlit session state management."""
import streamlit as st
from typing import Optional

# State keys
ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
CURRENT_USER = "current_user"
SELECTED_TENANT_ID = "selected_tenant_id"
SELECTED_CALL_ID = "selected_call_id"

def init_session_state():
    """Initialize session state keys."""
    if ACCESS_TOKEN not in st.session_state:
        st.session_state[ACCESS_TOKEN] = None
    if REFRESH_TOKEN not in st.session_state:
        st.session_state[REFRESH_TOKEN] = None
    if CURRENT_USER not in st.session_state:
        st.session_state[CURRENT_USER] = None
    if SELECTED_TENANT_ID not in st.session_state:
        st.session_state[SELECTED_TENANT_ID] = None
    if SELECTED_CALL_ID not in st.session_state:
        st.session_state[SELECTED_CALL_ID] = None

def require_login() -> bool:
    """Check if user is logged in."""
    init_session_state()
    return st.session_state[ACCESS_TOKEN] is not None

def require_tenant() -> Optional[str]:
    """Check if tenant is selected, return tenant_id or None."""
    init_session_state()
    return st.session_state[SELECTED_TENANT_ID]

def require_call() -> Optional[str]:
    """Check if call is selected, return call_id or None."""
    init_session_state()
    return st.session_state[SELECTED_CALL_ID]

def set_tokens(access_token: str, refresh_token: str):
    """Set authentication tokens."""
    st.session_state[ACCESS_TOKEN] = access_token
    st.session_state[REFRESH_TOKEN] = refresh_token

def clear_auth():
    """Clear authentication state."""
    st.session_state[ACCESS_TOKEN] = None
    st.session_state[REFRESH_TOKEN] = None
    st.session_state[CURRENT_USER] = None
    st.session_state[SELECTED_TENANT_ID] = None
    st.session_state[SELECTED_CALL_ID] = None

def set_tenant(tenant_id: str):
    """Set selected tenant."""
    st.session_state[SELECTED_TENANT_ID] = tenant_id

def set_call(call_id: str):
    """Set selected call."""
    st.session_state[SELECTED_CALL_ID] = call_id

