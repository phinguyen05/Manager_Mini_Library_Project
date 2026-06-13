from tkinter import messagebox
import tkinter as tk

class ReaderController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.setup_bindings()
        self.refresh_table()

    def setup_bindings(self):
        self.view.add_reader_btn.config(command=self.add_reader)
        self.view.clear_btn.config(command=self.clear_fields)
        self.view.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.view.view_history_btn.config(command=self.show_borrow_history)

    def refresh_table(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        readers = self.model.get_all_readers()
        for idx, reader in enumerate(readers, start=1):
            self.view.tree.insert("", tk.END, values=(idx, reader[0], reader[1], reader[2], reader[3], reader[4]))

    def on_tree_select(self, event):
        selected_item = self.view.tree.focus()
        if not selected_item:
            return
        values = self.view.tree.item(selected_item, "values")
        if values:
            data = {
                "code": values[1],
                "full_name": values[2],
                "email": values[3],
                "phone": values[4]
            }
            self.view.set_inputs(data)

    def add_reader(self):
        inputs = self.view.get_inputs()
        
        if not inputs["code"] or not inputs["full_name"]:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đầy đủ Mã ĐG và Họ tên (*)")
            return

        existing = self.model.get_reader_by_code(inputs["code"])
        if existing:
            messagebox.showerror("Lỗi trùng mã", f"Mã độc giả \'{inputs["code"]}\' đã tồn tại trong hệ thống!")
            return

        try:
            self.model.add_reader(
                inputs["code"],
                inputs["full_name"],
                inputs["email"],
                inputs["phone"]
            )
            messagebox.showinfo("Thành công", "Đăng ký độc giả mới thành công!")
            self.clear_fields()
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đăng ký độc giả: {str(e)}")

    def clear_fields(self):
        self.view.clear_inputs()

    def show_borrow_history(self):
        selected_item = self.view.tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn độc giả", "Vui lòng chọn một độc giả để xem lịch sử mượn.")
            return
        
        values = self.view.tree.item(selected_item, "values")
        reader_code = values[1]
        
        history = self.model.get_borrow_history(reader_code)
        self.view.show_borrow_history_popup(reader_code, history)
