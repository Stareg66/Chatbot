from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

CONFIG_FILE = "userconfig.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data
        except Exception:
            return {}
    return {}


@app.route("/chat", methods=["POST"])
def chat():
    config = load_config()
    api_key = config.get("api_key")
    username = config.get("username")
    model = config.get("model")
    
    # Validate configuration
    if not api_key or not username or not model:
        return jsonify({"error": "Missing API key, username, or model in configuration"}), 400

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call OpenRouter API
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Provide the information {username} requires."},
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=60,
        )

        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
