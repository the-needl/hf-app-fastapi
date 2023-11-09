from typing import Dict

from fastapi import APIRouter

from app.models.health import HealthResult

router = APIRouter()

@router.get("/", response_model=HealthResult, name="health")
async def get_hearbeat() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "alive"}