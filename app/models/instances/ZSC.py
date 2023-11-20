# {
#   "sequence": "Top OpenAI executives have swung behind Sam Altman, as a groundswell of support from employees and investors raised pressure on board members to reinstate the chief executive of the company behind ChatGPT who they sacked on Friday.\n\nVenture backers and executives at Microsoft — which has committed more than $10bn to OpenAI and is expected to have a key role in negotiations — were exploring options this weekend including clearing out the board and reinstating Altman, according to three people briefed on the discussions.\n\nIn a memo circulated to staff of the generative artificial intelligence company late on Saturday night, chief strategy officer Jason Kwon said he was “optimistic” that Altman and co-founder Greg Brockman — who quit on Friday — would return, according to a person with direct knowledge of its contents. The memo’s existence was first reported by The Information.\n\nAccording to one person with knowledge of the situation, Altman had been attempting to raise as much as $100bn from investors in the Middle East and SoftBank founder Masayoshi Son to establish a new microchip development company which could compete with Nvidia and TSMC. Those efforts, in the weeks before his sacking, had caused concerns on the board, this person said.\n\nAltman’s firing shocked Silicon Valley. The 38-year old has become a leading voice on generative AI, a technology which has had a breakthrough year in part thanks to OpenAI’s launch of ChatGPT in November 2022.\n\nAltman has also become a de facto ambassador for AI start-ups, meeting presidents, prime ministers and regulators on a world tour earlier this year and speaking at the Apec Asia-Pacific regional summit in San Francisco just a day before he was sacked.\n\nWith the board and his backers at an impasse on Saturday night, Altman posted “i love the openai team so much” on X. Within an hour hundreds of employees still at OpenAI — including interim CEO Mira Murati and chief operating officer Brad Lightcap — had liked or reposted the tweet.\n\nInvestors also rallied behind Altman over the weekend. The company’s biggest venture capitalist backers — including Thrive Capital, its second-largest shareholder, Tiger Global, Khosla Ventures and Sequoia Capital — have signalled their support for Altman in whatever he does next. That includes a possible return as OpenAI’s CEO, according to several people with direct knowledge of the matter.\n\nWhile they have no seats on the non-profit board which ultimately controls OpenAI, investors could refuse further backing and employees could quit the company in an attempt to force the board’s hand.\n\nA plan to sell as much as $1bn in employee stock, which was nearing completion, is in the balance as a result of the division between the board and investors. Thrive Capital was set to lead that tender offer, which was expected to value OpenAI at $86bn.",
#   "labels": [
#     "news article",
#     " other"
#   ],
#   "scores": [
#     0.5095037221908569,
#     0.49049627780914307
#   ],
#   "warnings": [
#     "The `multi_class` argument has been deprecated and renamed to `multi_label`. `multi_class` will be removed in a future version of Transformers."
#   ]
# }

from typing import Dict, List
from pydantic import BaseModel

import logging

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from app.core.config import settings
from app.models.base import Base

from app.models.payload import ZSCPayload
from app.models.result import ZSCResult
from app.core.messages import NO_VALID_PAYLOAD

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

        self.engine = pipeline("zero-shot-classification", model=self.model, tokenizer=self.tokenizer)

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
        
        SUM_input = context
        prediction_result = self.engine(SUM_input)

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