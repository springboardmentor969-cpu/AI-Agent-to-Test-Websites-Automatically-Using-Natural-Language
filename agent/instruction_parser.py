def parse_instruction(instruction: str):
    
    instruction = instruction.lower()
    actions = []

    # -------- PAGE NAVIGATION --------
    if "open" in instruction or "navigate" in instruction:
        page = "unknown page"

        if "home" in instruction:
            page = "home page"
        elif "dashboard" in instruction:
            page = "dashboard page"
        elif "profile" in instruction:
            page = "profile page"
        elif "settings" in instruction:
            page = "settings page"

        actions.append({
            "action": "open_page",
            "target": page
        })

    # -------- TEXT INPUT --------
    if "enter" in instruction or "type" in instruction:
        if "username" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "username field"
            })

        if "password" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "password field"
            })

        if "email" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "email field"
            })

    # -------- CLICK ACTION --------
    if "click" in instruction or "submit" in instruction:
        button = "button"

        if "submit" in instruction:
            button = "submit button"
        elif "login" in instruction:
            button = "login button"
        elif "save" in instruction:
            button = "save button"

        actions.append({
            "action": "click",
            "target": button
        })

    return actions
