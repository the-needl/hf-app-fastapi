from typing import Callable, Type

from fastapi import FastAPI
import logging

from app.models.base import Base

logger = logging.getLogger(__name__)

def _startup_model(app: FastAPI, model_instance: Base) -> None:
    app.state.model = model_instance

def start_app_handler(app: FastAPI, model_instance: Base) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app, model_instance)

    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info(f"Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown

def _shutdown_model(app: FastAPI) -> None:
    #setattr(app, f"state.{model}", None)
    app.state.model = None