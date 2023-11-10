from pydantic import BaseModel
from app.core.config import settings

class SUMPayload(BaseModel):
    
    context: str = None
    