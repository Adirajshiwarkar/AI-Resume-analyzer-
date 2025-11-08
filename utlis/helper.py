import re

def extract_score_from_response(response_text: str):
    """
    Extracts a numeric ATS score (0–100) from the AI's text response robustly.
    Returns None if no valid score is found.
    """
    if not response_text:
        return None

    # ✅ Try to capture patterns like "ATS Score: 85%" or "Score = 90"
    match = re.search(r"(?:ATS\s*Score[:\s=]*)(\d{1,3})", response_text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 0 <= score <= 100:
            return score

    # ✅ If that fails, fall back to finding *all* numbers in text
    numbers = re.findall(r"\d{1,3}", response_text)
    possible_scores = [int(n) for n in numbers if 0 <= int(n) <= 100]

    if possible_scores:
        # return the *highest plausible score* (since ATS usually gives one main score)
        return max(possible_scores)

    # If nothing found
    return None
