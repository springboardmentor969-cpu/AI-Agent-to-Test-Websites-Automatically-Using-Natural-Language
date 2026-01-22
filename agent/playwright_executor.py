import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from agent.schemas import Action, ExecutionStepResult

class PlaywrightExecutor:
    def __init__(self, screenshot_dir="screenshots"):
        self.screenshot_dir = screenshot_dir  # Store as instance variable
        self.playwright = sync_playwright().start()
        # Run in HEADED mode so user can see the browser
        # Optimized for Windows with GPU acceleration
        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=50,  # Reduced for smoother interactions
            args=[
                '--start-maximized',
                '--window-size=1920,1080',  # Fallback size
                '--window-position=0,0',
                '--disable-blink-features=AutomationControlled',
                '--enable-gpu',
                '--disable-software-rasterizer',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--force-device-scale-factor=1',
                '--disable-smooth-scrolling',
                # Stealth mode for external sites
                '--disable-blink-features=AutomationControlled',
                '--exclude-switches=enable-automation',
                '--disable-extensions',
            ]
        )
        # Create context and page with no viewport to allow full maximization
        context = self.browser.new_context(no_viewport=True)
        self.page = context.new_page()
        
        # Maximize the window using CDP
        try:
            cdp = self.page.context.new_cdp_session(self.page)
            cdp.send('Browser.setWindowBounds', {
                'windowId': 1,
                'bounds': {'windowState': 'maximized'}
            })
        except:
            pass  # Fallback to args if CDP fails
        
        # Enable smooth scrolling via CSS
        self.page.add_init_script("""
            document.documentElement.style.scrollBehavior = 'auto';
        """)
        self.screenshot_dir = screenshot_dir
        
        # Create screenshot directory if it doesn't exist
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    def _adaptive_selector(self, selector: str) -> str:
        """Try multiple selector strategies if primary fails"""
        if not selector:
            return selector
        
        # First, check if the original selector works
        try:
            if self.page.locator(selector).count() > 0:
                return selector
        except Exception:
            pass
        
        # Extract text from :has-text() or text= selectors
        text_match = None
        if ':has-text(' in selector:
            import re
            match = re.search(r":has-text\('([^']+)'\)", selector)
            if match:
                text_match = match.group(1)
        elif selector.startswith('text='):
            text_match = selector.replace('text=', '')
            
        # Build more targeted fallback strategies
        strategies = []
        
        # If selector looks like it might be an ID (no special chars)
        if selector and not any(c in selector for c in ['#', '.', '[', '>', ' ', ':']):
            strategies.extend([
                f"#{selector}",  # ID selector
                f"[id='{selector}']",  # ID attribute
                f"[name='{selector}']",  # Name attribute
                f"input[name='{selector}']",  # Input with name
                f"textarea[name='{selector}']",  # Textarea with name
                f"button[name='{selector}']",  # Button with name
                f"select[name='{selector}']",  # Select with name
            ])
        
        # Text-based strategies if we have text
        if text_match:
            strategies.extend([
                f"text={text_match}",
                f"button:has-text('{text_match}')",
                f"a:has-text('{text_match}')",
                f"[aria-label='{text_match}']",
                f"[aria-label*='{text_match}' i]",
                f"button >> text={text_match}",
                f"a >> text={text_match}",
            ])
        
        # Try each strategy
        for strategy in strategies:
            try:
                count = self.page.locator(strategy).count()
                if count > 0:
                    # Only use this strategy if it finds exactly one element
                    # or if it's a very specific selector (ID, name, etc.)
                    if count == 1 or strategy.startswith('#') or strategy.startswith('[id=') or strategy.startswith('[name='):
                        return strategy
            except Exception:
                continue
        
        # Return original if none work (will fail with better error message)
        return selector

    def _take_screenshot(self, action_type: str) -> str:
        """Take a screenshot and return the path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{action_type}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        self.page.screenshot(path=filepath)
        return filepath

    def execute(self, action: Action) -> ExecutionStepResult:
        start_time = time.time()
        screenshot_path = None
        
        try:
            if action.type == "navigate":
                # Use domcontentloaded instead of networkidle for faster loading
                self.page.goto(action.value, wait_until="domcontentloaded", timeout=30000)
                # Small wait to ensure page is stable
                self.page.wait_for_timeout(500)

            elif action.type == "click":
                adaptive_selector = self._adaptive_selector(action.selector)
                self.page.click(adaptive_selector, timeout=10000)

            elif action.type == "fill":
                # Use adaptive selector directly without smart discovery
                adaptive_selector = self._adaptive_selector(action.selector)
                # Clear and fill in one smooth operation
                self.page.fill(adaptive_selector, "", timeout=10000)
                self.page.fill(adaptive_selector, str(action.value), timeout=10000)

            elif action.type == "wait":
                self.page.wait_for_timeout(int(action.value))

            elif action.type == "screenshot":
                screenshot_path = self._take_screenshot(action.value or "manual")

            elif action.type == "scroll":
                if action.value in ["top", "bottom"]:
                    script = "window.scrollTo({top: 0, behavior: 'auto'})" if action.value == "top" else "window.scrollTo({top: document.body.scrollHeight, behavior: 'auto'})"
                    self.page.evaluate(script)
                elif action.value in ["up", "down"]:
                    pixels = -500 if action.value == "up" else 500
                    self.page.evaluate(f"window.scrollBy({{top: {pixels}, behavior: 'auto'}})")
                else:
                    # Assume it's a pixel value
                    self.page.evaluate(f"window.scrollBy({{top: {action.value}, behavior: 'auto'}})")

            elif action.type == "select_dropdown":
                adaptive_selector = self._adaptive_selector(action.selector)
                self.page.select_option(adaptive_selector, label=action.value, timeout=10000)

            elif action.type == "check_checkbox":
                adaptive_selector = self._adaptive_selector(action.selector)
                # Determine if we should check or uncheck
                # Default to checking if value is not explicitly "false", "0", "no", or "unchecked"
                should_check = action.value.lower() not in ["false", "0", "no", "unchecked", "uncheck"]
                
                # Use force=True to ensure checkbox is clicked even if partially obscured
                if should_check:
                    self.page.check(adaptive_selector, timeout=10000, force=True)
                else:
                    self.page.uncheck(adaptive_selector, timeout=10000, force=True)

            elif action.type == "assert_visible":
                adaptive_selector = self._adaptive_selector(action.selector)
                self.page.wait_for_selector(adaptive_selector, state="visible", timeout=10000)

            elif action.type == "assert_text":
                adaptive_selector = self._adaptive_selector(action.selector)
                element = self.page.locator(adaptive_selector)
                actual_text = element.inner_text(timeout=10000)
                if action.value not in actual_text:
                    raise AssertionError(f"Expected text '{action.value}' not found. Actual: '{actual_text}'")

            elif action.type == "assert_url":
                current_url = self.page.url
                if action.value not in current_url:
                    raise AssertionError(f"Expected URL pattern '{action.value}' not found. Actual: '{current_url}'")

            else:
                raise ValueError(f"Unsupported action type: {action.type}")

            # Take screenshot after successful action (except for screenshot action itself)
            if action.type != "screenshot" and action.type != "wait":
                screenshot_path = self._take_screenshot(action.type)

            execution_time = int((time.time() - start_time) * 1000)
            
            return ExecutionStepResult(
                action=action,
                success=True,
                screenshot_path=screenshot_path,
                execution_time_ms=execution_time
            )

        except PlaywrightTimeoutError as e:
            execution_time = int((time.time() - start_time) * 1000)
            error_msg = f"Timeout: Element '{action.selector}' not found or not interactable within 10s"
            
            # Try to take error screenshot
            try:
                screenshot_path = self._take_screenshot(f"error_{action.type}")
            except:
                pass
                
            return ExecutionStepResult(
                action=action,
                success=False,
                error=error_msg,
                screenshot_path=screenshot_path,
                execution_time_ms=execution_time
            )

        except AssertionError as e:
            execution_time = int((time.time() - start_time) * 1000)
            
            # Take error screenshot
            try:
                screenshot_path = self._take_screenshot(f"assertion_failed_{action.type}")
            except:
                pass
                
            return ExecutionStepResult(
                action=action,
                success=False,
                error=str(e),
                screenshot_path=screenshot_path,
                execution_time_ms=execution_time
            )

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            # Try to take error screenshot
            try:
                screenshot_path = self._take_screenshot(f"error_{action.type}")
            except:
                pass
                
            return ExecutionStepResult(
                action=action,
                success=False,
                error=error_msg,
                screenshot_path=screenshot_path,
                execution_time_ms=execution_time
            )

    def close(self):
        """Close browser with proper cleanup and delay"""
        try:
            # Wait 10 seconds so user can see the final state
            print("✓ Test complete! Browser will close in 10 seconds...")
            time.sleep(10)
            
            # Close in proper order
            if hasattr(self, 'page') and self.page:
                try:
                    self.page.close()
                except:
                    pass
            
            if hasattr(self, 'browser') and self.browser:
                try:
                    self.browser.close()
                except:
                    pass
            
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    self.playwright.stop()
                except:
                    pass
                    
        except Exception as e:
            # Silently handle cleanup errors
            pass

