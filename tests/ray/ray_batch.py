from typing import List

from starlette.requests import Request
from transformers import pipeline

from ray import serve

@serve.deployment(       
    ray_actor_options={"num_cpus": 0.1},
    num_replicas=10,
)    
class BatchTextGenerator:
    def __init__(self, pipeline_key: str, model_key: str):
        self.model = pipeline(pipeline_key, model_key)

    @serve.batch(max_batch_size=10)
    async def handle_batch(self, inputs: List[str]) -> List[str]:
        print("Our input array has length:", len(inputs))

        results = self.model(inputs)
        print(results)
        return [result["summary_text"] for result in results]

    async def __call__(self, request: Request) -> List[str]:
        return await self.handle_batch(request.query_params["text"])
    
generator = BatchTextGenerator.bind("summarization", "sshleifer/distilbart-xsum-12-3")