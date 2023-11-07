from typing import Dict, List

import logging
from abc import abstractmethod

from transformers import AutoTokenizer
from transformers import AutoModelForQuestionAnswering
from transformers import pipeline

from huggingfastapi.models.payload import QAPredictionPayload
from huggingfastapi.models.prediction import QAPredictionResult

from app.services.utils import ModelLoader
from app.config.config import settings

logger = logging.getLogger(__name__)

class BaseModel:
    def __init__(self, path=settings.DEFAULT_MODEL_PATH):
        self.path = path
        self._load_local_model()

    def _load_local_model(self):
        # TODO: allow for generic model management both for ModelLoader() arguments and pipeline execution
        tokenizer, model = ModelLoader(
            model_name=settings.SUM_MODEL_NAME,
            model_directory=settings.DEFAULT_MODEL_PATH,
            tokenizer_loader=AutoTokenizer,
            model_loader=AutoModelForQuestionAnswering,
        ).retrieve()

        self.nlp = pipeline("summarization", model=model, tokenizer=tokenizer)

    @abstractmethod
    def _pre_process(self):
        logger.debug("Pre-processing payload.")
        pass
    
    @abstractmethod
    def _post_process(self):
        logger.debug("Post-processing prediction.")
        pass

    @abstractmethod
    def _output(self):
        logger.debug("Predicting.")
        pass

    @abstractmethod
    def output(self):
        pass