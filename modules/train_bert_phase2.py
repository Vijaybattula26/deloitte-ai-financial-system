import os
import time
import pandas as pd
import numpy as np
import torch

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments
)

# ---------------------------------------------------
# PATH SETUP
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "financial_transactions_100k_realistic.csv"
)

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading dataset from:", DATA_PATH)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)
print("Columns:", df.columns.tolist())

# ---------------------------------------------------
# TEXT FEATURE FUSION
# ---------------------------------------------------

df["full_text"] = (
    df["description"].astype(str) + " " +
    df["merchant_name"].astype(str) + " " +
    df["payment_method"].astype(str) + " " +
    df["customer_segment"].astype(str) + " " +
    df["location"].astype(str)
)

# ---------------------------------------------------
# LABEL MAPPING
# ---------------------------------------------------

df["type"] = df["type"].map({
    "income": 1,
    "expense": 0
})

df = df[["full_text", "type"]].dropna()

print("Training Samples:", len(df))

# ---------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------

train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["full_text"].tolist(),
    df["type"].tolist(),
    test_size=0.2,
    random_state=42,
    stratify=df["type"]
)

# ---------------------------------------------------
# TOKENIZER (FINBERT)
# ---------------------------------------------------

print("\nLoading FinBERT tokenizer...")

tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")

train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=256
)

test_encodings = tokenizer(
    test_texts,
    truncation=True,
    padding=True,
    max_length=256
)

# ---------------------------------------------------
# DATASET CLASS
# ---------------------------------------------------

class FinancialDataset(torch.utils.data.Dataset):

    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):

        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])

        return item

    def __len__(self):

        return len(self.labels)


train_dataset = FinancialDataset(train_encodings, train_labels)
test_dataset = FinancialDataset(test_encodings, test_labels)

# ---------------------------------------------------
# MODEL (FINBERT)
# ---------------------------------------------------

print("\nLoading FinBERT model...")

model = BertForSequenceClassification.from_pretrained(
    "ProsusAI/finbert",
    num_labels=2
)

# ---------------------------------------------------
# TRAINING CONFIG
# ---------------------------------------------------

training_args = TrainingArguments(

    output_dir="./bert_results",

    num_train_epochs=4,

    learning_rate=2e-5,

    per_device_train_batch_size=16,

    per_device_eval_batch_size=16,

    warmup_steps=500,

    weight_decay=0.01,

    logging_dir="./logs",

    evaluation_strategy="epoch",

    save_strategy="epoch",

    logging_steps=100,

    load_best_model_at_end=True,

)

# ---------------------------------------------------
# TRAINER
# ---------------------------------------------------

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=test_dataset,

)

# ---------------------------------------------------
# TRAIN
# ---------------------------------------------------

print("\nTraining FinBERT model...\n")

start_time = time.time()

trainer.train()

end_time = time.time()

print("\nTraining Time:", round(end_time - start_time, 2), "seconds")

# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------

print("\nRunning evaluation...\n")

predictions = trainer.predict(test_dataset)

preds = np.argmax(predictions.predictions, axis=1)

accuracy = accuracy_score(test_labels, preds)
precision = precision_score(test_labels, preds)
recall = recall_score(test_labels, preds)
f1 = f1_score(test_labels, preds)

print("\n========== FINBERT RESULTS ==========")
print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))
print("=====================================")

print("\nConfusion Matrix:")

print(confusion_matrix(test_labels, preds))

print("\nClassification Report:")

print(classification_report(test_labels, preds))

# ---------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------

print("\nSaving model...")

model.save_pretrained(os.path.join(MODEL_DIR, "finbert_financial_model"))

tokenizer.save_pretrained(os.path.join(MODEL_DIR, "finbert_tokenizer"))

print("\n✅ FinBERT model saved successfully in /models folder")