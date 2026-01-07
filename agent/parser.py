def parse_instruction(text):
    steps = []
    text = text.lower()

    if "open" in text or "launch" in text:
        steps.append({
            "action": "open_browser",
            "target": "url"
        })

    if "click" in text:
        steps.append({
            "action": "click",
            "target": "button"
        })

    if "enter" in text or "type" in text:
        steps.append({
            "action": "input",
            "target": "text_field"
        })

    if "submit" in text:
        steps.append({
            "action": "submit",
            "target": "form"
        })
        
    return steps