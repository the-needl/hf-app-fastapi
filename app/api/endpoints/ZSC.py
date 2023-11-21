from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.ZSC import ZSCModel
from app.engine.result import ZSCResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ZSCResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> ZSCResult:

    model: ZSCModel = request.app.state.models[settings.MODEL_TYPE]
    output: ZSCResult = model.output(payload)

    return output