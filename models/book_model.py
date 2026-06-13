class BookModel:
    def __init__(self, db):
        self.db = db

    def add_book(self, code, title, author, category, quantity, year):
        query = """
        INSERT INTO books (code, title, author, category, quantity, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (code, title, author, category, quantity, year))

    def update_book(self, code, title, author, category, quantity, year):
        query = """
        UPDATE books
        SET title = ?, author = ?, category = ?, quantity = ?, year = ?
        WHERE code = ?
        """
        self.db.execute_query(query, (title, author, category, quantity, year, code))

    def delete_book(self, code):
        query = "DELETE FROM books WHERE code = ?"
        self.db.execute_query(query, (code,))

    def search_books(self, keyword):
        query = """
        SELECT code, title, author, category, quantity, year
        FROM books
        WHERE title LIKE ? OR author LIKE ? OR category LIKE ? OR code LIKE ?
        """
        pattern = f"%{keyword}%"
        return self.db.fetch_all(query, (pattern, pattern, pattern, pattern))

    def get_all_books(self):
        query = "SELECT code, title, author, category, quantity, year FROM books"
        return self.db.fetch_all(query)

    def get_book_by_code(self, code):
        query = "SELECT code, title, author, category, quantity, year FROM books WHERE code = ?"
        return self.db.fetch_one(query, (code,))

    def update_quantity(self, code, delta):
        # delta can be positive (return book) or negative (borrow book)
        query = "UPDATE books SET quantity = quantity + ? WHERE code = ?"
        self.db.execute_query(query, (delta, code))
