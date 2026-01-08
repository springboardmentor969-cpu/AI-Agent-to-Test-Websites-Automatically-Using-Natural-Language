import os
import json


def _py(val: str) -> str:
    return json.dumps(val)


def generate_playwright_test(steps, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    lines = [
        "from playwright.sync_api import sync_playwright, expect",
        "",
        "def test_generated():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        context = browser.new_context()",
        "        page = context.new_page()",
        "",
    ]

    for step in steps:
        a = step.get("action")

        if a == "goto":
            lines.append(
                f"        page.goto({_py(step['url'])}, wait_until='domcontentloaded', timeout=10000)"
            )
        elif a == "fill":
            lines.append(
                f"        page.fill({_py(step['selector'])}, {_py(step['value'])})"
            )
        elif a == "click":
            lines.append(
                f"        page.click({_py(step['selector'])})"
            )
        elif a == "assert_text":
            lines.append(
                f"        expect(page.locator({_py(step['selector'])})).to_contain_text({_py(step['value'])}, timeout=5000)"
            )

    lines += [
        "",
        "        context.close()",
        "        browser.close()",
    ]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
