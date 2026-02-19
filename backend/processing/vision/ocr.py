import pytesseract
from PIL import Image
from pathlib import Path
import json

def run_ocr(frames_dir: Path, interval: int = 2):
    """
    Runs OCR on extracted frames and maps text to timestamps.
    """
    ocr_results = []

    frames = sorted(frames_dir.glob("frame_*.jpg"))

    for idx, frame_path in enumerate(frames):
        image = Image.open(frame_path)
        text = pytesseract.image_to_string(image).strip()

        timestamp = idx * interval

        if text:
            ocr_results.append({
                "timestamp": timestamp,
                "text": text
            })

    output_path = Path("data/ocr/ocr_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ocr_results, f, indent=2)

    return output_path
