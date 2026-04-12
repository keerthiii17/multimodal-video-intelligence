import json
from pathlib import Path
import requests


def seconds_to_mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def generate_summary(video_dir: Path) -> str:

    multimodal_path = video_dir / "multimodal" / "multimodal_chunks.json"

    # ---------- LOAD CHUNKS ----------
    try:
        with open(multimodal_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception as e:
        return f"⚠️ Failed to load chunks: {str(e)}"

    if not chunks:
        return "⚠️ No content found for summary."

    # ---------- SELECT LIMITED CHUNKS ----------
    selected = chunks[:12]

    formatted_content = ""

    for c in selected:
        start = seconds_to_mmss(c["start_time"])
        end = seconds_to_mmss(c["end_time"])

        text = c.get("speech", "")[:100]  # limit for speed

        formatted_content += f"[{start} – {end}] {text}\n"

    # ---------- PROMPT ----------
    prompt = f"""
You are an AI video assistant.

Summarize the video in a structured way.

For EACH timestamp:
- give 1–2 line explanation
- keep it simple and clear

Format:
[time] → explanation

Video content:
{formatted_content}
"""

    # ---------- LLM CALL ----------
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "tinyllama",   # better quality for summary
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            return f"⚠️ LLM error: {response.status_code}"

        data = response.json()
        summary = data.get("response")

        if not summary:
            return "⚠️ Summary generation failed (empty response)"

        return summary

    except Exception as e:
        return f"⚠️ Error generating summary: {str(e)}"