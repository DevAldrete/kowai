"""
Logging middleware for request/response tracking
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logging.config import get_logger, set_correlation_id, set_user_id


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger("middleware.logging")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details"""
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        set_correlation_id(correlation_id)
        
        # Extract user ID from token if available
        auth_header = request.headers.get("authorization")
        if auth_header:
            # TODO: Extract user ID from JWT token
            # user_id = extract_user_id_from_token(auth_header)
            # set_user_id(user_id)
            pass
        
        start_time = time.time()
        
        # Log request
        self.logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "request_query": str(request.query_params),
                "user_agent": request.headers.get("user-agent"),
                "client_ip": request.client.host if request.client else None,
                "correlation_id": correlation_id
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log response
            self.logger.info(
                f"Response: {response.status_code}",
                extra={
                    "response_status": response.status_code,
                    "execution_time": execution_time,
                    "correlation_id": correlation_id
                }
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Log error
            self.logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "execution_time": execution_time,
                    "correlation_id": correlation_id
                },
                exc_info=True
            )
            
            raise