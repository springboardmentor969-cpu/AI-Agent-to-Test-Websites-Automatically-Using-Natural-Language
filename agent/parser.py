def parse_instruction(text):
    actions = []

    text = text.lower()

    if "open" in text:
        actions.append({"action": "open", "target": "website"})

    if "login" in text:
        actions.append({"action": "click", "target": "login_button"})

    if "enter username" in text:
        actions.append({"action": "type", "target": "username"})

    if "enter password" in text:
        actions.append({"action": "type", "target": "password"})

    return actions
