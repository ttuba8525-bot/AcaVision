"""
generate_data.py
Generates a realistic student dataset with a proper Pass/Fail split (~65% Pass, ~35% Fail).
Run from the project root: python data/generate_data.py
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 1500

# ── Features ──────────────────────────────────────────────────────────────────
attendance          = np.random.uniform(30, 100, n)       # wide range → some low
study_hours         = np.random.uniform(0, 10, n)         # 0–10 hrs/day
assignment_scores   = np.random.uniform(20, 100, n)       # some very low
previous_gpa        = np.random.uniform(2, 10, n)         # some failing GPAs
participation_level = np.random.choice(["Low", "Medium", "High"], n, p=[0.35, 0.40, 0.25])
internet_usage      = np.random.uniform(0, 12, n)
sleep_hours         = np.random.uniform(3, 10, n)
family_support      = np.random.randint(1, 11, n)
extra_curricular    = np.random.choice(["Yes", "No"], n, p=[0.45, 0.55])

# Participation numeric map
part_map = {"Low": 2, "Medium": 5, "High": 9}
participation_numeric = np.array([part_map[p] for p in participation_level])

# ── Exam Score formula with noise ─────────────────────────────────────────────
raw_score = (
    0.30 * attendance           +   # attendance matters most
    4.00 * study_hours          +   # study hours big driver
    0.18 * assignment_scores    +
    2.50 * previous_gpa         +
    1.80 * participation_numeric -
    1.20 * internet_usage       +
    1.20 * sleep_hours          +
    1.00 * family_support       +
    np.random.normal(0, 6, n)       # realistic noise
)

# Normalise to 0–100 (don't clip hard — let the formula spread)
score_min, score_max = raw_score.min(), raw_score.max()
final_exam_score = (raw_score - score_min) / (score_max - score_min) * 100
final_exam_score = np.clip(final_exam_score, 0, 100).round(2)

# ── Labels ────────────────────────────────────────────────────────────────────
# Threshold at 50 → gives roughly 60-65% Pass, 35-40% Fail
pass_fail = np.where(final_exam_score >= 50, "Pass", "Fail")

performance_category = []
for score in final_exam_score:
    if score < 40:
        performance_category.append("Low")
    elif score < 65:
        performance_category.append("Medium")
    else:
        performance_category.append("High")

# ── DataFrame ─────────────────────────────────────────────────────────────────
df = pd.DataFrame({
    "Attendance (%)":           attendance.round(2),
    "Study Hours (per day)":    study_hours.round(2),
    "Assignment Score":         assignment_scores.round(2),
    "Previous GPA":             previous_gpa.round(2),
    "Participation Level":      participation_level,
    "Internet Usage (hrs/day)": internet_usage.round(2),
    "Sleep Hours":              sleep_hours.round(2),
    "Family Support Index":     family_support,
    "Extra Curricular":         extra_curricular,
    "Final Exam Score":         final_exam_score,
    "Pass/Fail":                pass_fail,
    "Performance Category":     performance_category,
})

# Save to project data folder
out_path = os.path.join(os.path.dirname(__file__), "student_synthetic_data.csv")
df.to_csv(out_path, index=False)

print(f"Dataset saved → {out_path}")
print(f"Shape: {df.shape}")
print(f"\nPass/Fail distribution:\n{df['Pass/Fail'].value_counts()}")
print(f"\nPerformance distribution:\n{df['Performance Category'].value_counts()}")
print(f"\nScore stats:\n{df['Final Exam Score'].describe().round(2)}")
