from fastapi import FastAPI
from database import SessionLocal, Candidate
from model import generate_questions

app = FastAPI(title="TalentScout Hiring Assistant")

@app.get("/")
def root():
    return {"message": "TalentScout API is running"}

@app.post("/candidate/")
def create_candidate(data: dict):
    db = SessionLocal()

    questions = generate_questions(data["tech_stack"])

    candidate = Candidate(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        experience=data["experience"],
        position=data["position"],
        location=data["location"],
        tech_stack=data["tech_stack"],
        questions=questions
    )

    db.add(candidate)
    db.commit()
    db.close()

    return {
        "status": "success",
        "technical_questions": questions
    }
