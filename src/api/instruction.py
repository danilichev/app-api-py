from typing import Annotated, List
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.services.instruction_manager import manager as instruction_manager


class GetInstructionsResponseDto(BaseModel):
    instructions: List[str]


class PostInstructionDto(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
    client_id: str
    instruction: str


class PostInstructionResponseDto(BaseModel):
    success: bool


router = APIRouter()


@router.get(
    "/instruction",
    response_model=GetInstructionsResponseDto,
    status_code=status.HTTP_200_OK,
)
async def get_instruciton_endpoint(client_id: Annotated[str, Query(alias="clientId")]):
    instructions = instruction_manager.get_instructions(client_id)
    return GetInstructionsResponseDto(instructions=instructions)


@router.post(
    "/instruction",
    response_model=PostInstructionResponseDto,
    status_code=status.HTTP_200_OK,
)
async def post_instruciton_endpoint(post: PostInstructionDto):
    instruction_manager.add_instruction(post.client_id, post.instruction)
    return PostInstructionResponseDto(success=True)
