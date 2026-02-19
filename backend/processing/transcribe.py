from pathlib import Path
import whisper
import json

TRANSCRIPT_DIR = Path("data/transcripts")

def transcribe_audio(audio_path: Path) -> Path:
    """
    Transcribes audio using Whisper and returns transcript JSON path
    """
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    model = whisper.load_model("base")
    result = model.transcribe(
        str(audio_path),
        word_timestamps=True
    )

    transcript_path = TRANSCRIPT_DIR / f"{audio_path.stem}.json"

    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return transcript_path
