import re

def clean_text(text: str) -> str:
    """
    Safe text cleaner for financial parsing.
    Preserves:
    - Dates (01-06-2026)
    - Slash dates (01/06/2026)
    - Spaces
    - Line structure
    - Decimal values
    """

    if not text:
        return ""

    # Normalize newlines
    text = text.replace("\r", "\n")

    # Preserve letters, numbers, spaces, dash, slash, dot, newline
    text = re.sub(r"[^a-zA-Z0-9\s\-/\.]", "", text)

    # Remove extra spaces (but keep new lines)
    text = re.sub(r"[ ]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()