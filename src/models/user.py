import uuid

import bcrypt
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy import String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    @property
    def password(self):
        return self.password_hash.decode("utf-8")

    @password.setter
    def password(self, password: SecretStr):
        password_str = password.get_secret_value()
        self.password_hash = bcrypt.hashpw(
            password_str.encode("utf-8"), bcrypt.gensalt()
        )

    def check_password(self, password: SecretStr):
        return pwd_context.verify(password.get_secret_value(), self.password)
