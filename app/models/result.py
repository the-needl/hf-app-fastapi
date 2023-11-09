from pydantic import BaseModel
from app.core.config import settings


class SUMResult(BaseModel):
    summary: str
    model: str = settings.MODEL_NAME
    