from typing import Dict, List

import logging

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline

from app.services.utils import ModelLoader
from app.core.config import settings
from app.models.base import BaseModel

logger = logging.getLogger(__name__)

class SUMMmodel(BaseModel):
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