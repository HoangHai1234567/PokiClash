# Đưa hình Nhà vào Unity: tách nền (trắng hoặc xanh phẳng) bằng tô loang từ mép, cắt sát, đo góc dưới chân thoi và bề ngang chân thoi,
# gọt thoi cỏ có viền dưới chân công trình (foot_strip.py),
# ghi Assets/03 Art/Home/<tên>.png và home_art.json (pivot theo tỉ lệ ảnh, footprint px để code đổi ra ô lưới).
# Nguồn: ArtGen/Home/base (nền, khối rừng), ArtGen/Home/buildings (tờ công trình, mây). Chạy: py -3 -I import_home.py
import os, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from foot_strip import measure_diamond, strip_foot  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Home")
os.makedirs(OUT, exist_ok=True)
B = os.path.join(HERE, "buildings")
KEY = (255, 0, 255)


def cut_region(im, box=None, bg="white", thresh=45):
    """Tách nền của một vùng ảnh: trả RGBA cắt sát."""
    src = im.crop(box) if box else im.copy()
    src = src.convert("RGB")
    w, h = src.size
    work = src.copy()
    seeds = [(x, 0) for x in range(0, w, 16)] + [(x, h - 1) for x in range(0, w, 16)] + [(0, y) for y in range(0, h, 16)] + [(w - 1, y) for y in range(0, h, 16)]
    for xy in seeds:
        p = work.getpixel(xy)
        if p == KEY:
            continue
        ok = sum(p) > 690 if bg == "white" else (p[2] > 150 and p[0] < 120)
        if ok:
            ImageDraw.floodfill(work, xy, KEY, thresh=thresh)
    out = Image.new("RGBA", (w, h))
    wp, sp, op = work.load(), src.load(), out.load()
    for y in range(h):
        for x in range(w):
            if wp[x, y] != KEY:
                op[x, y] = sp[x, y] + (255,)
    bb = out.getbbox()
    return out.crop(bb) if bb else out


def footprint(img):
    """Góc dưới chân thoi (điểm đặc thấp nhất) và bề ngang chân thoi (điểm trái nhất, phải nhất ở 35% dưới)."""
    a = img.split()[3].load()
    w, h = img.size
    bottom = max(y for y in range(h) for x in range(0, w, 2) if a[x, y] > 0)
    xs = [x for x in range(w) if a[x, bottom] > 0]
    bx = sum(xs) / len(xs)
    lo = [x for y in range(int(h * 0.65), h) for x in range(w) if a[x, y] > 0]
    return bx, bottom, max(lo) - min(lo)


meta = {}


# công trình tự có nền riêng trên cả chân thoi (luống đất, vườn rào, sàn gỗ, núi đá): không gọt
NO_STRIP = {"home_b_field", "home_b_orchard", "home_b_sawmill", "home_b_mine"}


def save(name, img, cells=None, kind="object"):
    w, h = img.size
    m = {"w": w, "h": h, "kind": kind}
    if cells:
        bx, by, fw = footprint(img)  # đo neo trên thoi trước khi gọt
        m.update({"pivot": [round(bx / w, 4), round(1 - (by + 1) / h, 4)], "foot": fw, "cells": cells})
        if kind == "object" and name not in NO_STRIP:
            # bỏ thoi cỏ có viền dưới chân cho công trình hoà vào đất (người dùng dặn 2026-11-18); khung ảnh giữ nguyên
            dx, _, dfw = measure_diamond(img, by)
            img = strip_foot(img, dx, by, dfw)
    img.save(os.path.join(OUT, name + ".png"))
    meta[name] = m
    print(name, w, h, m.get("foot"), m.get("pivot"))


# tờ 3 chỗ (1344 x 752): chia ba cột đều; tờ 4 chỗ: bốn cột
def sheet(fn, names, cells):
    im = Image.open(os.path.join(B, fn))
    w, h = im.size
    n = len(names)
    for k, nm in enumerate(names):
        box = (int(k * w / n), 0, int((k + 1) * w / n), h)
        save(nm, cut_region(im, box), cells)


sheet("sheet_A.png", ["home_b_field", "home_b_orchard", "home_b_sawmill"], 4)
sheet("sheet_B.png", ["home_b_storage", "home_b_pond", "home_b_forge"], 4)
sheet("sheet_C.png", ["home_b_kitchen", "home_b_hotspring", "home_b_waterwheel"], 4)
sheet("sheet_D.png", ["home_b_well", "home_b_tree", "home_b_bench", "home_b_swing"], 2)
save("home_b_main", cut_region(Image.open(os.path.join(B, "main.png"))), 6)
save("home_b_mine", cut_region(Image.open(os.path.join(B, "mine.png"))), 6)
for k in "ABC":
    save("home_forest_" + k.lower(), cut_region(Image.open(os.path.join(HERE, "base", f"forest_lot_{k}.png"))), 8, "forest")
# mây: nền xanh phẳng, ba mảng (trên trái, trên phải, dưới giữa)
cl = Image.open(os.path.join(B, "clouds.png"))
cw, ch = cl.size
for k, box in enumerate([(0, 0, cw // 2, ch // 2), (cw // 2, 0, cw, ch // 2), (0, ch // 2, cw, ch)]):
    save(f"home_cloud_{k + 1}", cut_region(cl, box, bg="blue", thresh=60), None, "cloud")
# nền: kéo ngang cho thoi đúng 2:1 (đo trên base_dao_nen_1: mũi trái (2,336), phải (1338,334), góc dưới (678,700))
base = Image.open(os.path.join(HERE, "base", "base_dao_nen_3.png")).convert("RGBA")
LEFT, RIGHT, BOTTOM = (2, 336), (1338, 334), (678, 700)
half_w = (RIGHT[0] - LEFT[0]) / 2
half_h = BOTTOM[1] - (LEFT[1] + RIGHT[1]) / 2
sx = (2 * half_h) / half_w  # đưa tỉ lệ thoi về 2:1
nb = base.resize((round(base.width * sx), base.height), Image.LANCZOS)
nb.save(os.path.join(OUT, "home_base.png"))
top = ((LEFT[0] + RIGHT[0] - BOTTOM[0]) * sx, LEFT[1] + RIGHT[1] - BOTTOM[1])
meta["home_base"] = {"w": nb.width, "h": nb.height, "kind": "base", "top": [round(top[0], 2), round(top[1], 2)],
                     "diamondW": round((RIGHT[0] - LEFT[0]) * sx, 2), "grid": 48, "stretchX": round(sx, 4)}
print("home_base", nb.size, meta["home_base"])
json.dump(meta, open(os.path.join(OUT, "home_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(meta))
