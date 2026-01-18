# agent/advanced_actions.py

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional, Dict, Any, List
import time
import os

class IframeHandler:
    """Handle iframe interactions"""
    
    @staticmethod
    def find_and_switch_to_iframe(page: Page, iframe_selector: Optional[str] = None) -> Optional[Any]:
        """Find and switch to iframe context"""
        try:
            if iframe_selector:
                frame = page.frame_locator(iframe_selector)
                return frame
            else:
                # Try to find any iframe
                frames = page.frames
                if len(frames) > 1:
                    return frames[1]  # First non-main frame
            return None
        except Exception as e:
            print(f"Iframe switch error: {e}")
            return None
    
    @staticmethod
    def execute_in_iframe(page: Page, iframe_selector: str, action_callback):
        """Execute action within iframe context"""
        try:
            frame_locator = page.frame_locator(iframe_selector)
            return action_callback(frame_locator)
        except Exception as e:
            print(f"Iframe execution error: {e}")
            return None


class FileHandler:
    """Handle file uploads and downloads"""
    
    @staticmethod
    def upload_file(page: Page, selector: str, file_path: str, timeout: int = 5000):
        """Upload file to input element"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Wait for file input
            page.wait_for_selector(selector, timeout=timeout)
            
            # Set files
            page.set_input_files(selector, file_path)
            return True
        except Exception as e:
            print(f"File upload error: {e}")
            return False
    
    @staticmethod
    def download_file(page: Page, trigger_selector: str, timeout: int = 30000) -> Optional[str]:
        """Trigger download and wait for completion"""
        try:
            with page.expect_download(timeout=timeout) as download_info:
                page.click(trigger_selector)
            
            download = download_info.value
            download_path = f"tests/downloads/{download.suggested_filename}"
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            download.save_as(download_path)
            
            return download_path
        except Exception as e:
            print(f"File download error: {e}")
            return None


class TabManager:
    """Manage multiple tabs and windows"""
    
    def __init__(self):
        self.tabs: Dict[str, Page] = {}
        self.current_tab_id: Optional[str] = None
    
    def open_new_tab(self, context, url: Optional[str] = None, tab_id: Optional[str] = None) -> str:
        """Open new tab and optionally navigate to URL"""
        new_page = context.new_page()
        
        if not tab_id:
            tab_id = f"tab_{len(self.tabs) + 1}"
        
        self.tabs[tab_id] = new_page
        self.current_tab_id = tab_id
        
        if url:
            new_page.goto(url)
        
        return tab_id
    
    def switch_to_tab(self, tab_id: str) -> Optional[Page]:
        """Switch to specific tab"""
        if tab_id in self.tabs:
            self.current_tab_id = tab_id
            page = self.tabs[tab_id]
            page.bring_to_front()
            return page
        return None
    
    def close_tab(self, tab_id: str):
        """Close specific tab"""
        if tab_id in self.tabs:
            self.tabs[tab_id].close()
            del self.tabs[tab_id]
            
            if self.current_tab_id == tab_id:
                self.current_tab_id = list(self.tabs.keys())[0] if self.tabs else None
    
    def get_current_tab(self) -> Optional[Page]:
        """Get current active tab"""
        if self.current_tab_id and self.current_tab_id in self.tabs:
            return self.tabs[self.current_tab_id]
        return None


class DataExtractor:
    """Extract data from web pages"""
    
    @staticmethod
    def extract_text(page: Page, selector: str) -> Optional[str]:
        """Extract text from element"""
        try:
            element = page.query_selector(selector)
            if element:
                return element.inner_text()
            return None
        except Exception as e:
            print(f"Text extraction error: {e}")
            return None
    
    @staticmethod
    def extract_attribute(page: Page, selector: str, attribute: str) -> Optional[str]:
        """Extract attribute value from element"""
        try:
            element = page.query_selector(selector)
            if element:
                return element.get_attribute(attribute)
            return None
        except Exception as e:
            print(f"Attribute extraction error: {e}")
            return None
    
    @staticmethod
    def extract_multiple(page: Page, selector: str, attribute: Optional[str] = None) -> List[str]:
        """Extract data from multiple elements"""
        try:
            elements = page.query_selector_all(selector)
            results = []
            
            for element in elements:
                if attribute:
                    value = element.get_attribute(attribute)
                else:
                    value = element.inner_text()
                
                if value:
                    results.append(value)
            
            return results
        except Exception as e:
            print(f"Multiple extraction error: {e}")
            return []
    
    @staticmethod
    def extract_table(page: Page, table_selector: str) -> List[Dict[str, str]]:
        """Extract data from HTML table"""
        try:
            # Get headers
            headers = []
            header_elements = page.query_selector_all(f"{table_selector} th")
            for header in header_elements:
                headers.append(header.inner_text().strip())
            
            # Get rows
            rows = []
            row_elements = page.query_selector_all(f"{table_selector} tbody tr")
            
            for row_element in row_elements:
                cells = row_element.query_selector_all("td")
                row_data = {}
                
                for i, cell in enumerate(cells):
                    header = headers[i] if i < len(headers) else f"column_{i}"
                    row_data[header] = cell.inner_text().strip()
                
                rows.append(row_data)
            
            return rows
        except Exception as e:
            print(f"Table extraction error: {e}")
            return []


class ScrollManager:
    """Handle scrolling strategies"""
    
    @staticmethod
    def scroll_to_element(page: Page, selector: str):
        """Scroll element into view"""
        try:
            element = page.query_selector(selector)
            if element:
                element.scroll_into_view_if_needed()
                return True
            return False
        except Exception as e:
            print(f"Scroll to element error: {e}")
            return False
    
    @staticmethod
    def scroll_by_pixels(page: Page, x: int = 0, y: int = 0):
        """Scroll by specific pixel amount"""
        try:
            page.evaluate(f"window.scrollBy({x}, {y})")
            return True
        except Exception as e:
            print(f"Scroll by pixels error: {e}")
            return False
    
    @staticmethod
    def scroll_to_bottom(page: Page, smooth: bool = True):
        """Scroll to bottom of page"""
        try:
            if smooth:
                # Smooth scroll with multiple steps
                total_height = page.evaluate("document.body.scrollHeight")
                current_position = 0
                step = 300
                
                while current_position < total_height:
                    page.evaluate(f"window.scrollTo(0, {current_position})")
                    time.sleep(0.1)
                    current_position += step
                    # Update total height in case of lazy loading
                    total_height = page.evaluate("document.body.scrollHeight")
            else:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            
            return True
        except Exception as e:
            print(f"Scroll to bottom error: {e}")
            return False
    
    @staticmethod
    def scroll_to_top(page: Page):
        """Scroll to top of page"""
        try:
            page.evaluate("window.scrollTo(0, 0)")
            return True
        except Exception as e:
            print(f"Scroll to top error: {e}")
            return False


class InteractionHandler:
    """Handle complex interactions"""
    
    @staticmethod
    def hover(page: Page, selector: str, timeout: int = 5000):
        """Hover over element"""
        try:
            page.hover(selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"Hover error: {e}")
            return False
    
    @staticmethod
    def drag_and_drop(page: Page, source_selector: str, target_selector: str, timeout: int = 5000):
        """Drag element from source to target"""
        try:
            page.drag_and_drop(source_selector, target_selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"Drag and drop error: {e}")
            return False
    
    @staticmethod
    def select_option(page: Page, selector: str, value: str = None, label: str = None, timeout: int = 5000):
        """Select option from dropdown"""
        try:
            if value:
                page.select_option(selector, value=value, timeout=timeout)
            elif label:
                page.select_option(selector, label=label, timeout=timeout)
            return True
        except Exception as e:
            print(f"Select option error: {e}")
            return False
    
    @staticmethod
    def press_key(page: Page, key: str, selector: Optional[str] = None):
        """Press keyboard key"""
        try:
            if selector:
                page.focus(selector)
            page.keyboard.press(key)
            return True
        except Exception as e:
            print(f"Key press error: {e}")
            return False
    
    @staticmethod
    def type_with_delay(page: Page, selector: str, text: str, delay: int = 100):
        """Type text with delay between characters (human-like)"""
        try:
            page.click(selector)
            page.keyboard.type(text, delay=delay)
            return True
        except Exception as e:
            print(f"Type with delay error: {e}")
            return False
