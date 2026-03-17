import re
from datetime import datetime


class TransparencyEngine:

    def __init__(self):
        pass

    # ==========================================================
    # MAIN PARSER
    # ==========================================================

    def parse(self, text: str):

        lines = [l.strip() for l in text.split("\n") if l.strip()]
        transactions = []
        current_block = []

        for line in lines:

            lower = line.lower()

            # Skip page headers and noise
            if lower.startswith("page"):
                continue
            if "structured bank statement" in lower:
                continue
            if "date description" in lower:
                continue

            # Detect new transaction block
            if re.match(r"^\d{2}[-/]\d{2}[-/]\d{4}", line):

                # Process previous block first
                if current_block:
                    tx = self.process_block(current_block)
                    if tx:
                        transactions.append(tx)
                    current_block = []

                # Try structured row parser
                structured_tx = self.parse_structured_row(line)
                if structured_tx:
                    transactions.append(structured_tx)
                else:
                    current_block = [line]

            else:
                current_block.append(line)

        # Process remaining block
        if current_block:
            tx = self.process_block(current_block)
            if tx:
                transactions.append(tx)

        return transactions

    # ==========================================================
    # STRUCTURED TABLE PARSER (SAFE & SMART)
    # ==========================================================

    def parse_structured_row(self, line):

        date_match = re.match(r"^\d{2}[-/]\d{2}[-/]\d{4}", line)
        if not date_match:
            return None

        date = date_match.group().replace("/", "-")
        remaining = line[len(date_match.group()):].strip()
        lower = remaining.lower()

        # Extract numbers AFTER removing date
        numbers = re.findall(r"\d+\.\d+|\d+", remaining)
        numbers = [float(n) for n in numbers]

        if len(numbers) < 2:
            return None

        # First number is transaction amount
        amount = numbers[0]

        # Remove numbers from description
        description = re.sub(r"\d+\.\d+|\d+", "", remaining).strip()

        # Smart type detection
        if any(word in lower for word in [
            "salary",
            "credited",
            "interest",
            "income",
            "bonus",
            "freelance"
        ]):
            tx_type = "income"
        else:
            tx_type = "expense"

        if amount <= 0:
            return None

        return {
            "date": date,
            "description": description,
            "type": tx_type,
            "product_amount": round(amount, 2),
            "deducted_amount": round(amount, 2),
            "amount": round(amount, 2),
            "extra_charge": 0,
            "percentage_charge": 0,
            "charge_reason": "No Extra Charges",
            "mode": "Unknown",
            "bank": "Unknown"
        }

    # ==========================================================
    # BLOCK STYLE PARSER (GST / FEES / OCR)
    # ==========================================================

    def process_block(self, block_lines):

        product_amount = None
        deducted_amount = None
        fee_total = 0

        bank = "Unknown"
        mode = "Unknown"
        date = None
        description = None
        tx_type = "expense"

        for line in block_lines:

            lower = line.lower()

            # DATE
            date_match = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", line)
            if date_match:
                date = date_match.group().replace("/", "-")

            # Income keywords
            if any(word in lower for word in [
                "salary",
                "credited",
                "income",
                "bonus",
                "interest",
                "freelance"
            ]):
                tx_type = "income"

            # Bank detection
            for b in ["hdfc", "sbi", "icici", "axis", "kotak", "phonepe", "paytm"]:
                if b in lower:
                    bank = b.upper()

            # Mode detection
            if "upi" in lower:
                mode = "UPI"
            elif "credit card" in lower:
                mode = "Credit Card"
            elif "debit card" in lower:
                mode = "Debit Card"
            elif "netbanking" in lower:
                mode = "NetBanking"
            elif "auto debit" in lower:
                mode = "Auto Debit"
            elif "atm" in lower:
                mode = "ATM"

            numbers = re.findall(r"\d+\.\d+|\d+", line)
            numbers = [float(n) for n in numbers]

            # TOTAL lines
            if any(word in lower for word in [
                "total deducted",
                "total paid",
                "total amount"
            ]):
                if numbers:
                    deducted_amount = numbers[-1]
                continue

            # FEE lines
            if any(word in lower for word in [
                "gst",
                "service charge",
                "processing fee",
                "platform fee",
                "convenience fee",
                "bank surcharge"
            ]):
                if numbers:
                    fee_total += numbers[-1]
                continue

            # PRODUCT line
            if numbers and product_amount is None:
                product_amount = numbers[-1]
                clean_line = re.sub(r"\d+\.\d+|\d+", "", line)
                clean_line = re.sub(r"\d{2}[-/]\d{2}[-/]\d{4}", "", clean_line)
                description = clean_line.strip()

        if product_amount is None:
            return None

        # Final calculation
        if tx_type == "income":
            deducted_amount = product_amount
            extra = 0
        else:
            if deducted_amount is None:
                deducted_amount = product_amount + fee_total
            extra = deducted_amount - product_amount

        if not date:
            date = datetime.now().strftime("%d-%m-%Y")

        return {
            "date": date,
            "description": description or "Transaction",
            "type": tx_type,
            "product_amount": round(product_amount, 2),
            "deducted_amount": round(deducted_amount, 2),
            "amount": round(deducted_amount, 2),
            "extra_charge": round(extra, 2),
            "percentage_charge": round((extra / product_amount) * 100, 2) if product_amount else 0,
            "charge_reason": "Fee Applied" if extra > 0 else "No Extra Charges",
            "mode": mode,
            "bank": bank
        }