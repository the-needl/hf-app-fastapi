from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.EMB import EMBModel
from app.engine.result import EMBResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=EMBResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> EMBResult:

    model: EMBModel = request.app.state.models[settings.MODEL_TYPE]
    output: EMBResult = model.output(payload)

    return output