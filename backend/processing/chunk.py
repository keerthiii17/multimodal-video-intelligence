from pathlib import Path
import json

def create_chunks(transcript_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    chunks = []
    for seg in transcript["segments"]:
        chunks.append({
            "start_time": seg["start"],
            "end_time": seg["end"],
            "text": seg["text"].strip()
        })

    output_path = output_dir / "chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return output_path