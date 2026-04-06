from pathlib import Path
import shutil
from fastapi import UploadFile

RAW_VIDEO_DIR = Path("data/raw_videos")

def ingest_upload(file_path: str) -> Path:
    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    source = Path(file_path)
    destination = RAW_VIDEO_DIR / source.name

    shutil.copy(source, destination)
    return destination




def save_uploaded_video(file: UploadFile) -> Path:
    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    save_path = RAW_VIDEO_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return save_path
