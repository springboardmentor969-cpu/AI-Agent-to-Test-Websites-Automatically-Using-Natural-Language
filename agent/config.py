import os
from dotenv import load_dotenv

try:
    load_dotenv(encoding='utf-8')
except:
    print("Warning: Could not load .env file")

class config:
    """Application configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', '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')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Groq AI settings 
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')
    AI_MODEL = os.getenv('AI_MODEL', 'llama-3.3-70b-versatile')
    
    # Playwright settings
    HEADLESS = True
    BROWSER_TYPE = 'chromium'
    TIMEOUT = 30000
    
    # Report settings
    REPORT_DIR = 'reports'
    REPORT_FORMAT = 'html'
    
    # Test settings
    MAX_RETRIES = 3
    SCREENSHOT_ON_FAILURE = True
    VIDEO_RECORDING = False
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist"""
        os.makedirs(config.REPORT_DIR, exist_ok=True)
        os.makedirs('static/screenshots', exist_ok=True)
        os.makedirs('static/videos', exist_ok=True)
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY must be set in environment variables")
        return True