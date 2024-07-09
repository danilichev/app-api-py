import time
import jwt

from src.config import config
from src.models.user import User

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .redis import get_from_redis, set_to_redis


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

        if not await self.verify_jwt(request, credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return credentials.credentials

    async def verify_jwt(self, request: Request, token: str) -> bool:
        payload = await get_from_redis(request, token)
        return bool(payload)


async def create_access_token(user: User, request: Request):
    payload = {
        "email": user.email,
        "expiry": time.time() + config.jwt_expire,
        "platform": request.headers.get("User-Agent"),
    }

    token = jwt.encode(payload, str(user.password), algorithm=config.jwt_algorithm)

    saved = await set_to_redis(request, token, str(payload), ex=config.jwt_expire)

    return token if saved else None
