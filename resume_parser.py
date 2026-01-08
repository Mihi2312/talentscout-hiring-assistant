from PyPDF2 import PdfReader
from docx import Document

def parse_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_docx(file) -> str:
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_resume_text(file, filename: str) -> str:
    if filename.endswith(".pdf"):
        return parse_pdf(file)
    elif filename.endswith(".docx"):
        return parse_docx(file)
    else:
        raise ValueError("Unsupported file format")
