from pathlib import Path
from backend.ingest.youtube import ingest_youtube
from backend.ingest.upload import ingest_upload
from backend.cache.fingerprint import compute_video_hash


def ingest_video(source: str, source_type: str) -> Path:
    """
    Only handles ingestion (download/upload)
    Your pipeline already processes data elsewhere
    """

    if source_type == "youtube":
        video_path = ingest_youtube(source)

    elif source_type == "upload":
        video_path = ingest_upload(source)

    else:
        raise ValueError("Unsupported source type")

    video_id = compute_video_hash(video_path)

    video_dir = Path(f"data/videos/{video_id}")
    video_dir.mkdir(parents=True, exist_ok=True)

    return video_dir