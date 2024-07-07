from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class BaseUserDto(BaseModel):
    email: EmailStr


class TokenDto(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserDto(BaseUserDto):
    id: UUID


class CreateUserDto(BaseUserDto):
    password: SecretStr


class CreateUserResponseDto(UserDto, TokenDto):
    pass
