from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.SENT import SENTModel
from app.engine.result import SENTResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SENTResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> SENTResult:

    model: SENTModel = request.app.state.models[settings.MODEL_TYPE]
    output: SENTResult = model.output(payload)

    return output