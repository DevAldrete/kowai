"""
C7 Compression middleware for optimal response compression
"""
import gzip
import zlib
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import StreamingResponse
import asyncio

from app.core.logging.config import get_logger


class CompressionMiddleware(BaseHTTPMiddleware):
    """Advanced compression middleware with C7 level compression"""
    
    def __init__(self, app: ASGIApp, compression_level: int = 7, minimum_size: int = 1000):
        super().__init__(app)
        self.compression_level = compression_level
        self.minimum_size = minimum_size
        self.logger = get_logger("middleware.compression")
        
        # Compressible content types
        self.compressible_types = {
            "application/json",
            "application/javascript",
            "application/xml",
            "text/html",
            "text/css",
            "text/javascript",
            "text/plain",
            "text/xml",
            "application/rss+xml",
            "application/atom+xml",
            "image/svg+xml"
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and apply compression if appropriate"""
        # Check if client accepts compression
        accept_encoding = request.headers.get("accept-encoding", "").lower()
        supports_gzip = "gzip" in accept_encoding
        supports_deflate = "deflate" in accept_encoding
        
        if not (supports_gzip or supports_deflate):
            return await call_next(request)
        
        # Get response
        response = await call_next(request)
        
        # Check if response should be compressed
        if not self._should_compress(response):
            return response
        
        # Get response body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        
        # Check minimum size
        if len(body) < self.minimum_size:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type
            )
        
        # Compress the body
        compressed_body, encoding = await self._compress_body(body, supports_gzip, supports_deflate)
        
        # Log compression ratio
        original_size = len(body)
        compressed_size = len(compressed_body)
        ratio = (1 - compressed_size / original_size) * 100
        
        self.logger.info(
            f"Compressed response: {original_size} -> {compressed_size} bytes ({ratio:.1f}% reduction)",
            extra={
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": ratio,
                "compression_encoding": encoding
            }
        )
        
        # Update headers
        headers = dict(response.headers)
        headers["content-encoding"] = encoding
        headers["content-length"] = str(len(compressed_body))
        headers["vary"] = "Accept-Encoding"
        
        return Response(
            content=compressed_body,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type
        )
    
    def _should_compress(self, response: Response) -> bool:
        """Check if response should be compressed"""
        # Don't compress if already compressed
        if response.headers.get("content-encoding"):
            return False
        
        # Check content type
        content_type = response.headers.get("content-type", "").split(";")[0].strip()
        
        return content_type in self.compressible_types
    
    async def _compress_body(self, body: bytes, supports_gzip: bool, supports_deflate: bool) -> tuple[bytes, str]:
        """Compress response body using best available method"""
        # Use gzip if available (better compression)
        if supports_gzip:
            compressed = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: gzip.compress(body, compresslevel=self.compression_level)
            )
            return compressed, "gzip"
        
        # Use deflate as fallback
        elif supports_deflate:
            compressed = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: zlib.compress(body, level=self.compression_level)
            )
            return compressed, "deflate"
        
        # Should not reach here
        return body, ""