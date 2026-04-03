from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from profile import build_system_prompt

# ============================================
# FLASK APP SETUP
# ============================================

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"]) # Allow React to call this server

# Ollama runs locally on this URL
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

# Build system prompt once when server starts
SYSTEM_PROMPT = build_system_prompt()

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
        # Get message from React
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"📩 Received: {user_message}")

        # Build messages for Ollama
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False  # Get full response at once
            },
            timeout=60
        )

        # Check if Ollama responded ok
        if response.status_code != 200:
            return jsonify({"error": "Ollama error"}), 500

        # Extract the answer
        result = response.json()
        answer = result["message"]["content"]

        print(f"🤖 Answer: {answer[:80]}...")

        return jsonify({
            "answer": answer,
            "model": MODEL
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot connect to Ollama. Make sure it is running with: ollama serve"
        }), 503

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        ollama_status = "running"
    except:
        ollama_status = "not running"

    return jsonify({
        "backend": "running",
        "ollama": ollama_status,
        "model": MODEL
    })


# ============================================
# START SERVER
# ============================================

if __name__ == "__main__":
    print("\n🚀 Starting Madheshwaran's Personal AI Backend...")
    print("📡 Server will run at: http://localhost:5000")
    print("💬 Chat endpoint: http://localhost:5000/chat")
    print("❤️  Health check: http://localhost:5000/health\n")
    app.run(debug=True, port=5000)