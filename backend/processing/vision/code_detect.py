import re
import json
from pathlib import Path


CODE_PATTERNS = [
    r"\bdef\b", r"\bclass\b", r"\bimport\b",
    r"\bfor\b", r"\bwhile\b", r"\breturn\b",
    r"\{", r"\}", r"\(", r"\)", r";", r"=="
]


def is_code_text(text: str) -> bool:
    matches = sum(bool(re.search(p, text)) for p in CODE_PATTERNS)
    return matches >= 2


def detect_code_from_ocr(ocr_path: Path, output_dir: Path) -> Path:
    """
    Detects code-like text from OCR results and saves it inside output_dir.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(ocr_path, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)

    code_frames = []

    for item in ocr_data:
        text = item.get("text", "")
        if is_code_text(text):
            code_frames.append({
                "timestamp": item["timestamp"],
                "text": text
            })

    output_path = output_dir / "code_segments.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(code_frames, f, indent=2)

    return output_path
