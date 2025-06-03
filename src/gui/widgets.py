from tkinter import END, image_names
from customtkinter import *

class StandardFrame(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StandardButton(CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            font=("Arial", 14),
            corner_radius=8,
            height=40,
        )

class StandardLabel(CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            font=("Arial", 20)
        )
class LogPanel(StandardFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_textbox = CTkTextbox(self, wrap="none", state="disabled")
        self.log_textbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def write(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(END, message)
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see(END)

    def clear(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", END)
        self.log_textbox.configure(state="disabled")
