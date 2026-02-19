import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

EMBED_DIR = Path("data/embeddings")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_chunks(query: str, top_k: int = 3):
    embeddings = np.load(EMBED_DIR / "chunk_embeddings.npy")

    with open(EMBED_DIR / "chunk_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vec = model.encode([query], convert_to_numpy=True)[0]

    scores = [
        cosine_similarity(query_vec, emb) for emb in embeddings
    ]

    top_indices = np.argsort(scores)[-top_k:][::-1]

    return [metadata[i] for i in top_indices]
