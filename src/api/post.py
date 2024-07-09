from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.mappers.post import PostMapper
from src.models.post import Post
from src.schemas.post import CreatePostDto, PostDto
from src.services.auth import AuthBearer
from src.services.crud import create, find_by_id


router = APIRouter(prefix="/posts")


@router.post("/", response_model=PostDto, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(
    post: CreatePostDto,
    db_session: AsyncSession = Depends(get_db),
    token: str = Security(AuthBearer()),
):
    new_post = await create(
        db_session, Post(content=post.content, title=post.title, user_id=post.user_id)
    )
    return PostMapper.model_to_dto(new_post)


@router.get("/", response_model=PostDto, status_code=status.HTTP_200_OK)
async def get_post_endpoint(id: str, db_session: AsyncSession = Depends(get_db)):
    post = await find_by_id(db_session, Post, id)
    return PostMapper.model_to_dto(post)
