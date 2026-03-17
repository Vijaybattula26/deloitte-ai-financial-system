class FinancialValidator:

    def clean_transactions(self, transactions):

        cleaned = []

        for tx in transactions:

            # Remove zero amounts
            if tx["amount"] <= 0:
                continue

            # Remove balance rows
            if "balance" in tx["description"].lower():
                continue

            # Fix wrong deposit detection
            if "deposit" in tx["description"].lower():
                tx["type"] = "income"

            cleaned.append(tx)

        return cleaned
