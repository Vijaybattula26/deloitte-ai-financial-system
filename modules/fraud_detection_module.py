# ==========================================================
# ENTERPRISE FRAUD DETECTION MODULE
# Bank-grade fraud detection system
# Compatible with multilingual AI system
# ==========================================================

from datetime import datetime, timedelta


class FraudDetector:

    def __init__(self):

        # configurable thresholds
        self.large_transaction_threshold = 50000

        # rapid transaction detection window
        self.rapid_window_minutes = 2

        # number of transactions to consider suspicious
        self.rapid_count_threshold = 3


    # ======================================================
    # SAFE DATE PARSER
    # ======================================================

    def parse_date(self, date_str):

        formats = [
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d/%m/%Y"
        ]

        for fmt in formats:

            try:
                return datetime.strptime(date_str, fmt)
            except:
                pass

        return None


    # ======================================================
    # MAIN FRAUD DETECTION
    # ======================================================

    def detect(self, transactions):

        if not transactions:
            return transactions

        # Initialize fraud flags
        for t in transactions:

            t["fraud"] = False
            t["fraud_reason"] = ""

        # ==================================================
        # RULE-1: Large transaction detection
        # ==================================================

        for t in transactions:

            amount = float(t.get("amount", 0))

            if amount >= self.large_transaction_threshold:

                t["fraud"] = True

                t["fraud_reason"] = \
                    "Large transaction exceeds safe threshold"


        # ==================================================
        # RULE-2: Rapid repeated transaction detection
        # ==================================================

        parsed = []

        for t in transactions:

            dt = self.parse_date(t.get("date", ""))

            if dt:
                parsed.append((dt, t))

        parsed.sort(key=lambda x: x[0])

        for i in range(len(parsed)):

            window = []

            base_time = parsed[i][0]

            for j in range(i, len(parsed)):

                current_time = parsed[j][0]

                diff = (current_time - base_time).total_seconds()

                if diff <= self.rapid_window_minutes * 60:

                    window.append(parsed[j][1])

                else:
                    break

            if len(window) >= self.rapid_count_threshold:

                for tx in window:

                    tx["fraud"] = True

                    if not tx["fraud_reason"]:

                        tx["fraud_reason"] = \
                            "Multiple rapid transactions detected"


        return transactions


    # ======================================================
    # FRAUD SUMMARY
    # ======================================================

    def fraud_summary(self, transactions):

        total = len(transactions)

        fraud_count = sum(
            1 for t in transactions if t.get("fraud", False)
        )

        safe_count = total - fraud_count

        risk_percent = (
            (fraud_count / total) * 100 if total > 0 else 0
        )

        return {

            "total_transactions": total,

            "fraud_transactions": fraud_count,

            "safe_transactions": safe_count,

            "fraud_risk_percent": round(risk_percent, 2)

        }
