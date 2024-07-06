from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


async def create(db_session: AsyncSession, model: Model) -> Model:
    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return model


async def find_by(
    db_session: AsyncSession, model: Model, attribute: str, value: Any
) -> Model | None:
    result = await db_session.execute(
        select(model).where(getattr(model, attribute) == value)
    )
    return result.scalars().first()


async def find_by_id(db_session: AsyncSession, model: Model, id: Any) -> Model | None:
    result = await find_by(db_session, model, "id", id)
    return result
