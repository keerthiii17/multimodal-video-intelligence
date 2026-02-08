import hashlib
from pathlib import Path

def compute_video_hash(video_path: Path) -> str:
    """
    Computes SHA256 hash of the video file
    """
    hash_sha256 = hashlib.sha256()

    with open(video_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()
