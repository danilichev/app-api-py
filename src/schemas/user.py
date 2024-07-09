from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class TokenDto(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CreateTokenDto(BaseModel):
    email: EmailStr
    password: SecretStr


class UserDto(BaseModel):
    email: EmailStr
    id: UUID


class CreateUserDto(BaseModel):
    email: EmailStr
    password: SecretStr


class CreateUserResponseDto(UserDto, TokenDto):
    pass
