from logging import config
from flask import Flask, render_template, request, jsonify, send_file
import os
import asyncio
from agent.config import config
from agent.langgraph_agent import TestingAgent

app = Flask(__name__)
app.config.from_object(config)

# Ensure directories exist
config.ensure_directories()

# Initialize testing agent
try:
    config.validate()
    agent = TestingAgent({
        'groq_api_key': config.GROQ_API_KEY,  
        'ai_model': config.AI_MODEL,           
        'headless': config.HEADLESS,
        'timeout': config.TIMEOUT,
        'report_dir': config.REPORT_DIR,
        'report_format': config.REPORT_FORMAT

        
    })
except Exception as e:
    print(f"Warning: Could not initialize agent: {e}")
    agent = None
    
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/test-page')
def test_page():
    """Sample test page for demonstration"""
    return send_file('static/test_page.html')

@app.route('/api/run-test', methods=['POST'])
def run_test():
    """
    API endpoint to run a test from natural language input.
    
    Expected JSON payload:
    {
        "test_description": "natural language test case",
        "use_code_generation": false,
        "url": "optional URL override"
    }
    """
    if not agent:
        return jsonify({
            'success': False,
            'error': 'Agent not initialized. Check GROQ_API_KEY configuration.'
        }), 500
    
    try:
        data = request.get_json()
        test_description = data.get('test_description')
        use_code_generation = data.get('use_code_generation', False)
        
        if not test_description:
            return jsonify({
                'success': False,
                'error': 'test_description is required'
            }), 400
        
        # Run the test workflow
        result = agent.run_sync(test_description, use_code_generation)
        
        # Check for errors
        if result.get('error'):
            return jsonify({
                'success': False,
                'error': result['error'],
                'state': result
            }), 500
        
        # Return success response
        response_data = {
            'success': True,
            'test_name': result['parsed_test'].get('test_name'),
            'status': result['execution_result'].get('status'),
            'duration': result['execution_result'].get('duration'),
            'passed_steps': result['execution_result'].get('passed_steps'),
            'failed_steps': result['execution_result'].get('failed_steps'),
            'total_steps': result['execution_result'].get('total_steps'),
            'report_path': result.get('report_path'),
            'parsed_test': result.get('parsed_test'),
            'execution_result': result.get('execution_result')
        }
         # Add code path if available
        if result.get('code_path'):
            response_data['code_path'] = result.get('code_path')
        
        # Add generated code if available
        if result.get('generated_code'):
            response_data['generated_code'] = result.get('generated_code')
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/parse-test', methods=['POST'])
def parse_test():
    """
    API endpoint to only parse test (without execution).
    Useful for previewing what the agent understood.
    """
    if not agent:
        return jsonify({
            'success': False,
            'error': 'Agent not initialized'
        }), 500
    
    try:
        data = request.get_json()
        test_description = data.get('test_description')
        
        if not test_description:
            return jsonify({
                'success': False,
                'error': 'test_description is required'
            }), 400
        
        # Parse the test
        parsed_test = agent.parser.parse(test_description)
        summary = agent.parser.get_test_summary(parsed_test)
        
        return jsonify({
            'success': True,
            'parsed_test': parsed_test,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reports')
def list_reports():
    """List all generated reports"""
    try:
        reports = []
        report_dir = config.REPORT_DIR
        
        if os.path.exists(report_dir):
            for filename in os.listdir(report_dir):
                if filename.endswith('.html') or filename.endswith('.json'):
                    filepath = os.path.join(report_dir, filename)
                    reports.append({
                        'filename': filename,
                        'path': filepath,
                        'size': os.path.getsize(filepath),
                        'modified': os.path.getmtime(filepath)
                    })
        
        # Sort by modification time (newest first)
        reports.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/report/<path:filename>')
def get_report(filename):
    """Serve a specific report file"""
    try:
        report_path = os.path.join(config.REPORT_DIR, filename)
        
        if not os.path.exists(report_path):
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
        
        return send_file(report_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/report/<path:filename>')
def view_report(filename):
    """View report in browser"""
    return get_report(filename)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent_initialized': agent is not None,
        'config': {
            'headless': config.HEADLESS,
            'browser_type': config.BROWSER_TYPE,
            'timeout': config.TIMEOUT
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = config.DEBUG
    

    app.run(debug=debug, port=port, host='0.0.0.0')