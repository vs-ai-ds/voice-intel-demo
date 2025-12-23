"""Calls page."""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.api import list_calls, create_call, APIError
from lib.state import require_login, require_tenant, set_call, SELECTED_TENANT_ID
from lib.components import render_sidebar, show_error, show_success

st.set_page_config(
    page_title="Calls - Voice Intelligence",
    page_icon="📞",
    layout="wide"
)

render_sidebar()

# Check login
if not require_login():
    st.warning("⚠️ Please login first")
    st.page_link("pages/01_Login.py", label="Go to Login", icon="🔐")
    st.stop()

# Check tenant
tenant_id = require_tenant()
if not tenant_id:
    st.warning("⚠️ Please select a tenant first")
    st.page_link("pages/02_Tenants.py", label="Go to Tenants", icon="🏢")
    st.stop()

st.title("📞 Calls")
st.info(f"Managing calls for tenant: {tenant_id[:8]}...")

# Create call form
with st.expander("➕ Create New Call", expanded=False):
    with st.form("create_call_form"):
        col1, col2 = st.columns(2)
        with col1:
            provider = st.selectbox("Provider", ["simulated", "twilio"], index=0)
            provider_call_id = st.text_input("Provider Call ID", placeholder="CA_test_001")
            from_phone = st.text_input("From Phone", placeholder="+1234567890")
            to_phone = st.text_input("To Phone", placeholder="+0987654321")
        with col2:
            direction = st.selectbox("Direction", ["INBOUND", "OUTBOUND"], index=0)
            agent_id = st.text_input("Agent ID", placeholder="Enter agent ID")
            locale_hint = st.text_input("Locale Hint", value="en-US")
        
        submit = st.form_submit_button("Create Call", use_container_width=True)
        
        if submit:
            if not provider_call_id or not from_phone or not to_phone or not agent_id:
                st.error("Provider Call ID, From Phone, To Phone, and Agent ID are required")
            else:
                try:
                    result = create_call(tenant_id, {
                        "provider": provider,
                        "provider_call_id": provider_call_id,
                        "from_phone": from_phone,
                        "to_phone": to_phone,
                        "direction": direction,
                        "agent_id": agent_id,
                        "locale_hint": locale_hint
                    })
                    
                    show_success(f"Call '{result['id']}' created successfully!")
                    st.rerun()
                    
                except APIError as e:
                    show_error(e)
                except Exception as e:
                    show_error(f"Failed to create call: {str(e)}")

st.markdown("---")

# Filters
st.markdown("### Filters")
col1, col2, col3, col4 = st.columns(4)
with col1:
    status_filter = st.selectbox("Status", [None, "INITIATED", "IN_PROGRESS", "COMPLETED", "FAILED"], index=0)
with col2:
    from_phone_filter = st.text_input("From Phone", value="")
with col3:
    to_phone_filter = st.text_input("To Phone", value="")
with col4:
    pass

# List calls
st.markdown("### Call List")

try:
    page = st.number_input("Page", min_value=1, value=1, step=1)
    page_size = st.number_input("Page Size", min_value=1, max_value=200, value=25, step=1)
    
    if st.button("Refresh", key="calls_refresh", use_container_width=True):
        st.rerun()
    
    result = list_calls(
        tenant_id,
        page=page,
        page_size=page_size,
        status=status_filter,
        from_phone=from_phone_filter if from_phone_filter else None,
        to_phone=to_phone_filter if to_phone_filter else None
    )
    calls = result.get("data", []) if isinstance(result, dict) else result
    meta = result.get("meta", {}) if isinstance(result, dict) else {}
    
    if calls:
        st.info(f"Showing {len(calls)} of {meta.get('total', 0)} calls")
        
        for call in calls:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.markdown(f"**Call {call['id'][:8]}...**")
                    st.caption(f"Status: {call['status']}")
                    if call.get('from_phone'):
                        st.caption(f"From: {call['from_phone']}")
                with col2:
                    st.caption(f"Started: {call.get('started_at', 'N/A')}")
                    if call.get('ended_at'):
                        st.caption(f"Ended: {call['ended_at']}")
                with col3:
                    if call.get('duration_sec'):
                        st.caption(f"Duration: {call['duration_sec']}s")
                    if call.get('language'):
                        st.caption(f"Language: {call['language']}")
                with col4:
                    if st.button("Open", key=f"open_{call['id']}"):
                        set_call(call['id'])
                        st.switch_page("pages/05_Call_Detail.py")
                
                st.markdown("---")
    else:
        st.info("No calls found. Create one above.")
        
except APIError as e:
    show_error(e)
except Exception as e:
    show_error(f"Failed to load calls: {str(e)}")

