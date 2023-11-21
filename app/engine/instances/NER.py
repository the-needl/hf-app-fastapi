from typing import List

import logging

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from app.core.config import settings
from app.core.messages import NO_VALID_PAYLOAD

from app.engine.models import Base
from app.engine.payload import BasePayload
from app.engine.result import NERResult

logger = logging.getLogger(__name__)

class NERModel(Base):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': AutoModelForTokenClassification,
            'tokenizer_loader': AutoTokenizer
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        self.model_params = {"aggregation_strategy":"simple"}
        self.engine = pipeline("ner", model=self.model, tokenizer=self.tokenizer)
    
    def _pre_process(self, payload: BasePayload) -> str:
        logger.debug("Pre-processing payload..")
        result = payload.context
        
        return result
    
    def _post_process(self, prediction: List) -> NERResult:
        logger.debug("Post-processing prediction..")
        
        # returned data is a List of Dicts
        result_raw = prediction[0]
        result = NERResult(entities=result_raw)
        
        return result

    def _output(self, context: str) -> List:
        logger.debug("Predicting..")
        
        context = self._split_context(context)

        if len(context) > 1:
            # If chunks created, recursive summarization triggered
            ners = []
            for chunk in context:
                [ners.append(key) for key in self.engine(chunk, **self.model_params)]
        else:
            ners = self.engine(context, **self.model_params)

        return ners

    def output(self, payload: BasePayload) -> NERResult:
        super().output()
        
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))
        
        # prepare model arguments to be submitted
        pre_proc_out = self._pre_process(payload)
        
        # call the model itself
        out = self._output(pre_proc_out)
        logger.info(out)
        
        # prepare model output
        post_proc_out = self._post_process(out)
        
        return post_proc_out
