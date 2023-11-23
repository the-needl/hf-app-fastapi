from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.QA import QAModel
from app.engine.result import QAResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=QAResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> QAResult:

    model: QAModel = request.app.state.models[settings.MODEL_TYPE]
    output: QAResult = model.output(payload)

    return output