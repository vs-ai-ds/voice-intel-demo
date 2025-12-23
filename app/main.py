"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from app.routers import calls

app = FastAPI(title="Voice Intelligence Platform", version="1.0.0")

app.include_router(calls.router, prefix="/api/calls", tags=["calls"])

@app.get("/")
async def root():
    return {"message": "Voice Intelligence Platform API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

