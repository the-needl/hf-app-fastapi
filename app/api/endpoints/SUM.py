from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.SUM import SUMModel
from app.engine.result import SUMResult
from app.engine.payload import SUMPayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SUMResult, name="run")
async def summarize(
    request: Request,
    payload: SUMPayload,
) -> SUMResult:

    model: SUMModel = request.app.state.models[settings.MODEL_TYPE]
    output: SUMResult = model.predict(payload)

    return output