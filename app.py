import os
from functools import wraps
from flask import (
    Flask, render_template, redirect, url_for, request, jsonify, flash, session
)
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bachphuc-tea-secret-key-2026")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin"):
            flash("Vui lòng đăng nhập để truy cập trang quản trị.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# ==================== 1. CÁC TUYẾN ĐƯỜNG DẪN WEBSITE ====================

@app.route("/")
@app.route("/trangchu")
def index():
    return render_template("index.html")

@app.route("/dongsanpham")
def dong_san_pham():
    return render_template("dongsanpham.html")

@app.route("/dongsanpham/thuonghoang")
def sp_thuong_hoang():
    return render_template("dongsanpham_thuonghoang.html")

@app.route("/dongsanpham/kimhoang")
def sp_kim_hoang():
    return render_template("dongsanpham_kimhoang.html")

@app.route("/dongsanpham/minhhoang")
def sp_minh_hoang():
    return render_template("dongsanpham_minhhoang.html")

@app.route("/tailieu")
def tai_lieu():
    return render_template("tailieu.html")

@app.route("/tailieu/tuanhoan")
def tl_tuan_hoan():
    return render_template("tailieu_tuanhoan.html")

@app.route("/tailieu/tebao")
def tl_te_bao():
    return render_template("tailieu_tebao.html")

@app.route("/tailieu/chuyenhoa")
def tl_chuyen_hoa():
    return render_template("tailieu_chuyenhoa.html")

@app.route("/suckhoe")
def suc_khoe():
    return render_template("suckhoe.html")

@app.route("/suckhoe/noicanbang")
def sk_noi_can_bang():
    return render_template("suckhoe_noicanbang.html")

@app.route("/suckhoe/tuchualanh")
def sk_tu_chua_lanh():
    return render_template("suckhoe_tuchualanh.html")

@app.route("/suckhoe/thichnghi")
def sk_thich_nghi():
    return render_template("suckhoe_thichnghi.html")

@app.route("/suckhoe/nhipsinhhoc")
def sk_nhip_sinh_hoc():
    return render_template("suckhoe_nhipsinhhoc.html")

@app.route("/thuhai")
def thu_hai():
    return render_template("thuhai.html")

@app.route("/tracuu")
def tra_cuu():
    return render_template("tracuu.html")

@app.route("/lienhe", methods=["GET", "POST"])
def lien_he():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        interest = request.form.get("interest", "").strip()
        message = request.form.get("message", "").strip()
        if name and phone:
            db.db_add_consultation(name, phone, email, interest, message)
            flash("Cảm ơn bạn! Bách Phục đã tiếp nhận yêu cầu và sẽ liên hệ sớm nhất.", "success")
        else:
            flash("Vui lòng nhập họ tên và số điện thoại.", "danger")
        return redirect(url_for("lien_he"))
    return render_template("lienhe.html")

# ==================== 2. API TIẾP NHẬN YÊU CẦU & GIỎ HÀNG ====================

@app.route("/api/consultation", methods=["POST"])
def api_consultation():
    """API lưu yêu cầu hướng dẫn sử dụng và tư vấn dòng trà vào CSDL."""
    data = request.get_json(silent=True) or request.form
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    interest = data.get("interest", "Tư vấn chung").strip()
    message = data.get("message", "").strip()

    if not name or not phone:
        return jsonify({"ok": False, "error": "Thiếu họ tên hoặc số điện thoại"}), 400

    new_id = db.db_add_consultation(name, phone, email, interest, message)
    return jsonify({"ok": True, "id": new_id, "message": "Đã ghi nhận yêu cầu thành công!"})

@app.route("/api/order", methods=["POST"])
def api_order():
    """API tạo đơn đặt hàng mới từ giỏ hàng vào PostgreSQL."""
    data = request.get_json(silent=True) or request.form
    name = data.get("customer_name", "").strip()
    phone = data.get("customer_phone", "").strip()
    address = data.get("customer_address", "").strip()
    note = data.get("note", "").strip()
    items = data.get("items", [])
    total_amount = float(data.get("total_amount", 0))

    if not name or not phone or not address:
        return jsonify({"ok": False, "error": "Vui lòng nhập đầy đủ thông tin giao hàng"}), 400

    order_code = db.db_add_order(name, phone, address, note, items, total_amount)
    if order_code:
        return jsonify({"ok": True, "order_code": order_code, "message": "Đặt hàng thành công!"})
    return jsonify({"ok": False, "error": "Lỗi khi lưu đơn hàng vào CSDL"}), 500

# ==================== 3. PANEL QUẢN TRỊ ADMIN ====================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        # Kiểm tra qua DB hoặc tài khoản mặc định
        if db.db_check_admin(username, password) or (username == "admin" and password == "123admin"):
            session["admin"] = True
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("admin_index"))
        flash("Sai tài khoản hoặc mật khẩu.", "danger")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("admin_login"))

@app.route("/admin")
@login_required
def admin_index():
    orders = db.db_list_orders(limit=10)
    consultations = db.db_list_consultations(limit=10)
    return render_template("admin/index.html", orders=orders, consultations=consultations)

@app.route("/admin/orders")
@login_required
def admin_orders():
    orders = db.db_list_orders(limit=50)
    return render_template("admin/orders.html", orders=orders)

@app.route("/admin/consultations")
@login_required
def admin_consultations():
    consultations = db.db_list_consultations(limit=50)
    return render_template("admin/consultations.html", consultations=consultations)

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("index"))

# Tự động khởi tạo database khi app được tải
try:
    db.init_db()
except Exception as e:
    print(f"init_db notice: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
