# playwright_generator.py
def generate_actions(commands: list, target=None):
    actions = []
    for cmd in commands:
        if cmd == "login":
            actions += [
                'page.goto("http://127.0.0.1:5000/login")',
                'page.fill("#username", "testuser")',
                'page.fill("#password", "password")',
                'page.click("#login-btn")',
                'page.wait_for_selector("#login-status")',
                'result = page.inner_text("#login-status")'
            ]
        elif cmd == "search":
            q = target.strip() if target else "laptop"
            actions += [
                f'page.goto("http://127.0.0.1:5000/search")',
                f'page.fill("#query", "{q}")',
                'page.click("#search-btn")',
                'page.wait_for_selector("#search-status")',
                'result = page.inner_text("#search-status")'
            ]
        else:
            actions.append('raise Exception("Unsupported command")')
    return actions