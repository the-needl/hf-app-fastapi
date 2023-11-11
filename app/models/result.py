from pydantic import BaseModel

from typing import Dict

class SUMResult(BaseModel):
    # model output fields to be listed here, once passed to this class,
    # a new object with filled corresponding fields will be init
    summary: str
    #model: str = settings.MODEL_NAME