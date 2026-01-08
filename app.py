import streamlit as st
import time
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🧠",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.tech_qs = [
        "What is the difference between supervised and unsupervised learning?",
        "How do you use Git and GitHub in real-world projects?",
        "Explain vectors and how Vector Databases are used."
    ]
    st.session_state.tech_index = 0

# ---------------- HELPERS ----------------
def typing_animation(text):
    placeholder = st.empty()
    for dots in ["", ".", "..", "..."]:
        placeholder.markdown(f"🧠 AI is typing{dots}")
        time.sleep(0.25)
    placeholder.empty()
    st.session_state.messages.append(("bot", text))

def user(msg):
    st.session_state.messages.append(("user", msg))

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# ---------------- RESUME UPLOAD ----------------
st.markdown("### 📎 Upload Resume (optional)")
uploaded_file = st.file_uploader(
    "Upload resume (PDF/DOCX)",
    type=["pdf", "docx"],
    label_visibility="collapsed"
)

if uploaded_file and "resume_loaded" not in st.session_state:
    st.session_state.resume_loaded = True

    # 🔹 Mock parsed resume (replace with HF later)
    parsed_data = {
        "name": "Extracted Name",
        "email": "resume@email.com",
        "phone": "9999999999",
        "experience": "0",
        "role": "AI/ML Intern",
        "location": "India",
        "tech_stack": "Python, ML, GenAI"
    }

    st.session_state.data.update(parsed_data)

    typing_animation("📄 I’ve extracted the following details from your resume:")
    for k, v in parsed_data.items():
        st.session_state.messages.append(("bot", f"- **{k.capitalize()}**: {v}"))

    typing_animation("Type **confirm** to proceed or **edit field_name** (example: `edit email`).")
    st.session_state.step = 8

# ---------------- INITIAL GREETING ----------------
if st.session_state.step == 0:
    typing_animation("👋 Hey! Welcome to **TalentScout** 🚀")
    typing_animation("I’ll guide you through a quick screening and a short tech interview.")
    typing_animation("What’s your **full name**?")
    st.session_state.step = 1

# ---------------- CHAT DISPLAY ----------------
for role, msg in st.session_state.messages:
    if role == "bot":
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(msg)
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg)

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Type your response…")

if prompt:
    user(prompt)

    # -------- NAME --------
    if st.session_state.step == 1:
        st.session_state.data["name"] = prompt
        typing_animation("📧 What’s your **email address**?")
        st.session_state.step = 2

    # -------- EMAIL --------
    elif st.session_state.step == 2:
        if not valid_email(prompt):
            typing_animation("❌ That email doesn’t look right. Try again.")
        else:
            st.session_state.data["email"] = prompt
            typing_animation("📞 Your **phone number**?")
            st.session_state.step = 3

    # -------- PHONE --------
    elif st.session_state.step == 3:
        if not valid_phone(prompt):
            typing_animation("❌ Phone number should be at least 10 digits.")
        else:
            st.session_state.data["phone"] = prompt
            typing_animation("💼 Years of **experience**?")
            st.session_state.step = 4

    # -------- EXPERIENCE --------
    elif st.session_state.step == 4:
        st.session_state.data["experience"] = prompt
        typing_animation("🎯 Which **role** are you applying for?")
        st.session_state.step = 5

    # -------- ROLE --------
    elif st.session_state.step == 5:
        st.session_state.data["role"] = prompt
        typing_animation("📍 Your **location**?")
        st.session_state.step = 6

    # -------- LOCATION --------
    elif st.session_state.step == 6:
        st.session_state.data["location"] = prompt
        typing_animation("🧰 List your **tech stack**.")
        st.session_state.step = 7

    # -------- TECH STACK --------
    elif st.session_state.step == 7:
        st.session_state.data["tech_stack"] = prompt

        typing_animation("✅ Please confirm your details:")
        for k, v in st.session_state.data.items():
            st.session_state.messages.append(("bot", f"- **{k.capitalize()}**: {v}"))

        typing_animation("Type **confirm** or **edit field_name**")
        st.session_state.step = 8

    # -------- CONFIRM / EDIT --------
    elif st.session_state.step == 8:
        if prompt.lower() == "confirm":
            typing_animation("🚀 Awesome! Let’s begin the technical interview.")
            typing_animation(f"**Question 1:** {st.session_state.tech_qs[0]}")
            st.session_state.step = 9
        elif prompt.startswith("edit"):
            field = prompt.replace("edit", "").strip()
            if field in st.session_state.data:
                typing_animation(f"✏️ Enter new value for **{field}**")
                st.session_state.step = ("edit", field)
            else:
                typing_animation("❌ Invalid field name.")

    # -------- EDIT MODE --------
    elif isinstance(st.session_state.step, tuple):
        _, field = st.session_state.step
        st.session_state.data[field] = prompt
        typing_animation(f"✅ {field} updated. Type **confirm** to continue.")
        st.session_state.step = 8

    # -------- TECH INTERVIEW --------
    elif st.session_state.step == 9:
        st.session_state.tech_index += 1
        if st.session_state.tech_index < 3:
            typing_animation(
                f"**Question {st.session_state.tech_index + 1}:** "
                f"{st.session_state.tech_qs[st.session_state.tech_index]}"
            )
        else:
            typing_animation("📊 Interview complete. Thank you!")
            typing_animation("🎉 Our team will contact you soon.")
            st.session_state.step = 10

    st.rerun()
