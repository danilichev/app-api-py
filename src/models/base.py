from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    id: Any
