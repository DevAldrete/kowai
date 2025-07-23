"""
Chat API routes with persona-based responses
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.logging.config import get_logger
from app.ai.nodes.agents.base import PersonaType
from app.ai.workflows.flows.sequential_processing import sequential_chat_processing_flow

router = APIRouter()
logger = get_logger("api.chat")


class ChatMessageRequest(BaseModel):
    """Request model for chat messages"""
    message: str = Field(..., description="User's message", min_length=1, max_length=10000)
    context: Optional[str] = Field(None, description="Additional context")
    persona_type: Optional[PersonaType] = Field(None, description="Preferred persona type")
    user_id: str = Field(..., description="User identifier")


class ChatMessageResponse(BaseModel):
    """Response model for chat messages"""
    response: str = Field(..., description="AI response")
    persona_type: str = Field(..., description="Persona type used")
    confidence: float = Field(..., description="Response confidence score")
    conversation_id: str = Field(..., description="Conversation identifier")
    timestamp: datetime = Field(..., description="Response timestamp")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class ChatHistoryResponse(BaseModel):
    """Response model for chat history"""
    conversations: List[Dict[str, Any]] = Field(..., description="List of conversations")
    total_count: int = Field(..., description="Total number of conversations")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")


class PersonaListResponse(BaseModel):
    """Response model for available personas"""
    personas: List[Dict[str, Any]] = Field(..., description="Available personas")


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    background_tasks: BackgroundTasks
) -> ChatMessageResponse:
    """
    Send a chat message and receive AI response
    
    This endpoint processes messages using the persona-based AI system
    with sequential processing for optimal conversation flow.
    """
    try:
        logger.info(
            f"Processing chat message from user {request.user_id}",
            extra={
                "user_id": request.user_id,
                "message_length": len(request.message),
                "persona_type": request.persona_type.value if request.persona_type else None
            }
        )
        
        # Process message using sequential workflow
        result = await sequential_chat_processing_flow(
            message=request.message,
            user_id=request.user_id,
            context=request.context or "",
            persona_type=request.persona_type
        )
        
        # Create response
        response = ChatMessageResponse(
            response=result["response"],
            persona_type=result["persona_type"],
            confidence=result["confidence"],
            conversation_id=result["conversation_id"],
            timestamp=datetime.utcnow(),
            processing_time=0.0  # TODO: Calculate actual processing time
        )
        
        logger.info(
            f"Chat message processed successfully",
            extra={
                "user_id": request.user_id,
                "persona_type": result["persona_type"],
                "confidence": result["confidence"],
                "conversation_id": result["conversation_id"]
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Chat message processing failed: {str(e)}",
            extra={
                "user_id": request.user_id,
                "error": str(e)
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat message"
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: str,
    page: int = 1,
    per_page: int = 20
) -> ChatHistoryResponse:
    """
    Get chat history for a user
    
    Returns paginated chat history with conversation details.
    """
    try:
        logger.info(
            f"Fetching chat history for user {user_id}",
            extra={
                "user_id": user_id,
                "page": page,
                "per_page": per_page
            }
        )
        
        # TODO: Implement actual database query
        # This would typically use the repository pattern
        
        # Mock response for now
        conversations = [
            {
                "conversation_id": f"conv_{user_id}_{i}",
                "message": f"Sample message {i}",
                "response": f"Sample response {i}",
                "persona_type": "assistant",
                "confidence": 0.95,
                "timestamp": datetime.utcnow().isoformat()
            }
            for i in range(1, min(per_page + 1, 6))
        ]
        
        response = ChatHistoryResponse(
            conversations=conversations,
            total_count=len(conversations),
            page=page,
            per_page=per_page
        )
        
        logger.info(
            f"Chat history fetched successfully",
            extra={
                "user_id": user_id,
                "returned_count": len(conversations)
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Failed to fetch chat history: {str(e)}",
            extra={
                "user_id": user_id,
                "error": str(e)
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch chat history"
        )


@router.get("/personas", response_model=PersonaListResponse)
async def get_available_personas() -> PersonaListResponse:
    """
    Get list of available personas
    
    Returns information about all available AI personas.
    """
    try:
        personas = [
            {
                "type": PersonaType.ASSISTANT.value,
                "name": "Assistant",
                "description": "General helpful assistant for everyday tasks",
                "capabilities": ["general_help", "conversation", "task_assistance"]
            },
            {
                "type": PersonaType.ANALYST.value,
                "name": "Analyst",
                "description": "Data-driven analyst for insights and patterns",
                "capabilities": ["data_analysis", "pattern_recognition", "insights"]
            },
            {
                "type": PersonaType.CREATIVE.value,
                "name": "Creative",
                "description": "Creative thinker for innovative solutions",
                "capabilities": ["creative_writing", "brainstorming", "innovation"]
            },
            {
                "type": PersonaType.TECHNICAL.value,
                "name": "Technical",
                "description": "Technical expert for implementation details",
                "capabilities": ["technical_analysis", "implementation", "troubleshooting"]
            }
        ]
        
        response = PersonaListResponse(personas=personas)
        
        logger.info(
            f"Available personas fetched: {len(personas)} personas",
            extra={
                "persona_count": len(personas)
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Failed to fetch personas: {str(e)}",
            extra={
                "error": str(e)
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch available personas"
        )


class FeedbackRequest(BaseModel):
    """Request model for feedback submission"""
    conversation_id: str = Field(..., description="Conversation identifier")
    rating: int = Field(..., description="Rating 1-5", ge=1, le=5)
    feedback: Optional[str] = Field(None, description="Optional feedback text")


@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest
) -> Dict[str, Any]:
    """
    Submit feedback for a conversation
    
    Allows users to rate and provide feedback on AI responses.
    """
    try:
        logger.info(
            f"Feedback submitted for conversation {request.conversation_id}",
            extra={
                "conversation_id": request.conversation_id,
                "rating": request.rating,
                "has_feedback": request.feedback is not None
            }
        )
        
        # TODO: Store feedback in database
        # This would typically update the conversation record
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "conversation_id": request.conversation_id,
            "submitted_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(
            f"Failed to submit feedback: {str(e)}",
            extra={
                "conversation_id": request.conversation_id,
                "error": str(e)
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=500,
            detail="Failed to submit feedback"
        )