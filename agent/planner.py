import json
import re
from agent.schemas import Plan
from agent.llm_client import get_llm

PROMPT_TEMPLATE = """
You are a senior QA automation planner.

Convert the instruction into a STRICT JSON execution plan.

CRITICAL SELECTOR RULES:
- For LOGIN form elements, use: #username, #password, #loginBtn
- For REGISTRATION form elements, use: #name, #email, #country, #terms, #registerBtn
- For SEARCH form elements, use: #search-input, #search-btn
- For Google search, use: textarea[name='q'] and input[name='btnK']
- For buttons with text, use: button:has-text('Button Text') or text=Button Text
- For generic inputs, try: input[type='text'], input[type='email'], input[type='password'], textarea
- For buttons, try: button[type='submit'], input[type='submit'], or button:has-text('text')
- NEVER use :contains() - use :has-text() or text= instead
- ALWAYS use simple, reliable selectors that will work
- When user says "name" or "full name", use #name for registration form
- When user says "username", use #username for login form
- When user says "terms" or "agree to terms", use #terms checkbox

Supported Actions:
  * navigate - Navigate to URL (value: full URL with https://)
  * click - Click element (selector: CSS selector)
  * fill - Fill input field (selector: CSS selector, value: text)
  * wait - Wait milliseconds (value: milliseconds as number)
  * screenshot - Take screenshot (value: filename)
  * scroll - Scroll page (value: "up"/"down"/"top"/"bottom")
  * select_dropdown - Select dropdown option (selector: CSS selector, value: option text)
  * check_checkbox - Check/uncheck checkbox (selector: CSS selector, value: "true"/"false")
  * assert_visible - Assert element visible (selector: CSS selector)
  * assert_text - Assert element contains text (selector: CSS selector, value: expected text)
  * assert_url - Assert current URL (value: expected URL or pattern)

Output format (NO markdown, NO code blocks, ONLY JSON):
{"actions": [{"type": "action_name", "selector": "css_selector", "value": "value"}]}

Examples:

Input: "Navigate to http://127.0.0.1:5000/static/test_page.html, fill search input with 'AI testing', and click search button"
Output: {"actions": [{"type": "navigate", "value": "http://127.0.0.1:5000/static/test_page.html"}, {"type": "fill", "selector": "#search-input", "value": "AI testing"}, {"type": "click", "selector": "#search-btn"}]}

Input: "Go to test page, fill username with 'admin', password with 'secret', and click login"
Output: {"actions": [{"type": "navigate", "value": "http://127.0.0.1:5000/static/test_page.html"}, {"type": "fill", "selector": "#username", "value": "admin"}, {"type": "fill", "selector": "#password", "value": "secret"}, {"type": "click", "selector": "#loginBtn"}]}

Input: "Go to test page, fill name with 'John Doe', email with 'john@test.com', select country 'USA', check terms checkbox, and click register"
Output: {"actions": [{"type": "navigate", "value": "http://127.0.0.1:5000/static/test_page.html"}, {"type": "fill", "selector": "#name", "value": "John Doe"}, {"type": "fill", "selector": "#email", "value": "john@test.com"}, {"type": "select_dropdown", "selector": "#country", "value": "USA"}, {"type": "check_checkbox", "selector": "#terms", "value": "true"}, {"type": "click", "selector": "#registerBtn"}]}

Input: "search machine learning"
Output: {"actions": [{"type": "navigate", "value": "https://www.google.com"}, {"type": "fill", "selector": "textarea[name='q']", "value": "machine learning"}, {"type": "wait", "value": "1000"}, {"type": "click", "selector": "input[name='btnK']"}]}

Input: "go to deeplearning.ai and click start learning and enter email id as deepshika0408@gmail.com and password as hello"
Output: {"actions": [{"type": "navigate", "value": "https://www.deeplearning.ai"}, {"type": "wait", "value": "2000"}, {"type": "click", "selector": "button:has-text('Start Learning')"}, {"type": "wait", "value": "1000"}, {"type": "fill", "selector": "input[type='email']", "value": "deepshika0408@gmail.com"}, {"type": "fill", "selector": "input[type='password']", "value": "hello"}, {"type": "click", "selector": "button[type='submit']"}]}

Instruction:
{INSTRUCTION}
"""


def plan_actions(instruction: str) -> Plan:
    llm = get_llm()
    
    # Format the prompt with the instruction
    prompt = PROMPT_TEMPLATE.replace("{INSTRUCTION}", instruction)
    
    response = llm.invoke(prompt)

    try:
        # Clean response - remove markdown code blocks and extra text
        content = response.content.strip()
        
        # Remove markdown code blocks
        if content.startswith("```"):
            lines = content.split("\n")
            # Find the actual JSON content
            json_lines = []
            in_code_block = False
            for line in lines:
                if line.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or (not line.startswith("```") and "{" in line):
                    json_lines.append(line)
            content = "\n".join(json_lines)
        
        # Try to extract JSON if there's extra text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        # Parse JSON
        data = json.loads(content)
        
        # Validate required fields
        if "actions" not in data:
            raise ValueError("Missing 'actions' field in response")
        
        return Plan(**data)
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Parse Error: {e}")
        print(f"Raw response: {response.content[:500]}")
        raise RuntimeError(
            f"Planner produced invalid JSON. Error: {e}\nResponse: {response.content[:200]}"
        ) from e
    except Exception as e:
        print(f"\n❌ Planner Error: {e}")
        print(f"Raw response: {response.content[:500]}")
        raise RuntimeError(
            f"Planner error: {e}\nResponse: {response.content[:200]}"
        ) from e
