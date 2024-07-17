from pydantic import EmailStr, SecretStr

from .base import BaseDto


class AuthTokenDto(BaseDto):
    access_token: str
    token_type: str = "bearer"


class CreateAuthTokenDto(BaseDto):
    email: EmailStr
    password: SecretStr
