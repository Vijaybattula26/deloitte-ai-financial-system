import re

COMMON_OCR_FIXES = {
    "seivioe": "service",
    "peiod": "period",
    "renatl": "rental",
    "elecricity": "electricity",
    "insurence": "insurance"
}

def correct_ocr_errors(text):
    text = text.lower()
    for wrong, correct in COMMON_OCR_FIXES.items():
        text = re.sub(rf"\b{wrong}\b", correct, text)
    return text
