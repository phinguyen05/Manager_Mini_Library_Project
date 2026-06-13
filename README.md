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
- `models/`: Chứa các file xử lý dữ liệu và tương tác SQLite.
- `views/`: Định nghĩa giao diện đồ họa sử dụng Tkinter.
- `controllers/`: Cầu nối logic điều hướng dữ liệu từ Model sang View.
- `main.py`: Entry point khởi tạo ứng dụng.

## ✨ Chức năng chính
- **Quản lý sách**: Thêm, sửa, xóa, tìm kiếm sách trong thư viện.
- **Quản lý độc giả**: Đăng ký thông tin độc giả và xem lịch sử mượn/trả sách.
- **Mượn/Trả**: Tạo phiếu mượn (PM-YYYYMMDD-XXX) có kiểm tra số lượng sách, tính phí phạt trễ hạn khi trả sách (5.000đ/ngày).

## 👤 Tác giả
[Tên sinh viên - MSSV]
