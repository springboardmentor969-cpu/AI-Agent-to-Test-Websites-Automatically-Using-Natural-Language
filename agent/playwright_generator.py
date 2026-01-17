def generate_steps(intent):
    steps = []

    if intent["action"] == "open_google":
        steps.append("page.goto('https://www.google.com')")

    elif intent["action"] == "search":
        steps.extend([
            "page.goto('https://www.google.com')",
            f"page.fill(\"input[name='q']\", '{intent['query']}')",
            "page.keyboard.press('Enter')"
        ])

    return steps
