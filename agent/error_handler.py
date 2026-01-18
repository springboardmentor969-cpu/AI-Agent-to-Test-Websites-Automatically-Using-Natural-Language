# agent/error_handler.py

from typing import Dict, Optional, List, Tuple
from enum import Enum

class ErrorCategory(Enum):
    """Error categories for classification"""
    TIMEOUT = "Timeout Error"
    ELEMENT_NOT_FOUND = "Element Not Found"
    NAVIGATION_ERROR = "Navigation Error"
    ASSERTION_ERROR = "Assertion Failure"
    NETWORK_ERROR = "Network Error"
    PERMISSION_ERROR = "Permission Error"
    FILE_ERROR = "File Operation Error"
    IFRAME_ERROR = "Iframe Error"
    UNKNOWN = "Unknown Error"


class ErrorHandler:
    """
    Centralized error handling with categorization, recovery strategies,
    and detailed reporting.
    """
    
    def __init__(self):
        self.error_history: List[Dict] = []
    
    def categorize_error(self, error: Exception, context: Dict = None) -> ErrorCategory:
        """Categorize error based on exception type and message"""
        error_msg = str(error).lower()
        
        if "timeout" in error_msg or "timed out" in error_msg:
            return ErrorCategory.TIMEOUT
        elif "not found" in error_msg or "no such element" in error_msg:
            return ErrorCategory.ELEMENT_NOT_FOUND
        elif "navigation" in error_msg or "net::" in error_msg:
            return ErrorCategory.NETWORK_ERROR
        elif "assertion" in error_msg or "expected" in error_msg:
            return ErrorCategory.ASSERTION_ERROR
        elif "permission" in error_msg or "denied" in error_msg:
            return ErrorCategory.PERMISSION_ERROR
        elif "file" in error_msg or "upload" in error_msg or "download" in error_msg:
            return ErrorCategory.FILE_ERROR
        elif "iframe" in error_msg or "frame" in error_msg:
            return ErrorCategory.IFRAME_ERROR
        else:
            return ErrorCategory.UNKNOWN
    
    def get_recovery_strategy(self, category: ErrorCategory, action: Dict) -> List[str]:
        """Get recovery strategies for specific error category"""
        strategies = {
            ErrorCategory.TIMEOUT: [
                "Increase timeout duration",
                "Wait for network idle before action",
                "Check if page is still loading",
                "Verify element selector is correct"
            ],
            ErrorCategory.ELEMENT_NOT_FOUND: [
                "Use AI healing to find correct selector",
                "Wait longer for element to appear",
                "Check if element is in iframe",
                "Verify page has loaded completely",
                "Try alternative selectors"
            ],
            ErrorCategory.NAVIGATION_ERROR: [
                "Check internet connection",
                "Verify URL is correct",
                "Try navigation with different wait strategy",
                "Check for redirects or popups"
            ],
            ErrorCategory.ASSERTION_ERROR: [
                "Verify expected value is correct",
                "Check if page content has changed",
                "Wait for dynamic content to load",
                "Review test logic"
            ],
            ErrorCategory.NETWORK_ERROR: [
                "Check network connectivity",
                "Verify server is accessible",
                "Try with longer timeout",
                "Check for CORS issues"
            ],
            ErrorCategory.PERMISSION_ERROR: [
                "Check browser permissions",
                "Verify file paths are accessible",
                "Run with appropriate privileges"
            ],
            ErrorCategory.FILE_ERROR: [
                "Verify file path exists",
                "Check file permissions",
                "Ensure correct file format",
                "Verify upload/download directory exists"
            ],
            ErrorCategory.IFRAME_ERROR: [
                "Use frame_locator for iframe access",
                "Wait for iframe to load",
                "Verify iframe selector is correct",
                "Check iframe permissions"
            ],
            ErrorCategory.UNKNOWN: [
                "Review error message for clues",
                "Check browser console logs",
                "Verify test environment",
                "Try with headed mode for debugging"
            ]
        }
        
        return strategies.get(category, strategies[ErrorCategory.UNKNOWN])
    
    def handle_error(self, error: Exception, action: Dict, context: Dict = None) -> Dict:
        """
        Handle error with categorization and suggestions
        
        Returns:
            Dict with error details, category, and recovery suggestions
        """
        category = self.categorize_error(error, context)
        strategies = self.get_recovery_strategy(category, action)
        
        error_details = {
            'error_message': str(error),
            'error_type': type(error).__name__,
            'category': category.value,
            'action': action,
            'context': context or {},
            'recovery_strategies': strategies,
            'timestamp': self._get_timestamp()
        }
        
        # Track error history
        self.error_history.append(error_details)
        
        return error_details
    
    def should_retry(self, error_category: ErrorCategory, retry_count: int, max_retries: int = 3) -> Tuple[bool, int]:
        """
        Determine if action should be retried and suggest wait time
        
        Returns:
            Tuple of (should_retry: bool, wait_ms: int)
        """
        if retry_count >= max_retries:
            return False, 0
        
        # Different retry strategies based on error type
        retry_config = {
            ErrorCategory.TIMEOUT: (True, 2000),  # Retry with longer wait
            ErrorCategory.ELEMENT_NOT_FOUND: (True, 1000),  # Retry with healing
            ErrorCategory.NETWORK_ERROR: (True, 3000),  # Retry after network recovery
            ErrorCategory.NAVIGATION_ERROR: (True, 2000),
            ErrorCategory.ASSERTION_ERROR: (False, 0),  # Don't retry assertions
            ErrorCategory.PERMISSION_ERROR: (False, 0),  # Can't fix with retry
            ErrorCategory.FILE_ERROR: (True, 500),
            ErrorCategory.IFRAME_ERROR: (True, 1000),
            ErrorCategory.UNKNOWN: (True, 1000)
        }
        
        should_retry, base_wait = retry_config.get(error_category, (True, 1000))
        
        # Exponential backoff
        wait_time = base_wait * (2 ** retry_count)
        
        return should_retry, min(wait_time, 10000)  # Cap at 10 seconds
    
    def format_error_report(self, error_details: Dict) -> str:
        """Format error details into readable report"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                     ERROR REPORT                             ║
╠══════════════════════════════════════════════════════════════╣
║ Category: {error_details['category']}
║ Type: {error_details['error_type']}
║ Message: {error_details['error_message'][:60]}
║ Action: {error_details['action'].get('action', 'unknown')}
╠══════════════════════════════════════════════════════════════╣
║ RECOVERY SUGGESTIONS:
"""
        
        for i, strategy in enumerate(error_details['recovery_strategies'], 1):
            report += f"║ {i}. {strategy}\n"
        
        report += "╚══════════════════════════════════════════════════════════════╝"
        
        return report
    
    def get_error_statistics(self) -> Dict:
        """Get statistics about errors encountered"""
        if not self.error_history:
            return {'total_errors': 0}
        
        total = len(self.error_history)
        categories = {}
        
        for error in self.error_history:
            category = error['category']
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_errors': total,
            'by_category': categories,
            'most_common': max(categories.items(), key=lambda x: x[1])[0] if categories else None
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def clear_history(self):
        """Clear error history"""
        self.error_history = []
