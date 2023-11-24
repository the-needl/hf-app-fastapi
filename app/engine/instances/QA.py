from typing import List

import logging

import numpy as np

from transformers import AutoTokenizer, DistilBertForQuestionAnswering, pipeline

from app.core.config import settings
from app.core.messages import NO_VALID_PAYLOAD

from app.engine.models import Base
from app.engine.payload import BasePayload
from app.engine.result import QAResult

logger = logging.getLogger(__name__)

_questions = ["who", "what", "where", "why", "when"]

class QAModel(Base):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': DistilBertForQuestionAnswering,
            'tokenizer_loader': AutoTokenizer
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        # model_params as list of dicts, each containing a different quest. Model not able to process chunks o quests
        self.questions = [q+"?" for q in _questions]
        self.engine = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)
    
    def _pre_process(self, payload: BasePayload) -> str:
        logger.debug("Pre-processing payload..")
        result = payload.context
        
        return result
    
    def _post_process(self, prediction: List) -> QAResult:
        logger.debug("Post-processing prediction..")
        
        # returned data is a List of Dicts
        result_raw = [{"question":res["question"],"answer":res["answer"],"score":res["score"]} for res in prediction]
        # result_raw = [{"answer":answer.strip(), "score":score} for answer, score in zip(result_raw["answer"], result_raw["score"])]
        result = QAResult(answers=result_raw)
        
        return result

    def _output(self, context: str) -> List:
        logger.debug("Predicting..")
        
        context = self._split_context(context)
        
        if len(context) > 1:
            raise ValueError("Context too long for model. Try shorter context!")
            # If chunks created, evaluate each chunk then take average score for each label
        else:
            answers = []
            
            for q in self.questions:
                ans = self.engine(question=q, context=context[0])
                ans["question"] = q
                answers.append(ans)

        return answers

    def output(self, payload: BasePayload) -> QAResult:
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
