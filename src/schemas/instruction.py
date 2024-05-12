from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel


class AutomationDto(BaseModel):
    automation: str
    client_id: str
    id: str
    status: str  # "inactive" | "started" | "paused" | "stopped"


class CreateAutomationDto(BaseModel):
    automation: str
    client_id: str


class CreateAutomationResponseDto(BaseModel):
    automation: str
    client_id: str
    id: str
    status: str  # "inactive"


class DataToInstructionDto(BaseModel):
    automation_id: str
    client_id: str
    instruction_id: Optional[str] = None
    message: Optional[str] = (
        None  # "start automation" | "pause automation" | "stop automation"
    )
    screenshot: Optional[UploadFile] = None


class InstructionDto(BaseModel):
    id: str
    instruction: str


class InstructionsDto(BaseModel):
    automation_id: str
    client_id: str
    instructions: List[InstructionDto]


# Create Automation:
# POST /automations
# Pause/Stop Automation:
# PATCH /automations/{automation_id}/
# Get Instructions:
# GET /automations/{automation_id}/instructions
# Post instruction result:
# POST /automations/{automation_id}/instructions/{instruction_id}/result
