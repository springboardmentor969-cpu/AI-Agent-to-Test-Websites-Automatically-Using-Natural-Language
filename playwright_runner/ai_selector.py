def find_element(page, selectors, steps):
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=2000)
            steps.append(f"Selector matched: {sel}")
            return sel
        except:
            steps.append(f"Selector failed: {sel}")
    raise Exception("Element not found using self-healing selector")
