from typing import Callable, Type

from fastapi import FastAPI
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

def _startup_model(app: FastAPI, Model: Type) -> None:
    model_path = settings.DEFAULT_MODEL_PATH
    model_instance = Model(model_path)
    #setattr(app, f"state.{model_instance.model_name}")
    app.state.model = model_instance

def start_app_handler(app: FastAPI, Model: Type) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app, Model)

    return startup

def stop_app_handler(app: FastAPI, model: str) -> Callable:
    def shutdown() -> None:
        logger.info(f"Running app shutdown handler on: {model}..")
        _shutdown_model(app, model)

    return shutdown

def _shutdown_model(app: FastAPI, model: str) -> None:
    #setattr(app, f"state.{model}", None)
    app.state.model = None