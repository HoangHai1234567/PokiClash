# Chờ Unity biên dịch xong sau khi chép .cs: đọc Editor.log từ vị trí byte đã ghi trước khi chép, chờ dòng "Reloading assemblies after"
# (hoặc lỗi biên dịch), rồi in lỗi nếu có.   py -3 -I unity_cho.py <vị trí byte> [giây tối đa] [chuỗi chờ thêm]
import os, sys, time, re

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unity_mcp as um

LOG = os.path.join(os.environ["LOCALAPPDATA"], "Unity", "Editor", "Editor.log")
pos = int(sys.argv[1])
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 300
want = sys.argv[3] if len(sys.argv) > 3 else "Reloading assemblies after"
t0 = time.time()
txt = ""
while time.time() - t0 < limit:
    with open(LOG, "rb") as f:
        f.seek(pos)
        txt = f.read().decode("utf-8", "replace")
    if want in txt or re.search(r"error CS\d+", txt):
        break
    try:
        um.state(um.open_session())  # hỏi trạng thái cũng là đánh thức Unity đang nằm nền
    except Exception:
        pass
    time.sleep(4)
errs = sorted(set(l.strip() for l in txt.splitlines() if re.search(r"error CS\d+", l)))
print("thấy '%s':" % want, want in txt, "| sau %.0f giây" % (time.time() - t0), "| lỗi biên dịch:", len(errs))
for e in errs[:20]:
    print(" ", e[:260])
for l in txt.splitlines():
    if "[Nhập dữ liệu]" in l or "Nhập dữ liệu" in l or "DataImporter" in l:
        print(" ", l[:300])
try:
    st = um.state(um.open_session())
    print("is_playing", um.find(st, "is_playing"), "| is_compiling", um.find(st, "is_compiling"))
except Exception as e:
    print("không hỏi được trạng thái:", e)
