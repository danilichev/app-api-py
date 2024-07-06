from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import create, find_by_id
from src.db import get_db
from src.models.post import Post
from src.schemas.post import CreatePostDto, PostDto


router = APIRouter()


@router.post("/post", response_model=PostDto, status_code=status.HTTP_201_CREATED)
async def create_post(post: CreatePostDto, db_session: AsyncSession = Depends(get_db)):
    new_post = await create(db_session, Post(title=post.title, content=post.content))
    return PostDto(
        content=new_post.content,
        id=str(new_post.id),
        title=new_post.title,
    )


@router.get("/post", response_model=PostDto, status_code=status.HTTP_200_OK)
async def get_post(id: str, db_session: AsyncSession = Depends(get_db)):
    post = await find_by_id(db_session, Post, id)
    return PostDto(
        content=post.content,
        id=str(post.id),
        title=post.title,
    )
