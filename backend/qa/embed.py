from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_DIR = Path("data/embeddings")

from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def embed_chunks(
    chunk_path: Path,
    output_dir: Path
) -> Path:
    """
    Embed speech-only chunks (baseline embeddings) and save per video.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]

    
    embeddings = model.encode(texts, convert_to_numpy=True)

    output_path = output_dir / "audio_embeddings.npz"

    np.savez(
        output_path,
        embeddings=embeddings,
        chunks=chunks
    )

    return output_path
