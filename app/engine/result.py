from pydantic import BaseModel

from typing import Dict

class SUMResult(BaseModel):
    summary: str
    #model: str = settings.MODEL_NAME