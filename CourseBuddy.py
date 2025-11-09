import json
import os

FEEDBACK_FILE = "feedback.json"

# Editable course catalog (full structure like your catalog variable)
COURSE_LIST = {
    "CPS100": {"name": "Computers and Applications", "course_number": "CPS100", "credits": 3, "prereqs": []},
    "CPS210": {"name": "Computer Science I", "course_number": "CPS210", "credits": 4, "prereqs": []},
    "CPS310": {"name": "Computer Science II", "course_number": "CPS310", "credits": 4, "prereqs": ["CPS210"]},
    "CPS315": {"name": "Computer Science III", "course_number": "CPS315", "credits": 3, "prereqs": ["CPS310"]},
    "CPS330": {"name": "Assembly Language and Computer Architecture", "course_number": "CPS330", "credits": 3, "prereqs": ["CPS210"]},
    "CPS340": {"name": "Operating Systems I", "course_number": "CPS340", "credits": 3, "prereqs": ["CPS310"]},
    "CPS341": {"name": "Operating Systems II", "course_number": "CPS341", "credits": 3, "prereqs": ["CPS340"]},
    "CPS342": {"name": "Embedded Linux", "course_number": "CPS342", "credits": 3, "prereqs": ["CPS330"]},
    "CPS352": {"name": "Object Oriented Programming", "course_number": "CPS352", "credits": 3, "prereqs": ["CPS310"]},
    "CPS353": {"name": "Software Engineering", "course_number": "CPS353", "credits": 3, "prereqs": ["CPS352"]},
    "CPS393": {"name": "Computer Science Selected Topic", "course_number": "CPS393", "credits": 3, "prereqs": []},
    "CPS415": {"name": "Discrete and Continuous Computer Algorithms", "course_number": "CPS415", "credits": 3, "prereqs": ["CPS315", "MAT320"]},
    "CPS430": {"name": "Database Systems", "course_number": "CPS430", "credits": 3, "prereqs": ["CPS310"]},
    "CPS493": {"name": "Computer Science Seminar", "course_number": "CPS493", "credits": 1, "prereqs": ["CPS353"]},
    "CPS104": {"name": "Visual Programming", "course_number": "CPS104", "credits": 3, "prereqs": []},
    "CPS110": {"name": "Web Page Design", "course_number": "CPS110", "credits": 3, "prereqs": []},
    "CPS193": {"name": "Computer Science Selected Topic", "course_number": "CPS193", "credits": 3, "prereqs": []},
    "CPS293": {"name": "Computer Science Selected Topic", "course_number": "CPS293", "credits": 3, "prereqs": []},
    "MAT320": {"name": "Discrete Math for Computing", "course_number": "MAT320", "credits": 3, "prereqs": []},
    "EGC220": {"name": "Digital Logic Fundamentals", "course_number": "EGC220", "credits": 3, "prereqs": []},
    "EGC221": {"name": "Digital Logic Lab", "course_number": "EGC221", "credits": 1, "prereqs": ["EGC220"]}
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
