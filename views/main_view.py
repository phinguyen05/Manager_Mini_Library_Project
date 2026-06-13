import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ Thống Quản Lý Thư Viện Mini")
        self.geometry("1100x700")
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks() # Update geometry
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Main frame for consistent padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Style configuration for Notebook
        style = ttk.Style()
        style.configure("TNotebook", background="#2C3E50", borderwidth=0)
        style.configure("TNotebook.Tab", background="#34495E", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#1ABC9C")], foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
