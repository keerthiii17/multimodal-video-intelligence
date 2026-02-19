from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_DIR = Path("data/embeddings")

def embed_chunks(chunk_path: Path):
    EMBED_DIR.mkdir(parents=True, exist_ok=True)

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks]

    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

    embeddings = model.encode(texts, convert_to_numpy=True)

    np.save(EMBED_DIR / "chunk_embeddings.npy", embeddings)

    with open(EMBED_DIR / "chunk_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    return EMBED_DIR / "chunk_embeddings.npy"
