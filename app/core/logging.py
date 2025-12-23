"""Structured logging configuration."""
import logging
import sys
from typing import Optional
from contextvars import ContextVar

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

def setup_logging():
    """Configure structured JSON logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def get_logger(name: str) -> logging.Logger:
    """Get a logger with request context."""
    logger = logging.getLogger(name)
    return logger

def log_with_context(logger: logging.Logger, level: int, message: str, **kwargs):
    """Log with request_id and correlation_id context."""
    extra = {
        "request_id": request_id_var.get(),
        "correlation_id": correlation_id_var.get(),
        **kwargs
    }
    logger.log(level, message, extra=extra)

