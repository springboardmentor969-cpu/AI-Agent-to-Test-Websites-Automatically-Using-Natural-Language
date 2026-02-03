from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
from agent.groq_agent import get_steps_from_instruction
from agent.step_parser import parse_steps
from agent.playwright_executor import execute_steps
import json
import os

app = Flask(__name__)

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run-test", methods=["POST"])
def run_test():
    try:
        instruction = request.json.get("instruction", "").strip()
        if not instruction:
            return jsonify({"status": "error", "message": "Instruction is empty"}), 400

        # Step 1: Generate raw steps from instruction
        raw_steps = get_steps_from_instruction(instruction)

        # Step 2: Parse steps
        steps = parse_steps(raw_steps)

        # Step 3: Execute steps safely
        try:
            report, video = execute_steps(steps)
        except Exception as e:
            report = {"error": f"Execution failed: {str(e)}"}
            video = None

        # Step 4: Save last report
        with open("reports/last_report.json", "w") as f:
            json.dump(report, f, indent=4)

        # Step 5: Return structured JSON for frontend
        return jsonify({
            "status": "success",
            "parsed_steps": steps,
            "playwright_code": raw_steps,
            "report": report
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
