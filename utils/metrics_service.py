# ============================================================
#  utils/metrics_service.py — AckVision Model Metrics Service
#  Calculates and returns evaluation metrics for all 4 models.
#  Called by the /api/metrics route in app.py.
# ============================================================

import pandas as pd
import numpy as np
import joblib
import config
from utils import model_loader
from utils.preprocessing import get_feature_array
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, f1_score, precision_score, recall_score,
    silhouette_score, classification_report
)


def get_all_metrics() -> dict:
    """
    Load the dataset and evaluate all 4 models.
    Returns a structured dict of metrics for each model.

    Note:
        This runs predictions on the full dataset.
        Results are re-computed each time — add caching if needed for production.
    """
    try:
        df      = pd.read_csv(config.DATA_PATH)
        scaler  = joblib.load(config.SCALER_PATH)
        X       = scaler.transform(df[config.FEATURE_COLUMNS].values)

        metrics = {}

        # ── Linear Regression ────────────────────────────────────────────
        if "Final Exam Score" in df.columns:
            y_true = df["Final Exam Score"].values
            y_pred = model_loader.get_linear().predict(X)
            metrics["linear_regression"] = {
                "name":  "Linear Regression",
                "task":  "Regression (Final Exam Score)",
                "mae":   round(mean_absolute_error(y_true, y_pred), 4),
                "rmse":  round(np.sqrt(mean_squared_error(y_true, y_pred)), 4),
                "r2":    round(r2_score(y_true, y_pred), 4),
            }

        # ── Decision Tree ─────────────────────────────────────────────────
        if "Pass/Fail" in df.columns:
            pass_enc = joblib.load(config.PASS_ENCODER_PATH)
            y_true   = pass_enc.transform(df["Pass/Fail"].values)
            y_pred = model_loader.get_decision_tree().predict(X)
            metrics["decision_tree"] = {
                "name":      "Decision Tree",
                "task":      "Classification (Pass/Fail)",
                "accuracy":  round(accuracy_score(y_true, y_pred), 4),
                "f1":        round(f1_score(y_true, y_pred, average="weighted"), 4),
                "precision": round(precision_score(y_true, y_pred, average="weighted"), 4),
                "recall":    round(recall_score(y_true, y_pred, average="weighted"), 4),
            }

        # ── KNN ──────────────────────────────────────────────────────
        if "Performance Category" in df.columns:
            perf_enc = joblib.load(config.PERFORMANCE_ENCODER_PATH)
            y_true   = perf_enc.transform(df["Performance Category"].values)
            y_pred = model_loader.get_knn().predict(X)
            metrics["knn"] = {
                "name":      "K-Nearest Neighbours",
                "task":      "Classification (Performance Category)",
                "accuracy":  round(accuracy_score(y_true, y_pred), 4),
                "f1":        round(f1_score(y_true, y_pred, average="weighted"), 4),
                "precision": round(precision_score(y_true, y_pred, average="weighted"), 4),
                "recall":    round(recall_score(y_true, y_pred, average="weighted"), 4),
            }

        # ── K-Means ──────────────────────────────────────────
        cluster_labels = model_loader.get_kmeans().predict(X)
        metrics["kmeans"] = {
            "name":             "K-Means Clustering",
            "task":             "Clustering (Academic Risk Groups)",
            "silhouette_score": round(silhouette_score(X, cluster_labels), 4),
            "inertia":          round(float(model_loader.get_kmeans().inertia_), 4),
            "n_clusters":       int(model_loader.get_kmeans().n_clusters),
        }

        return {"status": "ok", "metrics": metrics}

    except Exception as e:
        return {"status": "error", "message": str(e)}
