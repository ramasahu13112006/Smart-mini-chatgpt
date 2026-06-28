from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Aapki original OpenAI API Key yahan set ho gayi hai
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")

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

    # Official OpenAI API Endpoint
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Fast and stable model
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        # Checking if response has choices
        if "choices" in response_json:
            bot_reply = response_json["choices"][0]["message"]["content"]
        else:
            # Agar OpenAI account me free credits khatam ho gaye hon toh error message handle karne ke liye
            bot_reply = "API Connected! But please check your OpenAI billing/quota dashboard."
    except Exception as e:
        bot_reply = "Error: Unable to connect to ChatGPT server right now."

    return jsonify({"reply": bot_reply})

app.debug = False

        
