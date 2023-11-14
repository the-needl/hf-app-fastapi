import logging
import sys
import time

# import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routers import api_router
from app.models.model import create_instance

from app.models.model import SUMModel
from app.models.result import SUMResult
from app.models.payload import SUMPayload

from ray import serve


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
    app.state.models[settings.MODEL_TYPE] = create_instance(settings.MODEL_TYPE)
    yield
    app.state.models.clear()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
    )

app.include_router(api_router, prefix=settings.API_PREFIX)

@serve.deployment
@serve.ingress(app)
class HFModel:
    def __init__(self):
        self._model = create_instance(settings.MODEL_TYPE)

    @app.post("/sum")
    async def summarize(
        self,
        # request: Request,
        payload: SUMPayload,
    ) -> SUMResult:

        # model: SUMModel = request.app.state.models[settings.MODEL_TYPE]
        summary: SUMResult = self._model.predict(payload)

        return summary
    
    @app.get("/test")
    async def test():
        return "prova test"


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
    # uvicorn.run(
    #     "app.main:app",
    #     host="0.0.0.0",
    #     port=8000,
    #     reload=True,
    #     workers=settings.UVICORN_WORKER_COUNT
    # )
main = HFModel.bind()
    # serve.run(main, route_prefix="/api")

