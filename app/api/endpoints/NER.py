from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.NER import NERModel
from app.engine.result import NERResult
from app.engine.payload import BasePayload


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=NERResult, name="run")
async def summarize(
    request: Request,
    payload: BasePayload,
) -> NERResult:

    model: NERModel = request.app.state.models[settings.MODEL_TYPE]
    output: NERResult = model.output(payload)

    return output