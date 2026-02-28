import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n = 1200

# Generate independent features
attendance = np.random.uniform(50, 100, n)  # percentage
study_hours = np.random.uniform(1, 8, n)  # hours per day
assignment_scores = np.random.uniform(40, 100, n)
previous_gpa = np.random.uniform(4, 10, n)
participation_level = np.random.choice(["Low", "Medium", "High"], n)
internet_usage = np.random.uniform(1, 10, n)  # hours per day
sleep_hours = np.random.uniform(4, 9, n)
family_support = np.random.randint(1, 11, n)
extra_curricular = np.random.choice(["Yes", "No"], n)

# Convert participation to numeric for calculation
participation_numeric = []
for level in participation_level:
    if level == "Low":
        participation_numeric.append(2)
    elif level == "Medium":
        participation_numeric.append(5)
    else:
        participation_numeric.append(8)

participation_numeric = np.array(participation_numeric)

# Create final exam score with realistic logic
final_exam_score = (
    0.25 * attendance +
    5 * study_hours +
    0.2 * assignment_scores +
    2 * previous_gpa +
    2 * participation_numeric -
    1.5 * internet_usage +
    1.5 * sleep_hours +
    1.5 * family_support +
    np.random.normal(0, 5, n)  # noise
)

# Normalize score between 0–100
final_exam_score = np.clip(final_exam_score, 0, 100)

# Pass/Fail
pass_fail = np.where(final_exam_score >= 40, "Pass", "Fail")

# Performance Category
performance_category = []
for score in final_exam_score:
    if score < 50:
        performance_category.append("Low")
    elif score < 75:
        performance_category.append("Medium")
    else:
        performance_category.append("High")

# Create DataFrame
df = pd.DataFrame({
    "Attendance (%)": attendance,
    "Study Hours (per day)": study_hours,
    "Assignment Score": assignment_scores,
    "Previous GPA": previous_gpa,
    "Participation Level": participation_level,
    "Internet Usage (hrs/day)": internet_usage,
    "Sleep Hours": sleep_hours,
    "Family Support Index": family_support,
    "Extra Curricular": extra_curricular,
    "Final Exam Score": final_exam_score,
    "Pass/Fail": pass_fail,
    "Performance Category": performance_category
})

# Round numeric columns
df = df.round(2)

# Save to CSV
df.to_csv("student_synthetic_data.csv", index=False)

print("Dataset generated successfully!")
print("Shape of dataset:", df.shape)
print("\nSample data:")
print(df.head())