"""
Streamlit page for viewing call history.
"""
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Call History",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Call History")

# API endpoint (adjust based on your deployment)
API_BASE = st.sidebar.text_input("API Base URL", value="http://localhost:8000")

if st.button("Refresh Calls"):
    try:
        response = requests.get(f"{API_BASE}/api/calls/")
        if response.status_code == 200:
            data = response.json()
            calls = data.get("calls", [])
            st.success(f"Loaded {len(calls)} calls")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to fetch calls: {str(e)}")

# Placeholder for call list
st.info("Call history will be displayed here. Connect to the API to see calls.")

# Example call display
with st.expander("Example Call"):
    st.json({
        "id": "call_123",
        "started_at": "2024-01-01T10:00:00",
        "ended_at": "2024-01-01T10:05:00",
        "scenario": "order_inquiry",
        "language": "en",
        "summary": "Customer inquiry about order status",
        "action_items": ["Follow up", "Send confirmation"]
    })

