import re

def parse_instruction(text: str):
    text = text.lower().strip()

    command = {
        "action": None,
        "target": None,
        "value": None
    }

    if "open" in text or "navigate" in text:
        if "login" in text:
            command["action"] = "navigate"
            command["target"] = "login_page"

    if "click" in text:
        match = re.search(r"click (.+)", text)
        if match:
            command["action"] = "click"
            command["target"] = match.group(1).replace(" ", "_")

    if "enter" in text or "type" in text:
        match = re.search(r"(enter|type) (.+?) in (.+)", text)
        if match:
            command["action"] = "type"
            command["value"] = match.group(2)
            command["target"] = match.group(3).replace(" ", "_")

    return command
