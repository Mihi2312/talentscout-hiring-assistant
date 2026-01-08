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
    prompt = (
        "Generate 3 technical interview questions for the following tech stack:\n"
        f"{tech_stack}"
    )

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=30
    )

    if response.status_code != 200:
        return f"Hugging Face error: {response.status_code}"

    data = response.json()

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return "AI response format error"
