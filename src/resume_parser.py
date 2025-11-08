import PyPDF2
from docx import Document

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type in ["doc", "docx"]:
        return extract_text_from_docx(uploaded_file)
    elif file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file format! Upload PDF, DOCX, or TXT.")
