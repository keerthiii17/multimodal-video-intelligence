import subprocess
from pathlib import Path

RAW_VIDEO_DIR = Path("data/raw_videos")

def ingest_youtube(url: str) -> Path:
    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_VIDEO_DIR / "youtube_video.mp4"

    subprocess.run(
        ["yt-dlp", "-f", "best", "-o", str(output_path), url],
        check=True
    )

    return output_path
