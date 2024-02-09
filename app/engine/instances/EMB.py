from typing import List

import logging

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.messages import NO_VALID_PAYLOAD

from app.engine.models import EmbeddingBase
from app.engine.payload import EMBPayload
from app.engine.result import EMBResult

logger = logging.getLogger(__name__)

class EMBModel(EmbeddingBase):
    def __init__(self, *args, **kwargs):
        
        model_args = {
            'model_name': settings.MODEL_NAME,
            'model_path': settings.DEFAULT_MODEL_PATH,
            'model_loader': SentenceTransformer,
        }
        model_args.update(kwargs)
        
        super().__init__(*args, **model_args)

        self.model_params = {"aggregation_strategy":"simple"}
        self.engine = self.model.encode
    
    def _pre_process(self, payload: EMBPayload) -> str:
        logger.debug("Pre-processing payload..")
        result = payload.context
        
        return result
    
    def _post_process(self, prediction: List) -> EMBResult:
        logger.debug("Post-processing prediction..")
        
        # returned data is a List of Dicts
        result_raw = prediction
        result = EMBResult(embeddings=result_raw)
        
        return result

    def _output(self, context: List[str]) -> List:
            """
            Embeds a list of contexts.

            Args:
                context (List[str]): A list of contexts to be embedded.

            Returns:
                List: A list of embeddings for the input contexts.
            """
            
            logger.debug("Embedding..")
            
            try:
                embs = self.engine(context)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                embs = []

            return embs

    def output(self, payload: EMBPayload) -> EMBResult:
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
