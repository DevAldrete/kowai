"""
AI Agents API routes for persona management
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai.nodes.agents.base import PersonaType, persona_router
from app.core.logging.config import get_logger

router = APIRouter()
logger = get_logger("api.agents")


class AgentConfigRequest(BaseModel):
    """Request model for agent configuration"""

    persona_type: PersonaType = Field(..., description="Persona type to configure")
    configuration: Dict[str, Any] = Field(
        ..., description="Agent configuration parameters"
    )


class AgentConfigResponse(BaseModel):
    """Response model for agent configuration"""

    agent_id: str = Field(..., description="Agent identifier")
    persona_type: str = Field(..., description="Persona type")
    configuration: Dict[str, Any] = Field(..., description="Applied configuration")
    status: str = Field(..., description="Configuration status")
    updated_at: datetime = Field(..., description="Last update timestamp")


class AgentStatusResponse(BaseModel):
    """Response model for agent status"""

    agent_id: str = Field(..., description="Agent identifier")
    persona_type: str = Field(..., description="Persona type")
    status: str = Field(..., description="Current status")
    uptime: float = Field(..., description="Uptime in seconds")
    total_interactions: int = Field(..., description="Total interactions processed")
    average_confidence: float = Field(..., description="Average confidence score")
    last_interaction: Optional[datetime] = Field(
        None, description="Last interaction timestamp"
    )


class AgentListResponse(BaseModel):
    """Response model for agent list"""

    agents: List[AgentStatusResponse] = Field(..., description="List of agents")
    total_count: int = Field(..., description="Total number of agents")


class AgentTestRequest(BaseModel):
    """Request model for agent testing"""

    persona_type: PersonaType = Field(..., description="Persona type to test")
    test_message: str = Field(
        ..., description="Test message", min_length=1, max_length=1000
    )
    context: Optional[str] = Field(None, description="Test context")


class AgentTestResponse(BaseModel):
    """Response model for agent testing"""

    persona_type: str = Field(..., description="Tested persona type")
    test_message: str = Field(..., description="Test message sent")
    response: str = Field(..., description="Agent response")
    confidence: float = Field(..., description="Response confidence")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(..., description="Test timestamp")


@router.get("/", response_model=AgentListResponse)
async def list_agents() -> AgentListResponse:
    """
    List all available AI agents

    Returns status and metrics for all persona-based agents.
    """
    try:
        logger.info("Listing all available agents")

        # Get agent information from persona router
        agents = []
        for persona_type in PersonaType:
            # TODO: Get actual agent metrics from monitoring system
            agent_status = AgentStatusResponse(
                agent_id=f"agent_{persona_type.value}",
                persona_type=persona_type.value,
                status="active",
                uptime=3600.0,  # Mock uptime
                total_interactions=100,  # Mock interaction count
                average_confidence=0.85,  # Mock confidence
                last_interaction=datetime.utcnow(),
            )
            agents.append(agent_status)

        response = AgentListResponse(agents=agents, total_count=len(agents))

        logger.info(f"Listed {len(agents)} agents", extra={"agent_count": len(agents)})

        return response

    except Exception as e:
        logger.error(
            f"Failed to list agents: {str(e)}", extra={"error": str(e)}, exc_info=True
        )

        raise HTTPException(status_code=500, detail="Failed to list agents")


@router.get("/{agent_id}", response_model=AgentStatusResponse)
async def get_agent_status(agent_id: str) -> AgentStatusResponse:
    """
    Get status of a specific agent

    Returns detailed status and metrics for a single agent.
    """
    try:
        logger.info(
            f"Getting status for agent {agent_id}", extra={"agent_id": agent_id},
        )

        # Extract persona type from agent ID
        if not agent_id.startswith("agent_"):
            raise HTTPException(status_code=400, detail="Invalid agent ID format")

        persona_type_str = agent_id.replace("agent_", "")

        # Validate persona type
        try:
            persona_type = PersonaType(persona_type_str)
        except ValueError:
            raise HTTPException(status_code=404, detail="Agent not found")

        # TODO: Get actual agent metrics from monitoring system
        agent_status = AgentStatusResponse(
            agent_id=agent_id,
            persona_type=persona_type.value,
            status="active",
            uptime=3600.0,
            total_interactions=100,
            average_confidence=0.85,
            last_interaction=datetime.utcnow(),
        )

        logger.info(
            f"Agent status retrieved successfully",
            extra={
                "agent_id": agent_id,
                "persona_type": persona_type.value,
                "status": agent_status.status,
            },
        )

        return agent_status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to get agent status: {str(e)}",
            extra={"agent_id": agent_id, "error": str(e)},
            exc_info=True,
        )

        raise HTTPException(status_code=500, detail="Failed to get agent status")


@router.post("/test", response_model=AgentTestResponse)
async def test_agent(request: AgentTestRequest) -> AgentTestResponse:
    """
    Test an agent with a sample message

    Allows testing of persona-based agents with custom messages.
    """
    try:
        logger.info(
            f"Testing agent with persona {request.persona_type.value}",
            extra={
                "persona_type": request.persona_type.value,
                "test_message_length": len(request.test_message),
            },
        )

        start_time = datetime.utcnow()

        # Test the agent using persona router
        response = persona_router(
            message=request.test_message,
            context=request.context or "",
            preferred_persona=request.persona_type,
        )

        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()

        test_response = AgentTestResponse(
            persona_type=request.persona_type.value,
            test_message=request.test_message,
            response=response.response,
            confidence=response.confidence,
            processing_time=processing_time,
            timestamp=end_time,
        )

        logger.info(
            f"Agent test completed successfully",
            extra={
                "persona_type": request.persona_type.value,
                "confidence": response.confidence,
                "processing_time": processing_time,
            },
        )

        return test_response

    except Exception as e:
        logger.error(
            f"Agent test failed: {str(e)}",
            extra={"persona_type": request.persona_type.value, "error": str(e)},
            exc_info=True,
        )

        raise HTTPException(status_code=500, detail="Agent test failed")


@router.post("/configure", response_model=AgentConfigResponse)
async def configure_agent(request: AgentConfigRequest) -> AgentConfigResponse:
    """
    Configure an agent's parameters

    Allows dynamic configuration of persona-based agents.
    """
    try:
        logger.info(
            f"Configuring agent with persona {request.persona_type.value}",
            extra={
                "persona_type": request.persona_type.value,
                "configuration_keys": list(request.configuration.keys()),
            },
        )

        # TODO: Implement actual agent configuration
        # This would typically update the agent's parameters

        agent_id = f"agent_{request.persona_type.value}"

        config_response = AgentConfigResponse(
            agent_id=agent_id,
            persona_type=request.persona_type.value,
            configuration=request.configuration,
            status="configured",
            updated_at=datetime.utcnow(),
        )

        logger.info(
            f"Agent configured successfully",
            extra={"agent_id": agent_id, "persona_type": request.persona_type.value},
        )

        return config_response

    except Exception as e:
        logger.error(
            f"Agent configuration failed: {str(e)}",
            extra={"persona_type": request.persona_type.value, "error": str(e)},
            exc_info=True,
        )

        raise HTTPException(status_code=500, detail="Agent configuration failed")


@router.post("/{agent_id}/reset")
async def reset_agent(agent_id: str) -> Dict[str, Any]:
    """
    Reset an agent to default state

    Resets agent configuration and clears any accumulated state.
    """
    try:
        logger.info(f"Resetting agent {agent_id}", extra={"agent_id": agent_id})

        # Validate agent ID
        if not agent_id.startswith("agent_"):
            raise HTTPException(status_code=400, detail="Invalid agent ID format")

        persona_type_str = agent_id.replace("agent_", "")

        try:
            persona_type = PersonaType(persona_type_str)
        except ValueError:
            raise HTTPException(status_code=404, detail="Agent not found")

        # TODO: Implement actual agent reset logic

        logger.info(
            f"Agent reset successfully",
            extra={"agent_id": agent_id, "persona_type": persona_type.value},
        )

        return {
            "status": "success",
            "message": f"Agent {agent_id} reset successfully",
            "agent_id": agent_id,
            "persona_type": persona_type.value,
            "reset_at": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Agent reset failed: {str(e)}",
            extra={"agent_id": agent_id, "error": str(e)},
            exc_info=True,
        )

        raise HTTPException(status_code=500, detail="Agent reset failed")
