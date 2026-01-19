from flask import Flask, render_template, request, jsonify
import threading

from agent.langgraph_agent import build_agent
from agent.executor import execute_test
from agent.reporter import generate_report
from agent.playwright_generator import generate_playwright_code

app = Flask(__name__)

agent = build_agent()

# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# Run Test (REAL EXECUTION)
# -------------------------
@app.route("/run-test", methods=["POST"])
def run_test_api():
    print("🔥 /run-test API CALLED")

    data = request.get_json()
    if not data or "instruction" not in data:
        return jsonify({
            "status": "error",
            "message": "Instruction missing"
        }), 400

    instruction = data["instruction"]

    try:
        # 1️⃣ NLP → Parsed Steps
        agent_result = agent.invoke({
            "instruction": instruction
        })

        parsed_steps = agent_result.get("parsed_steps", [])

        # 2️⃣ Generate Playwright Code (for UI display only)
        playwright_code = generate_playwright_code(parsed_steps)

        # 3️⃣ Execute Playwright in SEPARATE THREAD
        step_results = []
        error = None

        def run_browser():
            nonlocal step_results, error
            step_results, error = execute_test(parsed_steps)

        t = threading.Thread(target=run_browser)
        t.start()
        t.join()

        # 4️⃣ Generate Report
        report = generate_report(parsed_steps, step_results, error)

        return jsonify({
            "status": "success" if not error else "failed",
            "parsed_steps": parsed_steps,
            "playwright_code": playwright_code,
            "report": report
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False   # 🔥 MOST IMPORTANT LINE
    )
