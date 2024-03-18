from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_async_session
from src.models.post import Post
from src.schemas.post import CreatePostDto, PostDto


router = APIRouter()


@router.post("/post", response_model=PostDto, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: CreatePostDto, db_session: AsyncSession = Depends(get_db_async_session)
):
    new_post = Post(title=post.title, content=post.content)
    await new_post.save(db_session)
    return PostDto(
        content=new_post.content,
        id=str(new_post.id),
        title=new_post.title,
    )
