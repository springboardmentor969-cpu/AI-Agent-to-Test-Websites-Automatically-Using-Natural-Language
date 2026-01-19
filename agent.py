from typing import TypedDict, List, Dict, Optional, Any
from dataclasses import dataclass
import re
from playwright_executor import generate_assertions

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    StateGraph = None  # type: ignore
    END = None  # type: ignore


@dataclass
class Command:
    """Structured command representing a browser action."""
    action_type: str  # navigate, click, fill, submit, assert, wait
    target: Optional[str] = None  # URL, selector, text
    value: Optional[str] = None  # input value, expected text
    description: str = ""  # human-readable description


class AgentState(TypedDict):
    input: str
    actions: List[str]  # Legacy: human-readable actions
    commands: List[Dict[str, Any]]  # Structured commands
    assertions: List[Dict[str, Any]]  # Generated assertions
    response: str
    generated_code: str  # Playwright code output


def _parse_input(state: AgentState) -> AgentState:
    """
    Enhanced Instruction Parser Module for interpreting natural language test cases.
    Extracts detailed information: action types, targets, values, assertions.
    """
    instruction = state.get("input", "").lower()
    actions: List[str] = []
    commands: List[Dict[str, Any]] = []
    
    # Extract URLs
    url_pattern = r'(?:go to|navigate to|visit|open|test|check)\s+(?:the\s+)?(?:page\s+)?(?:at\s+)?(?:url\s+)?([/\w\-]+|http[^\s]+)'
    url_match = re.search(url_pattern, instruction)
    base_url = "http://127.0.0.1:5000"
    
    # Login flow detection
    if "login" in instruction or "sign in" in instruction:
        # Extract username if mentioned
        username_match = re.search(r'(?:with|as|using)\s+(\w+)', instruction)
        username = username_match.group(1) if username_match else "admin"
        
        # Extract password if mentioned
        password_match = re.search(r'password[:\s]+(\w+)', instruction)
        password = password_match.group(1) if password_match else None
        
        actions.append("Navigate to login page")
        commands.append({
            "action_type": "navigate",
            "target": f"{base_url}/login",
            "description": "Navigate to login page"
        })
        
        actions.append(f"Fill username field with '{username}'")
        commands.append({
            "action_type": "fill",
            "target": "input[name='username']",
            "value": username,
            "description": f"Fill username field with '{username}'"
        })
        
        if password:
            actions.append(f"Fill password field")
            commands.append({
                "action_type": "fill",
                "target": "input[name='password']",
                "value": password,
                "description": "Fill password field"
            })
        
        actions.append("Click submit button")
        commands.append({
            "action_type": "click",
            "target": "button[type='submit']",
            "description": "Click login submit button"
        })
        
        if "dashboard" in instruction or "check" in instruction:
            actions.append("Verify redirect to dashboard or home")
            commands.append({
                "action_type": "assert",
                "target": "url",
                "value": f"{base_url}/dashboard|{base_url}/",
                "description": "Verify successful login redirect"
            })
    
    # Signup/Register flow
    elif "signup" in instruction or "register" in instruction or "sign up" in instruction:
        actions.append("Navigate to signup page")
        commands.append({
            "action_type": "navigate",
            "target": f"{base_url}/signup",
            "description": "Navigate to signup page"
        })
        
        actions.append("Fill registration form")
        commands.append({
            "action_type": "fill",
            "target": "input[name='username']",
            "value": "testuser",
            "description": "Fill username field"
        })
        commands.append({
            "action_type": "fill",
            "target": "input[name='email']",
            "value": "test@example.com",
            "description": "Fill email field"
        })
        commands.append({
            "action_type": "fill",
            "target": "input[name='password']",
            "value": "testpass123",
            "description": "Fill password field"
        })
        
        actions.append("Submit registration form")
        commands.append({
            "action_type": "click",
            "target": "button[type='submit']",
            "description": "Submit signup form"
        })
    
    # Search functionality
    elif "search" in instruction:
        search_term_match = re.search(r'search\s+(?:for\s+)?["\']?([^"\']+)["\']?', instruction)
        search_term = search_term_match.group(1) if search_term_match else "test"
        
        if url_match:
            target_url = url_match.group(1)
            if not target_url.startswith("http"):
                target_url = f"{base_url}{target_url}"
        else:
            target_url = f"{base_url}/testpage"
        
        actions.append(f"Navigate to test page")
        commands.append({
            "action_type": "navigate",
            "target": target_url,
            "description": "Navigate to test page"
        })
        
        actions.append(f"Enter search term '{search_term}'")
        commands.append({
            "action_type": "fill",
            "target": "#test-search",
            "value": search_term,
            "description": f"Enter search term '{search_term}'"
        })
        
        actions.append("Click search button")
        commands.append({
            "action_type": "click",
            "target": "#test-search-button",
            "description": "Click search button"
        })
        
        if "verify" in instruction or "check" in instruction:
            actions.append(f"Verify search results contain '{search_term}'")
            commands.append({
                "action_type": "assert",
                "target": "#test-search-result",
                "value": search_term,
                "description": f"Verify search results contain '{search_term}'"
            })
    
    # Generic navigation
    elif url_match or "navigate" in instruction or "go to" in instruction:
        target_url = url_match.group(1) if url_match else "/"
        if not target_url.startswith("http"):
            target_url = f"{base_url}{target_url}"
        
        actions.append(f"Navigate to {target_url}")
        commands.append({
            "action_type": "navigate",
            "target": target_url,
            "description": f"Navigate to {target_url}"
        })
    
    # Toggle/switch detection
    elif "toggle" in instruction or "switch" in instruction:
        if url_match:
            target_url = url_match.group(1)
            if not target_url.startswith("http"):
                target_url = f"{base_url}{target_url}"
        else:
            target_url = f"{base_url}/testpage"
        
        actions.append("Navigate to test page")
        commands.append({
            "action_type": "navigate",
            "target": target_url,
            "description": "Navigate to test page"
        })
        
        actions.append("Toggle the switch")
        commands.append({
            "action_type": "click",
            "target": "#test-toggle",
            "description": "Toggle the switch"
        })
        
        if "verify" in instruction or "check" in instruction:
            actions.append("Verify toggle status changed")
            commands.append({
                "action_type": "assert",
                "target": "#test-toggle-status",
                "value": "ON|OFF",
                "description": "Verify toggle status changed"
            })
    
    # Fallback for unrecognized instructions
    if not actions:
        actions.append("Interpret instruction and plan browser steps")
        commands.append({
            "action_type": "navigate",
            "target": f"{base_url}/",
            "description": "Navigate to home page"
        })
    
    return {
        **state,
        "actions": actions,
        "commands": commands
    }


