def seconds_to_mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def format_answer(question: str, chunks: list) -> str:
    """
    Formats retrieved chunks into a clean, timestamped answer.
    """
    lines = []
    lines.append(f"Q: {question}\n")
    lines.append("Answer (key moments):\n")

    for c in chunks:
        start = seconds_to_mmss(c["start_time"])
        end = seconds_to_mmss(c["end_time"])
        text = c["text"]
        lines.append(f"- [{start} – {end}] {text}")

    return "\n".join(lines)
