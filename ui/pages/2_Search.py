"""
Streamlit page for searching calls.
"""
import streamlit as st
import requests

st.set_page_config(
    page_title="Search Calls",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Search Calls")

# API endpoint (adjust based on your deployment)
API_BASE = st.sidebar.text_input("API Base URL", value="http://localhost:8000")

search_query = st.text_input("Search query", placeholder="Enter keywords to search...")

if st.button("Search") and search_query:
    try:
        response = requests.get(f"{API_BASE}/api/calls/search/{search_query}")
        if response.status_code == 200:
            data = response.json()
            calls = data.get("calls", [])
            
            if calls:
                st.success(f"Found {len(calls)} matching calls")
                for call in calls:
                    with st.expander(f"Call {call.get('id', 'unknown')}"):
                        st.json(call)
            else:
                st.info("No calls found matching your search.")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to search: {str(e)}")
elif st.button("Search") and not search_query:
    st.warning("Please enter a search query.")

st.markdown("---")
st.info("💡 This is a simple keyword search. Vector search will be available in a future update.")

