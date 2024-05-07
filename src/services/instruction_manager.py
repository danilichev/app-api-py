from typing import Dict, List


class InstructionManager:
    def __init__(self):
        self.instructions: Dict[str, List[str]] = {}

    def add_instruction(self, client_id: str, instruction: str):
        self.get_instructions(client_id).append(instruction)

    def get_instructions(self, client_id: str) -> List[str]:
        if client_id not in self.instructions:
            self.instructions[client_id] = []
        return self.instructions[client_id]

    def has_instructions(self, client_id: str) -> bool:
        return len(self.get_instructions(client_id)) > 0

    def remove_instructions(self, client_id: str):
        self.instructions[client_id] = []


manager = InstructionManager()
