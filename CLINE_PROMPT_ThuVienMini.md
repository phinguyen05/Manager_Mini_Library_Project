# PROMPT CHO CLINE – HỆ THỐNG QUẢN LÝ THƯ VIỆN MINI

> **Cách dùng:** Copy toàn bộ nội dung bên dưới, dán vào ô "Type your task here..." của Cline rồi nhấn Send.

---

## NHIỆM VỤ TỔNG QUAN

Xây dựng hoàn chỉnh hệ thống **Mini Library Management System** theo kiến trúc MVC bằng Python, bao gồm giao diện đồ họa, logic xử lý, cơ sở dữ liệu SQLite, cấu hình Git và file README.md. Dự án đặt tại thư mục hiện tại (`Mini_Library_Project`).

---

## BƯỚC 1 – KHỞI TẠO GIT TRƯỚC KHI VIẾT CODE

```bash
git init
git checkout -b main
```

Tạo file `.gitignore` với nội dung:
```
__pycache__/
*.pyc
*.db
*.sqlite
.env
.vscode/
```

Commit khởi tạo:
```bash
git add .gitignore
git commit -m "chore: initial project setup with .gitignore"
```

---

## BƯỚC 2 – CẤU TRÚC THƯ MỤC DỰ ÁN

Tạo đúng cấu trúc sau (kiến trúc MVC):

```
Mini_Library_Project/
├── models/
│   ├── __init__.py
│   ├── database.py        # Kết nối & khởi tạo SQLite
│   ├── book_model.py      # CRUD sách
│   ├── reader_model.py    # CRUD độc giả
│   └── borrow_model.py    # CRUD phiếu mượn/trả
├── views/
│   ├── __init__.py
│   ├── main_view.py       # Cửa sổ chính, thanh điều hướng
│   ├── book_view.py       # Tab quản lý sách
│   ├── reader_view.py     # Tab quản lý độc giả
│   └── borrow_view.py     # Tab mượn/trả sách
├── controllers/
│   ├── __init__.py
│   ├── book_controller.py
│   ├── reader_controller.py
│   └── borrow_controller.py
├── main.py                # Entry point
├── requirements.txt
└── README.md
```

---

## BƯỚC 3 – CÔNG NGHỆ SỬ DỤNG

- **Ngôn ngữ:** Python 3.x  
- **GUI:** `tkinter` + `ttk` (thư viện chuẩn, không cần cài thêm)  
- **Database:** SQLite qua module `sqlite3` (chuẩn, không cần cài thêm)  
- **Kiến trúc:** MVC — Model (dữ liệu) / View (giao diện) / Controller (logic)

`requirements.txt` chỉ cần:
```
# No external dependencies required
# Python standard library only (tkinter, sqlite3)
```

---

## BƯỚC 4 – CHI TIẾT TRIỂN KHAI

### 4.1 – MODEL: `models/database.py`
- Tạo class `Database` khởi tạo kết nối SQLite file `library.db`
- `__init__` tạo 3 bảng nếu chưa tồn tại:

```sql
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT,
    quantity INTEGER DEFAULT 0,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    register_date TEXT DEFAULT (DATE('now'))
);

CREATE TABLE IF NOT EXISTS borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrow_code TEXT UNIQUE NOT NULL,
    book_code TEXT NOT NULL,
    reader_code TEXT NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT DEFAULT 'Đang mượn',
    fine INTEGER DEFAULT 0,
    FOREIGN KEY (book_code) REFERENCES books(code),
    FOREIGN KEY (reader_code) REFERENCES readers(code)
);
```

### 4.2 – MODEL: `models/book_model.py`
Implement class `BookModel` với các method:
- `add_book(code, title, author, category, quantity, year)` → INSERT
- `update_book(code, title, author, category, quantity, year)` → UPDATE
- `delete_book(code)` → DELETE
- `search_books(keyword)` → SELECT WHERE title/author/category LIKE %keyword%
- `get_all_books()` → SELECT tất cả
- `get_book_by_code(code)` → SELECT theo mã
- `update_quantity(code, delta)` → tăng/giảm quantity (dùng cho mượn/trả)

