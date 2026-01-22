from flask import Flask, render_template, request, jsonify, send_from_directory
from agent.workflow import create_workflow
import os
import glob

app = Flask(__name__)
workflow = create_workflow()

@app.route("/screenshots/<path:filename>")
def serve_screenshot(filename):
    screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    return send_from_directory(screenshots_dir, filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        instruction = request.json.get("instruction")
        if not instruction:
            return jsonify({"error": "No instruction provided"}), 400
        
        result = workflow.invoke({"instruction": instruction})
        
        # Format results for JSON serialization
        formatted_results = []
        if result.get("results"):
            for r in result["results"]:
                formatted_result = {
                    "action_type": getattr(r, 'action_type', getattr(r.action, 'type', 'unknown') if hasattr(r, 'action') else 'unknown'),
                    "success": getattr(r, 'success', True),
                    "selector": getattr(r.action, 'selector', None) if hasattr(r, 'action') else None,
                    "value": getattr(r.action, 'value', None) if hasattr(r, 'action') else None,
                    "error": getattr(r, 'error', None),
                    "execution_time": getattr(r, 'execution_time_ms', None),
                    "screenshot_path": getattr(r, 'screenshot_path', None)
                }
                # Convert screenshot path to URL path if it exists
                if formatted_result['screenshot_path']:
                    rel_path = os.path.relpath(formatted_result['screenshot_path'], os.path.dirname(__file__))
                    formatted_result['screenshot_path'] = '/' + rel_path.replace('\\', '/')
                
                formatted_results.append(formatted_result)
        
        response = {
            "instruction": instruction,
            "results": formatted_results,
            "plan": str(result.get("plan", "")),
            "report": str(result.get("report", ""))
        }
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {error_details}")
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "details": error_details
        }), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

