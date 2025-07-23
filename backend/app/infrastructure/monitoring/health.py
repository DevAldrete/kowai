"""
Health check and monitoring endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import psutil
import os

from app.core.logging.config import get_logger
from app.core.config import get_settings

health_router = APIRouter()
logger = get_logger("monitoring.health")


class HealthCheckResponse(BaseModel):
    """Response model for health checks"""

    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Uptime in seconds")
    checks: Dict[str, Any] = Field(..., description="Individual health checks")


class SystemMetricsResponse(BaseModel):
    """Response model for system metrics"""

    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    load_average: Optional[list] = Field(None, description="System load average")
    process_count: int = Field(..., description="Number of processes")
    timestamp: datetime = Field(..., description="Metrics timestamp")


# Track application start time for uptime calculation
_start_time = datetime.utcnow()


@health_router.get("/", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Comprehensive health check endpoint

    Checks all system components and returns overall health status.
    """
    try:
        logger.info("Performing health check")

        settings = get_settings()
        uptime = (datetime.utcnow() - _start_time).total_seconds()

        # Perform individual health checks
        checks = {}

        # Database health check
        checks["database"] = await _check_database_health()

        # AI services health check
        checks["ai_services"] = await _check_ai_services_health()

        # Cache health check
        checks["cache"] = await _check_cache_health()

        # External services health check
        checks["external_services"] = await _check_external_services_health()

        # System resources check
        checks["system_resources"] = await _check_system_resources()

        # Determine overall status
        all_healthy = all(check.get("status") == "healthy" for check in checks.values())
        overall_status = "healthy" if all_healthy else "unhealthy"

        response = HealthCheckResponse(
            status=overall_status,
            timestamp=datetime.now(),
            version=settings.app_version,
            uptime=uptime,
            checks=checks,
        )

        logger.info(
            f"Health check completed: {overall_status}",
            extra={
                "overall_status": overall_status,
                "uptime": uptime,
                "checks_count": len(checks),
            },
        )

        return response

    except Exception as e:
        logger.error(
            f"Health check failed: {str(e)}", extra={"error": str(e)}, exc_info=True
        )

        # Return unhealthy status even if health check itself fails
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="unknown",
            uptime=0.0,
            checks={
                "health_check": {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            },
        )


@health_router.get("/metrics", response_model=SystemMetricsResponse)
async def get_system_metrics() -> SystemMetricsResponse:
    """
    Get system performance metrics

    Returns current system resource usage and performance metrics.
    """
    try:
        logger.info("Collecting system metrics")

        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        # Disk usage
        disk = psutil.disk_usage("/")
        disk_usage = (disk.used / disk.total) * 100

        # Load average (Unix-like systems only)
        load_average = None
        if hasattr(os, "getloadavg"):
            load_average = list(os.getloadavg())

        # Process count
        process_count = len(psutil.pids())

        metrics = SystemMetricsResponse(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            load_average=load_average,
            process_count=process_count,
            timestamp=datetime.utcnow(),
        )

        logger.info(
            f"System metrics collected",
            extra={
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
            },
        )

        return metrics

    except Exception as e:
        logger.error(
            f"Failed to collect system metrics: {str(e)}",
            extra={"error": str(e)},
            exc_info=True,
        )

        raise HTTPException(status_code=500, detail="Failed to collect system metrics")


@health_router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Kubernetes readiness probe endpoint

    Returns simple ready/not ready status for container orchestration.
    """
    try:
        # Basic readiness checks
        ready = True

        # Check if AI services are initialized
        # TODO: Add actual readiness checks

        return {
            "status": "ready" if ready else "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail="Service not ready")


@health_router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """
    Kubernetes liveness probe endpoint

    Returns simple alive/dead status for container orchestration.
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


# Health check helper functions


async def _check_database_health() -> Dict[str, Any]:
    """Check database connectivity and health"""
    try:
        # TODO: Implement actual database health check
        # This would typically:
        # 1. Check database connection
        # 2. Perform a simple query
        # 3. Check connection pool status

        return {
            "status": "healthy",
            "response_time": 0.05,  # Mock response time
            "connections_active": 5,  # Mock active connections
            "connections_idle": 15,  # Mock idle connections
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


async def _check_ai_services_health() -> Dict[str, Any]:
    """Check AI services health"""
    try:
        # TODO: Implement actual AI services health check
        # This would typically:
        # 1. Check DSPy module initialization
        # 2. Check AI model availability
        # 3. Perform test inference

        return {
            "status": "healthy",
            "personas_loaded": 4,  # Mock loaded personas
            "models_available": ["gpt-3.5-turbo", "claude-3-sonnet"],  # Mock models
            "response_time": 0.2,  # Mock response time
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


async def _check_cache_health() -> Dict[str, Any]:
    """Check cache (Redis) health"""
    try:
        # TODO: Implement actual cache health check
        # This would typically:
        # 1. Check Redis connection
        # 2. Perform ping test
        # 3. Check memory usage

        return {
            "status": "healthy",
            "response_time": 0.01,  # Mock response time
            "memory_usage": "45MB",  # Mock memory usage
            "keys_count": 150,  # Mock keys count
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


async def _check_external_services_health() -> Dict[str, Any]:
    """Check external services health"""
    try:
        # TODO: Implement actual external services health check
        # This would typically check:
        # 1. Appwrite API
        # 2. AI service providers (OpenAI, Anthropic)
        # 3. Other external APIs

        return {
            "status": "healthy",
            "appwrite": {"status": "healthy", "response_time": 0.1},
            "openai": {"status": "healthy", "response_time": 0.3},
            "anthropic": {"status": "healthy", "response_time": 0.25},
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


async def _check_system_resources() -> Dict[str, Any]:
    """Check system resource usage"""
    try:
        # Get current resource usage
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        # Define thresholds
        cpu_threshold = 80.0
        memory_threshold = 85.0

        # Determine status based on thresholds
        status = "healthy"
        warnings = []

        if cpu_usage > cpu_threshold:
            status = "warning"
            warnings.append(f"High CPU usage: {cpu_usage}%")

        if memory.percent > memory_threshold:
            status = "warning"
            warnings.append(f"High memory usage: {memory.percent}%")

        return {
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory.percent,
            "warnings": warnings,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }

