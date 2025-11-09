import json
import os

FEEDBACK_FILE = "feedback.json"

# Editable course catalog (full structure like your catalog variable)
COURSE_LIST = {
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




# ---------- Feedback System ----------

def load_feedback():
    """Load existing feedback from file."""
    if not os.path.exists(FEEDBACK_FILE):
        return {}
    with open(FEEDBACK_FILE, "r") as file:
        return json.load(file)


def save_feedback(data):
    """Save feedback to JSON file."""
    with open(FEEDBACK_FILE, "w") as file:
        json.dump(data, file, indent=4)


def give_advice(feedback_data):
    """Display advice for a selected course."""
    course = input("Enter the course number you want advice on (e.g., CPS352): ").upper()

    if course not in COURSE_LIST:
        print("❌ This course is not recognized. Please check your input.")
        return

    course_info = COURSE_LIST[course]
    print(f"\nCourse Selected: {course} - {course_info['name']}")
    print(f"Credits: {course_info['credits']}")
    print(f"Prerequisites: {', '.join(course_info['prereqs']) if course_info['prereqs'] else 'None'}")

    if course not in feedback_data:
        print("\nNo prior student feedback available yet. Proceed with standard preparation.")
        return

    print("\n--- Student Feedback Summary ---")
    for entry in feedback_data[course]:
        print(f"• Reported Assignment/Exam Issues: {entry['problems']}")
        print(f"• Recommended Prerequisite(s): {entry['recommended_prereq']}\n")


def collect_feedback(feedback_data):
    """Collect new feedback from the user."""
    course = input("Enter the course number you are giving feedback for (e.g., CPS352): ").upper()

    if course not in COURSE_LIST:
        print("❌ This course is not recognized. Please check your input.")
        return

    problems = input("What were the problems with exams and assignments? ")
    recommended_prereq = input("Recommended course(s) you should take before this one (list course numbers): ")

    if course not in feedback_data:
        feedback_data[course] = []

    feedback_data[course].append({
        "problems": problems,
        "recommended_prereq": recommended_prereq
    })

    save_feedback(feedback_data)
    print("\n✅ Your feedback has been saved. Thank you!\n")


def main():
    feedback_data = load_feedback()

    print("Welcome to the Computer Science Course Advisor & Feedback System\n")
    choice = input("Do you want advice (A) or give feedback (F)? ").strip().upper()

    if choice == "A":
        give_advice(feedback_data)
    elif choice == "F":
        collect_feedback(feedback_data)
    else:
        print("Invalid option. Please restart the program.")


if __name__ == "__main__":
    main()
