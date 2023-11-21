from pydantic import BaseModel

from typing import List


class SUMResult(BaseModel):
    summary: str

class KEYResult(BaseModel):
    summary: str

class NERResult(BaseModel):
    class Entity(BaseModel):
        entity_group: str
        score: float
        word: str
        start: int
        end: int    
    
    entities: List[Entity]
    

class QAResult(BaseModel):
    summary: str

class ZSCResult(BaseModel):
    summary: str