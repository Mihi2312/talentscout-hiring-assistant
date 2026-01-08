import streamlit as st
import re

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

# ---------------- INIT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.tech_qs = [
        "Explain the difference between supervised and unsupervised learning.",
        "How do you use Git and GitHub in a real project?",
        "Explain vectors and how VectorDBs are used."
    ]
    st.session_state.tech_index = 0

# ---------------- HELPERS ----------------
def bot(msg):
    st.session_state.messages.append(("bot", msg))

def user(msg):
    st.session_state.messages.append(("user", msg))

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# ---------------- START ----------------
if st.session_state.step == 0:
    bot("👋 Welcome to **TalentScout Hiring Assistant**!")
    bot("I’ll collect your details and conduct a short technical interview.")
    bot("May I know your **full name**?")
    st.session_state.step = 1

# ---------------- CHAT DISPLAY ----------------
for role, msg in st.session_state.messages:
    with st.chat_message("assistant" if role == "bot" else "user"):
        st.markdown(msg)

# ---------------- INPUT ----------------
prompt = st.chat_input("Type your response...")

if prompt:
    user(prompt)

    # -------- Name --------
    if st.session_state.step == 1:
        st.session_state.data["name"] = prompt
        bot("📧 Please provide your **email address**.")
        st.session_state.step = 2

    # -------- Email --------
    elif st.session_state.step == 2:
        if not valid_email(prompt):
            bot("❌ Invalid email. Please enter a valid email address.")
        else:
            st.session_state.data["email"] = prompt
            bot("📞 Please share your **phone number**.")
            st.session_state.step = 3

    # -------- Phone --------
    elif st.session_state.step == 3:
        if not valid_phone(prompt):
            bot("❌ Invalid phone number. Please enter at least 10 digits.")
        else:
            st.session_state.data["phone"] = prompt
            bot("💼 How many **years of experience** do you have?")
            st.session_state.step = 4

    # -------- Experience --------
    elif st.session_state.step == 4:
        st.session_state.data["experience"] = prompt
        bot("🎯 What **role** are you applying for?")
        st.session_state.step = 5

    # -------- Role --------
    elif st.session_state.step == 5:
        st.session_state.data["role"] = prompt
        bot("📍 Your **location**?")
        st.session_state.step = 6

    # -------- Location --------
    elif st.session_state.step == 6:
        st.session_state.data["location"] = prompt
        bot("🧰 Please list your **tech stack**.")
        st.session_state.step = 7

    # -------- Tech Stack --------
    elif st.session_state.step == 7:
        st.session_state.data["tech_stack"] = prompt

        bot("✅ **Please confirm your details:**")
        for k, v in st.session_state.data.items():
            bot(f"- **{k.capitalize()}**: {v}")

        bot("Type **confirm** to proceed or **edit email / phone / role**")
        st.session_state.step = 8

    # -------- Confirm / Edit --------
    elif st.session_state.step == 8:
        if prompt.lower() == "confirm":
            bot("🚀 Great! Let’s start the technical interview.")
            bot(f"**Question 1:** {st.session_state.tech_qs[0]}")
            st.session_state.step = 9
        elif prompt.startswith("edit"):
            field = prompt.replace("edit", "").strip()
            if field in st.session_state.data:
                bot(f"✏️ Enter new value for **{field}**")
                st.session_state.step = ("edit", field)
            else:
                bot("❌ Invalid field name.")
        else:
            bot("Please type **confirm** or **edit field_name**")

    # -------- Edit Mode --------
    elif isinstance(st.session_state.step, tuple):
        _, field = st.session_state.step
        st.session_state.data[field] = prompt
        bot(f"✅ {field} updated.")
        bot("Type **confirm** to proceed.")
        st.session_state.step = 8

    # -------- Technical Interview --------
    elif st.session_state.step == 9:
        st.session_state.tech_index += 1
        if st.session_state.tech_index < 3:
            bot(f"**Question {st.session_state.tech_index + 1}:** "
                f"{st.session_state.tech_qs[st.session_state.tech_index]}")
        else:
            bot("📊 **Final Feedback:** Thank you for your responses.")
            bot("🎉 Your interview is complete. Our team will contact you soon.")
            st.session_state.step = 10

    st.rerun()
