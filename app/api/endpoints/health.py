from typing import Dict

from fastapi import APIRouter


router = APIRouter()

@router.get("/", name="health")
async def get_hearbeat() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "alive"}