import logging
import sys
import time

import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.factory import create_instance, create_router

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

local_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.models = {}
    app.state.models[settings.MODEL_TYPE] = create_instance()
    yield
    app.state.models.clear()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan)

app.include_router(create_router(settings.MODEL_TYPE), prefix=settings.API_PREFIX)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

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