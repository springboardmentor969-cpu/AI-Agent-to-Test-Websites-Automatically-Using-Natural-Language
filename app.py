"""
AI Website Testing Agent - Main Application
Milestone 1: Week 1-2 Implementation
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from agent.langgraph_agent import create_test_agent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize the LangGraph agent
print("Initializing LangGraph agent...")
test_agent = create_test_agent()
print(" Agent initialized successfully!")


@app.route('/')
def index():
    """
    Main interface for the testing agent.
    Renders the HTML page where users can input test instructions.
    """
    return render_template('index.html')


@app.route('/test-page')
def test_page():
    """
    Static test page for running tests against.
    This is a simple HTML form that the agent can practice testing.
    """
    return send_from_directory('static', 'test_page.html')


@app.route('/api/test', methods=['POST'])
def run_test():
    """
    API endpoint to receive natural language test instructions
    and execute them using the LangGraph agent.
    
    Expected JSON body:
    {
        "instruction": "Click the submit button and verify success",
        "url": "http://localhost:5000/test-page"
    }
    
    Returns:
    {
        "success": true/false,
        "result": {...} or "error": "error message"
    }
    """
    try:
        # Parse JSON request body
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract instruction and URL
        test_instruction = data.get('instruction', '').strip()
        target_url = data.get('url', 'http://localhost:5000/test-page').strip()
        
        # Validate instruction is provided
        if not test_instruction:
            return jsonify({
                'success': False,
                'error': 'No test instruction provided'
            }), 400
        
        # Log the incoming request
        print(f"\n{'='*60}")
        print(f" Received test request:")
        print(f"   Instruction: {test_instruction}")
        print(f"   Target URL: {target_url}")
        print(f"{'='*60}\n")
        
        # Process the instruction through the LangGraph agent
        result = test_agent.invoke({
            'instruction': test_instruction,
            'url': target_url
        })
        
        # Log completion
        print(f"\n Test processing completed!")
        print(f"   Status: {result.get('status')}")
        print(f"   Parsed Actions: {len(result.get('parsed_actions', []))}")
        
        # Return successful result
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        # Log and return error
        print(f"\n Error processing test: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health')
def health():
    """
    Health check endpoint.
    Returns the status of the application and whether all components are ready.
    """
    return jsonify({
        'status': 'healthy',
        'agent_ready': test_agent is not None,
        'api_key_configured': bool(os.environ.get('ANTHROPIC_API_KEY'))
    })


@app.route('/api/examples')
def examples():
    """
    Returns example test instructions that users can try.
    """
    return jsonify({
        'examples': [
            {
                'name': 'Click Submit Button',
                'instruction': 'Click the submit button',
                'description': 'Simple click action'
            },
            {
                'name': 'Fill Form Field',
                'instruction': 'Type "testuser" into the username field',
                'description': 'Input text into a field'
            },
            {
                'name': 'Verify Element',
                'instruction': 'Verify that the form exists on the page',
                'description': 'Check element presence'
            },
            {
                'name': 'Complex Test',
                'instruction': 'Fill the username field with "john", fill email with "john@example.com", click submit, and verify success message appears',
                'description': 'Multi-step test scenario'
            }
        ]
    })


if __name__ == '__main__':
    # Print startup information
    print("\n" + "="*60)
    print(" AI Website Testing Agent - Milestone 1")
    print("="*60)
    
    # Check for API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("\n WARNING: ANTHROPIC_API_KEY not found!")
        print("Please create a .env file with your API key:")
        print("ANTHROPIC_API_KEY=your_key_here\n")
    else:
        print("\n Anthropic API key configured")
    
    # Print access URLs
    print("\n Access the application at:")
    print("   Main Interface:  http://localhost:5000")
    print("   Test Page:       http://localhost:5000/test-page")
    print("   Health Check:    http://localhost:5000/api/health")
    print("   Examples API:    http://localhost:5000/api/examples")
    print("\n" + "="*60)
    print("Press CTRL+C to stop the server\n")
    
    # Start the Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )