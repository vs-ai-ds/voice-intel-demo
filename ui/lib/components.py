"""Reusable UI components."""
import streamlit as st
from lib.state import (
    require_login, require_tenant, require_call,
    CURRENT_USER, SELECTED_TENANT_ID, SELECTED_CALL_ID,
    clear_auth
)

def render_sidebar():
    """Render sidebar with app info and navigation."""
    st.sidebar.title("📞 Voice Intelligence")
    st.sidebar.markdown("---")
    
    # Login status
    if require_login():
        user = st.session_state.get(CURRENT_USER, {})
        st.sidebar.success(f"✅ Logged in as {user.get('email', 'User')}")
        if st.sidebar.button("Logout", use_container_width=True):
            clear_auth()
            st.rerun()
    else:
        st.sidebar.info("🔒 Not logged in")
    
    st.sidebar.markdown("---")
    
    # Selected tenant
    tenant_id = require_tenant()
    if tenant_id:
        st.sidebar.success(f"🏢 Tenant: {tenant_id[:8]}...")
    else:
        st.sidebar.warning("⚠️ No tenant selected")
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    st.sidebar.page_link("pages/01_Login.py", label="🔐 Login", icon="🔐")
    st.sidebar.page_link("pages/02_Tenants.py", label="🏢 Tenants", icon="🏢")
    st.sidebar.page_link("pages/03_Agents.py", label="🤖 Agents", icon="🤖")
    st.sidebar.page_link("pages/04_Calls.py", label="📞 Calls", icon="📞")
    st.sidebar.page_link("pages/05_Call_Detail.py", label="📋 Call Detail", icon="📋")

def show_error(error: Exception):
    """Show error message."""
    if isinstance(error, Exception):
        st.error(f"❌ {str(error)}")
    else:
        st.error(f"❌ {error}")

def show_success(message: str):
    """Show success message."""
    st.success(f"✅ {message}")

