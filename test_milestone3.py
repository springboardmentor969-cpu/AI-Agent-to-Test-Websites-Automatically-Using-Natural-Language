from agent import run_agent
from playwright_executor import PlaywrightExecutor, generate_assertions


def test_code_generation():
    """Test that code generation works correctly."""
    print("\n" + "="*60)
    print("Test 1: Code Generation")
    print("="*60)
    
    instruction = "Login with admin and check dashboard"
    state = run_agent(instruction)
    
    assert state.get("generated_code"), "Generated code should not be empty"
    assert "playwright" in state.get("generated_code", "").lower(), "Code should contain playwright"
    assert "def " in state.get("generated_code", ""), "Code should contain function definition"
    
    print("[OK] Code generation test passed")
    print(f"   Generated {len(state.get('generated_code', ''))} characters of code")
    return True


def test_assertion_generator():
    """Test assertion generator."""
    print("\n" + "="*60)
    print("Test 2: Assertion Generator")
    print("="*60)
    
    commands = [
        {"action_type": "navigate", "target": "/login", "description": "Navigate to login"},
        {"action_type": "fill", "target": "input[name='username']", "value": "admin", "description": "Fill username"},
        {"action_type": "click", "target": "button[type='submit']", "description": "Click submit"},
        {"action_type": "assert", "target": "url", "value": "/dashboard", "description": "Check dashboard"}
    ]
    
    assertions = generate_assertions(commands)
    
    assert len(assertions) > 0, "Should generate assertions"
    assert any(a["type"] == "url_check" for a in assertions), "Should have URL check assertion"
    assert any(a["type"] == "field_filled" for a in assertions), "Should have field filled assertion"
    
    print("[OK] Assertion generator test passed")
    print(f"   Generated {len(assertions)} assertions")
    for idx, assertion in enumerate(assertions, 1):
        print(f"   {idx}. {assertion['type']} - {assertion['description']}")
    return True


def test_code_validation():
    """Test code validation."""
    print("\n" + "="*60)
    print("Test 3: Code Validation")
    print("="*60)
    
    executor = PlaywrightExecutor()
    
    # Valid code
    valid_code = """
from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")
        browser.close()
"""
    
    result = executor.validate_code(valid_code)
    assert result["valid"], "Valid code should pass validation"
    assert result["has_playwright"], "Should detect Playwright import"
    assert result["has_function"], "Should detect function definition"
    
    # Invalid code
    invalid_code = "def test(  # syntax error"
    result = executor.validate_code(invalid_code)
    assert not result["valid"], "Invalid code should fail validation"
    
    print("[OK] Code validation test passed")
    return True


def test_local_form_interaction():
    """Test interaction with local HTML forms."""
    print("\n" + "="*60)
    print("Test 4: Local Form Interaction Test")
    print("="*60)
    
    instruction = "Navigate to testpage and search for 'test'"
    state = run_agent(instruction)
    
    code = state.get("generated_code", "")
    assert code, "Should generate code for testpage interaction"
    assert "testpage" in code.lower() or "/testpage" in code, "Code should target testpage"
    
    print("[OK] Local form interaction test passed")
    print("   Generated code for testpage interaction")
    return True


def test_execution_workflow():
    """Test the complete execution workflow."""
    print("\n" + "="*60)
    print("Test 5: Execution Workflow")
    print("="*60)
    
    instruction = "Go to home page"
    state = run_agent(instruction)
    
    code = state.get("generated_code", "")
    commands = state.get("commands", [])
    assertions = state.get("assertions", [])
    
    assert code, "Should generate code"
    assert len(commands) > 0, "Should have commands"
    assert len(assertions) > 0, "Should have assertions"
    
    executor = PlaywrightExecutor()
    validation = executor.validate_code(code)
    assert validation["valid"], "Generated code should be valid"
    
    print("[OK] Execution workflow test passed")
    print(f"   Commands: {len(commands)}")
    print(f"   Assertions: {len(assertions)}")
    print(f"   Code valid: {validation['valid']}")
    return True


def main():
    """Run all Milestone 3 tests."""
    print("\n" + "="*60)
    print("Milestone 3: Playwright Execution Tests")
    print("="*60)
    
    tests = [
        test_code_generation,
        test_assertion_generator,
        test_code_validation,
        test_local_form_interaction,
        test_execution_workflow
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_func.__name__}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("[SUCCESS] All Milestone 3 tests passed!")
        return 0
    else:
        print("[FAILED] Some tests failed.")
        return 1


if __name__ == "__main__":
    exit(main())

