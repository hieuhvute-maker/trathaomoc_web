import os
import sys

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

client = app.test_client()

routes = [
    '/',
    '/trangchu',
    '/dongsanpham',
    '/dongsanpham/thuonghoang',
    '/dongsanpham/kimhoang',
    '/dongsanpham/minhhoang',
    '/tailieu',
    '/tailieu/tuanhoan',
    '/tailieu/tebao',
    '/tailieu/chuyenhoa',
    '/suckhoe',
    '/suckhoe/noicanbang',
    '/suckhoe/tuchualanh',
    '/suckhoe/thichnghi',
    '/suckhoe/nhipsinhhoc',
    '/thuhai',
    '/tracuu',
    '/lienhe'
]

print("Testing all routes...")
all_ok = True
for r in routes:
    res = client.get(r)
    status = res.status_code
    length = len(res.data)
    ok = (status == 200)
    if not ok:
        all_ok = False
    print(f"Route: {r:<28} | Status: {status} | Bytes: {length}")

if all_ok:
    print("\n>>> ALL 18 ROUTES RETURNED HTTP 200 OK! <<<")
else:
    print("\n>>> SOME ROUTES RETURNED ERRORS! <<<")
