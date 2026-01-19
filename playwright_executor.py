import subprocess
import tempfile
import os
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime


class PlaywrightExecutor:
    """Executes Playwright test scripts and captures results."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url
        self.results_dir = os.path.join(os.path.dirname(__file__), "test_results")
        os.makedirs(self.results_dir, exist_ok=True)
        self._check_playwright_browsers()
    
    def _check_playwright_browsers(self) -> bool:
        """Check if Playwright browsers are installed."""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                # Try to get browser path - this will fail if browsers aren't installed
                try:
                    browser_path = p.chromium.executable_path
                    if browser_path and os.path.exists(browser_path):
                        return True
                except Exception:
                    pass
            return False
        except Exception:
            return False
    
    def install_browsers(self) -> Dict[str, Any]:
        """Install Playwright browsers."""
        try:
            python_exe = sys.executable
            process = subprocess.Popen(
                [python_exe, "-m", "playwright", "install", "chromium"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "message": "Browsers installed successfully",
                    "output": stdout
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to install browsers",
                    "error": stderr,
                    "output": stdout
                }
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "message": "Browser installation timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error installing browsers: {str(e)}"
            }
    
    def execute_test(self, code: str, test_name: str = "test_automated") -> Dict[str, Any]:
        """
        Execute Playwright test code and return results.
        
        Args:
            code: Generated Playwright Python code
            test_name: Name of the test
            
        Returns:
            Dictionary with execution results, logs, and status
        """
        # Check if browsers are installed
        if not self._check_playwright_browsers():
            return {
                "status": "browser_not_installed",
                "success": False,
                "error": "Playwright browsers are not installed. Please run: python -m playwright install chromium",
                "error_details": "Browser executable not found. Run 'python -m playwright install chromium' to install browsers.",
                "output": "",
                "execution_time": 0,
                "assertions_passed": 0,
                "assertions_failed": 0,
                "requires_browser_install": True
            }
        
        # Create temporary test file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_file = os.path.join(self.results_dir, f"{test_name}_{timestamp}.py")
        
        try:
            # Write code to temporary file
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Execute the test
            result = self._run_test(test_file)
            
            # Check if error is about missing browsers
            if result.get("error") and "Executable doesn't exist" in result.get("error", ""):
                result["status"] = "browser_not_installed"
                result["requires_browser_install"] = True
                result["error"] = "Playwright browsers are not installed. Please run: python -m playwright install chromium"
            
            # Clean up test file
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            requires_install = "Executable doesn't exist" in error_msg or "playwright install" in error_msg.lower()
            
            return {
                "status": "browser_not_installed" if requires_install else "error",
                "success": False,
                "error": "Playwright browsers are not installed. Please run: python -m playwright install chromium" if requires_install else error_msg,
                "error_details": error_msg,
                "output": "",
                "execution_time": 0,
                "assertions_passed": 0,
                "assertions_failed": 0,
                "requires_browser_install": requires_install
            }
    
    def _run_test(self, test_file: str) -> Dict[str, Any]:
        """Run the test file and capture output."""
        import time
        import sys
        start_time = time.time()
        
        try:
            # Determine Python executable
            python_exe = sys.executable
            
            # Run the test using subprocess
            process = subprocess.Popen(
                [python_exe, test_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(test_file),
                encoding='utf-8',
                errors='replace'
            )
            
            stdout, stderr = process.communicate(timeout=60)  # 60 second timeout
            
            execution_time = time.time() - start_time
            
            # Parse output for assertions
            assertions_passed = stdout.count('[SUCCESS]') + stdout.count('assert') - stdout.count('AssertionError')
            assertions_failed = stderr.count('AssertionError') + stderr.count('assert')
            
            if process.returncode == 0:
                return {
                    "status": "passed",
                    "success": True,
                    "error": None,
                    "output": stdout,
                    "error_output": stderr,
                    "execution_time": round(execution_time, 2),
                    "assertions_passed": assertions_passed,
                    "assertions_failed": assertions_failed
                }
            else:
                return {
                    "status": "failed",
                    "success": False,
                    "error": stderr if stderr else "Test execution failed",
                    "output": stdout,
                    "error_output": stderr,
                    "execution_time": round(execution_time, 2),
                    "assertions_passed": max(0, assertions_passed),
                    "assertions_failed": max(1, assertions_failed)
                }
                
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return {
                "status": "timeout",
                "success": False,
                "error": "Test execution timed out after 60 seconds",
                "output": "",
                "error_output": "Execution timeout",
                "execution_time": 60,
                "assertions_passed": 0,
                "assertions_failed": 0
            }
        except FileNotFoundError:
            return {
                "status": "error",
                "success": False,
                "error": "Python executable not found. Make sure Python is installed and in PATH.",
                "output": "",
                "error_output": "Python not found",
                "execution_time": round(time.time() - start_time, 2),
                "assertions_passed": 0,
                "assertions_failed": 0
            }
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            return {
                "status": "error",
                "success": False,
                "error": str(e),
                "error_details": error_trace,
                "output": "",
                "error_output": str(e),
                "execution_time": round(time.time() - start_time, 2),
                "assertions_passed": 0,
                "assertions_failed": 0
            }
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        Validate generated code syntax without executing.
        
        Args:
            code: Generated Playwright Python code
            
        Returns:
            Dictionary with validation results
        """
        import ast
        
        try:
            # Check Python syntax
            ast.parse(code)
            
            # Check for required imports
            has_playwright = "playwright" in code.lower() or "sync_playwright" in code
            has_function = "def " in code
            
            return {
                "valid": True,
                "errors": [],
                "warnings": [],
                "has_playwright": has_playwright,
                "has_function": has_function
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Syntax error at line {e.lineno}: {e.msg}"],
                "warnings": [],
                "has_playwright": False,
                "has_function": False
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "warnings": [],
                "has_playwright": False,
                "has_function": False
            }


def generate_assertions(commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enhanced Assertion Generator for result validation.
    Generates comprehensive assertions based on commands.
    
    Args:
        commands: List of structured commands
        
    Returns:
        List of assertion objects
    """
    assertions = []
    
    for idx, cmd in enumerate(commands, 1):
        action_type = cmd.get("action_type", "")
        target = cmd.get("target", "")
        value = cmd.get("value", "")
        
        if action_type == "navigate":
            # Assert URL navigation
            assertions.append({
                "step": idx,
                "type": "url_check",
                "target": target,
                "expected": target,
                "description": f"Verify navigation to {target}"
            })
        
        elif action_type == "fill":
            # Assert field is filled
            assertions.append({
                "step": idx,
                "type": "field_filled",
                "target": target,
                "expected": value,
                "description": f"Verify field {target} contains {value}"
            })
        
        elif action_type == "click":
            # Assert element is clickable/clicked
            assertions.append({
                "step": idx,
                "type": "element_clickable",
                "target": target,
                "description": f"Verify element {target} is clickable"
            })
        
        elif action_type == "assert":
            # Explicit assertion command
            assertions.append({
                "step": idx,
                "type": "explicit_assert",
                "target": target,
                "expected": value,
                "description": cmd.get("description", "Verify assertion")
            })
    
    return assertions

