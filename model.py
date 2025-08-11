# model.py
"""
Train or load a TF-IDF + LogisticRegression model to score resumes versus job descriptions.
If no preexisting model in /models, a small synthetic dataset will be created and model trained.
Outputs: models/model.pkl and models/vectorizer.pkl
"""
import os
import joblib
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

MODELS_DIR = "models"
VEC_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")

def ensure_dirs():
    os.makedirs(MODELS_DIR, exist_ok=True)

def synthetic_dataset():
    # small synthetic examples (job text vs resume text) — labels: 1 = good match, 0 = poor
    job = "Data analysis Python SQL machine learning NLP TensorFlow scikit-learn Power BI OCI"
    samples = [
        (job + " experience with TF-IDF and XGBoost", 1),
        ("Python pandas SQL data visualization Power BI", 1),
        ("Selenium automation testing test cases pytest", 0),
        ("Administrative assistant scheduling bookkeeping", 0),
        ("Machine learning model deployment OCI containerization", 1),
        ("Graphic design photoshop illustrator", 0),
        ("NLP sentiment analysis spaCy NLTK", 1),
        ("Customer support call handling", 0),
        ("Data engineer ETL pipeline AWS S3", 1),
        ("waiter hospitality service", 0),
    ]
    df = pd.DataFrame(samples, columns=["text","label"])
    return df

def train_and_save():
    ensure_dirs()
    print("Training model (synthetic dataset)...")
    df = synthetic_dataset()
    X = df["text"].values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vect = TfidfVectorizer(ngram_range=(1,2), max_features=3000)
    clf = LogisticRegression(max_iter=1000)
    pipeline = make_pipeline(vect, clf)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:,1]
    acc = accuracy_score(y_test, preds)
    try:
        auc = roc_auc_score(y_test, probs)
    except:
        auc = None
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model trained. Accuracy: {acc:.3f} AUC: {auc}")
    return pipeline

def load_model():
    if os.path.exists(MODEL_PATH):
        print("Loading saved model...")
        pipeline = joblib.load(MODEL_PATH)
    else:
        pipeline = train_and_save()
    return pipeline

if __name__ == "__main__":
    load_model()
