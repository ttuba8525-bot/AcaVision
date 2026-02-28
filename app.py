# ============================================================
#  app.py — AckVision Main Flask Application
#  All routes live here. ML logic is handled by utils/.
# ============================================================

from flask import Flask, request, jsonify, render_template
import config
from utils import model_loader
from utils import prediction_service, clustering_service
from utils.advisory import get_advisory, get_summary_badge

# ── App Initialisation ───────────────────────────────────────
app = Flask(__name__)
app.secret_key          = config.SECRET_KEY
app.config["DEBUG"]     = config.DEBUG
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

# Load all ML models once at startup
model_loader.load_all()


# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def index():
    """Home / Landing page."""
    return render_template("index.html")


@app.route("/landing")
def landing():
    """EduInsight standalone landing page."""
    from flask import send_from_directory
    import os
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "eduinsight_landing.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    GET  → Render the prediction form page.
    POST → Accept JSON form data, run all models, return predictions.
    """
    if request.method == "GET":
        return render_template("prediction.html")

    # ── Parse incoming data ───────────────────────────────────
    data = request.get_json(silent=True) or request.form.to_dict()

    if not data:
        return jsonify({"error": "No input data received."}), 400

    # ── Validate required fields ──────────────────────────────
    # Keys must match what preprocessing.get_feature_array() reads from form_data
    REQUIRED_KEYS = [
        "attendance", "study_hours", "assignment_score",
        "previous_gpa", "participation_level", "internet_usage",
        "sleep_hours", "family_support", "extra_curricular",
    ]
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        # ── Run all predictions ───────────────────────────────
        exam_score   = prediction_service.predict_exam_score(data)
        pass_fail    = prediction_service.predict_pass_fail(data)
        performance  = prediction_service.predict_performance(data)
        risk_cluster = clustering_service.assign_risk_cluster(data)

        # ── Generate advisory ─────────────────────────────────
        advisory     = get_advisory(exam_score, pass_fail, performance, risk_cluster, data)
        badge        = get_summary_badge(pass_fail, risk_cluster)

        return jsonify({
            "exam_score":   exam_score,
            "pass_fail":    pass_fail,
            "performance":  performance,
            "risk_cluster": risk_cluster,
            "advisory":     advisory,
            "badge":        badge,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/metrics")
def metrics():
    """
    GET → Returns model evaluation metrics as JSON.
    Also renders the metrics page when accessed directly via browser.
    """
    if request.headers.get("Accept") == "application/json":
        # Return raw JSON for the frontend JS to fetch
        from utils.metrics_service import get_all_metrics
        return jsonify(get_all_metrics())

    return render_template("metrics.html")


@app.route("/api/metrics")
def api_metrics():
    """JSON-only metrics endpoint for the frontend to fetch."""
    from utils.metrics_service import get_all_metrics
    return jsonify(get_all_metrics())


@app.route("/visualize")
def visualize():
    """
    GET → Renders the visualization dashboard page.
    """
    return render_template("visualization.html")


@app.route("/api/visualize")
def api_visualize():
    """
    JSON-only endpoint for chart data.
    Frontend fetches this to render Chart.js plots.
    """
    import pandas as pd

    try:
        df = pd.read_csv(config.DATA_PATH)

        cluster_data = clustering_service.get_cluster_data_for_visualization()

        # Use actual CSV column names (Dev 1's headers with spaces)
        performance_counts = df["Performance Category"].value_counts().to_dict() \
            if "Performance Category" in df.columns else {}

        pass_fail_counts = df["Pass/Fail"].value_counts().to_dict() \
            if "Pass/Fail" in df.columns else {}

        return jsonify({
            "clusters":    cluster_data,
            "performance": performance_counts,
            "pass_fail":   pass_fail_counts,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/advisory", methods=["POST"])
def advisory():
    """
    POST → Return standalone advisory messages for given predictions.
    Expects JSON: { exam_score, pass_fail, performance, risk_cluster, ...form_data }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided."}), 400

    tips = get_advisory(
        exam_score   = float(data.get("exam_score", 0)),
        pass_fail    = data.get("pass_fail", ""),
        performance  = data.get("performance", ""),
        risk_cluster = data.get("risk_cluster", ""),
        form_data    = data,
    )
    return jsonify({"advisory": tips})


@app.route("/upload", methods=["POST"])
def upload():
    """
    POST → Accept a CSV file upload, run predictions on all rows,
           return batch results as JSON.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if file.filename == "" or not file.filename.endswith(".csv"):
        return jsonify({"error": "Please upload a valid .csv file."}), 400

    try:
        import pandas as pd

        df = pd.read_csv(file)

        # Support both header styles: "attendance" (app style) or "Attendance (%)" (CSV style)
        COL_MAP = {
            "Attendance (%)":           "attendance",
            "Study Hours (per day)":    "study_hours",
            "Assignment Score":         "assignment_score",
            "Previous GPA":             "previous_gpa",
            "Participation Level":      "participation_level",
            "Internet Usage (hrs/day)": "internet_usage",
            "Sleep Hours":              "sleep_hours",
            "Family Support Index":     "family_support",
            "Extra Curricular":         "extra_curricular",
        }
        # Rename CSV-style headers to app-style keys if present
        df.rename(columns=COL_MAP, inplace=True)

        REQUIRED = ["attendance","study_hours","assignment_score","previous_gpa",
                    "participation_level","internet_usage","sleep_hours",
                    "family_support","extra_curricular"]
        missing_cols = [c for c in REQUIRED if c not in df.columns]
        if missing_cols:
            return jsonify({"error": f"CSV missing columns: {missing_cols}"}), 400

        results = []
        for _, row in df.iterrows():
            row_dict     = row.to_dict()
            exam_score   = prediction_service.predict_exam_score(row_dict)
            pass_fail    = prediction_service.predict_pass_fail(row_dict)
            performance  = prediction_service.predict_performance(row_dict)
            risk_cluster = clustering_service.assign_risk_cluster(row_dict)
            advisory_list = get_advisory(exam_score, pass_fail, performance, risk_cluster, row_dict)

            results.append({
                **row_dict,
                "exam_score":   exam_score,
                "pass_fail":    pass_fail,
                "performance":  performance,
                "risk_cluster": risk_cluster,
                "advisory":     advisory_list,
            })

        return jsonify({"count": len(results), "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
