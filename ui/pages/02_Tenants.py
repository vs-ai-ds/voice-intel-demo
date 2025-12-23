"""Tenants page."""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.api import list_tenants, create_tenant, APIError
from lib.state import require_login, require_tenant, set_tenant, SELECTED_TENANT_ID
from lib.components import render_sidebar, show_error, show_success

st.set_page_config(
    page_title="Tenants - Voice Intelligence",
    page_icon="🏢",
    layout="wide"
)

render_sidebar()

# Check login
if not require_login():
    st.warning("⚠️ Please login first")
    st.page_link("pages/01_Login.py", label="Go to Login", icon="🔐")
    st.stop()

st.title("🏢 Tenants")

# Create tenant form
with st.expander("➕ Create New Tenant", expanded=False):
    with st.form("create_tenant_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", placeholder="Dana Pani")
            slug = st.text_input("Slug", placeholder="dana-pani")
        with col2:
            timezone = st.text_input("Timezone", value="UTC")
            default_language = st.text_input("Default Language", value="en-US")
        
        st.markdown("**Features** (JSON)")
        features_json = st.text_area(
            "Features",
            value='{"rag": true, "otp_order_status": true, "human_transfer": true}',
            height=100
        )
        
        submit = st.form_submit_button("Create Tenant", use_container_width=True)
        
        if submit:
            if not name or not slug:
                st.error("Name and slug are required")
            else:
                try:
                    import json
                    features = json.loads(features_json) if features_json else {}
                    
                    result = create_tenant({
                        "name": name,
                        "slug": slug,
                        "timezone": timezone,
                        "default_language": default_language,
                        "features": features
                    })
                    
                    show_success(f"Tenant '{result['name']}' created successfully!")
                    st.rerun()
                    
                except json.JSONDecodeError:
                    st.error("Invalid JSON in features field")
                except APIError as e:
                    show_error(e)
                except Exception as e:
                    show_error(f"Failed to create tenant: {str(e)}")

st.markdown("---")

# List tenants
st.markdown("### Tenant List")

try:
    page = st.number_input("Page", min_value=1, value=1, step=1)
    page_size = st.number_input("Page Size", min_value=1, max_value=200, value=25, step=1)
    
    if st.button("Refresh", key="tenants_refresh", use_container_width=True):
        st.rerun()
    
    result = list_tenants(page=page, page_size=page_size)
    tenants = result.get("data", [])
    meta = result.get("meta", {})
    
    if tenants:
        st.info(f"Showing {len(tenants)} of {meta.get('total', 0)} tenants")
        
        for tenant in tenants:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{tenant['name']}** ({tenant['slug']})")
                    st.caption(f"ID: {tenant['id']}")
                with col2:
                    st.caption(f"Timezone: {tenant['timezone']}")
                    st.caption(f"Language: {tenant['default_language']}")
                with col3:
                    is_selected = st.session_state.get(SELECTED_TENANT_ID) == tenant['id']
                    if is_selected:
                        st.success("✓ Selected")
                    else:
                        if st.button("Select", key=f"select_{tenant['id']}"):
                            set_tenant(tenant['id'])
                            show_success(f"Selected tenant: {tenant['name']}")
                            st.rerun()
                
                st.markdown("---")
        
        # Pagination info
        if meta.get('has_more'):
            st.info("More tenants available - increase page number")
    else:
        st.info("No tenants found. Create one above.")
        
except APIError as e:
    show_error(e)
except Exception as e:
    show_error(f"Failed to load tenants: {str(e)}")

# Show selected tenant
selected = require_tenant()
if selected:
    st.success(f"✅ Active tenant: {selected}")

