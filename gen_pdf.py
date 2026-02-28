from fpdf import FPDF, XPos, YPos

# ── Colours ──────────────────────────────────────────────────
NAVY   = (26, 31, 94)
BLUE   = (45, 52, 148)
LIGHT  = (76, 86, 214)
WHITE  = (255, 255, 255)
BG     = (244, 246, 251)
TEXT   = (30, 35, 64)
GREY   = (100, 110, 150)
GREEN  = (26, 122, 69)
LGREY  = (232, 234, 248)
CODEBG = (30, 35, 64)
CODECL = (168, 240, 168)

class PDF(FPDF):
    def header(self): pass
    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GREY)
        self.cell(0, 10, "AckVision · Student Academic Performance Prediction System · Dev 1 Brief", align="C")

def pill(pdf, text, x, y, w=38, h=8, bg=LGREY, fg=BLUE):
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*bg)
    pdf.set_text_color(*fg)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, border=0, fill=True, align="C",
             new_x=XPos.RIGHT, new_y=YPos.TOP)

def section_header(pdf, icon, title, highlight):
    pdf.set_fill_color(*WHITE)
    pdf.set_draw_color(*LGREY)
    pdf.rect(10, pdf.get_y(), 190, 10, "F")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(12, pdf.get_y() + 1)
    pdf.cell(0, 8, f"{icon}  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*LIGHT)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

def code_block(pdf, lines):
    pdf.set_fill_color(*CODEBG)
    x0, y0 = 14, pdf.get_y()
    block_h = len(lines) * 5.5 + 8
    pdf.rect(x0, y0, 183, block_h, "F")
    pdf.set_text_color(*CODECL)
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(x0 + 4, y0 + 4)
    for line in lines:
        pdf.cell(175, 5.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(x0 + 4)
    pdf.ln(4)

def card_start(pdf, margin=10):
    pdf.set_fill_color(*WHITE)
    Card_y = pdf.get_y()
    return Card_y

def bullet(pdf, text, indent=16):
    pdf.set_text_color(*BLUE)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_x(indent)
    pdf.cell(5, 6, chr(149))
    pdf.set_text_color(*TEXT)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(175 - indent, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ── Build PDF ─────────────────────────────────────────────────
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(10, 10, 10)

# ── HEADER BANNER ─────────────────────────────────────────────
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 52, "F")
pdf.set_fill_color(*LIGHT)
pdf.rect(0, 46, 210, 4, "F")

pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 7)
pdf.set_xy(10, 8)
pdf.set_fill_color(76, 86, 214)
pdf.cell(36, 5.5, "  AckVision PROJECT  ", border=1, fill=True, align="C")

pdf.set_font("Helvetica", "B", 20)
pdf.set_xy(10, 17)
pdf.cell(0, 10, "Developer 1 - Task Summary")

pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(200, 205, 240)
pdf.set_xy(10, 30)
pdf.cell(0, 7, "ML & Data Layer  |  Student Academic Performance Prediction System")

pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(180, 185, 230)
pdf.set_xy(10, 40)
pdf.cell(60, 5, "Role: ML Engineer / Data Layer")
pdf.set_x(78)
pdf.cell(60, 5, "Branch: dev1/data-and-models")
pdf.set_x(150)
pdf.cell(50, 5, "Handoff before Dev 2 starts")

pdf.set_y(58)

# ── GIT SETUP ─────────────────────────────────────────────────
pdf.set_fill_color(*NAVY)
pdf.rect(10, pdf.get_y(), 190, 7, "F")
pdf.set_text_color(124, 133, 201)
pdf.set_font("Helvetica", "B", 7.5)
pdf.set_xy(14, pdf.get_y() + 1.5)
pdf.cell(0, 5, "⚡  GIT SETUP — RUN THESE COMMANDS FIRST")
pdf.ln(8)

code_block(pdf, [
    "git clone https://github.com/ttuba8525-bot/AcaVision.git",
    "cd AcaVision",
    "git checkout -b dev1/data-and-models",
])

# ── FILES YOU OWN ─────────────────────────────────────────────
pdf.set_fill_color(*LGREY)
pdf.rect(10, pdf.get_y(), 190, 8, "F")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 11)
pdf.set_xy(14, pdf.get_y() + 1)
pdf.cell(0, 6, "📁  Files You Own")
pdf.ln(10)

files = [
    "utils/data_generator.py",
    "utils/preprocessing.py",
    "data/synthetic_data.csv",
    "models/linear.pkl",
    "models/decision_tree.pkl",
    "models/knn.pkl",
    "models/kmeans.pkl",
    "notebooks/model_training.ipynb",
    "requirements.txt",
]
cols = 2
col_w = 92
for i, f in enumerate(files):
    col = i % cols
    row = i // cols
    x = 12 + col * col_w
    y = pdf.get_y()
    pdf.set_fill_color(*LGREY)
    pdf.rect(x, y, col_w - 4, 7, "F")
    pdf.set_text_color(*BLUE)
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(x + 3, y + 1)
    pdf.cell(col_w - 8, 5, f)
    if col == cols - 1:
        pdf.ln(8)
if len(files) % cols != 0:
    pdf.ln(8)

pdf.ln(4)

# ── TASKS ─────────────────────────────────────────────────────
pdf.set_fill_color(*LGREY)
pdf.rect(10, pdf.get_y(), 190, 8, "F")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 11)
pdf.set_xy(14, pdf.get_y() + 1)
pdf.cell(0, 6, "✅  Tasks In Order")
pdf.ln(10)

