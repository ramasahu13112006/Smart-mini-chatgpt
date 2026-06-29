from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# FIX: Gsk_ ko badal kar gsk_ kar diya hai (Small 'g')
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"reply": "Invalid request format."}), 400
        
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Please type something!"}), 400

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "choices" in response_json:
            bot_reply = response_json["choices"][0]["message"]["content"]
        elif "error" in response_json:
            bot_reply = f"Groq Error: {response_json['error'].get('message')}"
        else:
            bot_reply = "API Connected, but response format is unexpected."
    except Exception as e:
        bot_reply = f"Backend error: {str(e)}"

    return jsonify({"reply": bot_reply})

app.debug = False
