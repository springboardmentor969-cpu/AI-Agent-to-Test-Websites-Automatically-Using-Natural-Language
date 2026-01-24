
from typing import Dict, List
def parse_instruction(text: str) -> Dict:
    text = text.lower()
    commands: List[str] = []
    if "login" in text:
        commands.append("login")
    if "search" in text:
        commands.append("search")
    if not commands:
        commands.append("unsupported")
    return {
        "raw": text,
        "commands": commands
    }