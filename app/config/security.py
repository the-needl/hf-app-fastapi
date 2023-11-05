import secrets
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.config.config import settings
from app.config.messages import AUTH_REQ, NO_API_KEY

api_key = APIKeyHeader(name="token", auto_error=False)


def validate_request(header: Optional[str] = Security(api_key)) -> bool:
    if header is None:
        raise HTTPException(
            status_code=400, detail=NO_API_KEY, headers={}
        )
    if not secrets.compare_digest(header, str(settings.API_KEY)):
        raise HTTPException(
            status_code=401, detail=AUTH_REQ, headers={}
        )
    return True