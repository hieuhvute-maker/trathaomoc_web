# HƯỚNG DẪN KẾT NỐI VÀ LÀM VIỆC DỰ ÁN TRÀ THẢO MỘC BÁCH PHỤC
## QUY TRÌNH 100% VIBE CODING VỚI GOOGLE ANTIGRAVITY & VIBEHOST

---

## 1. TỔNG QUAN HỆ THỐNG DỰ ÁN

Website **Trà Thảo Mộc Bách Phục** được phát triển và vận hành theo triết lý **100% Vibe Coding** — nghĩa là toàn bộ thành viên trong nhóm không cần phải tự tay gõ từng dòng mã nguồn phức tạp, mà sẽ làm việc trực tiếp với **Google Antigravity AI Agent** bằng ngôn ngữ tự nhiên để hiện thực hóa ý tưởng, tính năng và giao diện.

### Thông tin hạ tầng kỹ thuật:
- **Ngôn ngữ & Framework**: Python 3.11 + Flask Framework
- **Giao diện (Frontend)**: Tinh gọn, chuẩn nhận diện Bách Phục, hỗ trợ song ngữ (Tiếng Việt & English), tối ưu hiển thị máy tính và điện thoại.
- **Cơ sở dữ liệu**: **PostgreSQL 16** (quản lý trên nền tảng VibeHost, có tích hợp cơ chế Offline JSON Fallback để test máy nội bộ mượt mà).
- **VibeHost Project ID**: `cmwljifwn0j3u0i5fzrkqiyeo`
- **Kho mã nguồn (GitHub)**: [https://github.com/hieuhvute-maker/trathaomoc_web](https://github.com/hieuhvute-maker/trathaomoc_web)
- **Thư mục dự án cục bộ**: `C:\Users\223041607\.gemini\antigravity\scratch\trathaomoc_web`
- **Tên miền hoạt động**:
  - Tên miền chính thức: [https://trathaomocbachphuc.vn](https://trathaomocbachphuc.vn)
  - Tên miền triển khai trực tiếp VibeHost: [https://trathaomoc-web.n3.tinhgon.xyz](https://trathaomoc-web.n3.tinhgon.xyz)
- **Cổng Quản trị (Admin Panel)**: `/admin` (hoặc `/admin/login`)
  - **Tài khoản**: `nguyendacdanh`
  - **Mật khẩu**: `BachPhuc@136`

---

## 2. HƯỚNG DẪN THÀNH VIÊN MỚI THIẾT LẬP KẾT NỐI (SETUP)

Mỗi thành viên trong team khi tham gia phát triển chỉ cần thực hiện 3 bước đơn giản:

### Bước 1: Kéo mã nguồn về máy tính
Mở Terminal hoặc PowerShell trên máy tính và chạy lệnh:
```bash
git clone https://github.com/hieuhvute-maker/trathaomoc_web.git
cd trathaomoc_web
```

### Bước 2: Cài đặt phụ thuộc (Dependencies)
```bash
pip install flask psycopg2-binary werkzeug requests
```
*(Nếu máy chưa có thư viện psycopg2, hệ thống code đã tích hợp sẵn cơ chế Fallback sang file JSON cục bộ trong thư mục `data/` nên bạn vẫn có thể chạy web bình thường).*

### Bước 3: Cấu hình MCP VibeHost vào Antigravity
Để Antigravity có quyền tự động kiểm tra trạng thái hosting, tự động redeploy khi xong code, hãy thêm cấu hình sau vào file cấu hình MCP của Antigravity (`~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "vibehost": {
      "serverUrl": "https://v2.tinhgon.xyz/api/agent/mcp",
      "headers": {
        "Authorization": "Bearer <KHOA_API_VIBEHOST_CUA_BAN>"
      }
    }
  }
}
```
*(Khóa API lấy trực tiếp tại mục **Kết nối AI Agent** trên Dashboard VibeHost).*

---

## 3. CƠ CHẾ LÀM VIỆC "100% VIBE CODING" VỚI ANTIGRAVITY

Khác với lập trình truyền thống, làm việc theo phương pháp **Vibe Coding** với Antigravity gồm chu trình 4 bước khép kín:

```
[1. Ý tưởng / Yêu cầu] ➡️ [2. Antigravity phân tích & viết code] ➡️ [3. Kiểm thử tự động] ➡️ [4. Deploy tự động lên Cloud]
```

### Chi tiết từng bước:

### Bước 1: Ra đề bài (Prompting) cho Antigravity
Khi muốn thêm trang, đổi màu sắc, cập nhật giá hoặc bổ sung chức năng, bạn chỉ cần mở Antigravity và chat bằng Tiếng Việt một cách tự nhiên.
> **Mẹo ra lệnh chuẩn**: Nêu rõ mục tiêu, trang cần sửa, luồng trải nghiệm khách hàng và điều kiện hoàn thành.

### Bước 2: Antigravity tự động thực hiện
- Tự đọc cấu trúc file (`app.py`, `db.py`, thư mục `templates/`, `static/`).
- Tự thêm hoặc chỉnh sửa code, bổ sung bảng database nếu cần.
- Luôn giữ vững tính toàn vẹn của mã nguồn hiện có.

### Bước 3: Tự động kiểm thử (Verification)
Antigravity sẽ tự động chạy thử app, kiểm tra logic form, kiểm tra giao diện để bảo đảm không phát sinh lỗi trước khi đẩy lên production.

### Bước 4: Tự động đồng bộ & Triển khai (Deploy)
- Antigravity tự commit vào Git và push lên nhánh `main` của GitHub: `git push origin main`.
- Tự động gọi tool MCP VibeHost: `redeploy_project(projectId="cmwljifwn0j3u0i5fzrkqiyeo")`.
- Tự gọi `wait_for_job` theo dõi tiến trình build cho đến khi đạt 100% (`state: succeeded`) và website hoạt động trở lại.

---

## 4. CÁC TÍNH NĂNG ĐẶC BIỆT ĐANG CÓ TRÊN WEBSITE

1. **Hệ Thống Song Ngữ Toàn Diện (Bilingual VI / EN)**:
   - Khách hàng bấm chuyển đổi `VI • Tiếng Việt` hoặc `EN • English` ở góc trên cùng bên phải.
   - Toàn bộ nội dung tiêu đề, mô tả, nút bấm, thành phần nấm linh chi sẽ chuyển đổi mượt mà và lưu lại tùy chọn trong trình duyệt.

2. **Cơ Chế Bật/Tắt Mua Hàng Online Trong Admin**:
   - Truy cập `/admin` > Khối **"Cài đặt Chức Năng Mua Hàng Online"**.
   - **Khi BẬT**: Nút "🛒 Thêm vào giỏ hàng" và Icon Giỏ Hàng góc trên bên phải sẽ hiển thị. Khách hàng có thể đặt hàng và gửi về database.
   - **Khi TẮT**: Toàn bộ nút giỏ hàng và icon giỏ hàng trên tất cả các trang đều ẩn hoàn toàn (invisible), trang web quay về trạng thái giới thiệu văn hóa trà & tư vấn kết nối mộc bản.

3. **Cổng Tra Cứu Mộc Bản 1-1 (`/tracuu`)**:
   - Quét mã QR hoặc nhập mã hộp trà + mã PIN 4 số bí mật.
   - Kết nối trực tiếp cơ sở dữ liệu kiểm nghiệm (Polysaccharide 0.967%, vùng thu hái, thợ rừng, ngày đóng gói).

4. **Biểu Mẫu Nhận Tư Vấn & Đặt Hàng**:
   - Yêu cầu hướng dẫn & liên hệ từ khách hàng được lưu tức thì vào bảng `consultations` và `orders` trong PostgreSQL.

---

## 5. MẪU CÂU LỆNH (PROMPT TEMPLATES) ĐỂ TEAM DÙNG HÀNG NGÀY

Các thành viên chỉ cần sao chép các mẫu prompt bên dưới và dán vào Antigravity:

### Mẫu 1: Thêm một sản phẩm mới
> *"Antigravity ơi, mình muốn thêm một dòng trà mới tên là 'Bách Phục Hoàng Cúc'. Hãy thêm route trong app.py, tạo trang giao diện chi tiết dựa trên mẫu dongsanpham_thuonghoang.html, cập nhật vào menu dropdown 'Sản Phẩm' và bổ sung nút thêm giỏ hàng. Sau đó test thử và deploy lên VibeHost giúp mình."*

### Mẫu 2: Thay đổi thông tin liên hệ / Hotline
> *"Hãy cập nhật số hotline tư vấn từ 0796674679 thành [SỐ_MỚI] trên toàn bộ các trang giao diện và footer, đồng thời cập nhật link liên hệ Zalo tương ứng. Làm xong hãy push lên GitHub và deploy lên VibeHost."*

### Mẫu 3: Bổ sung phương thức thanh toán mới
> *"Trong trang giỏ hàng (/giohang), hãy thêm phương thức thanh toán mới là 'Thanh toán qua ví MoMo / VNPAY QR' và ghi nhận thông tin này vào cơ sở dữ liệu khi khách đặt hàng."*

### Mẫu 4: Kiểm tra trạng thái hệ thống và Database
> *"Hãy kiểm tra xem kết nối PostgreSQL trên VibeHost có đang hoạt động ổn định không, và thống kê cho mình xem hôm nay có bao nhiêu đơn hàng và bao nhiêu yêu cầu tư vấn mới."*

---

## 6. LƯU Ý KỸ THUẬT QUAN TRỌNG CHO TEAM

1. **Không can thiệp sửa trực tiếp trên server VibeHost**:
   - Luôn thực hiện thay đổi thông qua Antigravity trên repo Git. Mỗi khi commit được push lên nhánh `main`, hệ thống CI/CD của VibeHost sẽ tự động kéo về và biên dịch lại trong vòng 30-45 giây.
2. **Cơ sở dữ liệu PostgreSQL**:
   - Địa chỉ host nội bộ VibeHost: `vays-db-b94ecb95-postgresql-5432:5432`
   - Tên database: `trathaomoc_db`
   - Module `db.py` đã viết sẵn cơ chế tự động khởi tạo bảng (`CREATE TABLE IF NOT EXISTS`) và tự động seed dữ liệu ban đầu, không cần phải chạy file migration thủ công.
3. **Bảo mật tài khoản Admin**:
   - Mật khẩu admin đã được mã hóa bảo mật chuẩn `scrypt` trong cơ sở dữ liệu. Nếu muốn đổi mật khẩu trong tương lai, chỉ cần ra lệnh cho Antigravity: *"Đổi mật khẩu admin thành [Mật_Khẩu_Mới]"*, Antigravity sẽ tự băm hash và cập nhật an toàn.

---
*Tài liệu được khởi tạo tự động bởi Antigravity AI Agent — Đồng hành cùng Đội ngũ Trà Thảo Mộc Bách Phục.*
