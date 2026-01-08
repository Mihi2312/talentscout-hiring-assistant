from fastapi import FastAPI, UploadFile, File, Form
from model import generate_questions
from resume_parser import extract_resume_text

app = FastAPI(title="TalentScout Hiring Assistant")

@app.get("/")
def root():
    return {"status": "TalentScout API running"}

@app.post("/analyze")
async def analyze_candidate(
    resume: UploadFile = File(None),
    manual_text: str = Form(None)
):
    if not resume and not manual_text:
        return {"error": "Provide resume or manual input"}

    if resume:
        profile_text = extract_resume_text(resume.file, resume.filename)
    else:
        profile_text = manual_text

    questions = generate_questions(profile_text)

    return {
        "status": "success",
        "questions": questions
    }
