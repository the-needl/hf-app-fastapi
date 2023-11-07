import logging
import sys

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.config import settings
from app.config.event_handlers import start_app_handler, stop_app_handler
from app.api.router import api_router
from app.models import * #SUM, KEY, NER - Import everything for managing models via config

logger = logging.getLogger(__name__)

def __setup_logging(log_level: str):
    log_level = getattr(logging, log_level.upper())
    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)
    logger.info("Set up logging with log level %s", log_level)
    
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    for model_name in settings.MODELS_TO_RUN:
        try:
            model = globals()[model_name]
            start_app_handler(app, model)
        except KeyError:
            print(f"Model '{model_name}' not found in the 'models' module.")
    yield
    stop_app_handler(app)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, lifespan=lifespan)
app.include_router(api_router, prefix=settings.API_PREFIX)

def start():
    print("Running in AppEnvironment: " + settings.ENVIRONMENT.value)
    __setup_logging(settings.LOG_LEVEL)
    
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=settings.UVICORN_WORKER_COUNT
    )