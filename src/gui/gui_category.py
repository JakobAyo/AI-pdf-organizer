import os
from dotenv import load_dotenv
from gui.widgets import LogPanel, StandardButton, StandardLabel, StandardFrame
from customtkinter import *
from helper import load_config, save_config
from services.ai_service import AIService
from services.pdf_service import PDFService
from utils.file_utils import FileUtils
import main

load_dotenv()
api_key = os.getenv("API_KEY")

pdf_service = PDFService()
file_utils = FileUtils()
ai_service = AIService(api_key)

class CategoryGUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.config = load_config()
        self.title("AI Invoice Organizer")
        self.geometry("900x600")


        self.frame_top = StandardFrame(self, width=50, height=20)
        self.frame_top.pack(fill=BOTH, padx=10, pady=5, side=TOP)

        self.frame_log = LogPanel(self)
        self.frame_log.pack(fill=BOTH, padx=10, pady=5, expand=True)

        self.frame_bottom = StandardFrame(self, width=30, height=20)
        self.frame_bottom.pack(padx=10, pady=5, side=BOTTOM)

        self.label = StandardLabel(self.frame_top, text="AI Invoice Organizer")
        self.label.pack(side=TOP, pady=10)

        self.suggest_categories_button = StandardButton(self.frame_bottom, text="Suggest Categories", state="disabled", command=self.suggest_categories)
        self.suggest_categories_button.pack(fill=BOTH, side=LEFT, padx=5)

        self.resuggest_categories_button = StandardButton(self.frame_bottom, text="Resuggest Categories", state="disabled")
        self.resuggest_categories_button.pack(fill=BOTH, side=RIGHT, padx=5)

        self.select_button = StandardButton(self.frame_bottom, text="Select Invoices Folder", command=self.ask_folder)
        self.select_button.pack(side=RIGHT, padx=5)

    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        self.config["folder_path"] = folder_name
        save_config(self.config)
        self.suggest_categories_button.configure(state="normal")

    def suggest_categories(self):
        files = main.get_files()
        documents = main.extract_text(files)
        document_batches = main.split_batches(documents)
        main.extract_invoices(document_batches, self.frame_log)


