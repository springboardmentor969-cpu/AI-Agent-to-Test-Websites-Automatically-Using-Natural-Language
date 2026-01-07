from flask import Flask, render_template, request, jsonify
from agent.lang_agent import run_agent
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/run", methods=["POST"])
def run():
    instructon=request.form.get("instruction")
    result=run_agent(instructon)
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)