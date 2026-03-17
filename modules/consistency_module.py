class FinancialConsistencyEngine:

    def __init__(self):

        self.transactions = []

    def add_transactions(self, transactions):

        self.transactions = transactions

    def stability_score(self):

        income = sum(
            tx["amount"] for tx in self.transactions
            if tx["type"] == "income"
        )

        expense = sum(
            tx["amount"] for tx in self.transactions
            if tx["type"] == "expense"
        )

        if income == 0:
            return 0

        savings = income - expense

        ratio = savings / income

        if ratio <= 0:
            return 20

        elif ratio < 0.1:
            return 40

        elif ratio < 0.25:
            return 60

        elif ratio < 0.4:
            return 80

        else:
            return 95
