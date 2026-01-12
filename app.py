from flask import Flask, render_template, request, jsonify
from agent.lang_agent import run_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sample_form.html")
def sample_form():
    return render_template("sample_form.html")

@app.route("/run", methods=["POST"])
def run():
    instruction = request.form.get("instruction")
    result = run_agent(instruction)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
