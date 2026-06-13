from models.database import Database
from datetime import datetime, timedelta

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
        query_get_borrow = "SELECT due_date FROM borrows WHERE borrow_code = ?"
        borrow = self.db.fetch_one(query_get_borrow, (borrow_code,))

        if not borrow:
            raise ValueError(f"Không tìm thấy phiếu mượn với mã: {borrow_code}")

        due_date_str = borrow[0]
        
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()

        fine = 0
        if return_date_obj > due_date:
            days_late = (return_date_obj - due_date).days
            fine = days_late * 5000  # 5000 VND per day

        query_update_borrow = """
        UPDATE borrows
        SET return_date = ?, status = ?, fine = ?
        WHERE borrow_code = ?
        """
        self.db.execute_query(query_update_borrow, (return_date, 'Đã trả', fine, borrow_code))
        return fine

    def get_all_borrows(self):
        query = """
        SELECT
            br.borrow_code, b.title, r.full_name, br.borrow_date, br.due_date, br.return_date, br.status, br.fine
        FROM
            borrows AS br
        JOIN
            books AS b ON br.book_code = b.code
        JOIN
            readers AS r ON br.reader_code = r.code
        ORDER BY br.borrow_date DESC
        """
        return self.db.fetch_all(query)

    def get_active_borrows(self):
        query = """
        SELECT
            br.borrow_code, b.title, r.full_name, br.borrow_date, br.due_date, br.status
        FROM
            borrows AS br
        JOIN
            books AS b ON br.book_code = b.code
        JOIN
            readers AS r ON br.reader_code = r.code
        WHERE
            br.status = 'Đang mượn'
        ORDER BY br.borrow_date DESC
        """
        return self.db.fetch_all(query)
    
    def get_borrow_by_code(self, borrow_code):
        query = "SELECT borrow_code, book_code, reader_code, borrow_date, due_date, return_date, status, fine FROM borrows WHERE borrow_code = ?"
        return self.db.fetch_one(query, (borrow_code,))
