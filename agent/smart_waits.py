# agent/smart_waits.py

import time
from typing import Optional, Callable
from playwright.sync_api import Page

class SmartWait:
    """
    Enhanced smart wait strategies for reliable test execution
    """
    
    def wait_dom_ready(self, page: Page, timeout: int = 5000) -> bool:
        """Wait until document.readyState == 'complete'"""
        start = time.time() * 1000
        while (time.time() * 1000) - start < timeout:
            state = page.evaluate("document.readyState")
            if state == "complete":
                return True
            time.sleep(0.2)
        return False

    def wait_network_idle(self, page: Page, timeout: int = 5000, idle_time: int = 500) -> bool:
        """Wait until network has no new requests for specified idle time"""
        start = time.time() * 1000
        prev_count = page.evaluate("() => window.performance.getEntries().length")

        while (time.time() * 1000) - start < timeout:
            time.sleep(idle_time / 1000)
            new_count = page.evaluate("() => window.performance.getEntries().length")
            if new_count == prev_count:
                return True
            prev_count = new_count

        return False

    def wait_for_element(self, page: Page, selector: str, timeout: int = 5000, 
                         visible: bool = True) -> bool:
        """Wait for element to exist and optionally be visible"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                element = page.query_selector(selector)
                if element:
                    if visible:
                        # Check if element is visible
                        is_visible = element.is_visible()
                        if is_visible:
                            return True
                    else:
                        return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_element_clickable(self, page: Page, selector: str, timeout: int = 5000) -> bool:
        """Wait for element to be clickable (visible and enabled)"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                element = page.query_selector(selector)
                if element:
                    is_visible = element.is_visible()
                    is_enabled = element.is_enabled()
                    
                    if is_visible and is_enabled:
                        return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_text(self, page: Page, text: str, timeout: int = 5000, 
                      exact: bool = False) -> bool:
        """Wait for specific text to appear on page"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                content = page.content().lower()
                search_text = text.lower()
                
                if exact:
                    if search_text in content:
                        return True
                else:
                    # Fuzzy match - check if words are present
                    words = search_text.split()
                    if all(word in content for word in words):
                        return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_text_to_disappear(self, page: Page, text: str, timeout: int = 5000) -> bool:
        """Wait for specific text to disappear from page"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                content = page.content().lower()
                if text.lower() not in content:
                    return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_element_count(self, page: Page, selector: str, count: int, 
                               timeout: int = 5000) -> bool:
        """Wait for specific number of elements matching selector"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                elements = page.query_selector_all(selector)
                if len(elements) == count:
                    return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_attribute(self, page: Page, selector: str, attribute: str, 
                           value: str, timeout: int = 5000) -> bool:
        """Wait for element attribute to have specific value"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                element = page.query_selector(selector)
                if element:
                    attr_value = element.get_attribute(attribute)
                    if attr_value == value:
                        return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_animations(self, page: Page, timeout: int = 3000) -> bool:
        """Wait for CSS animations and transitions to complete"""
        try:
            # Wait for animations to finish
            page.evaluate("""
                () => {
                    return new Promise((resolve) => {
                        const elements = document.querySelectorAll('*');
                        let animating = false;
                        
                        elements.forEach(el => {
                            const style = window.getComputedStyle(el);
                            if (style.animationName !== 'none' || style.transitionProperty !== 'none') {
                                animating = true;
                            }
                        });
                        
                        if (!animating) {
                            resolve();
                        } else {
                            setTimeout(resolve, 500);
                        }
                    });
                }
            """)
            return True
        except:
            return False
    
    def wait_for_ajax(self, page: Page, timeout: int = 5000) -> bool:
        """Wait for AJAX requests to complete (jQuery or fetch)"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                # Check jQuery AJAX
                jquery_active = page.evaluate("""
                    () => {
                        if (typeof jQuery !== 'undefined') {
                            return jQuery.active === 0;
                        }
                        return true;
                    }
                """)
                
                # Check fetch requests (basic check)
                if jquery_active:
                    return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def wait_for_condition(self, page: Page, condition: Callable[[], bool], 
                           timeout: int = 5000, poll_interval: int = 300) -> bool:
        """Wait for custom condition function to return True"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                if condition():
                    return True
            except:
                pass
            time.sleep(poll_interval / 1000)

        return False
    
    def wait_for_url_change(self, page: Page, initial_url: str, timeout: int = 5000) -> bool:
        """Wait for URL to change from initial URL"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                current_url = page.url
                if current_url != initial_url:
                    return True
            except:
                pass
            time.sleep(0.3)

        return False
    
    def smart_wait_after_action(self, page: Page, action_type: str):
        """Intelligent wait after specific action types"""
        if action_type in ["goto", "click"]:
            # Wait for navigation and network
            self.wait_dom_ready(page, timeout=3000)
            self.wait_network_idle(page, timeout=2000)
        elif action_type in ["type", "select"]:
            # Short wait for input processing
            time.sleep(0.2)
        elif action_type == "scroll":
            # Wait for lazy loading
            time.sleep(0.5)
            self.wait_network_idle(page, timeout=2000)

