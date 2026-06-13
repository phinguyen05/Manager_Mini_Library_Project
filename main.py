from models.database import Database
from models.book_model import BookModel
from models.reader_model import ReaderModel
from models.borrow_model import BorrowModel
from views.main_view import MainView
from views.book_view import BookView
from views.reader_view import ReaderView
from views.borrow_view import BorrowView
from controllers.book_controller import BookController
from controllers.reader_controller import ReaderController
from controllers.borrow_controller import BorrowController

def main():
    db = Database()
    
    # Models
    book_model = BookModel(db)
    reader_model = ReaderModel(db)
    borrow_model = BorrowModel(db)
    
    # Main window + Views
    app = MainView()
    book_view = BookView(app.notebook)
    reader_view = ReaderView(app.notebook)
    borrow_view = BorrowView(app.notebook)
    
    # Add tabs
    app.notebook.add(book_view, text="📚 Quản Lý Sách")
    app.notebook.add(reader_view, text="👤 Quản Lý Độc Giả")
    app.notebook.add(borrow_view, text="📋 Mượn / Trả Sách")
    
    # Controllers
    BookController(book_view, book_model)
    ReaderController(reader_view, reader_model)
    BorrowController(borrow_view, borrow_model, book_model, reader_model)
    
    app.mainloop()

if __name__ == "__main__":
    main()
