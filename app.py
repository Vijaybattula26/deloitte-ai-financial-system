from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    session,
    jsonify,
    flash
)

import pandas as pd
import os
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================================
# IMPORT MODULES
# ==========================================================

from modules.recommendation_engine import RecommendationEngine
from modules.database import (
    init_db,
    create_user,
    get_user_by_email,
    save_user_device,
    is_known_device,
    insert_transaction,
    get_all_transactions,
    delete_transaction,
    clear_user_transactions
)

from modules.ocr_module import extract_text_from_file
from modules.nlp_module import clean_text
from modules.consistency_module import FinancialConsistencyEngine
from modules.savings_module import SavingsAdvisor
from modules.phase2_engine import Phase2IntelligenceEngine
from modules.transparency_engine import TransparencyEngine
from modules.transaction_intelligence import TransactionIntelligenceEngine
from modules.email_otp import send_email_otp, verify_email_otp
from modules.voice_processor import VoiceProcessor


# ==========================================================
# FLASK INIT
# ==========================================================

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "finintel_final_key")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=30)
)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

init_db()

phase2_engine = Phase2IntelligenceEngine()
recommendation_engine = RecommendationEngine()
intelligence_engine = TransactionIntelligenceEngine()
voice_processor = VoiceProcessor()


# ==========================================================
# MULTILINGUAL SUPPORT (ALL 5 LANGUAGES)
# ==========================================================

