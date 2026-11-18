@echo off
rem Trang xem hiệu ứng Kingdom Rush 5 (chỉ chạy trên máy, không đăng công khai)
cd /d "%~dp0"
if not exist "fx_viewer\data.json" (
  echo Chua co du lieu. Chay: py -3 -I tools\build_fx_viewer.py D:\Ripper\KingdomRush5
  pause
  exit /b 1
)
start "" http://localhost:8767/fx_viewer/index.html
py -3 -m http.server 8767 --bind 127.0.0.1
