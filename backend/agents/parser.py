def parse_instruction(state):
    text = state["instruction"].lower()
    steps = []

    if "open" in text:
        steps.append({"action": "open"})

    if "email" in text:
        steps.append({
            "action": "fill",
            "selector": "#email",
            "value": "test@example.com"
        })

    if "click" in text:
        steps.append({
            "action": "click",
            "selector": "#submit"
        })

    if "verify" in text or "success" in text:
        steps.append({
            "action": "assert_text",
            "text": "Success"
        })

    return {"steps": steps}
