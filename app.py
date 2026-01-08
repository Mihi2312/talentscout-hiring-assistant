import streamlit as st
import requests

API_URL = "https://talentscout-hiring-assistant-zsp8.onrender.com/analyze"

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

mode = st.radio(
    "How would you like to apply?",
    ["Upload Resume", "Enter Details Manually"]
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
