import json
from pathlib import Path


def fuse_multimodal_chunks(
    speech_chunks_path: Path,
    ocr_path: Path,
    code_path: Path,
    output_dir: Path,
    window: int = 5
) -> Path:
    """
    Fuse speech, OCR, and code into unified multimodal chunks.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(speech_chunks_path, "r", encoding="utf-8") as f:
        speech_chunks = json.load(f)

    with open(ocr_path, "r", encoding="utf-8") as f:
        ocr_chunks = json.load(f)

    with open(code_path, "r", encoding="utf-8") as f:
        code_chunks = json.load(f)

    multimodal_chunks = []

    for sc in speech_chunks:
        start = sc["start_time"]
        end = sc["end_time"]

        slide_texts = [
            o["text"]
            for o in ocr_chunks
            if abs(o["timestamp"] - start) <= window
        ]

        code_texts = [
            c["text"]
            for c in code_chunks
            if abs(c["timestamp"] - start) <= window
        ]

        multimodal_chunks.append({
            "start_time": start,
            "end_time": end,
            "speech": sc["text"],
            "slide_text": " ".join(slide_texts) if slide_texts else None,
            "code_text": " ".join(code_texts) if code_texts else None
        })

    output_path = output_dir / "multimodal_chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(multimodal_chunks, f, indent=2)

    return output_path