"""
Health check endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from ..database import get_db_session

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    summary="Basic Health Check",
    description="Check if the service is running",
    response_description="Service health status"
)
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Admin Agent",
        "version": "1.0.0"
    }


@router.get(
    "/detailed",
    summary="Detailed Health Check",
    description="Check service health including database connectivity",
    response_description="Detailed health status"
)
async def detailed_health_check(db: AsyncSession = Depends(get_db_session)):
    """Detailed health check including dependencies"""
    health_status = {
        "status": "healthy",
        "service": "Admin Agent",
        "version": "1.0.0",
        "checks": {
            "database": "unknown",
            "dapr": "ready"
        }
    }
    
    # Test database connectivity
    try:
        result = await db.execute(text("SELECT 1"))
        if result:
            health_status["checks"]["database"] = "healthy"
        else:
            health_status["checks"]["database"] = "unhealthy"
            health_status["status"] = "degraded"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["checks"]["database"] = "unhealthy"
        health_status["status"] = "degraded"
    
    logger.info("Health check completed", status=health_status["status"])
    
    return health_status


@router.get(
    "/ready",
    summary="Readiness Check",
    description="Check if the service is ready to accept requests",
    response_description="Service readiness status"
)
async def readiness_check():
    """Readiness check for Kubernetes"""
    try:
        return {"status": "ready"}
        
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get(
    "/live",
    summary="Liveness Check",
    description="Check if the service is alive",
    response_description="Service liveness status"
)
async def liveness_check():
    """Liveness check for Kubernetes"""
    return {"status": "alive"}
