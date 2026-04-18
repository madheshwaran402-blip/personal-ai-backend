import os
import json
import requests
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
from profile import build_system_prompt, PROFILE

load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "https://madheshwaran-ai.vercel.app"
])

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2")
MAX_HISTORY = 6


def get_recent_history(history: list) -> list:
    return history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history


def check_ollama() -> bool:
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return res.status_code == 200
    except Exception:
        return False


# ============================================
# ROUTES
# ============================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "model": MODEL,
        "assistant": "Madheshwaran Personal AI",
        "version": "2.0"
    })


@app.route("/health", methods=["GET"])
def health():
    ollama_ok = check_ollama()
    return jsonify({
        "backend": "running",
        "ollama": "running" if ollama_ok else "offline",
        "model": MODEL,
        "streaming": True
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not message:
            return jsonify({"error": "No message provided"}), 400

        system_prompt = build_system_prompt(recruiter_mode)
        recent_history = get_recent_history(history)

        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt}
                ] + messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 300,
                    "top_p": 0.9
                }
            },
            timeout=120
        )

        data_response = response.json()
        answer = data_response.get("message", {}).get("content", "")

        return jsonify({
            "answer": answer,
            "model": MODEL,
            "recruiterMode": recruiter_mode
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Ollama is not running. Start with: ollama serve"
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not message:
            return jsonify({"error": "No message provided"}), 400

        system_prompt = build_system_prompt(recruiter_mode)
        recent_history = get_recent_history(history)

        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        def generate():
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={
                        "model": MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt}
                        ] + messages,
                        "stream": True,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 300,
                            "top_p": 0.9
                        }
                    },
                    stream=True,
                    timeout=120
                )

                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode("utf-8"))
                            word = chunk.get("message", {}).get("content", "")
                            if word:
                                yield f"data: {json.dumps({'word': word})}\n\n"
                            if chunk.get("done"):
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                        except json.JSONDecodeError:
                            continue

            except requests.exceptions.ConnectionError:
                yield f"data: {json.dumps({'error': 'Ollama not running. Run: ollama serve'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive"
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Starting Madheshwaran Personal AI Backend")
    print(f"Model: {MODEL}")
    print(f"Ollama URL: {OLLAMA_URL}")
    app.run(debug=True, host="0.0.0.0", port=5000)