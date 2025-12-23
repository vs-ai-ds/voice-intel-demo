You are implementing the project defined in SPEC.md.

Rules:
1) No "AI" comments or meta references in code.
2) Modular code, clear boundaries, small files.
3) Fix root causes. Avoid patchy defensive code.
4) Human-like comments: explain intent and decisions.
5) All external services through provider interfaces.
6) Configuration via env vars, no hard-coded secrets.
7) Keep deployability: Render + Supabase defaults.
8) Update SPEC.md if behavior changes.

Environment & File Organization:
9) Virtual environment is required. Use `.venv/` (already in .gitignore).
10) All documentation, summaries, and test scripts go in `scripts/` folder.
11) Never create files in project root except: README.md, requirements.txt, SPEC.md, alembic.ini, .env.example
12) When running commands, assume virtual environment is activated. If not, user will activate it.
13) For Windows: use PowerShell commands. For Unix/Mac: use bash commands.
14) Always check if dependencies are installed before running commands that require them.

Command Execution:
- User will run setup commands (virtual env creation, pip install).
- You can propose commands but user will execute them.
- Always provide clear, copy-pastable commands.
- Document setup steps in scripts/SETUP_*.md files.