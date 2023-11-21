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

        self.engine = pipeline("token-classification", model=self.model, tokenizer=self.tokenizer)
    
    def _post_process(self, prediction: List) -> NERResult:
        logger.debug("Post-processing prediction..")
        
        # returned data is a List of Dicts
        result_raw = prediction
        result = NERResult(entities=result_raw)
        
        return result

    def output(self, payload: BasePayload) -> NERResult:
        super().output()
        
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
