"""Call detail page with transcript and events."""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.api import get_call, get_transcript, post_event, APIError
from lib.state import require_login, require_tenant, require_call, SELECTED_TENANT_ID, SELECTED_CALL_ID
from lib.components import render_sidebar, show_error, show_success

st.set_page_config(
    page_title="Call Detail - Voice Intelligence",
    page_icon="📋",
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

# Check call
call_id = require_call()
if not call_id:
    st.warning("⚠️ Please select a call first")
    st.page_link("pages/04_Calls.py", label="Go to Calls", icon="📞")
    st.stop()

st.title("📋 Call Detail")
st.info(f"Call ID: {call_id[:8]}... | Tenant: {tenant_id[:8]}...")

# Refresh button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh", key="call_detail_refresh", use_container_width=True):
        st.rerun()
with col2:
    auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)

if auto_refresh:
    import time
    time.sleep(5)
    st.rerun()

st.markdown("---")

# Call details
try:
    call_data = get_call(tenant_id, call_id)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Call Information")
        st.json(call_data)
    
    with col2:
        st.markdown("### Summary")
        if call_data.get('summary'):
            st.json(call_data['summary'])
        else:
            st.info("No summary available yet")
        
        st.markdown("### Metrics")
        if call_data.get('metrics'):
            st.json(call_data['metrics'])
        else:
            st.info("No metrics available yet")
    
    st.markdown("---")
    
    # Transcript
    st.markdown("### Transcript")
    try:
        transcript_data = get_transcript(tenant_id, call_id)
        turns = transcript_data.get("turns", [])
        
        if turns:
            for turn in turns:
                speaker = turn.get("speaker", "UNKNOWN")
                text = turn.get("text", "")
                ts = turn.get("ts", "")
                confidence = turn.get("confidence")
                
                # Color code by speaker
                if speaker == "USER" or speaker == "CUSTOMER":
                    st.markdown(f"**👤 {speaker}** ({ts})")
                    st.markdown(f"> {text}")
                elif speaker == "ASSISTANT" or speaker == "AGENT":
                    st.markdown(f"**🤖 {speaker}** ({ts})")
                    st.markdown(f"> {text}")
                else:
                    st.markdown(f"**{speaker}** ({ts})")
                    st.markdown(f"> {text}")
                
                if confidence is not None:
                    st.caption(f"Confidence: {confidence:.2f}")
                
                st.markdown("---")
        else:
            st.info("No transcript available yet")
            
    except APIError as e:
        show_error(f"Failed to load transcript: {e}")
    except Exception as e:
        show_error(f"Error loading transcript: {str(e)}")
    
    st.markdown("---")
    
    # Events
    st.markdown("### Events")
    
    # Post event form
    with st.expander("➕ Post Event", expanded=False):
        with st.form("post_event_form"):
            event_type = st.text_input("Event Type", placeholder="TOOL_CALL")
            correlation_id = st.text_input("Correlation ID (optional)", placeholder="corr_123")
            
            st.markdown("**Payload (JSON)**")
            payload_json = st.text_area(
                "Payload",
                value='{"tool": "woo.products.search", "args": {"query": "test"}, "result": {"count": 1}}',
                height=150
            )
            
            submit = st.form_submit_button("Post Event", use_container_width=True)
            
            if submit:
                if not event_type:
                    st.error("Event type is required")
                else:
                    try:
                        import json
                        payload = json.loads(payload_json) if payload_json else {}
                        
                        result = post_event(
                            tenant_id,
                            call_id,
                            {
                                "type": event_type,
                                "correlation_id": correlation_id if correlation_id else None,
                                "payload": payload
                            },
                            correlation_id=correlation_id if correlation_id else None
                        )
                        
                        show_success("Event posted successfully!")
                        st.rerun()
                        
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in payload field")
                    except APIError as e:
                        show_error(e)
                    except Exception as e:
                        show_error(f"Failed to post event: {str(e)}")
    
    st.info("💡 Events are append-only. Use the form above to add new events.")
    
except APIError as e:
    show_error(e)
except Exception as e:
    show_error(f"Failed to load call: {str(e)}")

