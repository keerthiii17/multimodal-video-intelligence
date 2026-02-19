import subprocess
from pathlib import Path

def extract_frames(video_path: str, interval: int = 2):
    """
    Extracts frames every `interval` seconds using FFmpeg.
    """
    output_dir = Path("data/frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / "frame_%06d.jpg"

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps=1/{interval}",
        str(output_pattern)
    ]

    subprocess.run(command, check=True)

    return output_dir
