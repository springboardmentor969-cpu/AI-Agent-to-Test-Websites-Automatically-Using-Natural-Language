# # from flask import Flask, render_template, request, jsonify
# # from agent.graph import app_graph

# # app = Flask(__name__)

# # @app.route("/")
# # def home():
# #     return render_template("index.html")

# # # @app.route("/run", methods=["POST"])
# # # def run():
# # #     user_input = request.json["input"]

# # #     result = app_graph.invoke({
# # #         "input": user_input
# # #     })

# # #     return jsonify(result)
# # # @app.route("/run", methods=["POST"])
# # # def run():
# # #     user_input = request.json["input"]
# # #     result = app_graph.invoke({"input": user_input})
# # #     return jsonify(result)
# # @app.route("/run", methods=["POST"])
# # def run():
# #     user_input = request.json["input"]
# #     report = app_graph.invoke({"input": user_input})
# #     return jsonify(report)


# # if __name__ == "__main__":
# #     app.run(debug=True)

# from flask import Flask, request, jsonify, render_template
# from agent.graph import app_graph

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/run", methods=["POST"])
# def run():
#     return jsonify(app_graph.invoke({"input": request.json["input"]}))

# from flask import send_file
# import os

# @app.route("/download/<path:filename>")
# def download(filename):
#     return send_file(filename, as_attachment=True)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template, send_file
from agent.graph import app_graph

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    result = app_graph.invoke(data)
    print("SAVING HISTORY:", result)   # debug
    return jsonify(result)


from reporting.history_store import get_history

@app.route("/history")
def history():
    return jsonify(get_history())


@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

app.run(debug=True)
