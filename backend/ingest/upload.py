from pathlib import Path
import shutil
from fastapi import UploadFile

RAW_VIDEO_DIR = Path("data/raw_videos")


# 🔥 MAIN FUNCTION USED BY PIPELINE
def ingest_upload(file_path: str) -> Path:
    """
    Used by ingest pipeline.
    Accepts a file path and returns stored video path.
    """

    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    source = Path(file_path)
    destination = RAW_VIDEO_DIR / source.name

    # 🔥 IMPORTANT: avoid overwriting same file
    if not destination.exists():
        shutil.copy(source, destination)

    return destination


# 🔥 USED BY API (UPLOAD ENDPOINT)
def save_uploaded_video(file: UploadFile) -> Path:
    """
    Saves uploaded file and returns full path
    """

    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    save_path = RAW_VIDEO_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return save_path