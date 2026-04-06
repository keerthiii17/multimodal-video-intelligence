from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def embed_multimodal_chunks(
    multimodal_path: Path,
    output_dir: Path
) -> Path:
    """
    Generate embeddings for multimodal chunks and save them to output_dir.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(multimodal_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    

    texts = []
    for c in chunks:
        combined = c.get("speech", "")
        if c.get("slide_text"):
            combined += " " + c["slide_text"]
        if c.get("code_text"):
            combined += " " + c["code_text"]
        texts.append(combined)

    embeddings = model.encode(texts, convert_to_numpy=True)

    output_path = output_dir / "multimodal_embeddings.npz"

    np.savez(
        output_path,
        embeddings=embeddings,
        chunks=chunks
    )

    return output_path
