from fastapi import APIRouter

import importlib
from app.core.config import settings
from app.api.endpoints import health

def create_router(model_type: str) -> APIRouter:
    model = importlib.import_module(f"app.api.endpoints.{model_type}")

    api_router = APIRouter()
    
    api_router.include_router(model.router, prefix="/run", tags=["execution"])
    api_router.include_router(health.router, prefix="/alive", tags=["health"])
    
    return api_router
