def generate_playwright_code(parsed_steps):
    lines = [
        "from playwright.sync_api import sync_playwright\n",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=False)",
        "        page = browser.new_page()"
    ]

    for step in parsed_steps:
        if step["action"] in ["open", "open_url"]:
            lines.append(f"        page.goto('{step['value']}')")

        elif step["action"] == "fill":
            lines.append(
                f"        page.fill('{step['selector']}', '{step['text']}')"
            )

        elif step["action"] == "click":
            lines.append(
                f"        page.click('{step['value']}')"
            )

    lines.append("        browser.close()")
    return "\n".join(lines)
