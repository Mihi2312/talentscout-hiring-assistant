from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_questions(tech_stack: str):
    prompt = f"""
    Generate 3 to 5 technical interview questions
    for each technology in this tech stack:
    {tech_stack}
    """
    output = generator(prompt, max_length=300)
    return output[0]["generated_text"]
