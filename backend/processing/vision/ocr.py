import pytesseract
from PIL import Image
from pathlib import Path
import json
import re


def run_ocr(frames_dir: Path, output_dir: Path, interval: int = 2) -> Path:
    """
    Runs OCR on extracted frames and maps text to timestamps.
    Saves results inside the given output_dir.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    ocr_results = []

    frames = sorted(frames_dir.glob("frame_*.jpg"))

    for idx, frame_path in enumerate(frames):
        image = Image.open(frame_path)
        text = pytesseract.image_to_string(image)
        text = clean_text(text)
        timestamp = idx * interval

        if text:
            ocr_results.append({
                "timestamp": timestamp,
                "text": text
            })

    output_path = output_dir / "ocr_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ocr_results, f, indent=2)

    return output_path



def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9(){}=+\-*/., ]", "", text)
    return text.strip()

