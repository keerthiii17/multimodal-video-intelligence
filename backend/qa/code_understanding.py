def detect_language(code: str) -> str:
    if "public static void" in code:
        return "Java"
    elif "def " in code:
        return "Python"
    elif "#include" in code:
        return "C++"
    else:
        return "Unknown"