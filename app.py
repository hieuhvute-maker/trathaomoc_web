import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bachphuc-tea-secret-key-2026")

# 1. Trang chủ
@app.route("/")
@app.route("/trangchu")
def index():
    return render_template("index.html")

# 2. Dòng sản phẩm
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

# 3. Tài liệu chuyên khảo
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

# 4. Cơ chế tự chữa lành & Sức khỏe
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

# 5. Thu hái đại ngàn
@app.route("/thuhai")
def thu_hai():
    return render_template("thuhai.html")

# 6. Tra cứu & Bảo chứng 1-to-1
@app.route("/tracuu")
def tra_cuu():
    return render_template("tracuu.html")

# 7. Liên hệ & Tư vấn
@app.route("/lienhe")
def lien_he():
    return render_template("lienhe.html")

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
