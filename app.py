from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__)

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading Smart ML Model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Python 3.14+ ke liye torch_dtype ka warning fix kiya
model = AutoModelForCausalLM.from_pretrained(model_name)

ai_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
print("Model Successfully Loaded! Server starting...")

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
        return jsonify({"reply": "Kuch toh type kijiye!"}), 400
    
    chat_history.append({"role": "user", "content": user_message})

    try:
        # Generation configuration ko clean kiya taaki naye python versions me crash na ho
        outputs = ai_pipeline(
            chat_history, 
            max_new_tokens=256, 
            do_sample=True, 
            temperature=0.7, 
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id  # explicitly token add kiya loop se bachne ke liye
        )
        
        bot_reply = outputs[0]["generated_text"][-1]["content"]
    except Exception as e:
        # Agar koi internal error aaye toh terminal me print hoga aur frontend crash nahi hoga
        print(f"Error target: {str(e)}")
        bot_reply = "I encountered an error while processing that. Please try again!"

    chat_history.append({"role": "assistant", "content": bot_reply})
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    # debug=True ko hata diya taaki Python 3.14 ka reloading loop error na kare
    app.run(debug=False, port=5000)
