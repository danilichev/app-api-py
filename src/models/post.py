import uuid
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Post(Base):
    __name__ = "posts"
    content: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
