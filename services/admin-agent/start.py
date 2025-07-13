#!/usr/bin/env python3
"""
Startup script for Admin Agent microservice
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Set environment variables for testing
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("HOST", "0.0.0.0")
os.environ.setdefault("PORT", "8000")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")  # Use SQLite for testing
os.environ.setdefault("LOG_LEVEL", "INFO")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Admin Agent Microservice...")
    print("📖 Swagger Documentation: http://localhost:8000/docs")
    print("📊 ReDoc Documentation: http://localhost:8000/redoc")
    print("🔍 Health Check: http://localhost:8000/health/")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
