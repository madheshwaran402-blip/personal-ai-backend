import os
import json
import requests
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
from madheshwaran_profile import build_system_prompt, PROFILE

load_dotenv()

app = Flask(__name__)

# ============================================
# CORS — allow frontend domains
# ============================================
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "https://madheshwaran-ai.vercel.app"
])

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "madheshwaran-ai")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "llama3.2")
PORT = int(os.getenv("PORT", 5000))
MAX_HISTORY = 6


def get_recent_history(history: list) -> list:
    return history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history


def check_ollama() -> bool:
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return res.status_code == 200
    except Exception:
        return False


def check_model_exists(model_name: str) -> bool:
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if res.status_code == 200:
            models = res.json().get("models", [])
            return any(
                m.get("name", "").startswith(model_name)
                for m in models
            )
        return False
    except Exception:
        return False


def get_best_model() -> str:
    if check_model_exists(MODEL):
        return MODEL
    return FALLBACK_MODEL


def chat_with_ollama(
    messages: list,
    system_prompt: str,
    model: str,
    stream: bool = False
) -> requests.Response:
    return requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt}
            ] + messages,
            "stream": stream,
            "options": {
                "temperature": 0.65,
                "top_p": 0.85,
                "top_k": 35,
                "num_predict": 250,
                "repeat_penalty": 1.15,
                "num_ctx": 4096
            }
        },
        stream=stream,
        timeout=120
    )


# ============================================
# ROUTES
# ============================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "model": MODEL,
        "assistant": "Madheshwaran Personal AI",
        "version": "2.0",
        "environment": os.getenv("FLASK_ENV", "production")
    })


@app.route("/health", methods=["GET"])
def health():
    ollama_ok = check_ollama()
    model_exists = check_model_exists(MODEL) if ollama_ok else False

    return jsonify({
        "backend": "running",
        "ollama": "running" if ollama_ok else "offline",
        "model": MODEL,
        "model_ready": model_exists,
        "fallback": FALLBACK_MODEL,
        "streaming": True
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if len(message) > 1000:
            return jsonify({"error": "Message too long"}), 400

        system_prompt = build_system_prompt(recruiter_mode)
        recent_history = get_recent_history(history)
        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        best_model = get_best_model()
        response = chat_with_ollama(
            messages,
            system_prompt,
            best_model,
            stream=False
        )

        data_response = response.json()
        answer = data_response.get("message", {}).get("content", "")

        return jsonify({
            "answer": answer,
            "model": best_model,
            "recruiterMode": recruiter_mode
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "AI is starting up. Please try again in 30 seconds."
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timed out. Please try again."
        }), 504
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        message = data.get("message", "").strip()
        history = data.get("history", [])
        recruiter_mode = data.get("recruiterMode", False)

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if len(message) > 1000:
            return jsonify({"error": "Message too long"}), 400

        system_prompt = build_system_prompt(recruiter_mode)
        recent_history = get_recent_history(history)
        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        best_model = get_best_model()

        def generate():
            try:
                response = chat_with_ollama(
                    messages,
                    system_prompt,
                    best_model,
                    stream=True
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
                yield f"data: {json.dumps({'error': 'AI is starting up. Try again in 30 seconds.'})}\n\n"
            except requests.exceptions.Timeout:
                yield f"data: {json.dumps({'error': 'Request timed out. Please try again.'})}\n\n"
            except Exception as e:
                app.logger.error(f"Stream error: {str(e)}")
                yield f"data: {json.dumps({'error': 'Something went wrong'})}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        app.logger.error(f"Stream setup error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route("/models", methods=["GET"])
def list_models():
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if res.status_code == 200:
            models = [m.get("name") for m in res.json().get("models", [])]
            return jsonify({
                "models": models,
                "current": MODEL,
                "fallback": FALLBACK_MODEL
            })
        return jsonify({"error": "Ollama not responding"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    is_dev = os.getenv("FLASK_ENV") == "development"
    print(f"Starting Madheshwaran Personal AI Backend v2.0")
    print(f"Environment: {'Development' if is_dev else 'Production'}")
    print(f"Primary Model: {MODEL}")
    print(f"Fallback Model: {FALLBACK_MODEL}")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Port: {PORT}")
    app.run(
        debug=is_dev,
        host="0.0.0.0",
        port=PORT
    )