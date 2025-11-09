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
    "CPS100": {"name": "Computers and Applications", "course_number": "CPS100", "credits": 3, "prereqs": []},
    "CPS104": {"name": "Visual Programming", "course_number": "CPS104", "credits": 3, "prereqs": []},
    "CPS110": {"name": "Web Page Design", "course_number": "CPS110", "credits": 3, "prereqs": []},
    "CPS193": {"name": "Computer Science Selected Topic", "course_number": "CPS193", "credits": 1, "prereqs": []},
    "CPS210": {"name": "Computer Science I: Foundations", "course_number": "CPS210", "credits": 4, "prereqs": []},
    "CPS293": {"name": "Computer Science Selected Topic", "course_number": "CPS293", "credits": 1, "prereqs": []},
    "CPS295": {"name": "Independent Study Computer Science", "course_number": "CPS295", "credits": 1, "prereqs": []},
    "CPS296": {"name": "Departmental Elective", "course_number": "CPS296", "credits": 0, "prereqs": []},
    "CPS299": {"name": "Modular Course", "course_number": "CPS299", "credits": 0, "prereqs": []},
    "CPS310": {"name": "Computer Science II: Data Structures", "course_number": "CPS310", "credits": 4, "prereqs": ["CPS210"]},
    "CPS315": {"name": "Computer Science III", "course_number": "CPS315", "credits": 4, "prereqs": ["CPS310"]},
    "CPS330": {"name": "Assembly Language and Computer Architecture", "course_number": "CPS330", "credits": 4, "prereqs": ["CPS310"]},
    "CPS340": {"name": "Operating Systems", "course_number": "CPS340", "credits": 4, "prereqs": ["CPS330"]},
    "CPS341": {"name": "Operating Systems II", "course_number": "CPS341", "credits": 3, "prereqs": ["CPS340"]},
    "CPS342": {"name": "Embedded Linux", "course_number": "CPS342", "credits": 3, "prereqs": ["CPS310"]},
    "CPS352": {"name": "Object Oriented Programming", "course_number": "CPS352", "credits": 3, "prereqs": ["CPS310"]},
    "CPS353": {"name": "Software Engineering", "course_number": "CPS353", "credits": 3, "prereqs": ["CPS310"]},
    "CPS393": {"name": "Computer Science Selected Topic", "course_number": "CPS393", "credits": 1, "prereqs": []},
    "CPS396": {"name": "Departmental Elective", "course_number": "CPS396", "credits": 0, "prereqs": []},
    "CPS399": {"name": "Modular Course", "course_number": "CPS399", "credits": 0, "prereqs": []},
    "CPS415": {"name": "Discrete and Continuous Computer Algorithms", "course_number": "CPS415", "credits": 3, "prereqs": ["MAT320"]},
    "CPS425": {"name": "Language Processing", "course_number": "CPS425", "credits": 4, "prereqs": ["CPS310","CPS330"]},
    "CPS440": {"name": "Database Principles", "course_number": "CPS440", "credits": 3, "prereqs": ["CPS310"]},
    "CPS441": {"name": "Database Projects", "course_number": "CPS441", "credits": 4, "prereqs": ["CPS440"]},
    "CPS460": {"name": "Computer Architecture", "course_number": "CPS460", "credits": 3, "prereqs": []},
    "CPS470": {"name": "Computer Communication Networks", "course_number": "CPS470", "credits": 3, "prereqs": []},
    "CPS471": {"name": "Computer Communication Networks II", "course_number": "CPS471", "credits": 4, "prereqs": ["CPS470"]},
    "CPS485": {"name": "Projects", "course_number": "CPS485", "credits": 4, "prereqs": ["CPS493","CPS470","CPS440"]},
    "CPS493": {"name": "Computer Science Selected Topic", "course_number": "CPS493", "credits": 3, "prereqs": []},
    "CPS494": {"name": "Fieldwork Computer Science", "course_number": "CPS494", "credits": 1, "prereqs": []},
    "CPS495": {"name": "Independent Study Computer Science", "course_number": "CPS495", "credits": 1, "prereqs": []},
    "MAT251": {"name": "Calculus I", "course_number": "MAT251", "credits": 4, "prereqs": ["MAT181"]},
    "MAT252": {"name": "Calculus II", "course_number": "MAT252", "credits": 4, "prereqs": ["MAT251"]},
    "MAT320": {"name": "Discrete Mathematics for Computing", "course_number": "MAT320", "credits": 3, "prereqs": ["MAT181"]},
    "EGC220": {"name": "Digital Logic Fundamentals", "course_number": "EGC220", "credits": 3, "prereqs": ["MAT251", "EGC221"]},
    "EGS221": {"name": "Digital Logic Lab", "course_number": "EGC221", "credits": 1, "prereqs": ["EGC220"]},
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
