"""
Quick test to verify headed mode works
"""
from dotenv import load_dotenv
load_dotenv()

from agent.playwright_executor import PlaywrightExecutor
import time

print("Testing headed mode...")
print("A browser window should open now!\n")

executor = PlaywrightExecutor()

try:
    print("1. Navigating to test page...")
    from agent.schemas import Action
    
    nav_action = Action(type="navigate", value="http://127.0.0.1:5000/static/test_page.html")
    result = executor.execute(nav_action)
    print(f"   Result: {'SUCCESS' if result.success else 'FAILED'}")
    
    print("\n2. Waiting 3 seconds so you can see the browser...")
    time.sleep(3)
    
    print("\n3. Taking screenshot...")
    screenshot_action = Action(type="screenshot", value="test")
    result = executor.execute(screenshot_action)
    print(f"   Result: {'SUCCESS' if result.success else 'FAILED'}")
    
    print("\n4. Closing browser...")
    
finally:
    executor.close()

print("\n✓ Test complete! Did you see the browser window?")
