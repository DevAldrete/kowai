"""
Security middleware for headers and protection
"""
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logging.config import get_logger


class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for adding security headers and protection"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger("middleware.security")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response"""
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' wss: https:; "
            "frame-ancestors 'none';"
        )
        
        # Remove server header for security
        if "server" in response.headers:
            del response.headers["server"]
        
        return response