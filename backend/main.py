from backend.ingest.ingest import ingest_video
from backend.cache.fingerprint import compute_video_hash
from backend.cache.cache_manager import (
    is_video_processed,
    mark_video_processed
)

if __name__ == "__main__":
    video_path = ingest_video(
        source="https://www.youtube.com/watch?v=gN07gbipMoY",
        source_type="youtube"
    )

    video_hash = compute_video_hash(video_path)

    if is_video_processed(video_hash):
        print("Video already processed. Skipping pipeline.")
    else:
        print("New video. Processing pipeline...")
        
        # Future steps: transcription, OCR, embeddings
        
        mark_video_processed(
            video_hash,
            {
                "path": str(video_path),
                "status": "processed"
            }
        )
