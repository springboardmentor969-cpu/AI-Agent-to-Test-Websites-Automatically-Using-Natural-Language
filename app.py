from flask import Flask, render_template, request, redirect, url_for
from agent import run_test_cycle

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        report=None,
        last_instruction=None
    )


@app.route("/run-test", methods=["POST"])
def run_test():
    instruction = request.form.get("instruction", "").strip()
    print(">>> instruction:", instruction)

    try:
        report = run_test_cycle(instruction)
    except Exception as e:
        report = f"Error running test cycle: {e}"

    return render_template(
        "dashboard.html",
        report=report,
        last_instruction=instruction
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
        threaded=True,
        use_reloader=False   
    )

