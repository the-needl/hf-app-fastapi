from fastapi import APIRouter

from app.api.endpoints import SUM #,health, NER, KEY, QA

api_router = APIRouter()

api_router.include_router(SUM.router, prefix="/sum", tags=["summary"])
# api_router.include_router(health.router, prefix="/alive", tags=["health"])

# api_router.include_router(NER.router, prefix="/ner", tags=["ner"])
# api_router.include_router(KEY.router, prefix="/key", tags=["key"])
# api_router.include_router(KEY.router, prefix="/qa", tags=["qa"])