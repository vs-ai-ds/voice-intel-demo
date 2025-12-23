"""Error handling and standard error responses."""
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from datetime import datetime
from app.core.logging import request_id_var

class APIError(Exception):
    """Base API error."""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[List[Dict[str, str]]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []

class ErrorEnvelope:
    """Standard error response envelope per API_CONTRACTS.md."""
    
    @staticmethod
    def create(
        code: str,
        message: str,
        details: Optional[List[Dict[str, str]]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> JSONResponse:
        """Create error response matching contract."""
        request_id = request_id_var.get() or "unknown"
        
        error_data = {
            "ok": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or []
            },
            "meta": {
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        return JSONResponse(
            status_code=status_code,
            content=error_data
        )

# Error code mappings
ERROR_CODES = {
    "VALIDATION_ERROR": status.HTTP_400_BAD_REQUEST,
    "UNAUTHORIZED": status.HTTP_401_UNAUTHORIZED,
    "FORBIDDEN": status.HTTP_403_FORBIDDEN,
    "NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "CONFLICT": status.HTTP_409_CONFLICT,
    "RATE_LIMITED": status.HTTP_429_TOO_MANY_REQUESTS,
    "PROVIDER_ERROR": status.HTTP_502_BAD_GATEWAY,
    "OTP_FAILED": status.HTTP_400_BAD_REQUEST,
    "TOOL_EXECUTION_FAILED": status.HTTP_500_INTERNAL_SERVER_ERROR,
}

def handle_api_error(exc: APIError) -> JSONResponse:
    """Handle APIError exceptions."""
    return ErrorEnvelope.create(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        status_code=exc.status_code
    )

def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException."""
    code = "VALIDATION_ERROR"
    if exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"
    elif exc.status_code == 403:
        code = "FORBIDDEN"
    elif exc.status_code == 409:
        code = "CONFLICT"
    
    return ErrorEnvelope.create(
        code=code,
        message=exc.detail,
        status_code=exc.status_code
    )

def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError (validation errors)."""
    return ErrorEnvelope.create(
        code="VALIDATION_ERROR",
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST
    )

