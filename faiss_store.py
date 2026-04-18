import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from knowledge_base import KNOWLEDGE_CHUNKS

# ============================================
# FAISS VECTOR STORE
# ============================================

MODEL_NAME = "all-MiniLM-L6-v2"
FAISS_INDEX_FILE = "faiss_index.pkl"
DIMENSION = 384  # all-MiniLM-L6-v2 output dimension


class FAISSStore:
    def __init__(self):
        print("Initializing FAISS store...")
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks = KNOWLEDGE_CHUNKS
        self.texts = [chunk["content"] for chunk in self.chunks]
        self.index = None
        print(f"Model loaded: {MODEL_NAME}")
        print(f"Knowledge chunks: {len(self.chunks)}")

    def build_index(self, force_rebuild: bool = False):
        if not force_rebuild and os.path.exists(FAISS_INDEX_FILE):
            print("Loading cached FAISS index...")
            with open(FAISS_INDEX_FILE, "rb") as f:
                self.index = pickle.load(f)
            print(f"FAISS index loaded with {self.index.ntotal} vectors")
            return

        print("Building FAISS index...")

        # Generate embeddings
        embeddings = self.model.encode(
            self.texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        # Convert to float32 (FAISS requirement)
        embeddings = np.array(embeddings, dtype=np.float32)

        # Create FAISS index
        # IndexFlatIP = Inner Product (cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(DIMENSION)

        # Add embeddings to index
        self.index.add(embeddings)

        # Cache the index
        with open(FAISS_INDEX_FILE, "wb") as f:
            pickle.dump(self.index, f)

        print(f"FAISS index built with {self.index.ntotal} vectors")
        print(f"Index cached to {FAISS_INDEX_FILE}")

    def search(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.3
    ) -> list:
        if self.index is None:
            self.build_index()

        # Encode query
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        # Search FAISS index
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            if float(score) < min_score:
                continue
            results.append({
                "content": self.chunks[idx]["content"],
                "category": self.chunks[idx]["category"],
                "id": self.chunks[idx]["id"],
                "score": float(score)
            })

        return results

    def get_context(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.3
    ) -> str:
        results = self.search(query, top_k, min_score)

        if not results:
            return ""

        context_parts = [r["content"] for r in results]
        return "\n\n".join(context_parts)

    def get_context_with_scores(
        self,
        query: str,
        top_k: int = 3
    ) -> dict:
        results = self.search(query, top_k)
        return {
            "context": "\n\n".join([r["content"] for r in results]),
            "results": results,
            "query": query
        }

    def add_chunk(self, content: str, category: str, chunk_id: str):
        embedding = self.model.encode(
            [content],
            normalize_embeddings=True
        )
        embedding = np.array(embedding, dtype=np.float32)
        self.index.add(embedding)
        self.chunks.append({
            "id": chunk_id,
            "category": category,
            "content": content
        })
        self.texts.append(content)
        print(f"Added chunk: {chunk_id}")

    def get_stats(self) -> dict:
        return {
            "total_chunks": len(self.chunks),
            "index_size": self.index.ntotal if self.index else 0,
            "model": MODEL_NAME,
            "dimension": DIMENSION,
            "categories": list(set(
                c["category"] for c in self.chunks
            ))
        }


# ============================================
# SINGLETON
# ============================================

_store = None

def get_store() -> FAISSStore:
    global _store
    if _store is None:
        _store = FAISSStore()
        _store.build_index()
    return _store


# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    store = FAISSStore()
    store.build_index(force_rebuild=True)

    print("\n" + "=" * 50)
    print("FAISS STORE STATS")
    print("=" * 50)
    stats = store.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    test_queries = [
        "What sensors does the Smart Shoe have?",
        "Tell me about Determinex FPGA project",
        "What are Madheshwaran's research interests?",
        "Did he win any competitions or awards?",
        "What programming languages does he know?",
        "Tell me about the Safety Watch startup",
        "What is his career goal?",
        "What is the water tank project?",
        "What are his hardware skills?",
        "Tell me about neuromorphic computing"
    ]

    print("\n" + "=" * 50)
    print("SEMANTIC SEARCH TESTS")
    print("=" * 50)

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = store.search(query, top_k=2)
        for r in results:
            print(
                f"  [{r['score']:.3f}] "
                f"({r['category']}) "
                f"{r['content'][:70]}..."
            )