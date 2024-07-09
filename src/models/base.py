from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from src.utils.strings import add_plural_suffix


class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return add_plural_suffix(self.__name__.lower())
