from pydantic import BaseModel
from typing import List

class BasePayload(BaseModel):
    context: str
    
class EMBPayload(BaseModel):
    context : List[str]