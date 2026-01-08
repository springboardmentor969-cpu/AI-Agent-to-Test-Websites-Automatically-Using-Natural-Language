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
        parsed_data["element"] = "google"
        parsed_data["action"] = "open"

    # Identify action
    elif "check" in instruction or "verify" in instruction or "validate" in instruction:
        parsed_data["action"] = "verify_visibility"

    # Identify element
    elif "search" in instruction:
        parsed_data["element"] = "search_box"
    
    elif "open" in instruction or "navigate" in instruction:
        parsed_data["action"] = "open"
    
    elif "click" in instruction:
        parsed_data["action"] = "click"
    
    elif "fill" in instruction or "enter" in instruction:
        parsed_data["action"] = "fill"


    # Detect target/page
    elif "homepage" in instruction or "home page" in instruction:
        parsed_data["url"] = "/home"
        parsed_data["element"] = "homepage"

    elif "login page" in instruction:
        parsed_data["url"] = "/login"
        parsed_data["element"] = "login page"

    elif "signup button" in instruction:
        parsed_data["element"] = "signup button"

    elif "profile page" in instruction:
        parsed_data["url"] = "/profile"
        parsed_data["element"] = "profile page"

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
    # if parsed_data["action"] == "open" and parsed_data["url"]:
    #     commands.append({
    #         "command": "open_url",
    #         "value": parsed_data["url"]
    #     })

    # if parsed_data["action"] in ["check", "verify"] and parsed_data["element"]:
    #     commands.append({
    #         "command": "assert_element",
    #         "value": parsed_data["element"]
    #     })
    # if parsed_data["action"] == "open" and parsed_data["url"]:
    #     commands.append({
    #         "command": "open_url",
    #         "value": parsed_data["url"]
    #     })

    # Verify element or title
    elif parsed_data["action"] == "verify" and parsed_data["element"]:
        commands.append({
            "command": "assert_element",
            "value": parsed_data["element"]
        })

    # Click action
    elif parsed_data["action"] == "click" and parsed_data["element"]:
        commands.append({
            "command": "click_element",
            "value": parsed_data["element"]
        })

    # Fill input field
    elif parsed_data["action"] == "fill" and parsed_data["element"]:
        commands.append({
            "command": "fill_input",
            "value": parsed_data["element"]
        })
    return commands
