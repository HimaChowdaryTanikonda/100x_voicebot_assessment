from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from voicebot_logic import get_response

app = Flask(__name__)
CORS(app)


@app.route("/api/ask", methods=["POST"])
def ask():
	data = request.get_json(force=True)
	question = data.get("question")
	if not question:
		return jsonify({"error": "missing 'question' field"}), 400

	try:
		resp_text = get_response(question)
		return jsonify({"answer": resp_text})
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
