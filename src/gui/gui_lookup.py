import customtkinter as ctk
import json
from pathlib import Path
import os
import subprocess
from helper import load_json

# Load parsed invoice data
project_root = Path(__file__).parent.parent.parent
PDF_DIR = Path(project_root) / "categorized_invoices"

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Invoice Organizer")
        self.geometry("900x600")
        self.invoices = load_json(project_root, "invoices")
        self.result_index_map = []

        # Set default appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # Search input
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Search Invoices...")
        self.search_entry.pack(padx=20, pady=20, fill="x")

        # Results frame
        self.results_frame = ctk.CTkScrollableFrame(self)
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Label to show status
        self.status_label = ctk.CTkLabel(self, text="Enter search term above", anchor="w")
        self.status_label.pack(padx=20, pady=(0, 10), anchor="w")

        # Update results on key release
        self.search_var.trace_add("write", self.on_search)

    def on_search(self, *args):
        query = self.search_var.get().strip()
        self.clear_results()
        
        if not query:
            self.status_label.configure(text="Enter search term")
            return

        matches = self.search_invoices(query)
        self.status_label.configure(text=f"Found {len(matches)} matching invoice(s)")

        if not matches:
            label = ctk.CTkLabel(self.results_frame, text="No matches found.", fg_color="transparent")
            label.pack(anchor="w", pady=2)
            return

        for idx, invoice in enumerate(matches[:50]):  # limit to 50 results
            display_text = f"{invoice['Invoice Number']} - {invoice['Item']}"
            result_btn = ctk.CTkButton(
                self.results_frame,
                text=display_text,
                anchor="w",
                command=lambda inv=invoice: self.open_pdf(inv)
            )
            result_btn.pack(anchor="w", pady=2)
            self.result_index_map.append(invoice)

    def search_invoices(self, query):
        query = query.lower()
        results = []

        for invoice in self.invoices:
            match = False
            for value in invoice.values():
                if value is not None and str(value).lower().find(query) != -1:
                    match = True
                    break
            if match:
                results.append(invoice)

        return results

    def open_pdf(self, invoice):
        pdf_path = PDF_DIR / f"{invoice['filename']}"

        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            return

        # Open the PDF
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path)
            elif os.name == 'posix':
                subprocess.Popen(["xdg-open", pdf_path])
            else:
                print("Opening PDF not supported on this OS.")
        except Exception as e:
            print("Error opening PDF:", e)

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.result_index_map.clear()


if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()
