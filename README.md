# Voice Intelligence Platform

Real-Time Voice Intelligence for E-commerce Support (Phase 1)

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL with pgvector extension
- Supabase account (or local PostgreSQL)

### Setup

1. **Clone and setup virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Install backend dependencies:**
   ```bash
   pip install -r requirements-backend.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your DATABASE_URL
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Seed database (optional):**
   ```bash
   python scripts/db_smoke_seed.py
   ```

6. **Start backend API:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Install UI dependencies (in separate terminal):**
   ```bash
   cd ui
   pip install -r requirements-ui.txt
   ```

8. **Start Streamlit UI:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure

- `app/` - FastAPI backend
- `ui/` - Streamlit frontend
- `scripts/` - Utility scripts
- `alembic/` - Database migrations
- `tests/` - Test files

## Requirements Files

- `requirements-backend.txt` - Backend API dependencies (FastAPI, SQLAlchemy, etc.)
- `ui/requirements-ui.txt` - Streamlit UI dependencies

## Documentation

- `QUICK_START.md` - Quick start guide
- `scripts/SETUP_DB.md` - Database setup instructions
- `.cursor/PROJECT_OVERVIEW.md` - Project specification
- `.cursor/ARCHITECTURE_DECISIONS.md` - Architecture decisions
- `.cursor/API_CONTRACTS.md` - API contracts
