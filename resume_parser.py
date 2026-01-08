from PyPDF2 import PdfReader
from docx import Document

def extract_resume_text(file, filename: str) -> str:
    text = ""

    if filename.lower().endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif filename.lower().endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"

    else:
        raise ValueError("Unsupported file format")

    # 🔴 CRITICAL SAFETY CHECK
    if len(text.strip()) < 50:
        raise ValueError("Resume text could not be extracted")

    return text
