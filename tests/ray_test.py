from fastapi import FastAPI
import torch
from transformers import pipeline

import os

from ray import serve
from ray.serve.handle import DeploymentHandle


app = FastAPI()


@serve.deployment(
    ray_actor_options={"num_cpus": 1},
    num_replicas=16
)
@serve.ingress(app)
class APIIngress:
    def __init__(self) -> None:
        self.classifier = pipeline(
            "summarization",
            model="sshleifer/distilbart-xsum-12-3",
            # framework="pt",
            # Transformers requires you to pass device with index
            device=torch.device("cpu"),
        )

    @app.get("/sum")
    async def classify(self, sentence: str):
        return self.classifier(sentence)


entrypoint = APIIngress.bind()
