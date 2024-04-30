from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __name__: str

    id: Any

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    async def find_by_id(self, db_session: AsyncSession, id: Any):
        result = await db_session.execute(select(self).where(self.id == id))
        return result.scalars().first()

    async def save(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex
