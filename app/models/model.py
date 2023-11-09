from typing import Type
from app.models.base import BaseModel

class Model:
    def __init__(self, model_type: str):
        self.create_instance(model_type)
        
    @staticmethod
    def create_instance(model_type: str) -> BaseModel:
        model_mapping = {
            "SUM": SUMModel,
            "NET": NERModel,
            "KEY": KEYModel,
            "QA": QAModel,
        }
        model_class = model_mapping.get(model_type)
        if model_class:
            return model_class()
        else:
            raise ValueError(f"Model {model_type} not supported.")

class SUMModel(BaseModel):
    pass

class NERModel(BaseModel):
    pass

class KEYModel(BaseModel):
    pass

class QAModel(BaseModel):
    pass