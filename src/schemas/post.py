from uuid import UUID

from pydantic import Field

from .base import BaseDto


class CreatePostDto(BaseDto):
    content: str
    title: str = Field(min_length=3, max_length=100)
    user_id: UUID


class PostDto(CreatePostDto):
    id: UUID