LANG = {

# ======================================================
# ENGLISH
# ======================================================

"en":{

"title":"Financial Intelligence Dashboard",

"income":"Total Income",
"expense":"Total Expense",
"savings":"Monthly Savings",
"health":"Financial Health",

"history":"Transaction History",
"logout":"Logout",
"toggle_theme":"Toggle Theme",
"mode":"Mode",

"voice_summary":"Hear Financial Summary",
"voice_query":"Ask by Voice",

"charts":"Charts",
"table":"Table",
"Summary Report":"Summary Report",
"recommendations":"Recommendations",

"search":"Search transactions...",

"trusted_recommendations":"Trusted Recommendations",
"verified":"Verified",
"visit_site":"Visit Official Website",

"income_vs_expense":"Income vs Expense",
"category_breakdown":"Category Breakdown",
"monthly_trend":"Monthly Trend",

"description":"Description",
"amount":"Amount",
"type":"Type",
"category":"Category",
"mode":"Mode",
"bank":"Bank",
"extra":"Extra",
"risk":"Risk",
"fraud":"Fraud",
"date":"Date",

"safe":"Safe",
"anomaly":"Anomaly",

"process":"Process",
"product":"Product",
"deducted":"Deducted",
"reason":"Reason",

"download_excel":"Download Excel",
"download_csv":"Download CSV",

"excellent_health":"Excellent Financial Health!",
"saved_amount":"You saved",
"view_recommendations":"View Trusted Recommendations",

"spent":"You spent",

"income_word":"income",
"expense_word":"expense"

},


# ======================================================
# TELUGU
# ======================================================

"te":{

"title":"ఆర్థిక మేధస్సు డాష్‌బోర్డ్",

"income":"మొత్తం ఆదాయం",
"expense":"మొత్తం ఖర్చు",
"savings":"నెలవారీ పొదుపు",
"health":"ఆర్థిక ఆరోగ్యం",

"history":"లావాదేవీ చరిత్ర",
"logout":"లాగ్ అవుట్",
"toggle_theme":"థీమ్ మార్చండి",
"mode":"మోడ్",

"voice_summary":"ఆర్థిక సంగ్రహాన్ని వినండి",
"voice_query":"వాయిస్ ద్వారా అడగండి",

"charts":"చార్ట్స్",
"table":"పట్టిక",
"Summary Report":"సారాంశ నివేదిక",
"recommendations":"సిఫార్సులు",

"search":"లావాదేవీలను వెతకండి...",

"trusted_recommendations":"నమ్మకమైన సిఫార్సులు",
"verified":"ధృవీకరించబడింది",
"visit_site":"అధికారిక వెబ్‌సైట్ చూడండి",

"income_vs_expense":"ఆదాయం vs ఖర్చు",
"category_breakdown":"వర్గ విభజన",
"monthly_trend":"నెలవారీ ట్రెండ్",

"description":"వివరణ",
"amount":"మొత్తం",
"type":"రకం",
"category":"వర్గం",
"mode":"చెల్లింపు విధానం",
"bank":"బ్యాంక్",
"extra":"అదనపు",
"risk":"ప్రమాదం",
"fraud":"మోసం",
"date":"తేదీ",

"safe":"సురక్షితం",
"anomaly":"అసాధారణం",

"process":"ప్రాసెస్",
"product":"ఉత్పత్తి",
"deducted":"తగ్గింపు",
"reason":"కారణం",

"download_excel":"ఎక్సెల్ డౌన్‌లోడ్",
"download_csv":"CSV డౌన్‌లోడ్",

"excellent_health":"అద్భుతమైన ఆర్థిక ఆరోగ్యం!",
"saved_amount":"మీరు సేవ్ చేసినది",
"view_recommendations":"నమ్మకమైన సిఫార్సులు చూడండి",

"spent":"మీరు ఖర్చు చేసినది",

"income_word":"income",
"expense_word":"expense"

},


# ======================================================
# HINDI
# ======================================================

"hi":{

"title":"वित्तीय बुद्धिमत्ता डैशबोर्ड",

"income":"कुल आय",
"expense":"कुल खर्च",
"savings":"मासिक बचत",
"health":"वित्तीय स्वास्थ्य",

"history":"लेन-देन इतिहास",
"logout":"लॉग आउट",
"toggle_theme":"थीम बदलें",
"mode":"मोड",

"voice_summary":"वित्तीय सार सुनें",
"voice_query":"आवाज़ से पूछें",

"charts":"चार्ट",
"table":"तालिका",
"Summary Report":"सारांश रिपोर्ट",
"recommendations":"सिफारिशें",

"search":"लेन-देन खोजें...",

"trusted_recommendations":"विश्वसनीय सिफारिशें",
"verified":"सत्यापित",
"visit_site":"आधिकारिक वेबसाइट देखें",

"income_vs_expense":"आय बनाम खर्च",
"category_breakdown":"श्रेणी विभाजन",
"monthly_trend":"मासिक प्रवृत्ति",

"description":"विवरण",
"amount":"राशि",
"type":"प्रकार",
"category":"श्रेणी",
"mode":"भुगतान तरीका",
"bank":"बैंक",
"extra":"अतिरिक्त",
"risk":"जोखिम",
"fraud":"धोखाधड़ी",
"date":"तारीख",

"safe":"सुरक्षित",
"anomaly":"असामान्य",

"process":"प्रक्रिया",
"product":"उत्पाद",
"deducted":"कटा हुआ",
"reason":"कारण",

"download_excel":"एक्सेल डाउनलोड",
"download_csv":"CSV डाउनलोड",

"excellent_health":"उत्कृष्ट वित्तीय स्वास्थ्य!",
"saved_amount":"आपने बचाया",
"view_recommendations":"विश्वसनीय सिफारिशें देखें",

"spent":"आपने खर्च किया",

"income_word":"income",
"expense_word":"expense"

},


# ======================================================
# TAMIL
# ======================================================

"ta":{

"title":"நிதி நுண்ணறிவு டாஷ்போர்டு",

"income":"மொத்த வருமானம்",
"expense":"மொத்த செலவு",
"savings":"மாத சேமிப்பு",
"health":"நிதி நிலை",

"history":"பரிவர்த்தனை வரலாறு",
"logout":"வெளியேறு",
"toggle_theme":"தீம் மாற்று",
"mode":"முறை",

"voice_summary":"நிதி சுருக்கத்தை கேளுங்கள்",
"voice_query":"குரலில் கேளுங்கள்",

"charts":"வரைபடங்கள்",
"table":"அட்டவணை",
"Summary Report":"சுருக்க அறிக்கை",
"recommendations":"பரிந்துரைகள்",

"search":"பரிவர்த்தனைகளை தேடுங்கள்...",

"trusted_recommendations":"நம்பகமான பரிந்துரைகள்",
"verified":"சரிபார்க்கப்பட்டது",
"visit_site":"அதிகாரப்பூர்வ இணையதளம்",

"income_vs_expense":"வருமானம் vs செலவு",
"category_breakdown":"வகை பிரிப்பு",
"monthly_trend":"மாத போக்கு",

"description":"விளக்கம்",
"amount":"தொகை",
"type":"வகை",
"category":"வகை",
"mode":"கட்டணம் முறை",
"bank":"வங்கி",
"extra":"கூடுதல்",
"risk":"ஆபத்து",
"fraud":"மோசடி",
"date":"தேதி",

"safe":"பாதுகாப்பான",
"anomaly":"அசாதாரணம்",

"process":"செயல்முறை",
"product":"தயாரிப்பு",
"deducted":"கழிக்கப்பட்டது",
"reason":"காரணம்",

"download_excel":"எக்செல் பதிவிறக்கம்",
"download_csv":"CSV பதிவிறக்கம்",

"excellent_health":"சிறந்த நிதி நிலை!",
"saved_amount":"நீங்கள் சேமித்தது",
"view_recommendations":"நம்பகமான பரிந்துரைகள் பார்க்க",

"spent":"நீங்கள் செலவிட்டது",

"income_word":"income",
"expense_word":"expense"

},


# ======================================================
# KANNADA
# ======================================================

"kn":{

"title":"ಆರ್ಥಿಕ ಬುದ್ಧಿವಂತಿಕೆ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",

"income":"ಒಟ್ಟು ಆದಾಯ",
"expense":"ಒಟ್ಟು ಖರ್ಚು",
"savings":"ಮಾಸಿಕ ಉಳಿವು",
"health":"ಆರ್ಥಿಕ ಆರೋಗ್ಯ",

"history":"ವಹಿವಾಟು ಇತಿಹಾಸ",
"logout":"ಲಾಗ್ ಔಟ್",
"toggle_theme":"ಥೀಮ್ ಬದಲಿಸಿ",
"mode":"ಮೋಡ್",

"voice_summary":"ಆರ್ಥಿಕ ಸಾರಾಂಶವನ್ನು ಕೇಳಿ",
"voice_query":"ಧ್ವನಿಯಿಂದ ಕೇಳಿ",

"charts":"ಚಾರ್ಟ್‌ಗಳು",
"table":"ಪಟ್ಟಿ",
"Summary Report":"ಸಾರಾಂಶ ನಿವೇದಿಕ",
"recommendations":"ಶಿಫಾರಸುಗಳು",

"search":"ವಹಿವಾಟುಗಳನ್ನು ಹುಡುಕಿ...",

"trusted_recommendations":"ವಿಶ್ವಾಸಾರ್ಹ ಶಿಫಾರಸುಗಳು",
"verified":"ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
"visit_site":"ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್",

"income_vs_expense":"ಆದಾಯ vs ಖರ್ಚು",
"category_breakdown":"ವರ್ಗ ವಿಭಾಗ",
"monthly_trend":"ಮಾಸಿಕ ಪ್ರವೃತ್ತಿ",

"description":"ವಿವರಣೆ",
"amount":"ಮೊತ್ತ",
"type":"ಪ್ರಕಾರ",
"category":"ವರ್ಗ",
"mode":"ಪಾವತಿ ವಿಧಾನ",
"bank":"ಬ್ಯಾಂಕ್",
"extra":"ಹೆಚ್ಚುವರಿ",
"risk":"ಅಪಾಯ",
"fraud":"ವಂಚನೆ",
"date":"ದಿನಾಂಕ",

"safe":"ಸುರಕ್ಷಿತ",
"anomaly":"ಅಸಾಮಾನ್ಯ",

"process":"ಪ್ರಕ್ರಿಯೆ",
"product":"ಉತ್ಪನ್ನ",
"deducted":"ಕಡಿತ",
"reason":"ಕಾರಣ",

"download_excel":"ಎಕ್ಸೆಲ್ ಡೌನ್‌ಲೋಡ್",
"download_csv":"CSV ಡೌನ್‌ಲೋಡ್",

"excellent_health":"ಅತ್ಯುತ್ತಮ ಆರ್ಥಿಕ ಆರೋಗ್ಯ!",
"saved_amount":"ನೀವು ಉಳಿಸಿದ ಮೊತ್ತ",
"view_recommendations":"ವಿಶ್ವಾಸಾರ್ಹ ಶಿಫಾರಸುಗಳನ್ನು ನೋಡಿ",

"spent":"ನೀವು ಖರ್ಚು ಮಾಡಿದುದು",

"income_word":"income",
"expense_word":"expense"

}

}


