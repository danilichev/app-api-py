from src.models.user import User
from src.schemas.user import UserDto


class UserMapper:
    @staticmethod
    def model_to_dto(model: User) -> UserDto:
        return UserDto(
            email=model.email,
            id=str(model.id),
        )
