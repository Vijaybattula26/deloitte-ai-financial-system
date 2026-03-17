import re

# ==========================================================
# KEYWORDS
# ==========================================================

INCOME_KEYWORDS = [
    "salary", "credit", "income", "received",
    "refund", "bonus", "payment received"
]

EXPENSE_KEYWORDS = [
    "bill", "rent", "grocery", "purchase", "debit",
    "fee", "tax", "electricity", "water", "internet",
    "shopping", "fuel", "expense", "paid"
]

# Units to ignore
IGNORE_UNITS = [
    "mg", "mm", "%", "lbs", "kg", "ml", "cm",
    "lot", "sample", "no.", "date"
]

# ==========================================================
# CLEAN LINE
# ==========================================================

def is_valid_money(amount):

    # Reject very small values
    if amount < 10:
        return False

    # Reject unrealistic large values
    if amount > 10000000:
        return False

    return True


def contains_ignore_units(text):

    text = text.lower()

    for unit in IGNORE_UNITS:
        if unit in text:
            return True

    return False


# ==========================================================
# MAIN EXTRACTION FUNCTION
# ==========================================================

def extract_financial_data(text):

    lines = text.split("\n")

    income_total = 0
    expense_total = 0
    transactions = []

    money_pattern = re.compile(
        r'(₹\s?\d[\d,]*\.?\d*|\b\d{2,9}\.?\d{0,2}\b)'
    )

    for line in lines:

        lower_line = line.lower()

        if contains_ignore_units(lower_line):
            continue

        matches = money_pattern.findall(line)

        if not matches:
            continue

        for match in matches:

            # Remove currency symbol and commas
            clean_amount = match.replace("₹", "").replace(",", "").strip()

            try:
                amount = float(clean_amount)
            except:
                continue

            if not is_valid_money(amount):
                continue

            # Detect income or expense
            if any(word in lower_line for word in INCOME_KEYWORDS):
                income_total += amount
                transactions.append(("Income", amount, line.strip()))

            elif any(word in lower_line for word in EXPENSE_KEYWORDS):
                expense_total += amount
                transactions.append(("Expense", amount, line.strip()))

            else:
                # Default rule: treat as expense
                expense_total += amount
                transactions.append(("Expense", amount, line.strip()))

    return income_total, expense_total, transactions