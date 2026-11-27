# Bản dịch tiếng Anh cho chuỗi mới của thanh hải trình đảo (ZoneHeader bản 2, 2026-11-27: ô boss giấu bóng đen, chạm báo cấp boss).
# Chỉ THÊM khoá chưa có vào Assets/Resources/Loc/en/ui.json (đọc file mới nhất ngay lúc ghi: nhiều phiên cùng thêm khoá), giữ BOM /
# xuống dòng / thứ tự sắp xếp. Chạy: py -3 -I loc_hai_trinh.py
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
UI = os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "ui.json")

ADD = {
    "Boss đảo: {0}, cấp {1}.": "Island boss: {0}, level {1}.",
    "Boss đảo cấp {0}. Tới ải cuối mới lộ diện.": "Island boss, level {0}. Reach the last stage to reveal it.",
}

raw = open(UI, "rb").read()
bom = raw.startswith(b"\xef\xbb\xbf")
t = raw.decode("utf-8-sig")
crlf = "\r\n" in t
d = json.loads(t)
was_sorted = list(d.keys()) == sorted(d.keys())
n = 0
for k, v in ADD.items():
    if k not in d:
        d[k] = v
        n += 1
if was_sorted:
    d = dict(sorted(d.items()))
out = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
if crlf:
    out = out.replace("\n", "\r\n")
with open(UI, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
    f.write(out)
print("ui.json +", n, "khoá")
