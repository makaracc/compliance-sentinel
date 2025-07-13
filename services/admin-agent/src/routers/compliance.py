"""
Compliance management endpoints (simplified for testing)
"""

from fastapi import APIRouter
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/requirements", summary="List Compliance Requirements")
async def list_compliance_requirements():
    """Get list of compliance requirements"""
    return [
        {"id": 1, "name": "Data Protection Assessment", "framework": "GDPR", "severity_level": "High"},
        {"id": 2, "name": "Financial Controls Review", "framework": "SOX", "severity_level": "Critical"},
        {"id": 3, "name": "Security Audit", "framework": "ISO27001", "severity_level": "High"}
    ]


@router.get("/requirements/{requirement_id}", summary="Get Compliance Requirement")
async def get_compliance_requirement(requirement_id: int):
    """Get a specific compliance requirement by ID"""
    return {
        "id": requirement_id, 
        "name": f"Requirement {requirement_id}", 
        "framework": "GDPR", 
        "severity_level": "High"
    }
