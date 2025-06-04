import os
import shutil
from helper import load_json, load_config, save_json
from pathlib import Path

project_root = Path(__file__).parent.parent.parent

class InvoiceOrganizer:
    PDF_FOLDER = load_config()["folder_path"]
    categories = None
    invoices = None

    @staticmethod
    def create_folders():
        InvoiceOrganizer.categories = load_json(project_root, "categories")
        for category in InvoiceOrganizer.categories:
            category_dir = os.path.join(InvoiceOrganizer.PDF_FOLDER, category)
            os.makedirs(category_dir, exist_ok=True)
            print(f"Created folder: {category_dir}")

    @staticmethod
    def move_to_folders():
        InvoiceOrganizer.invoices = load_json(project_root, "invoices")
        for category, ids in InvoiceOrganizer.categories.items():
            category_folder = os.path.join(InvoiceOrganizer.PDF_FOLDER, category)
            for id in ids:
                shutil.move(InvoiceOrganizer.invoices[int(id)]["filename"], category_folder)
                InvoiceOrganizer.update_folder_path(id, category)

    @staticmethod
    def update_folder_path(id, category):
        invoices = load_json(project_root, "invoices")
        file_name = invoices[int(id)]["filename"].split("/")[-1]
        invoices[int(id)]["filename"] = os.path.join(InvoiceOrganizer.PDF_FOLDER, category, file_name)
        save_json(project_root, invoices, "invoices")



