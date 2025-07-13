"""
Workflow management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from ..database import get_db_session
from ..models import WorkflowStartRequest, WorkflowResponse
from ..dapr_client import DaprWorkflowManager

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post(
    "/start",
    response_model=dict,
    summary="Start Workflow",
    description="Start a new Dapr workflow",
    response_description="Workflow instance details"
)
async def start_workflow(
    workflow_request: WorkflowStartRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Start a new Dapr workflow"""
    try:
        instance_id = await DaprWorkflowManager.start_workflow(
            workflow_name=workflow_request.workflow_name,
            input_data=workflow_request.input_data
        )
        
        logger.info("Workflow started", 
                   workflow_name=workflow_request.workflow_name, 
                   instance_id=instance_id)
        
        return {
            "message": "Workflow started successfully",
            "workflow_name": workflow_request.workflow_name,
            "instance_id": instance_id,
            "input_data": workflow_request.input_data
        }
        
    except Exception as e:
        logger.error("Failed to start workflow", 
                    workflow_name=workflow_request.workflow_name, 
                    error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start workflow")


@router.get(
    "/{instance_id}/status",
    summary="Get Workflow Status",
    description="Get the status of a workflow instance",
    response_description="Workflow status details"
)
async def get_workflow_status(
    instance_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get workflow status"""
    try:
        status = await DaprWorkflowManager.get_workflow_status(instance_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Workflow instance not found")
        
        logger.info("Workflow status retrieved", instance_id=instance_id)
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get workflow status", instance_id=instance_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get workflow status")


@router.post(
    "/{instance_id}/terminate",
    summary="Terminate Workflow",
    description="Terminate a running workflow instance",
    response_description="Termination confirmation"
)
async def terminate_workflow(
    instance_id: str,
    output: Optional[dict] = None,
    db: AsyncSession = Depends(get_db_session)
):
    """Terminate a workflow"""
    try:
        await DaprWorkflowManager.terminate_workflow(instance_id, output)
        
        logger.info("Workflow terminated", instance_id=instance_id)
        
        return {
            "message": "Workflow terminated successfully",
            "instance_id": instance_id
        }
        
    except Exception as e:
        logger.error("Failed to terminate workflow", instance_id=instance_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to terminate workflow")


@router.post(
    "/{instance_id}/events/{event_name}",
    summary="Raise Workflow Event",
    description="Raise an event to a workflow instance",
    response_description="Event raised confirmation"
)
async def raise_workflow_event(
    instance_id: str,
    event_name: str,
    event_data: Optional[dict] = None,
    db: AsyncSession = Depends(get_db_session)
):
    """Raise an event to a workflow"""
    try:
        await DaprWorkflowManager.raise_workflow_event(instance_id, event_name, event_data)
        
        logger.info("Workflow event raised", 
                   instance_id=instance_id, 
                   event_name=event_name)
        
        return {
            "message": "Event raised successfully",
            "instance_id": instance_id,
            "event_name": event_name,
            "event_data": event_data
        }
        
    except Exception as e:
        logger.error("Failed to raise workflow event", 
                    instance_id=instance_id, 
                    event_name=event_name, 
                    error=str(e))
        raise HTTPException(status_code=500, detail="Failed to raise workflow event")
