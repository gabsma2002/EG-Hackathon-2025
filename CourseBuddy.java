import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class CourseBuddy {

    private static final String FEEDBACK_FILE = "feedback.json";

    // Editable course list
    private static final Map<String, String> COURSE_LIST = new HashMap<>();
    static {
        COURSE_LIST.put("CPS210", "Computer Science I");
        COURSE_LIST.put("CPS310", "Computer Science II");
        COURSE_LIST.put("CPS315", "Computer Organization");
        COURSE_LIST.put("CPS330", "Assembly Programming");
        COURSE_LIST.put("CPS352", "Data Structures");
        COURSE_LIST.put("CPS353", "Operating Systems");
        COURSE_LIST.put("CPS430", "Database Systems");
        COURSE_LIST.put("CPS493", "Computer Science Seminar");
    }

    // Load feedback from JSON file
    private static JSONObject loadFeedback() {
        try {
            File file = new File(FEEDBACK_FILE);
            if (!file.exists()) {
                return new JSONObject();
            }
            String content = new String(Files.readAllBytes(Paths.get(FEEDBACK_FILE)));
            return new JSONObject(content);
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }

    // Save JSON feedback to file
    private static void saveFeedback(JSONObject data) {
        try (FileWriter file = new FileWriter(FEEDBACK_FILE)) {
            file.write(data.toString(4));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Give advice based on previous feedback
    private static void giveAdvice(JSONObject feedbackData, Scanner scanner) {
        System.out.print("Enter the course number you want advice on (e.g., CPS352): ");
        String course = scanner.nextLine().trim().toUpperCase();

        if (!COURSE_LIST.containsKey(course)) {
            System.out.println("This course is not recognized. Make sure you entered it correctly.");
            return;
        }

        System.out.println("\nCourse Selected: " + course + " - " + COURSE_LIST.get(course));

        if (!feedbackData.has(course)) {
            System.out.println("No prior student feedback available yet. Proceed with standard preparation.");
            return;
        }

        System.out.println("\n--- Student Feedback Summary ---");
        JSONArray feedbackArray = feedbackData.getJSONArray(course);
        for (int i = 0; i < feedbackArray.length(); i++) {
            JSONObject entry = feedbackArray.getJSONObject(i);
            System.out.println("• Reported Assignment/Exam Issues: " + entry.getString("problems"));
            System.out.println("• Recommended Prerequisite(s): " + entry.getString("recommended_prereq") + "\n");
        }
    }

    // Collect new feedback
    private static void collectFeedback(JSONObject feedbackData, Scanner scanner) {
        System.out.print("Enter the course number you are giving feedback for (e.g., CPS352): ");
        String course = scanner.nextLine().trim().toUpperCase();

        System.out.print("What were the problems with exams and assignments? ");
        String problems = scanner.nextLine();

        System.out.print("Recommended course(s) you should take before this one: ");
        String recommendedPrereq = scanner.nextLine();

        JSONArray feedbackArray = feedbackData.optJSONArray(course);
        if (feedbackArray == null) {
            feedbackArray = new JSONArray();
            feedbackData.put(course, feedbackArray);
        }

        JSONObject entry = new JSONObject();
        entry.put("problems", problems);
        entry.put("recommended_prereq", recommendedPrereq);
        feedbackArray.put(entry);

        saveFeedback(feedbackData);
        System.out.println("\n✅ Your feedback has been saved. Thank you!\n");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        JSONObject feedbackData = loadFeedback();

        System.out.println("Welcome to the Computer Science Course Advisor & Feedback System\n");
        System.out.print("Do you want advice (A) or give feedback (F)? ");
        String choice = scanner.nextLine().trim().toUpperCase();

        if (choice.equals("A")) {
            giveAdvice(feedbackData, scanner);
        } else if (choice.equals("F")) {
            collectFeedback(feedbackData, scanner);
        } else {
            System.out.println("Invalid option. Please restart the program.");
        }
    }
}
