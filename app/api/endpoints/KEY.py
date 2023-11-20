from fastapi import APIRouter, Request

import logging

from app.core.config import settings

from app.engine.instances.KEY import KEYModel
from app.engine.result import KEYResult
from app.engine.payload import KEYPayload

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=KEYResult, name="run")
async def summarize(
    request: Request,
    payload: KEYPayload,
) -> KEYResult:

    model: KEYModel = request.app.state.models[settings.MODEL_TYPE]
    output: KEYResult = model.predict(payload)

    return output