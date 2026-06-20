import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def generate_synthetic_dataset(n_samples=2000):
    """
    Generates synthetic patient records with realistic ranges:
      - glucose (mg/dL): normal ~70-99, prediabetic ~100-125, diabetic >125
      - haemoglobin (g/dL): normal ~13-17 (men), ~12-15 (women); low = anemia risk
      - cholesterol (mg/dL): normal <200, borderline 200-239, high >=240

    Label (risk_level) is derived from simple medical heuristics combined
    with random noise, then used as ground truth to train the classifier.
    """
    glucose = np.random.normal(110, 35, n_samples).clip(50, 400)
    haemoglobin = np.random.normal(14, 2.5, n_samples).clip(5, 20)
    cholesterol = np.random.normal(190, 50, n_samples).clip(100, 400)

    risk_level = []
    for g, h, c in zip(glucose, haemoglobin, cholesterol):
        score = 0
        if g >= 126:
            score += 2
        elif g >= 100:
            score += 1

        if h < 12:
            score += 1

        if c >= 240:
            score += 2
        elif c >= 200:
            score += 1

        if score >= 3:
            risk_level.append("High")
        elif score >= 1:
            risk_level.append("Moderate")
        else:
            risk_level.append("Low")

    df = pd.DataFrame(
        {
            "glucose": glucose,
            "haemoglobin": haemoglobin,
            "cholesterol": cholesterol,
            "risk_level": risk_level,
        }
    )
    return df


def train_and_save_model():
    df = generate_synthetic_dataset()

    X = df[["glucose", "haemoglobin", "cholesterol"]]
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150, max_depth=6, random_state=RANDOM_SEED
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model trained. Test accuracy: {accuracy:.2%}")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
    joblib.dump(model, output_path)
    print(f"Model saved to: {output_path}")


if __name__ == "__main__":
    train_and_save_model()