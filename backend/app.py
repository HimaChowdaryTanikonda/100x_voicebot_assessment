from flask import Flask, request, jsonify
from flask_cors import CORS
from voicebot_logic import generate_answer

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    answer = generate_answer(question)
    return jsonify({"answer": answer})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
