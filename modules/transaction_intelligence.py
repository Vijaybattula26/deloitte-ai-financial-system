# ==========================================================
# ADVANCED TRANSACTION INTELLIGENCE ENGINE (FINAL STABLE VERSION)
# TransparencyEngine Compatible
# ==========================================================

import re


class TransactionIntelligenceEngine:

    def __init__(self):
        pass

    # ======================================================
    # MAIN ANALYZE FUNCTION
    # ======================================================

    def analyze(self, tx: dict) -> dict:

        description = str(tx.get("description", "")).lower()
        amount = float(tx.get("amount", 0))
        tx_type = tx.get("type")

        # --------------------------------------------------
        # CATEGORY
        # --------------------------------------------------
        tx["category"] = self.detect_category(description)

        # --------------------------------------------------
        # PAYMENT MODE
        # --------------------------------------------------
        tx["mode"] = self.detect_mode(description)

        # --------------------------------------------------
        # BANK
        # --------------------------------------------------
        tx["bank"] = self.detect_bank(description)

        # --------------------------------------------------
        # AMOUNT DETECTION (RESPECT TRANSPARENCY ENGINE)
        # --------------------------------------------------

        if "product_amount" in tx and "deducted_amount" in tx:
            product_amount = float(tx["product_amount"])
            deducted_amount = float(tx["deducted_amount"])
        else:
            product_amount, deducted_amount = self.detect_amounts(
                description, amount
            )

        tx["product_amount"] = round(product_amount, 2)
        tx["deducted_amount"] = round(deducted_amount, 2)

        # --------------------------------------------------
        # EXTRA CHARGE
        # --------------------------------------------------

        extra_charge = round(deducted_amount - product_amount, 2)

        if extra_charge < 0:
            extra_charge = 0

        tx["extra_charge"] = extra_charge

        # --------------------------------------------------
        # PERCENTAGE CHARGE
        # --------------------------------------------------

        if product_amount > 0:
            percentage_charge = round(
                (extra_charge / product_amount) * 100, 2
            )
        else:
            percentage_charge = 0

        tx["percentage_charge"] = percentage_charge

        # --------------------------------------------------
        # CHARGE REASON
        # --------------------------------------------------

        tx["charge_reason"] = self.detect_charge_reason(
            description, extra_charge
        )

        # --------------------------------------------------
        # FRAUD + RISK DETECTION
        # --------------------------------------------------

        fraud_flag, risk_score = self.detect_fraud(
            percentage_charge,
            tx["mode"],
            tx["bank"],
            tx_type
        )

        tx["fraud"] = fraud_flag
        tx["risk_score"] = risk_score
        tx["risk_level"] = self.risk_level(risk_score)

        # --------------------------------------------------
        # ANOMALY DETECTION
        # --------------------------------------------------

        tx["anomaly"] = self.detect_anomaly(
            product_amount,
            percentage_charge,
            tx_type
        )

        # --------------------------------------------------
        # PROCESS EXPLANATION
        # --------------------------------------------------

        tx["process_explanation"] = self.generate_process_explanation(tx)

        # --------------------------------------------------
        # SAVINGS IMPACT
        # --------------------------------------------------

        tx["savings_impact"] = self.calculate_savings_impact(tx)

        return tx

    # ======================================================
    # CATEGORY DETECTION
    # ======================================================

    def detect_category(self, desc):

        categories = {
            "food": [
                "swiggy", "zomato", "restaurant", "cafe",
                "dining", "food", "taj", "hotel"
            ],
            "shopping": ["amazon", "flipkart", "mall", "store"],
            "utilities": ["electricity", "water", "gas", "bill", "internet"],
            "rent": ["rent", "landlord"],
            "salary": ["salary", "credited"],
            "travel": ["uber", "ola", "flight", "bus"],
            "atm": ["atm", "withdrawal"],
        }

        for category, keywords in categories.items():
            for word in keywords:
                if word in desc:
                    return category

        return "others"

    # ======================================================
    # MODE DETECTION
    # ======================================================

    def detect_mode(self, desc):

        if "upi" in desc:
            return "UPI"
        if "neft" in desc:
            return "NEFT"
        if "imps" in desc:
            return "IMPS"
        if "credit card" in desc:
            return "Credit Card"
        if "debit card" in desc:
            return "Debit Card"
        if "atm" in desc:
            return "Cash Withdrawal"

        return "Unknown"

    # ======================================================
    # BANK DETECTION
    # ======================================================

    def detect_bank(self, desc):

        banks = [
            "sbi", "hdfc", "icici", "axis",
            "kotak", "phonepe", "google pay", "paytm"
        ]

        for bank in banks:
            if bank in desc:
                return bank.upper()

        return "Unknown"

    # ======================================================
    # AMOUNT EXTRACTION (Fallback Only)
    # ======================================================

    def detect_amounts(self, desc, fallback_amount):

        numbers = re.findall(r"\d+\.\d+|\d+", desc)
        amounts = [float(n) for n in numbers if float(n) > 0]

        if len(amounts) >= 2:
            return min(amounts), max(amounts)

        if len(amounts) == 1:
            return amounts[0], amounts[0]

        return fallback_amount, fallback_amount

    # ======================================================
    # CHARGE REASON
    # ======================================================

    def detect_charge_reason(self, desc, extra_charge):

        if extra_charge == 0:
            return "No Extra Charges"

        if "gst" in desc:
            return "GST"
        if "processing" in desc:
            return "Processing Fee"
        if "convenience" in desc:
            return "Convenience Fee"
        if "service charge" in desc:
            return "Service Charge"

        return "Bank or Platform Fee"

    # ======================================================
    # FRAUD DETECTION
    # ======================================================

    def detect_fraud(self, percentage_charge, mode, bank, tx_type):

        if tx_type == "income":
            return False, 0

        risk_score = 0

        if percentage_charge > 25:
            risk_score += 60
        elif percentage_charge > 15:
            risk_score += 40
        elif percentage_charge > 5:
            risk_score += 20

        if bank == "Unknown" and percentage_charge > 10:
            risk_score += 10

        if mode == "Unknown" and percentage_charge > 10:
            risk_score += 10

        fraud_flag = risk_score >= 60

        return fraud_flag, min(risk_score, 100)

    # ======================================================
    # RISK LEVEL
    # ======================================================

    def risk_level(self, risk_score):

        if risk_score >= 70:
            return "High"
        elif risk_score >= 40:
            return "Medium"
        else:
            return "Low"

    # ======================================================
    # ANOMALY DETECTION
    # ======================================================

    def detect_anomaly(self, product_amount, percentage_charge, tx_type):

        if tx_type == "income":
            return False

        if product_amount > 50000:
            return True

        if percentage_charge > 30:
            return True

        return False

    # ======================================================
    # PROCESS EXPLANATION
    # ======================================================

    def generate_process_explanation(self, tx):

        explanation = f"""
        Product Amount: ₹{tx['product_amount']}.
        Deducted Amount: ₹{tx['deducted_amount']}.
        Extra Charge: ₹{tx['extra_charge']} ({tx['percentage_charge']}%).
        Charge Reason: {tx['charge_reason']}.
        Payment Mode: {tx['mode']}.
        Bank/Platform: {tx['bank']}.
        Risk Level: {tx['risk_level']}.
        """

        if tx["fraud"]:
            explanation += " ⚠ This transaction shows high fraud risk."

        return explanation.strip()

    # ======================================================
    # SAVINGS IMPACT
    # ======================================================

    def calculate_savings_impact(self, tx):

        if tx.get("type") == "expense":
            return -tx.get("deducted_amount", 0)

        if tx.get("type") == "income":
            return tx.get("deducted_amount", 0)

        return 0