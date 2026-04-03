from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import requests
import json
import time
from profile import build_system_prompt, build_recruiter_prompt

# ============================================
# SETUP
# ============================================
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"
MAX_RETRIES = 2

SYSTEM_PROMPT = build_system_prompt()
RECRUITER_PROMPT = build_recruiter_prompt()

print("✅ Personal AI Backend started")
print(f"✅ Using model: {MODEL}")
print("✅ Error handling enabled")

# ============================================
# HELPERS
# ============================================

def call_ollama(messages, stream=False):
    """Call Ollama with retry logic"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": stream,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300,
                        "top_p": 0.9
                    }
                },
                stream=stream,
                timeout=60
            )
            if response.status_code == 200:
                return response
            print(f"⚠️ Attempt {attempt + 1} failed: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"⚠️ Attempt {attempt + 1} timed out")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Attempt {attempt + 1} connection error")

        if attempt < MAX_RETRIES - 1:
            time.sleep(1)  # Wait before retry

    return None


def build_messages(user_message, history, recruiter_mode):
    """Build message array for Ollama"""
    system = RECRUITER_PROMPT if recruiter_mode else SYSTEM_PROMPT
    messages = [{"role": "system", "content": system}]
    for item in history[-6:]:
        messages.append({
            "role": item["role"],
            "content": item["content"]
        })
    messages.append({"role": "user", "content": user_message})
    return messages


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


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        if len(user_message) > 500:
            return jsonify({"error": "Message too long (max 500 chars)"}), 400

        print(f"📩 Stream: {user_message[:60]}...")

        messages = build_messages(user_message, history, recruiter_mode)

        def generate():
            response = call_ollama(messages, stream=True)

            if response is None:
                yield f"data: {json.dumps({'error': 'AI unavailable after retries'})}\n\n"
                return

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        if "message" in chunk:
                            word = chunk["message"].get("content", "")
                            if word:
                                yield f"data: {json.dumps({'word': word})}\n\n"

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


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        if len(user_message) > 500:
            return jsonify({"error": "Message too long"}), 400

        messages = build_messages(user_message, history, recruiter_mode)
        response = call_ollama(messages, stream=False)

        if response is None:
            return jsonify({
                "error": "AI unavailable. Check Ollama is running."
            }), 503

        result = response.json()
        answer = result["message"]["content"]
        return jsonify({"answer": answer, "model": MODEL})

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
        "model": MODEL,
        "streaming": True,
        "max_retries": MAX_RETRIES
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("\n🚀 Starting Madheshwaran's Personal AI Backend...")
    print("📡 Server: http://localhost:5000")
    print("💬 Stream: http://localhost:5000/chat/stream")
    print("💬 Chat:   http://localhost:5000/chat")
    print("❤️  Health: http://localhost:5000/health\n")
    app.run(debug=True, port=5000, threaded=True)