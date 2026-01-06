from flask import Flask, request, jsonify, render_template
from agent import run_agent

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agent", methods=["POST"])
def agent_api():
    data = request.get_json()
    instruction = data.get("instruction", "")
    result = run_agent(instruction)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
