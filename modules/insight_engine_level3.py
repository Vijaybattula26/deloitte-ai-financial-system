# ==========================================================
# LEVEL-3 ADVANCED AI INSIGHT ENGINE
# Resume-grade intelligent financial insights
# ==========================================================

import pandas as pd


class AdvancedInsightEngine:

    def generate(self, transactions):

        if not transactions:
            return ["No financial data available."]

        df = pd.DataFrame(transactions)

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        insights = []

        # ==================================================
        # CATEGORY SPENDING ANALYSIS
        # ==================================================

        category_spend = df.groupby("category")["amount"].sum()

        top_category = category_spend.idxmax()
        top_amount = category_spend.max()

        insights.append(
            f"Highest spending is on {top_category} (₹{top_amount:.0f})."
        )

        # ==================================================
        # SUBSCRIPTION ANALYSIS
        # ==================================================

        subscription_keywords = [
            "netflix",
            "amazon",
            "spotify",
            "subscription"
        ]

        subscription_total = 0

        for t in transactions:

            desc = t.get("description", "").lower()

            if any(word in desc for word in subscription_keywords):

                subscription_total += t.get("amount", 0)

        if subscription_total > 0:

            insights.append(
                f"You spent ₹{subscription_total:.0f} on subscriptions. "
                f"Consider reducing to save money."
            )

        # ==================================================
        # ATM WITHDRAWAL ANALYSIS
        # ==================================================

        atm_total = df[
            df["category"] == "Cash Withdrawal"
        ]["amount"].sum()

        if atm_total > 10000:

            insights.append(
                f"High ATM withdrawals detected (₹{atm_total:.0f}). "
                f"Consider using digital payments."
            )

        # ==================================================
        # INCOME VS EXPENSE RATIO
        # ==================================================

        income = df[df["type"] == "income"]["amount"].sum()

        expense = df[df["type"] == "expense"]["amount"].sum()

        if income > 0:

            ratio = (expense / income) * 100

            if ratio > 80:

                insights.append(
                    "Your expenses are very high compared to income."
                )

            elif ratio < 50:

                insights.append(
                    "Your savings rate is excellent."
                )

        return insights
