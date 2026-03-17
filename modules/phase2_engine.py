import os
import joblib
import numpy as np


class Phase2IntelligenceEngine:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(BASE_DIR)

        MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best_ensemble_model.pkl")
        VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "models", "tfidf_vectorizer.pkl")

        self.model = joblib.load(MODEL_PATH)
        self.vectorizer = joblib.load(VECTORIZER_PATH)

        print("✅ Enterprise ML Engine Loaded")

    def predict(self, transaction):

        description = transaction.get("description", "")

        if not description:
            return transaction.get("type", "expense"), 0.50

        try:

            X = self.vectorizer.transform([description])

            prediction = self.model.predict(X)[0]

            probabilities = self.model.predict_proba(X)[0]

            confidence = float(np.max(probabilities))

            label = "income" if prediction == 1 else "expense"

            # Hybrid override logic
            if confidence >= 0.80:
                return label, round(confidence, 2)

            return transaction.get("type", label), round(confidence, 2)

        except:
            return transaction.get("type", "expense"), 0.50
