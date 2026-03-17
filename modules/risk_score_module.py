# ==========================================================
# AI FINANCIAL RISK SCORE MODULE
# Combines anomaly detection, fraud detection, and spending behavior
# Outputs final risk score (0 to 100)
# ==========================================================

class RiskScorer:

    def __init__(self):

        # weight configuration
        self.anomaly_weight = 40
        self.fraud_weight = 40
        self.expense_weight = 20


    # ======================================================
    # MAIN RISK SCORE FUNCTION
    # ======================================================

    def calculate(self, transactions, stability_score=100):

        if not transactions:

            return {
                "risk_score": 0,
                "risk_level": "Safe",
                "anomaly_count": 0,
                "fraud_count": 0
            }

        total = len(transactions)

        anomaly_count = sum(
            1 for t in transactions
            if t.get("anomaly", False)
        )

        fraud_count = sum(
            1 for t in transactions
            if t.get("fraud", False)
        )

        expense_count = sum(
            1 for t in transactions
            if t.get("type") == "expense"
        )

        # ==================================================
        # COMPONENT SCORES
        # ==================================================

        anomaly_score = (
            anomaly_count / total
        ) * self.anomaly_weight

        fraud_score = (
            fraud_count / total
        ) * self.fraud_weight

        expense_ratio = expense_count / total

        expense_score = expense_ratio * self.expense_weight

        stability_penalty = (100 - stability_score) * 0.2

        # ==================================================
        # FINAL RISK SCORE
        # ==================================================

        risk_score = (
            anomaly_score
            + fraud_score
            + expense_score
            + stability_penalty
        )

        risk_score = min(100, max(0, round(risk_score, 2)))

        # ==================================================
        # RISK LEVEL CLASSIFICATION
        # ==================================================

        if risk_score <= 20:
            level = "Safe"

        elif risk_score <= 40:
            level = "Low Risk"

        elif risk_score <= 60:
            level = "Moderate Risk"

        elif risk_score <= 80:
            level = "High Risk"

        else:
            level = "Critical Risk"

        return {

            "risk_score": risk_score,
            "risk_level": level,
            "anomaly_count": anomaly_count,
            "fraud_count": fraud_count,
            "total_transactions": total

        }


    # ======================================================
    # TEXT SUMMARY (for UI)
    # ======================================================

    def generate_summary(self, risk_data):

        score = risk_data["risk_score"]
        level = risk_data["risk_level"]

        if level == "Safe":

            message = \
                "Your account activity appears safe and normal."

        elif level == "Low Risk":

            message = \
                "Minor unusual patterns detected. Monitor regularly."

        elif level == "Moderate Risk":

            message = \
                "Suspicious patterns detected. Review transactions."

        elif level == "High Risk":

            message = \
                "High risk activity detected. Immediate attention required."

        else:

            message = \
                "Critical fraud risk detected. Take immediate action."

        return {

            "score": score,
            "level": level,
            "message": message

        }
