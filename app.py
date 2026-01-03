from flask import Flask, request, jsonify, render_template
import uuid
app = Flask(__name__)
# ---- LangGraph workflow STUB ----
def langgraph_stub(nl_instruction: str):
    return {
        "intent": nl_instruction,
        "steps": [
            "Open browser",
            "Navigate to login page",
            "Enter credentials",
            "Submit form",
            "Validate result"
        ]
    }
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
    nl_instruction = request.data.decode("utf-8")
    job_id = str(uuid.uuid4())
    action_plan = langgraph_stub(nl_instruction)
    return jsonify({
        "job_id": job_id,
        "action_plan": action_plan,
        "status": "created"
    })
if __name__ == "__main__":
    app.run(debug=True, port=5000)