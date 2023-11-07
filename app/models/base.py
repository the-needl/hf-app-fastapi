from typing import Dict, List

import logging
from abc import abstractmethod

from transformers import AutoTokenizer
from transformers import AutoModelForQuestionAnswering
from transformers import pipeline

from app.services.utils import ModelLoader
from app.config.config import settings

logger = logging.getLogger(__name__)

class BaseModel:
    def __init__(self, path=settings.DEFAULT_MODEL_PATH):
        self.path = path
        self._load_local_model()

    @abstractmethod
    def _load_local_model(self):
        pass

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