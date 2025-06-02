import os
import shutil
from helper import load_json
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
categories = load_json(project_root, "categories")
invoices = load_json(project_root, "invoices")

class InvoiceOrganizer:
    PDF_FOLDER = "PDF_FILES"
    OUTPUT_FOLDER = "categorized_invoices"

    @staticmethod
    def create_folders():
        os.makedirs(InvoiceOrganizer.OUTPUT_FOLDER, exist_ok=True)

        for category in categories:
            category_dir = os.path.join(InvoiceOrganizer.OUTPUT_FOLDER, category)
            os.makedirs(category_dir, exist_ok=True)
            print(f"Created folder: {category_dir}")

    @staticmethod
    def move_to_folders():
        for category, ids in categories.items():
            category_folder = os.path.join(project_root, "categorized_invoices", category)
            for id in ids:
                shutil.copy(invoices[int(id)]["filename"], category_folder)
