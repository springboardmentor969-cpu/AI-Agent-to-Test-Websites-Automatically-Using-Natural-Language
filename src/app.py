# ===== PATH FIX (VERY IMPORTANT) =====
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ===== IMPORTS =====
from flask import Flask, request, jsonify

from agent.nl_parser import parse_instruction
from agent.playwright_generator import generate_steps
from agent.assertion_engine import generate_assertions
from executor.runner import run_test
from report.reporter import generate_report

# ===== APP INIT =====
app = Flask(__name__)

# ===== BLANK HOME (NO 404) =====
@app.route("/")
def home():
    return "", 204   # Blank page, backend only

# ===== MAIN API (MILESTONE 3 + 4) =====
@app.route("/run", methods=["POST"])
def run():
    data = request.get_json() or {}
    instruction = data.get("instruction", "")

    # Milestone 3 logic
    intent = parse_instruction(instruction)
    steps = generate_steps(intent)
    assertions = generate_assertions()

    results = run_test(steps, assertions, headless=True)

    # Milestone 4 reporting
    report = generate_report(results)

    return jsonify(report)

# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
