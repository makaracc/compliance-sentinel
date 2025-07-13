"""
Agent registry for Dapr agents
"""

import structlog
from .compliance_matcher import compliance_matcher_agent
from .step_generator import step_generator_agent
from .progress_monitor import progress_monitor_agent
from .evidence_validator import evidence_validator_agent
from .notification import notification_agent

logger = structlog.get_logger(__name__)


async def register_agents():
    """Register all Dapr agents"""
    try:
        # Register compliance matcher agent
        logger.info("Registered compliance_matcher_agent", 
                   agent_name=compliance_matcher_agent.name,
                   capabilities=compliance_matcher_agent.capabilities)
        
        # Register step generator agent
        logger.info("Registered step_generator_agent", 
                   agent_name=step_generator_agent.name,
                   capabilities=step_generator_agent.capabilities)
        
        # Register progress monitor agent
        logger.info("Registered progress_monitor_agent", 
                   agent_name=progress_monitor_agent.name,
                   capabilities=progress_monitor_agent.capabilities)
        
        # Register evidence validator agent
        logger.info("Registered evidence_validator_agent", 
                   agent_name=evidence_validator_agent.name,
                   capabilities=evidence_validator_agent.capabilities)
        
        # Register notification agent
        logger.info("Registered notification_agent", 
                   agent_name=notification_agent.name,
                   capabilities=notification_agent.capabilities)
        
        logger.info("All agents registered successfully", agents_count=5)
        
    except Exception as e:
        logger.error("Failed to register agents", error=str(e))
        raise


# Global registry of all agents
AGENTS_REGISTRY = {
    "compliance_matcher": compliance_matcher_agent,
    "step_generator": step_generator_agent,
    "progress_monitor": progress_monitor_agent,
    "evidence_validator": evidence_validator_agent,
    "notification": notification_agent
}


def get_agent(agent_name: str):
    """Get agent by name"""
    return AGENTS_REGISTRY.get(agent_name)
