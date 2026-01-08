import streamlit as st
import time
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🧠",
    layout="centered"
)

# ---------------- DARK MODE CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f1117;
}
.chat-container {
    max-width: 720px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.tech_qs = [
        "What is the difference between supervised and unsupervised learning?",
        "How do you use Git and GitHub in a real-world project?",
        "Explain vectors and how Vector Databases are used."
    ]
    st.session_state.tech_index = 0

# ---------------- HELPERS ----------------
def bot(msg, delay=True):
    if delay:
        with st.spinner("🧠 AI is thinking..."):
            time.sleep(0.6)
    st.session_state.messages.append(("bot", msg))

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

    bot("📄 I’ve extracted these details from your resume:")
    for k, v in parsed_data.items():
        bot(f"**{k.capitalize()}**: {v}", delay=False)

    bot("Type **confirm** to proceed or **edit field_name** (example: `edit email`).")
    st.session_state.step = 8

# ---------------- INITIAL GREETING ----------------
if st.session_state.step == 0:
    bot("👋 Hey! Welcome to **TalentScout** 🚀")
    bot("I’ll guide you through a quick screening and a short tech interview.")
    bot("What’s your **full name**?")
    st.session_state.step = 1

# ---------------- CHAT DISPLAY ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "bot":
        with st.chat_message("assistant", avatar="🧠✨"):
            st.markdown(msg)
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Type your response…")

if prompt:
    user(prompt)

    # -------- NAME --------
    if st.session_state.step == 1:
        st.session_state.data["name"] = prompt
        bot("📧 What’s your **email address**?")
        st.session_state.step = 2

    # -------- EMAIL --------
    elif st.session_state.step == 2:
        if not valid_email(prompt):
            bot("❌ That email doesn’t look right. Try again.")
        else:
            st.session_state.data["email"] = prompt
            bot("📞 Your **phone number**?")
            st.session_state.step = 3

    # -------- PHONE --------
    elif st.session_state.step == 3:
        if not valid_phone(prompt):
            bot("❌ Phone number should be at least 10 digits.")
        else:
            st.session_state.data["phone"] = prompt
            bot("💼 Years of **experience**?")
            st.session_state.step = 4

    # -------- EXPERIENCE --------
    elif st.session_state.step == 4:
        st.session_state.data["experience"] = prompt
        bot("🎯 Which **role** are you applying for?")
        st.session_state.step = 5

    # -------- ROLE --------
    elif st.session_state.step == 5:
        st.session_state.data["role"] = prompt
        bot("📍 Your **location**?")
        st.session_state.step = 6

    # -------- LOCATION --------
    elif st.session_state.step == 6:
        st.session_state.data["location"] = prompt
        bot("🧰 List your **tech stack**.")
        st.session_state.step = 7

    # -------- TECH STACK --------
    elif st.session_state.step == 7:
        st.session_state.data["tech_stack"] = prompt

        bot("✅ Please confirm your details:")
        for k, v in st.session_state.data.items():
            bot(f"- **{k.capitalize()}**: {v}", delay=False)

        bot("Type **confirm** or **edit field_name**")
        st.session_state.step = 8

    # -------- CONFIRM / EDIT --------
    elif st.session_state.step == 8:
        if prompt.lower() == "confirm":
            bot("🚀 Awesome! Let’s begin the technical interview.")
            bot(f"**Question 1:** {st.session_state.tech_qs[0]}")
            st.session_state.step = 9
        elif prompt.startswith("edit"):
            field = prompt.replace("edit", "").strip()
            if field in st.session_state.data:
                bot(f"✏️ Enter new value for **{field}**")
                st.session_state.step = ("edit", field)
            else:
                bot("❌ Invalid field name.")

    # -------- EDIT MODE --------
    elif isinstance(st.session_state.step, tuple):
        _, field = st.session_state.step
        st.session_state.data[field] = prompt
        bot(f"✅ {field} updated. Type **confirm** to continue.")
        st.session_state.step = 8

    # -------- TECH INTERVIEW --------
    elif st.session_state.step == 9:
        st.session_state.tech_index += 1
        if st.session_state.tech_index < 3:
            bot(f"**Question {st.session_state.tech_index + 1}:** "
                f"{st.session_state.tech_qs[st.session_state.tech_index]}")
        else:
            bot("📊 Thanks! Your interview is complete.")
            bot("🎉 Our team will reach out soon.")
            st.session_state.step = 10

    st.rerun()
