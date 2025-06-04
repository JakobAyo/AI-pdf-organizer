from services.pdf_service import PDFService
from services.ai_service import AIService
from utils.file_utils import FileUtils
from config.settings import settings
from dotenv import load_dotenv
import os
from utils import print_utils
from helper import chunk_list, load_config, save_json
from utils.logging_utils import logger

load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
api_key = os.getenv("API_KEY")

# Initialize components
pdf_service = PDFService()
file_utils = FileUtils()
ai_service = AIService(api_key)

# Get inputs
def get_files():
    folder_path = load_config()["folder_path"]
    files = file_utils.get_supported_files(folder_path)
    return files

# Extract text from all PDFs
def extract_text(files):
    documents = []
    for file in files:
        extracted_text = pdf_service.extract_text(file)
        if extracted_text:
            documents.append({
                "filename": file,
                "text": extracted_text
            })
    return documents

# Split docuemnts into batches
def split_batches(documents):
    document_batches = chunk_list(documents, settings.BATCH_SIZE)
    return document_batches

def extract_invoices(document_batches, log_frame, callback=None):
    all_invoices = []

    log_frame.write(print_utils.start())
    for i, batch in enumerate(document_batches):
        log_frame.write(f"Processing batch {i+1}/{len(document_batches)} ({len(batch)} invoices)\n")

        batch_texts = [doc["text"] for doc in batch]
        invoices = ai_service.extract_invoice(batch_texts)
            
        for idx, invoice in enumerate(invoices):
            invoice["filename"] = batch[idx]["filename"]

        logger.info(f"{i+1}/{len(document_batches)} ({len(batch)} invoices)")
        all_invoices.extend(invoices)

    log_frame.write(f"Total processed invoices: {len(all_invoices)}\n")
    log_frame.write(print_utils.end())

    # Save to json
    save_json(project_root, all_invoices, "invoices")

    if callback:
        callback()
        
    return all_invoices

def suggest_categories():
    categories = ai_service.categorize_invoice(settings.NUM_CATEGORIES)
    save_json(project_root, categories, "categories")

    return categories
