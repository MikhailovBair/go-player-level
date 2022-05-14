from flask import Flask, request, jsonify
from get_prediction_for_games import get_prediction
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            path = 'sgf_for_analysis/current.sgf'
            file.save(path)
            prediction = get_prediction()
            return jsonify(prediction)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
