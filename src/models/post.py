import uuid
from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base


class Post(Base):
    content: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    user = relationship("User", back_populates="posts")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