def get_ui():
    return LANG.get(session.get("lang","en"), LANG["en"])


# ==========================================================
# VALIDATION
# ==========================================================

def is_valid_statement(text):

    if not text:
        return False

    text = text.lower()

    keywords = [
        "debit","credit","withdrawal","deposit",
        "paid","deducted","salary",
        "interest","upi","atm","gst"
    ]

    score = 0

    for word in keywords:
        if word in text:
            score += 1

    return score >= 2


def login_required():

    user_id = session.get("user_id")

    if not user_id:
        return False

    return True

# ==========================================================
# VOICE QUERY INTERPRETER
# ==========================================================

def interpret_voice_query(text, user_id):

    df = pd.DataFrame(get_all_transactions(user_id))

    if df.empty:
        return "No financial data available."

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    query = text.lower()

    # INCOME
    if any(word in query for word in ["income", "earn", "salary"]):
    
        total_income = df[df["type"]=="income"]["amount"].sum()

        return f"Your total income is ₹ {int(total_income)}"


    # EXPENSE
    elif any(word in query for word in ["expense", "expenses", "spend", "spent", "expensive"]):

        total_expense = df[df["type"]=="expense"]["amount"].sum()

        return f"Your total expenses are ₹ {int(total_expense)}"


    # SAVINGS
    elif "saving" in query or "savings" in query:

        income = df[df["type"]=="income"]["amount"].sum()
        expense = df[df["type"]=="expense"]["amount"].sum()
        savings = income - expense

        return f"Your total savings are ₹ {int(savings)}"


    else:
        return "Sorry, I could not understand your financial query."

    # History query
    if "transaction" in query or "history" in query:

        return f"You have {len(df)} transactions recorded."

    return "Sorry, I could not understand your financial query."


