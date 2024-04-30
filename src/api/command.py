from fastapi import APIRouter, status
from pydantic import BaseModel

from .ws.connection_manager import manager as ws_manager


class SendCommandDto(BaseModel):
    command: str


class SendCommandResponseDto(BaseModel):
    success: bool


router = APIRouter()


@router.post(
    "/command", response_model=SendCommandResponseDto, status_code=status.HTTP_200_OK
)
async def send_command_endpoint(post: SendCommandDto):
    await ws_manager.send_message(post.command)
    return SendCommandResponseDto(success=True)
