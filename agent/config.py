# agent/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration for the AI Web Testing Agent"""
    
    # API Configuration
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    GROK_API_URL = "https://api.x.ai/v1/chat/completions"
    GROK_MODEL = "grok-beta"
    
    # Timeout Configuration (in milliseconds)
    DEFAULT_TIMEOUT = 10000
    NAVIGATION_TIMEOUT = 30000
    ELEMENT_TIMEOUT = 5000
    NETWORK_IDLE_TIMEOUT = 5000
    
    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 1000  # milliseconds
    EXPONENTIAL_BACKOFF = True
    
    # Wait Strategy Configuration
    SMART_WAIT_ENABLED = True
    WAIT_FOR_ANIMATIONS = True
    WAIT_FOR_NETWORK_IDLE = True
    
    # AI Healing Configuration
    AI_HEALING_ENABLED = True
    VISUAL_HEALING_ENABLED = False  # Requires additional setup
    SELECTOR_CACHE_ENABLED = True
    MAX_HEALING_ATTEMPTS = 2
    
    # Screenshot Configuration
    SCREENSHOT_ON_ERROR = True
    SCREENSHOT_ON_SUCCESS = False
    SCREENSHOT_EACH_STEP = False
    
    # Video Recording
    VIDEO_RECORDING_ENABLED = True
    VIDEO_DIR = "tests/videos/"
    
    # Reporting Configuration
    GENERATE_HTML_REPORT = True
    GENERATE_PDF_REPORT = True
    GENERATE_JSON_REPORT = True
    INCLUDE_CONSOLE_LOGS = True
    INCLUDE_NETWORK_LOGS = False
    
    # Browser Configuration
    HEADLESS_MODE = True
    SLOW_MO = 0  # milliseconds delay between actions
    VIEWPORT_WIDTH = 1280
    VIEWPORT_HEIGHT = 720
    
    # Advanced Features
    IFRAME_SUPPORT = True
    MULTI_TAB_SUPPORT = True
    FILE_UPLOAD_SUPPORT = True
    SHADOW_DOM_SUPPORT = True
    
    # Logging
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    VERBOSE_LOGGING = False
    
    @classmethod
    def get_timeout(cls, action_type: str) -> int:
        """Get timeout for specific action type"""
        timeout_map = {
            "goto": cls.NAVIGATION_TIMEOUT,
            "click": cls.ELEMENT_TIMEOUT,
            "type": cls.ELEMENT_TIMEOUT,
            "wait": cls.DEFAULT_TIMEOUT,
            "upload": cls.NAVIGATION_TIMEOUT,
            "download": cls.NAVIGATION_TIMEOUT,
        }
        return timeout_map.get(action_type, cls.DEFAULT_TIMEOUT)
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GROK_API_KEY and cls.AI_HEALING_ENABLED:
            print("⚠️ Warning: GROK_API_KEY not set. AI healing will be disabled.")
            cls.AI_HEALING_ENABLED = False
        return True
