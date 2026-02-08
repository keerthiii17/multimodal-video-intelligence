from pathlib import Path
import shutil

RAW_VIDEO_DIR = Path("data/raw_videos")

def ingest_upload(file_path: str) -> Path:
    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    source = Path(file_path)
    destination = RAW_VIDEO_DIR / source.name

    shutil.copy(source, destination)
    return destination
