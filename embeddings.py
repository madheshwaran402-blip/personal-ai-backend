import os
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from knowledge_base import KNOWLEDGE_CHUNKS

# ============================================
# EMBEDDING ENGINE
# ============================================

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = "embeddings_cache.pkl"


class EmbeddingEngine:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks = KNOWLEDGE_CHUNKS
        self.embeddings = None
        self.texts = [chunk["content"] for chunk in self.chunks]
        print(f"Embedding model loaded: {MODEL_NAME}")

    def build_embeddings(self, force_rebuild: bool = False):
        if not force_rebuild and os.path.exists(EMBEDDINGS_FILE):
            print("Loading cached embeddings...")
            with open(EMBEDDINGS_FILE, "rb") as f:
                self.embeddings = pickle.load(f)
            print(f"Loaded {len(self.embeddings)} cached embeddings")
            return

        print(f"Building embeddings for {len(self.texts)} chunks...")
        self.embeddings = self.model.encode(
            self.texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump(self.embeddings, f)

        print(f"Built and cached {len(self.embeddings)} embeddings")

    def search(self, query: str, top_k: int = 3) -> list:
        if self.embeddings is None:
            self.build_embeddings()

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "content": self.chunks[idx]["content"],
                "category": self.chunks[idx]["category"],
                "id": self.chunks[idx]["id"],
                "score": float(similarities[idx])
            })

        return results

    def get_context(self, query: str, top_k: int = 3) -> str:
        results = self.search(query, top_k)
        context_parts = []
        for r in results:
            if r["score"] > 0.3:
                context_parts.append(r["content"])

        return "\n\n".join(context_parts) if context_parts else ""


# Singleton instance
_engine = None

def get_engine() -> EmbeddingEngine:
    global _engine
    if _engine is None:
        _engine = EmbeddingEngine()
        _engine.build_embeddings()
    return _engine


if __name__ == "__main__":
    engine = EmbeddingEngine()
    engine.build_embeddings(force_rebuild=True)

    test_queries = [
        "What sensors does the Smart Shoe have?",
        "Tell me about Determinex",
        "What are Madheshwaran's research interests?",
        "Did he win any competitions?",
        "What programming languages does he know?"
    ]

    print("\n" + "="*50)
    print("TESTING SEMANTIC SEARCH")
    print("="*50)

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = engine.search(query, top_k=2)
        for r in results:
            print(f"  Score: {r['score']:.3f} | {r['content'][:80]}...")