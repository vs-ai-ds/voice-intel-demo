"""Request middleware for request_id and correlation_id."""
import uuid
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import request_id_var, correlation_id_var

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to generate and track request_id."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request_id if not present
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = f"req_{uuid.uuid4().hex[:8]}"
        
        # Get correlation_id from header
        correlation_id = request.headers.get("X-Correlation-ID")
        
        # Set context variables
        request_id_var.set(request_id)
        correlation_id_var.set(correlation_id)
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add request_id to response headers
        response.headers["X-Request-ID"] = request_id
        if correlation_id:
            response.headers["X-Correlation-ID"] = correlation_id
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

