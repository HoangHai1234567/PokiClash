@echo off
rem Chay ban web thu PokiClash. Lan dau tu cai thu vien, roi mo trinh duyet.
cd /d "%~dp0"
if not exist node_modules (
  echo Dang cai thu vien lan dau...
  call npm install
)
call npm run dev -- --open
pause
