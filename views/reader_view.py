import tkinter as tk
from tkinter import ttk, messagebox

class ReaderView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ==========================================
        # PANEL TRÊN: FORM NHẬP LIỆU ĐỘC GIẢ
        # ==========================================
        form_lf = ttk.LabelFrame(self, text="Thông tin Độc giả", padding=10)
        form_lf.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        for i in range(4):
            form_lf.grid_columnconfigure(i, weight=1)

        ttk.Label(form_lf, text="Mã ĐG (*):", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.code_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Họ tên (*):", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.full_name_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.full_name_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Email:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.email_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_lf, text="Số điện thoại:", font=("Helvetica", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.phone_entry = ttk.Entry(form_lf, font=("Helvetica", 10))
        self.phone_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        btn_frame = ttk.Frame(form_lf)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.add_reader_btn = ttk.Button(btn_frame, text="➕ Đăng ký", width=15)
        self.add_reader_btn.grid(row=0, column=0, padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="🧹 Làm mới", width=15)
        self.clear_btn.grid(row=0, column=1, padx=5)
        

        # ==========================================
        # PANEL DƯỚI: DANH SÁCH ĐỘC GIẢ
        # ==========================================
        list_lf = ttk.LabelFrame(self, text="Danh sách Độc giả", padding=5)
        list_lf.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        list_lf.grid_rowconfigure(0, weight=1)
        list_lf.grid_columnconfigure(0, weight=1)

        columns = ("stt", "code", "full_name", "email", "phone", "register_date")
        self.tree = ttk.Treeview(list_lf, columns=columns, show="headings")

        self.tree.heading("stt", text="STT")
        self.tree.heading("code", text="Mã ĐG")
        self.tree.heading("full_name", text="Họ tên")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="SĐT")
        self.tree.heading("register_date", text="Ngày ĐK")

        self.tree.column("stt", width=50, anchor="center")
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("full_name", width=200, anchor="w")
        self.tree.column("email", width=180, anchor="w")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("register_date", width=120, anchor="center")

        vsb = ttk.Scrollbar(list_lf, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_lf, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Bottom buttons for history
        bottom_btn_frame = ttk.Frame(list_lf)
        bottom_btn_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="e")
        self.view_history_btn = ttk.Button(bottom_btn_frame, text="📋 Xem lịch sử mượn", width=20)
        self.view_history_btn.pack(side=tk.RIGHT, padx=5)


    def get_inputs(self):
        return {
            "code": self.code_entry.get().strip(),
            "full_name": self.full_name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip()
        }

    def set_inputs(self, data):
        self.clear_inputs()
        self.code_entry.insert(0, data.get("code", ""))
        self.full_name_entry.insert(0, data.get("full_name", ""))
        self.email_entry.insert(0, data.get("email", ""))
        self.phone_entry.insert(0, data.get("phone", ""))

    def clear_inputs(self):
        self.code_entry.delete(0, tk.END)
        self.full_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def show_borrow_history_popup(self, reader_code, history_data):
        popup = tk.Toplevel(self)
        popup.title(f"Lịch sử mượn của ĐG: {reader_code}")
        popup.geometry("700x400")
        popup.grab_set() # Make it modal

        # Treeview for history
        history_tree = ttk.Treeview(popup, columns=("title", "author", "borrow_date", "due_date", "return_date", "status", "fine"), show="headings")
        history_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        history_tree.heading("title", text="Tên Sách")
        history_tree.heading("author", text="Tác giả")
        history_tree.heading("borrow_date", text="Ngày Mượn")
        history_tree.heading("due_date", text="Hạn Trả")
        history_tree.heading("return_date", text="Ngày Trả")
        history_tree.heading("status", text="Trạng thái")
        history_tree.heading("fine", text="Tiền phạt")

        history_tree.column("title", width=150, anchor="w")
        history_tree.column("author", width=100, anchor="w")
        history_tree.column("borrow_date", width=100, anchor="center")
        history_tree.column("due_date", width=100, anchor="center")
        history_tree.column("return_date", width=100, anchor="center")
        history_tree.column("status", width=100, anchor="center")
        history_tree.column("fine", width=80, anchor="center")

        for item in history_data:
            history_tree.insert("", tk.END, values=item)

        # Add scrollbars to history_tree
        vsb = ttk.Scrollbar(popup, orient="vertical", command=history_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        history_tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(popup, orient="horizontal", command=history_tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        history_tree.configure(xscrollcommand=hsb.set)

        # Close button
        close_btn = ttk.Button(popup, text="Đóng", command=popup.destroy)
        close_btn.pack(pady=10)
