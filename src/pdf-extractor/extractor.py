import pdfplumber
import os

folder_path = os.path.join(os.getcwd(), "PDF_files")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text