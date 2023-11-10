from pydantic import BaseModel
from app.core.config import settings

class SUMResult(BaseModel):
    # model output fields to be listed here, once passed to this class,
    # a new object with filled corresponding fields will be init
    summary_text: str = None
    model: str = settings.MODEL_NAME