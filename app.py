from flask import Flask, render_template, request, jsonify
from agent.langgraph_agent import build_agent
from agent.assertion_generator import generate_assertions

app = Flask(__name__)

agent = build_agent()

# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# Run Test
# -------------------------
@app.route("/run-test", methods=["POST"])
def run_test_api():
    data = request.get_json()

    if not data or "instruction" not in data:
        return jsonify({
            "status": "error",
            "message": "Instruction missing"
        }), 400

    instruction = data["instruction"]

    try:
        # NLP → Steps → Code
        result = agent.invoke({"instruction": instruction})

        parsed_steps = result.get("parsed_steps", [])
        playwright_code = result.get("playwright_code", "")

        # Assertions (dummy but valid)
        assertions = generate_assertions("login_success")

        return jsonify({
            "status": "success",
            "parsed_steps": parsed_steps,
            "assertions": assertions,
            "playwright_code": playwright_code
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
