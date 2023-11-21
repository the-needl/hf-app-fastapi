from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.SUM import SUMModel
from app.engine.result import SUMResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SUMResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> SUMResult:

    model: SUMModel = request.app.state.models[settings.MODEL_TYPE]
    output: SUMResult = model.output(payload)

    return output