"""
Dapr client management and utilities
"""

import asyncio
from typing import Optional, Dict, Any
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowClient
import structlog

from .config import settings

logger = structlog.get_logger(__name__)


class DaprClientManager:
    """Manages Dapr client instances"""
    
    _dapr_client: Optional[DaprClient] = None
    _workflow_client: Optional[DaprWorkflowClient] = None
    _workflow_runtime: Optional[WorkflowRuntime] = None
    
    @classmethod
    async def initialize(cls):
        """Initialize Dapr clients"""
        try:
            # Initialize Dapr client
            cls._dapr_client = DaprClient(
                address=f"{settings.DAPR_HOST}:{settings.DAPR_GRPC_PORT}"
            )
            
            # Initialize workflow client
            cls._workflow_client = DaprWorkflowClient()
            
            # Initialize workflow runtime
            cls._workflow_runtime = WorkflowRuntime()
            
            logger.info("Dapr clients initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize Dapr clients", error=str(e))
            raise
    
    @classmethod
    async def close(cls):
        """Close Dapr clients"""
        try:
            if cls._dapr_client:
                cls._dapr_client.close()
            
            if cls._workflow_runtime:
                await cls._workflow_runtime.stop()
            
            logger.info("Dapr clients closed")
            
        except Exception as e:
            logger.error("Error closing Dapr clients", error=str(e))
    
    @classmethod
    def get_client(cls) -> DaprClient:
        """Get Dapr client instance"""
        if not cls._dapr_client:
            raise RuntimeError("Dapr client not initialized")
        return cls._dapr_client
    
    @classmethod
    def get_workflow_client(cls) -> DaprWorkflowClient:
        """Get workflow client instance"""
        if not cls._workflow_client:
            raise RuntimeError("Workflow client not initialized")
        return cls._workflow_client
    
    @classmethod
    def get_workflow_runtime(cls) -> WorkflowRuntime:
        """Get workflow runtime instance"""
        if not cls._workflow_runtime:
            raise RuntimeError("Workflow runtime not initialized")
        return cls._workflow_runtime


class DaprStateManager:
    """Manages Dapr state operations"""
    
    @staticmethod
    async def save_state(store_name: str, key: str, value: Any) -> None:
        """Save state to Dapr state store"""
        client = DaprClientManager.get_client()
        await client.save_state(store_name, key, value)
        logger.debug("State saved", store=store_name, key=key)
    
    @staticmethod
    async def get_state(store_name: str, key: str) -> Any:
        """Get state from Dapr state store"""
        client = DaprClientManager.get_client()
        result = await client.get_state(store_name, key)
        logger.debug("State retrieved", store=store_name, key=key)
        return result.data if result else None
    
    @staticmethod
    async def delete_state(store_name: str, key: str) -> None:
        """Delete state from Dapr state store"""
        client = DaprClientManager.get_client()
        await client.delete_state(store_name, key)
        logger.debug("State deleted", store=store_name, key=key)


class DaprPubSubManager:
    """Manages Dapr pub/sub operations"""
    
    @staticmethod
    async def publish_event(pubsub_name: str, topic: str, data: Dict[str, Any]) -> None:
        """Publish event to Dapr pub/sub"""
        client = DaprClientManager.get_client()
        await client.publish_event(pubsub_name, topic, data)
        logger.info("Event published", pubsub=pubsub_name, topic=topic)


class DaprWorkflowManager:
    """Manages Dapr workflow operations"""
    
    @staticmethod
    async def start_workflow(workflow_name: str, input_data: Dict[str, Any], instance_id: Optional[str] = None) -> str:
        """Start a Dapr workflow"""
        client = DaprClientManager.get_workflow_client()
        
        instance_id = await client.schedule_new_workflow(
            workflow=workflow_name,
            input=input_data,
            instance_id=instance_id
        )
        
        logger.info("Workflow started", workflow=workflow_name, instance_id=instance_id)
        return instance_id
    
    @staticmethod
    async def get_workflow_status(instance_id: str) -> Dict[str, Any]:
        """Get workflow status"""
        client = DaprClientManager.get_workflow_client()
        
        state = await client.get_workflow_state(instance_id, fetch_payloads=True)
        
        if state:
            return {
                "instance_id": instance_id,
                "workflow_name": state.name,
                "status": state.runtime_status.name,
                "input_data": state.serialized_input,
                "output_data": state.serialized_output,
                "created_at": state.created_at,
                "last_updated_at": state.last_updated_at
            }
        
        return None
    
    @staticmethod
    async def terminate_workflow(instance_id: str, output: Optional[Any] = None) -> None:
        """Terminate a workflow"""
        client = DaprClientManager.get_workflow_client()
        await client.terminate_workflow(instance_id, output)
        logger.info("Workflow terminated", instance_id=instance_id)
    
    @staticmethod
    async def raise_workflow_event(instance_id: str, event_name: str, event_data: Any = None) -> None:
        """Raise an event to a workflow"""
        client = DaprClientManager.get_workflow_client()
        await client.raise_workflow_event(instance_id, event_name, event_data)
        logger.info("Workflow event raised", instance_id=instance_id, event=event_name)
