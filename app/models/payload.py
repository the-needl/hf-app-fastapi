from pydantic import BaseModel

class SUMPayload(BaseModel):
    context: str
    