from pathlib import Path
import subprocess


def extract_frames(video_path: Path, output_dir: Path, interval: int = 2) -> Path:
    """
    Extract frames from video at a fixed interval (seconds)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    frame_pattern = output_dir / "frame_%04d.jpg"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vf", f"fps=1/{interval}",
        str(frame_pattern)
    ]

    subprocess.run(command, check=True)

    return output_dir