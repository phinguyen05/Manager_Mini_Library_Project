from tkinter import messagebox
from datetime import datetime

class BorrowController:
    def __init__(self, view, borrow_model, book_model, reader_model):
        self.view = view
        self.borrow_model = borrow_model
        self.book_model = book_model
        self.reader_model = reader_model
        self.setup_bindings()
        self.refresh_active_borrows_table()

    def setup_bindings(self):
        self.view.create_borrow_btn.config(command=self.create_borrow)
        self.view.return_book_btn.config(command=self.return_book)
        self.view.tree.bind("<<TreeviewSelect>>", self.view.on_tree_select)

    def refresh_active_borrows_table(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        active_borrows = self.borrow_model.get_active_borrows()
        for borrow in active_borrows:
            self.view.tree.insert("", "end", values=borrow)

    def create_borrow(self):
        inputs = self.view.get_borrow_inputs()

        borrow_code = inputs["borrow_code"]
        book_code = inputs["book_code"]
        reader_code = inputs["reader_code"]
        borrow_date = inputs["borrow_date"]
        due_date = inputs["due_date"]

        if not book_code or not reader_code or not borrow_date or not due_date:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đầy đủ các trường bắt buộc cho phiếu mượn (*)")
            return
        
        # Date validation
        try:
            datetime.strptime(borrow_date, "%Y-%m-%d")
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Ngày mượn và Hạn trả phải có định dạng YYYY-MM-DD.")
            return

        # Check if book exists and is available
        book = self.book_model.get_book_by_code(book_code)
        if not book:
            messagebox.showerror("Lỗi", f"Mã sách \'{book_code}\' không tồn tại.")
            return
        if book[4] <= 0: # Assuming quantity is at index 4
            messagebox.showwarning("Sách đã hết", "Sách đã hết, không thể mượn!")
            return

        # Check if reader exists
        reader = self.reader_model.get_reader_by_code(reader_code)
        if not reader:
            messagebox.showerror("Lỗi", f"Mã độc giả \'{reader_code}\' không tồn tại.")
            return

        # Check if borrow code already exists
        if self.borrow_model.get_borrow_by_code(borrow_code):
            messagebox.showerror("Lỗi", f"Mã phiếu mượn \'{borrow_code}\' đã tồn tại. Vui lòng thử lại hoặc làm mới.")
            return

        try:
            self.borrow_model.create_borrow(borrow_code, book_code, reader_code, borrow_date, due_date)
            self.book_model.update_quantity(book_code, -1) # Decrease book quantity
            messagebox.showinfo("Thành công", "Tạo phiếu mượn thành công!")
            self.view.clear_borrow_inputs()
            self.refresh_active_borrows_table()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi khi tạo phiếu mượn: {str(e)}")

    def return_book(self):
        inputs = self.view.get_return_inputs()

        borrow_code = inputs["borrow_code"]
        return_date = inputs["return_date"]

        if not borrow_code or not return_date:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đầy đủ Mã phiếu mượn và Ngày trả (*)")
            return
        
        # Date validation
        try:
            datetime.strptime(return_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Ngày trả phải có định dạng YYYY-MM-DD.")
            return

        # Check if borrow exists and is active
        borrow = self.borrow_model.get_borrow_by_code(borrow_code)
        if not borrow:
            messagebox.showerror("Lỗi", f"Không tìm thấy phiếu mượn với mã \'{borrow_code}\'")
            return
        if borrow[6] == 'Đã trả': # Assuming status is at index 6
            messagebox.showwarning("Phiếu đã trả", f"Phiếu mượn \'{borrow_code}\' đã được trả trước đó.")
            return

        try:
            book_code = borrow[1] # Assuming book_code is at index 1
            fine = self.borrow_model.return_book(borrow_code, return_date)
            self.book_model.update_quantity(book_code, 1) # Increase book quantity

            if fine > 0:
                messagebox.showinfo("Trả sách trễ hạn", f"Trả sách thành công! Trả trễ {(fine // 5000)} ngày. Tiền phạt: {fine:,}đ")
            else:
                messagebox.showinfo("Thành công", "Trả sách thành công!")
            
            self.view.clear_return_inputs()
            self.refresh_active_borrows_table()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi khi trả sách: {str(e)}")
