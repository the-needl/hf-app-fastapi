from fastapi import Depends, APIRouter, Request

import anyio
from uuid import uuid4
import datetime
import asyncio
import logging
from collections import OrderedDict

from app.core.config import settings

from app.models.model import SUMModel
from app.models.result import SUMResult
from app.models.payload import SUMPayload

from uuid import UUID

from typing import Dict, Any

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SUMResult, name="summary")
async def summarize(
    request: Request,
    payload: SUMPayload,
) -> SUMResult:

    model: SUMModel = request.app.state.models[settings.MODEL_TYPE]
    summary: SUMResult = model.predict(payload)

    return summary