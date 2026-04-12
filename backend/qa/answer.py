import requests
from backend.qa.code_understanding import detect_language
from backend.cache.answer_cache import get_cached_answer, set_cached_answer


def seconds_to_mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def generate_llm_answer(question, chunks, mode):

    if not chunks:
        return "❌ This topic is not discussed in the video."

    # ---------- BUILD CONTEXT ----------
    context_parts = []

    for c in chunks[:2]:   # limit = faster
        text = ""
        if c.get("speech"):
            text += c["speech"][:150] + " "
        if c.get("slide_text"):
            text += c["slide_text"][:150] + " "
        if c.get("code_text"):
            text += c["code_text"][:150]
        text = text.replace("\n", " ").strip()

        context_parts.append(text.strip())

    context = "\n".join(context_parts)

    # ---------- CODE DETECTION ----------
    code_texts = [c.get("code_text") for c in chunks if c.get("code_text")]

    code_info = ""
    if code_texts:
        lang = detect_language(code_texts[0])
        code_info = f"\nDetected Code Language: {lang}\n"

    # ---------- MODE ----------
    if mode == "short":
        instruction = "Answer in ONE LINE only."
    else:
        instruction = "Explain clearly with intuition."

    prompt = f"""
You are an AI tutor.

STRICT RULES:
- ONLY use the provided video content
- If the answer is NOT clearly present → say:
  "This is not clearly explained in the video."
- DO NOT generate code unless explicitly present
- DO NOT invent examples
- DO NOT hallucinate

Answer based only on this:

Video Content:
{context}

Question: {question}
"""

    # ---------- CACHE ----------
    cache_key = f"{question}_{mode}_{chunks[0]['start_time']}"

    cached = get_cached_answer(cache_key)
    if cached:
        return cached

    # ---------- LLM CALL ----------
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "tinyllama",   # fast
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
    except Exception as e:
        return f"⚠️ LLM connection error: {str(e)}"

    # ---------- RESPONSE ----------
    try:
        data = response.json()
        result = data.get("response")

        if not result:
            return "⚠️ Empty response from model"

        set_cached_answer(cache_key, result)

        return result

    except Exception as e:
        return f"⚠️ Error parsing response: {str(e)}"


def format_answer(question, chunks, mode="detailed"):

    if not chunks:
        return "❌ This topic is not discussed in the video."

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
        lines.append(f"- [{start} – {end}]")

    return "\n".join(lines)