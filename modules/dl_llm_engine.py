from transformers import pipeline

class FinancialDLClassifier:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )

    def predict(self, text):
        if not text or not text.strip():
            return "expense"

        result = self.classifier(text)[0]

        # Labels look like: "1 star", "2 stars", ..., "5 stars"
        stars = int(result["label"][0])

        # Simple semantic mapping
        # Low sentiment → expense
        # High sentiment → income
        if stars >= 4:
            return "income"
        else:
            return "expense"
