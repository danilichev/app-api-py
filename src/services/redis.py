from fastapi import Request


async def get_from_redis(request: Request, key: str):
    return await request.app.redis.get(key)


async def set_to_redis(request: Request, key: str, value: str, ex: int):
    return await request.app.redis.set(key, value, ex=ex)
