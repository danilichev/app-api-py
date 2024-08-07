from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Security,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import get_db
from src.mappers.user import UserMapper
from src.models.user import User
from src.schemas.auth import AuthTokenDto, CreateAuthTokenDto
from src.schemas.user import (
    CreateUserDto,
    CreateUserResponseDto,
    UserDto,
    UserEstimatedAgeDto,
)
from src.services.age_estimator import AgeEstimator
from src.services.auth import AuthBearer, create_access_token, get_current_user
from src.utils.guards import image_guard


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", response_model=CreateUserResponseDto, status_code=status.HTTP_201_CREATED
)
async def create_user_endpoint(
    user: CreateUserDto, request: Request, db_session: AsyncSession = Depends(get_db)
):
    is_user_exists = bool(await User.find_by_email(db_session, user.email))

    if is_user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    new_user = await User.create(db_session, email=user.email, password=user.password)

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user"
        )

    access_token = await create_access_token(new_user, request)

    return CreateUserResponseDto(
        **UserMapper.model_to_dto(new_user).model_dump(),
        access_token=access_token,
    )


@router.post("/age-estimation", response_model=UserEstimatedAgeDto)
async def get_age_estimation_endpoint(
    image: UploadFile = Depends(image_guard()),
    token: str = Security(AuthBearer()),
):
    estimated_age, err = await AgeEstimator().estimate_age(image)

    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    return UserEstimatedAgeDto(estimated_age=estimated_age)


@router.get("/me", response_model=UserDto)
async def get_current_user_endpoint(
    request: Request,
    db_session: AsyncSession = Depends(get_db),
    token: str = Security(AuthBearer()),
):
    current_user = await get_current_user(token, request, db_session)

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserMapper.model_to_dto(current_user)


@router.post("/token", response_model=AuthTokenDto, status_code=status.HTTP_201_CREATED)
async def create_token_endpoint(
    credentials: CreateAuthTokenDto,
    request: Request,
    db_session: AsyncSession = Depends(get_db),
):
    user = await User.find_by_email(db_session, credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.check_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = await create_access_token(user, request)

    return AuthTokenDto(access_token=access_token)
