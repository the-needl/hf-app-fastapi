from typing import Dict, List
from pydantic import BaseModel

import logging

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from app.core.config import settings
from app.models.base import Base

from app.models.payload import SUMPayload
from app.models.result import SUMResult
from app.core.messages import NO_VALID_PAYLOAD

logger = logging.getLogger(__name__)

class SUMModel(Base):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': AutoModelForSeq2SeqLM,
            'tokenizer_loader': AutoTokenizer
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        self.engine = pipeline("summarization", model=self.model, tokenizer=self.tokenizer)

    def _pre_process(self, payload: SUMPayload) -> str:
        logger.debug("Pre-processing payload.")
        result = payload.context
        
        return result
    
    def _post_process(self, prediction: List) -> SUMResult:
        logger.debug("Post-processing prediction.")
        
        # returned data is a Dict within a List, Dict to be passed to SUMResult
        summary_raw = prediction[0]['summary_text']
        summary = SUMResult(summary=summary_raw)
        
        return summary

    def _predict(self, context: str) -> List:
        logger.debug("Predicting.")
        
        _input = context
        prediction_result = self.engine(_input)

        return prediction_result

    def predict(self, payload: SUMPayload) -> SUMResult:
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))
        
        # prepare model arguments to be submitted
        pre_proc_out = self._pre_process(payload)
        
        # call the model itself
        out = self._predict(pre_proc_out)
        logger.info(out)
        
        # prepare model output
        post_proc_out = self._post_process(out)
        
        return post_proc_out