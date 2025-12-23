"""Login page."""
import streamlit as st
import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.api import login, get_current_user, logout, APIError
from lib.state import set_tokens, clear_auth, require_login, CURRENT_USER, REFRESH_TOKEN
from lib.components import render_sidebar, show_error, show_success

st.set_page_config(
    page_title="Login - Voice Intelligence",
    page_icon="🔐",
    layout="wide"
)

render_sidebar()

st.title("🔐 Login")

# Check if already logged in
if require_login():
    user = st.session_state.get(CURRENT_USER, {})
    st.success(f"✅ Already logged in as {user.get('email', 'User')}")
    
    if st.button("Logout", key="login_logout"):
        try:
            refresh_token = st.session_state.get(REFRESH_TOKEN)
            if refresh_token:
                logout(refresh_token)
            clear_auth()
            show_success("Logged out successfully")
            st.rerun()
        except APIError as e:
            show_error(e)
        except Exception as e:
            show_error(e)
    
    st.markdown("---")
    
    # Show current user info
    try:
        user_data = get_current_user()
        st.json(user_data)
    except APIError as e:
        show_error(e)
        if e.status_code == 401:
            clear_auth()
            st.rerun()
    
else:
    # Login form
    with st.form("login_form"):
        st.markdown("### Enter your credentials")
        email = st.text_input("Email", placeholder="admin@dana-pani.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                try:
                    # Call login API
                    result = login(email, password)
                    
                    # Store tokens
                    set_tokens(
                        access_token=result["access_token"],
                        refresh_token=result["refresh_token"]
                    )
                    
                    # Store user info
                    st.session_state[CURRENT_USER] = result["user"]
                    
                    show_success(f"Logged in as {result['user']['email']}")
                    st.rerun()
                    
                except APIError as e:
                    show_error(e)
                except Exception as e:
                    show_error(f"Login failed: {str(e)}")

