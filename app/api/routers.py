from fastapi import APIRouter

from app.api.endpoints import SUM, health#, NER, KEY, QA

api_router = APIRouter()

api_router.include_router(SUM.router, prefix="/sum", tags=["summary"])
api_router.include_router(health.router, prefix="/alive", tags=["health"])
