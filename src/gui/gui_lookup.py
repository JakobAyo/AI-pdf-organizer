from customtkinter import *
from tkinter import StringVar
from pathlib import Path
import os
import subprocess
from helper import load_json, load_config

# Load parsed invoice data
project_root = Path(__file__).parent.parent.parent
PDF_DIR = load_config()["folder_path"]

class InvoiceApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Invoice Organizer")
        self.geometry("1000x700")

        self.invoices = load_json(PDF_DIR, "invoices")
        self.filtered_invoices = self.invoices  # Will be updated on filter
        self.result_index_map = []

        # Set appearance
        set_appearance_mode("dark")
        set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # --- Top Frame: Search + Filters ---
        top_frame = CTkFrame(self)
        top_frame.pack(padx=20, pady=10, fill="x")

        # Search input
        self.search_var = StringVar()
        self.search_entry = CTkEntry(top_frame, textvariable=self.search_var, placeholder_text="Search Invoices...")
        self.search_entry.pack(side="left", fill="x", expand=True)

        # --- Filter Frame ---
        filter_frame = CTkFrame(self)
        filter_frame.pack(padx=20, pady=5, fill="x")

        # Category Filter
        self.category_var = StringVar(value="All Categories")
        categories = self.get_unique_categories()
        self.category_menu = CTkOptionMenu(
            filter_frame,
            variable=self.category_var,
            values=["All Categories"] + categories,
            command=self.apply_filters
        )
        self.category_menu.pack(side="left", padx=5)

        # Date Range Filter
        self.date_var = StringVar(value="All Dates")
        dates = self.get_unique_dates()
        self.date_menu = CTkOptionMenu(
            filter_frame,
            variable=self.date_var,
            values=["All Dates"] + dates,
            command=self.apply_filters
        )
        self.date_menu.pack(side="left", padx=5)

        # Total Amount Filter
        self.amount_var = StringVar(value="Any Amount")
        self.amount_menu = CTkOptionMenu(
            filter_frame,
            variable=self.amount_var,
            values=["Any Amount", "$0 - $100", "$100 - $500", "$500 - $1000", "$1000+"],
            command=self.apply_filters
        )
        self.amount_menu.pack(side="left", padx=5)

        # Clear Filters Button
        clear_button = CTkButton(filter_frame, text="Reset", width=80, command=self.reset_filters)
        clear_button.pack(side="right", padx=5)

        # --- Results Area ---
        self.results_frame = CTkScrollableFrame(self)
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Status label
        self.status_label = CTkLabel(self, text="Enter search term above", anchor="w")
        self.status_label.pack(padx=20, pady=(0, 10), anchor="w")

        # Bind events
        self.search_var.trace_add("write", self.apply_filters)

    def get_unique_categories(self):
        """Extract unique categories from invoices"""
        return list({inv.get("category", "Uncategorized") for inv in self.invoices})

    def get_unique_dates(self):
        """Extract unique years from invoice dates"""
        return list({inv["Date"].split()[-1] for inv in self.invoices})

    def apply_filters(self, *args):
        query = self.search_var.get().lower()
        selected_category = self.category_var.get()
        selected_date = self.date_var.get()
        selected_amount = self.amount_var.get()

        self.filtered_invoices = self.invoices  # Reset base list

        # Apply filters one by one
        if selected_category != "All Categories":
            self.filtered_invoices = [inv for inv in self.filtered_invoices
                                      if inv.get("category", "") == selected_category]

        if selected_date != "All Dates":
            self.filtered_invoices = [inv for inv in self.filtered_invoices
                                      if selected_date in inv.get("Date", "")]

        if selected_amount != "Any Amount":
            try:
                low, high = self.parse_amount_range(selected_amount)
                self.filtered_invoices = [
                    inv for inv in self.filtered_invoices
                    if inv.get("Total") and
                    float(inv["Total"].replace("$", "").replace(",", "")) >= low and
                    float(inv["Total"].replace("$", "").replace(",", "")) <= high
                ]
            except Exception as e:
                print("Amount filter error:", e)

        # Apply search query
        results = []
        for inv in self.filtered_invoices:
            match = False
            for value in inv.values():
                if value is not None and str(value).lower().find(query) != -1:
                    match = True
                    break
            if match:
                results.append(inv)

        # Update UI
        self.clear_results()
        self.display_results(results)

    def parse_amount_range(self, amount_str):
        """Convert strings like '$0 - $100' or '$1000+' into min/max values"""
        amount_str = amount_str.strip()

        if "Any Amount" in amount_str:
            return (0, float('inf'))

        elif " - " in amount_str:
            low, high = amount_str.replace("$", "").split(" - ")
            return float(low), float(high)

        elif "+" in amount_str:
            low = amount_str.replace("$", "").replace("+", "")
            return float(low), float('inf')

        else:
            return 0, float('inf')

    def display_results(self, matches):
        if not matches:
            label = CTkLabel(self.results_frame, text="No matches found.", fg_color="transparent")
            label.pack(anchor="w", pady=2)
            self.status_label.configure(text="No matches found.")
            return

        self.status_label.configure(text=f"Found {len(matches)} matching invoice(s)")

        for idx, invoice in enumerate(matches):
            display_text = f"{invoice['Invoice Number']} - {invoice['Bill To']} - {invoice['Item']} - {invoice['Total']}"
            result_btn = CTkButton(
                self.results_frame,
                text=display_text,
                anchor="w",
                command=lambda inv=invoice: self.open_pdf(inv)
            )
            result_btn.pack(anchor="w", pady=2)
            self.result_index_map.append(invoice)

    def reset_filters(self):
        self.category_var.set("All Categories")
        self.date_var.set("All Dates")
        self.amount_var.set("Any Amount")
        self.filtered_invoices = self.invoices
        self.clear_results()

    def open_pdf(self, invoice):
        pdf_path = Path(PDF_DIR) / invoice['filename']

        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            return

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
