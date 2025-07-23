"""
KowAI Backend - Main FastAPI Application
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import api_router
from app.core.config import get_settings
from app.core.logging.config import setup_logging
from app.api.middleware.compression_middleware import CompressionMiddleware
from app.api.middleware.logging_middleware import LoggingMiddleware
from app.api.middleware.security_middleware import SecurityMiddleware
from app.infrastructure.monitoring.health import health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, AsyncSession]:
    """Application lifespan management"""
    # Startup
    logger = logging.getLogger("kowai")
    logger.info("Starting KowAI Backend...")

    # Initialize database connections, AI services, etc.
    await startup_event()

    yield

    # Shutdown
    logger.info("Shutting down KowAI Backend...")
    await shutdown_event()


async def startup_event():
    """Initialize application resources"""
    # Setup logging
    setup_logging()

    # Initialize database
    # await init_database()

    # Initialize AI services
    # await init_ai_services()

    # Start Prefect workers
    # await start_prefect_workers()


async def shutdown_event():
    """Cleanup application resources"""
    # Close database connections
    # await close_database_connections()

    # Stop Prefect workers
    # await stop_prefect_workers()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered backend service with persona architecture",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Add middleware (order matters!)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Security middleware
    app.add_middleware(SecurityMiddleware)

    # Compression middleware (C7 level)
    if settings.compression_enabled and settings.compression_level is not None:
        app.add_middleware(
            CompressionMiddleware, compression_level=settings.compression_level,
        )
        app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Logging middleware
    app.add_middleware(LoggingMiddleware)

    # Include routers
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(api_router, prefix="/api/v1")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger = logging.getLogger("kowai")
        logger.error("Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            },
        )

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
