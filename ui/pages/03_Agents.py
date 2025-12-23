"""Agents page."""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.api import list_agents, create_agent, get_agent, update_agent, APIError
from lib.state import require_login, require_tenant, SELECTED_TENANT_ID
from lib.components import render_sidebar, show_error, show_success

st.set_page_config(
    page_title="Agents - Voice Intelligence",
    page_icon="🤖",
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

st.title("🤖 Agents")
st.info(f"Managing agents for tenant: {tenant_id[:8]}...")

# Create agent form
with st.expander("➕ Create New Agent", expanded=False):
    with st.form("create_agent_form"):
        name = st.text_input("Name", placeholder="Dana Pani Voice Agent")
        status = st.selectbox("Status", ["ACTIVE", "INACTIVE"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            languages_input = st.text_input("Languages (comma-separated)", value="hi-IN, en-IN")
            st.markdown("**Voice Config (JSON)**")
            voice_json = st.text_area(
                "Voice",
                value='{"provider": "google", "voice_id": "hi-IN-Standard-A", "speaking_rate": 1.0}',
                height=80
            )
            st.markdown("**STT Config (JSON)**")
            stt_json = st.text_area(
                "STT",
                value='{"provider": "google", "model": "latest_long", "punctuate": true}',
                height=80
            )
        with col2:
            st.markdown("**LLM Config (JSON)**")
            llm_json = st.text_area(
                "LLM",
                value='{"provider": "openai", "model": "gpt-4.1-mini", "temperature": 0.3}',
                height=80
            )
            st.markdown("**Routing Config (JSON)**")
            routing_json = st.text_area(
                "Routing",
                value='{"human_transfer": {"enabled": true, "mode": "warm", "transfer_number": "+919999999999"}}',
                height=80
            )
        
        st.markdown("**Policies (JSON)**")
        policies_json = st.text_area(
            "Policies",
            value='{"no_medical_advice": true, "no_payment_capture": true}',
            height=60
        )
        
        tools_input = st.text_input("Tools Enabled (comma-separated)", value="woo.products.search, woo.orders.status, kb.search")
        
        submit = st.form_submit_button("Create Agent", use_container_width=True)
        
        if submit:
            if not name:
                st.error("Name is required")
            else:
                try:
                    import json
                    languages = [l.strip() for l in languages_input.split(",") if l.strip()]
                    tools = [t.strip() for t in tools_input.split(",") if t.strip()]
                    
                    result = create_agent(tenant_id, {
                        "name": name,
                        "status": status,
                        "languages": languages,
                        "voice": json.loads(voice_json),
                        "stt": json.loads(stt_json),
                        "llm": json.loads(llm_json),
                        "routing": json.loads(routing_json),
                        "policies": json.loads(policies_json),
                        "tools_enabled": tools
                    })
                    
                    show_success(f"Agent '{result['name']}' created successfully!")
                    st.rerun()
                    
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {str(e)}")
                except APIError as e:
                    show_error(e)
                except Exception as e:
                    show_error(f"Failed to create agent: {str(e)}")

st.markdown("---")

# List agents
st.markdown("### Agent List")

try:
    page = st.number_input("Page", min_value=1, value=1, step=1)
    page_size = st.number_input("Page Size", min_value=1, max_value=200, value=25, step=1)
    
    if st.button("Refresh", key="agents_refresh", use_container_width=True):
        st.rerun()
    
    result = list_agents(tenant_id, page=page, page_size=page_size)
    agents = result.get("data", []) if isinstance(result, dict) else result
    meta = result.get("meta", {}) if isinstance(result, dict) else {}
    
    if agents:
        st.info(f"Showing {len(agents)} of {meta.get('total', 0)} agents")
        
        for agent in agents:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{agent['name']}**")
                    st.caption(f"ID: {agent['id']}")
                    st.caption(f"Status: {agent['status']}")
                with col2:
                    st.caption(f"Languages: {', '.join(agent.get('languages', []))}")
                    st.caption(f"Tools: {len(agent.get('tools_enabled', []))} enabled")
                with col3:
                    with st.expander("View"):
                        st.json(agent)
                
                st.markdown("---")
    else:
        st.info("No agents found. Create one above.")
        
except APIError as e:
    show_error(e)
except Exception as e:
    show_error(f"Failed to load agents: {str(e)}")

