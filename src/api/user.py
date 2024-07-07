from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.mappers.user import UserMapper
from src.models.user import User
from src.schemas.user import CreateUserDto, UserDto
from src.services.crud import create


router = APIRouter(prefix="/user")


@router.post("/", response_model=UserDto, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: CreateUserDto, db_session: AsyncSession = Depends(get_db)
):
    new_user = await create(db_session, User(email=user.email, password=user.password))
    return UserMapper.model_to_dto(new_user)
