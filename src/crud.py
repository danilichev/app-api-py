from typing import Any, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# async def find_by_id(db_session: AsyncSession, model, id: Any):
#     result = await db_session.execute(select(model).where(model.id == id))
#     return result.scalars().first()


Model = TypeVar("Model")


async def find_by_id(db_session: AsyncSession, model: Model, id: Any) -> Model:
    result = await db_session.execute(select(model).where(model.id == id))
    return result.scalars().first()


async def find_by(db_session: AsyncSession, model, attribute: str, value: Any):
    result = await db_session.execute(
        select(model).where(getattr(model, attribute) == value)
    )
    return result.scalars().first()