# ==========================================================
# LANGUAGE SWITCH
# ==========================================================

@app.route("/set_language", methods=["POST"])
def set_language():

    lang = request.form.get("language","en")

    if lang in LANG:
        session["lang"] = lang

    return redirect(request.referrer or "/dashboard")


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    if login_required():
        return redirect("/dashboard")

    return render_template("login_signup.html")


# ==========================================================
# AUTH LOGIN / SIGNUP
# ==========================================================

@app.route("/auth/email", methods=["POST"])
def auth_email():

    email = request.form.get("email","").strip()
    password = request.form.get("password","").strip()
    device_id = request.form.get("device_id", "unknown_device")
    device_name = request.form.get("device_name", "Unknown Device")

    if not email or not password:
        return render_template(
            "login_signup.html",
            error="Email and password required."
        )

    user = get_user_by_email(email)

    if user:

        if not check_password_hash(user["password_hash"], password):

            return render_template(
                "login_signup.html",
                error="Invalid password."
            )

    else:

        hashed = generate_password_hash(password)

        create_user(email=email, password_hash=hashed)

        user = get_user_by_email(email)

    # ======================================================
    # DEVICE TRUST CHECK
    # ======================================================

    if is_known_device(user["id"], device_id):

        session["user_id"] = user["id"]
        session.permanent = True

        return redirect("/dashboard")

    # ======================================================
    # SEND OTP FOR NEW DEVICE
    # ======================================================

    send_email_otp(email, device_id)
    print("OTP sent to:", email)

    return render_template(
        "verify_emailotp.html",
        email=email
    )
