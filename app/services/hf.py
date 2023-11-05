from typing import Dict, List

import logging

from transformers import AutoTokenizer
from transformers import AutoModelForQuestionAnswering
from transformers import pipeline

from huggingfastapi.models.payload import QAPredictionPayload
from huggingfastapi.models.prediction import QAPredictionResult

from app.services.utils import ModelLoader
from app.config.messages import NO_VALID_PAYLOAD
from app.config.config import settings

logger = logging.getLogger(__name__)

class SUMModel(object):
    def __init__(self, path=settings.DEFAULT_MODEL_PATH):
        self.path = path
        self._load_local_model()

    def _load_local_model(self):

        tokenizer, model = ModelLoader(
            model_name=settings.SUM_MODEL_NAME,
            model_directory=settings.DEFAULT_MODEL_PATH,
            tokenizer_loader=AutoTokenizer,
            model_loader=AutoModelForQuestionAnswering,
        ).retrieve()

        self.nlp = pipeline("summarization", model=model, tokenizer=tokenizer)

    def _pre_process(self, payload: QAPredictionPayload) -> List:
        logger.debug("Pre-processing payload.")
        result = [payload.context, payload.question]
        return result

    def _post_process(self, prediction: Dict) -> QAPredictionResult:
        logger.debug("Post-processing prediction.")

        qa = QAPredictionResult(**prediction)

        return qa

    def _predict(self, features: List) -> tuple:
        logger.debug("Predicting.")

        context, question = features

        QA_input = {
            "question": question,
            "context": context,
        }

        prediction_result = self.nlp(QA_input)

        return prediction_result

    def predict(self, payload: QAPredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result
    
    
class QAModel(object):
    def __init__(self, path=settings.DEFAULT_MODEL_PATH):
        self.path = path
        self._load_local_model()

    def _load_local_model(self):

        tokenizer, model = ModelLoader(
            model_name=settings.QUESTION_ANSWER_MODEL,
            model_directory=settings.DEFAULT_MODEL_PATH,
            tokenizer_loader=AutoTokenizer,
            model_loader=AutoModelForQuestionAnswering,
        ).retrieve()

        self.nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)

    def _pre_process(self, payload: QAPredictionPayload) -> List:
        logger.debug("Pre-processing payload.")
        result = [payload.context, payload.question]
        return result

    def _post_process(self, prediction: Dict) -> QAPredictionResult:
        logger.debug("Post-processing prediction.")

        qa = QAPredictionResult(**prediction)

        return qa

    def _predict(self, features: List) -> tuple:
        logger.debug("Predicting.")

        context, question = features

        QA_input = {
            "question": question,
            "context": context,
        }

        prediction_result = self.nlp(QA_input)

        return prediction_result

    def predict(self, payload: QAPredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result