from pydantic import BaseModel

class BasePayload(BaseModel):
    context: str