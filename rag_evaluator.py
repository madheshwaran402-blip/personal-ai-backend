import json
from faiss_store import get_store

# ============================================
# RAG QUALITY EVALUATOR
# ============================================

store = get_store()

TEST_CASES = [
    {
        "query": "What sensors does the Smart Shoe have?",
        "expected_category": "project",
        "expected_keywords": ["MPU6050", "MAX30102", "accelerometer"]
    },
    {
        "query": "Tell me about Determinex",
        "expected_category": "project",
        "expected_keywords": ["FPGA", "deterministic", "TRL"]
    },
    {
        "query": "What did Madheshwaran win?",
        "expected_category": "achievement",
        "expected_keywords": ["IDEATHON", "Medal", "PSNA"]
    },
    {
        "query": "What are his research interests?",
        "expected_category": "research",
        "expected_keywords": ["Neuromorphic", "Spiking", "SNN"]
    },
    {
        "query": "What programming languages does he know?",
        "expected_category": "skills",
        "expected_keywords": ["Python", "Java", "TypeScript"]
    },
    {
        "query": "What is his email and contact?",
        "expected_category": "identity",
        "expected_keywords": ["madheshwaran402@gmail.com"]
    },
    {
        "query": "Tell me about Safety Watch startup",
        "expected_category": "startup",
        "expected_keywords": ["offline", "wearable", "Hospital"]
    },
    {
        "query": "What are his career goals?",
        "expected_category": "goals",
        "expected_keywords": ["VLSI", "semiconductor", "Intel"]
    },
    {
        "query": "What is MQTT water tank project?",
        "expected_category": "project",
        "expected_keywords": ["MQTT", "pump", "water"]
    },
    {
        "query": "What hardware skills does he have?",
        "expected_category": "skills",
        "expected_keywords": ["Verilog", "FPGA", "SystemVerilog"]
    }
]


def evaluate_rag():
    print("=" * 60)
    print("RAG QUALITY EVALUATION")
    print("=" * 60)

    passed = 0
    failed = 0
    results = []

    for test in TEST_CASES:
        query = test["query"]
        expected_cat = test["expected_category"]
        expected_kws = test["expected_keywords"]

        search_results = store.search(query, top_k=3, min_score=0.2)

        top_result = search_results[0] if search_results else None

        category_match = any(
            r["category"] == expected_cat
            for r in search_results
        )

        combined_text = " ".join([r["content"] for r in search_results])
        keyword_matches = [
            kw for kw in expected_kws
            if kw.lower() in combined_text.lower()
        ]
        keyword_score = len(keyword_matches) / len(expected_kws)

        success = category_match and keyword_score >= 0.5
        if success:
            passed += 1
        else:
            failed += 1

        result = {
            "query": query,
            "success": success,
            "category_match": category_match,
            "keyword_score": keyword_score,
            "top_score": top_result["score"] if top_result else 0,
            "keywords_found": keyword_matches,
            "keywords_missing": [
                kw for kw in expected_kws
                if kw.lower() not in combined_text.lower()
            ]
        }
        results.append(result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} | {query}")
        print(f"  Category match: {category_match}")
        print(f"  Keyword score: {keyword_score:.0%}")
        print(f"  Top similarity: {result['top_score']:.3f}")
        if result["keywords_missing"]:
            print(f"  Missing: {result['keywords_missing']}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{len(TEST_CASES)} passed")
    print(f"Success rate: {passed/len(TEST_CASES):.0%}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    evaluate_rag()