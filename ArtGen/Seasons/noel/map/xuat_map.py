# Xuất bản tuyết phủ màn Nhà / đảo Casino vào game: out/noel/<tên>.png (tach_map.py) → Assets/03 Art/Seasons/Resources/Seasons/noel/map/.
# SeasonSkin nạp theo tên texture gốc, đòi đúng cỡ texture gốc: script kiểm cỡ từng ảnh với ảnh gốc trước khi chép.
# py -3 -I xuat_map.py
import json, os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ART = os.path.join(PROJ, "Assets", "03 Art")
SRC = os.path.join(HERE, "out", "noel")
DST = os.path.join(ART, "Seasons", "Resources", "Seasons", "noel", "map")
sys.stdout.reconfigure(encoding="utf-8")

# tên texture gốc → đường ảnh gốc (từ các tờ của dung_to.py)
orig = {}
for f in os.listdir(os.path.join(HERE, "to")):
    if f.endswith(".json"):
        for it in json.load(open(os.path.join(HERE, "to", f), encoding="utf-8"))["items"]:
            orig[os.path.splitext(os.path.basename(it["src"]))[0]] = os.path.join(ART, it["src"])
# viền cỏ ô lát (tuyet_o_lat.py)
for k in ("lip", "cor"):
    for i in range(4):
        orig[f"{k}_grass_{i}"] = os.path.join(ART, "Home", "tiles", f"{k}_grass_{i}.png")
os.makedirs(DST, exist_ok=True)
n, bad = 0, 0
for f in sorted(os.listdir(SRC)):
    name = os.path.splitext(f)[0]
    if name not in orig:
        print("bỏ (không rõ ảnh gốc):", f)
        continue
    a, b = Image.open(os.path.join(SRC, f)).size, Image.open(orig[name]).size
    if a != b:
        print(f"LỆCH CỠ {f}: {a} khác ảnh gốc {b}")
        bad += 1
        continue
    shutil.copyfile(os.path.join(SRC, f), os.path.join(DST, f))
    n += 1
print(f"đã chép {n} ảnh vào {DST}" + (f", {bad} ảnh lệch cỡ" if bad else ""))
