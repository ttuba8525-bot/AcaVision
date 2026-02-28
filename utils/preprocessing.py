import os
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# =========================================
# Absolute Path Setup
# =========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "student_synthetic_data.csv")

# =========================================
# Global Objects
# =========================================
scaler = StandardScaler()
participation_encoder = LabelEncoder()
extra_encoder = LabelEncoder()
pass_encoder = LabelEncoder()
performance_encoder = LabelEncoder()


# =========================================
# Load CSV + Handle Nulls
# =========================================
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Fill numeric nulls
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Fill categorical nulls
    df.fillna("Medium", inplace=True)

    return df


# =========================================
# Train/Test Split Utility
# =========================================
def preprocess_and_split(test_size=0.2, random_state=42):
    df = load_data()

    # Encode categorical input features
    df["Participation Level"] = participation_encoder.fit_transform(df["Participation Level"])
    df["Extra Curricular"] = extra_encoder.fit_transform(df["Extra Curricular"])

    # Encode categorical targets
    df["Pass/Fail"] = pass_encoder.fit_transform(df["Pass/Fail"])
    df["Performance Category"] = performance_encoder.fit_transform(df["Performance Category"])

    feature_cols = [
        "Attendance (%)",
        "Study Hours (per day)",
        "Assignment Score",
        "Previous GPA",
        "Participation Level",
        "Internet Usage (hrs/day)",
        "Sleep Hours",
        "Family Support Index",
        "Extra Curricular"
    ]

    X = df[feature_cols]
    y_score = df["Final Exam Score"]
    y_pass = df["Pass/Fail"]
    y_perf = df["Performance Category"]

    # Apply StandardScaler
    X_scaled = scaler.fit_transform(X)

    # Save preprocessing objects
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

    joblib.dump(scaler, os.path.join(BASE_DIR, "models", "scaler.pkl"))
    joblib.dump(participation_encoder, os.path.join(BASE_DIR, "models", "participation_encoder.pkl"))
    joblib.dump(extra_encoder, os.path.join(BASE_DIR, "models", "extra_encoder.pkl"))
    joblib.dump(pass_encoder, os.path.join(BASE_DIR, "models", "pass_encoder.pkl"))
    joblib.dump(performance_encoder, os.path.join(BASE_DIR, "models", "performance_encoder.pkl"))

    return train_test_split(
        X_scaled,
        y_score,
        y_pass,
        y_perf,
        test_size=test_size,
        random_state=random_state
    )


# =========================================
# SCALER ACCESSOR (used by clustering_service & metrics_service)
# =========================================
def get_scaler():
    """Returns the saved StandardScaler from models/scaler.pkl."""
    return joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))


# =========================================
# REQUIRED FUNCTION (DO NOT CHANGE NAME)
# =========================================
def get_feature_array(form_data: dict) -> np.ndarray:
    """
    Takes raw user input dict → returns scaled array ready for model.predict()
    """

    scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
    participation_encoder = joblib.load(os.path.join(BASE_DIR, "models", "participation_encoder.pkl"))
    extra_encoder = joblib.load(os.path.join(BASE_DIR, "models", "extra_encoder.pkl"))

    input_df = pd.DataFrame([{
        "Attendance (%)": float(form_data["attendance"]),
        "Study Hours (per day)": float(form_data["study_hours"]),
        "Assignment Score": float(form_data["assignment_score"]),
        "Previous GPA": float(form_data["previous_gpa"]),
        "Participation Level": form_data["participation_level"],
        "Internet Usage (hrs/day)": float(form_data["internet_usage"]),
        "Sleep Hours": float(form_data["sleep_hours"]),
        "Family Support Index": int(form_data["family_support"]),
        "Extra Curricular": form_data["extra_curricular"]
    }])

    input_df["Participation Level"] = participation_encoder.transform(input_df["Participation Level"])
    input_df["Extra Curricular"] = extra_encoder.transform(input_df["Extra Curricular"])

    return scaler.transform(input_df)