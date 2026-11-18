import json
import os
import tempfile
import threading
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
DB_FILE = os.path.join(DATA_DIR, "db.json")

STATUSES = {
    "moi": "Mới",
    "dang_xu_ly": "Đang xử lý",
    "da_xu_ly": "Đã xử lý",
}

ORDER_STATUSES = {
    "cho_xac_nhan": "Chờ xác nhận",
    "dang_giao": "Đang giao",
    "hoan_thanh": "Hoàn thành",
    "huy": "Đã hủy",
}

_lock = threading.Lock()


def _read():
    if not os.path.exists(DB_FILE):
        return {"next_id": 1, "requests": [], "next_order_id": 1, "orders": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("next_order_id", 1)
    data.setdefault("orders", [])
    return data


def _write(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, DB_FILE)


def add_request(name, phone, dong_tra, loi_nhan):
    with _lock:
        data = _read()
        req = {
            "id": data["next_id"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "phone": phone,
            "dong_tra": dong_tra,
            "loi_nhan": loi_nhan,
            "status": "moi",
            "ghi_chu": "",
        }
        data["requests"].append(req)
        data["next_id"] += 1
        _write(data)
        return req


def list_requests(status=None):
    with _lock:
        items = _read()["requests"]
    if status:
        items = [r for r in items if r["status"] == status]
    return sorted(items, key=lambda r: r["id"], reverse=True)


def update_request(req_id, status, ghi_chu):
    with _lock:
        data = _read()
        for req in data["requests"]:
            if req["id"] == req_id:
                req["status"] = status
                req["ghi_chu"] = ghi_chu
                _write(data)
                return True
    return False


def delete_request(req_id):
    with _lock:
        data = _read()
        before = len(data["requests"])
        data["requests"] = [r for r in data["requests"] if r["id"] != req_id]
        if len(data["requests"]) != before:
            _write(data)
            return True
    return False


def add_order(customer, items, tong_tien, co_gia_chua_cong_bo):
    with _lock:
        data = _read()
        order = {
            "id": data["next_order_id"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": customer,
            "items": items,
            "tong_tien": tong_tien,
            "co_gia_chua_cong_bo": co_gia_chua_cong_bo,
            "status": "cho_xac_nhan",
            "ghi_chu": "",
        }
        data["orders"].append(order)
        data["next_order_id"] += 1
        _write(data)
        return order


def list_orders(status=None):
    with _lock:
        items = _read()["orders"]
    if status:
        items = [o for o in items if o["status"] == status]
    return sorted(items, key=lambda o: o["id"], reverse=True)


def update_order(order_id, status, ghi_chu):
    with _lock:
        data = _read()
        for order in data["orders"]:
            if order["id"] == order_id:
                order["status"] = status
                order["ghi_chu"] = ghi_chu
                _write(data)
                return True
    return False
