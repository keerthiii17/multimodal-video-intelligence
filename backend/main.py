from backend.ingest.ingest import ingest_video
from backend.cache.fingerprint import compute_video_hash
from backend.cache.cache_manager import (
    is_video_processed,
    mark_video_processed
)
from backend.processing.audio import extract_audio

if __name__ == "__main__":
    video_path = ingest_video(
        source="https://www.youtube.com/watch?v=OfkYUaCp3mc",
        source_type="youtube"
    )

    video_hash = compute_video_hash(video_path)

    if is_video_processed(video_hash):
        print("Video already processed. Skipping pipeline.")
    else:
        print("New video. Processing pipeline...")

        # 🔹 Day 4 addition
        audio_path = extract_audio(video_path)
        print(f"Audio extracted at: {audio_path}")

        mark_video_processed(
            video_hash,
            {
                "video_path": str(video_path),
                "audio_path": str(audio_path),
                "status": "audio_extracted"
            }
        )
