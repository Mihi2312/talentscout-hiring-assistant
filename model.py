import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def generate_questions(tech_stack: str):
    prompt = f"""
    Generate 3 to 5 technical interview questions
    for each technology in this tech stack:
    {tech_stack}
    """

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    return result[0]["generated_text"]
