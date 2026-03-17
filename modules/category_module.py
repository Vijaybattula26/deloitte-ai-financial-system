# ==========================================================
# TRANSACTION CATEGORY CLASSIFICATION ENGINE
# ==========================================================

CATEGORY_RULES = {

    # Income
    "salary": "Salary",
    "interest": "Interest",
    "refund": "Refund",
    "subsidy": "Subsidy",
    "credit": "Income",

    # Utilities
    "electricity": "Utilities",
    "internet": "Utilities",
    "wifi": "Utilities",
    "bill": "Utilities",

    # Transportation
    "fuel": "Transportation",
    "petrol": "Transportation",
    "diesel": "Transportation",

    # Cash
    "atm": "Cash Withdrawal",
    "withdraw": "Cash Withdrawal",

    # Shopping
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "purchase": "Shopping",

    # Food
    "restaurant": "Food",
    "swiggy": "Food",
    "zomato": "Food",

    # Insurance
    "insurance": "Insurance",

    # Entertainment
    "subscription": "Entertainment",
    "netflix": "Entertainment",
    "spotify": "Entertainment",

    # Bank
    "charges": "Bank Charges",

    # Transfer
    "to self": "Self Transfer"

}


# ==========================================================
# CATEGORY DETECTION FUNCTION
# ==========================================================

def detect_category(description):

    description_lower = description.lower()

    for keyword, category in CATEGORY_RULES.items():

        if keyword in description_lower:

            return category

    return "Others"
