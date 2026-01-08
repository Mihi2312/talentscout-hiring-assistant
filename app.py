import streamlit as st
import requests

# ================= CONFIG =================
BACKEND_URL = "https://talentscout-hiring-assistant-z7w3.onrender.com"

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    layout="centered"
)

# ================= SESSION INIT =================
if "mode" not in st.session_state:
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.chat = []
    st.session_state.tech_qs = []
    st.session_state.tech_index = 0

# ================= UI HEADER =================
st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered screening & technical interview")

# ================= RESUME UPLOAD =================
uploaded_resume = st.file_uploader(
    "➕ Upload Resume (PDF / DOCX) to auto-fill details",
    type=["pdf", "docx"]
)

if uploaded_resume and st.session_state.mode is None:
    with st.spinner("Parsing resume..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                files={"resume": uploaded_resume},
                timeout=60
            )

            parsed = response.json()

            st.session_state.data = {
                "name": parsed.get("name", "Not found"),
                "email": parsed.get("email", "Not found"),
                "phone": parsed.get("phone", "Not found"),
                "experience": parsed.get("experience", "Not found"),
                "role": parsed.get("role", "Not specified"),
                "location": parsed.get("location", "Not specified"),
                "tech_stack": parsed.get("tech_stack", "Not specified")
            }

            st.session_state.mode = "resume"
            st.session_state.step = "confirm"
            st.experimental_rerun()

        except Exception:
            st.error("Failed to parse resume. Please use manual mode.")

# ================= MANUAL MODE INIT =================
if st.session_state.mode is None and not uploaded_resume:
    if st.button("Start Manual Application"):
        st.session_state.mode = "manual"
        st.session_state.step = 0
        st.experimental_rerun()

# ================= MANUAL QUESTIONS =================
manual_questions = [
    ("name", "May I know your full name?"),
    ("email", "Please provide your email address."),
    ("phone", "Please share your phone number."),
    ("experience", "How many years of experience do you have?"),
    ("role", "What position are you applying for?"),
    ("location", "Where are you located?"),
    ("tech_stack", "Please list your tech stack.")
]

# ================= CHAT DISPLAY =================
for speaker, message in st.session_state.chat:
    st.markdown(f"**{speaker}:** {message}")

# ================= MANUAL CHAT FLOW =================
if st.session_state.mode == "manual" and st.session_state.step < len(manual_questions):
    key, question = manual_questions[st.session_state.step]

    st.markdown(f"**Bot:** {question}")
    user_input = st.text_input("Your response", key=f"manual_{key}")

    if st.button("Send"):
        st.session_state.data[key] = user_input
        st.session_state.chat.append(("You", user_input))
        st.session_state.step += 1
        st.experimental_rerun()

# ================= CONFIRMATION =================
if st.session_state.step == "confirm" or (
    st.session_state.mode == "manual"
    and st.session_state.step == len(manual_questions)
):
    st.subheader("Please confirm your details")

    for k, v in st.session_state.data.items():
        st.write(f"**{k.capitalize()}**: {v}")

    confirm_input = st.text_input("Type `confirm` to proceed")

    if confirm_input.lower() == "confirm":
        with st.spinner("Starting technical interview..."):
            response = requests.post(
                f"{BACKEND_URL}/technical-questions",
                params={"tech_stack": st.session_state.data["tech_stack"]},
                timeout=30
            )

            st.session_state.tech_qs = response.json()["questions"]
            st.session_state.tech_index = 0
            st.session_state.step = "tech"
            st.experimental_rerun()

# ================= TECHNICAL INTERVIEW =================
if st.session_state.step == "tech":
    question = st.session_state.tech_qs[st.session_state.tech_index]
    st.markdown(f"**Question {st.session_state.tech_index + 1}:** {question}")

    tech_answer = st.text_input("Your answer", key=f"tech_{st.session_state.tech_index}")

    if st.button("Next"):
        st.session_state.chat.append(("You", tech_answer))
        st.session_state.tech_index += 1

        if st.session_state.tech_index >= 3:
            st.success("🎉 Interview completed. Thank you!")
            st.stop()

        st.experimental_rerun()
