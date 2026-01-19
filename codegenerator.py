def generate_playwright_code(commands: list, target_url: str):
    lines = []

    # Always navigate first
    lines.append(f"page.goto('{target_url}')")
    lines.append("page.wait_for_load_state('networkidle')")

    for cmd in commands:
        action = cmd.get("action")
        target = cmd.get("target")
        value = cmd.get("value")

        if action == "type":
            lines.append(f"page.wait_for_selector('#{target}')")

            
            if target == "role_select":
                lines.append(
                    f"page.select_option('#{target}', '{value}')"
                )
            else:
                lines.append(
                    f"page.fill('#{target}', '{value}')"
                )

        elif action == "click":
            lines.append(f"page.wait_for_selector('#{target}')")
            lines.append(f"page.click('#{target}')")

    action_block = "\n".join(lines)

    full_script = f"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=700)
    page = browser.new_page()
    {action_block}
    page.screenshot(path="screenshots/test.png")
    browser.close()
""".strip()

    return action_block, full_script
