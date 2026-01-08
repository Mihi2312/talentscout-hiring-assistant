import streamlit as st
import requests

BACKEND_URL = "https://talentscout-hiring-assistant-z7w3.onrender.com"

st.set_page_config(page_title="TalentScout Hiring Assistant")

st.title("🤖 TalentScout Hiring Assistant")

# ➕ Resume Upload
uploaded_resume = st.file_uploader(
    "➕ Upload Resume (PDF/DOCX) to auto-fill details",
    type=["pdf", "docx"]
)


profile_text = None
resume_file = None

if mode == "Upload Resume":
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

else:
    profile_text = st.text_area(
        "Enter your profile (skills, experience, tech stack)",
        height=200
    )

if st.button("Generate Interview Questions"):
    with st.spinner("Analyzing profile..."):
        if resume_file:
            response = requests.post(
                API_URL,
                files={"resume": resume_file}
            )
        else:
            response = requests.post(
                API_URL,
                data={"manual_text": profile_text}
            )

        result = response.json()

        if result.get("status") == "success":
            st.success("Here are your interview questions:")
            st.markdown(result["questions"])
        else:
            st.error(result.get("error", "Something went wrong"))
