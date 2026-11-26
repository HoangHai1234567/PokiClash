# Soi clip sl_pull của Lão Mực có bám núm cần không: chép project AtomSpine của Lão Mực sang thư mục tạm, thêm một đĩa đỏ (núm cần,
# đúng cỡ trong bố cục lều) chạy theo đường núm của clip pull của máy (atom/duong_num.json), vẽ sau tay; dựng tờ khung 30 khung/giây.
# Ra: ../xem/keo_can_to.png. Chỉ để xem, không sửa project nào. Chạy: py -3 -I xem_keo.py
import json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MQ = os.path.abspath(os.path.join(HERE, ".."))
DEALER = os.path.abspath(os.path.join(MQ, "..", "dealer", "atom"))
TMP = os.path.join(os.environ.get("TEMP", "C:/Temp"), "may_qua_xem_keo")
sys.path.insert(0, HERE)
from atom_cli import CLI, TSX, ATOMSPINE  # noqa: E402
BC = json.load(open(os.path.join(MQ, "bo_cuc.json"), encoding="utf-8"))
NUM = json.load(open(os.path.join(MQ, "atom", "duong_num.json")))
m, d = BC["may"], BC["dealer"]
R = round(64.25 * m["scale"] / d["scale"])

def to_dealer(x, y):
    sx, sy = m["x"] + m["scale"] * x, m["y"] - m["scale"] * y
    return ((sx - d["x"]) / d["scale"], (d["y"] - sy) / d["scale"])

if os.path.isdir(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)
shutil.copy(os.path.join(DEALER, "atomspine.json"), TMP)
shutil.copytree(os.path.join(DEALER, "images"), os.path.join(TMP, "images"))
im = Image.new("RGBA", (2 * R + 4, 2 * R + 4), (0, 0, 0, 0))
ImageDraw.Draw(im).ellipse([2, 2, 2 * R + 2, 2 * R + 2], fill=(214, 60, 48, 255))
im.save(os.path.join(TMP, "images", "xem_num.png"))
pts = [(t, *to_dealer(x, y)) for t, x, y in NUM["pull"]]
ops = ["bone.add xem_num_b parent=root x=0 y=0", "image.add xem_num path=images/xem_num.png", "slot.add xem_num bone=xem_num_b att=xem_num",
       "slot.order xem_num to=before:tay_trai",
       "key sl_pull xem_num_b.translate " + " ".join(f"{t:.4f}:{x:.1f},{y:.1f}" for t, x, y in pts)]
open(os.path.join(TMP, "xem.ops"), "w", encoding="utf-8").write("\n".join(ops) + "\n")
r = subprocess.run(CLI + ["do", "-f", os.path.join(TMP, "xem.ops"), "-p", TMP], capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout + r.stderr).strip()[-200:])
BOX = (-560, 300, 560, 1560)
r = subprocess.run(TSX + [os.path.join(HERE, "khung.mts"), TMP, TMP, "30", ",".join(map(str, BOX)), "280", "315", "12", "sl_pull", "EFE5D2"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, ATOMSPINE_DIR=ATOMSPINE))
print((r.stdout + r.stderr).strip()[-300:])
os.makedirs(os.path.join(MQ, "xem"), exist_ok=True)
Image.open(os.path.join(TMP, "sl_pull_sheet.png")).convert("RGB").save(os.path.join(MQ, "xem", "keo_can_to.png"))
