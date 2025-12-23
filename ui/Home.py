"""
Streamlit home page for Voice Intelligence Platform.
Redirects to main app.
"""
import streamlit as st

st.set_page_config(
    page_title="Voice Intelligence Platform",
    page_icon="📞",
    layout="wide"
)

# Redirect to main app
st.switch_page("streamlit_app.py")

