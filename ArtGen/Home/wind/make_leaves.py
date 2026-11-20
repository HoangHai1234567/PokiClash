# Lá, cánh hoa bay theo gió trên màn Nhà (GD_Claude/22_Critters_Home.md mốc A4, học hạt gió pbvx_camp_wind của Clash of Critters).
# Vẽ tay giả lập theo nét game: tô phẳng một màu, viền mực nâu sẫm, không bóng, không quầng. Vẽ to gấp 4 rồi thu nhỏ cho mép mịn.
# Ra: Assets/03 Art/Home/home_leaf_<1..4>.png. Chạy: py -3 -I ArtGen/Home/wind/make_leaves.py
import math
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Home")
INK = (74, 46, 28, 255)
K = 4


def leaf(w, h, fill, vein=True, petal=False):
    W, H = w * K, h * K
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = W / 2, H / 2
    pts = []
    for i in range(64):
        t = i / 64 * 2 * math.pi
        x = math.cos(t)
        y = math.sin(t)
        if petal:  # cánh hoa: tròn, khía ở đầu
            r = 1 - 0.18 * max(0, math.cos(t)) ** 8
            pts.append((cx + x * r * (W / 2 - 2 * K), cy + y * r * (H / 2 - 2 * K)))
        else:      # lá: thuôn nhọn hai đầu
            yy = y * (abs(math.cos(t * 0.5)) ** 0.0) * (1 - 0.35 * abs(x) ** 3)
            pts.append((cx + x * (W / 2 - 2 * K), cy + yy * (H / 2 - 2 * K)))
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=INK, width=int(1.6 * K), joint="curve")
    if vein:
        d.line([(cx - W * 0.36, cy + H * 0.04), (cx + W * 0.34, cy - H * 0.03)], fill=INK, width=int(1.0 * K))
    return im.resize((w, h), Image.LANCZOS)


if __name__ == "__main__":
    shapes = [
        leaf(30, 16, (124, 192, 74, 255)),                 # lá xanh
        leaf(26, 14, (168, 214, 90, 255)),                 # lá non
        leaf(28, 15, (240, 192, 64, 255)),                 # lá vàng
        leaf(18, 15, (244, 167, 192, 255), vein=False, petal=True),  # cánh hoa hồng
    ]
    for i, im in enumerate(shapes, 1):
        im.save(os.path.join(OUT, "home_leaf_%d.png" % i))
    print("ok", len(shapes), "ảnh lá")
