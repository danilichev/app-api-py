from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from .base import Base


class Post(Base):
    content: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    user = relationship("User", back_populates="posts")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    @classmethod
    async def create(
        cls, db_session: AsyncSession, content: str, title: str, user_id: uuid.UUID
    ):
        post = await super().create(
            db_session, content=content, title=title, user_id=user_id
        )
        return post
