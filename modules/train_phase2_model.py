import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ---------------------------------------------------
# SAFE DATA PATH
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# ---------------------------------------------------
# DATA PATHS (MULTIPLE DATASETS)
# ---------------------------------------------------

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

dataset_files = [
    "financial_transactions_100k_realistic.csv",
    "financial_dataset_300k.csv",
    "financial_dataset_400k.csv",
    "financial_dataset_500k.csv"
]

dataframes = []

print("\nLoading datasets...\n")

for file in dataset_files:

    path = os.path.join(DATA_DIR, file)

    if not os.path.exists(path):
        raise Exception(f"❌ Dataset not found: {path}")

    print("Loading dataset:", path)

    df_temp = pd.read_csv(path)

    print("Shape:", df_temp.shape)

    dataframes.append(df_temp)

# ---------------------------------------------------
# COMBINE DATASETS
# ---------------------------------------------------

df = pd.concat(dataframes, ignore_index=True)

print("\nFinal Combined Dataset Shape:", df.shape)

print("Columns Found:", df.columns.tolist())

# Fill missing values caused by different dataset columns
df = df.fillna("")

# ---------------------------------------------------
# AUTO DETECT COLUMNS
# ---------------------------------------------------

possible_text_cols = ["description", "transaction", "details", "text"]

possible_label_cols = ["type", "category", "label"]

TEXT_COLUMN = None
LABEL_COLUMN = None

for col in df.columns:

    if col.lower() in possible_text_cols:
        TEXT_COLUMN = col

    if col.lower() in possible_label_cols:
        LABEL_COLUMN = col

if TEXT_COLUMN is None or LABEL_COLUMN is None:

    raise Exception("❌ Could not detect description/type column.")

print("\nDetected Text Column:", TEXT_COLUMN)

print("Detected Label Column:", LABEL_COLUMN)

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

df = df[[TEXT_COLUMN, LABEL_COLUMN]].dropna()

df[LABEL_COLUMN] = df[LABEL_COLUMN].astype(str).str.lower()

# ---------------------------------------------------
# CORRECT LABEL MAPPING
# ---------------------------------------------------

df[LABEL_COLUMN] = df[LABEL_COLUMN].replace({
    "credit": "income",
    "debit": "expense",
    "transfer": "expense"
})

# Keep only valid labels
df = df[df[LABEL_COLUMN].isin(["income", "expense"])]

print("\nFinal Training Samples:", len(df))

if len(df) == 0:
    raise Exception("❌ No valid training samples after label mapping.")

# ---------------------------------------------------
# PREPARE DATA
# ---------------------------------------------------

X_text = df[TEXT_COLUMN]

y = df[LABEL_COLUMN].map({
    "income": 1,
    "expense": 0
})

# ---------------------------------------------------
# TRAIN TEST SPLIT (FIRST - PREVENT DATA LEAKAGE)
# ---------------------------------------------------

print("\nSplitting dataset...")

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------
# TF-IDF VECTORIZATION (ADVANCED)
# ---------------------------------------------------

vectorizer = TfidfVectorizer(

    ngram_range=(1,4),

    stop_words="english",

    max_features=50000,

    min_df=2,

    max_df=0.95,

    sublinear_tf=True

)

print("\nGenerating TF-IDF features...")

X_train = vectorizer.fit_transform(X_train_text)

X_test = vectorizer.transform(X_test_text)

# ---------------------------------------------------
# MODEL (Balanced Logistic Regression)
# ---------------------------------------------------

print("\nTraining Logistic Regression model...")

model = LogisticRegression(

    max_iter=3000,

    solver="saga",

    class_weight="balanced",

    n_jobs=-1

)

model.fit(X_train, y_train)

# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------

print("\nEvaluating model...\n")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

print("====== PHASE 2 RESEARCH EVALUATION ======")

print("Accuracy :", round(accuracy, 4))

print("Precision:", round(precision, 4))

print("Recall   :", round(recall, 4))

print("F1 Score :", round(f1, 4))

print("==========================================")

# ---------------------------------------------------
# CROSS VALIDATION
# ---------------------------------------------------

print("\nRunning 5-Fold Cross Validation...")

X_full = vectorizer.transform(X_text)

skf = StratifiedKFold(

    n_splits=5,

    shuffle=True,

    random_state=42

)

cv_scores = cross_val_score(

    model,

    X_full,

    y,

    cv=skf,

    n_jobs=-1

)

print("CV Scores:", cv_scores)

print("Mean CV Accuracy:", round(cv_scores.mean(), 4))

# ---------------------------------------------------
# CONFUSION MATRIX
# ---------------------------------------------------

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")

print(classification_report(y_test, y_pred))

# ---------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(MODEL_DIR, "financial_model.pkl")

vectorizer_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

joblib.dump(model, model_path)

joblib.dump(vectorizer, vectorizer_path)

print("\n✅ Model saved successfully!")

print("Model Path:", model_path)

print("Vectorizer Path:", vectorizer_path)