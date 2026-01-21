from groq import Groq
from typing import Dict
import re

class PlaywrightCodeGenerator:
    """Generates Playwright code using Groq AI"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def generate(self, parsed_test: Dict) -> str:
        """Generate Playwright code from parsed test"""
        
        # Use template-based generation for reliability
        test_name = parsed_test.get('test_name', 'test').replace(' ', '_').lower()
        test_name = re.sub(r'[^a-z0-9_]', '', test_name)  # Remove invali
        url = parsed_test.get('url', 'about:blank')
        steps = parsed_test.get('steps', [])
        
        # Build code manually for reliability
        code = f"""import asyncio
from playwright.async_api import async_playwright

async def test_{test_name}():
    \"\"\"
    Test: {parsed_test.get('test_name', 'Test')}
    Generated automatically by AI Web Testing Agent
    \"\"\"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
"""
        
        # Add URL navigation if provided
        if url and url != 'about:blank':
            code += f"            # Navigate to URL\n"
            code += f"            await page.goto('{url}')\n"
            code += f"            await page.wait_for_load_state('networkidle')\n\n"
        
        # Add steps
        for step in steps:
            action = step.get('action', '').lower()
            target = step.get('target', '')
            value = step.get('value', '')
            step_num = step.get('step_number', '?')
            description = step.get('description', '')
            
            code += f"            # Step {step.get('step_number')}: {step.get('description')}\n"
            
            if action == 'navigate':
                nav_url = value or target
                code += f"            await page.goto('{nav_url}')\n"
                code += f"            await page.wait_for_load_state('networkidle')\n"
            
            elif action == 'click':
                code += f"            await page.locator(\"text='{target}'\").click()\n"
                code += f"            await page.wait_for_timeout(500)\n"
            
            elif action == 'type':
                 if 'email' in target.lower():
                    code += f"            await page.locator('input[type=\"email\"]').fill('{value}')"
                 elif 'password' in target.lower():
                    code += f"            await page.locator('input[type=\"password\"]').fill('{value}')"
                 else:
                    code += f"            await page.locator('input[type=\"email\"]').fill('{value}')"
            
                 code += f"            await page.locator(\"input\").fill('{value}')\n"
            
            elif action == 'wait':
                timeout = int(value) * 1000 if value else 1000
                code += f"            await page.wait_for_timeout({timeout})\n"
            
            elif action == 'verify':
                code += f"            # Verify page is loaded\n"
                code += f"            await page.wait_for_load_state('domcontentloaded')\n"

            elif action == 'select':
                code += f"            await page.locator('select').select_option('{value}')\n"
            
            elif action == 'scroll':
                code += f"            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')\n"
            
            elif action == 'hover':
                code += f"            await page.locator('button').first.hover()\n"

            code += "\n"
        
        # Close code
        code += """            print("Test completed successfully!")
            
        except Exception as e:
            print(f"Test failed: {{e}}")
            await page.screenshot(path='error_screenshot.png')
            raise
        
        finally:
            await browser.close()

     if __name__ == '__main__':
     asyncio.run(test_{test_name}())
     """
        
        print(f"=== Generated Code ===\n{code}\n==================")
        return code