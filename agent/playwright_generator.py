def generate_playwright_steps(steps):
    code_steps = []

    for step in steps:
        if step["action"] == "open_browser":
            code_steps.append(f'page.goto("{step["url"]}")')

        elif step["action"] == "click":
            code_steps.append(f'page.click("{step["selector"]}")')

        elif step["action"] == "submit":
            code_steps.append(f'page.click("{step["selector"]}")')

    return code_steps
