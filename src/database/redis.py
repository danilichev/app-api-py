import redis.asyncio as redis

from src.config import config


async def get_cache():
    return await redis.from_url(
        config.redis_url.unicode_string(),
        decode_responses=False,
    )


async def get_redis():
    return await redis.from_url(
        config.redis_url.unicode_string(),
        encoding="utf-8",
        decode_responses=True,
    )
