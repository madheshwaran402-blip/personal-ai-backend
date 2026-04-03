from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import requests
import json
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
print("✅ Streaming enabled")

# ============================================
# STREAMING CHAT ROUTE
# ============================================

@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not user_message:
            return jsonify({"error": "No message"}), 400

        print(f"📩 Stream request: {user_message}")

        system = RECRUITER_PROMPT if recruiter_mode else SYSTEM_PROMPT

        # Build messages
        messages = [{"role": "system", "content": system}]
        for item in history[-6:]:
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })
        messages.append({"role": "user", "content": user_message})

        def generate():
            # Call Ollama with stream=True
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": True,   # ← KEY: stream words as they generate
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300,
                        "top_p": 0.9
                    }
                },
                stream=True,
                timeout=60
            )

            # Send each word as it arrives
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if "message" in chunk:
                            word = chunk["message"].get("content", "")
                            if word:
                                # Send as Server-Sent Event
                                yield f"data: {json.dumps({'word': word})}\n\n"

                        # Send done signal when finished
                        if chunk.get("done", False):
                            yield f"data: {json.dumps({'done': True})}\n\n"
                            break

                    except json.JSONDecodeError:
                        continue

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        print(f"❌ Stream error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================
# REGULAR CHAT ROUTE (kept as fallback)
# ============================================

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        system = RECRUITER_PROMPT if recruiter_mode else SYSTEM_PROMPT

        messages = [{"role": "system", "content": system}]
        for item in history[-6:]:
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })
        messages.append({"role": "user", "content": user_message})

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 300,
                    "top_p": 0.9
                }
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({"error": "Ollama error"}), 500

        result = response.json()
        answer = result["message"]["content"]

        return jsonify({"answer": answer, "model": MODEL})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# HEALTH
# ============================================

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
        "model": MODEL,
        "streaming": True
    })


if __name__ == "__main__":
    print("\n🚀 Starting Madheshwaran's Personal AI Backend...")
    print("📡 Server: http://localhost:5000")
    print("💬 Stream: http://localhost:5000/chat/stream")
    print("💬 Chat:   http://localhost:5000/chat")
    print("❤️  Health: http://localhost:5000/health\n")
    app.run(debug=True, port=5000, threaded=True)