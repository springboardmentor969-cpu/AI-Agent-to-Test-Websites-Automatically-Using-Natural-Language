def generate_playwright_steps(parsed_steps):
    actions = []

    for step in parsed_steps:
        if step["action"] == "open_browser":
            actions.append("OPEN_BROWSER")

        elif step["action"] == "click":
            actions.append("CLICK")

        elif step["action"] == "input":
            actions.append("TYPE")

        elif step["action"] == "submit":
            actions.append("SUBMIT")

    return actions