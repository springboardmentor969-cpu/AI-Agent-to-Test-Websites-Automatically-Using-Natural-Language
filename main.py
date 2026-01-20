from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from src.agent import agent
from src.playwright_executor.playwright_executor import execute_actions
from src.reporting.report_generator import generate_report
from src.langchain_agent import get_langchain_agent

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('static', 'agent.html')

@app.route('/agent')
def agent_page():
    return send_from_directory('static', 'agent.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    print(f"Serving static file: {filename}")
    return send_from_directory('tests', filename)

@app.route('/static/screenshots/<filename>')
def serve_screenshot(filename):
    return send_from_directory('tests/screenshots', filename)

@app.route('/run-playwright', methods=['POST'])
def run_playwright():
    instruction = request.json.get("instruction")

    agent_result = agent.invoke({"instruction": instruction})

    actions = agent_result["actions"]
    assertions = agent_result["assertions"]

    execution_result = execute_actions(actions, assertions)

    report = generate_report(actions, assertions, execution_result)

    return jsonify(report)

@app.route('/run-langchain', methods=['POST'])
def run_langchain():
    instruction = request.json.get("instruction")

    try:
        langchain_agent = get_langchain_agent()
        result = langchain_agent.execute_instruction(instruction)

        report = {
            "timestamp": str(datetime.now()),
            "instruction": instruction,
            "result": result
        }

        return jsonify(report)
    except Exception as e:
        return jsonify({
            "timestamp": str(datetime.now()),
            "instruction": instruction,
            "result": {
                "success": False,
                "error": str(e)
            }
        })

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)

