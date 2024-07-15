from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Any, Optional, TypeVar
import uuid

from src.utils.strings import add_plural_suffix
import src.services.crud as crud

T = TypeVar("T", bound="Base")


class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return add_plural_suffix(self.__name__.lower())

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    @classmethod
    async def create(cls: type[T], db_session: AsyncSession, **kwargs) -> Optional[T]:
        instance = cls(**kwargs)
        return await crud.create(db_session, instance)

    @classmethod
    async def find_by(
        cls: type[T], db_session: AsyncSession, attribute: str, value: Any
    ) -> Optional[T]:
        return await crud.find_by(db_session, cls, attribute, value)

    @classmethod
    async def find_by_id(
        cls: type[T], db_session: AsyncSession, id: str
    ) -> Optional[T]:
        return await crud.find_by_id(db_session, cls, "id", id)
