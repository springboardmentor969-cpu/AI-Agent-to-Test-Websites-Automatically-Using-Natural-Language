def generate_steps(intent: dict):
    steps = []

    if intent["action"] == "open":
        steps.append({"type": "goto", "url": intent["url"]})

    elif intent["action"] == "search":
        steps.extend([
            {"type": "goto", "url": intent["url"]},
            {"type": "fill", "selector": "input[name='q']", "value": intent["query"]},
            {"type": "press", "key": "Enter"}
        ])

    return steps
