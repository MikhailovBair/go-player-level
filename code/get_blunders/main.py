from flask import Flask, request, jsonify
from parse_analyzed import parse_game

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def process():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            path = 'sgf_for_analysis/current.sgf'
            file.save(path)
            worst_moves = parse_game(path)
            return jsonify(worst_moves)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)