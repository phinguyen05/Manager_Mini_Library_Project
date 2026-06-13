import tkinter as tk
from tkinter import ttk

class BookView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Configure layout padding
        self.grid_rowconfigure(0, weight=0) # Form Frame
        self.grid_rowconfigure(1, weight=0) # Search Frame
        self.grid_rowconfigure(2, weight=1) # Treeview Frame
        self.grid_columnconfigure(0, weight=1)

        # Style configurations
        style = ttk.Style()
        style.configure("Header.TLabelframe", font=("Helvetica", 11, "bold"))
        style.configure("Action.TButton", font=("Helvetica", 10))

        # ==========================================
        # PANEL TRÊN: FORM NHẬP LIỆU
        # ==========================================
        form_lf = ttk.LabelFrame(self, text="Thông tin chi tiết Sách", padding=10)
        form_lf.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Configure columns inside form_lf
        for idx in range(6):
            form_lf.grid_columnconfigure(idx, weight=1)

        # Labels & Entry Fields
        ttk.Label(form_lf, text="Mã sách (*):", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.code_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Tên sách (*):", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.title_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Tác giả (*):", font=("Helvetica", 10)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.author_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.author_entry.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Thể loại:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.category_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Số lượng (*):", font=("Helvetica", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.quantity_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.quantity_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Năm xuất bản:", font=("Helvetica", 10)).grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.year_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.year_entry.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

        # Buttons Frame within upper panel
        btn_frame = ttk.Frame(form_lf)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

        self.add_btn = ttk.Button(btn_frame, text="➕ Thêm", width=12)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.update_btn = ttk.Button(btn_frame, text="💾 Cập nhật", width=12)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="❌ Xóa", width=12)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="🧹 Làm mới", width=12)
        self.clear_btn.grid(row=0, column=3, padx=5)


        # ==========================================
        # PANEL GIỮA: TÌM KIẾM
        # ==========================================
        search_lf = ttk.LabelFrame(self, text="Tìm kiếm Sách", padding=5)
        search_lf.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(search_lf, text="Từ khóa tìm kiếm:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_lf, font=("Helvetica", 10), width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        self.search_btn = ttk.Button(search_lf, text="🔍 Tìm kiếm", width=12)
        self.search_btn.grid(row=0, column=2, padx=5, pady=5)


        # ==========================================
        # PANEL DƯỚI: DANH SÁCH SÁCH
        # ==========================================
        list_lf = ttk.LabelFrame(self, text="Danh sách Sách", padding=5)
        list_lf.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        list_lf.grid_rowconfigure(0, weight=1)
        list_lf.grid_columnconfigure(0, weight=1)

        # Treeview Columns
        columns = ("stt", "code", "title", "author", "category", "quantity", "year")
        self.tree = ttk.Treeview(list_lf, columns=columns, show="headings")

        self.tree.heading("stt", text="STT")
        self.tree.heading("code", text="Mã Sách")
        self.tree.heading("title", text="Tên Sách")
        self.tree.heading("author", text="Tác giả")
        self.tree.heading("category", text="Thể loại")
        self.tree.heading("quantity", text="Số lượng")
        self.tree.heading("year", text="Năm XB")

        self.tree.column("stt", width=50, anchor="center")
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("title", width=250, anchor="w")
        self.tree.column("author", width=150, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("quantity", width=80, anchor="center")
        self.tree.column("year", width=80, anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(list_lf, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_lf, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    def get_inputs(self):
        return {
            "code": self.code_entry.get().strip(),
            "title": self.title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "category": self.category_entry.get().strip(),
            "quantity": self.quantity_entry.get().strip(),
            "year": self.year_entry.get().strip()
        }

    def set_inputs(self, data):
        self.clear_inputs()
        self.code_entry.insert(0, data.get("code", ""))
        self.title_entry.insert(0, data.get("title", ""))
        self.author_entry.insert(0, data.get("author", ""))
        self.category_entry.insert(0, data.get("category", ""))
        self.quantity_entry.insert(0, str(data.get("quantity", "")))
        self.year_entry.insert(0, str(data.get("year", "")))

    def clear_inputs(self):
        self.code_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
