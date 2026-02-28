"""
train_models.py  —  AckVision Model Training Script
Run from the project root: python train_models.py
Trains all 4 models and saves encoders/scaler to models/
"""
import os, sys
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_absolute_error, r2_score,
    accuracy_score, classification_report
)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "student_synthetic_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("=" * 60)
print(" AckVision — Model Training")
print("=" * 60)

# ── Load & inspect ────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"\nLoaded {len(df)} rows from {DATA_PATH}")
print(f"Pass/Fail:\n{df['Pass/Fail'].value_counts()}")
print(f"Performance:\n{df['Performance Category'].value_counts()}")

# ── Encode categorical features ───────────────────────────────────
part_enc  = LabelEncoder()
extra_enc = LabelEncoder()
pass_enc  = LabelEncoder()
perf_enc  = LabelEncoder()

df["Participation Level"] = part_enc.fit_transform(df["Participation Level"])
df["Extra Curricular"]    = extra_enc.fit_transform(df["Extra Curricular"])
df["Pass/Fail"]           = pass_enc.fit_transform(df["Pass/Fail"])
df["Performance Category"]= perf_enc.fit_transform(df["Performance Category"])

print(f"\nPass/Fail encoder classes: {list(pass_enc.classes_)}")
print(f"  → class indices:         {list(range(len(pass_enc.classes_)))}")
print(f"Performance encoder classes: {list(perf_enc.classes_)}")

FEATURE_COLS = [
    "Attendance (%)",
    "Study Hours (per day)",
    "Assignment Score",
    "Previous GPA",
    "Participation Level",
    "Internet Usage (hrs/day)",
    "Sleep Hours",
    "Family Support Index",
    "Extra Curricular",
]

X = df[FEATURE_COLS]
y_score = df["Final Exam Score"]
y_pass  = df["Pass/Fail"]
y_perf  = df["Performance Category"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, ys_tr, ys_te, yp_tr, yp_te, yq_tr, yq_te = train_test_split(
    X_scaled, y_score, y_pass, y_perf, test_size=0.2, random_state=42
)

# ── 1. Linear Regression ──────────────────────────────────────────
lr = LinearRegression()
lr.fit(X_train, ys_tr)
ys_pred = lr.predict(X_test)
print(f"\nLinear Regression  MAE={mean_absolute_error(ys_te, ys_pred):.2f}  R²={r2_score(ys_te, ys_pred):.4f}")

# ── 2. Decision Tree (Pass/Fail) ──────────────────────────────────
dt = DecisionTreeClassifier(max_depth=6, random_state=42)
dt.fit(X_train, yp_tr)
yp_pred = dt.predict(X_test)
print(f"Decision Tree      Acc={accuracy_score(yp_te, yp_pred):.4f}")
print(classification_report(yp_te, yp_pred, target_names=pass_enc.classes_))

# ── 3. KNN (Performance Category) ────────────────────────────────
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train, yq_tr)
yq_pred = knn.predict(X_test)
print(f"KNN                Acc={accuracy_score(yq_te, yq_pred):.4f}")

# ── 4. K-Means (Risk Clusters) ────────────────────────────────────
km = KMeans(n_clusters=3, random_state=42, n_init=10)
km.fit(X_scaled)
# Map clusters by mean score (0=lowest→High Risk, 2=highest→Low Risk)
cluster_means = {c: y_score[km.labels_ == c].mean() for c in range(3)}
sorted_clusters = sorted(cluster_means, key=cluster_means.get)  # low→high score
risk_map = {
    sorted_clusters[0]: 2,   # lowest score  → High Risk (label 2)
    sorted_clusters[1]: 1,   # middle score  → Medium Risk (label 1)
    sorted_clusters[2]: 0,   # highest score → Low Risk (label 0)
}
print(f"\nK-Means cluster score means: {cluster_means}")
print(f"Cluster→risk map: {risk_map}")

# ── Save all artefacts ────────────────────────────────────────────
joblib.dump(lr,        os.path.join(MODELS_DIR, "linear.pkl"))
joblib.dump(dt,        os.path.join(MODELS_DIR, "decision_tree.pkl"))
joblib.dump(knn,       os.path.join(MODELS_DIR, "knn.pkl"))
joblib.dump(km,        os.path.join(MODELS_DIR, "kmeans.pkl"))
joblib.dump(scaler,    os.path.join(MODELS_DIR, "scaler.pkl"))
joblib.dump(part_enc,  os.path.join(MODELS_DIR, "participation_encoder.pkl"))
joblib.dump(extra_enc, os.path.join(MODELS_DIR, "extra_encoder.pkl"))
joblib.dump(pass_enc,  os.path.join(MODELS_DIR, "pass_encoder.pkl"))
joblib.dump(perf_enc,  os.path.join(MODELS_DIR, "performance_encoder.pkl"))
# Save risk map so app can use proper cluster→label mapping
joblib.dump(risk_map,  os.path.join(MODELS_DIR, "risk_map.pkl"))

print("\nAll models & encoders saved to models/")
print("=" * 60)
print(f"Pass encoder classes  : {list(pass_enc.classes_)}")
print(f"  Fail → {pass_enc.transform(['Fail'])[0]}   Pass → {pass_enc.transform(['Pass'])[0]}")
print(f"Performance classes   : {list(perf_enc.classes_)}")
