#!/usr/bin/env python3
"""
Simple test script for Admin Agent microservice without Dapr dependencies
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create a simple FastAPI app for testing
app = FastAPI(
    title="Admin Agent - Compliance Management API (Test Mode)",
    description="Testing the basic FastAPI structure without Dapr dependencies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Admin Agent",
        "version": "1.0.0",
        "status": "running",
        "mode": "test",
        "description": "Dapr-powered compliance management microservice (Test Mode)"
    }

@app.get("/health/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "Admin Agent",
        "version": "1.0.0",
        "mode": "test"
    }

@app.get("/api/tasks/")
async def list_tasks():
    """Test tasks endpoint"""
    return [
        {
            "id": 1,
            "title": "Test Task 1",
            "status": "Pending",
            "priority": "High"
        },
        {
            "id": 2,
            "title": "Test Task 2", 
            "status": "In Progress",
            "priority": "Medium"
        }
    ]

if __name__ == "__main__":
    print("🚀 Starting Admin Agent Microservice (Test Mode)...")
    print("📖 Swagger Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health/")
    print("📋 Test Tasks: http://localhost:8000/api/tasks/")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
