from typing import Callable, Type

from fastapi import FastAPI
import logging

from app.config.config import settings

logger = logging.getLogger(__name__)

def _startup_model(app: FastAPI, Model:Type) -> None:
    model_path = settings.DEFAULT_MODEL_PATH
    model_instance = Model(model_path)
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