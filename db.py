import os
import json
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

# Thông tin kết nối PostgreSQL nội bộ từ VibeHost
DEFAULT_POSTGRES_URI = "postgresql://user_31f427595f2e:YwnITl-U-sILVcP7Tv0Svj9Ul4uV1gvk@vays-db-b94ecb95-postgresql-5432:5432/trathaomoc_db"

def get_database_url():
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or DEFAULT_POSTGRES_URI
    if "@:0/" in url:
        url = url.replace("@:0/", "@vays-db-b94ecb95-postgresql-5432:5432/")
    elif "@/" in url:
        url = url.replace("@/", "@vays-db-b94ecb95-postgresql-5432:5432/")
    return url

_CONNECTION_ATTEMPTED = False
_DB_AVAILABLE = False
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_ADMIN_USER = "nguyendacdanh"
DEFAULT_ADMIN_PASS = "BachPhuc@136"

def _load_local_json(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default

def _save_local_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_connection():
    global _CONNECTION_ATTEMPTED, _DB_AVAILABLE
    if _CONNECTION_ATTEMPTED and not _DB_AVAILABLE:
        return None
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(get_database_url(), cursor_factory=RealDictCursor, connect_timeout=3)
        _DB_AVAILABLE = True
        _CONNECTION_ATTEMPTED = True
        return conn
    except Exception as e:
        if not _CONNECTION_ATTEMPTED:
            logger.warning(f"Chạy offline hoặc chưa vào mạng nội bộ VibeHost ({e}). Chuyển sang lưu JSON cục bộ.")
        _DB_AVAILABLE = False
        _CONNECTION_ATTEMPTED = True
        return None

def init_db(default_content=None):
    """Tự động khởi tạo cấu trúc bảng trên PostgreSQL khi kết nối được."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # 1. Bảng lưu nội dung website (JSONB)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS site_content (
                    key VARCHAR(50) PRIMARY KEY,
                    data JSONB NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Bảng quản trị viên (Admin)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 3. Bảng cài đặt cấu hình (Settings - mua hàng online,...)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS site_settings (
                    key VARCHAR(50) PRIMARY KEY,
                    value JSONB NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 4. Bảng yêu cầu hướng dẫn & tư vấn (Inquiries / Consultations)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS consultations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(30),
                    email VARCHAR(120),
                    interest VARCHAR(100),
                    message TEXT,
                    status VARCHAR(30) DEFAULT 'Mới',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 5. Bảng đơn đặt hàng & giỏ hàng (Orders)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    order_code VARCHAR(50) UNIQUE NOT NULL,
                    customer_name VARCHAR(100) NOT NULL,
                    customer_phone VARCHAR(30) NOT NULL,
                    customer_address TEXT NOT NULL,
                    note TEXT,
                    items JSONB NOT NULL,
                    total_amount NUMERIC(15, 2) NOT NULL,
                    status VARCHAR(30) DEFAULT 'Chờ xác nhận',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Cập nhật / tạo tài khoản admin nguyendacdanh
            new_hash = generate_password_hash(DEFAULT_ADMIN_PASS)
            cur.execute("SELECT id FROM admin_users WHERE username = %s;", (DEFAULT_ADMIN_USER,))
            if cur.fetchone():
                cur.execute(
                    "UPDATE admin_users SET password_hash = %s WHERE username = %s;",
                    (new_hash, DEFAULT_ADMIN_USER)
                )
            else:
                cur.execute(
                    "INSERT INTO admin_users (username, password_hash) VALUES (%s, %s);",
                    (DEFAULT_ADMIN_USER, new_hash)
                )

            # Cài đặt mặc định cho mua hàng online: mặc định bật True hoặc False
            cur.execute("SELECT key FROM site_settings WHERE key = 'enable_online_shopping';")
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO site_settings (key, value) VALUES ('enable_online_shopping', 'false'::jsonb);"
                )

            # Seed Site Content nếu chưa có
            cur.execute("SELECT key FROM site_content WHERE key = 'content';")
            if not cur.fetchone() and default_content:
                cur.execute(
                    "INSERT INTO site_content (key, data) VALUES (%s, %s);",
                    ("content", json.dumps(default_content, ensure_ascii=False))
                )

        conn.commit()
        conn.close()
        logger.info("Đã đồng bộ cấu trúc bảng vào PostgreSQL thành công!")
        return True
    except Exception as e:
        logger.error(f"Lỗi khi init_db: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# --- CÁC HÀM CÀI ĐẶT (SETTINGS) ---

def db_get_setting(key, default=None):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT value FROM site_settings WHERE key = %s;", (key,))
                row = cur.fetchone()
                if row:
                    val = row["value"]
                    return val if not isinstance(val, str) else json.loads(val)
        except Exception as e:
            logger.error(f"Lỗi db_get_setting: {e}")
        finally:
            conn.close()
    
    settings = _load_local_json("settings.json", {})
    return settings.get(key, default)

def db_set_setting(key, value):
    settings = _load_local_json("settings.json", {})
    settings[key] = value
    _save_local_json("settings.json", settings)

    conn = get_connection()
    if not conn:
        return True
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO site_settings (key, value, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (key) DO UPDATE
                SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP;
            """, (key, json.dumps(value)))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Lỗi db_set_setting: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# --- CÁC HÀM XỬ LÝ NỘI DUNG (CMS) ---

