# ==========================================================
# PRODUCTION-GRADE MULTILINGUAL AI FINANCIAL INSIGHT ENGINE
# Resume-level FinTech Feature
# Supports English, Hindi, Telugu, and 100+ languages
# Does NOT repeat KPI numbers already shown in dashboard
# ==========================================================


def generate_insight(
    income,
    expense,
    savings,
    stability,
    risk_score=0,
    fraud_count=0,
    anomaly_count=0,
    translate_func=None,
    lang="en"
):
    """
    Generates intelligent financial interpretation.
    Does NOT repeat numeric values already shown in UI.
    Provides behavior analysis, risk interpretation, and advice.
    """

    # ======================================================
    # SAFETY CHECKS
    # ======================================================

    try:
        income = float(income)
    except:
        income = 0

    try:
        expense = float(expense)
    except:
        expense = 0

    try:
        savings = float(savings)
    except:
        savings = 0

    try:
        stability = float(stability)
    except:
        stability = 0

    try:
        risk_score = float(risk_score)
    except:
        risk_score = 0

    try:
        fraud_count = int(fraud_count)
    except:
        fraud_count = 0

    try:
        anomaly_count = int(anomaly_count)
    except:
        anomaly_count = 0


    # ======================================================
    # NO DATA CASE
    # ======================================================

    if income <= 0:

        insight = (
            "No financial activity detected. "
            "Upload a financial document to generate intelligent insights."
        )

        if translate_func and lang != "en":
            try:
                insight = translate_func(insight, lang)
            except:
                pass

        return insight


    # ======================================================
    # CALCULATE RATIOS
    # ======================================================

    savings_ratio = (savings / income) * 100 if income > 0 else 0

    expense_ratio = (expense / income) * 100 if income > 0 else 0


    # ======================================================
    # HEALTH ANALYSIS
    # ======================================================

    if savings_ratio >= 60:

        health_msg = (
            "Your financial profile is excellent with strong savings discipline."
        )

        discipline_msg = (
            "You demonstrate highly responsible financial behavior."
        )

    elif savings_ratio >= 40:

        health_msg = (
            "Your financial condition is good with a balanced saving and spending pattern."
        )

        discipline_msg = (
            "Your financial management approach is stable and reliable."
        )

    elif savings_ratio >= 20:

        health_msg = (
            "Your financial condition is moderate and can be improved."
        )

        discipline_msg = (
            "Improving spending control can significantly increase savings."
        )

    else:

        health_msg = (
            "Your financial condition is currently at risk due to low savings."
        )

        discipline_msg = (
            "Improved expense management is strongly recommended."
        )


    # ======================================================
    # RISK ANALYSIS
    # ======================================================

    if risk_score < 30:

        risk_msg = (
            "Your financial risk level is low, indicating safe financial behavior."
        )

    elif risk_score < 60:

        risk_msg = (
            "Your financial risk level is moderate. Monitoring spending is recommended."
        )

    else:

        risk_msg = (
            "Your financial risk level is high. Careful financial monitoring is required."
        )


    # ======================================================
    # STABILITY ANALYSIS
    # ======================================================

    if stability >= 80:

        stability_msg = (
            "Your financial activity is highly stable and consistent."
        )

    elif stability >= 50:

        stability_msg = (
            "Your financial activity shows moderate stability."
        )

    else:

        stability_msg = (
            "Your financial activity is unstable and irregular."
        )


    # ======================================================
    # EXPENSE BEHAVIOR ANALYSIS
    # ======================================================

    if expense_ratio >= 80:

        expense_msg = (
            "Your spending consumes a large portion of your income."
        )

    elif expense_ratio >= 60:

        expense_msg = (
            "Your spending level is moderately high."
        )

    else:

        expense_msg = (
            "Your spending level is well controlled."
        )


    # ======================================================
    # FRAUD ANALYSIS
    # ======================================================

    fraud_msg = ""

    if fraud_count > 0:

        fraud_msg = (
            f"{fraud_count} suspicious transaction(s) were detected. "
            "Reviewing these transactions is recommended."
        )


    # ======================================================
    # ANOMALY ANALYSIS
    # ======================================================

    anomaly_msg = ""

    if anomaly_count > 0:

        anomaly_msg = (
            f"{anomaly_count} unusual transaction pattern(s) were detected."
        )


    # ======================================================
    # FINAL ADVICE GENERATION
    # ======================================================

    if savings_ratio >= 60 and risk_score < 30:

        advice_msg = (
            "Excellent financial discipline. Consider investing to grow wealth further."
        )

    elif savings_ratio >= 40:

        advice_msg = (
            "Your financial condition is strong. Increasing savings can enhance security."
        )

    elif savings_ratio >= 20:

        advice_msg = (
            "Reducing discretionary expenses can improve financial stability."
        )

    else:

        advice_msg = (
            "Improving savings and reducing expenses should be your priority."
        )


    # ======================================================
    # BUILD FINAL INSIGHT
    # ======================================================

    insight_parts = [

        "Financial Analysis:",

        health_msg,

        discipline_msg,

        stability_msg,

        expense_msg,

        risk_msg

    ]


    if fraud_msg:
        insight_parts.append(fraud_msg)


    if anomaly_msg:
        insight_parts.append(anomaly_msg)


    insight_parts.append("Advice:")
    insight_parts.append(advice_msg)


    insight = "\n\n".join(insight_parts)


    # ======================================================
    # MULTILINGUAL TRANSLATION
    # ======================================================

    if translate_func and lang != "en":

        try:
            insight = translate_func(insight, lang)
        except:
            pass


    return insight
