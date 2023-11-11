from pydantic import BaseModel

from typing import Dict
from app.core.config import settings

class SUMResult(BaseModel):
    # model output fields to be listed here, once passed to this class,
    # a new object with filled corresponding fields will be init
    summary: Dict[str, str]
    model: str = settings.MODEL_NAME