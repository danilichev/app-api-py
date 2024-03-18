from pydantic import BaseModel, Field


class CreatePostDto(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    content: str


class PostDto(CreatePostDto):
    id: str
