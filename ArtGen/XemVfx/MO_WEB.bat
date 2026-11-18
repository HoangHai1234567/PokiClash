@echo off
rem Trang so sánh hiệu ứng từng tướng (chỉ xem trên máy). Dựng lại: py -3 -I xay_trang.py
cd /d "%~dp0"
if not exist "data.json" py -3 -I xay_trang.py
start "" http://localhost:8768/index.html
py -3 -m http.server 8768 --bind 127.0.0.1
