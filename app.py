from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from profile import build_system_prompt, build_recruiter_prompt

# ============================================
# SETUP
# ============================================
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

SYSTEM_PROMPT = build_system_prompt()
RECRUITER_PROMPT = build_recruiter_prompt()

print("✅ Personal AI Backend started")
print(f"✅ Using model: {MODEL}")
print("✅ System prompt loaded")

# ============================================
# ROUTES
# ============================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Madheshwaran's Personal AI Backend",
        "model": MODEL
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        # Get conversation history from React
        history = data.get("history", [])
        # Check if recruiter mode is on
        recruiter_mode = data.get("recruiterMode", False)

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"📩 Received: {user_message}")
        print(f"📚 History length: {len(history)}")
        print(f"👔 Recruiter mode: {recruiter_mode}")

        # Pick the right system prompt
        system = RECRUITER_PROMPT if recruiter_mode else SYSTEM_PROMPT

        # Build messages — system prompt + history + new message
        messages = [{"role": "system", "content": system}]

        # Add conversation history for memory
        for item in history[-6:]:  # Last 6 messages only
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,      # Creativity level 0-1
                    "num_predict": 300,      # Max tokens — keeps answers short
                    "top_p": 0.9
                }
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({"error": "Ollama error"}), 500

        result = response.json()
        answer = result["message"]["content"]

        print(f"🤖 Answer: {answer[:100]}...")

        return jsonify({
            "answer": answer,
            "model": MODEL,
            "recruiterMode": recruiter_mode
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot connect to Ollama. Run: ollama serve"
        }), 503

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    try:
        requests.get("http://localhost:11434", timeout=3)
        ollama_status = "running"
    except:
        ollama_status = "not running"

    return jsonify({
        "backend": "running",
        "ollama": ollama_status,
        "model": MODEL
    })


if __name__ == "__main__":
    print("\n🚀 Starting Madheshwaran's Personal AI Backend...")
    print("📡 Server: http://localhost:5000")
    print("💬 Chat: http://localhost:5000/chat")
    print("❤️  Health: http://localhost:5000/health\n")
    app.run(debug=True, port=5000)