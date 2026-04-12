import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def parse_timestamp(question: str):
    import re
    match = re.search(r"\d{1,2}:\d{2}", question)
    if match:
        time_str = match.group()
        m, s = map(int, time_str.split(":"))
        return m * 60 + s
    return None
def search_multimodal(question: str, video_dir: Path, top_k: int = 3):

    embeddings_path = video_dir / "embeddings" / "multimodal_embeddings.npz"

    data = np.load(embeddings_path, allow_pickle=True)
    embeddings = data["embeddings"]
    chunks = data["chunks"]

    # 🔥 CHECK timestamp query
    target_time = parse_timestamp(question)

    if target_time is not None:
        results = []
        for c in chunks:
            if c["start_time"] <= target_time <= c["end_time"]:
                results.append({
                    "score": 1.0,
                    "start_time": c["start_time"],
                    "end_time": c["end_time"],
                    "speech": c.get("speech"),
                    "slide_text": c.get("slide_text"),
                    "code_text": c.get("code_text")
                })
        return results[:top_k]

    # 🔥 normal semantic search
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode([question])

    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_indices:
        for idx in top_indices:
         if scores[idx] < 0.4:
          continue
        results.append({
            "score": float(scores[idx]),
            "start_time": chunks[idx]["start_time"],
            "end_time": chunks[idx]["end_time"],
            "speech": chunks[idx].get("speech"),
            "slide_text": chunks[idx].get("slide_text"),
            "code_text": chunks[idx].get("code_text")
        })

    return results

