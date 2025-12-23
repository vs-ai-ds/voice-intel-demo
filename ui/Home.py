"""
Streamlit home page for Voice Intelligence Platform.
"""
import streamlit as st

st.set_page_config(
    page_title="Voice Intelligence Platform",
    page_icon="📞",
    layout="wide"
)

st.title("📞 Voice Intelligence Platform")
st.markdown("### E-commerce Support Call Analytics")

st.markdown("""
Welcome to the Voice Intelligence Platform demo. This application provides:

- **Live Call Simulation**: Watch real-time transcription of support calls
- **Call History**: Browse past calls and their summaries
- **Search**: Find calls by keyword or content

Use the sidebar to navigate between pages.
""")

st.info("🚀 This is a demo application. Calls are simulated for demonstration purposes.")

