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

    elif intent["action"] == "login":
        steps.extend([
            {"type": "goto", "url": intent["url"]},
            {"type": "fill", "selector": "input[type='text'], input[name='username']", "value": intent.get("username", "")},
            {"type": "fill", "selector": "input[type='password'], input[name='password']", "value": intent.get("password", "")},
            {"type": "click", "selector": "button[type='submit'], button:has-text('Login'), button:has-text('Sign In')"}
        ])
    
    elif intent["action"] == "click":
        steps.append({"type": "click", "selector": intent.get("selector", "button")})
    
    elif intent["action"] == "fill":
        steps.append({"type": "fill", "selector": intent.get("selector", "input"), "value": intent.get("value", "")})
    
    elif intent["action"] == "wait":
        steps.append({"type": "wait", "duration": intent.get("duration", 3)})

    return steps
