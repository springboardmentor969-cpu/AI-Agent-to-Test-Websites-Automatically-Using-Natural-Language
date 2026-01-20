from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import logging
import uuid
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def execute_actions(actions, assertions):
    try:
        # Force ProactorEventLoop on Windows for subprocess support (Playwright requirement)
        import asyncio
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        from src.smart_waits import SmartWait
        from src.ai_selector import AISelectorHealer

        logs = []
        screenshots = []
        video_path = None
        global_timeout = 5000  # Increased from 5000ms to 15000ms (15 seconds)

        is_headless = False  # Keep visible for now
        slow_mo = 0 if is_headless else 500

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=is_headless, slow_mo=slow_mo)

            context = browser.new_context(
                record_video_dir="tests/videos/",
                viewport={'width': 1280, 'height': 1024}
            )
            page = context.new_page()

            if not is_headless:
                page.bring_to_front()

            page.set_default_timeout(global_timeout)

            wait = SmartWait()
            healer = AISelectorHealer()

            for action in actions:
                retry_count = 0
                max_retries = 1
                action_success = False

                while retry_count <= max_retries and not action_success:
                    try:
                        logger.info(f"Executing action: {action}")
                        logs.append(f"Executing: {action}")

                        if action["action"] == "navigate":
                            # Use different wait strategies for different sites
                            url_lower = action["url"].lower()
                            wait_until = "domcontentloaded"

                            # For heavy sites like YouTube, Facebook, Instagram, wait for full load
                            if any(site in url_lower for site in ["youtube", "facebook", "instagram", "twitter", "linkedin"]):
                                wait_until = "load"  # Wait for full page load on social media sites
                                logs.append(f"[INFO] Using full page load for {url_lower} (may take longer)")

                            page.goto(action["url"], timeout=global_timeout, wait_until=wait_until)
                            logs.append(f"[OK] Navigated to {action['url']}")
                            wait.wait_dom_ready(page)
                            wait.wait_network_idle(page)
                            logs.append("[WAIT] DOM ready & network idle")

                        elif action["action"] == "fill":
                            selector = action["field"]
                            value = action["value"]

                            # Try to find the field
                            field_selectors = [
                                f'[name="{selector}"]',
                                f'#{selector}',
                                f'[placeholder*="{selector}"]',
                                f'input[type="text"]',
                                f'textarea',
                                f'input',
                            ]

                            filled = False
                            for sel in field_selectors:
                                try:
                                    page.wait_for_selector(sel, timeout=2000)
                                    page.fill(sel, value, timeout=global_timeout)
                                    filled = True
                                    logs.append(f"[OK] Filled '{value}' in {sel}")
                                    break
                                except:
                                    continue

                            if not filled:
                                # Try AI healing
                                html_snippet = page.content()
                                healed = healer.heal(html_snippet, selector, f"fill '{value}' in {selector}")
                                if healed != selector:
                                    try:
                                        page.fill(healed, value, timeout=global_timeout)
                                        logs.append(f"[AI HEAL] Filled '{value}' in healed selector: {healed}")
                                        filled = True
                                    except:
                                        pass

                            if not filled:
                                raise Exception(f"Could not find input field for '{selector}'")

                        elif action["action"] == "click":
                            element = action["element"]
                            selectors = [
                                f'[name="{element}"]',
                                f'#{element}',
                                f'button:has-text("{element}")',
                                f'a:has-text("{element}")',
                                f'[value="{element}"]',
                                f'input[type="submit"]',
                                f'[aria-label*="Search"]',
                                f'[role="button"]:has-text("{element}")',
                                f'input[name="btnK"]',
                                f'input[value="Google Search"]',
                            ]

                            clicked = False
                            for sel in selectors:
                                try:
                                    page.wait_for_selector(sel, timeout=2000)
                                    page.click(sel, timeout=global_timeout)
                                    clicked = True
                                    logs.append(f"[OK] Clicked {sel}")
                                    break
                                except:
                                    continue

                            if not clicked:
                                # AI healing
                                html_snippet = page.content()
                                healed = healer.heal(html_snippet, element, f"click {element}")
                                if healed != element:
                                    try:
                                        page.click(healed, timeout=global_timeout)
                                        logs.append(f"[AI HEAL] Clicked healed selector: {healed}")
                                        clicked = True
                                    except:
                                        pass

                            if not clicked:
                                raise Exception(f"Could not find clickable element '{element}'")

                        elif action["action"] == "press_enter":
                            field = action["field"]
                            value = action.get("value", "")

                            # If value is provided, fill the field first
                            if value:
                                field_selectors = [
                                    f'[name="{field}"]',
                                    f'#{field}',
                                    f'[placeholder*="{field}"]',
                                    f'input[type="text"]',
                                    f'textarea',
                                    f'input',
                                ]

                                filled = False
                                for sel in field_selectors:
                                    try:
                                        page.wait_for_selector(sel, timeout=2000)
                                        page.fill(sel, value, timeout=global_timeout)
                                        filled = True
                                        logs.append(f"[OK] Filled '{value}' in {sel}")
                                        break
                                    except:
                                        continue

                                if not filled:
                                    # Try AI healing
                                    html_snippet = page.content()
                                    healed = healer.heal(html_snippet, field, f"fill '{value}' in {field}")
                                    if healed != field:
                                        try:
                                            page.fill(healed, value, timeout=global_timeout)
                                            logs.append(f"[AI HEAL] Filled '{value}' in healed selector: {healed}")
                                            filled = True
                                        except:
                                            pass

                                if not filled:
                                    raise Exception(f"Could not find input field for '{field}'")

                            # Now press Enter
                            selectors = [
                                f'[name="{field}"]',
                                f'#{field}',
                                f'[placeholder*="{field}"]',
                                f'input[type="text"]',
                            ]

                            pressed = False
                            for sel in selectors:
                                try:
                                    page.press(sel, "Enter")
                                    pressed = True
                                    logs.append(f"[OK] Pressed Enter in {sel}")
                                    # Wait for navigation to complete after search
                                    if value:
                                        wait.wait_dom_ready(page)
                                        wait.wait_network_idle(page)
                                        logs.append("[WAIT] Search results loaded")
                                        # Take screenshot immediately after search results load
                                        search_screenshot = os.path.join(os.getcwd(), "tests", "screenshots", f"search_result_{uuid.uuid4()}.png")
                                        try:
                                            page.screenshot(path=search_screenshot, timeout=3000, full_page=True)
                                            screenshots.append(search_screenshot)
                                            logs.append(f"[SCREENSHOT] Search results: {search_screenshot}")
                                        except Exception as e:
                                            logs.append(f"[SCREENSHOT FAILED] Could not capture search screenshot: {e}")
                                    break
                                except:
                                    continue

                            if not pressed:
                                raise Exception(f"Could not find field '{field}' to press Enter in")

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
                            return {
                                "success": False,
                                "logs": logs,
                                "screenshots": screenshots,
                                "video": video_path
                            }
                        else:
                            logs.append(f"[RETRY] Retrying action due to: {str(e)[:50]}...")
                            time.sleep(1)
            # -------------------------
            # Assertions
            # -------------------------
            for assertion in assertions:
                logger.info(f"Checking assertion: {assertion}")
                logs.append(f"Checking assertion: {assertion}")

                if assertion["type"] == "url_contains":
                    if assertion["value"] not in page.url:
                        raise Exception(f"URL assertion failed: expected '{assertion['value']}' in {page.url}")
                    logs.append(f"[ASSERT OK] URL contains '{assertion['value']}'")

                elif assertion["type"] == "field_value":
                    field = assertion["field"]
                    selectors = [
                        f'[name="{field}"]',
                        f'#{field}',
                        f'[placeholder*="{field}"]',
                        f'input[type="text"]',
                    ]

                    actual_value = None
                    for sel in selectors:
                        try:
                            actual_value = page.input_value(sel)
                            break
                        except Exception:
                            continue

                    if actual_value is None:
                        raise Exception(f"Could not find input field '{field}' for assertion")

                    expected_value = assertion["value"]
                    if actual_value != expected_value:
                        raise Exception(f"Field assertion failed: field '{field}' has '{actual_value}', expected '{expected_value}'")
                    logs.append(f"[ASSERT OK] Field '{field}' has value '{expected_value}'")

                elif assertion["type"] == "text_contains":
                    text = assertion["value"]
                    if page.locator(f"text={text}").count() == 0:
                        raise Exception(f"Text assertion failed: '{text}' not found on page")
                    logs.append(f"[ASSERT OK] Text '{text}' found on page")

            # Take a final screenshot on success to show the result
            import os
            screenshot_dir = os.path.join(os.getcwd(), "tests", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            final_screenshot = os.path.join(screenshot_dir, f"success_{uuid.uuid4()}.png")
            try:
                # Small delay to ensure page is stable
                import time
                time.sleep(0.5)
                page.screenshot(path=final_screenshot, timeout=3000, full_page=True)
                screenshots.append(final_screenshot)
                logs.append(f"[SCREENSHOT] Final result: {final_screenshot}")
                logs.append(f"[SCREENSHOT] File exists: {os.path.exists(final_screenshot)}")
            except Exception as e:
                logs.append(f"[SCREENSHOT FAILED] Could not capture final screenshot: {e}")
                # Try a fallback screenshot without full_page
                try:
                    fallback_screenshot = os.path.join(screenshot_dir, f"success_fallback_{uuid.uuid4()}.png")
                    page.screenshot(path=fallback_screenshot, timeout=2000, full_page=False)
                    screenshots.append(fallback_screenshot)
                    logs.append(f"[SCREENSHOT] Fallback result: {fallback_screenshot}")
                    logs.append(f"[SCREENSHOT] Fallback file exists: {os.path.exists(fallback_screenshot)}")
                except Exception as e2:
                    logs.append(f"[SCREENSHOT] All screenshot attempts failed: {e2}")

            if page.video: video_path = page.video.path()
            context.close()

            return {
                "success": True,
                "logs": logs,
                "screenshots": screenshots,
                "video": video_path
            }

    except Exception as e:
        return {
            "success": False,
            "logs": logs if 'logs' in locals() else [],
            "screenshots": screenshots if 'screenshots' in locals() else [],
            "video": video_path if 'video_path' in locals() else None,
            "error": str(e)
        }
