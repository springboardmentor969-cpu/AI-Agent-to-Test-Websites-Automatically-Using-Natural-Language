"""
Validation script for Milestone 2: Test case conversion output validation.
Tests the instruction parser, command mapping, and code generation.
"""

from agent import run_agent


def validate_test_case(instruction: str, expected_actions: int = 1):
    """Validate a test case conversion."""
    print(f"\n{'='*60}")
    print(f"Testing: '{instruction}'")
    print('='*60)
    
    state = run_agent(instruction)
    
    # Check response
    assert state.get("response"), "Response should not be empty"
    print(f"[OK] Response generated: {len(state.get('response', ''))} chars")
    
    # Check actions
    actions = state.get("actions", [])
    assert len(actions) >= expected_actions, f"Expected at least {expected_actions} actions, got {len(actions)}"
    print(f"[OK] Actions parsed: {len(actions)}")
    for idx, action in enumerate(actions, 1):
        print(f"   {idx}. {action}")
    
    # Check structured commands
    commands = state.get("commands", [])
    assert len(commands) > 0, "Should have at least one structured command"
    print(f"[OK] Structured commands: {len(commands)}")
    for idx, cmd in enumerate(commands, 1):
        print(f"   {idx}. {cmd.get('action_type')} - {cmd.get('description')}")
    
    # Check generated code
    code = state.get("generated_code", "")
    assert code, "Generated code should not be empty"
    assert "playwright" in code.lower() or "sync_playwright" in code, "Code should contain Playwright imports"
    assert "def test" in code or "def " in code, "Code should contain function definition"
    print(f"[OK] Code generated: {len(code)} chars")
    print(f"   First 100 chars: {code[:100]}...")
    
    return True


def main():
    """Run validation tests."""
    print("Milestone 2 Validation: Test Case Conversion Output")
    print("="*60)
    
    test_cases = [
        ("Login with admin and check dashboard", 3),
        ("Navigate to signup page and register", 2),
        ("Search for 'test' on testpage", 2),
        ("Toggle the switch and verify", 2),
        ("Go to /login page", 1),
    ]
    
    passed = 0
    failed = 0
    
    for instruction, min_actions in test_cases:
        try:
            validate_test_case(instruction, min_actions)
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] Validation failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Validation Results: {passed} passed, {failed} failed")
    print('='*60)
    
    if failed == 0:
        print("[SUCCESS] All validations passed! Milestone 2 requirements met.")
        return 0
    else:
        print("[FAILED] Some validations failed. Please review.")
        return 1


if __name__ == "__main__":
    exit(main())

