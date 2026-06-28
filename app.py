from flask import Flask, render_template, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

# Chat history to maintain context
chat_history = [
    {"role": "system", "content": "You are a helpful, smart, and accurate AI assistant. Answer the user's questions clearly."}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Please type something!"}), 400

    chat_history.append({"role": "user", "content": user_message})

    try:
        # Using free external AI model API instead of local heavy files
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = "Error: Unable to connect to the AI model on Vercel."

    chat_history.append({"role": "assistant", "content": bot_reply})
    return jsonify({"reply": bot_reply})

# Vercel serverless requirements ke liye handler add kiya
app.debug = False
