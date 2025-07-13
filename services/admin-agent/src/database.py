"""
Database connection and session management
"""

import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
import structlog

from .config import settings
from .models import Base

logger = structlog.get_logger(__name__)

# Global database engine and session maker
engine = None
async_session_maker = None


async def init_db():
    """Initialize database connection"""
    global engine, async_session_maker
    
    try:
        # Create async engine for PostgreSQL
        database_url = settings.DATABASE_URL
        if not database_url:
            # Construct URL if not provided
            database_url = f"postgresql+asyncpg://user:password@host:5432/{settings.DATABASE_NAME}"
            logger.warning("DATABASE_URL not set, using default connection string")
        
        # Convert to async URL if needed
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        engine = create_async_engine(
            database_url,
            poolclass=NullPool,  # Use NullPool for serverless databases like Neon
            echo=settings.DEBUG,
            future=True
        )
        
        async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        logger.info("Database connection initialized", database=settings.DATABASE_NAME)
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db():
    """Close database connection"""
    global engine
    
    if engine:
        await engine.dispose()
        logger.info("Database connection closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    if not async_session_maker:
        raise RuntimeError("Database not initialized")
    
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


# Dependency for FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session"""
    async for session in get_db():
        yield session
