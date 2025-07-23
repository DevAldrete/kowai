"""
API v1 router configuration
"""
from fastapi import APIRouter

from app.api.v1.chat.routes import router as chat_router
from app.api.v1.agents.routes import router as agents_router
from app.api.v1.workflows.routes import router as workflows_router

api_router = APIRouter()

# Include all v1 routes
api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

api_router.include_router(
    agents_router,
    prefix="/agents",
    tags=["AI Agents"]
)

api_router.include_router(
    workflows_router,
    prefix="/workflows",
    tags=["Workflows"]
)