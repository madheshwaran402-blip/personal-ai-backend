import os
import json
import requests
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
from madheshwaran_profile import build_system_prompt, PROFILE
from faiss_store import get_store
from memory_store import get_memory_store

load_dotenv()

app = Flask(__name__)

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

print("Initializing RAG system...")
rag_store = get_store()
print(f"RAG ready: {rag_store.get_stats()['total_chunks']} chunks")

print("Initializing memory system...")
memory_store = get_memory_store()
print(f"Memory ready: {memory_store.get_stats()['total_conversations']} stored")


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


def build_enhanced_prompt(
    query: str,
    session_id: str,
    system_prompt: str
) -> str:
    rag_context = rag_store.get_context(
        query, top_k=3, min_score=0.3
    )
    memory_context = memory_store.get_relevant_memories(
        query, session_id, top_k=2
    )

    additions = []

    if rag_context:
        additions.append(
            f"=== KNOWLEDGE BASE ===\n{rag_context}\n=== END KNOWLEDGE ==="
        )

    if memory_context:
        additions.append(
            f"=== PAST CONVERSATIONS ===\n{memory_context}\n=== END MEMORIES ==="
        )

    if additions:
        context_block = "\n\n".join(additions)
        return (
            system_prompt
            + f"\n\n{context_block}\n\n"
            + "Use the above context and memories to give a specific, accurate answer."
        )

    return system_prompt


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
        "rag_chunks": rag_store.get_stats()["total_chunks"],
        "memory_conversations": memory_store.get_stats()["total_conversations"],
        "assistant": "Madheshwaran Personal AI with RAG + Memory",
        "version": "4.0"
    })


@app.route("/health", methods=["GET"])
def health():
    ollama_ok = check_ollama()
    model_exists = check_model_exists(MODEL) if ollama_ok else False
    rag_stats = rag_store.get_stats()
    memory_stats = memory_store.get_stats()

    return jsonify({
        "backend": "running",
        "ollama": "running" if ollama_ok else "offline",
        "model": MODEL,
        "model_ready": model_exists,
        "fallback": FALLBACK_MODEL,
        "streaming": True,
        "rag": {
            "enabled": True,
            "chunks": rag_stats["total_chunks"],
            "categories": rag_stats["categories"]
        },
        "memory": {
            "enabled": True,
            "total_conversations": memory_stats["total_conversations"],
            "total_sessions": memory_stats["total_sessions"]
        }
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
        session_id = data.get("sessionId", "default_session")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if len(message) > 1000:
            return jsonify({"error": "Message too long"}), 400

        base_prompt = build_system_prompt(recruiter_mode)
        enhanced_prompt = build_enhanced_prompt(
            message, session_id, base_prompt
        )

        recent_history = get_recent_history(history)
        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        best_model = get_best_model()
        response = chat_with_ollama(
            messages,
            enhanced_prompt,
            best_model,
            stream=False
        )

        data_response = response.json()
        answer = data_response.get("message", {}).get("content", "")

        memory_store.save_conversation(
            session_id,
            message,
            answer,
            {"recruiter_mode": recruiter_mode}
        )

        return jsonify({
            "answer": answer,
            "model": best_model,
            "recruiterMode": recruiter_mode,
            "rag_used": True,
            "memory_saved": True
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
        session_id = data.get("sessionId", "default_session")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if len(message) > 1000:
            return jsonify({"error": "Message too long"}), 400

        base_prompt = build_system_prompt(recruiter_mode)
        enhanced_prompt = build_enhanced_prompt(
            message, session_id, base_prompt
        )

        recent_history = get_recent_history(history)
        messages = recent_history + [
            {"role": "user", "content": message}
        ]

        best_model = get_best_model()
        full_response = []

        def generate():
            try:
                response = chat_with_ollama(
                    messages,
                    enhanced_prompt,
                    best_model,
                    stream=True
                )

                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode("utf-8"))
                            word = chunk.get("message", {}).get("content", "")
                            if word:
                                full_response.append(word)
                                yield f"data: {json.dumps({'word': word})}\n\n"
                            if chunk.get("done"):
                                complete_response = "".join(full_response)
                                memory_store.save_conversation(
                                    session_id,
                                    message,
                                    complete_response,
                                    {"recruiter_mode": recruiter_mode}
                                )
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                        except json.JSONDecodeError:
                            continue

            except requests.exceptions.ConnectionError:
                yield f"data: {json.dumps({'error': 'Ollama not running.'})}\n\n"
            except requests.exceptions.Timeout:
                yield f"data: {json.dumps({'error': 'Request timed out.'})}\n\n"
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


@app.route("/memory", methods=["GET"])
def get_memory_stats():
    stats = memory_store.get_stats()
    return jsonify(stats)


@app.route("/memory/search", methods=["POST"])
def search_memories():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        top_k = data.get("top_k", 3)

        if not query:
            return jsonify({"error": "No query provided"}), 400

        memories = memory_store.search_memories(query, top_k)
        return jsonify({
            "query": query,
            "memories": memories,
            "count": len(memories)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/memory/session/<session_id>", methods=["GET"])
def get_session(session_id: str):
    history = memory_store.get_session_history(session_id)
    return jsonify({
        "session_id": session_id,
        "history": history,
        "count": len(history)
    })


@app.route("/search", methods=["POST"])
def semantic_search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        top_k = data.get("top_k", 3)

        if not query:
            return jsonify({"error": "No query provided"}), 400

        results = rag_store.get_context_with_scores(query, top_k)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    print(f"\nStarting Madheshwaran Personal AI Backend v4.0")
    print(f"Features: RAG + Memory + FAISS + Query Expansion")
    print(f"Environment: {'Development' if is_dev else 'Production'}")
    print(f"Model: {MODEL} (fallback: {FALLBACK_MODEL})")
    print(f"Port: {PORT}\n")
    app.run(
        debug=is_dev,
        host="0.0.0.0",
        port=PORT
    )