### 4.3 – MODEL: `models/reader_model.py`
Implement class `ReaderModel`:
- `add_reader(code, full_name, email, phone)` → INSERT
- `get_all_readers()` → SELECT tất cả
- `get_reader_by_code(code)` → SELECT theo mã
- `get_borrow_history(reader_code)` → JOIN borrows với books để lấy lịch sử

### 4.4 – MODEL: `models/borrow_model.py`
Implement class `BorrowModel`:
- `create_borrow(borrow_code, book_code, reader_code, borrow_date, due_date)` → INSERT
- `return_book(borrow_code, return_date)`:
  - Tính số ngày trễ = return_date - due_date (nếu > 0)
  - Tính tiền phạt = số ngày trễ × 5000 (đồng)
  - UPDATE status='Đã trả', return_date, fine
- `get_all_borrows()` → SELECT tất cả JOIN tên sách, tên độc giả
- `get_active_borrows()` → SELECT WHERE status='Đang mượn'

### 4.5 – VIEW: `views/main_view.py`
- Tạo class `MainView(tk.Tk)`:
  - Tiêu đề: "Hệ Thống Quản Lý Thư Viện Mini"
  - Kích thước: 1100x700, căn giữa màn hình
  - Dùng `ttk.Notebook` với 3 tab: "📚 Quản Lý Sách" | "👤 Quản Lý Độc Giả" | "📋 Mượn / Trả Sách"
  - Màu nền header: #2C3E50, chữ trắng

### 4.6 – VIEW: `views/book_view.py`
Frame "Quản Lý Sách" gồm:
- **Panel trên:** Form nhập liệu (Mã sách, Tên sách, Tác giả, Thể loại, Số lượng, Năm XB) + các nút: `Thêm`, `Cập nhật`, `Xóa`, `Làm mới`
- **Panel giữa:** Ô tìm kiếm + nút `Tìm kiếm`
- **Panel dưới:** `ttk.Treeview` hiển thị danh sách sách, cột: STT | Mã sách | Tên sách | Tác giả | Thể loại | Số lượng | Năm XB
- Click vào dòng trong bảng → tự động điền vào form

### 4.7 – VIEW: `views/reader_view.py`
Frame "Quản Lý Độc Giả" gồm:
- **Panel trên:** Form nhập (Mã ĐG, Họ tên, Email, Số điện thoại) + nút `Đăng ký`, `Làm mới`
- **Panel dưới:** Treeview danh sách độc giả: STT | Mã ĐG | Họ tên | Email | SĐT | Ngày đăng ký
- Nút `Xem lịch sử mượn`: mở popup `Toplevel` hiển thị lịch sử mượn của độc giả được chọn

### 4.8 – VIEW: `views/borrow_view.py`
Frame "Mượn / Trả Sách" gồm 2 LabelFrame:

**LabelFrame "Tạo Phiếu Mượn":**
- Fields: Mã phiếu (tự tạo theo format PM-YYYYMMDD-XXX), Mã sách, Mã độc giả, Ngày mượn (mặc định hôm nay), Hạn trả (mặc định 14 ngày sau)
- Nút `Tạo phiếu mượn`
- Nếu sách hết (quantity = 0) → messagebox.showwarning "Sách đã hết, không thể mượn!"

**LabelFrame "Trả Sách":**
- Field: Mã phiếu mượn, Ngày trả (mặc định hôm nay)
- Nút `Xác nhận trả sách`
- Sau khi trả → hiện thông báo: nếu đúng hạn "Trả sách thành công!", nếu trễ "Trả trễ X ngày. Tiền phạt: Y,000đ"

**Bên dưới:** Treeview danh sách phiếu đang mượn: Mã phiếu | Tên sách | Tên độc giả | Ngày mượn | Hạn trả | Trạng thái

