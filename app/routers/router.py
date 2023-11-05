from fastapi import APIRouter

from app.routers import document_ctrl, conversation_ctrl, health_ctrl

api_router = APIRouter()
api_router.include_router(conversation_ctrl.router, prefix="/nlp", tags=["model"])