import asyncio
import sys
import traceback
from datetime import datetime
from typing import Dict, Optional
import os
from playwright.async_api import async_playwright, Browser, Page
import re


class TestExecutor:
    """
    Executes generated Playwright test code and captures results.
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.execution_log = []
    
    async def execute_code(self, test_code: str, test_name: str = "test") -> Dict:
        """Execute Playwright test code and return results"""
        
        start_time = datetime.now()
        result = {
            'test_name': test_name,
            'status': 'unknown',
            'start_time': start_time.isoformat(),
            'end_time': None,
            'duration': None,
            'error': None,
            'traceback': None,
            'screenshots': [],
            'logs': [],
            'passed_steps': 0,
            'failed_steps': 0,
            'total_steps': 0,
            'step_results': []
        }
        
        try:
            result['status'] = 'running'
            
            # Remove the asyncio.run() call from generated code if present
            test_code = test_code.replace("asyncio.run(", "await ")
            test_code = test_code.replace("if __name__ == '__main__':", "# Main removed")
            
            # Create execution namespace
            exec_globals = {
                '__name__': '__main__',
                'asyncio': asyncio,
                'async_playwright': async_playwright,
            }
            
            # Execute the code to define functions
            exec(test_code, exec_globals)
            
            # Find the test function
            test_func = None
            for name, obj in exec_globals.items():
                if callable(obj) and (name.startswith('test_') or name.startswith('main')):
                    test_func = obj
                    break
            
            if test_func is None:
                raise ValueError("No test function found in generated code")
            
            # Check if it's async and call appropriately
            if asyncio.iscoroutinefunction(test_func):
                # Check function signature
                import inspect
                sig = inspect.signature(test_func)
                
                if 'page' in sig.parameters:
                    # Function expects page argument
                    async with async_playwright() as p:
                        browser = await p.chromium.launch(headless=self.headless)
                        context = await browser.new_context()
                        page = await context.new_page()
                        
                        try:
                            await test_func(page)
                        finally:
                            await browser.close()
                else:
                    # Function is self-contained
                    await test_func()
            else:
                # Synchronous function
                test_func()
            
            result['status'] = 'passed'
            result['passed_steps'] = 1
            result['total_steps'] = 1
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            result['failed_steps'] = 1
            result['logs'].append(f"Error: {str(e)}")
        
        finally:
            end_time = datetime.now()
            result['end_time'] = end_time.isoformat()
            result['duration'] = (end_time - start_time).total_seconds()
        
        return result
    
    async def execute_structured_test(self, parsed_test: Dict, url: str = None) -> Dict:
        """Execute test steps directly without code generation"""
        
        start_time = datetime.now()
        test_name = parsed_test.get('test_name', 'Unnamed Test')
        steps = parsed_test.get('steps', [])
        
        # IMPORTANT: Initialize ALL required fields including 'logs'
        result = {
            'test_name': test_name,
            'status': 'running',
            'start_time': start_time.isoformat(),
            'end_time': None,
            'duration': None,
            'error': None,
            'traceback': None,
            'screenshots': [],
            'logs': [], 
            'passed_steps': 0,
            'failed_steps': 0,
            'total_steps': len(steps),
            'step_results': []
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            page.set_default_timeout(self.timeout)
            
            try:
                # Navigate to URL if provided
                if url or parsed_test.get('url'):
                    target_url = url or parsed_test['url']
                    await page.goto(target_url)
                    await page.wait_for_load_state('networkidle')
                    result['logs'].append(f"Navigated to {target_url}")
                
                # Execute each step
                for step in steps:
                    result['logs'].append(f"Executing step {step['step_number']}: {step['description']}")
                    step_result = await self._execute_step(page, step, result)
                    result['step_results'].append(step_result)
                    
                    if step_result['status'] == 'passed':
                        result['passed_steps'] += 1
                        result['logs'].append(f"Step {step['step_number']}: PASSED")
                    else:
                        result['failed_steps'] += 1
                        result['logs'].append(f"Step {step['step_number']}: FAILED - {step_result.get('error', 'Unknown error')}")
                        
                        # Take screenshot on first failure
                        if result['failed_steps'] == 1:
                            screenshot_path = f"static/screenshots/failure_{test_name}_{datetime.now().timestamp()}.png"
                            await page.screenshot(path=screenshot_path)
                            result['screenshots'].append(screenshot_path)
                            result['logs'].append(f"Screenshot saved: {screenshot_path}")
                
                # Determine overall status
                if result['failed_steps'] == 0:
                    result['status'] = 'passed'
                    result['logs'].append("Test completed successfully")
                else:
                    result['status'] = 'failed'
                    result['logs'].append(f"Test failed with {result['failed_steps']} failed steps")
                
            except Exception as e:
                result['status'] = 'failed'
                result['error'] = str(e)
                result['traceback'] = traceback.format_exc()
                result['logs'].append(f"Fatal error: {str(e)}")
                
                # Take error screenshot
                try:
                    screenshot_path = f"static/screenshots/error_{test_name}_{datetime.now().timestamp()}.png"
                    await page.screenshot(path=screenshot_path)
                    result['screenshots'].append(screenshot_path)
                    result['logs'].append(f"Error screenshot saved: {screenshot_path}")
                except:
                    pass
            
            finally:
                await browser.close()
                end_time = datetime.now()
                result['end_time'] = end_time.isoformat()
                result['duration'] = (end_time - start_time).total_seconds()
                result['logs'].append(f"Test completed in {result['duration']:.2f} seconds")
        
        return result
    
    async def _execute_step(self, page: Page, step: Dict, result: Dict) -> Dict:
        """Execute a single test step"""
        step_result = {
            'step_number': step['step_number'],
            'description': step['description'],
            'action': step['action'],
            'status': 'unknown',
            'error': None,
            'duration': None
        }
        
        start = datetime.now()
        
        try:
            action = step['action']
            target = step.get('target', '')
            value = step.get('value')
            expected = step.get('expected')
            
            result['logs'].append(f"Step {step['step_number']}: {step['description']}")
            
            if action == 'navigate':
                url = value or step.get('url')
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
            
            elif action == 'click':
                element = await self._find_element(page, target)
                await element.click()
                await page.wait_for_timeout(500)
            
            elif action == 'type':
                element = await self._find_element(page, target)
                await element.fill(value or '')
            
            elif action == 'select':
                element = await self._find_element(page, target)
                await element.select_option(value)
            
            elif action == 'verify':
                element = await self._find_element(page, target)
                is_visible = await element.is_visible()
                
                if not is_visible:
                    raise AssertionError(f"Element '{target}' is not visible")
                
                if expected:
                    text_content = await element.text_content()
                    if expected.lower() not in (text_content or '').lower():
                        raise AssertionError(
                            f"Expected text '{expected}' not found in '{text_content}'"
                        )
            
            elif action == 'wait':
                timeout = int(value) if value else 1000
                await page.wait_for_timeout(timeout)
            
            elif action == 'scroll':
                if target:
                    element = await self._find_element(page, target)
                    await element.scroll_into_view_if_needed()
                else:
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            
            elif action == 'hover':
                element = await self._find_element(page, target)
                await element.hover()
            
            step_result['status'] = 'passed'
            
        except Exception as e:
            step_result['status'] = 'failed'
            step_result['error'] = str(e)
            result['logs'].append(f"  Error: {str(e)}")
        
        finally:
            duration = (datetime.now() - start).total_seconds()
            step_result['duration'] = duration
        
        return step_result
    
    async def _find_element(self, page: Page, description: str):
        """Find element using smart selector strategies based on description"""
        desc_lower = description.lower()
        
        # Try different selector strategies
        strategies = []
        
        # Extract text in quotes
        quoted_text = re.findall(r"['\"]([^'\"]+)['\"]", description)
        
        if 'button' in desc_lower:
            if quoted_text:
                strategies.append(page.get_by_role('button', name=quoted_text[0]))
            strategies.append(page.get_by_role('button'))
        
        if 'link' in desc_lower:
            if quoted_text:
                strategies.append(page.get_by_role('link', name=quoted_text[0]))
            strategies.append(page.get_by_role('link'))
        
        if 'input' in desc_lower or 'field' in desc_lower:
            if 'email' in desc_lower:
                strategies.append(page.get_by_label('Email'))
                strategies.append(page.get_by_placeholder('Email'))
                strategies.append(page.locator('input[type="email"]'))
                strategies.append(page.locator('#email'))
            if 'password' in desc_lower:
                strategies.append(page.get_by_label('Password'))
                strategies.append(page.get_by_placeholder('Password'))
                strategies.append(page.locator('input[type="password"]'))
                strategies.append(page.locator('#password'))
            if quoted_text:
                strategies.append(page.get_by_label(quoted_text[0]))
                strategies.append(page.get_by_placeholder(quoted_text[0]))
        
        # Try text content
        if quoted_text:
            strategies.append(page.get_by_text(quoted_text[0]))
        
        # Try with partial description
        strategies.append(page.locator(f"text={description}"))
        
        # Try each strategy
        for strategy in strategies:
            try:
                await strategy.wait_for(timeout=5000)
                return strategy
            except:
                continue
        
        # Fallback: raise error
        raise Exception(f"Could not find element: {description}")
