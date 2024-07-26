from uuid import UUID
from pydantic import EmailStr, SecretStr

from .auth import AuthTokenDto
from .base import BaseDto


class UserDto(BaseDto):
    email: EmailStr
    id: UUID


class CreateUserDto(BaseDto):
    email: EmailStr
    password: SecretStr


class CreateUserResponseDto(UserDto, AuthTokenDto):
    pass


class UserEstimatedAgeDto(BaseDto):
    estimated_age: int
