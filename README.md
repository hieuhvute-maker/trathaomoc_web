# Trà Thảo Mộc Bách Phục - Python Flask Web App

Website giới thiệu thương hiệu và sản phẩm **Trà Thảo Mộc Bách Phục**, được nhân bản (clone) với độ trung thực cao từ phiên bản Google Sites gốc (`https://www.trathaomocbachphuc.vn/`).

## 🌿 Điểm nổi bật
- **Kiến trúc:** Python 3 + Flask.
- **Tương thích:** Đầy đủ 18 tuyến đường dẫn (routes), chuyển đổi ngôn ngữ tức thì **VI (Tiếng Việt)** và **EN (English)**.
- **Tài nguyên cục bộ:** Tải và phục vụ toàn bộ hình ảnh sản phẩm, hình ảnh thu hái và 6 loại nấm Linh Chi kinh điển ngay tại thư mục `static/images/`.
- **Triển khai linh hoạt:** Tích hợp sẵn `Dockerfile` và `Procfile`, sẵn sàng đưa lên GitHub và triển khai lên **VibeHost** / Cloud Run / Railway / Docker.

---

## 📂 Cấu trúc thư mục

```
trathaomoc_web/
├── app.py                 # File khởi chạy chính của ứng dụng Flask
├── requirements.txt       # Danh sách thư viện Python (Flask, Gunicorn)
├── Dockerfile             # Cấu hình container Docker
├── Procfile               # Cấu hình Web Process cho các nền tảng đám mây
├── .gitignore             # Danh sách loại trừ khi đẩy lên Git
├── static/
│   └── images/            # Toàn bộ hình ảnh sản phẩm, tư liệu thu hái, nấm linh chi
└── templates/             # 18 templates HTML tương ứng với các trang
    ├── index.html         # Trang chủ (/)
    ├── dongsanpham.html   # Danh mục sản phẩm (/dongsanpham)
    ├── dongsanpham_thuonghoang.html # Chi tiết Thượng Hoàng
    ├── dongsanpham_kimhoang.html    # Chi tiết Kim Hoàng
    ├── dongsanpham_minhhoang.html   # Chi tiết Minh Hoàng
    ├── tailieu.html       # Tài liệu chuyên khảo (/tailieu)
    ├── tailieu_*.html     # Chuyên khảo Tuần hoàn, Tế bào, Chuyển hóa
    ├── suckhoe.html       # Cơ chế tự chữa lành (/suckhoe)
    ├── suckhoe_*.html     # 4 bài viết khoa học dưỡng sinh
    ├── thuhai.html        # Nhật ký thu hái đại ngàn (/thuhai)
    ├── tracuu.html        # Cổng tra cứu xác thực hộp trà (/tracuu)
    └── lienhe.html        # Thông tin liên hệ & tư vấn Zalo (/lienhe)
```

---

## 🚀 Hướng dẫn chạy thử trên máy (Local)

1. Mở terminal tại thư mục này:
   ```bash
   cd trathaomoc_web
   ```

2. Cài đặt môi trường ảo và thư viện:
   ```bash
   python -m venv venv
   # Kích hoạt trên Windows:
   .\venv\Scripts\activate
   # Cài đặt thư viện:
   pip install -r requirements.txt
   ```

3. Khởi chạy ứng dụng:
   ```bash
   python app.py
   ```
   Mở trình duyệt truy cập: `http://localhost:5000`

---

## 📤 Hướng dẫn đưa lên GitHub (Bước 2)

Khởi tạo git và đẩy lên repository của bạn:
```bash
git init
git add .
git commit -m "feat: clone complete trathaomocbachphuc website to python flask"
git branch -M main
git remote add origin https://github.com/<tai-khoan-cua-ban>/<ten-repo>.git
git push -u origin main
```
