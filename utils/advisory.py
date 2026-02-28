# ============================================================
#  utils/advisory.py — AckVision Academic Advisory Engine
#  Generates personalised, rule-based academic suggestions
#  by combining all 4 model outputs.
#  No ML dependency — pure Python logic.
# ============================================================


def get_advisory(
    exam_score:   float,
    pass_fail:    str,
    performance:  str,
    risk_cluster: str,
    form_data:    dict = None,
) -> list:
    """
    Generate a list of personalised advisory messages for a student.

    Args:
        exam_score   : Predicted final exam score (0–100)
        pass_fail    : "Pass" or "Fail"
        performance  : "Excellent" | "Good" | "Average" | "Poor"
        risk_cluster : "High Risk" | "Medium Risk" | "Low Risk"
        form_data    : Optional original form data for feature-level tips

    Returns:
        List of advisory strings (3–7 messages depending on situation)
    """
    tips = []

    # ── Score-based advice ────────────────────────────────────
    if exam_score >= 85:
        tips.append("🏆 Outstanding predicted score! Keep up your excellent work.")
    elif exam_score >= 70:
        tips.append("📈 Good predicted score. A little more effort could push you to excellence.")
    elif exam_score >= 50:
        tips.append("⚠️  Borderline score predicted. Focus on weak subjects immediately.")
    else:
        tips.append("🚨 Critical: Very low score predicted. Seek academic support urgently.")

    # ── Pass/Fail advice ─────────────────────────────────────
    if pass_fail == "Fail":
        tips.append("❌ You are at risk of failing. Prioritise exam preparation over all else.")
    else:
        tips.append("✅ On track to pass. Maintain consistency to secure the result.")

    # ── Performance category advice ──────────────────────────
    perf_tips = {
        "Excellent": "🌟 Excellent performer! Consider mentoring peers or exploring advanced topics.",
        "Good":      "👍 Good performance. Target Excellent by improving weaker subjects.",
        "Average":   "📚 Average performance. Create a structured daily study plan.",
        "Poor":      "🆘 Poor performance detected. Reduce distractions and seek teacher guidance.",
    }
    tips.append(perf_tips.get(performance, "Keep working hard!"))

    # ── Risk cluster advice ──────────────────────────────────
    risk_tips = {
        "High Risk":   "🔴 High academic risk. Attend all classes and submit all assignments on time.",
        "Medium Risk": "🟡 Moderate risk. Small improvements in attendance and study hours will help.",
        "Low Risk":    "🟢 Low risk. Stay consistent and avoid last-minute studying.",
    }
    tips.append(risk_tips.get(risk_cluster, ""))

    # ── Feature-level tips (if raw form data is provided) ─────
    if form_data:
        attendance = float(form_data.get("attendance_percentage", 100))
        study_hrs  = float(form_data.get("study_hours", 6))
        sleep_hrs  = float(form_data.get("sleep_hours", 7))
        internet   = float(form_data.get("internet_usage", 4))

        if attendance < 75:
            tips.append(f"📅 Attendance is {attendance:.0f}% — below the 75% minimum. Attend more classes.")
        if study_hrs < 4:
            tips.append(f"📖 Only {study_hrs:.1f} study hours/day. Aim for at least 4–6 hours.")
        if sleep_hrs < 6:
            tips.append(f"😴 Sleeping only {sleep_hrs:.1f} hours. Poor sleep reduces memory retention.")
        if internet > 8:
            tips.append(f"📱 {internet:.1f} hours of internet usage/day is high. Reduce screen time.")

    return [t for t in tips if t]  # Remove any empty strings


def get_summary_badge(pass_fail: str, risk_cluster: str) -> dict:
    """
    Returns colour and emoji metadata for displaying result cards in the UI.

    Returns:
        dict with keys: color (CSS class name), emoji
    """
    if pass_fail == "Fail" or risk_cluster == "High Risk":
        return {"color": "danger",  "emoji": "🔴"}
    elif risk_cluster == "Medium Risk":
        return {"color": "warning", "emoji": "🟡"}
    else:
        return {"color": "success", "emoji": "🟢"}
