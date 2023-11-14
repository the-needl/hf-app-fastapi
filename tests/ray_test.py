from starlette.requests import Request
from typing import Dict

from transformers import pipeline

from ray import serve


# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("summarization", model="sshleifer/distilbart-xsum-12-1")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]

main = SentimentAnalysisDeployment.bind()