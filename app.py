import streamlit as st
import requests

BACKEND_URL = "https://talentscout-hiring-assistant-z7w3.onrender.com"

st.set_page_config(
    page_title="TalentScout AI",
    page_icon="🤖",
    layout="centered"
)

# ---------------- SESSION INIT ----------------
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.data = {}
    st.session_state.tech_qs = []
    st.session_state.tech_index = 0

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🤖 TalentScout Hiring Assistant</h1>
<p style='text-align:center; color:gray'>
AI-powered screening & technical interview
</p>
""", unsafe_allow_html=True)

st.divider()

# ---------------- RESUME UPLOAD ----------------
uploaded_resume = st.file_uploader(
    "📎 Upload Resume (optional)",
    type=["pdf", "docx"]
)

if uploaded_resume and st.session_state.step == "start":
    with st.spinner("Parsing resume..."):
        try:
            res = requests.post(
                f"{BACKEND_URL}/analyze",
                files={"resume": uploaded_resume},
                timeout=60
            )

            if res.status_code == 200:
                st.session_state.data = res.json()
                st.session_state.step = "confirm"
                st.rerun()
            else:
                st.warning("Resume parsing failed. Use manual mode.")

        except Exception:
            st.warning("Backend unavailable. Use manual mode.")

# ---------------- MANUAL MODE ----------------
if st.session_state.step == "start":
    st.subheader("📝 Manual Application")

    with st.form("manual_form", clear_on_submit=False):
        st.session_state.data["name"] = st.text_input("Full Name")
        st.session_state.data["email"] = st.text_input("Email")
        st.session_state.data["phone"] = st.text_input("Phone")
        st.session_state.data["experience"] = st.text_input("Experience (years)")
        st.session_state.data["role"] = st.text_input("Role Applied For")
        st.session_state.data["location"] = st.text_input("Location")
        st.session_state.data["tech_stack"] = st.text_area("Tech Stack")

        submitted = st.form_submit_button("Continue →")

        if submitted:
            st.session_state.step = "confirm"
            st.rerun()

# ---------------- CONFIRM ----------------
if st.session_state.step == "confirm":
    st.subheader("✅ Confirm Your Details")

    for k, v in st.session_state.data.items():
        st.write(f"**{k.capitalize()}**: {v}")

    with st.form("confirm_form"):
        confirm = st.text_input("Type `confirm` to proceed")
        ok = st.form_submit_button("Start Interview")

        if ok and confirm.lower() == "confirm":
            with st.spinner("Preparing interview..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/technical-questions",
                        params={"tech_stack": st.session_state.data["tech_stack"]},
                        timeout=30
                    )

                    if response.status_code == 200 and response.headers.get("content-type","").startswith("application/json"):
                        st.session_state.tech_qs = response.json().get("questions", [])
                        st.session_state.step = "tech"
                        st.rerun()
                    else:
                        st.error("Failed to generate questions.")

                except Exception:
                    st.error("Backend not responding.")

# ---------------- TECH INTERVIEW ----------------
if st.session_state.step == "tech":
    st.subheader("💻 Technical Interview")

    if st.session_state.tech_index < len(st.session_state.tech_qs):
        q = st.session_state.tech_qs[st.session_state.tech_index]

        with st.form("tech_form"):
            st.markdown(f"**Q{st.session_state.tech_index+1}:** {q}")
            ans = st.text_area("Your answer", height=120)
            next_btn = st.form_submit_button("Next")

            if next_btn:
                st.session_state.tech_index += 1
                st.rerun()

    else:
        st.success("🎉 Interview completed!")
        st.write("Our team will contact you soon.")
        st.stop()