def db_load_content():
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT data FROM site_content WHERE key = 'content';")
                row = cur.fetchone()
                if row:
                    data = row["data"]
                    return data if isinstance(data, dict) else json.loads(data)
        except Exception as e:
            logger.error(f"Lỗi db_load_content: {e}")
        finally:
            conn.close()
    return _load_local_json("content.json", {})

def db_save_content(content):
    _save_local_json("content.json", content)
    conn = get_connection()
    if not conn:
        return True
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO site_content (key, data, updated_at)
                VALUES ('content', %s, CURRENT_TIMESTAMP)
                ON CONFLICT (key) DO UPDATE
                SET data = EXCLUDED.data, updated_at = CURRENT_TIMESTAMP;
            """, (json.dumps(content, ensure_ascii=False),))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Lỗi db_save_content: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# --- CÁC HÀM XỬ LÝ ADMIN ---

def db_check_admin(username, password):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT username, password_hash FROM admin_users WHERE username = %s;", (username,))
                row = cur.fetchone()
                if row and check_password_hash(row["password_hash"], password):
                    return True
                return False
        except Exception as e:
            logger.error(f"Lỗi db_check_admin: {e}")
        finally:
            conn.close()
    
    admin_data = _load_local_json("admin.json", None)
    if not admin_data or admin_data.get("username") != DEFAULT_ADMIN_USER:
        admin_data = {
            "username": DEFAULT_ADMIN_USER,
            "password_hash": generate_password_hash(DEFAULT_ADMIN_PASS)
        }
        _save_local_json("admin.json", admin_data)
    if username == admin_data.get("username") and check_password_hash(admin_data.get("password_hash", ""), password):
        return True
    return False

# --- CÁC HÀM XỬ LÝ YÊU CẦU HƯỚNG DẪN / TƯ VẤN (INQUIRIES) ---

def db_add_consultation(name, phone, email, interest, message):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO consultations (name, phone, email, interest, message)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (name, phone, email, interest, message))
                new_id = cur.fetchone()["id"]
            conn.commit()
            return new_id
        except Exception as e:
            logger.error(f"Lỗi db_add_consultation: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    items = _load_local_json("consultations.json", [])
    new_entry = {
        "id": len(items) + 1,
        "name": name,
        "phone": phone,
        "email": email,
        "interest": interest,
        "message": message,
        "status": "Mới",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    items.insert(0, new_entry)
    _save_local_json("consultations.json", items)
    return new_entry["id"]

def db_list_consultations(limit=50):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM consultations ORDER BY created_at DESC LIMIT %s;", (limit,))
                return list(cur.fetchall())
        except Exception as e:
            logger.error(f"Lỗi db_list_consultations: {e}")
        finally:
            conn.close()
    return _load_local_json("consultations.json", [])[:limit]

# --- CÁC HÀM XỬ LÝ ĐƠN HÀNG (ORDERS) ---

def db_add_order(customer_name, customer_phone, customer_address, note, items, total_amount):
    import random
    order_code = f"BP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO orders (order_code, customer_name, customer_phone, customer_address, note, items, total_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING order_code;
                """, (order_code, customer_name, customer_phone, customer_address, note, json.dumps(items, ensure_ascii=False), total_amount))
                code = cur.fetchone()["order_code"]
            conn.commit()
            return code
        except Exception as e:
            logger.error(f"Lỗi db_add_order: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    orders = _load_local_json("orders.json", [])
    new_order = {
        "id": len(orders) + 1,
        "order_code": order_code,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "customer_address": customer_address,
        "note": note,
        "items": items,
        "total_amount": total_amount,
        "status": "Chờ xác nhận",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    orders.insert(0, new_order)
    _save_local_json("orders.json", orders)
    return order_code

def db_list_orders(limit=50):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT %s;", (limit,))
                return list(cur.fetchall())
        except Exception as e:
            logger.error(f"Lỗi db_list_orders: {e}")
        finally:
            conn.close()
    return _load_local_json("orders.json", [])[:limit]
