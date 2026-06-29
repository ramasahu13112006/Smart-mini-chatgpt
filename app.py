from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Aapki original Groq API Key yahan set ho gayi hai
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "Gsk_hLDgDmutK4V1OG7NmH8LWGdyb3FYaiuv9z8TqZMmI9sZ3ljEQNlo")

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

    # Fast and Free Groq Endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",  # Superfast model
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "choices" in response_json:
            bot_reply = response_json["choices"][0]["message"]["content"]
        else:
            bot_reply = "API Connected, but server is busy. Try again!"
    except Exception as e:
        bot_reply = "Backend error: Unable to connect to the free AI engine."

    return jsonify({"reply": bot_reply})

app.debug = False
