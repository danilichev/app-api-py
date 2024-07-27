from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import get_db
from src.mappers.post import PostMapper
from src.models.post import Post
from src.schemas.post import CreatePostDto, PostDto
from src.services.auth import AuthBearer, get_current_user


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostDto, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(
    post: CreatePostDto,
    request: Request,
    db_session: AsyncSession = Depends(get_db),
    token: str = Security(AuthBearer()),
):
    current_user = await get_current_user(token, request, db_session)

    if current_user is None or current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not allowed to create post",
        )

    new_post = await Post.create(
        db_session, title=post.title, content=post.content, user_id=post.user_id
    )

    if new_post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create post"
        )

    return PostMapper.model_to_dto(new_post)


@router.get("/{post_id}", response_model=PostDto, status_code=status.HTTP_200_OK)
async def get_post_endpoint(id: str, db_session: AsyncSession = Depends(get_db)):
    post = await Post.find_by_id(db_session, id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return PostMapper.model_to_dto(post)
