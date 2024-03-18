from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from .config import config


engine = create_async_engine(config.db_url)
make_async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_async_session() -> AsyncGenerator:
    async with make_async_session() as session:
        yield session
