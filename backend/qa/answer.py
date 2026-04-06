import requests
from backend.qa.code_understanding import detect_language


def seconds_to_mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def generate_llm_answer(question, chunks, mode):

    context_parts = []

    for c in chunks:
        text = ""
        if c.get("speech"):
            text += c["speech"] + " "
        if c.get("slide_text"):
            text += c["slide_text"] + " "
        if c.get("code_text"):
            text += c["code_text"]

        context_parts.append(text.strip())

    context = "\n".join(context_parts)

    # 🔥 Code detection
    code_texts = [c.get("code_text") for c in chunks if c.get("code_text")]

    code_info = ""
    if code_texts:
        lang = detect_language(code_texts[0])
        code_info = f"\nDetected Code Language: {lang}\n"

    # 🔥 Mode handling
    if mode == "short":
        instruction = "Answer in ONE LINE only."

    elif mode == "detailed":
        instruction = """
Explain clearly.
Include intuition and steps.
"""

    else:
        instruction = "Explain simply."

    prompt = f"""
You are an AI tutor.

{instruction}

{code_info}

Video Content:
{context}

Question: {question}
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def format_answer(question, chunks, mode="detailed"):

    explanation = generate_llm_answer(question, chunks, mode)

    if mode == "short":
        return explanation

    lines = []
    lines.append(f"\nQ: {question}\n")
    lines.append("🧠 Explanation:\n")
    lines.append(explanation + "\n")

    lines.append("📍 Refer in video:\n")

    for c in chunks:
     start = seconds_to_mmss(c["start_time"])
     end = seconds_to_mmss(c["end_time"])

    lines.append(f"- [{start} – {end}] → relevant explanation here")

    return "\n".join(lines)