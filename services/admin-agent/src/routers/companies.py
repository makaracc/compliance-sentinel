"""
Company management endpoints (simplified for testing)
"""

from typing import List
from fastapi import APIRouter
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/", summary="List Companies")
async def list_companies():
    """Get list of companies"""
    return [
        {"id": 1, "name": "TechCorp Australia", "industry": "technology", "location": "Australia"},
        {"id": 2, "name": "FinanceInc", "industry": "finance", "location": "US"}
    ]


@router.get("/{company_id}", summary="Get Company")
async def get_company(company_id: int):
    """Get a specific company by ID"""
    return {"id": company_id, "name": f"Company {company_id}", "industry": "technology", "location": "Australia"}


@router.post("/{company_id}/onboard", summary="Start Company Onboarding")
async def start_company_onboarding(company_id: int):
    """Start company onboarding workflow"""
    return {
        "message": "Company onboarding workflow started",
        "company_id": company_id,
        "workflow_instance_id": f"workflow_{company_id}"
    }
