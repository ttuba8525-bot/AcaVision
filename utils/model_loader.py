# ============================================================
#  utils/model_loader.py — AckVision Model Loader
#  Loads all 4 trained .pkl models once at app startup.
#  All service modules call the getter functions here.
# ============================================================

import joblib
import config

# Internal model registry — populated by load_all()
_models = {}


def load_all():
    """
    Load all 4 ML models from disk into memory.
    Called once when Flask app starts (in app.py).
    Raises FileNotFoundError with a clear message if any model is missing.
    """
    model_paths = {
        "linear":  config.LINEAR_MODEL_PATH,
        "dt":      config.DT_MODEL_PATH,
        "knn":     config.KNN_MODEL_PATH,
        "kmeans":  config.KMEANS_MODEL_PATH,
    }

    for name, path in model_paths.items():
        try:
            _models[name] = joblib.load(path)
            print(f"[model_loader] ✓ Loaded '{name}' from {path}")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"[model_loader] ✗ Model file not found: {path}\n"
                f"  → Make sure Dev 1 has trained and saved all models first."
            )


# ── Getters ─────────────────────────────────────────────────
# Each getter returns the corresponding loaded model object.
# Raises RuntimeError if load_all() was never called.

def _get(key):
    if key not in _models:
        raise RuntimeError(
            f"[model_loader] Model '{key}' not loaded. "
            "Call model_loader.load_all() before accessing models."
        )
    return _models[key]


def get_linear():
    """Returns the trained LinearRegression model."""
    return _get("linear")


def get_decision_tree():
    """Returns the trained DecisionTreeClassifier model."""
    return _get("dt")


def get_knn():
    """Returns the trained KNeighborsClassifier model."""
    return _get("knn")


def get_kmeans():
    """Returns the trained KMeans clustering model."""
    return _get("kmeans")


def is_loaded():
    """Returns True if all 4 models have been loaded successfully."""
    return len(_models) == 4
