import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")

_model = None


def _load_model():
    """
    Lazily loads the model into a module-level singleton so the .pkl
    file is read from disk only once, not on every prediction request.
    """
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "model.pkl not found. Run 'python train_model.py' inside "
                "backend/ml first to generate it."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_health_risk(glucose, haemoglobin, cholesterol):
    """
    Runs the ML model on the three blood test values and returns a
    human-readable remarks string, e.g.:
        "Low risk - Glucose, Haemoglobin and Cholesterol within normal range."
        "Moderate risk - Borderline glucose/cholesterol levels detected. Recommend follow-up."
        "High risk - Elevated glucose/cholesterol levels detected. Medical review advised."
    """
    model = _load_model()

    features = pd.DataFrame(
        [[float(glucose), float(haemoglobin), float(cholesterol)]],
        columns=["glucose", "haemoglobin", "cholesterol"],
    )

    risk_level = model.predict(features)[0]

    remarks_map = {
        "Low": "Low risk - Glucose, Haemoglobin and Cholesterol within normal range.",
        "Moderate": (
            "Moderate risk - Borderline levels detected in one or more parameters. "
            "Recommend follow-up testing."
        ),
        "High": (
            "High risk - Elevated glucose/cholesterol or low haemoglobin detected. "
            "Medical review advised."
        ),
    }

    return remarks_map.get(risk_level, "Unable to determine risk level.")