from flask import Flask, request, jsonify
from agents.graph import run_test

app = Flask(__name__)

@app.route("/run-test", methods=["POST"])
def run_test_api():
    data = request.json
    return jsonify(run_test(data.get("instruction", "")))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
