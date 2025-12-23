"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.router import api_router
from app.core.middleware import RequestIDMiddleware
from app.core.errors import (
    APIError, handle_api_error, handle_http_exception, handle_value_error
)
from app.core.logging import setup_logging
import sys

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Voice Intelligence Platform",
    version="0.1.0",
    description="Real-Time Voice Intelligence for E-commerce Support"
)

# CORS middleware (for Streamlit local dev and deployed UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        # Add your deployed Streamlit URL here if needed
        # "https://your-app.onrender.com",
        # "https://*.streamlit.app",  # Streamlit Cloud
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID middleware
app.add_middleware(RequestIDMiddleware)

# Include API router
app.include_router(api_router)

# Exception handlers
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Handle APIError exceptions."""
    return handle_api_error(exc)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTPException."""
    return handle_http_exception(request, exc)

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette HTTPException."""
    return handle_http_exception(request, exc)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError."""
    return handle_value_error(request, exc)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Voice Intelligence Platform API", "version": "0.1.0"}

