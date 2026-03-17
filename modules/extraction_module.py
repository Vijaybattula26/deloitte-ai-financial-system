import re
from datetime import datetime

# ==========================================================
# GPT-LEVEL ENTERPRISE FINANCIAL EXTRACTION ENGINE
# HARDENED VERSION – ERROR SAFE BUILD (FINAL FIXED VERSION)
# ==========================================================


# ==========================================================
# DOCUMENT TYPE DETECTION
# ==========================================================

STATEMENT_KEYWORDS = [
    "financial statement",
    "bank statement",
    "account statement",
    "statement period",
    "account number",
    "detailed statement"
]


def detect_document_type(text):

    text_lower = text.lower()

    for keyword in STATEMENT_KEYWORDS:
        if keyword in text_lower:
            return "bank_statement"

    return "personal_budget"


# ==========================================================
# KEYWORDS
# ==========================================================

INCOME_KEYWORDS = [
    "income",
    "credited",
    "credit",
    "salary",
    "bonus",
    "interest received",
    "freelance",
    "consulting",
    "payment received"
]


EXPENSE_KEYWORDS = [
    "expense",
    "payment",
    "bill",
    "emi",
    "rent",
    "fuel",
    "subscription",
    "insurance",
    "shopping",
    "medical",
    "electricity",
    "dining",
    "restaurant",
    "food",
    "grocery",
    "internet",
    "netflix",
    "entertainment"
]


# ==========================================================
# IGNORE WORDS
# ==========================================================

IGNORE_WORDS = [
    "total income",
    "total expense",
    "net savings",
    "financial recommendations",
    "ai-based financial analysis",
    "increase emergency fund",
    "diversify investment",
    "track variable expenses",
    "maintain consistent savings",
    "optimize recurring subscriptions",
    "savings ratio",
    "metric value",
    "summary",
    "analysis"
]


# ==========================================================
# AMOUNT EXTRACTION (HARDENED)
# ==========================================================

def extract_amount(line):

    matches = re.findall(
        r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d+(?:\.\d+)?\b",
        line
    )

    if not matches:
        return None

    value = matches[-1].replace(",", "")

    try:
        amount = float(value)

        if amount <= 0 or amount > 1_000_000_000:
            return None

        # 🚫 Reject year-like values
        if 1900 <= amount <= 2100:
            return None

        return amount

    except:
        return None


# ==========================================================
# DATE EXTRACTION
# ==========================================================

def extract_date(line):

    patterns = [
        r"\d{2}-\d{2}-\d{4}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{8}"
    ]

    for pattern in patterns:
        match = re.search(pattern, line)

        if match:
            raw = match.group()

            if len(raw) == 8:
                return f"{raw[:2]}-{raw[2:4]}-{raw[4:]}"

            return raw.replace("/", "-")

    return None


# ==========================================================
# TYPE EXTRACTION
# ==========================================================

def extract_type(line):

    line_lower = line.lower()

    if line_lower.endswith(" income"):
        return "income"

    if line_lower.endswith(" expense"):
        return "expense"

    for keyword in INCOME_KEYWORDS:
        if keyword in line_lower:
            return "income"

    for keyword in EXPENSE_KEYWORDS:
        if keyword in line_lower:
            return "expense"

    return None


# ==========================================================
# DESCRIPTION CLEANER
# ==========================================================

def clean_description(line, amount):

    line = re.sub(r"\d{2}[-/]\d{2}[-/]\d{4}", "", line)
    line = re.sub(r"\d{8}", "", line)

    if amount:
        line = re.sub(str(int(amount)), "", line)

    line = re.sub(r"\b(income|expense)\b", "", line, flags=re.I)
    line = re.sub(r"[|■•]", "", line)
    line = re.sub(r"\b(null|none|nan|n)\b", "", line, flags=re.I)
    line = re.sub(r"\s+", " ", line)

    return line.strip().title()


# ==========================================================
# INVALID LINE FILTER (UPGRADED)
# ==========================================================

def is_invalid_line(line):

    lower = line.lower().strip()

    # 🚫 Ignore summary totals (strong rule)
    if lower.startswith("total"):
        return True

    if lower.startswith("net"):
        return True

    # Ignore predefined words
    for word in IGNORE_WORDS:
        if word in lower:
            return True

    # Ignore report headers
    if lower.startswith("financial"):
        return True

    # Ignore standalone charge lines
    standalone_charge_keywords = [
        "gst",
        "service charge",
        "processing fee",
        "platform fee",
        "convenience fee",
        "bank surcharge"
    ]

    for keyword in standalone_charge_keywords:
        if lower.startswith(keyword):
            return True

    # Ignore long non-transaction sentences
    if len(line.split()) > 8:
        return True

    return False


# ==========================================================
# DUPLICATE CHECK
# ==========================================================

def is_duplicate(tx, seen):

    key = (
        tx["date"],
        tx["description"],
        tx["amount"],
        tx["type"]
    )

    if key in seen:
        return True

    seen.add(key)
    return False


# ==========================================================
# MAIN EXTRACTION ENGINE (FINAL SAFE VERSION)
# ==========================================================

def extract_financial_data_phase2(text):

    doc_type = detect_document_type(text)
    lines = text.split("\n")

    transactions = []
    seen = set()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # 🔥 ENTERPRISE FIX:
        # Only process lines that START with a valid date
        if not re.match(r"\d{2}[-/]\d{2}[-/]\d{4}", line):
            continue

        if is_invalid_line(line):
            continue

        amount = extract_amount(line)

        if amount is None:
            continue

        if amount < 10:
            continue

        tx_type = extract_type(line)

        if tx_type is None:
            fallback_keywords = [
                "bill", "rent", "emi", "shopping",
                "subscription", "fuel", "insurance"
            ]
            if not any(word in line.lower() for word in fallback_keywords):
                continue
            tx_type = "expense"

        date = extract_date(line)

        if not date:
            continue

        description = clean_description(line, amount)

        if not description:
            continue

        tx = {
            "date": date,
            "description": description,
            "amount": amount,
            "type": tx_type,
            "category": "General"
        }

        if is_duplicate(tx, seen):
            continue

        transactions.append(tx)

    return {
        "mode": doc_type,
        "data": transactions
    }