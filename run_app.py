"""
Simple script to run the Flask application with proper setup.
"""

import os
import sys
import subprocess

def check_playwright_browsers():
    """Check if Playwright browsers are installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser_path = p.chromium.executable_path
                if browser_path and os.path.exists(browser_path):
                    print("[OK] Playwright browsers are installed")
                    return True
            except Exception:
                pass
        print("[WARNING] Playwright browsers not found")
        return False
    except ImportError:
        print("[ERROR] Playwright not installed")
        return False
    except Exception as e:
        print(f"[WARNING] Could not check browsers: {e}")
        return False

def install_browsers():
    """Install Playwright browsers."""
    print("\n[INFO] Installing Playwright browsers...")
    print("This may take a few minutes...")
    try:
        python_exe = sys.executable
        result = subprocess.run(
            [python_exe, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("[OK] Browsers installed successfully!")
            return True
        else:
            print(f"[ERROR] Installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("[ERROR] Installation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error installing browsers: {e}")
        return False

def main():
    """Main function to run the app."""
    print("="*60)
    print("AI Testing Agent - Application Launcher")
    print("="*60)
    
    # Check if browsers are installed
    browsers_installed = check_playwright_browsers()
    
    if not browsers_installed:
        response = input("\nPlaywright browsers are not installed. Install now? (y/n): ")
        if response.lower() == 'y':
            if not install_browsers():
                print("\n[WARNING] Browser installation failed. You can install manually later with:")
                print("  python -m playwright install chromium")
        else:
            print("\n[INFO] You can install browsers later with:")
            print("  python -m playwright install chromium")
    
    print("\n" + "="*60)
    print("Starting Flask application...")
    print("="*60)
    print("\nAccess the application at: http://127.0.0.1:5000")
    print("Agent page: http://127.0.0.1:5000/agent")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Import and run the app
    from app import app
    app.run(debug=True, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    main()




