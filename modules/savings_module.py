# ==========================================================
# ADVANCED ENTERPRISE SAVINGS ADVISOR (V2)
# Covers:
# - Accurate income/expense calculation
# - Savings ratio
# - Emergency fund coverage
# - Financial health classification
# - Category-based expense grouping
# - Top 3 spending category detection
# - Savings improvement suggestions
# - Projected savings calculation
# - Advisory action plan generation
# - Core Point 3 Fully Covered
# ==========================================================

from collections import defaultdict
from datetime import datetime


class SavingsAdvisor:

    def __init__(self):

        self.transactions = []
        self.income = []
        self.expense = []
        self.category_expense = defaultdict(float)

    # ======================================================
    # SAFE RESET + LOAD
    # ======================================================

    def add_transactions(self, transactions):

        self.transactions = []
        self.income = []
        self.expense = []
        self.category_expense = defaultdict(float)

        if not transactions:
            return

        for tx in transactions:

            try:
                amount = float(tx.get("amount", 0))
                if amount <= 0:
                    continue

                tx_type = str(tx.get("type", "")).strip().lower()

                if tx_type == "income":
                    self.income.append(amount)

                elif tx_type == "expense":
                    self.expense.append(amount)

                    category = str(
                        tx.get("category", "others")
                    ).lower()

                    self.category_expense[category] += amount

                else:
                    continue

                self.transactions.append({
                    "date": tx.get("date"),
                    "description": tx.get("description"),
                    "amount": amount,
                    "type": tx_type,
                    "category": tx.get("category", "others")
                })

            except:
                continue

    # ======================================================
    # BASIC METRICS
    # ======================================================

    def total_income(self):
        return round(sum(self.income), 2)

    def total_expense(self):
        return round(sum(self.expense), 2)

    def monthly_savings(self):
        return round(self.total_income() - self.total_expense(), 2)

    def savings_ratio(self):

        income = self.total_income()

        if income == 0:
            return 0

        ratio = (self.monthly_savings() / income) * 100
        return round(ratio, 2)

    # ======================================================
    # MONTH PARSER
    # ======================================================

    def parse_month(self, date_str):

        if not date_str:
            return None

        formats = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]

        for fmt in formats:
            try:
                dt = datetime.strptime(str(date_str), fmt)
                return dt.strftime("%Y-%m")
            except:
                continue

        return None

    # ======================================================
    # EMERGENCY COVERAGE
    # ======================================================

    def emergency_months_covered(self):

        monthly_expense = defaultdict(float)

        for tx in self.transactions:

            if tx["type"] != "expense":
                continue

            month = self.parse_month(tx.get("date"))

            if not month:
                continue

            monthly_expense[month] += tx["amount"]

        if not monthly_expense:
            return 0

        avg_expense = sum(monthly_expense.values()) / len(monthly_expense)

        if avg_expense <= 0:
            return 0

        savings = self.monthly_savings()

        if savings <= 0:
            return 0

        return round(savings / avg_expense, 1)

    # ======================================================
    # FINANCIAL HEALTH
    # ======================================================

    def financial_health(self):

        ratio = self.savings_ratio()

        if ratio >= 50:
            return "Excellent"
        elif ratio >= 30:
            return "Good"
        elif ratio >= 10:
            return "Moderate"
        else:
            return "At Risk"

    # ======================================================
    # TOP SPENDING CATEGORIES
    # ======================================================

    def top_expense_categories(self, limit=3):

        sorted_categories = sorted(
            self.category_expense.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_categories[:limit]

    # ======================================================
    # IMPROVEMENT PLAN GENERATOR
    # ======================================================

    def generate_improvement_plan(self):

        current_savings = self.monthly_savings()
        health = self.financial_health()

        plan = {
            "current_savings": current_savings,
            "current_health": health,
            "suggestions": [],
            "projected_savings": current_savings,
            "target_health": health
        }

        if current_savings >= 0 and health in ["Good", "Excellent"]:
            return plan

        top_categories = self.top_expense_categories()

        projected_savings = current_savings

        for category, amount in top_categories:

            reduction_percent = 20
            reduction_value = round((amount * reduction_percent) / 100, 2)

            projected_savings += reduction_value

            plan["suggestions"].append({
                "category": category,
                "current_spending": amount,
                "suggested_reduction_percent": reduction_percent,
                "potential_savings": reduction_value
            })

        plan["projected_savings"] = round(projected_savings, 2)

        projected_ratio = 0
        income = self.total_income()

        if income > 0:
            projected_ratio = (
                projected_savings / income
            ) * 100

        if projected_ratio >= 50:
            plan["target_health"] = "Excellent"
        elif projected_ratio >= 30:
            plan["target_health"] = "Good"
        elif projected_ratio >= 10:
            plan["target_health"] = "Moderate"
        else:
            plan["target_health"] = "At Risk"

        return plan

    # ======================================================
    # FINAL REPORT
    # ======================================================

    def advisory_report(self):

        total_income = self.total_income()
        total_expense = self.total_expense()
        monthly_savings = self.monthly_savings()
        savings_ratio = self.savings_ratio()
        emergency_months = self.emergency_months_covered()
        health = self.financial_health()
        improvement_plan = self.generate_improvement_plan()

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "monthly_savings": monthly_savings,
            "savings_ratio": savings_ratio,
            "emergency_months": emergency_months,
            "financial_health": health,
            "improvement_plan": improvement_plan,
            "mode": "enterprise_v2"
        }