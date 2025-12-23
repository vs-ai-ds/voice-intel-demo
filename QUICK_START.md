# Quick Start Guide

## 1. Setup Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Unix/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure Database

**IMPORTANT:** Create `.env` file in project root with your Supabase connection string.

See `scripts/SETUP_ENV.md` for detailed instructions on getting your Supabase connection string.

Quick example:
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

## 3. Run Database Setup

```bash
# Run migrations
alembic upgrade head

# Seed test data
python scripts/db_smoke_seed.py

# Verify
python scripts/db_check.py
```

## 4. Run Tests (Optional)

```bash
pytest -q scripts/test_db_migration_smoke.py
```

## Next Steps

See `scripts/SETUP_DB.md` for detailed database setup instructions.