# ==========================================================
# VERIFY EMAIL OTP
# ==========================================================

@app.route("/auth/verify_email", methods=["POST"])
def verify_email():

    email = request.form.get("email")
    otp = request.form.get("otp")
    device_id = request.form.get("device_id")
    device_name = request.form.get("device_name")

    success, message = verify_email_otp(email, otp)

    if not success:

        return render_template(
            "verify_emailotp.html",
            email=email,
            error=message
        )

    user = get_user_by_email(email)

    session["user_id"] = user["id"]
    session.permanent = True

    if not is_known_device(user["id"], device_id):
        save_user_device(user["id"], device_id, device_name)

    return redirect("/dashboard")

    


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect("/")

    ui = get_ui()
    user_id = session["user_id"]

    transactions = get_all_transactions(user_id) or []
    df = pd.DataFrame(transactions)

    if df.empty:
        return render_template(
            "index.html",
            ui=ui,
            income=0,
            expense=0,
            savings={"monthly_savings":0,"financial_health":"N/A"},
            tables=[],
            monthly_labels=[],
            monthly_income=[],
            monthly_expense=[],
            recommendations=[],
            doc_mode="Personal Budget"
        )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date"])

    income = float(df[df["type"]=="income"]["amount"].sum())
    expense = float(df[df["type"]=="expense"]["amount"].sum())

    transactions = df.to_dict("records")

    advisor = SavingsAdvisor()
    advisor.add_transactions(transactions)
    savings = advisor.advisory_report()

    recommendations = recommendation_engine.get_recommendations_for_ui(
        savings.get("monthly_savings",0)
    )

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_income = df[df["type"]=="income"].groupby("month")["amount"].sum()
    monthly_expense = df[df["type"]=="expense"].groupby("month")["amount"].sum()

    months = sorted(df["month"].unique())

    monthly_income_list = [float(monthly_income.get(m,0)) for m in months]
    monthly_expense_list = [float(monthly_expense.get(m,0)) for m in months]

    return render_template(
        "index.html",
        ui=ui,
        income=round(income,2),
        expense=round(expense,2),
        savings=savings,
        tables=transactions,
        monthly_labels=months,
        monthly_income=monthly_income_list,
        monthly_expense=monthly_expense_list,
        recommendations=recommendations,
        doc_mode="Personal Budget"
    )


# ==========================================================
# HISTORY
# ==========================================================

@app.route("/history")
def history():

    if not login_required():
        return redirect("/")

    user_id = session["user_id"]

    df = pd.DataFrame(get_all_transactions(user_id))

    if df.empty:

        return render_template(
            "history.html",
            ui=get_ui(),
            transactions=[],
            income=0,
            expense=0
        )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    df = df.dropna(subset=["date"])

    income = float(df[df["type"] == "income"]["amount"].sum())
    expense = float(df[df["type"] == "expense"]["amount"].sum())

    df = df.sort_values("date", ascending=False)

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    return render_template(
        "history.html",
        ui=get_ui(),
        transactions=df.to_dict("records"),
        income=round(income,2),
        expense=round(expense,2)
    )


# ==========================================================
# DELETE
# ==========================================================

@app.route("/delete_transaction/<int:tx_id>")
def delete_tx(tx_id):

    if not login_required():
        return redirect("/")

    delete_transaction(tx_id, session["user_id"])

    return redirect("/history")


# ==========================================================
# PROCESS DOCUMENT
# ==========================================================

