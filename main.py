import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def generate_questions(profile_text: str) -> list[str]:
    prompt = f"""
You are a senior technical interviewer.

From the following candidate profile or tech description:

{profile_text}

Generate EXACTLY 3 technical interview questions.

Rules:
- Output ONLY the questions
- One question per line
- No numbering
- No explanations
- No answers
"""

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.6,
            "max_new_tokens": 150
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    raw_text = response.json()[0]["generated_text"]

    # 🔹 Clean & extract questions
    questions = [
        line.strip()
        for line in raw_text.split("\n")
        if "?" in line
    ]

    # 🔒 GUARANTEE EXACTLY 3
    return questions[:3]
