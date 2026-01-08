from flask import Flask, render_template, request, jsonify
from agent.langgraph import handle_instruction

app = Flask(__name__)

@app.route("/")
def home():
    """
    Serves the static HTML test page.
    """
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    """
    API endpoint to receive user instruction
    and pass it to the agent.
    """
    data = request.get_json()

    if not data or "instruction" not in data:
        return jsonify({
            "status": "error",
            "message": "No instruction provided"
        }), 400

    instruction = data.get("instruction")

    # Call agent logic
    result = handle_instruction(instruction)

    return jsonify({
        "status": "success",
        "instruction": instruction,
        "agent_response": result
    })


if __name__ == "__main__":
    app.run(debug=True)
