import subprocess
from pathlib import Path

def extract_audio(video_path: Path, output_dir: Path) -> Path:
    """
    Extracts mono 16kHz audio from video using ffmpeg
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        str(audio_path)
    ]

    subprocess.run(command, check=True)
    return audio_path