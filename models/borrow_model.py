from models.database import Database
from datetime import datetime

class BorrowModel:
    def __init__(self, db):
        self.db = db

    def create_borrow(self, borrow_code, book_code, reader_code, borrow_date, due_date):
        query = """
        INSERT INTO borrows (borrow_code, book_code, reader_code, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (borrow_code, book_code, reader_code, borrow_date, due_date, 'Đang mượn'))

    def return_book(self, borrow_code, return_date):
        # Tính tiền phạt nếu trễ hạn (Giả sử 5000đ/ngày)
        query_get = "SELECT due_date FROM borrows WHERE borrow_code = ?"
        borrow = self.db.fetch_one(query_get, (borrow_code,))
        fine = 0
        
        if borrow:
            due_date = datetime.fromisoformat(borrow[0])
            ret_date = datetime.fromisoformat(return_date)
            if ret_date > due_date:
                days_late = (ret_date - due_date).days
                fine = days_late * 5000 

        query_update = """
        UPDATE borrows
        SET return_date = ?, status = 'Đã trả', fine = ?
        WHERE borrow_code = ?
        """
        self.db.execute_query(query_update, (return_date, fine, borrow_code))
        return fine

    def get_all_borrows(self):
        query = """
        SELECT br.borrow_code, b.title, r.full_name, br.borrow_date, br.due_date, br.return_date, br.status, br.fine
        FROM borrows AS br
        JOIN books AS b ON br.book_code = b.code
        JOIN readers AS r ON br.reader_code = r.code
        ORDER BY br.borrow_date DESC
        """
        return self.db.fetch_all(query)

    def get_active_borrows(self):
        query = """
        SELECT br.borrow_code, b.title, r.full_name, br.borrow_date, br.due_date, br.status
        FROM borrows AS br
        JOIN books AS b ON br.book_code = b.code
        JOIN readers AS r ON br.reader_code = r.code
        WHERE br.status = 'Đang mượn'
        """
        return self.db.fetch_all(query)