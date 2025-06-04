import os
from sys import implementation
from time import sleep
from dotenv import load_dotenv
from gui.widgets import LogPanel, StandardButton, StandardLabel, StandardFrame
from gui.gui_lookup import InvoiceApp
from customtkinter import *
from helper import load_config, save_config, load_json
from services.ai_service import AIService
from services.pdf_service import PDFService
from utils.file_utils import FileUtils
import main
import threading

load_dotenv()
api_key = os.getenv("API_KEY")

script_dir = os.path.dirname(__file__)
project_root = os.path.join(script_dir, "..", "..")

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

        self.categories_button = StandardButton(self.frame_log, text="Show Categories", command=self.show_categories)
        self.categories_button.pack(pady=10)

        self.scrollable_frame = CTkScrollableFrame(self)

    def ask_folder(self):
        folder_name = filedialog.askdirectory()
        self.config["folder_path"] = folder_name
        save_config(self.config)
        self.suggest_categories_button.configure(state="normal")

    def suggest_categories(self):
        files = main.get_files()
        documents = main.extract_text(files)
        document_batches = main.split_batches(documents)

        def on_complete():
            self.after(0, self.show_categories_button)

        thread = threading.Thread(target=main.extract_invoices, args=(document_batches, self.frame_log, on_complete))
        thread.start()

    def show_categories_button(self):
        self.categories_button.pack(pady=10)

    def show_categories(self):
        self.frame_log.clear()
        self.frame_log.forget()
        self.scrollable_frame.pack(fill=BOTH, padx=10, pady=5, expand=True)
        categories = load_json(project_root, "categories")

        self.selected_categories = []
        self.category_buttons = {}

        for category, idx in categories.items():
            display_text = category
            category_button = StandardButton(
                self.scrollable_frame,
                text=display_text,
                command=lambda c=category: self.category_clicked(c)
            )
            category_button.pack(pady=2, expand=False)
            print(category_button.cget("fg_color"))
            self.category_buttons[category] = category_button

        label = StandardLabel(self.scrollable_frame, text="Select categories for resuggestion")
        label.pack(side=BOTTOM, pady=10)
            
    def category_clicked(self, category):
        button = self.category_buttons[category]
        if category in self.selected_categories:
            self.selected_categories.remove(category)
            button.configure(fg_color="#1F6AA5")
        else:
            self.selected_categories.append(category)
            button.configure(fg_color="red")



