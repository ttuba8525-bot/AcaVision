# ============================================================
#  utils/prediction_service.py — AckVision Prediction Service
#  Runs the three supervised ML models:
#    - Linear Regression  → Final Exam Score
#    - Decision Tree      → Pass / Fail
#    - KNN                → Performance Category
# ============================================================

import numpy as np
import config
from utils import model_loader
from utils.preprocessing import get_feature_array


def predict_exam_score(form_data: dict) -> float:
    """
    Predict the student's Final Exam Score using Linear Regression.

    Args:
        form_data: dict with keys matching config.FEATURE_COLUMNS

    Returns:
        Predicted score as a float, rounded to 2 decimal places.
        Clamped to [0, 100] to avoid out-of-range outputs.
    """
    features = get_feature_array(form_data)
    model    = model_loader.get_linear()
    score    = model.predict(features)[0]
    return round(float(np.clip(score, 0, 100)), 2)


def predict_pass_fail(form_data: dict) -> str:
    """
    Classify Pass or Fail using the Decision Tree classifier.

    Args:
        form_data: dict with keys matching config.FEATURE_COLUMNS

    Returns:
        "Pass" or "Fail" (decoded using config.PASS_FAIL_LABELS)
    """
    features   = get_feature_array(form_data)
    model      = model_loader.get_decision_tree()
    prediction = int(model.predict(features)[0])
    return config.PASS_FAIL_LABELS.get(prediction, "Unknown")


def predict_performance(form_data: dict) -> str:
    """
    Predict the Performance Category using K-Nearest Neighbours.

    Args:
        form_data: dict with keys matching config.FEATURE_COLUMNS

    Returns:
        One of: "Excellent", "Good", "Average", "Poor"
        (decoded using config.PERFORMANCE_LABELS)
    """
    features   = get_feature_array(form_data)
    model      = model_loader.get_knn()
    prediction = int(model.predict(features)[0])
    return config.PERFORMANCE_LABELS.get(prediction, "Unknown")


def run_all_predictions(form_data: dict) -> dict:
    """
    Convenience function — runs all three supervised predictions at once.

    Args:
        form_data: dict with keys matching config.FEATURE_COLUMNS

    Returns:
        dict with keys: exam_score, pass_fail, performance
    """
    return {
        "exam_score":  predict_exam_score(form_data),
        "pass_fail":   predict_pass_fail(form_data),
        "performance": predict_performance(form_data),
    }
