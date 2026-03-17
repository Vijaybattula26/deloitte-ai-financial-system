"""
=========================================================
ENTERPRISE MULTI-LANGUAGE SYSTEM
Supports: English, Hindi, Telugu
Fully compatible with your dashboard
=========================================================
"""

LANG = {

    # =====================================================
    # ENGLISH
    # =====================================================
    "en": {

        "title": "Financial Intelligence Dashboard",

        "income": "Total Income",
        "expense": "Total Expense",
        "savings": "Monthly Savings",

        "health": "Financial Health Status",

        "ai_insight": "AI Financial Insight",

        "stability": "Stability Score",

        "desc": "Description",
        "amount": "Amount",
        "type": "Type",

        "income_word": "Income",
        "expense_word": "Expense",

        "used": "Used",
        "remaining": "Remaining",

        "summary": "Summary",

        "total_income": "Total Income",
        "total_expense": "Total Expense",

        "savings_percentage": "Savings Percentage",

        "mode": "Mode",

        "no_data": "No financial data detected",

        # =================================================
        # FINANCIAL HEALTH VALUES (CRITICAL FIX)
        # =================================================

        "Excellent": "Excellent",
        "Good": "Good",
        "Moderate": "Moderate",
        "At Risk": "At Risk",

        # Mode types
        "personal_budget": "Personal Budget",
        "bank_statement": "Bank Statement",
        "financial_statement": "Financial Statement"

    },


    # =====================================================
    # HINDI
    # =====================================================
    "hi": {

        "title": "वित्तीय बुद्धिमत्ता डैशबोर्ड",

        "income": "कुल आय",
        "expense": "कुल खर्च",
        "savings": "मासिक बचत",

        "health": "वित्तीय स्थिति",

        "ai_insight": "AI वित्तीय विश्लेषण",

        "stability": "स्थिरता स्कोर",

        "desc": "विवरण",
        "amount": "राशि",
        "type": "प्रकार",

        "income_word": "आय",
        "expense_word": "खर्च",

        "used": "उपयोग",
        "remaining": "शेष",

        "summary": "सारांश",

        "total_income": "कुल आय",
        "total_expense": "कुल खर्च",

        "savings_percentage": "बचत प्रतिशत",

        "mode": "मोड",

        "no_data": "कोई वित्तीय डेटा नहीं मिला",

        # =================================================
        # FINANCIAL HEALTH VALUES
        # =================================================

        "Excellent": "उत्कृष्ट",
        "Good": "अच्छा",
        "Moderate": "मध्यम",
        "At Risk": "जोखिम में",

        # Mode types
        "personal_budget": "व्यक्तिगत बजट",
        "bank_statement": "बैंक स्टेटमेंट",
        "financial_statement": "वित्तीय विवरण"

    },


    # =====================================================
    # TELUGU
    # =====================================================
    "te": {

        "title": "ఆర్థిక మేధస్సు డ్యాష్‌బోర్డ్",

        "income": "మొత్తం ఆదాయం",
        "expense": "మొత్తం ఖర్చు",
        "savings": "నెలవారీ పొదుపు",

        "health": "ఆర్థిక స్థితి",

        "ai_insight": "AI ఆర్థిక విశ్లేషణ",

        "stability": "స్థిరత్వ స్కోర్",

        "desc": "వివరణ",
        "amount": "మొత్తం",
        "type": "రకం",

        "income_word": "ఆదాయం",
        "expense_word": "ఖర్చు",

        "used": "వినియోగం",
        "remaining": "మిగిలినది",

        "summary": "సారాంశం",

        "total_income": "మొత్తం ఆదాయం",
        "total_expense": "మొత్తం ఖర్చు",

        "savings_percentage": "పొదుపు శాతం",

        "mode": "మోడ్",

        "no_data": "ఆర్థిక డేటా కనబడలేదు",

        # =================================================
        # FINANCIAL HEALTH VALUES
        # =================================================

        "Excellent": "అద్భుతం",
        "Good": "మంచిది",
        "Moderate": "సాధారణం",
        "At Risk": "ప్రమాదంలో",

        # Mode types
        "personal_budget": "వ్యక్తిగత బడ్జెట్",
        "bank_statement": "బ్యాంక్ స్టేట్మెంట్",
        "financial_statement": "ఆర్థిక నివేదిక"

    }

}


# ==========================================================
# SAFE HELPER FUNCTION
# ==========================================================

def get_text(key, lang="en"):

    if lang not in LANG:
        lang = "en"

    return LANG[lang].get(key, key)
