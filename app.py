from flask import Flask, render_template, request, jsonify
from agent.langgraph_agent import build_agent

app = Flask(__name__)

# Build LangGraph Agent
agent = build_agent()

# Home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Run test using AI Agent
@app.route("/run-test", methods=["POST"])
def run_test():
    data = request.get_json()
    instruction = data.get("instruction")

    result = agent.invoke({
        "instruction": instruction
    })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
