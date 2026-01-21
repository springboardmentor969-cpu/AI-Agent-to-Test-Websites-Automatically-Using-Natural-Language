# from .langgraph_agent import handle_instruction
# modules/__init__.py
"""
AI Web Testing Agent - Modules Package
Contains core functionality for parsing, code generation, execution, and reporting.
"""

from .Instruction_parser import Instruction_Parser
from .code_generator import PlaywrightCodeGenerator
from .test_executor import TestExecutor
from .report_generator import ReportGenerator

__all__ = [
    'InstructionParser',
    'PlaywrightCodeGenerator',
    'TestExecutor',
    'ReportGenerator'
]

# agents/__init__.py
"""
AI Web Testing Agent - Agents Package
Contains LangGraph orchestration for testing workflows.
"""

from .langgraph_agent import TestingAgent

__all__ = ['TestingAgent']

# tests/__init__.py
"""
Test suite for AI Web Testing Agent
"""

# tests/sample_tests.py
"""
Sample test cases demonstrating the AI Web Testing Agent capabilities.
Run these tests to verify your installation.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .config import config
from .langgraph_agent import TestingAgent

async def test_basic_navigation():
    """Test basic navigation functionality"""
    print("\n" + "="*60)
    print("TEST 1: Basic Navigation")
    print("="*60)
    
    test_case = """
    Go to http://localhost:5000/test-page
    Wait 2 seconds
    Verify that the page contains 'Sample Login Form'
    """
    
    agent = TestingAgent({
        'groq_api_key': config.GROQ_API_KEY,
        'ai_model': config.AI_MODEL,
        'headless': config.HEADLESS,
        'timeout': config.TIMEOUT,
        'report_dir': config.REPORT_DIR
    })
    
    result = await agent.run(test_case)
    
    print(f"Status: {result['execution_result']['status']}")
    print(f"Duration: {result['execution_result']['duration']:.2f}s")
    print(f"Passed: {result['execution_result']['passed_steps']}/{result['execution_result']['total_steps']}")
    
    if result.get('error'):
        print(f"Error: {result['error']}")
    
    return result

async def test_form_interaction():
    """Test form filling and submission"""
    print("\n" + "="*60)
    print("TEST 2: Form Interaction")
    print("="*60)
    
    test_case = """
    Navigate to http://localhost:5000/test-page
    Type 'John Doe' in the name field
    Type 'john@example.com' in the email field
    Type 'password123' in the password field
    Click the Login button
    Wait 1 second
    Verify that the success message is displayed
    """
    
    agent = TestingAgent({
        'groqai_api_key': config.GROQ_API_KEY,
        'ai_model': config.AI_MODEL,
        'headless': config.HEADLESS,
        'timeout': config.TIMEOUT,
        'report_dir': config.REPORT_DIR
    })
    
    result = await agent.run(test_case)
    
    print(f"Status: {result['execution_result']['status']}")
    print(f"Duration: {result['execution_result']['duration']:.2f}s")
    print(f"Passed: {result['execution_result']['passed_steps']}/{result['execution_result']['total_steps']}")
    
    if result.get('report_path'):
        print(f"Report: {result['report_path']}")
    
    return result

async def test_with_code_generation():
    """Test with Playwright code generation"""
    print("\n" + "="*60)
    print("TEST 3: Code Generation Mode")
    print("="*60)
    
    test_case = """
    Go to http://localhost:5000/test-page
    Fill 'test@example.com' in the email field
    Click the Login button
    """
    
    agent = TestingAgent({
        'groq_api_key': config.GROQ_API_KEY,
        'ai_model': config.AI_MODEL,
        'headless': config.HEADLESS,
        'timeout': config.TIMEOUT,
        'report_dir': config.REPORT_DIR
    })
    
    result = await agent.run(test_case, use_code_generation=True)
    
    print(f"Status: {result['execution_result']['status']}")
    
    if result.get('generated_code'):
        print("\nGenerated Code (first 500 chars):")
        print(result['generated_code'][:500] + "...")
    
    return result

async def run_all_tests():
    """Run all sample tests"""
    print("\n" + "="*60)
    print("AI WEB TESTING AGENT - SAMPLE TESTS")
    print("="*60)
    print("\nMake sure Flask app is running on http://localhost:5000")
    print("You can start it with: python app.py")
    input("\nPress Enter to continue...")
    
    results = []
    
    try:
        # Test 1: Basic Navigation
        result1 = await test_basic_navigation()
        results.append(('Basic Navigation', result1))
        
        # Test 2: Form Interaction
        result2 = await test_form_interaction()
        results.append(('Form Interaction', result2))
        
        # Test 3: Code Generation
        result3 = await test_with_code_generation()
        results.append(('Code Generation', result3))
        
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, result in results:
        status = result['execution_result']['status']
        icon = '✓' if status == 'passed' else '✗'
        print(f"{icon} {name}: {status}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    # Ensure Flask server is running
    print("Sample Tests for AI Web Testing Agent")
    print("\nPrerequisites:")
    print("1. Flask server running: python app.py")
    print("2. OPENAI_API_KEY configured in .env")
    print("\nStarting tests in 3 seconds...")
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")