from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api import ping, post, user
from src.infra.redis import get_cache, get_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.redis = await get_redis()

    try:
        redis_cache = await get_cache()
        FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
        yield
    finally:
        app.redis.close()


app = FastAPI(lifespan=lifespan)

route_config = {"prefix": "/api"}

app.include_router(ping.router, **route_config)
app.include_router(post.router, **route_config)
app.include_router(user.router, **route_config)
