from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from resume_parser import extract_resume_text
from model import generate_questions

app = FastAPI(title="TalentScout Hiring Assistant")

@app.get("/")
def root():
    return {"status": "TalentScout API running"}

@app.post("/analyze")
async def analyze_candidate(
    resume: UploadFile = File(None),
    manual_text: str = Form(None)
):
    # ---------------- VALIDATION ----------------
    if not resume and not manual_text:
        raise HTTPException(
            status_code=400,
            detail="Provide resume or manual input"
        )

    # ---------------- EXTRACT PROFILE TEXT ----------------
    try:
        if resume:
            profile_text = extract_resume_text(
                resume.file,
                resume.filename
            )
        else:
            profile_text = manual_text.strip()

        if not profile_text or len(profile_text) < 20:
            raise ValueError("Extracted profile text is empty or invalid")

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Resume parsing failed: {str(e)}"
        )

    # ---------------- GENERATE QUESTIONS ----------------
    try:
        questions = generate_questions(profile_text)

        if not questions or len(questions) != 3:
            raise ValueError("AI did not return exactly 3 questions")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question generation failed: {str(e)}"
        )

    # ---------------- RESPONSE ----------------
    return {
        "status": "success",
        "questions": questions
    }