@app.route("/process", methods=["POST"])
def process():

    if not login_required():
        return redirect("/")

    selected_lang = request.form.get("language")

    if selected_lang in LANG:
        session["lang"] = selected_lang

    ui = get_ui()

    user_id = session["user_id"]

    text_note = request.form.get("text_note","")

    files = request.files.getlist("documents")

    extracted_text = ""

    for file in files:

        if file and file.filename:

            text, _ = extract_text_from_file(file)

            if text and len(text.strip()) > 20:
                extracted_text += "\n" + text

    text = text_note.strip() if text_note else extracted_text.strip()

    if not text:

        flash("No readable financial data found.")

        return redirect("/dashboard")

    if not is_valid_statement(text):
        flash("Invalid or unsupported financial file.")
        return redirect("/dashboard")

    cleaned_text = clean_text(text)

    transparency_engine = TransparencyEngine()

    raw_data = transparency_engine.parse(cleaned_text)

    if not raw_data:
        flash("No valid transactions found.")
        return redirect("/dashboard")

    # clear_user_transactions(user_id)

    for item in raw_data:

        try:

            label, confidence = phase2_engine.predict(item)

            item["type"] = label
            item["confidence"] = confidence

        except:

            item["type"] = item.get("type","expense")

        item = intelligence_engine.analyze(item)

        insert_transaction(item, user_id)

    df = pd.DataFrame(get_all_transactions(user_id))

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    df = df.dropna(subset=["date"])


    start_date = request.form.get("date_from")
    end_date = request.form.get("date_to")

    if start_date and end_date:

        df = df[
            (df["date"] >= pd.to_datetime(start_date)) &
            (df["date"] <= pd.to_datetime(end_date))
        ]


    df.to_csv(
        os.path.join(OUTPUT_DIR,"financial_report.csv"),
        index=False
    )

    df.to_excel(
        os.path.join(OUTPUT_DIR,"financial_report.xlsx"),
        index=False
    )


    income = float(df[df["type"] == "income"]["amount"].sum())

    expense = float(df[df["type"] == "expense"]["amount"].sum())


    filtered_transactions = df.to_dict("records")


    advisor = SavingsAdvisor()

    advisor.add_transactions(filtered_transactions)

    savings = advisor.advisory_report()


    consistency = FinancialConsistencyEngine()

    consistency.add_transactions(filtered_transactions)

    stability = consistency.stability_score()


    recommendations = recommendation_engine.get_recommendations_for_ui(
        savings.get("monthly_savings",0)
    )


    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_income = df[df["type"]=="income"].groupby("month")["amount"].sum()

    monthly_expense = df[df["type"]=="expense"].groupby("month")["amount"].sum()

    months = sorted(df["month"].unique())

    monthly_income_list = [
        float(monthly_income.get(m,0)) for m in months
    ]

    monthly_expense_list = [
        float(monthly_expense.get(m,0)) for m in months
    ]


    return render_template(
        "result.html",
        ui=ui,
        income=round(income,2),
        expense=round(expense,2),
        savings=savings,
        stability=stability,
        tables=filtered_transactions,
        doc_mode="Personal Budget",
        monthly_labels=months,
        monthly_income=monthly_income_list,
        monthly_expense=monthly_expense_list,
        recommendations=recommendations
    )


# ==========================================================
# DOWNLOAD
# ==========================================================

@app.route("/download/csv")
def download_csv():

    return send_from_directory(
        OUTPUT_DIR,
        "financial_report.csv",
        as_attachment=True
    )


@app.route("/download/excel")
def download_excel():

    return send_from_directory(
        OUTPUT_DIR,
        "financial_report.xlsx",
        as_attachment=True
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================================================
# RUN
# ==========================================================

# ==========================================================
# VOICE QUERY ROUTE
# ==========================================================

@app.route("/voice_query", methods=["POST"])
def voice_query():

    if not login_required():
        return jsonify({
            "success": False,
            "error": "User not logged in"
        }), 401

    user_id = session["user_id"]

    try:

        result = voice_processor.listen()

        if not result or not result.get("success"):

            return jsonify({
                "success": False,
                "error": result.get("error", "Voice recognition failed")
            })

        voice_text = result.get("text","")

        if not voice_text:
            return jsonify({
                "success": False,
                "error": "No speech detected"
            })

        answer = interpret_voice_query(voice_text, user_id)

        return jsonify({
            "success": True,
            "query": voice_text,
            "response": answer
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)