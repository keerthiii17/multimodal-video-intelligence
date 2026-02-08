from pathlib import Path
from backend.ingest.youtube import ingest_youtube
from backend.ingest.upload import ingest_upload

def ingest_video(source: str, source_type: str) -> Path:
    """
    source_type: 'youtube' or 'upload'
    """
    if source_type == "youtube":
        return ingest_youtube(source)

    elif source_type == "upload":
        return ingest_upload(source)

    else:
        raise ValueError("Unsupported source type")
