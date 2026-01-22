from agent.schemas import Action

class DOMValidator:
    def __init__(self, page):
        self.page = page

    def validate(self, action: Action) -> bool:
        """Validate assertions after action execution"""
        try:
            if action.type == "assert_visible":
                self.page.wait_for_selector(action.selector, state="visible", timeout=5000)
                return True
                
            elif action.type == "assert_text":
                element = self.page.locator(action.selector)
                actual_text = element.inner_text(timeout=5000)
                if action.value not in actual_text:
                    raise AssertionError(f"Text assertion failed. Expected '{action.value}' in '{actual_text}'")
                return True
                
            elif action.type == "assert_url":
                current_url = self.page.url
                if action.value not in current_url:
                    raise AssertionError(f"URL assertion failed. Expected '{action.value}' in '{current_url}'")
                return True
                
            return True
            
        except Exception as e:
            print(f"Validation failed: {e}")
            return False

