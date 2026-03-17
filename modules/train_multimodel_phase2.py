import pandas as pd
import numpy as np
import os
import joblib
import time
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier

# ---------------------------------------------------
# PATH SETUP
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

print("\nLoading datasets...\n")

# ---------------------------------------------------
# LOAD MULTIPLE DATASETS
# ---------------------------------------------------

dataset_files = [
    "financial_transactions_100k_realistic.csv",
    "financial_dataset_300k.csv",
    "financial_dataset_400k.csv",
    "financial_dataset_500k.csv"
]

dfs = []

for file in dataset_files:

    path = os.path.join(DATA_DIR, file)

    if not os.path.exists(path):
        raise Exception(f"❌ Dataset not found: {path}")

    temp = pd.read_csv(path)

    print("Loaded:", file, temp.shape)

    dfs.append(temp)

# Combine datasets
df = pd.concat(dfs, ignore_index=True)

print("\nFinal Dataset Size:", df.shape)

# ---------------------------------------------------
# PREPARE DATA
# ---------------------------------------------------

TEXT_COLUMN = "description"
LABEL_COLUMN = "type"

df = df[[TEXT_COLUMN, LABEL_COLUMN]].dropna()

df[LABEL_COLUMN] = df[LABEL_COLUMN].str.lower()

X_text = df[TEXT_COLUMN]

y = df[LABEL_COLUMN].map({
    "income": 1,
    "expense": 0
})

print("Training Samples:", len(df))

# ---------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------
# TF-IDF FEATURE ENGINEERING
# ---------------------------------------------------

vectorizer = TfidfVectorizer(
    ngram_range=(1,4),
    max_features=50000,
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

# ---------------------------------------------------
# BASE MODELS
# ---------------------------------------------------

linear_svc = LinearSVC(
    C=1.5,
    class_weight="balanced"
)

xgb = XGBClassifier(
    n_estimators=600,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="logloss",
    n_jobs=-1
)

# ---------------------------------------------------
# ENSEMBLE MODEL
# ---------------------------------------------------

ensemble = VotingClassifier(
    estimators=[
        ("svc", linear_svc),
        ("xgb", xgb)
    ],
    voting="hard"
)

# ---------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------

print("\nTraining Ensemble Model...\n")

start = time.time()

ensemble.fit(X_train, y_train)

end = time.time()

print("Training Time:", round(end - start, 2), "seconds")

# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------

y_pred = ensemble.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n========== ENSEMBLE RESULTS ==========")

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))

print("======================================")

# ---------------------------------------------------
# CROSS VALIDATION
# ---------------------------------------------------

print("\nRunning Stratified 5-Fold Cross Validation...\n")

X_full = vectorizer.transform(X_text)

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    ensemble,
    X_full,
    y,
    cv=skf,
    n_jobs=-1
)

print("5-Fold Stratified CV Accuracy:")
print("Scores:", cv_scores)
print("Mean CV Accuracy:", round(cv_scores.mean(), 4))

# ---------------------------------------------------
# CONFUSION MATRIX
# ---------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ---------------------------------------------------
# SAVE CONFUSION MATRIX IMAGE
# ---------------------------------------------------

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Expense", "Income"],
    yticklabels=["Expense", "Income"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Ensemble Model")

plt.tight_layout()

plt.savefig(os.path.join(MODEL_DIR, "confusion_matrix.png"))
plt.close()

# ---------------------------------------------------
# ROC CURVE
# ---------------------------------------------------

print("\nGenerating ROC Curve...\n")

xgb.fit(X_train, y_train)

y_probs = xgb.predict_proba(X_test)[:,1]

roc_auc = roc_auc_score(y_test, y_probs)

fpr, tpr, _ = roc_curve(y_test, y_probs)

plt.figure()

plt.plot(
    fpr,
    tpr,
    label="XGBoost ROC (AUC = %.4f)" % roc_auc
)

plt.plot([0,1], [0,1], linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.savefig(os.path.join(MODEL_DIR, "roc_curve.png"))
plt.close()

print("ROC-AUC Score:", round(roc_auc, 4))

# ---------------------------------------------------
# SAVE MODEL + VECTORIZER
# ---------------------------------------------------

joblib.dump(
    ensemble,
    os.path.join(MODEL_DIR, "best_ensemble_model.pkl")
)

joblib.dump(
    vectorizer,
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)

print("\n✅ Ensemble model saved successfully.")