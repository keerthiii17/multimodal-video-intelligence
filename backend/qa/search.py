from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def search_chunks(
    question: str,
    video_dir: Path,
    top_k: int = 3
):
    """
    Search speech-only embeddings (baseline) for a single video.
    """

    embeddings_path = (
        video_dir / "baseline_embeddings" / "audio_embeddings.npz"
    )

    data = np.load(embeddings_path, allow_pickle=True)
    embeddings = data["embeddings"]
    chunks = data["chunks"]

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode([question])

    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "score": float(scores[idx]),
            "start_time": chunks[idx]["start_time"],
            "end_time": chunks[idx]["end_time"],
            "text": chunks[idx]["text"]
        })

    return results
