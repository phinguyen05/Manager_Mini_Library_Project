from models.database import Database

class ReaderModel:
    def __init__(self, db):
        self.db = db

    def add_reader(self, code, full_name, email, phone):
        query = """
        INSERT INTO readers (code, full_name, email, phone)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (code, full_name, email, phone))

    def get_all_readers(self):
        query = "SELECT code, full_name, email, phone, register_date FROM readers"
        return self.db.fetch_all(query)

    def get_reader_by_code(self, code):
        query = "SELECT code, full_name, email, phone, register_date FROM readers WHERE code = ?"
        return self.db.fetch_one(query, (code,))

    def get_borrow_history(self, reader_code):
        query = """
        SELECT
            b.title, b.author, br.borrow_date, br.due_date, br.return_date, br.status, br.fine
        FROM
            borrows AS br
        JOIN
            books AS b ON br.book_code = b.code
        WHERE
            br.reader_code = ?
        ORDER BY br.borrow_date DESC
        """
        return self.db.fetch_all(query, (reader_code,))
