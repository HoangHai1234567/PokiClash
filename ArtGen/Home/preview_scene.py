# Ghép thử màn Nhà ngoài Unity bằng đúng phép tính của HomeScene (CellTop, điểm neo, cỡ = ô x 96 / bề ngang chân thoi), để soi hình khớp
# lưới trước khi Play. Ra: ArtGen/Home/preview_scene_full.png (cả bản đồ thu nhỏ), preview_scene_screen.png (một màn 1080 x 1920 quanh
# Nhà chính). Chạy: py -3 -I preview_scene.py
import os, sys, json
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Home")
meta = json.load(open(os.path.join(ART, "home_art.json"), encoding="utf-8"))
cfg = json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["home"]
CW, CH = 96, 48
bm = meta["home_base"]
s = bm["grid"] * CW / bm["diamondW"]
W, H = round(bm["w"] * s), round(bm["h"] * s)
TOP = (bm["top"][0] * s, bm["top"][1] * s)
defs = {b["id"]: b for b in cfg["buildings"]}


def cell_top(gx, gy):
    return (TOP[0] + (gx - gy) * CW / 2, TOP[1] + (gx + gy) * CH / 2)


canvas = Image.open(os.path.join(ART, "home_base.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
items = []  # (depth y, img, x, y)


def put(name, cells, bottom, overlap=1.0):
    m = meta[name]
    img = Image.open(os.path.join(ART, name + ".png")).convert("RGBA")
    k = cells * CW / max(1, m["foot"]) * overlap
    img = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))), Image.LANCZOS)
    px, py = m["pivot"]
    x = bottom[0] - px * img.width
    y = bottom[1] - (1 - py) * img.height
    items.append((bottom[1], img, x, y))


n = cfg["grid"] // cfg["lot"]
start = {(l[0], l[1]) for l in cfg["startLots"]}
hills = {(l["i"], l["j"]) for l in cfg["lots"] if l["kind"] == "hill"}
forest = ["home_forest_a", "home_forest_b", "home_forest_c"]
for i in range(n):
    for j in range(n):
        if (i, j) in start or (i, j) in hills:
            continue
        put(forest[(i * 7 + j * 3) % 3], cfg["lot"], cell_top((i + 1) * cfg["lot"], (j + 1) * cfg["lot"]), 1.13)
layout = list(cfg["layout"]) + [{"b": "tree", "gx": 31, "gy": 33}, {"b": "well", "gx": 29, "gy": 34}]
for p in layout:
    d = defs[p["b"]]
    put("home_b_" + p["b"], d["size"], cell_top(p["gx"] + d["size"], p["gy"] + d["size"]))
for _, img, x, y in sorted(items, key=lambda t: t[0]):
    canvas.alpha_composite(img, (round(x), round(y)))
# ô lát thử: đường đất từ bến lên Nhà chính
dr = ImageDraw.Draw(canvas)
full = canvas.copy()
full.thumbnail((1600, 1600))
full.save(os.path.join(HERE, "preview_scene_full.png"))
m = next(p for p in cfg["layout"] if p["b"] == "main")
c = cell_top(m["gx"] + 3, m["gy"] + 3)
box = (round(c[0] - 540), round(c[1] - 1000), round(c[0] + 540), round(c[1] + 920))
canvas.crop(box).save(os.path.join(HERE, "preview_scene_screen.png"))
print("ok", W, H, "top", TOP)
