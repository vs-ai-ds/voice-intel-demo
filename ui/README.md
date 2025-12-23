# Streamlit UI

Voice Intelligence Platform Streamlit console application.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Configure API URL (optional):**
   Create `.env` file in `ui/` directory:
   ```
   STREAMLIT_API_BASE_URL=http://localhost:8000
   ```
   Default is `http://localhost:8000` if not set.

3. **Start backend API:**
   ```bash
   # From project root
   uvicorn app.main:app --reload --port 8000
   ```

4. **Start Streamlit UI:**
   ```bash
   # From ui/ directory (recommended)
   cd ui
   streamlit run streamlit_app.py
   
   # Or from project root
   streamlit run ui/streamlit_app.py
   ```

## Pages

- **Login** - Authenticate with email/password
- **Tenants** - Create and select tenants
- **Agents** - Create and manage voice agents
- **Calls** - Create and list calls
- **Call Detail** - View transcript and post events

## Usage Flow

1. Login with credentials (use email from seed data: `admin@dana-pani.com`)
2. Create or select a tenant
3. Create an agent for the tenant
4. Create a call
5. Open call detail to view transcript and post events

## Notes

- All API calls use the backend API at `/api/v1`
- Authentication tokens are stored in session state
- Selected tenant persists across pages
- Call detail page supports auto-refresh

