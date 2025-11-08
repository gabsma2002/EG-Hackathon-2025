from pathlib import Path
import json
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------- Paths ----------
feedback_path = Path("feedback.json")
xlsx_out = Path("recommended_schedule.xlsx")
pdf_out = Path("recommended_schedule.pdf")


# ---------- Load Feedback ----------
if not feedback_path.exists():
    raise FileNotFoundError("feedback.json not found. Please place your file in this folder.")

with open(feedback_path, "r") as f:
    feedback = json.load(f)

taken = feedback.get("taken_classes", [])
taken_course_numbers = {c.get("course_number", "").upper() for c in taken}


# ---------- Course Catalog (Edit as Needed) ----------
catalog = {
    "CS101": {"name": "Introduction to Computer Science", "course_number": "CS101", "credits": 3, "prereqs": []},
    "CS102": {"name": "Intro to Programming (Python)", "course_number": "CS102", "credits": 3, "prereqs": ["CS101"]},
    "CS201": {"name": "Data Structures", "course_number": "CS201", "credits": 3, "prereqs": ["CS102"]},
    "CS301": {"name": "Algorithms", "course_number": "CS301", "credits": 3, "prereqs": ["CS201"]},
    "CS310": {"name": "Databases", "course_number": "CS310", "credits": 3, "prereqs": ["CS201"]},
    "CS350": {"name": "Operating Systems", "course_number": "CS350", "credits": 3, "prereqs": ["CS201"]},
    "CS360": {"name": "Machine Learning", "course_number": "CS360", "credits": 3, "prereqs": ["CS301"]},
    "MATH101": {"name": "Calculus I", "course_number": "MATH101", "credits": 4, "prereqs": []},
    "MATH201": {"name": "Discrete Mathematics", "course_number": "MATH201", "credits": 3, "prereqs": []},
    "STAT200": {"name": "Statistics for Engineers", "course_number": "STAT200", "credits": 3, "prereqs": ["MATH101"]},
}


# ---------- Helper Function ----------
def prereqs_satisfied(prereqs, taken_set):
    """Check if all prerequisites are in the taken course set."""
    return all(p.upper() in taken_set for p in prereqs)


# ---------- Generate Recommendations ----------
rows = []

for code, info in catalog.items():
    if code in taken_course_numbers:
        continue

    prereqs = info.get("prereqs", [])
    satisfied = prereqs_satisfied(prereqs, taken_course_numbers)

    if satisfied:
        why = "Prerequisites satisfied — natural next course in your program."
        alts = [f"{c['course_number']} - {c['name']}" for k, c in catalog.items()
                if k != code and c.get("course_number") not in taken_course_numbers][:3]
    else:
        missing = [p for p in prereqs if p not in taken_course_numbers]
        why = f"Missing prerequisites: {', '.join(missing)}."
        alts = [m for m in missing]

    rows.append({
        "Class Name": info["name"],
        "Course Number": info["course_number"],
        "Credits": info["credits"],
        "Prerequisites": ", ".join(prereqs),
        "Why Recommended": why,
        "Alternative Recommendations": "; ".join(alts)
    })


# ---------- Create DataFrame ----------
df = pd.DataFrame(rows, columns=[
    "Class Name",
    "Course Number",
    "Credits",
    "Prerequisites",
    "Why Recommended",
    "Alternative Recommendations"
])

df.to_excel(xlsx_out, index=False)
print(f"Excel file saved to: {xlsx_out}")


# ---------- Generate PDF ----------
doc = SimpleDocTemplate(str(pdf_out), pagesize=landscape(letter))
styles = getSampleStyleSheet()
elements = [
    Paragraph(f"Recommended Class Schedule for {feedback.get('student_name', 'Student')}", styles['Title']),
    Spacer(1, 12)
]

table_data = [df.columns.tolist()] + df.fillna("").values.tolist()
table = Table(table_data, repeatRows=1)

table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
]))

elements.append(table)
doc.build(elements)

print(f"PDF file saved to: {pdf_out}")
print("Done! 🎓")
