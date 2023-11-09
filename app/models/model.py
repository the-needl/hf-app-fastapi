from typing import Dict, List

import logging

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline

from app.core.config import settings
from app.models.base import BaseModel

logger = logging.getLogger(__name__)

class Model:
    def __init__(self, model_type: str):
        self.create_instance(model_type)
        
    @staticmethod
    def create_instance(model_type: str) -> BaseModel:
        model_mapping = {
            "SUM": SUMModel,
            "NER": NERModel,
            "KEY": KEYModel,
            "QA": QAModel,
        }
        model_class = model_mapping.get(model_type)
        if model_class:
            return model_class()
        else:
            raise ValueError(f"Model {model_type} not supported.")

class SUMModel(BaseModel):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.SUM_MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': AutoModelForSeq2SeqLM,
            'tokenizer_loader': AutoTokenizer
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        self.engine = pipeline(settings.MODEL_TASK, model=self.model, tokenizer=self.tokenizer)

    def _pre_process(self):
        logger.debug("Pre-processing payload.")
        pass
    
    def _post_process(self):
        logger.debug("Post-processing prediction.")
        pass

    def _output(self):
        logger.debug("Predicting.")
        pass

    def output(self):
        pass

class NERModel(BaseModel):
    pass

class KEYModel(BaseModel):
    pass

class QAModel(BaseModel):
    pass