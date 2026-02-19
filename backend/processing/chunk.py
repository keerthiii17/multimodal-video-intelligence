from pathlib import Path
import json

CHUNK_DIR = Path("data/chunks")

def create_chunks(transcript_path: Path) -> Path:
    """
    Convert Whisper transcript into structured timestamp chunks
    """
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    segments = transcript.get("segments", [])

    chunks = []

    for segment in segments:
        chunk = {
            "start_time": segment["start"],
            "end_time": segment["end"],
            "text": segment["text"].strip()
        }
        chunks.append(chunk)

    chunk_path = CHUNK_DIR / f"{transcript_path.stem}_chunks.json"

    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    return chunk_path
