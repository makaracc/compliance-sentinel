"""
Admin Agent Microservice
Main FastAPI application with Dapr integration and Swagger documentation
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db, close_db
from .routers import companies, compliance, workflows, health, steps, tasks

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager"""
    logger.info("Starting Admin Agent microservice")
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")
        
        # Initialize Dapr clients and register workflows/agents
        try:
            from .workflows.registry import register_workflows
            from .agents.registry import register_agents
            
            await register_workflows()
            await register_agents()
            logger.info("Dapr workflows and agents registered")
            
        except Exception as e:
            logger.warning("Dapr integration not available", error=str(e))
        
        yield
        
    except Exception as e:
        logger.error("Failed to start application", error=str(e))
        raise
    finally:
        # Cleanup
        await close_db()
        logger.info("Admin Agent microservice stopped")


# Create FastAPI application with comprehensive Swagger documentation
app = FastAPI(
    title="Admin Agent - Compliance Management API",
    description="""
    ## Dapr-powered Compliance Management Microservice
    
    This API provides comprehensive compliance management capabilities including:
    
    * **Company Management** - Manage companies and their compliance requirements
    * **Compliance Tracking** - Track compliance requirements and their status
    * **Step Management** - Detailed step-by-step compliance tracking
    * **Task Management** - Create and track compliance tasks
    * **Workflow Orchestration** - Dapr workflow management for compliance processes
    * **Evidence Management** - Handle compliance evidence and documentation
    * **Reporting** - Generate compliance reports and analytics
    
    ### Key Features:
    - **Dapr Workflows** for resilient compliance processes
    - **Dapr Agents** for intelligent compliance automation
    - **Step-by-step tracking** with evidence management
    - **Real-time progress monitoring**
    - **Automated notifications** and alerts
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Compliance Sentinel Team",
        "email": "admin@compliance-sentinel.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.compliance-sentinel.com",
            "description": "Production server"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper tags and descriptions
app.include_router(
    health.router, 
    prefix="/health", 
    tags=["Health Check"],
    responses={404: {"description": "Not found"}}
)

app.include_router(
    companies.router, 
    prefix="/api/companies", 
    tags=["Company Management"],
    responses={404: {"description": "Company not found"}}
)

app.include_router(
    compliance.router, 
    prefix="/api/compliance", 
    tags=["Compliance Management"],
    responses={404: {"description": "Compliance requirement not found"}}
)

app.include_router(
    steps.router, 
    prefix="/api/steps", 
    tags=["Step Management"],
    responses={404: {"description": "Step not found"}}
)

app.include_router(
    tasks.router, 
    prefix="/api/tasks", 
    tags=["Task Management"],
    responses={404: {"description": "Task not found"}}
)

app.include_router(
    workflows.router, 
    prefix="/api/workflows", 
    tags=["Workflow Management"],
    responses={404: {"description": "Workflow not found"}}
)


@app.get(
    "/",
    summary="Service Information",
    description="Get basic information about the Admin Agent service",
    response_description="Service metadata and status"
)
async def root():
    """Root endpoint providing service information"""
    return {
        "service": "Admin Agent",
        "version": "1.0.0",
        "status": "running",
        "description": "Dapr-powered compliance management microservice",
        "features": [
            "Company management",
            "Compliance tracking",
            "Step-by-step monitoring",
            "Task management",
            "Workflow orchestration",
            "Evidence handling",
            "Automated reporting"
        ],
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "dapr_enabled": True
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
