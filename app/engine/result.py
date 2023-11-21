from pydantic import BaseModel

from typing import List


class SUMResult(BaseModel):
    summary: str

class KEYResult(BaseModel):
    summary: str

class NERResult(BaseModel):
    entities: List

class QAResult(BaseModel):
    summary: str

class ZSCResult(BaseModel):
    summary: str