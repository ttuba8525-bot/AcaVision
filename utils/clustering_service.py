# ============================================================
#  utils/clustering_service.py — AckVision Clustering Service
#  Assigns a student to an Academic Risk Group using K-Means.
#  Risk Groups: High Risk / Medium Risk / Low Risk
# ============================================================

import config
from utils import model_loader
from utils.preprocessing import get_feature_array


def assign_risk_cluster(form_data: dict) -> str:
    """
    Assign the student to an Academic Risk Group using K-Means.

    Args:
        form_data: dict with keys matching config.FEATURE_COLUMNS

    Returns:
        One of: "High Risk", "Medium Risk", "Low Risk"
        (decoded using config.RISK_LABELS)

    Note:
        The cluster → label mapping in config.RISK_LABELS depends on
        the centroid ordering from Dev 1's training. If predictions seem
        reversed, swap the label assignments in config.RISK_LABELS.
    """
    features   = get_feature_array(form_data)
    model      = model_loader.get_kmeans()
    cluster_id = int(model.predict(features)[0])
    return config.RISK_LABELS.get(cluster_id, "Unknown")


def get_cluster_data_for_visualization() -> dict:
    """
    Returns raw cluster assignment data for all records in the dataset.
    Used by the /visualize route to generate the scatter plot.
    """
    import pandas as pd
    import joblib
    from utils.preprocessing import get_scaler

    try:
        df      = pd.read_csv(config.DATA_PATH)
        model   = model_loader.get_kmeans()
        scaler  = get_scaler()

        part_enc  = joblib.load(config.PARTICIPATION_ENCODER_PATH)
        extra_enc = joblib.load(config.EXTRA_ENCODER_PATH)

        # Encode categoricals before scaling — same as training
        df["Participation Level"] = part_enc.transform(df["Participation Level"])
        df["Extra Curricular"]    = extra_enc.transform(df["Extra Curricular"])

        X_scaled    = scaler.transform(df[config.FEATURE_COLUMNS].values)
        cluster_ids = model.predict(X_scaled).tolist()
        labels      = [config.RISK_LABELS.get(c, "Unknown") for c in cluster_ids]

        return {
            "cluster_ids": cluster_ids,
            "labels":      labels,
            "attendance":  df["Attendance (%)"].tolist(),
            "study_hours": df["Study Hours (per day)"].tolist(),
        }

    except Exception as e:
        return {"error": str(e)}
