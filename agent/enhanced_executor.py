# agent/enhanced_executor.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page
import uuid
import os
import re
import time
from typing import Dict, List, Any, Optional

from .smart_waits import SmartWait
from .ai_selector import AISelectorHealer
from .error_handler import ErrorHandler, ErrorCategory
from .advanced_actions import (
    IframeHandler, FileHandler, TabManager, DataExtractor, 
    ScrollManager, InteractionHandler
)
from .config import Config

class EnhancedExecutor:
    """
    Enhanced executor with support for complex actions, intelligent error handling,
    and advanced web interactions.
    """
    
    def __init__(self):
        self.wait = SmartWait()
        self.healer = AISelectorHealer(use_cache=True)
        self.error_handler = ErrorHandler()
        self.tab_manager = TabManager()
        self.variables: Dict[str, Any] = {}
        
        # Validate configuration
        Config.validate()
    
    def execute_actions(self, actions: List[Dict], settings: Optional[Dict] = None) -> Dict:
        """
        Execute list of actions with enhanced error handling and recovery
        """
        settings = settings or {}
        
        # Merge with default config
        is_headless = settings.get("headless", Config.HEADLESS_MODE)
        global_timeout = settings.get("timeout", Config.DEFAULT_TIMEOUT)
        
        # Force ProactorEventLoop on Windows
        import asyncio
        import sys
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        logs = []
        screenshots = []
        video_path = None
        console_logs = []
        
        slow_mo = 0 if is_headless else Config.SLOW_MO
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=is_headless, slow_mo=slow_mo)
            
            context = browser.new_context(
                record_video_dir=Config.VIDEO_DIR if Config.VIDEO_RECORDING_ENABLED else None,
                viewport={'width': Config.VIEWPORT_WIDTH, 'height': Config.VIEWPORT_HEIGHT}
            )
            
            page = context.new_page()
            
            # Capture console logs if enabled
            if Config.INCLUDE_CONSOLE_LOGS:
                page.on("console", lambda msg: console_logs.append(f"[CONSOLE] {msg.type}: {msg.text}"))
            
            if not is_headless:
                page.bring_to_front()
            
            page.set_default_timeout(global_timeout)
            
            # Execute actions
            for i, act in enumerate(actions):
                action_type = act.get("action", "unknown")
                logs.append(f"\n[STEP {i+1}] Executing: {action_type}")
                
                success, action_logs, action_screenshots = self._execute_single_action(
                    page, act, global_timeout, settings
                )
                
                logs.extend(action_logs)
                screenshots.extend(action_screenshots)
                
                if not success:
                    # Capture error screenshot
                    error_screenshot = f"tests/screenshots/error_{uuid.uuid4()}.png"
                    try:
                        os.makedirs(os.path.dirname(error_screenshot), exist_ok=True)
                        page.screenshot(path=error_screenshot, timeout=3000, animations="disabled")
                        screenshots.append(error_screenshot)
                        logs.append(f"[SCREENSHOT] {error_screenshot}")
                    except:
                        logs.append("[SCREENSHOT FAILED] Could not capture error screenshot")
                    
                    # Get video path before closing
                    if page.video:
                        video_path = page.video.path()
                    
                    context.close()
                    browser.close()
                    
                    return {
                        "success": False,
                        "logs": logs,
                        "screenshots": screenshots,
                        "video": video_path,
                        "console_logs": console_logs if Config.INCLUDE_CONSOLE_LOGS else [],
                        "error_stats": self.error_handler.get_error_statistics()
                    }
                
                # Optional: Screenshot each step
                if Config.SCREENSHOT_EACH_STEP:
                    step_screenshot = f"tests/screenshots/step_{i+1}_{uuid.uuid4()}.png"
                    try:
                        os.makedirs(os.path.dirname(step_screenshot), exist_ok=True)
                        page.screenshot(path=step_screenshot, timeout=3000)
                        screenshots.append(step_screenshot)
                    except:
                        pass
            
            # Success - get video path
            if page.video:
                video_path = page.video.path()
            
            context.close()
            browser.close()
            
            # Final success screenshot
            if Config.SCREENSHOT_ON_SUCCESS and screenshots:
                logs.append(f"[SUCCESS] All {len(actions)} actions completed successfully")
            
            return {
                "success": True,
                "logs": logs,
                "screenshots": screenshots,
                "video": video_path,
                "console_logs": console_logs if Config.INCLUDE_CONSOLE_LOGS else [],
                "variables": self.variables,
                "healing_stats": self.healer.get_healing_stats()
            }
    
    def _execute_single_action(self, page: Page, action: Dict, timeout: int, settings: Dict) -> tuple:
        """
        Execute a single action with retry logic and error handling
        
        Returns:
            Tuple of (success: bool, logs: List[str], screenshots: List[str])
        """
        logs = []
        screenshots = []
        action_type = action.get("action")
        retry_count = 0
        max_retries = Config.MAX_RETRIES
        
        while retry_count <= max_retries:
            try:
                # Execute the action
                action_logs = self._perform_action(page, action, timeout)
                logs.extend(action_logs)
                
                # Smart wait after action
                if Config.SMART_WAIT_ENABLED:
                    self.wait.smart_wait_after_action(page, action_type)
                
                return True, logs, screenshots
                
            except Exception as e:
                # Handle error
                error_details = self.error_handler.handle_error(
                    e, action, 
                    context={'page_url': page.url, 'retry_count': retry_count}
                )
                
                category = ErrorCategory(error_details['category'])
                should_retry, wait_time = self.error_handler.should_retry(category, retry_count, max_retries)
                
                if should_retry and retry_count < max_retries:
                    retry_count += 1
                    logs.append(f"[RETRY {retry_count}/{max_retries}] {error_details['category']}: {str(e)[:100]}")
                    
                    # Wait before retry with exponential backoff
                    if wait_time > 0:
                        time.sleep(wait_time / 1000)
                    
                    # Try healing for element not found errors
                    if category == ErrorCategory.ELEMENT_NOT_FOUND and Config.AI_HEALING_ENABLED:
                        logs.append("[AI HEALING] Attempting to heal selector...")
                else:
                    # Max retries reached or non-retryable error
                    logs.append(f"[ERROR] {error_details['category']}: {str(e)}")
                    logs.append(f"[SUGGESTIONS] {', '.join(error_details['recovery_strategies'][:2])}")
                    return False, logs, screenshots
        
        return False, logs, screenshots
    
    def _perform_action(self, page: Page, action: Dict, timeout: int) -> List[str]:
        """Perform the actual action and return logs"""
        logs = []
        action_type = action.get("action")
        
        # Get action-specific timeout
        action_timeout = Config.get_timeout(action_type)
        
        # === NAVIGATION ===
        if action_type == "goto":
            url = action.get("value", "")
            url = self._replace_variables(url)
            
            page.goto(url, timeout=action_timeout, wait_until="domcontentloaded")
            logs.append(f"[OK] Navigated to {url}")
            
            self.wait.wait_dom_ready(page)
            self.wait.wait_network_idle(page)
            logs.append("[WAIT] DOM ready & network idle")
        
        # === CLICK ===
        elif action_type == "click":
            selector = action.get("value", "")
            selector = self._replace_variables(selector)
            
            if not self.wait.wait_for_element_clickable(page, selector, timeout=action_timeout):
                # Try healing
                healed = self.healer.heal(
                    page.content(), selector, f"click {selector}",
                    page_url=page.url, page_title=page.title()
                )
                logs.append(f"[AI HEAL] Selector healed: {selector} → {healed}")
                selector = healed
            
            page.click(selector, timeout=action_timeout)
            logs.append(f"[OK] Clicked: {selector}")
        
        # === TYPE ===
        elif action_type == "type":
            selector = action.get("field", "input")
            value = action.get("value", "")
            selector = self._replace_variables(selector)
            value = self._replace_variables(value)
            
            if not self.wait.wait_for_element(page, selector, timeout=action_timeout):
                healed = self.healer.heal(
                    page.content(), selector, f"type '{value}' into {selector}",
                    page_url=page.url, page_title=page.title()
                )
                logs.append(f"[AI HEAL] Selector healed: {selector} → {healed}")
                selector = healed
            
            try:
                page.fill(selector, value, timeout=action_timeout)
                logs.append(f"[OK] Typed '{value}' into {selector}")
            except:
                # Fallback to keyboard typing
                page.click(selector)
                page.keyboard.type(value)
                logs.append(f"[FALLBACK] Typed '{value}' using keyboard")
        
        # === HOVER ===
        elif action_type == "hover":
            selector = action.get("value", "")
            selector = self._replace_variables(selector)
            
            InteractionHandler.hover(page, selector, timeout=action_timeout)
            logs.append(f"[OK] Hovered over: {selector}")
        
        # === SELECT ===
        elif action_type == "select":
            selector = action.get("field", "select")
            value = action.get("value")
            label = action.get("label")
            
            InteractionHandler.select_option(page, selector, value=value, label=label, timeout=action_timeout)
            logs.append(f"[OK] Selected option in: {selector}")
        
        # === SCROLL ===
        elif action_type == "scroll":
            direction = action.get("direction", "down")
            value = action.get("value", 500)
            
            if direction == "to_element":
                ScrollManager.scroll_to_element(page, str(value))
                logs.append(f"[OK] Scrolled to element: {value}")
            elif direction == "down":
                ScrollManager.scroll_by_pixels(page, y=int(value))
                logs.append(f"[OK] Scrolled down {value}px")
            elif direction == "up":
                ScrollManager.scroll_by_pixels(page, y=-int(value))
                logs.append(f"[OK] Scrolled up {value}px")
        
        # === WAIT ===
        elif action_type == "wait":
            condition = action.get("condition", "time")
            value = action.get("value", 1000)
            
            if condition == "time":
                time.sleep(int(value) / 1000)
                logs.append(f"[WAIT] Waited {value}ms")
            elif condition == "element":
                self.wait.wait_for_element(page, str(value), timeout=action_timeout)
                logs.append(f"[WAIT] Waited for element: {value}")
            elif condition == "text":
                self.wait.wait_for_text(page, str(value), timeout=action_timeout)
                logs.append(f"[WAIT] Waited for text: {value}")
        
        # === EXTRACT DATA ===
        elif action_type == "extract":
            selector = action.get("field", "")
            variable = action.get("variable", "extracted_value")
            attribute = action.get("attribute")
            
            if attribute:
                extracted = DataExtractor.extract_attribute(page, selector, attribute)
            else:
                extracted = DataExtractor.extract_text(page, selector)
            
            self.variables[variable] = extracted
            logs.append(f"[EXTRACT] Saved '{extracted}' as {{{variable}}}")
        
        # === UPLOAD FILE ===
        elif action_type == "upload":
            selector = action.get("field", "input[type='file']")
            file_path = action.get("value", "")
            file_path = self._replace_variables(file_path)
            
            FileHandler.upload_file(page, selector, file_path, timeout=action_timeout)
            logs.append(f"[OK] Uploaded file: {file_path}")
        
        # === PRESS KEY ===
        elif action_type == "press_key":
            key = action.get("value", "Enter")
            selector = action.get("field")
            
            InteractionHandler.press_key(page, key, selector=selector)
            logs.append(f"[OK] Pressed key: {key}")
        
        # === ASSERT TEXT ===
        elif action_type == "assert_text":
            expected = action.get("value", "")
            expected = self._replace_variables(expected)
            
            logs.append(f"[CHECK] Verifying text: '{expected}'...")
            
            # Use smart wait to poll for text (silent wait)
            if self.wait.wait_for_text(page, expected, timeout=action_timeout):
                logs.append(f"[ASSERT OK] Found text: '{expected}'")
            else:
                # Only raise error after timeout
                raise AssertionError(f"Expected text not found: '{expected}' after {action_timeout}ms")
        
        # === ASSERT ELEMENT ===
        elif action_type == "assert_element":
            selector = action.get("value", "")
            selector = self._replace_variables(selector)
            
            if self.wait.wait_for_element(page, selector, timeout=action_timeout):
                logs.append(f"[ASSERT OK] Element exists: {selector}")
            else:
                raise AssertionError(f"Element not found: {selector}")
        
        # === EXECUTE JAVASCRIPT ===
        elif action_type == "execute_js":
            js_code = action.get("value", "")
            result = page.evaluate(js_code)
            logs.append(f"[JS] Executed JavaScript, result: {result}")
        
        else:
            logs.append(f"[WARNING] Unknown action type: {action_type}")
        
        return logs
    
    def _replace_variables(self, text: str) -> str:
        """Replace {{variable}} placeholders with actual values"""
        if not isinstance(text, str):
            return text
        
        for var_name, var_value in self.variables.items():
            text = text.replace(f"{{{{{var_name}}}}}", str(var_value))
        
        return text
