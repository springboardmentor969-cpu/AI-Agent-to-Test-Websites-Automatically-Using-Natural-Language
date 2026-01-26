# agent/executor.py

from playwright.sync_api import sync_playwright
import uuid
import os
import time

class Executor:
    """
    Robust Web Testing Executor
    """

    def execute_actions(self, actions, settings=None):
        settings = settings or {"headless": True, "timeout": 30000}
        
        import asyncio
        import sys
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        logs = []
        screenshots = []
        video_path = None
        timeout = settings.get("timeout", 30000)
        is_headless = settings.get("headless", True)

        os.makedirs("tests/screenshots", exist_ok=True)
        os.makedirs("tests/videos", exist_ok=True)

        print(f"\n[EXECUTOR] Starting with {len(actions)} actions")
        logs.append(f"[INFO] Starting execution with {len(actions)} actions")
        
        for i, act in enumerate(actions):
            print(f"[EXECUTOR] Action {i+1}: {act}")
            logs.append(f"[INFO] Action {i+1}: {act.get('action')} - {str(act)[:80]}")

        current_site = ""

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(
                headless=is_headless,
                slow_mo=100 if not is_headless else 0
            )
            
            context = browser.new_context(
                record_video_dir="tests/videos/",
                viewport={'width': 1366, 'height': 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            
            page = context.new_page()
            page.set_default_timeout(timeout)

            try:
                for act_idx, act in enumerate(actions):
                    action_type = act.get("action")
                    logs.append(f"\n[STEP {act_idx + 1}] {action_type.upper()}")
                    print(f"\n[EXECUTOR] === Step {act_idx + 1}: {action_type} ===")

                    # ==================== GOTO ====================
                    if action_type == "goto":
                        url = act["value"]
                        print(f"[EXECUTOR] Navigating to: {url}")
                        
                        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
                        logs.append(f"[OK] Navigated to {url}")
                        
                        # Detect site type
                        url_lower = url.lower()
                        if "amazon" in url_lower:
                            current_site = "amazon"
                            logs.append("[INFO] Site detected: Amazon")
                        elif "instagram" in url_lower:
                            current_site = "instagram"
                            logs.append("[INFO] Site detected: Instagram")
                        elif "google.com/maps" in url_lower or "maps.google" in url_lower:
                            current_site = "google_maps"
                            logs.append("[INFO] Site detected: Google Maps")
                        elif "google.com/forms" in url_lower or "docs.google.com/forms" in url_lower:
                            current_site = "google_forms"
                            logs.append("[INFO] Site detected: Google Forms")
                        elif "facebook" in url_lower:
                            current_site = "facebook"
                            logs.append("[INFO] Site detected: Facebook")
                        elif "twitter" in url_lower or "x.com" in url_lower:
                            current_site = "twitter"
                            logs.append("[INFO] Site detected: Twitter/X")
                        else:
                            current_site = "generic"
                        
                        # Wait for page to be interactive
                        time.sleep(3)
                        print(f"[EXECUTOR] Page loaded, site type: {current_site}")

                    # ==================== SEARCH ====================
                    elif action_type == "search":
                        search_text = act["value"]
                        print(f"[EXECUTOR] Searching for: '{search_text}'")
                        logs.append(f"[INFO] Searching for: '{search_text}'")
                        
                        if current_site == "amazon":
                            print("[EXECUTOR] Using Amazon search flow...")
                            logs.append("[INFO] Using Amazon-specific search")
                            
                            # Wait for search box
                            search_box = None
                            search_selectors = [
                                "#twotabsearchtextbox",
                                "input[name='field-keywords']",
                                "input[id*='search']",
                                "input[placeholder*='Search']"
                            ]
                            
                            for sel in search_selectors:
                                try:
                                    print(f"[EXECUTOR] Trying search selector: {sel}")
                                    page.wait_for_selector(sel, timeout=5000)
                                    search_box = sel
                                    print(f"[EXECUTOR] Found search box: {sel}")
                                    break
                                except:
                                    continue
                            
                            if not search_box:
                                raise Exception("Could not find Amazon search box")
                            
                            # Clear and fill search box
                            page.click(search_box)
                            page.fill(search_box, "")
                            time.sleep(0.3)
                            page.fill(search_box, search_text)
                            logs.append(f"[OK] Typed '{search_text}' in search box")
                            print(f"[EXECUTOR] Filled search text: {search_text}")
                            
                            time.sleep(0.5)
                            
                            # Submit search
                            try:
                                page.click("#nav-search-submit-button", timeout=3000)
                                logs.append("[OK] Clicked search button")
                                print("[EXECUTOR] Clicked search button")
                            except:
                                page.keyboard.press("Enter")
                                logs.append("[OK] Pressed Enter to search")
                                print("[EXECUTOR] Pressed Enter")
                            
                            # Wait for results to load - increased time
                            print("[EXECUTOR] Waiting for search results...")
                            logs.append("[WAIT] Loading search results...")
                            time.sleep(5)
                            
                            # Scroll down to trigger lazy loading
                            page.evaluate("window.scrollBy(0, 300)")
                            time.sleep(2)
                            
                            # Verify we're on results page by checking URL or content
                            current_url = page.url
                            if "s?k=" in current_url or "/s?" in current_url:
                                logs.append("[OK] Search results URL confirmed")
                                print(f"[EXECUTOR] On search results page: {current_url[:60]}")
                            
                            # Try to find any product elements
                            product_check_selectors = [
                                "[data-component-type='s-search-result']",
                                ".s-result-item[data-asin]",
                                ".s-search-results .s-result-item",
                                "[data-asin]:not([data-asin=''])"
                            ]
                            
                            found_products = False
                            for check_sel in product_check_selectors:
                                try:
                                    page.wait_for_selector(check_sel, timeout=5000)
                                    count = len(page.query_selector_all(check_sel))
                                    if count > 0:
                                        logs.append(f"[OK] Found {count} product containers")
                                        print(f"[EXECUTOR] Found {count} products with {check_sel}")
                                        found_products = True
                                        break
                                except:
                                    continue
                            
                            if not found_products:
                                logs.append("[WARNING] Could not verify product containers, continuing anyway")
                                print("[EXECUTOR] Warning: Product verification failed")
                            
                            # Screenshot of results
                            ss_path = f"tests/screenshots/search_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] {ss_path}")
                        
                        elif current_site == "google_maps" or "google.com/maps" in page.url or "maps.google" in page.url:
                            # Google Maps search
                            print("[EXECUTOR] Using Google Maps search flow...")
                            logs.append("[INFO] Using Google Maps search")
                            
                            search_selectors = [
                                "#searchboxinput",
                                "input[name='q']",
                                "input[aria-label='Search Google Maps']",
                                "input[placeholder*='Search']"
                            ]
                            
                            filled = False
                            for sel in search_selectors:
                                try:
                                    page.wait_for_selector(sel, timeout=5000)
                                    page.fill(sel, search_text)
                                    filled = True
                                    logs.append(f"[OK] Typed '{search_text}' in Maps search")
                                    break
                                except:
                                    continue
                            
                            if filled:
                                page.keyboard.press("Enter")
                                logs.append("[OK] Pressed Enter to search")
                                time.sleep(3)
                            
                            # Screenshot
                            ss_path = f"tests/screenshots/maps_search_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] {ss_path}")
                        
                        else:
                            # Generic search
                            search_selectors = [
                                "input[type='search']",
                                "input[name='q']",
                                "input[placeholder*='Search']",
                                "input[aria-label*='Search']"
                            ]
                            
                            for sel in search_selectors:
                                try:
                                    page.fill(sel, search_text, timeout=5000)
                                    page.keyboard.press("Enter")
                                    logs.append(f"[OK] Searched for '{search_text}'")
                                    break
                                except:
                                    continue
                            
                            time.sleep(3)

                    # ==================== SELECT PRODUCT ====================
                    elif action_type == "select_product":
                        position = act.get("position", 1)
                        print(f"[EXECUTOR] Selecting product at position {position}")
                        logs.append(f"[INFO] Selecting product #{position}")
                        
                        # Give page more time to fully render
                        time.sleep(3)
                        
                        # Scroll down to trigger lazy loading
                        page.evaluate("window.scrollBy(0, 400)")
                        time.sleep(2)
                        
                        if current_site == "amazon":
                            print("[EXECUTOR] Using Amazon product selection...")
                            logs.append("[INFO] Using Amazon product selection")
                            
                            clicked = False
                            
                            # Method 1: Try clicking product title/link
                            # Look for h2 > a links which are product titles
                            try:
                                # Get all product title links
                                title_links = page.query_selector_all("h2 a.a-link-normal, h2 a[href*='/dp/']")
                                print(f"[EXECUTOR] Found {len(title_links)} product title links")
                                
                                if title_links and len(title_links) >= position:
                                    href = title_links[position - 1].get_attribute("href")
                                    if href:
                                        if not href.startswith("http"):
                                            href = "https://www.amazon.in" + href
                                        print(f"[EXECUTOR] Navigating to: {href[:70]}...")
                                        page.goto(href, wait_until="domcontentloaded")
                                        clicked = True
                                        logs.append(f"[OK] Opened product #{position}")
                            except Exception as e:
                                print(f"[EXECUTOR] Title link method failed: {e}")
                            
                            if not clicked:
                                # Method 2: Click on product image
                                try:
                                    images = page.query_selector_all(".s-image, img[data-image-latency='s-product-image']")
                                    print(f"[EXECUTOR] Found {len(images)} product images")
                                    if images and len(images) >= position:
                                        images[position - 1].click()
                                        clicked = True
                                        logs.append(f"[OK] Clicked product image #{position}")
                                except Exception as e:
                                    print(f"[EXECUTOR] Image click failed: {e}")
                            
                            if clicked:
                                time.sleep(4)
                                logs.append("[OK] Product page loaded")
                            else:
                                logs.append("[WARNING] Could not select product, continuing anyway")
                        
                        else:
                            # Generic product click
                            try:
                                page.click(f"a:nth-of-type({position})", timeout=timeout)
                                logs.append(f"[OK] Clicked item #{position}")
                            except:
                                logs.append("[WARNING] Could not select item")
                            time.sleep(2)

                    # ==================== ADD TO CART ====================
                    elif action_type == "add_to_cart":
                        print("[EXECUTOR] Adding to cart...")
                        logs.append("[INFO] Adding to cart")
                        
                        time.sleep(2)
                        
                        if current_site == "amazon":
                            # First check if we're on search results or product page
                            current_url = page.url
                            on_search_page = "/s?" in current_url or "s?k=" in current_url
                            
                            if on_search_page:
                                # On search results - click "Add to cart" button on first product
                                logs.append("[INFO] On search results page - clicking Add to cart button")
                                print("[EXECUTOR] On search results, looking for Add to cart button...")
                                
                                cart_btn_selectors = [
                                    "button.a-button-text:has-text('Add to cart')",
                                    "button:has-text('Add to cart')",
                                    "span.a-button-text:has-text('Add to cart')",
                                    "input[value='Add to cart']",
                                    ".a-button-input[aria-labelledby*='cart']",
                                    "[data-component-type='s-search-result'] button",
                                ]
                                
                                clicked = False
                                for sel in cart_btn_selectors:
                                    try:
                                        print(f"[EXECUTOR] Trying: {sel}")
                                        buttons = page.query_selector_all(sel)
                                        if buttons and len(buttons) > 0:
                                            buttons[0].click()  # Click first Add to cart button
                                            clicked = True
                                            logs.append(f"[OK] Clicked Add to cart on search results")
                                            print("[EXECUTOR] Clicked Add to cart!")
                                            break
                                    except Exception as e:
                                        print(f"[EXECUTOR] Failed: {str(e)[:30]}")
                                        continue
                                
                                if not clicked:
                                    # Try finding the button by text content
                                    try:
                                        page.click("text='Add to cart'", timeout=5000)
                                        clicked = True
                                        logs.append("[OK] Clicked 'Add to cart' by text")
                                    except:
                                        pass
                                
                                if not clicked:
                                    # Last resort: look for any button with cart in aria-label
                                    try:
                                        page.click("[aria-label*='cart'], [aria-label*='Cart']", timeout=5000)
                                        clicked = True
                                        logs.append("[OK] Clicked cart button by aria-label")
                                    except:
                                        pass
                                
                                if not clicked:
                                    raise Exception("Could not find Add to cart button on search results")
                            
                            else:
                                # On product detail page
                                logs.append("[INFO] On product page - clicking Add to cart button")
                                print("[EXECUTOR] On product page, looking for Add to cart button...")
                                
                                cart_selectors = [
                                    "#add-to-cart-button",
                                    "input#add-to-cart-button",
                                    "#buy-now-button",
                                    "input[name='submit.add-to-cart']",
                                    "#submit.add-to-cart",
                                ]
                                
                                clicked = False
                                for sel in cart_selectors:
                                    try:
                                        print(f"[EXECUTOR] Trying cart button: {sel}")
                                        page.wait_for_selector(sel, timeout=5000, state="visible")
                                        page.click(sel)
                                        clicked = True
                                        logs.append(f"[OK] Clicked: {sel}")
                                        print(f"[EXECUTOR] Added to cart!")
                                        break
                                    except:
                                        continue
                                
                                if not clicked:
                                    raise Exception("Could not find Add to cart button on product page")
                            
                            time.sleep(3)
                            
                            # Screenshot
                            ss_path = f"tests/screenshots/cart_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] {ss_path}")
                        
                        else:
                            page.click("button:has-text('Add to Cart'), .add-to-cart", timeout=timeout)
                            logs.append("[OK] Added to cart")
                        
                        logs.append("[OK] Item added to cart")

                    # ==================== TYPE ====================
                    elif action_type == "type":
                        field = act.get("field", "input")
                        value = act.get("value", "")
                        
                        selectors = [s.strip() for s in field.split(',')]
                        filled = False
                        
                        for sel in selectors:
                            try:
                                page.fill(sel, value, timeout=5000)
                                logs.append(f"[OK] Typed '{value}'")
                                filled = True
                                break
                            except:
                                continue
                        
                        if not filled:
                            raise Exception(f"Could not find input field")

                    # ==================== GET DIRECTIONS (Google Maps) ====================
                    elif action_type == "get_directions":
                        destination = act.get("destination", "")
                        logs.append(f"[INFO] Getting directions to: {destination}")
                        print(f"[EXECUTOR] Getting directions to: {destination}")
                        
                        # If not already on Google Maps, navigate there
                        if "google.com/maps" not in page.url and "maps.google" not in page.url:
                            logs.append("[INFO] Navigating to Google Maps...")
                            page.goto("https://www.google.com/maps", wait_until="domcontentloaded")
                            current_site = "google_maps"
                            time.sleep(3)
                        
                        # Accept cookies if prompted
                        try:
                            page.click("button:has-text('Accept all'), button:has-text('Accept')", timeout=3000)
                            logs.append("[OK] Accepted cookies")
                            time.sleep(1)
                        except:
                            pass
                        
                        # Search for the destination first
                        logs.append(f"[INFO] Searching for: {destination}")
                        print(f"[EXECUTOR] Searching for destination...")
                        
                        search_selectors = [
                            "#searchboxinput",
                            "input[name='q']",
                            "input[aria-label='Search Google Maps']",
                            "input[placeholder*='Search']"
                        ]
                        
                        search_filled = False
                        for sel in search_selectors:
                            try:
                                page.wait_for_selector(sel, timeout=5000)
                                page.click(sel)
                                page.fill(sel, destination)
                                search_filled = True
                                logs.append(f"[OK] Typed destination: {destination}")
                                print(f"[EXECUTOR] Filled: {destination}")
                                break
                            except Exception as e:
                                print(f"[EXECUTOR] Search selector failed: {sel} - {str(e)[:30]}")
                                continue
                        
                        if not search_filled:
                            raise Exception("Could not find Maps search box")
                        
                        # Press Enter to search
                        page.keyboard.press("Enter")
                        logs.append("[OK] Pressed Enter to search")
                        time.sleep(4)
                        
                        # Take screenshot of location
                        ss_path = f"tests/screenshots/maps_location_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path)
                        screenshots.append(ss_path)
                        logs.append(f"[SCREENSHOT] Location: {ss_path}")
                        
                        # Click on Directions button
                        logs.append("[INFO] Looking for Directions button...")
                        print("[EXECUTOR] Looking for Directions button...")
                        
                        directions_selectors = [
                            "button[data-value='Directions']",
                            "button[aria-label*='Directions']",
                            "button:has-text('Directions')",
                            "a[data-value='Directions']",
                            "[data-tooltip='Directions']",
                            "img[alt='Directions']"
                        ]
                        
                        clicked_directions = False
                        for sel in directions_selectors:
                            try:
                                print(f"[EXECUTOR] Trying: {sel}")
                                page.click(sel, timeout=5000)
                                clicked_directions = True
                                logs.append("[OK] Clicked Directions button")
                                print("[EXECUTOR] Clicked Directions!")
                                break
                            except Exception as e:
                                print(f"[EXECUTOR] Failed: {str(e)[:30]}")
                                continue
                        
                        if not clicked_directions:
                            # Try clicking by aria-label containing "Direction"
                            try:
                                page.click("[aria-label*='irection']", timeout=3000)
                                clicked_directions = True
                                logs.append("[OK] Clicked Directions (aria-label)")
                            except:
                                pass
                        
                        if not clicked_directions:
                            logs.append("[WARNING] Could not find Directions button, trying alternate method")
                            # Try direct URL with directions
                            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}"
                            page.goto(maps_url, wait_until="domcontentloaded")
                            logs.append("[OK] Navigated to directions URL directly")
                        
                        time.sleep(3)
                        
                        # The "From" field should now be visible - use current location or enter starting point
                        logs.append("[INFO] Setting starting point...")
                        
                        # Try to click "Your location" or enter a starting point
                        try:
                            # Look for the origin/from input field
                            from_selectors = [
                                "input[aria-label*='Choose starting point']",
                                "input[aria-label*='Starting point']",
                                "input[placeholder*='Choose starting point']",
                                "div[data-placeholder*='starting point'] input"
                            ]
                            
                            for sel in from_selectors:
                                try:
                                    page.click(sel, timeout=3000)
                                    page.fill(sel, "My location")
                                    page.keyboard.press("Enter")
                                    logs.append("[OK] Set starting point to: My location")
                                    break
                                except:
                                    continue
                        except:
                            logs.append("[INFO] Using default starting point")
                        
                        time.sleep(4)
                        
                        # Take screenshot of directions
                        ss_path = f"tests/screenshots/maps_directions_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path)
                        screenshots.append(ss_path)
                        logs.append(f"[SCREENSHOT] Directions: {ss_path}")
                        
                        # Try to click "Start" button to begin navigation
                        logs.append("[INFO] Looking for Start/Navigate button...")
                        
                        start_selectors = [
                            "button:has-text('Start')",
                            "button[aria-label*='Start']",
                            "button:has-text('Navigate')",
                            "div[role='button']:has-text('Start')"
                        ]
                        
                        for sel in start_selectors:
                            try:
                                page.click(sel, timeout=3000)
                                logs.append("[OK] Clicked Start navigation")
                                break
                            except:
                                continue
                        
                        time.sleep(3)
                        
                        # Final screenshot
                        ss_path = f"tests/screenshots/maps_navigation_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path)
                        screenshots.append(ss_path)
                        logs.append(f"[SCREENSHOT] Navigation: {ss_path}")
                        logs.append("[OK] Directions completed")

                    # ==================== CLICK ====================
                    elif action_type == "click":
                        selector = act.get("value", "button")
                        selectors = [s.strip() for s in selector.split(',')]
                        
                        clicked = False
                        for sel in selectors:
                            try:
                                page.click(sel, timeout=5000)
                                logs.append(f"[OK] Clicked: {sel[:40]}")
                                clicked = True
                                break
                            except:
                                continue
                        
                        if not clicked:
                            raise Exception(f"Could not click: {selector[:50]}")
                        
                        time.sleep(1)

                    # ==================== LOGIN ====================
                    elif action_type == "login":
                        email = act.get("email", "")
                        password = act.get("password", "")
                        
                        logs.append(f"[INFO] Logging in as: {email}")
                        print(f"[EXECUTOR] Logging in as: {email}")
                        
                        if current_site == "instagram" or "instagram" in page.url.lower():
                            # Instagram specific login
                            logs.append("[INFO] Using Instagram login flow")
                            print("[EXECUTOR] Instagram login flow...")
                            
                            time.sleep(2)
                            
                            # Handle cookie popup if present
                            try:
                                page.click("button:has-text('Allow'), button:has-text('Accept'), button:has-text('Only allow essential cookies')", timeout=3000)
                                logs.append("[OK] Accepted cookies")
                                time.sleep(1)
                            except:
                                pass
                            
                            # Username/Email field
                            username_selectors = [
                                "input[name='username']",
                                "input[aria-label='Phone number, username, or email']",
                                "input[aria-label*='username']",
                                "input[aria-label*='Phone number']",
                                "input[type='text']:first-of-type"
                            ]
                            
                            filled_user = False
                            for sel in username_selectors:
                                try:
                                    page.wait_for_selector(sel, timeout=5000)
                                    page.click(sel)
                                    page.fill(sel, "")  # Clear first
                                    page.fill(sel, email)
                                    filled_user = True
                                    logs.append(f"[OK] Entered username: {email}")
                                    print(f"[EXECUTOR] Filled username with: {sel}")
                                    break
                                except Exception as e:
                                    print(f"[EXECUTOR] Username selector failed: {sel} - {str(e)[:30]}")
                                    continue
                            
                            if not filled_user:
                                raise Exception("Could not find username field")
                            
                            time.sleep(0.5)
                            
                            # Password field
                            password_selectors = [
                                "input[name='password']",
                                "input[aria-label='Password']",
                                "input[type='password']"
                            ]
                            
                            filled_pass = False
                            for sel in password_selectors:
                                try:
                                    page.click(sel)
                                    page.fill(sel, "")  # Clear first
                                    page.fill(sel, password)
                                    filled_pass = True
                                    logs.append("[OK] Entered password")
                                    print("[EXECUTOR] Filled password")
                                    break
                                except Exception as e:
                                    print(f"[EXECUTOR] Password selector failed: {sel} - {str(e)[:30]}")
                                    continue
                            
                            if not filled_pass:
                                raise Exception("Could not find password field")
                            
                            time.sleep(1)
                            
                            # Click login button - Instagram specific selectors
                            login_selectors = [
                                "button[type='submit']",
                                "button:has-text('Log in')",
                                "button:has-text('Log In')",
                                "div[role='button']:has-text('Log in')",
                                "button._acan._acap._acas._aj1-",  # Instagram's actual button class
                                "button:not([type='button'])"  # Submit button that's not type=button
                            ]
                            
                            clicked = False
                            for sel in login_selectors:
                                try:
                                    print(f"[EXECUTOR] Trying login button: {sel}")
                                    page.wait_for_selector(sel, timeout=3000)
                                    page.click(sel)
                                    clicked = True
                                    logs.append(f"[OK] Clicked login button: {sel[:30]}")
                                    print("[EXECUTOR] Clicked login button!")
                                    break
                                except Exception as e:
                                    print(f"[EXECUTOR] Login button failed: {str(e)[:30]}")
                                    continue
                            
                            if not clicked:
                                # Try pressing Enter as last resort
                                print("[EXECUTOR] Trying Enter key...")
                                page.keyboard.press("Enter")
                                logs.append("[OK] Pressed Enter to login")
                            
                            # Wait for login to complete
                            logs.append("[WAIT] Waiting for login to complete...")
                            time.sleep(6)
                            
                            # Check if login was successful
                            current_url = page.url
                            print(f"[EXECUTOR] Current URL after login: {current_url}")
                            
                            if "challenge" in current_url:
                                logs.append("[WARNING] Security challenge detected")
                            elif "accounts/onetap" in current_url or "/accounts/" not in current_url:
                                logs.append("[OK] Login appears successful")
                            
                            # Handle "Save login info" popup if it appears
                            try:
                                page.click("button:has-text('Not Now'), button:has-text('Not now'), div:has-text('Not Now')", timeout=3000)
                                logs.append("[OK] Dismissed 'Save login' popup")
                                time.sleep(1)
                            except:
                                pass
                            
                            # Handle notifications popup if it appears
                            try:
                                page.click("button:has-text('Not Now'), button:has-text('Not now')", timeout=3000)
                                logs.append("[OK] Dismissed notifications popup")
                                time.sleep(1)
                            except:
                                pass
                            
                            # Take screenshot
                            ss_path = f"tests/screenshots/login_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] {ss_path}")
                        
                        else:
                            # Generic login flow
                            logs.append("[INFO] Using generic login flow")
                            print("[EXECUTOR] Generic login flow...")
                            
                            time.sleep(1)
                            
                            # Fill email/username
                            email_selectors = [
                                "input[type='email']",
                                "input[name='email']",
                                "input[name='username']",
                                "input[name='user']",
                                "input[id*='email']",
                                "input[id*='user']",
                                "input[placeholder*='email']",
                                "input[placeholder*='Email']",
                                "input[placeholder*='username']",
                                "input[type='text']"
                            ]
                            
                            filled = False
                            for sel in email_selectors:
                                try:
                                    page.fill(sel, email, timeout=3000)
                                    logs.append(f"[OK] Entered email/username")
                                    filled = True
                                    break
                                except:
                                    continue
                            
                            if not filled:
                                raise Exception("Could not find email/username field")
                            
                            time.sleep(0.5)
                            
                            # Fill password
                            try:
                                page.fill("input[type='password']", password, timeout=5000)
                                logs.append("[OK] Entered password")
                            except:
                                raise Exception("Could not find password field")
                            
                            time.sleep(0.5)
                            
                            # Click login/submit button
                            login_btn_selectors = [
                                "button[type='submit']",
                                "input[type='submit']",
                                "button:has-text('Log in')",
                                "button:has-text('Login')",
                                "button:has-text('Sign in')",
                                "button:has-text('Sign In')",
                                "a:has-text('Log in')",
                                "#login-button",
                                ".login-btn"
                            ]
                            
                            clicked = False
                            for sel in login_btn_selectors:
                                try:
                                    page.click(sel, timeout=3000)
                                    clicked = True
                                    logs.append("[OK] Clicked login button")
                                    break
                                except:
                                    continue
                            
                            if not clicked:
                                page.keyboard.press("Enter")
                                logs.append("[OK] Pressed Enter to submit")
                            
                            time.sleep(4)
                            
                            # Screenshot
                            ss_path = f"tests/screenshots/login_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] {ss_path}")
                        
                        logs.append("[OK] Login completed")

                    # ==================== LOGOUT ====================
                    elif action_type == "logout":
                        logs.append("[INFO] Logging out...")
                        print("[EXECUTOR] Logging out...")
                        
                        if current_site == "instagram" or "instagram" in page.url.lower():
                            # Instagram logout
                            logs.append("[INFO] Using Instagram logout flow")
                            
                            try:
                                # Click on profile or more menu
                                more_selectors = [
                                    "svg[aria-label='Settings']",
                                    "span:has-text('More')",
                                    "[aria-label='More']",
                                    "div:has-text('More'):last-child"
                                ]
                                
                                for sel in more_selectors:
                                    try:
                                        page.click(sel, timeout=3000)
                                        logs.append("[OK] Opened menu")
                                        break
                                    except:
                                        continue
                                
                                time.sleep(1)
                                
                                # Click logout
                                page.click("text='Log out'", timeout=5000)
                                logs.append("[OK] Clicked Log out")
                                
                                time.sleep(2)
                                
                                # Confirm logout if prompted
                                try:
                                    page.click("button:has-text('Log out'), button:has-text('Log Out')", timeout=3000)
                                    logs.append("[OK] Confirmed logout")
                                except:
                                    pass
                                
                            except Exception as e:
                                logs.append(f"[WARNING] Logout issue: {str(e)[:50]}")
                        
                        else:
                            # Generic logout
                            logout_selectors = [
                                "a:has-text('Log out')",
                                "a:has-text('Logout')",
                                "button:has-text('Log out')",
                                "button:has-text('Logout')",
                                "a:has-text('Sign out')",
                                "button:has-text('Sign out')",
                                "a[href*='logout']",
                                "a[href*='signout']",
                                "#logout",
                                ".logout"
                            ]
                            
                            clicked = False
                            for sel in logout_selectors:
                                try:
                                    page.click(sel, timeout=5000)
                                    clicked = True
                                    logs.append(f"[OK] Clicked logout")
                                    break
                                except:
                                    continue
                            
                            if not clicked:
                                logs.append("[WARNING] Could not find logout button")
                        
                        time.sleep(2)
                        
                        # Screenshot
                        ss_path = f"tests/screenshots/logout_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path)
                        screenshots.append(ss_path)
                        logs.append(f"[SCREENSHOT] {ss_path}")
                        logs.append("[OK] Logout completed")

                    # ==================== FILL FORM (Google Forms) ====================
                    elif action_type == "fill_form":
                        logs.append("[INFO] Filling form...")
                        print("[EXECUTOR] Filling form...")
                        
                        time.sleep(2)
                        
                        if current_site == "google_forms" or "forms.google" in page.url or "docs.google.com/forms" in page.url:
                            logs.append("[INFO] Detected Google Forms")
                            print("[EXECUTOR] Google Forms detected")
                            
                            # Google Forms uses specific structure
                            # Text inputs are inside divs with data-params attribute
                            
                            # Method 1: Fill text inputs by finding input fields
                            text_inputs = page.query_selector_all("input[type='text'], textarea")
                            print(f"[EXECUTOR] Found {len(text_inputs)} text inputs")
                            
                            # Sample data to fill
                            sample_data = [
                                "John Doe",           # Name
                                "johndoe@gmail.com",  # Gmail
                                "Great internship program! Learned a lot about technology and gained valuable experience.",  # Feedback
                                "Test Response",      # Fallback
                                "Sample Answer",      # Fallback
                            ]
                            
                            for i, inp in enumerate(text_inputs):
                                try:
                                    data_to_fill = sample_data[i] if i < len(sample_data) else f"Test Answer {i+1}"
                                    inp.click()
                                    inp.fill(data_to_fill)
                                    logs.append(f"[OK] Filled text field {i+1}: '{data_to_fill[:30]}...'")
                                    print(f"[EXECUTOR] Filled field {i+1}")
                                    time.sleep(0.3)
                                except Exception as e:
                                    print(f"[EXECUTOR] Could not fill field {i+1}: {e}")
                            
                            time.sleep(1)
                            
                            # Method 2: Try to select radio buttons (select "Mind Blowing" or last option)
                            logs.append("[INFO] Looking for radio buttons...")
                            print("[EXECUTOR] Looking for radio buttons...")
                            
                            try:
                                # Google Forms radio buttons are divs with role="radio"
                                radio_options = page.query_selector_all("div[role='radio'], div[data-value], label[role='radio']")
                                print(f"[EXECUTOR] Found {len(radio_options)} radio options")
                                
                                if radio_options and len(radio_options) > 0:
                                    # Try to find "Mind Blowing" or select the last option (usually best rating)
                                    clicked_radio = False
                                    
                                    # First try to find specific text
                                    for radio in radio_options:
                                        try:
                                            text = radio.inner_text().lower()
                                            if any(word in text for word in ['mind blowing', 'excellent', 'very good', 'best']):
                                                radio.click()
                                                logs.append(f"[OK] Selected radio: '{radio.inner_text()[:30]}'")
                                                print(f"[EXECUTOR] Clicked radio: {radio.inner_text()[:30]}")
                                                clicked_radio = True
                                                break
                                        except:
                                            continue
                                    
                                    # If not found, click the last option (usually highest rating)
                                    if not clicked_radio and len(radio_options) > 0:
                                        radio_options[-1].click()
                                        logs.append("[OK] Selected last radio option")
                                        print("[EXECUTOR] Clicked last radio option")
                                
                            except Exception as e:
                                print(f"[EXECUTOR] Radio button error: {e}")
                                logs.append(f"[WARNING] Could not select radio: {str(e)[:30]}")
                            
                            time.sleep(1)
                            
                            # Take screenshot before submit
                            ss_path = f"tests/screenshots/form_filled_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path, full_page=True)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] Form filled: {ss_path}")
                            
                            # Click submit button
                            logs.append("[INFO] Looking for Submit button...")
                            print("[EXECUTOR] Looking for Submit button...")
                            
                            submit_selectors = [
                                "div[role='button']:has-text('Submit')",
                                "span:has-text('Submit')",
                                "button:has-text('Submit')",
                                "[aria-label='Submit']",
                                "div:has-text('Submit'):last-of-type"
                            ]
                            
                            clicked_submit = False
                            for sel in submit_selectors:
                                try:
                                    print(f"[EXECUTOR] Trying submit: {sel}")
                                    page.click(sel, timeout=5000)
                                    clicked_submit = True
                                    logs.append(f"[OK] Clicked Submit button")
                                    print("[EXECUTOR] Clicked Submit!")
                                    break
                                except Exception as e:
                                    print(f"[EXECUTOR] Submit selector failed: {str(e)[:30]}")
                                    continue
                            
                            if not clicked_submit:
                                # Try finding by text content
                                try:
                                    page.click("text='Submit'", timeout=5000)
                                    clicked_submit = True
                                    logs.append("[OK] Clicked Submit (by text)")
                                except:
                                    logs.append("[WARNING] Could not find Submit button")
                            
                            time.sleep(3)
                            
                            # Screenshot after submit
                            ss_path = f"tests/screenshots/form_submitted_{uuid.uuid4().hex[:6]}.png"
                            page.screenshot(path=ss_path)
                            screenshots.append(ss_path)
                            logs.append(f"[SCREENSHOT] After submit: {ss_path}")
                            
                            # Check for success message
                            try:
                                success = page.query_selector("div:has-text('Your response has been recorded'), div:has-text('Thanks')")
                                if success:
                                    logs.append("[OK] Form submission confirmed!")
                            except:
                                pass
                        
                        else:
                            # Generic form
                            logs.append("[INFO] Using generic form fill")
                            inputs = page.query_selector_all("input[type='text'], textarea, input:not([type='hidden'])")
                            for i, inp in enumerate(inputs):
                                try:
                                    inp.fill(f"Test Value {i+1}")
                                    logs.append(f"[OK] Filled field {i+1}")
                                except:
                                    pass
                            
                            try:
                                page.click("button[type='submit'], input[type='submit']", timeout=5000)
                                logs.append("[OK] Submitted form")
                            except:
                                pass
                        
                        logs.append("[OK] Form handling completed")

                    # ==================== WAIT ====================
                    elif action_type == "wait":
                        wait_ms = act.get("value", 3000)
                        logs.append(f"[WAIT] {wait_ms}ms")
                        time.sleep(wait_ms / 1000)

                    # ==================== SCROLL ====================
                    elif action_type == "scroll":
                        direction = act.get("direction", "down")
                        if direction == "down":
                            page.evaluate("window.scrollBy(0, 500)")
                        else:
                            page.evaluate("window.scrollBy(0, -500)")
                        logs.append(f"[OK] Scrolled {direction}")
                        time.sleep(0.5)

                    # ==================== VIEW DETAILS ====================
                    elif action_type == "view_details":
                        time.sleep(1)
                        ss_path = f"tests/screenshots/details_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path, full_page=True)
                        screenshots.append(ss_path)
                        logs.append(f"[OK] Captured details")
                        logs.append(f"[SCREENSHOT] {ss_path}")

                    # ==================== SCREENSHOT ====================
                    elif action_type == "screenshot":
                        ss_path = f"tests/screenshots/manual_{uuid.uuid4().hex[:6]}.png"
                        page.screenshot(path=ss_path)
                        screenshots.append(ss_path)
                        logs.append(f"[SCREENSHOT] {ss_path}")

                    # ==================== ASSERT ====================
                    elif action_type == "assert_text":
                        text = act.get("value", "")
                        content = page.content().lower()
                        if text.lower() in content:
                            logs.append(f"[OK] Found text: '{text}'")
                        else:
                            raise Exception(f"Text not found: '{text}'")

                # Final screenshot
                final_ss = f"tests/screenshots/final_{uuid.uuid4().hex[:6]}.png"
                page.screenshot(path=final_ss)
                screenshots.append(final_ss)
                logs.append(f"[SCREENSHOT] Final: {final_ss}")
                
                if page.video:
                    video_path = page.video.path()
                
                context.close()
                browser.close()
                
                print("\n[EXECUTOR] All actions completed successfully!")
                return {"success": True, "logs": logs, "screenshots": screenshots, "video": video_path}

            except Exception as e:
                print(f"\n[EXECUTOR] ERROR: {str(e)}")
                logs.append(f"[ERROR] {str(e)}")
                
                # Error screenshot
                try:
                    err_ss = f"tests/screenshots/error_{uuid.uuid4().hex[:6]}.png"
                    page.screenshot(path=err_ss)
                    screenshots.append(err_ss)
                    logs.append(f"[SCREENSHOT] Error: {err_ss}")
                except:
                    pass
                
                if page.video:
                    video_path = page.video.path()
                
                context.close()
                browser.close()
                
                return {"success": False, "logs": logs, "screenshots": screenshots, "video": video_path}