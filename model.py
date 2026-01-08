import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "User-Agent": "TalentScout/1.0",
    "Content-Type": "application/json"
}

def generate_questions(profile_text: str) -> str:
    prompt = (
        "Generate 5 technical interview questions based on this candidate profile:\n"
        f"{profile_text}"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=30
        )

        if response.status_code != 200:
            raise Exception("HF unavailable")

        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

    except Exception:
        return (
            "AI service temporarily unavailable.\n\n"
            "Sample Questions:\n"
            "1. Explain your core technical skills.\n"
            "2. What projects have you worked on?\n"
            "3. How do you handle problem-solving?\n"
            "4. Explain REST APIs.\n"
            "5. What challenges have you faced?"
        )
