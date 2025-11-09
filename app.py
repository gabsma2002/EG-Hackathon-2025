import streamlit as st
import pandas as pd
from openai import OpenAI

# ===============================
# 🔧 Configuration
# ===============================
API_KEY = "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"  # your API key
client = OpenAI(api_key=API_KEY)

SUNY_CATALOG_URL = "https://catalog.newpaltz.edu/undergraduate/course-descriptions/cps/"

st.set_page_config(page_title="CourseBuddy AI", layout="wide")
st.title("🎓 CourseBuddy – AI Course Recommender")

st.write(
    "CourseBuddy generates personalized course recommendations based on your completed courses. "
    "The AI will double-check each course against the official SUNY New Paltz Computer Science catalog."
)

# ===============================
# Step 1: User inputs completed courses
# ===============================
st.subheader("✅ Enter your completed courses")
taken_courses = st.text_area(
    "Enter completed course codes (comma-separated, e.g., CPS100,CPS210,MAT320):"
)

# ===============================
# Step 2: Generate Recommended Schedule
# ===============================
if st.button("Generate Recommended Schedule"):
    if not taken_courses.strip():
        st.warning("Please enter at least one completed course.")
    else:
        with st.spinner("Generating schedule..."):
            try:
                response = client.responses.create(
                    model="gpt-4.1",
                    input=(
                        f"Using the CourseBuddy system prompt (which contains the course catalog and feedback.json), "
                        f"generate a recommended schedule for a student who has completed these courses: {taken_courses}. "
                        f"Double-check each course code, name, and prerequisites against the official SUNY New Paltz Computer Science catalog "
                        f"({SUNY_CATALOG_URL}) to ensure all recommended courses actually exist. "
                        f"For each recommended course, include: course name, course number, credits, prerequisites, reasoning based on feedback, "
                        f"and alternative recommendations. Return the output as JSON suitable for Excel."
                    )
                )

                gpt_output = response.output[0].content[0].text

                # Try to parse JSON for Excel
                try:
                    recommendations = pd.read_json(gpt_output)
                    st.success("✅ Schedule generated successfully!")
                    st.dataframe(recommendations)

                    # Export to Excel
                    excel_file = "recommended_schedule.xlsx"
                    recommendations.to_excel(excel_file, index=False)
                    with open(excel_file, "rb") as f:
                        st.download_button(
                            label="📥 Download Schedule (Excel)",
                            data=f,
                            file_name=excel_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                except Exception:
                    st.warning("⚠️ Could not parse JSON. Showing raw GPT output instead:")
                    st.text_area("GPT Output", gpt_output, height=300)

            except Exception as e:
                st.error(f"Error generating schedule: {e}")

# ===============================
# Step 3: Chat-based follow-up
# ===============================
st.subheader("💬 Ask CourseBuddy")
user_q = st.text_input("Ask a question about courses or study plan:")

if user_q:
    with st.spinner("Thinking..."):
        try:
            chat_response = client.responses.create(
                model="gpt-4.1-mini",
                input=(
                    f"Using the CourseBuddy system prompt and feedback.json, "
                    f"answer this question from the student: {user_q}. "
                    f"Double-check any course references against the official SUNY New Paltz catalog: {SUNY_CATALOG_URL}."
                )
            )
            st.write(chat_response.output[0].content[0].text)
        except Exception as e:
            st.error(f"Chat error: {e}")
