"""Streamlit app entry point."""
import streamlit as st
import sys
import os
from pathlib import Path

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Voice Intelligence Platform",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
from lib.state import init_session_state
init_session_state()

# Render sidebar
from lib.components import render_sidebar
render_sidebar()

# Main content
st.title("📞 Voice Intelligence Platform")
st.markdown("### E-commerce Support Call Analytics")

# Show API URL configuration
from lib.config import API_BASE_URL
with st.expander("⚙️ API Configuration", expanded=False):
    st.info(f"**API Base URL:** `{API_BASE_URL}`")
    st.caption("To change this, set `STREAMLIT_API_BASE_URL` or `API_BASE_URL` environment variable")

st.markdown("""
Welcome to the Voice Intelligence Platform demo. This application provides:

- **Call Management**: Create and manage support calls
- **Transcripts**: View real-time call transcripts
- **Events**: Track call events and tool calls
- **Analytics**: Analyze call data and summaries

Use the sidebar to navigate between pages.
""")

st.info("🚀 Use the sidebar to login and get started!")