def _map_commands(state: AgentState) -> AgentState:
    """
    Map parsed actions into structured commands.
    Validates and enriches command structure.
    """
    commands = state.get("commands", [])
    
    # Validate commands
    validated_commands = []
    for cmd in commands:
        if isinstance(cmd, dict) and "action_type" in cmd:
            # Ensure required fields
            validated_cmd = {
                "action_type": cmd.get("action_type", "unknown"),
                "target": cmd.get("target"),
                "value": cmd.get("value"),
                "description": cmd.get("description", "")
            }
            validated_commands.append(validated_cmd)
    
    # Generate assertions for validation
    assertions = generate_assertions(validated_commands)
    
    return {
        **state,
        "commands": validated_commands,
        "assertions": assertions
    }


def _generate_code(state: AgentState) -> AgentState:
    """
    Code Generation Module: Converts structured commands into perfectly formatted,
    clean, and professional Playwright Python code.
    """
    commands = state.get("commands", [])
    
    if not commands:
        return {
            **state,
            "generated_code": "# No commands to generate code for.",
            "response": "No structured commands available for code generation.",
            "assertions": []
        }
    
    # Extract test name from input for function naming
    test_name = state.get("input", "automated_test")[:50].replace(" ", "_").lower()
    test_name = "".join(c for c in test_name if c.isalnum() or c == "_")
    if not test_name or not test_name[0].isalpha():
        test_name = "test_automated"
    
    code_lines = []
    
    # ==================== IMPORTS SECTION ====================
    code_lines.append("from playwright.sync_api import sync_playwright")
    code_lines.append("")
    code_lines.append("")
    
    # ==================== CONFIGURATION SECTION ====================
    code_lines.append("# ==================== Configuration ====================")
    code_lines.append("BASE_URL = 'http://127.0.0.1:5000'")
    code_lines.append("HEADLESS_MODE = True  # Set to False to see browser actions")
    code_lines.append("TIMEOUT_MS = 30000  # 30 seconds timeout")
    code_lines.append("")
    code_lines.append("")
    
    # ==================== MAIN TEST FUNCTION ====================
    code_lines.append(f"def {test_name}():")
    code_lines.append('    """')
    code_lines.append(f'    Automated test case: {state.get("input", "Unknown test")}')
    code_lines.append('    Generated by AI Testing Agent')
    code_lines.append('    """')
    code_lines.append("    ")
    code_lines.append("    with sync_playwright() as playwright:")
    code_lines.append("        # Initialize browser")
    code_lines.append("        browser = playwright.chromium.launch(headless=HEADLESS_MODE)")
    code_lines.append("        page = browser.new_page()")
    code_lines.append("        page.set_default_timeout(TIMEOUT_MS)")
    code_lines.append("        ")
    code_lines.append("        try:")
    code_lines.append("            ")
    
    # Generate test steps with perfect formatting
    for idx, cmd in enumerate(commands, 1):
        action_type = cmd.get("action_type", "")
        target = cmd.get("target", "")
        value = cmd.get("value", "")
        desc = cmd.get("description", "")
        
        # Add blank line before each step for clarity
        code_lines.append("            ")
        code_lines.append(f"            # Step {idx}: {desc}")
        
        if action_type == "navigate":
            # Handle URL - use BASE_URL variable if it's a local URL
            url = target
            if url.startswith("http://127.0.0.1:5000"):
                # Extract path and use BASE_URL
                path = url.replace("http://127.0.0.1:5000", "")
                if path:
                    code_lines.append(f"            page.goto(BASE_URL + '{path}')")
                else:
                    code_lines.append("            page.goto(BASE_URL)")
            elif url.startswith("http"):
                code_lines.append(f'            page.goto("{url}")')
            else:
                # Ensure path starts with /
                path = url if url.startswith("/") else f"/{url}"
                code_lines.append(f"            page.goto(BASE_URL + '{path}')")
            code_lines.append("            page.wait_for_load_state('networkidle')")
        
        elif action_type == "fill":
            if target and value:
                # Escape quotes in value
                safe_value = str(value).replace('"', '\\"').replace("'", "\\'")
                code_lines.append(f'            page.fill("{target}", "{safe_value}")')
        
        elif action_type == "click":
            if target:
                code_lines.append(f'            page.click("{target}")')
                code_lines.append("            page.wait_for_timeout(500)  # Wait for action to complete")
        
        elif action_type == "submit":
            if target:
                code_lines.append(f'            page.locator("{target}").press("Enter")')
            else:
                code_lines.append('            page.keyboard.press("Enter")')
            code_lines.append("            page.wait_for_timeout(1000)  # Wait for form submission")
        
        elif action_type == "assert":
            if target == "url":
                # URL assertion with proper formatting
                code_lines.append("            current_url = page.url")
                if "|" in str(value):
                    urls = [u.strip() for u in str(value).split("|")]
                    # Generate proper any() with generator expression
                    url_list_str = "[" + ", ".join([f'"{url}"' for url in urls]) + "]"
                    code_lines.append(f'            assert any(url in current_url for url in {url_list_str}), \\')
                    code_lines.append(f'                f"Expected URL to contain one of {urls}, got {{current_url}}"')
                else:
                    safe_value = str(value).replace('"', '\\"')
                    code_lines.append(f'            assert "{safe_value}" in current_url, \\')
                    code_lines.append(f'                f"Expected URL to contain \'{safe_value}\', got {{current_url}}"')
            else:
                # Text/content assertion with proper formatting
                if value:
                    code_lines.append(f'            element = page.locator("{target}")')
                    code_lines.append("            element.wait_for(state='visible')")
                    code_lines.append("            content = element.text_content()")
                    if "|" in str(value):
                        values = [v.strip() for v in str(value).split("|")]
                        # Generate proper any() with generator expression
                        value_list_str = "[" + ", ".join([f'"{v}"' for v in values]) + "]"
                        code_lines.append(f'            assert any(v in content for v in {value_list_str}), \\')
                        code_lines.append(f'                f"Expected content to contain one of {values}, got {{content}}"')
                    else:
                        safe_value = str(value).replace('"', '\\"')
                        code_lines.append(f'            assert "{safe_value}" in content, \\')
                        code_lines.append(f'                f"Expected content to contain \'{safe_value}\', got {{content}}"')
        
        elif action_type == "wait":
            wait_time = value if value else "1000"
            code_lines.append(f"            page.wait_for_timeout({wait_time})")
    
    # Close try block and add error handling
    code_lines.append("            ")
    code_lines.append("            print('[SUCCESS] Test completed successfully!')")
    code_lines.append("            ")
    code_lines.append("        except Exception as e:")
    code_lines.append("            print(f'[FAILED] Test failed with error: {e}')")
    code_lines.append("            raise")
    code_lines.append("            ")
    code_lines.append("        finally:")
    code_lines.append("            browser.close()")
    code_lines.append("")
    code_lines.append("")
    
    # ==================== MAIN ENTRY POINT ====================
    code_lines.append("if __name__ == '__main__':")
    code_lines.append(f"    {test_name}()")
    
    generated_code = "\n".join(code_lines)
    
    response_lines = [
        "✅ Test case parsed and converted to Playwright code.",
        "",
        f"📋 Found {len(commands)} structured command(s):",
    ]
    for idx, cmd in enumerate(commands, 1):
        response_lines.append(f"  {idx}. {cmd.get('description', 'Unknown action')}")
    
    response_lines.append("")
    response_lines.append("💻 Generated Playwright code is ready for execution.")
    
    assertions = state.get("assertions", [])
    
    return {
        **state,
        "generated_code": generated_code,
        "response": "\n".join(response_lines),
        "assertions": assertions
    }


