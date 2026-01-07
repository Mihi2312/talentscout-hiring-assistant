# TalentScout Hiring Assistant 🤖

An AI-powered hiring assistant built using FastAPI and Hugging Face models.
This system collects candidate details, generates technical interview questions
based on the candidate’s tech stack, and stores data in a database.

## Features
- FastAPI backend
- Hugging Face LLM (FLAN-T5)
- SQLite database
- REST API with Swagger UI
- HTTPS deployment ready

## Tech Stack
- Python
- FastAPI
- Hugging Face Transformers
- SQLite
- GitHub
- Render

## API Endpoints
- POST /candidate/ → Create candidate and generate questions
- GET / → Health check

## Deployment
The application is deployed on Render with HTTPS enabled.
