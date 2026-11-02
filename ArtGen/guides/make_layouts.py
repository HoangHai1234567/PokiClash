# Dựng ảnh bố cục 1024 x 1536 cho GPT vẽ bản đồ đảo hệ (Z1–Z5 trong ArtGen/Islands/PROMPTS.md), học bố cục bản đồ cuộn dọc:
# đất phủ kín khung (chỉ dải biển và bãi cát ở đáy), một con đường rộng lượn chữ S lớn từ bãi dưới lên bãi đấu boss trên đỉnh,
# khúc giữa phình rộng cho mini boss. Không vẽ ô ải: game đặt nút ải lên đường.
# Toạ độ đường (PATHS) và 8 ải dự kiến tính theo khung 9:16 của game (x, y từ 0 đến 1, y từ trên); ảnh 9:16 nằm ở dải giữa
# x 80..944 của khung GPT. Màn đảo phóng 1,27 lần nên chỉ thấy khoảng x 0,11..0,89: giữ đường trong 0,2..0,8.
# Ghi ArtGen/guides/L_zone_<hệ>.png và zone_nodes.json (8 ải dự kiến, chép vào ZONES[].nodes khi có ảnh thật).
# Chạy từ thư mục PokiWar: py -3 -I ArtGen/guides/make_layouts.py
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent
W, H, BAND_X, BAND_W = 1024, 1536, 80, 864
INK = (43, 33, 24)
SEA = (68, 206, 220)
SAND = (246, 228, 176)
ROAD_W = 118  # bề rộng đường (px khung GPT), khoảng 1/7 bề ngang

# hệ: (màu đất, màu đường, các điểm uốn của đường từ bãi dưới lên đỉnh)
PATHS = {
    "thuy": ((176, 222, 168), (246, 230, 180), [(0.50, 0.98), (0.76, 0.84), (0.28, 0.66), (0.74, 0.47), (0.30, 0.29), (0.52, 0.11)]),
    "hoa": ((214, 116, 84), (205, 188, 170), [(0.40, 0.98), (0.72, 0.85), (0.66, 0.70), (0.27, 0.58), (0.32, 0.41), (0.74, 0.29), (0.50, 0.11)]),
    "kim": ((186, 192, 204), (226, 224, 216), [(0.50, 0.98), (0.79, 0.87), (0.22, 0.74), (0.79, 0.59), (0.23, 0.43), (0.76, 0.28), (0.50, 0.11)]),
    "moc": ((140, 200, 100), (226, 204, 152), [(0.60, 0.98), (0.26, 0.83), (0.72, 0.66), (0.29, 0.50), (0.71, 0.34), (0.44, 0.21), (0.50, 0.10)]),
    "tho": ((226, 186, 104), (246, 232, 190), [(0.45, 0.98), (0.76, 0.81), (0.30, 0.70), (0.25, 0.53), (0.71, 0.42), (0.73, 0.25), (0.50, 0.11)]),
}


def spline(pts, n=400):
    """Catmull-Rom qua các điểm uốn"""
    p = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n // (len(p) - 3)):
            t = k / (n // (len(p) - 3))
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def at_length(line, frac):
    """điểm ở phân số frac của chiều dài đường (đo trong khung 9:16 có tỉ lệ thật)"""
    seg = [math.hypot((b[0] - a[0]) * 9, (b[1] - a[1]) * 16) for a, b in zip(line, line[1:])]
    target, acc = frac * sum(seg), 0
    for (a, b), s in zip(zip(line, line[1:]), seg):
        if acc + s >= target:
            t = (target - acc) / s if s else 0
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        acc += s
    return line[-1]


def px(p):
    return (BAND_X + p[0] * BAND_W, p[1] * H)


def hatch(d, box, base, seed, n=2600):
    r = random.Random(seed)
    dark = tuple(max(0, c - 40) for c in base)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, L = r.uniform(x0 - 40, x1), r.uniform(y0, y1 + 40), r.uniform(24, 60)
        d.line([(x, y), (x + L * 0.42, y - L)], fill=dark + (r.randint(40, 90),), width=2)


nodes_all = {}
for zid, (ground, road, pts) in PATHS.items():
    im = Image.new("RGB", (W, H), ground)
    d = ImageDraw.Draw(im, "RGBA")
    hatch(d, (0, 0, W, H), ground, hash(zid) % 1000)
    # biển và bãi cát ở đáy (điểm xuất phát)
    beach = [(0, H * 0.93)] + [(x, H * (0.93 + 0.012 * math.sin(x / 70))) for x in range(0, W + 1, 16)] + [(W, H)] + [(0, H)]
    d.polygon(beach, fill=SAND)
    sea = [(0, H * 0.965)] + [(x, H * (0.965 + 0.008 * math.sin(x / 55 + 1))) for x in range(0, W + 1, 16)] + [(W, H)] + [(0, H)]
    d.polygon(sea, fill=SEA)
    d.line([(x, H * (0.93 + 0.012 * math.sin(x / 70))) for x in range(0, W + 1, 16)], fill=INK, width=4)
    # đường: dải rộng có viền mực, bãi đấu boss tròn ở đỉnh, khúc giữa phình cho mini boss
    line = spline(pts)
    pl = [px(p) for p in line]
    nodes = [at_length(line, f) for f in (0.05, 0.18, 0.31, 0.45, 0.58, 0.71, 0.84, 1.0)]
    # đóng dấu tròn dọc đường (mép mượt): cả lớp viền mực trước, rồi cả lớp mặt đường, nên viền chỉ còn ở mép ngoài
    bulges = ((px(nodes[3]), 0.85), (px(nodes[7]), 1.35))
    for w, col in ((ROAD_W + 10, INK), (ROAD_W, road)):
        for p in pl:
            d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)
        for c, k in bulges:
            rad = ROAD_W * k + (5 if col == INK else 0)
            d.ellipse((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), fill=col)
    im.save(OUT / f"L_zone_{zid}.png")
    nodes_all[zid] = [[round(x, 3), round(y, 3)] for x, y in nodes]
    print(f"L_zone_{zid}: 8 ải dự kiến", nodes_all[zid])

(OUT / "zone_nodes.json").write_text(json.dumps(nodes_all, indent=1), encoding="utf-8")
