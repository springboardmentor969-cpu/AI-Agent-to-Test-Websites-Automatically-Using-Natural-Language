from flask import Flask, request, jsonify, render_template
from langgraph_agent import langgraph_app   # <-- IMPORT THE REAL GRAPH
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/search")
def search():
    return render_template("search.html")
@app.route("/api/submit_test", methods=["POST"])
def submit_test():
    instruction = request.data.decode("utf-8")
    initial_state = {"instruction": instruction}
    # RUN THE REAL WORKFLOW
    result = langgraph_app.invoke(initial_state)
    return jsonify({
        "instruction": instruction,
        "action_plan": result.get("action_plan", {}),
        "generated_code": result.get("generated_code", []),
        "report": result.get("report", [])
    })
if __name__ == "__main__":
    app.run(debug=True, port=5000)