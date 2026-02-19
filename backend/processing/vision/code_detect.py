import re
from pathlib import Path
import json

CODE_PATTERNS = [
    r"\bdef\b", r"\bclass\b", r"\bimport\b",
    r"\bfor\b", r"\bwhile\b", r"\breturn\b",
    r"\{", r"\}", r"\(", r"\)", r";", r"=="
]

def is_code_text(text: str) -> bool:
    matches = sum(bool(re.search(p, text)) for p in CODE_PATTERNS)
    return matches >= 2

def detect_code_from_ocr(ocr_path: Path):
    with open(ocr_path, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)

    code_frames = []

    for item in ocr_data:
        text = item["text"]
        if is_code_text(text):
            code_frames.append({
                "timestamp": item["timestamp"],
                "text": text
            })

    output_path = Path("data/code/code_segments.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(code_frames, f, indent=2)

    return output_path
