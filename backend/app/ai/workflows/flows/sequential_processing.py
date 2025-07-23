"""
Sequential processing workflows using Prefect
"""

from typing import Any
from typing import Literal
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from app.core.logging.config import get_logger
import dspy

## Sequential Processing of Messages from User
# The workflow would be: User sent message -> Chatbot generates a response -> And we display the message for the user
# For this, we only need to focus on the main core functionality: Chatbot generates a response, a proper response for an API (JSON)

# What functions do we currently have?
# process_message_task, analyze_conversation_task, store_conversation_task, update_user_profile_task7

logger = get_logger("ai.prefect.sequential_processing")

@task(retries=3, retry_delay_seconds=5)
async def security_check(agent: dspy.Module, msg: str):
    """Security check for incoming messages"""
    logger.info("Doing security check...")

    result: Literal["passed", "failed"] = await agent(msg)

    return result.lower() == "passed"

@task(retries=3, retry_delay_seconds=5)
async def get_response(agent: dspy.Module, msg: str):
    """Get response from agent"""
    logger.info("Getting response...")

    try:
        result = await agent(msg)
    except Exception as e:
        raise e

    return result

@flow(task_runner=ConcurrentTaskRunner(), timeout_seconds=300)
async def sequential_chat_processing_flow(
    agent: dspy.Module,
    message: str,
) -> dict[str, Any]:
    """
    Sequential processing flow for chat messages
    Processes messages in order to maintain conversation coherence
    """

    logger.info("Starting sequential chat processing flow")

    try:
        security_passed = await security_check(agent, message)
        if not security_passed:
            raise ValueError("Security check failed")

        response = await get_response(agent, message)
        return response

    except Exception as e:
        raise e

# Build a Batch Processing Flow
# Build a Scheduled Analysis Flow
# Build Scheduled functionalities
