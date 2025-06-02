import os
import shutil
from helper import load_json
from pathlib import Path

categories_path = Path(__file__).parent.parent.parent
categories = load_json(categories_path, "categories")

class InvoiceOrganizer:
    PDF_FOLDER = "PDF_FILES"
    OUTPUT_FOLDER = "categorized_invoices"

    @staticmethod
    def organize_pdfs():
        os.makedirs(InvoiceOrganizer.OUTPUT_FOLDER, exist_ok=True)

        for category in categories:
            category_dir = os.path.join(InvoiceOrganizer.OUTPUT_FOLDER, category)
            os.makedirs(category_dir, exist_ok=True)
            print(f"Created folder: {category_dir}")
