import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def search_multimodal(
    question: str,
    video_dir: Path,
    top_k: int = 3
):
    """
    Search multimodal embeddings for a single video.
    """

    embeddings_path = video_dir / "embeddings" / "multimodal_embeddings.npz"

    data = np.load(embeddings_path, allow_pickle=True)
    embeddings = data["embeddings"]
    chunks = data["chunks"]

    
    query_embedding = model.encode([question])

    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "score": float(scores[idx]),
            "start_time": chunks[idx]["start_time"],
            "end_time": chunks[idx]["end_time"],
            "speech": chunks[idx].get("speech"),
            "slide_text": chunks[idx].get("slide_text"),
            "code_text": chunks[idx].get("code_text")
        })

    return results