# Task 1
pdf.set_fill_color(*LIGHT)
pdf.rect(12, pdf.get_y(), 6, 6, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 8)
pdf.set_xy(13, pdf.get_y() + 0.5)
pdf.cell(4, 5, "1", align="C")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(22)
pdf.cell(0, 6, "data_generator.py — Synthetic Dataset")
pdf.ln(7)

bullet(pdf, "Generate 1000+ synthetic student records using NumPy & Pandas")
bullet(pdf, "Features: Attendance %, Study Hours, Assignment Score, Previous GPA, Participation Level, Internet Usage, Sleep Hours, Family Support Index, Extra-Curricular (0/1)")
bullet(pdf, "Derive targets: Final Exam Score [continuous], Pass/Fail [binary], Performance Category [Excellent/Good/Average/Poor]")
bullet(pdf, "Save output → data/synthetic_data.csv")
pdf.ln(3)

# Task 2
pdf.set_fill_color(*LIGHT)
pdf.rect(12, pdf.get_y(), 6, 6, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 8)
pdf.set_xy(13, pdf.get_y() + 0.5)
pdf.cell(4, 5, "2", align="C")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(22)
pdf.cell(0, 6, "preprocessing.py — Feature Pipeline")
pdf.ln(7)

bullet(pdf, "Load CSV, handle nulls, apply StandardScaler on all features")
bullet(pdf, "Encode categorical targets with LabelEncoder where needed")
bullet(pdf, "Provide a train/test split utility function")
bullet(pdf, "MUST expose this exact function (Dev 2 depends on it):")
pdf.ln(1)
code_block(pdf, [
    "def get_feature_array(form_data: dict) -> np.ndarray:",
    '    """Takes raw user input dict -> returns scaled array ready for model.predict()"""',
    "    ...",
])

# Task 3
pdf.set_fill_color(*LIGHT)
pdf.rect(12, pdf.get_y(), 6, 6, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 8)
pdf.set_xy(13, pdf.get_y() + 0.5)
pdf.cell(4, 5, "3", align="C")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(22)
pdf.cell(0, 6, "Model Training — All 4 Models")
pdf.ln(7)

# Table header
headers = ["Type", "Algorithm", "Target Variable", "Key Metrics", "Save As"]
widths  = [22, 46, 40, 38, 42]
pdf.set_fill_color(*NAVY)
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 8.5)
pdf.set_x(12)
for h, w in zip(headers, widths):
    pdf.cell(w, 7, h, fill=True, border=0)
pdf.ln(7)

rows = [
    ("Regression",  "LinearRegression",         "Final Exam Score",    "R2, MAE, RMSE",     "models/linear.pkl"),
    ("Classifier",  "DecisionTreeClassifier",    "Pass / Fail",         "Accuracy, F1, AUC", "models/decision_tree.pkl"),
    ("Classifier",  "KNeighborsClassifier",      "Performance Category","Accuracy, F1",      "models/knn.pkl"),
    ("Clustering",  "KMeans (k=3)",              "Risk Group",          "Silhouette Score",  "models/kmeans.pkl"),
]
for i, row in enumerate(rows):
    pdf.set_fill_color(*(LGREY if i % 2 == 0 else WHITE))
    pdf.set_text_color(*TEXT)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_x(12)
    for val, w in zip(row, widths):
        pdf.cell(w, 6.5, val, fill=True, border=0)
    pdf.ln(6.5)

pdf.ln(3)
bullet(pdf, "Use joblib.dump(model, 'models/<name>.pkl') to save each trained model")
pdf.ln(2)
code_block(pdf, [
    "import joblib",
    "joblib.dump(linear_model,   'models/linear.pkl')",
    "joblib.dump(dt_model,       'models/decision_tree.pkl')",
    "joblib.dump(knn_model,      'models/knn.pkl')",
    "joblib.dump(kmeans_model,   'models/kmeans.pkl')",
])

# Task 4
pdf.set_fill_color(*LIGHT)
pdf.rect(12, pdf.get_y(), 6, 6, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 8)
pdf.set_xy(13, pdf.get_y() + 0.5)
pdf.cell(4, 5, "4", align="C")
pdf.set_text_color(*NAVY)
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(22)
pdf.cell(0, 6, "requirements.txt — Pin Dependencies")
pdf.ln(7)

reqs = ["flask", "scikit-learn", "pandas", "numpy", "joblib"]
x0 = 14
for r in reqs:
    pdf.set_fill_color(*LGREY)
    pdf.set_draw_color(*LIGHT)
    pdf.set_text_color(*BLUE)
    pdf.set_font("Courier", "B", 9)
    w = pdf.get_string_width(r) + 10
    pdf.set_x(x0)
    pdf.cell(w, 6.5, r, border=1, fill=True)
    x0 += w + 4
pdf.ln(10)

# ── HANDOFF ───────────────────────────────────────────────────
pdf.set_fill_color(*GREEN)
pdf.rect(10, pdf.get_y(), 190, 8, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("Helvetica", "B", 11)
pdf.set_xy(14, pdf.get_y() + 1)
pdf.cell(0, 6, "🤝  Handoff — Push When Done")
pdf.ln(10)

code_block(pdf, [
    "git add .",
    'git commit -m "feat: data generation, preprocessing, trained models"',
    "git push origin dev1/data-and-models",
])

pdf.set_text_color(*TEXT)
pdf.set_font("Helvetica", "", 9.5)
pdf.set_x(12)
pdf.multi_cell(186, 6,
    "Open a Pull Request to main on GitHub. Dev 2 will pull main and take over the "
    "Flask API layer. Since you own completely separate files, the merge will be "
    "automatic with zero conflicts.",
    new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ── Save ──────────────────────────────────────────────────────
out = r"C:\Users\motiv\Desktop\AckVision\dev1_summary.pdf"
pdf.output(out)
print(f"PDF saved → {out}")
