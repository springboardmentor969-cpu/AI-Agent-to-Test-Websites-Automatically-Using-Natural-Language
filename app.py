from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from agent import run_agent
import os

app = Flask(__name__)
CORS(app)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/form_page")
def form_page():
    return render_template("form_page.html")



@app.route("/screenshots/<path:filename>")
def screenshots(filename):
    return send_from_directory("screenshots", filename)



@app.route("/agent", methods=["POST"])
def agent_api():
    data = request.get_json(force=True)

    instruction = data.get("instruction", "").strip()
    target_url = data.get("target_url", "").strip()

    if not instruction:
        return jsonify({
            "status": "FAILED",
            "error": "Instruction cannot be empty"
        }), 400

    result = run_agent(instruction, target_url)
    return jsonify(result)

#

if __name__ == "__main__":
    os.makedirs("screenshots", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
