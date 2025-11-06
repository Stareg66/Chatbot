from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get your OpenRouter API key from environment
OPENROUTER_API_KEY = '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'

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    model = data.get("model", "z-ai/glm-4.5-air:free")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call OpenRouter API
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
