# PHASE-2 ML CLASSIFIER MODULE

import joblib

def predict_document_type(text):
    '''
    Predicts document type: Bank Statement / Receipt / Salary Slip
    '''
    try:
        model = joblib.load("models/doc_classifier.pkl")
        return model.predict([text])[0]
    except:
        return "Unknown"


def classify_transaction(description, amount):
    '''
    Predicts Income / Expense category
    '''
    try:
        model = joblib.load("models/transaction_classifier.pkl")
        features = [description, amount]
        return model.predict([features])[0]
    except:
        return "Uncategorized"
