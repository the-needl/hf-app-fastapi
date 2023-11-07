from typing import Callable

from fastapi import FastAPI
import logging

from app.config.config import settings
from app.services.models import QAModel

logger = logging.getLogger(__name__)

def _startup_model(app: FastAPI) -> None:
    model_path = settings.DEFAULT_MODEL_PATH
    model_instance = QAModel(model_path)
    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown