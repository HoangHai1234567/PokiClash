# Cắt 15 món rời ở ba tờ cây (5 chỗ mỗi tờ, nền trắng), gộp vào một atlas để Unity vẽ chung một lượt:
# Assets/03 Art/Baked/Home/home_trees.png + home_trees.json (tên, khung x y w h tính từ góc trên trái, pivot ở gốc chân, bề ngang chân thoi cỏ,
# nhóm: tall / special / palm / small). Bỏ nền thoi cỏ có viền dưới chân (strip_foot) cho cây hoà vào đất. Chạy: py -3 -I pack_trees.py
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from foot_strip import measure_diamond, strip_foot  # noqa: E402
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Home")  # Baked: ArtImporter không ép về một sprite
KEY = (255, 0, 255)
SHEETS = ["tree_sheet_1.png", "tree_sheet_2.png", "tree_sheet_3_nobase.png"]
NAMES = [
    [("pine", "tall"), ("oak", "tall"), ("cypress", "tall"), ("twin", "tall"), ("pine_young", "tall")],
    [("blossom", "special"), ("birch", "tall"), ("old", "special"), ("palm", "palm"), ("round", "tall")],
    [("bush", "small"), ("fern", "small"), ("rock", "small"), ("stump", "small"), ("log", "small")],
]


def cut(src, box, keep):
    reg = src.crop(box).convert("RGB")
    w, h = reg.size
    work = reg.copy()
    for xy in [(x, 0) for x in range(0, w, 12)] + [(x, h - 1) for x in range(0, w, 12)] + [(0, y) for y in range(0, h, 12)] + [(w - 1, y) for y in range(0, h, 12)]:
        if work.getpixel(xy) != KEY and sum(work.getpixel(xy)) > 690:
            ImageDraw.floodfill(work, xy, KEY, thresh=45)
    out = Image.new("RGBA", (w, h))
    wp, sp, op = work.load(), reg.load(), out.load()
    for y in range(h):
        for x in range(w):
            if wp[x, y] != KEY:
                op[x, y] = sp[x, y] + (255,)
    # vùng cắt rộng hơn cột để không xén tán: chỉ giữ các khối liền có giữa nằm trong cột (bỏ mẩu của món bên cạnh)
    lo, hi = keep
    seen = set()
    for y in range(h):
        for x in range(w):
            if op[x, y][3] == 0 or (x, y) in seen:
                continue
            comp, st = [], [(x, y)]
            seen.add((x, y))
            while st:
                c = st.pop()
                comp.append(c)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (c[0] + dx, c[1] + dy)
                    if 0 <= q[0] < w and 0 <= q[1] < h and q not in seen and op[q][3] > 0:
                        seen.add(q)
                        st.append(q)
            xs = [q[0] for q in comp]
            if not lo <= (min(xs) + max(xs)) / 2 < hi or len(comp) < 60:  # ngoài cột, hoặc chấm vụn
                for q in comp:
                    op[q] = (0, 0, 0, 0)
    bb = out.getbbox()
    return out.crop(bb)


items = []
for s, row in enumerate(NAMES):
    # tờ 3 (đồ nhỏ) gen lại không có thoi nền (small_props_nobase.txt, Magnific 2026-11-18): gọt thoi lá / rêu bị thủng
    src = Image.open(os.path.join(HERE, SHEETS[s]))
    W, H = src.size
    for k, (name, group) in enumerate(row):
        x0, x1 = int(k * W / 5), int((k + 1) * W / 5)
        pad = 70
        bx0 = max(0, x0 - pad)
        img = cut(src, (bx0, 0, min(W, x1 + pad), H), (x0 - bx0, x1 - bx0))
        a = img.split()[3].load()
        w, h = img.size
        bottom = max(y for y in range(h) for x in range(0, w, 2) if a[x, y] > 0)
        lo = [x for y in range(int(h * 0.82), h) for x in range(w) if a[x, y] > 0]
        bx = (min(lo) + max(lo)) / 2
        if group == "small":
            foot = img.size[0]  # không có thoi nền
        else:
            foot = round(measure_diamond(img, bottom)[2])
            img = strip_foot(img, bx, bottom, foot)
        items.append({"name": name, "group": group, "img": img, "pivot": [round(bx / w, 4), round(1 - (bottom + 1) / h, 4)], "foot": foot})

# xếp kệ: hàng cao bằng món cao nhất của hàng, lề 4 px
PAD, MAXW = 4, 2048
x = y = rowh = 0
for it in items:
    w, h = it["img"].size
    if x + w + PAD > MAXW:
        x, y, rowh = 0, y + rowh + PAD, 0
    it["x"], it["y"] = x, y
    x += w + PAD
    rowh = max(rowh, h)
AW, AH = MAXW, y + rowh
atlas = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
meta = []
for it in items:
    atlas.alpha_composite(it["img"], (it["x"], it["y"]))
    w, h = it["img"].size
    meta.append({"name": "tree_" + it["name"], "group": it["group"], "x": it["x"], "y": it["y"], "w": w, "h": h, "pivot": it["pivot"], "foot": it["foot"]})
atlas.save(os.path.join(OUT, "home_trees.png"))
json.dump({"w": AW, "h": AH, "items": meta}, open(os.path.join(OUT, "home_trees.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", AW, AH, [(m["name"], m["w"], m["h"], m["foot"]) for m in meta])
