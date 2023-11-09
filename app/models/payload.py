from pydantic import BaseModel
from app.core.config import settings

class SUMPayload:
    
    context: str = None
    