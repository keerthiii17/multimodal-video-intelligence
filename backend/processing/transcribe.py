from pathlib import Path
import whisper
import json

def transcribe_audio(audio_path: Path, output_dir: Path) -> Path:
    """
    Transcribes audio using Whisper and saves JSON transcript
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    transcript_path = output_dir / f"{audio_path.stem}.json"

    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path))

    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return transcript_path