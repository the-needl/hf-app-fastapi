from pydantic import BaseModel

from typing import List, Dict


class SUMResult(BaseModel):
    summary: str

class NERResult(BaseModel):
    class Entity(BaseModel):
        entity_group: str
        score: float
        word: str
    
    entities: List[Entity]
    
class SENTResult(BaseModel):
    class Sentiment(BaseModel):
        label: str
        score: float
        
    sentiments: List[Sentiment]

class ZSCResult(BaseModel):
    class Entity(BaseModel):
        label: str
        score: float
        
    entities: List[Entity]

class QAResult(BaseModel):
    class Answer(BaseModel):
        question: str
        answer: str
        score: float
        
    answers: List[Answer]

class EMBResult(BaseModel):
    class Embedding(BaseModel):
        vector: List[float]
        
    embeddings: List[Embedding]

