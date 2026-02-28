# ============================================================
#  config.py — AckVision Central Configuration
#  All paths, constants, and settings live here.
#  Every other module imports from this file.
# ============================================================

import os

# ── Base Directory ───────────────────────────────────────────
# Resolves to the project root (wherever app.py lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Flask Settings ───────────────────────────────────────────
SECRET_KEY = "ackvision-secret-2024"
DEBUG      = True                  # Set False in production

# ── Dataset Path ─────────────────────────────────────────────
DATA_PATH = os.path.join(BASE_DIR, "data", "student_synthetic_data.csv")

# ── Model Paths ──────────────────────────────────────────────
LINEAR_MODEL_PATH   = os.path.join(BASE_DIR, "models", "linear.pkl")
DT_MODEL_PATH       = os.path.join(BASE_DIR, "models", "decision_tree.pkl")
KNN_MODEL_PATH      = os.path.join(BASE_DIR, "models", "knn.pkl")
KMEANS_MODEL_PATH   = os.path.join(BASE_DIR, "models", "kmeans.pkl")

# ── Encoder / Scaler Paths (saved by Dev 1's preprocessing.py) ──
SCALER_PATH                 = os.path.join(BASE_DIR, "models", "scaler.pkl")
PARTICIPATION_ENCODER_PATH  = os.path.join(BASE_DIR, "models", "participation_encoder.pkl")
EXTRA_ENCODER_PATH          = os.path.join(BASE_DIR, "models", "extra_encoder.pkl")
PASS_ENCODER_PATH           = os.path.join(BASE_DIR, "models", "pass_encoder.pkl")
PERFORMANCE_ENCODER_PATH    = os.path.join(BASE_DIR, "models", "performance_encoder.pkl")

# ── Feature Column Order ─────────────────────────────────────
# MUST match the exact column order used by Dev 1 during training.
# These are the ACTUAL CSV column headers from student_synthetic_data.csv.
FEATURE_COLUMNS = [
    "Attendance (%)",           # 0 – 100
    "Study Hours (per day)",    # 0 – 12
    "Assignment Score",         # 0 – 100
    "Previous GPA",             # 0 – 10
    "Participation Level",      # Low / Medium / High (encoded)
    "Internet Usage (hrs/day)", # 0 – 12
    "Sleep Hours",              # 3 – 10
    "Family Support Index",     # 1 – 10
    "Extra Curricular",         # Yes / No (encoded)
]

# ── Target Label Mappings ────────────────────────────────────
# Used by prediction_service and clustering_service
#   to decode model outputs back to human-readable labels.

# Dev 1 used LabelEncoder on Pass/Fail — encoded alphabetically: Fail=0, Pass=1
PASS_FAIL_LABELS = {0: "Fail", 1: "Pass"}

# Dev 1's Performance Category values in CSV: Low, Medium, High
# LabelEncoder encodes alphabetically: High=0, Low=1, Medium=2
PERFORMANCE_LABELS = {
    0: "High",
    1: "Low",
    2: "Medium",
}

# K-Means cluster → risk label mapping.
# Verify cluster centroids after testing — swap if labels seem reversed.
RISK_LABELS = {
    0: "High Risk",
    1: "Medium Risk",
    2: "Low Risk",
}

# ── Upload Settings ───────────────────────────────────────────
UPLOAD_FOLDER    = os.path.join(BASE_DIR, "data", "uploads")
ALLOWED_EXTENSIONS = {"csv"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024   # 5 MB upload limit
