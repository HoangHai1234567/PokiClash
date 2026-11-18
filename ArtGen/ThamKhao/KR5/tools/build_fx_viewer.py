# Dựng dữ liệu cho trang xem hiệu ứng Kingdom Rush 5 (fx_viewer/)
#   py -3 -I tools/build_fx_viewer.py <bản rút Kingdom Rush 5, vd. D:/Ripper/KingdomRush5>
# Ghi vào ../fx_viewer (data.json, sheets/, exo/): không commit, xem .gitignore.
# Mã chính ở fx_build.py; file này mỏng để tiến trình con (multiprocessing) không chạy lại phần nạp dữ liệu.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    import fx_build
    fx_build.main()
