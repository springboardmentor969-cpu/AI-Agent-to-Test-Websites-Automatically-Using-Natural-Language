# agent/code_generator.py

class CodeGenerator:
    """
    Converts parsed actions into Playwright Python test script.
    """

    def generate_script(self, actions):
        script = [
            "from playwright.async_api import async_playwright",
            "import asyncio\n",
            "async def run_test():",
            "    async with async_playwright() as p:",
            "        browser = await p.chromium.launch(headless=True)",
            "        page = await browser.new_page()\n"
        ]

        for act in actions:
            if act["action"] == "goto":
                script.append(f'        await page.goto("{act["value"]}")')

            elif act["action"] == "click":
                script.append(f'        await page.click("{act["value"]}")')

            elif act["action"] == "type":
                script.append(f'        await page.fill("{act["field"]}", "{act["value"]}")')

            elif act["action"] == "assert_text":
                script.append("        content = await page.content()")
                script.append(f'        assert "{act["value"]}" in content, "Assertion Failed: Expected text not found"')

        script.append("        await browser.close()\n")
        script.append("asyncio.run(run_test())")

        return "\n".join(script)