### 4.9 – CONTROLLER (3 file tương ứng)
Mỗi controller:
- Nhận View và Model làm tham số
- Kết nối sự kiện (button click) của View với logic trong Model
- Xử lý validation: kiểm tra trường bắt buộc, kiểu dữ liệu, trùng mã
- Hiển thị `messagebox.showerror` khi có lỗi, `messagebox.showinfo` khi thành công
- Làm mới Treeview sau mỗi thao tác CRUD

### 4.10 – `main.py`
```python
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
```

---

## BƯỚC 5 – VIẾT README.md

Tạo `README.md` với đầy đủ các mục:

```markdown
# 📚 Mini Library Management System

Hệ thống quản lý thư viện mini được xây dựng bằng Python, Tkinter và SQLite.

## 🛠️ Công nghệ sử dụng
- Python 3.x
- Tkinter (GUI)
- SQLite (Database)
- Kiến trúc MVC

## ⚙️ Cài đặt & Chạy ứng dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên

### Cài đặt
```bash
# Clone repository
git clone <repo-url>
cd Mini_Library_Project

# Không cần cài thêm thư viện (dùng stdlib)
```

### Chạy ứng dụng
```bash
python main.py
```

## 📁 Cấu trúc thư mục
[mô tả cấu trúc MVC]

## ✨ Chức năng chính
- Quản lý sách: Thêm, sửa, xóa, tìm kiếm
- Quản lý độc giả: Đăng ký, xem lịch sử
- Mượn/Trả: Tạo phiếu, tính phạt trễ hạn (5.000đ/ngày)

## 👤 Tác giả
[Tên sinh viên - MSSV]
```

---

## BƯỚC 6 – COMMIT THEO NHÁNH (thực hiện sau khi xong code)

Thực hiện đúng quy trình Git sau:

```bash
# --- Nhánh 1: Cấu trúc cơ bản ---
git checkout -b feature/project-setup
git add models/database.py models/__init__.py main.py requirements.txt README.md
git commit -m "feat: setup project structure and database initialization"
git checkout main
git merge feature/project-setup

# --- Nhánh 2: Quản lý sách ---
git checkout -b feature/manage-books
git add models/book_model.py views/book_view.py controllers/book_controller.py
git commit -m "feat: add book management (CRUD + search)"
git checkout main
git merge feature/manage-books

# --- Nhánh 3: Quản lý độc giả ---
git checkout -b feature/manage-readers
git add models/reader_model.py views/reader_view.py controllers/reader_controller.py
git commit -m "feat: add reader management and borrow history"
git checkout main
git merge feature/manage-readers

# --- Nhánh 4: Mượn/Trả sách ---
git checkout -b feature/borrow-ticket
git add models/borrow_model.py views/borrow_view.py controllers/borrow_controller.py
git commit -m "feat: add borrow/return management with late fee calculation"
git checkout main
git merge feature/borrow-ticket

# --- Cập nhật main_view sau khi tích hợp ---
git add views/main_view.py views/__init__.py controllers/__init__.py
git commit -m "chore: integrate all modules into main view"
```

---

## YÊU CẦU CHẤT LƯỢNG

1. **Mỗi file phải có đầy đủ code thực thi, không để placeholder**
2. **Tất cả nút bấm phải hoạt động**, không có nút nào chưa kết nối
3. **Validation đầu vào:** không để trống trường bắt buộc, số lượng phải là số nguyên ≥ 0
4. **Thông báo rõ ràng** khi: thêm thành công, sách hết, trả trễ hạn, mã bị trùng
5. **Treeview tự làm mới** sau mỗi thao tác CRUD
6. **Ứng dụng chạy được ngay** bằng lệnh `python main.py` mà không cần bước nào thêm

---

**Hãy bắt đầu từ BƯỚC 1 (Git init) và thực hiện tuần tự đến BƯỚC 6.**
