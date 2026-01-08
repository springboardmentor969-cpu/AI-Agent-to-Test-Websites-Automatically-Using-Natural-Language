"""
parser.py
Parses natural language test instructions
and converts them into structured commands.
"""

from typing import Dict, List


def parse_instruction(instruction: str) -> Dict:
    """
    Extracts intent and target information
    from natural language instruction.
    """
    instruction = instruction.lower()

    parsed_data = {
        "url": None,
        "action": None,
        "element": None
    }

    # Identify website
    if "google" in instruction:
        parsed_data["url"] = "https://www.google.com"

    # Identify action
    if "check" in instruction or "verify" in instruction:
        parsed_data["action"] = "verify_visibility"

    # Identify element
    if "search" in instruction:
        parsed_data["element"] = "search_box"

    return parsed_data


def generate_commands(parsed_data: Dict) -> List[Dict]:
    """
    Converts parsed instruction into
    structured test commands.
    """
    commands = []

    if parsed_data.get("url"):
        commands.append({
            "command": "open_url",
            "value": parsed_data["url"]
        })

    if parsed_data.get("action") and parsed_data.get("element"):
        commands.append({
            "command": parsed_data["action"],
            "value": parsed_data["element"]
        })

    return commands
