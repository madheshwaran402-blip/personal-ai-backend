import re
from typing import Optional

# ============================================
# QUERY PREPROCESSOR
# ============================================

QUERY_EXPANSIONS = {
    "shoe": "smart shoe esp32 sensors MPU6050",
    "patent": "smart shoe patented esp32 wearable",
    "determinex": "determinex FPGA deterministic data stream",
    "fpga": "FPGA verilog determinex hardware",
    "snn": "spiking neural networks neuromorphic SNN Brian2",
    "neuromorphic": "neuromorphic computing spiking neural networks",
    "contact": "email phone contact madheshwaran402@gmail.com",
    "award": "IDEATHON winner achievement medal PSNA",
    "win": "IDEATHON winner achievement medal prize",
    "startup": "startup determinex safety watch platform",
    "safety watch": "safety watch platform offline wearable hospital",
    "water tank": "water tank MQTT automation Node.js",
    "mqtt": "MQTT water tank automation Node.js",
    "research": "neuromorphic computing research interests Scopus",
    "goal": "career goals VLSI semiconductor Intel Qualcomm",
    "skill": "Verilog Python Java hardware programming skills",
    "project": "determinex smart shoe water tank personal AI",
    "education": "VLSI design technology degree second year"
}

STOP_WORDS = {
    "tell", "me", "about", "what", "is", "are", "does",
    "did", "has", "have", "how", "why", "when", "where",
    "who", "the", "a", "an", "his", "her", "your",
    "madheshwaran", "please", "can", "you", "i", "want",
    "know", "like", "just", "really", "very"
}


def clean_query(query: str) -> str:
    query = query.lower().strip()
    query = re.sub(r'[^\w\s]', ' ', query)
    query = re.sub(r'\s+', ' ', query)
    return query


def expand_query(query: str) -> str:
    cleaned = clean_query(query)
    expanded_parts = [query]

    for keyword, expansion in QUERY_EXPANSIONS.items():
        if keyword.lower() in cleaned:
            expanded_parts.append(expansion)
            break

    return " ".join(expanded_parts)


def extract_keywords(query: str) -> list:
    cleaned = clean_query(query)
    words = cleaned.split()
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return keywords


def preprocess_query(query: str) -> dict:
    original = query
    cleaned = clean_query(query)
    expanded = expand_query(query)
    keywords = extract_keywords(query)

    return {
        "original": original,
        "cleaned": cleaned,
        "expanded": expanded,
        "keywords": keywords
    }


def get_search_query(query: str) -> str:
    processed = preprocess_query(query)
    return processed["expanded"]


if __name__ == "__main__":
    test_queries = [
        "Tell me about the shoe",
        "What did he win?",
        "What's his email?",
        "Tell me about neuromorphic research",
        "What FPGA skills does he have?",
        "Does he have any startups?"
    ]

    print("QUERY PREPROCESSING TEST")
    print("=" * 50)

    for query in test_queries:
        result = preprocess_query(query)
        print(f"\nOriginal:  {result['original']}")
        print(f"Expanded:  {result['expanded']}")
        print(f"Keywords:  {result['keywords']}")