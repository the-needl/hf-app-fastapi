from typing import List

import logging

import numpy as np

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

from app.core.config import settings
from app.core.messages import NO_VALID_PAYLOAD

from app.engine.models import Base
from app.engine.payload import BasePayload
from app.engine.result import ZSCResult

logger = logging.getLogger(__name__)

class ZSCModel(Base):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': AutoModelForSequenceClassification,
            'tokenizer_loader': AutoTokenizer
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        self.model_params = {"candidate_labels":["article", "other"], "multi_label":False}
        self.engine = pipeline("zero-shot-classification", model=self.model, tokenizer=self.tokenizer)
    
    def _pre_process(self, payload: BasePayload) -> str:
        logger.debug("Pre-processing payload..")
        result = payload.context
        
        return result
    
    def _post_process(self, prediction: List) -> ZSCResult:
        logger.debug("Post-processing prediction..")
        
        # returned data is a List of Dicts
        result_raw = prediction[0]
        result_raw = [{"label":label.strip(), "score":score} for label, score in zip(result_raw["labels"], result_raw["scores"])]
        result = ZSCResult(entities=result_raw)
        
        return result

    def _output(self, context: str) -> List:
        logger.debug("Predicting..")
        
        context = self._split_context(context)
        
        if len(context) > 1:
            # If chunks created, evaluate each chunk then take average score for each label

            result = self.engine(context[0], **self.model_params)
            scores = np.array(result['scores'])
            labels = np.array(result['labels'])
            
            for chunk in context[1:]:
                result = self.engine(chunk, **self.model_params)
                scores += np.array(result['scores'])
                
            scores = [{"labels":labels, "scores":scores/len(context)}]
        else:
            scores = self.engine(context, **self.model_params)

        return scores

    def output(self, payload: BasePayload) -> ZSCResult:
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
