# agent/executor.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import uuid
import os
import re

class Executor:

    def heal_selector(self, page, selector, action_hint="perform action"):
        """
        Attempt to fix selectors when they fail using:
        - CSS fallback
        - Partial text search
        - Heuristic DOM scanning
        - AI-powered DOM analysis (Grok)
        """

        # 1. Try alternative selectors (Heuristics)
        alternatives = [
            selector,
            selector.replace("input", "textarea"),
            selector.replace("textarea", "input"),
            selector.replace("'", '"'),
            selector.replace('"', "'"),
            "input[type='text']",
            "textarea",
            "input",
        ]

        for alt in alternatives:
            try:
                page.wait_for_selector(alt, timeout=2000)
                return alt, "HEURISTIC"
            except:
                pass

        # 2. Try fuzzy searching the DOM (Heuristics)
        try:
            elements = page.query_selector_all("*")
            for el in elements:
                try:
                    outer = el.evaluate("e => e.outerHTML")[:200].lower()
                    if any(key in outer for key in ["search", "input", "query", "text"]):
                        healed = el.evaluate("e => e.tagName.toLowerCase()")
                        return healed, "HEURISTIC"
                except:
                    pass
        except:
            pass

        # 3. AI Powered Healing (Grok) fallback
        try:
            from .ai_selector import AISelectorHealer
            healer = AISelectorHealer()
            html_snippet = page.content()
            ai_healed = healer.heal(html_snippet, selector, action_hint)
            
            if ai_healed:
                return ai_healed, "AI"
        except Exception as e:
            print(f"AI Healing failed: {e}")

        # If nothing works, return original
        return selector, "NONE"

    def execute_actions(self, actions, settings=None):
        settings = settings or {"headless": True, "timeout": 5000}
        
        # Force ProactorEventLoop on Windows for subprocess support (Playwright requirement)
        import asyncio
        import sys
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        from .smart_waits import SmartWait
        
        logs = []
        screenshots = []
        video_path = None
        global_timeout = settings.get("timeout", 5000)

        is_headless = settings.get("headless", True)
        slow_mo = 0 if is_headless else 500  # Add delay for headed mode visibility/stability

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=is_headless, slow_mo=slow_mo)
            
            # Standardize viewport for consistent layout across modes
            context = browser.new_context(
                record_video_dir="tests/videos/",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            
            if not is_headless:
                page.bring_to_front()
                
            page.set_default_timeout(global_timeout)

            self.wait = SmartWait()  # Smart waits

            for act in actions:
                retry_count = 0
                max_retries = 1
                action_success = False
                
                while retry_count <= max_retries and not action_success:
                    try:
                        # GOTO
                        if act["action"] == "goto":
                            # Use domcontentloaded for faster initial entry, then rely on SmartWait
                            page.goto(act["value"], timeout=global_timeout, wait_until="domcontentloaded")
                            logs.append(f"[OK] Navigated to {act['value']}")
                            self.wait.wait_dom_ready(page)
                            self.wait.wait_network_idle(page)
                            logs.append("[WAIT] DOM ready & network idle")

                        # CLICK
                        elif act["action"] == "click":
                            selector = act["value"]
                            if not self.wait.wait_for_element(page, selector, timeout=global_timeout):
                                healed, mode = self.heal_selector(page, selector, action_hint=f"click {selector}")
                                logs.append(f"[{mode} HEAL] Click selector healed to: {healed}")
                                selector = healed
                            page.click(selector, timeout=global_timeout)
                            logs.append(f"[OK] Clicked {selector}")

                        # TYPE
                        elif act["action"] == "type":
                            selector = act["field"]
                            value = act["value"]
                            if not self.wait.wait_for_element(page, selector, timeout=global_timeout):
                                healed, mode = self.heal_selector(page, selector, action_hint=f"type '{value}' into {selector}")
                                logs.append(f"[{mode} HEAL] Type selector healed to: {healed}")
                                selector = healed
                            try:
                                page.fill(selector, value, timeout=global_timeout)
                                logs.append(f"[OK] Typed '{value}'")
                            except:
                                page.click(selector)
                                page.keyboard.type(value)
                                logs.append(f"[FALLBACK] Typed '{value}' using keyboard")

                        # ASSERT TEXT
                        elif act["action"] == "assert_text":
                            content = page.content().lower()
                            expected = act["value"].lower()
                            self.wait.wait_dom_ready(page)
                            if expected in content:
                                logs.append(f"[ASSERT OK] Found text: {expected}")
                            else:
                                raise Exception(f"Expected text not found: {expected}")
                        
                        action_success = True

                    except Exception as e:
                        retry_count += 1
                        if retry_count > max_retries:
                            screenshot = f"tests/screenshots/error_{uuid.uuid4()}.png"
                            try:
                                page.screenshot(path=screenshot, timeout=3000, animations="disabled")
                                screenshots.append(screenshot)
                                logs.append(f"[SCREENSHOT] {screenshot}")
                            except:
                                logs.append("[SCREENSHOT FAILED] Could not capture screenshot within timeout")
                            
                            logs.append(f"[ERROR] {str(e)}")
                            if page.video: video_path = page.video.path()
                            return {"success": False, "logs": logs, "screenshots": screenshots, "video": video_path}
                        else:
                            logs.append(f"[RETRY] Retrying action due to: {str(e)[:50]}...")
                            import time
                            time.sleep(1)

            if page.video: video_path = page.video.path()
            context.close()
            return {"success": True, "logs": logs, "screenshots": screenshots, "video": video_path}
