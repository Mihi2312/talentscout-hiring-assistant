import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "User-Agent": "TalentScout/1.0",
    "Content-Type": "application/json"
}

def generate_questions(tech_stack: str):
    prompt = f"Generate 3 interview questions for {tech_stack}"

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=30
    )

    # 🔴 If Hugging Face blocks or errors
    if response.status_code != 200:
        return (
            "AI service unavailable right now.\n"
            "Sample questions:\n"
            "1. Explain core concepts of Python.\n"
            "2. What are REST APIs?\n"
            "3. Explain MVC/MVT architecture."
        )

    try:
        data = response.json()
    except Exception:
        return "AI response parsing failed."

    # 🔴 Handle non-list responses safely
    if not isinstance(data, list):
        return (
            "AI response unavailable.\n"
            "Sample questions:\n"
            "1. What is Python?\n"
            "2. Explain functions.\n"
            "3. What are lists and dictionaries?"
        )

    if len(data) == 0 or "generated_text" not in data[0]:
        return "AI returned
