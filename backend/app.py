from flask import Flask, request, jsonify
from flask_cors import CORS
from voicebot_logic import get_ai_response

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = get_ai_response(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
