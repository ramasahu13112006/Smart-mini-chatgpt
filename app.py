from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Yahan apni copy ki hui Gemini API key daal 
GEMINI_API_KEY = "AQ.Ab8RN6InpGfpJO0JYyAW-wvgU-EliJ6pV63mAghK6T_j-mhR8w"

genai.configure(api_key=GEMINI_API_KEY)

# Model configuration
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Please type something!"}), 400

    try:
        # Vercel compatible direct API request
        response = model.generate_content(user_message)
        bot_reply = response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        bot_reply = "Error: Faceing some issues while fetching response. Please try again."

    return jsonify({"reply": bot_reply})

    
