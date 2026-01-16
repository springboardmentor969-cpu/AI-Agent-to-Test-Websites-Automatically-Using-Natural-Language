# agent/smart_waits.py

import time

class SmartWait:

    def wait_dom_ready(self, page, timeout=5000):
        """Wait until document.readyState == 'complete'"""
        start = time.time() * 1000
        while (time.time() * 1000) - start < timeout:
            state = page.evaluate("document.readyState")
            if state == "complete":
                return True
            time.sleep(0.2)
        return False

    def wait_network_idle(self, page, timeout=5000):
        """Wait until network has no requests for 500ms"""
        start = time.time() * 1000
        prev_count = page.evaluate("() => window.performance.getEntries().length")

        while (time.time() * 1000) - start < timeout:
            time.sleep(0.5)
            new_count = page.evaluate("() => window.performance.getEntries().length")
            if new_count == prev_count:
                return True
            prev_count = new_count

        return False

    def wait_for_element(self, page, selector, timeout=5000):
        """Try multiple times to wait for element"""
        start = time.time() * 1000

        while (time.time() * 1000) - start < timeout:
            try:
                element = page.query_selector(selector)
                if element:
                    return True
            except:
                pass
            time.sleep(0.3)

        return False
