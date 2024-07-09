import json
import logging
import time
import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis.asyncio import Redis
from typing import TypedDict

from src.config import config
from src.models.user import User

# https://github.com/pyca/bcrypt/issues/684
logging.getLogger("passlib").setLevel(logging.ERROR)


def get_redis(request: Request) -> Redis:
    return request.app.redis


class AuthBearer(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials.credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        redis = get_redis(request)

        token_payload = await redis.get(credentials.credentials)

        if not token_payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return credentials.credentials


class AccessTokenPayload(TypedDict):
    email: str
    expiry: float
    platform: str


async def create_access_token(user: User, request: Request) -> str | None:
    payload: AccessTokenPayload = {
        "email": user.email,
        "expiry": time.time() + config.jwt_expire,
        "platform": request.headers.get("User-Agent"),
    }

    token = jwt.encode(payload, str(user.password), algorithm=config.jwt_algorithm)

    redis = get_redis(request)

    saved = await redis.set(token, json.dumps(payload), ex=config.jwt_expire)

    return token if saved else None


async def get_access_token_payload(
    token: str, request: Request
) -> AccessTokenPayload | None:
    redis = get_redis(request)

    payload = await redis.get(token)

    return json.loads(payload) if payload else None
