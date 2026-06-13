import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class BorrowView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ==========================================
        # LabelFrame: Tạo Phiếu Mượn
        # ==========================================
        borrow_lf = ttk.LabelFrame(self, text="📖 Tạo Phiếu Mượn", padding=10)
        borrow_lf.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        for i in range(4):
            borrow_lf.grid_columnconfigure(i, weight=1)

        ttk.Label(borrow_lf, text="Mã phiếu: ", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.borrow_code_entry = ttk.Entry(borrow_lf, font=("Helvetica", 10), state="readonly")
        self.borrow_code_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.generate_borrow_code()

        ttk.Label(borrow_lf, text="Mã sách (*): ", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.book_code_entry = ttk.Entry(borrow_lf, font=("Helvetica", 10))
        self.book_code_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(borrow_lf, text="Mã độc giả (*): ", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.reader_code_entry = ttk.Entry(borrow_lf, font=("Helvetica", 10))
        self.reader_code_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(borrow_lf, text="Ngày mượn (*): ", font=("Helvetica", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.borrow_date_entry = ttk.Entry(borrow_lf, font=("Helvetica", 10))
        self.borrow_date_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        self.borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(borrow_lf, text="Hạn trả (*): ", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.due_date_entry = ttk.Entry(borrow_lf, font=("Helvetica", 10))
        self.due_date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))

        self.create_borrow_btn = ttk.Button(borrow_lf, text="➕ Tạo phiếu mượn", width=20)
        self.create_borrow_btn.grid(row=3, column=0, columnspan=4, pady=10)


        # ==========================================
        # LabelFrame: Trả Sách
        # ==========================================
        return_lf = ttk.LabelFrame(self, text="↩️ Trả Sách", padding=10)
        return_lf.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        for i in range(4):
            return_lf.grid_columnconfigure(i, weight=1)

        ttk.Label(return_lf, text="Mã phiếu mượn (*): ", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.return_borrow_code_entry = ttk.Entry(return_lf, font=("Helvetica", 10))
        self.return_borrow_code_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(return_lf, text="Ngày trả (*): ", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.return_date_entry = ttk.Entry(return_lf, font=("Helvetica", 10))
        self.return_date_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.return_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.return_book_btn = ttk.Button(return_lf, text="✅ Xác nhận trả sách", width=25)
        self.return_book_btn.grid(row=1, column=0, columnspan=4, pady=10)


        # ==========================================
        # Treeview: Danh sách phiếu đang mượn
        # ==========================================
        active_borrows_lf = ttk.LabelFrame(self, text="📋 Phiếu Mượn Đang Hoạt Động", padding=5)
        active_borrows_lf.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        active_borrows_lf.grid_rowconfigure(0, weight=1)
        active_borrows_lf.grid_columnconfigure(0, weight=1)

        columns = ("borrow_code", "book_title", "reader_name", "borrow_date", "due_date", "status")
        self.tree = ttk.Treeview(active_borrows_lf, columns=columns, show="headings")

        self.tree.heading("borrow_code", text="Mã Phiếu")
        self.tree.heading("book_title", text="Tên Sách")
        self.tree.heading("reader_name", text="Tên Độc giả")
        self.tree.heading("borrow_date", text="Ngày Mượn")
        self.tree.heading("due_date", text="Hạn Trả")
        self.tree.heading("status", text="Trạng thái")

        self.tree.column("borrow_code", width=120, anchor="center")
        self.tree.column("book_title", width=250, anchor="w")
        self.tree.column("reader_name", width=180, anchor="w")
        self.tree.column("borrow_date", width=100, anchor="center")
        self.tree.column("due_date", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        vsb = ttk.Scrollbar(active_borrows_lf, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(active_borrows_lf, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def generate_borrow_code(self):
        today = datetime.now().strftime("%Y%m%d")
        # This is a placeholder; a real implementation would check the DB for existing codes
        # and generate a unique suffix.
        # For now, we'll just use a simple static code.
        # In a real app, you'd likely have a counter in the DB or a more robust UUID system.
        self.borrow_code_entry.config(state=tk.NORMAL)
        self.borrow_code_entry.delete(0, tk.END)
        self.borrow_code_entry.insert(0, f"PM-{today}-001")
        self.borrow_code_entry.config(state="readonly")

    def get_borrow_inputs(self):
        return {
            "borrow_code": self.borrow_code_entry.get().strip(),
            "book_code": self.book_code_entry.get().strip(),
            "reader_code": self.reader_code_entry.get().strip(),
            "borrow_date": self.borrow_date_entry.get().strip(),
            "due_date": self.due_date_entry.get().strip()
        }

    def get_return_inputs(self):
        return {
            "borrow_code": self.return_borrow_code_entry.get().strip(),
            "return_date": self.return_date_entry.get().strip()
        }

    def clear_borrow_inputs(self):
        # Only clear editable fields
        self.book_code_entry.delete(0, tk.END)
        self.reader_code_entry.delete(0, tk.END)
        self.borrow_date_entry.delete(0, tk.END)
        self.borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        self.generate_borrow_code()

    def clear_return_inputs(self):
        self.return_borrow_code_entry.delete(0, tk.END)
        self.return_date_entry.delete(0, tk.END)
        self.return_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        values = self.tree.item(selected_item, "values")
        if values:
            self.return_borrow_code_entry.delete(0, tk.END)
            self.return_borrow_code_entry.insert(0, values[0])
