from services.pdf_service import PDFService
from services.ai_service import AIService
from utils.file_utils import FileUtils
from config.settings import settings
from dotenv import load_dotenv
import os
from utils import print_utils, inquiry
from helper import chunk_list, save_json
from utils.logging_utils import logger

load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
api_key = os.getenv("API_KEY")


def main():
    # Initialize components
    pdf_service = PDFService()
    file_utils = FileUtils()
    ai_service = AIService(api_key)

    # Get inputs
    folder_path = os.path.join(project_root, "PDF_files")
    files = file_utils.get_supported_files(folder_path)

    # Extract text from all PDFs
    documents = []
    for file in files:
        extracted_text = pdf_service.extract_text(file)
        if extracted_text:
            documents.append({
                "filename": file,
                "text": extracted_text
            })

    # Split docuemnts into batches
    document_batches = chunk_list(documents, settings.BATCH_SIZE)

    all_invoices = []

    print_utils.start()
    for i, batch in enumerate(document_batches):
        print(f"Processing batch {i+1}/{len(document_batches)} ({len(batch)} invoices)")

        batch_texts = [doc["text"] for doc in batch]
        invoices = ai_service.extract_invoice(batch_texts)
            
        for idx, invoice in enumerate(invoices):
            invoice["filename"] = batch[idx]["filename"]

        logger.info(f"{i+1}/{len(document_batches)} ({len(batch)} invoices)")
        all_invoices.extend(invoices)

    print("Total processed invoices:", len(all_invoices))
    print_utils.end()

    # Save to json
    save_json(project_root, all_invoices)

    # Categories
    categories = ai_service.categorize_invoice(settings.NUM_CATEGORIES)

    print(categories)
    user_input = input("Enter for resuggestions: ")
    selection = [item.strip() for item in user_input.split(',')]
    
    new_categories = ai_service.resuggest_categories(selection)
    print(new_categories)

if __name__ == "__main__":
    main()
