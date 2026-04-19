import os
import json
import sqlite3
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from faiss_store import get_store

# ============================================
# CONVERSATION MEMORY STORE
# ============================================

DB_FILE = "memory.db"
MODEL_NAME = "all-MiniLM-L6-v2"
MAX_MEMORIES = 5


class MemoryStore:
    def __init__(self):
        self.db_path = DB_FILE
        self.model = SentenceTransformer(MODEL_NAME)
        self._init_db()
        print(f"Memory store initialized: {DB_FILE}")

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                embedding BLOB,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                message_count INTEGER DEFAULT 0,
                summary TEXT
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session
            ON conversations(session_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON conversations(timestamp)
        """)

        conn.commit()
        conn.close()

    def save_conversation(
        self,
        session_id: str,
        user_message: str,
        ai_response: str,
        metadata: dict = None
    ) -> int:
        combined_text = f"Question: {user_message} Answer: {ai_response}"
        embedding = self.model.encode(
            [combined_text],
            normalize_embeddings=True
        )[0]
        embedding_bytes = embedding.astype(np.float32).tobytes()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations
            (session_id, user_message, ai_response, timestamp, embedding, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            user_message,
            ai_response,
            datetime.now().isoformat(),
            embedding_bytes,
            json.dumps(metadata or {})
        ))

        conv_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO sessions (id, created_at, message_count)
            VALUES (?, ?, 1)
            ON CONFLICT(id) DO UPDATE SET
            message_count = message_count + 1
        """, (session_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        return conv_id

    def search_memories(
        self,
        query: str,
        top_k: int = MAX_MEMORIES,
        min_score: float = 0.4
    ) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, session_id, user_message, ai_response,
                   timestamp, embedding, metadata
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT 100
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0].astype(np.float32)

        scored = []
        for row in rows:
            conv_id, session_id, user_msg, ai_resp, ts, emb_bytes, meta = row

            if emb_bytes:
                stored_emb = np.frombuffer(
                    emb_bytes,
                    dtype=np.float32
                )
                score = float(np.dot(query_embedding, stored_emb))

                if score >= min_score:
                    scored.append({
                        "id": conv_id,
                        "session_id": session_id,
                        "user_message": user_msg,
                        "ai_response": ai_resp,
                        "timestamp": ts,
                        "score": score,
                        "metadata": json.loads(meta or "{}")
                    })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def get_session_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_message, ai_response, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "user_message": r[0],
                "ai_response": r[1],
                "timestamp": r[2]
            }
            for r in reversed(rows)
        ]

    def get_relevant_memories(
        self,
        query: str,
        current_session: str,
        top_k: int = 3
    ) -> str:
        memories = self.search_memories(query, top_k=top_k + 2)
        relevant = [
            m for m in memories
            if m["session_id"] != current_session
        ][:top_k]

        if not relevant:
            return ""

        memory_parts = []
        for mem in relevant:
            ts = mem["timestamp"][:10]
            memory_parts.append(
                f"[{ts}] User asked: {mem['user_message']}\n"
                f"Response: {mem['ai_response'][:150]}..."
            )

        return "\n\n".join(memory_parts)

    def get_stats(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM conversations")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sessions")
        sessions = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM conversations
            WHERE timestamp > datetime('now', '-7 days')
        """)
        recent = cursor.fetchone()[0]

        conn.close()

        return {
            "total_conversations": total,
            "total_sessions": sessions,
            "conversations_last_7_days": recent
        }

    def clear_old_memories(self, days: int = 30):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM conversations
            WHERE timestamp < datetime('now', ? || ' days')
        """, (f"-{days}",))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        print(f"Cleared {deleted} old memories")
        return deleted


_memory_store = None


def get_memory_store() -> MemoryStore:
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryStore()
    return _memory_store


if __name__ == "__main__":
    store = MemoryStore()

    print("Testing memory store...")

    test_session = "test_session_001"
    store.save_conversation(
        test_session,
        "What is Determinex?",
        "Determinex is Madheshwaran's FPGA-based project for handling deterministic data streams.",
        {"recruiter_mode": False}
    )

    store.save_conversation(
        test_session,
        "What sensors does the Smart Shoe have?",
        "The Smart Shoe uses MPU6050 for motion and MAX30102 for heart rate monitoring.",
        {"recruiter_mode": False}
    )

    store.save_conversation(
        "session_002",
        "What are his career goals?",
        "Madheshwaran wants to work in core VLSI at Intel, Qualcomm, or Texas Instruments.",
        {"recruiter_mode": True}
    )

    print("\n" + "=" * 50)
    print("MEMORY SEARCH TEST")
    print("=" * 50)

    test_queries = [
        "FPGA project",
        "shoe sensors motion",
        "career goals VLSI"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = store.search_memories(query, top_k=2)
        for r in results:
            print(f"  [{r['score']:.3f}] {r['user_message']}")

    print("\n" + "=" * 50)
    print("SESSION HISTORY TEST")
    print("=" * 50)

    history = store.get_session_history(test_session)
    for h in history:
        print(f"User: {h['user_message']}")
        print(f"AI: {h['ai_response'][:80]}...")
        print()

    print("\n" + "=" * 50)
    print("STATS")
    print("=" * 50)
    stats = store.get_stats()
    for k, v in stats.items():
        print(f"{k}: {v}")