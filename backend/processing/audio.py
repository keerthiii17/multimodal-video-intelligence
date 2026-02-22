import subprocess
from pathlib import Path

AUDIO_DIR = Path("data/audio")

def extract_audio(video_path: Path) -> Path:
    """
    Extracts audio from video using ffmpeg (mono, 16kHz)
    """
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    audio_path = AUDIO_DIR / f"{video_path.stem}.wav"

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
