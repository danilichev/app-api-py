from uuid import UUID

from pydantic import BaseModel, Field


class CreatePostDto(BaseModel):
    content: str
    title: str = Field(min_length=3, max_length=100)


class PostDto(CreatePostDto):
    id: UUID
