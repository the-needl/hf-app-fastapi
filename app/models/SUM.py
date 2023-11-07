from typing import Dict, List

import logging

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline

from app.services.utils import ModelLoader
from app.config.config import settings
from app.models.base import BaseModel

logger = logging.getLogger(__name__)

class SUMMmodel(BaseModel):
    def _load_local_model(self):
        tokenizer, model = ModelLoader(
            model_name=settings.SUM_MODEL_NAME,
            model_directory=settings.DEFAULT_MODEL_PATH,
            tokenizer_loader=AutoTokenizer,
            model_loader=AutoModelForSeq2SeqLM,
        ).retrieve()

        self.engine = pipeline("summarization", model=model, tokenizer=tokenizer)

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