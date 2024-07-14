from uuid import UUID

from pydantic import EmailStr, SecretStr

from .base import BaseDto


class TokenDto(BaseDto):
    access_token: str
    token_type: str = "bearer"


class CreateTokenDto(BaseDto):
    email: EmailStr
    password: SecretStr


class TokenPayloadDto(BaseDto):
    email: EmailStr
    expiry: float
    platform: str


class UserDto(BaseDto):
    email: EmailStr
    id: UUID


class CreateUserDto(BaseDto):
    email: EmailStr
    password: SecretStr


class CreateUserResponseDto(UserDto, TokenDto):
    pass
