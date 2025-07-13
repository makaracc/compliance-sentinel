"""
Workflow registry for Dapr workflows
"""

import structlog
from ..dapr_client import DaprClientManager
from .company_onboarding import company_onboarding_workflow
from .step_generation import step_generation_workflow
from .step_completion import step_completion_workflow
from .compliance_reporting import compliance_reporting_workflow

logger = structlog.get_logger(__name__)


async def register_workflows():
    """Register all Dapr workflows"""
    try:
        # Get workflow runtime
        runtime = DaprClientManager.get_workflow_runtime()
        
        # Register company onboarding workflow
        runtime.register_workflow(company_onboarding_workflow)
        logger.info("Registered company_onboarding_workflow")
        
        # Register step generation workflow
        runtime.register_workflow(step_generation_workflow)
        logger.info("Registered step_generation_workflow")
        
        # Register step completion workflow
        runtime.register_workflow(step_completion_workflow)
        logger.info("Registered step_completion_workflow")
        
        # Register compliance reporting workflow
        runtime.register_workflow(compliance_reporting_workflow)
        logger.info("Registered compliance_reporting_workflow")
        
        logger.info("All workflows registered successfully", 
                   workflows_count=4)
        
    except Exception as e:
        logger.error("Failed to register workflows", error=str(e))
        raise
