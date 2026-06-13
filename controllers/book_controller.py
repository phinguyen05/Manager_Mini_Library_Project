from tkinter import messagebox
import tkinter as tk

class BookController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.setup_bindings()
        self.refresh_table()

    def setup_bindings(self):
        self.view.add_btn.config(command=self.add_book)
        self.view.update_btn.config(command=self.update_book)
        self.view.delete_btn.config(command=self.delete_book)
        self.view.clear_btn.config(command=self.clear_fields)
        self.view.search_btn.config(command=self.search_books)
        self.view.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def refresh_table(self, books=None):
        # Clear existing items
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        if books is None:
            books = self.model.get_all_books()

        for idx, book in enumerate(books, start=1):
            self.view.tree.insert("", tk.END, values=(idx, book[0], book[1], book[2], book[3], book[4], book[5]))

    def on_tree_select(self, event):
        selected_item = self.view.tree.focus()
        if not selected_item:
            return
        values = self.view.tree.item(selected_item, "values")
        if values:
            data = {
                "code": values[1],
                "title": values[2],
                "author": values[3],
                "category": values[4],
                "quantity": values[5],
                "year": values[6]
            }
            self.view.set_inputs(data)

    def add_book(self):
        inputs = self.view.get_inputs()
        
        # Validation
        if not inputs["code"] or not inputs["title"] or not inputs["author"] or not inputs["quantity"]:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đầy đủ các trường bắt buộc (*)")
            return

        # Quantity validation
        try:
            quantity = int(inputs["quantity"])
            if quantity < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng phải là một số nguyên không âm (>= 0)")
            return

        # Year validation (optional)
        year = None
        if inputs["year"]:
            try:
                year = int(inputs["year"])
                if year < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Năm xuất bản phải là số nguyên hợp lệ")
                return

        # Check existing code
        existing = self.model.get_book_by_code(inputs["code"])
        if existing:
            messagebox.showerror("Lỗi trùng mã", f"Mã sách '{inputs['code']}' đã tồn tại trong hệ thống!")
            return

        try:
            self.model.add_book(
                inputs["code"],
                inputs["title"],
                inputs["author"],
                inputs["category"],
                quantity,
                year
            )
            messagebox.showinfo("Thành công", "Thêm sách mới thành công!")
            self.clear_fields()
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể thêm sách: {str(e)}")

    def update_book(self):
        inputs = self.view.get_inputs()
        
        if not inputs["code"]:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng chọn hoặc nhập Mã sách cần cập nhật")
            return

        if not inputs["title"] or not inputs["author"] or not inputs["quantity"]:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng điền đầy đủ thông tin Tên sách, Tác giả và Số lượng")
            return

        # Quantity validation
        try:
            quantity = int(inputs["quantity"])
            if quantity < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng phải là một số nguyên không âm (>= 0)")
            return

        # Year validation (optional)
        year = None
        if inputs["year"]:
            try:
                year = int(inputs["year"])
                if year < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu", "Năm xuất bản phải là số nguyên hợp lệ")
                return

        # Verify that the book exists
        existing = self.model.get_book_by_code(inputs["code"])
        if not existing:
            messagebox.showerror("Lỗi", f"Không tìm thấy sách có mã '{inputs['code']}' để cập nhật!")
            return

        try:
            self.model.update_book(
                inputs["code"],
                inputs["title"],
                inputs["author"],
                inputs["category"],
                quantity,
                year
            )
            messagebox.showinfo("Thành công", "Cập nhật thông tin sách thành công!")
            self.clear_fields()
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể cập nhật sách: {str(e)}")

    def delete_book(self):
        inputs = self.view.get_inputs()
        code = inputs["code"]
        
        if not code:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoặc nhập Mã sách cần xóa")
            return

        existing = self.model.get_book_by_code(code)
        if not existing:
            messagebox.showerror("Lỗi", f"Không tìm thấy sách có mã '{code}'!")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa sách '{existing[1]}' (Mã: {code}) không?")
        if confirm:
            try:
                self.model.delete_book(code)
                messagebox.showinfo("Thành công", "Xóa sách thành công!")
                self.clear_fields()
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể xóa sách: {str(e)}")

    def clear_fields(self):
        self.view.clear_inputs()
        self.view.search_entry.delete(0, tk.END)

    def search_books(self):
        keyword = self.view.search_entry.get().strip()
        results = self.model.search_books(keyword)
        self.refresh_table(results)