def _build_agent():
    """
    Build LangGraph workflow: parser → command mapper → code generator.
    """
    if StateGraph is None or END is None:
        return None

    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("parse_input", _parse_input)
    graph.add_node("map_commands", _map_commands)
    graph.add_node("generate_code", _generate_code)
    
    # Set workflow: parse → map → generate → END
    graph.set_entry_point("parse_input")
    graph.add_edge("parse_input", "map_commands")
    graph.add_edge("map_commands", "generate_code")
    graph.add_edge("generate_code", END)
    
    return graph.compile()


_agent = _build_agent()


def run_agent(user_input: str) -> AgentState:
    """
    Execute the LangGraph agent with enhanced parser and code generation.
    
    Returns structured state with:
    - input: original user input
    - actions: human-readable action list
    - commands: structured command objects
    - response: summary message
    - generated_code: Playwright Python code
    """
    if not user_input:
        return {
            "input": "",
            "actions": [],
            "commands": [],
            "assertions": [],
            "response": "No instruction provided.",
            "generated_code": ""
        }

    if _agent is None:
        return {
            "input": user_input,
            "actions": [],
            "commands": [],
            "assertions": [],
            "response": (
                "LangGraph is not installed. Install it with "
                "`pip install langgraph` to enable agent planning."
            ),
            "generated_code": ""
        }

    state: AgentState = {
        "input": user_input,
        "actions": [],
        "commands": [],
        "assertions": [],
        "response": "",
        "generated_code": ""
    }
    return _agent.invoke(state)
