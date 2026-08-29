from pathlib import Path

from docx import Document
from pypdf import PdfReader

def read_pdf(file_path: Path) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text

def read_docx(file_path: Path) -> str:
    document = Document(file_path)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text

def read_resume(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(file_path)

    if suffix == ".docx":
        return read_docx(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")