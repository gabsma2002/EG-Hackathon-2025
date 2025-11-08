import json
import os

FEEDBACK_FILE = "feedback.json"

# Example editable course list (add/remove courses as needed)
COURSE_LIST = {
    "CPS210": "Computer Science I",
    "CPS310": "Computer Science II",
    "CPS315": "Computer Organization",
    "CPS330": "Assembly Programming",
    "CPS352": "Data Structures",
    "CPS353": "Operating Systems",
    "CPS430": "Database Systems",
    "CPS493": "Computer Science Seminar"
}

# Load existing feedback if available
def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return {}
    with open(FEEDBACK_FILE, "r") as file:
        return json.load(file)

# Save feedback to file
def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Give advice based on previous feedback
def give_advice(feedback_data):
    course = input("Enter the course number you want advice on (e.g., CPS352): ").upper()
    
    if course not in COURSE_LIST:
        print("This course is not recognized. Make sure you entered it correctly.")
        return
    
    print(f"\nCourse Selected: {course} - {COURSE_LIST[course]}")
    
    if course not in feedback_data:
        print("No prior student feedback available yet. Proceed with standard preparation.")
        return
    
    print("\n--- Student Feedback Summary ---")
    for entry in feedback_data[course]:
        print(f"• Reported Assignment/Exam Issues: {entry['problems']}")
        print(f"• Recommended Prerequisite(s): {entry['recommended_prereq']}\n")

# Collect feedback from a student
def collect_feedback(feedback_data):
    course = input("Enter the course number you are giving feedback for (e.g., CPS352): ").upper()
    
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
