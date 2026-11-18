# Ba kiểu đường hai chiều cho đảo Thủy (GD_Claude/18): xoắn ốc, zíc zắc ngang, quần đảo. Ảnh 1024 x 1024.
import os, math
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
SEA, SAND, GRASS, ROAD, WATER = (120, 180, 220), (236, 222, 170), (170, 210, 130), (240, 226, 180), (120, 180, 220)

def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def blob(cx, cy, rx, ry, seed=0, n=48):
    return [(cx + rx * (1 + .06 * math.sin(a * 5 + seed) + .04 * math.sin(a * 9 + seed * 2)) * math.cos(a),
             cy + ry * (1 + .06 * math.sin(a * 4 + seed) + .04 * math.sin(a * 7 + seed)) * math.sin(a))
            for a in [i / n * 2 * math.pi for i in range(n)]]

def catmull(pts, k=12):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                   + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1]); return out

def diamond(d, x, y, s, label):
    w = 150 if s == 3 else 205; h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(210, 190, 150), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(30), anchor="mm")

def reserve(d, x, y):
    w = 170; h = w / 2; dm = [(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)]
    for a, b in zip(dm, dm[1:] + dm[:1]):
        for k in range(0, 10, 2):
            d.line([(a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10),
                    (a[0] + (b[0] - a[0]) * (k + 1) / 10, a[1] + (b[1] - a[1]) * (k + 1) / 10)], fill=(90, 90, 90), width=3)
    d.text((x, y), "R", fill=(90, 90, 90), font=font(26), anchor="mm")

def road(d, pts, bridges=()):
    c = catmull(pts)
    d.line(c, fill=ROAD, width=34, joint="curve")
    for a, b in bridges:  # cầu gỗ: dải nâu có ván
        d.line([a, b], fill=(150, 105, 60), width=30)
        L = math.dist(a, b); n = int(L / 14)
        for i in range(n + 1):
            t = i / max(n, 1); x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
            ux, uy = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
            d.line([(x - ux * 15, y - uy * 15), (x + ux * 15, y + uy * 15)], fill=(95, 65, 35), width=3)
    # chấm ải xen giữa
    acc, last = 0, c[0]
    for p in c[1:]:
        acc += math.dist(p, last); last = p
        if acc > 48: acc = 0; d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=(255, 255, 255), outline=(90, 70, 50))

def save(im, name): im.save(os.path.join(OUT, name))

# A. Xoắn ốc: chạy vòng ngoài ngược chiều kim đồng hồ rồi cuộn vào giữa, boss ở giữa
def spiral():
    im = Image.new("RGB", (1024, 1024), SEA); d = ImageDraw.Draw(im)
    d.polygon(blob(512, 520, 480, 470, 1), fill=SAND); d.polygon(blob(512, 520, 450, 440, 1), fill=GRASS)
    d.polygon(blob(512, 500, 120, 90, 3), fill=WATER)  # hồ giữa quanh đền boss
    cx, cy = 512, 520; pts = []
    for i in range(0, 61):
        f = i / 60; th = math.radians(95 - 600 * f); r = 1 - 0.78 * f
        pts.append((cx + 380 * r * math.cos(th), cy + 370 * r * math.sin(th)))
    pts = [(470, 1010)] + pts
    road(d, pts[:-3], bridges=[(pts[-6], pts[-1])])
    habs = [(1, .04, 1), (5, .12, -1), (10, .2, 1), (15, .28, -1), (20, .37, 1), (30, .47, -1), (40, .57, 1), (50, .68, -1), (60, .8, 1)]
    for st, f, side in habs:
        th = math.radians(95 - 600 * f); r = 1 - 0.78 * f + side * 0.2 * (1 - f * 0.4)
        diamond(d, cx + 380 * r * math.cos(th), cy + 370 * r * math.sin(th), 4 if st >= 50 else 3, str(st))
    diamond(d, 512, 500, 4, "70")
    reserve(d, 150, 520); reserve(d, 880, 240)
    save(im, "layout_xoan_oc.png")

# B. Zíc zắc ngang: 4 tầng bậc thềm, mỗi tầng đi hết bề ngang rồi leo lên tầng trên
def zigzag():
    im = Image.new("RGB", (1024, 1024), SEA); d = ImageDraw.Draw(im)
    d.polygon(blob(512, 520, 490, 470, 2), fill=SAND); d.polygon(blob(512, 520, 460, 440, 2), fill=GRASS)
    for y in (770, 540, 310):  # vách bậc thềm
        d.line([(70, y), (954, y)], fill=(150, 110, 80), width=8)
    pts = [(160, 1010), (150, 900), (500, 885), (860, 880), (900, 790), (860, 690), (500, 660), (150, 650), (120, 560),
           (160, 460), (500, 430), (860, 420), (900, 330), (860, 230), (600, 190)]
    road(d, pts)
    for st, x, y, s in [(1, 330, 960, 3), (5, 680, 810, 3), (10, 820, 975, 3), (15, 620, 735, 3), (20, 280, 585, 3),
                        (30, 420, 735, 3), (40, 700, 500, 3), (50, 330, 355, 4), (60, 720, 275, 4), (70, 420, 160, 4)]:
        diamond(d, x, y, s, str(st))
    reserve(d, 900, 590); reserve(d, 150, 270)
    save(im, "layout_zic_zac.png")

# C. Quần đảo: các đảo nhỏ nối bằng cầu gỗ, đường đi vòng trên biển
def archipelago():
    im = Image.new("RGB", (1024, 1024), SEA); d = ImageDraw.Draw(im)
    isl = [(240, 870, 205, 115, 1), (770, 840, 195, 115, 2), (830, 560, 140, 100, 3), (320, 560, 220, 125, 4),
           (190, 260, 160, 115, 5), (500, 300, 150, 110, 6), (800, 190, 190, 130, 7)]
    small = [(565, 710, 85, 55, 8), (560, 80, 90, 55, 9), (960, 380, 70, 60, 10)]
    for cx, cy, rx, ry, s in isl + small:
        d.polygon(blob(cx, cy, rx + 14, ry + 12, s), fill=SAND); d.polygon(blob(cx, cy, rx, ry, s), fill=GRASS)
    pts = [(240, 1010), (240, 930), (330, 900), (440, 880), (600, 870), (700, 900), (820, 880), (850, 760), (840, 640),
           (800, 580), (660, 565), (530, 560), (400, 590), (260, 560), (220, 450), (210, 360), (230, 290), (330, 300),
           (420, 320), (560, 290), (650, 250), (720, 230)]
    road(d, pts, bridges=[((440, 880), (585, 872)), ((852, 745), (845, 655)), ((690, 566), (535, 562)),
                          ((218, 440), (212, 372)), ((340, 302), (380, 312)), ((640, 255), (665, 245))])
    for st, x, y, s in [(1, 140, 860, 3), (5, 330, 820, 3), (10, 690, 790, 3), (15, 880, 830, 3), (20, 860, 520, 3),
                        (30, 220, 620, 3), (40, 420, 510, 3), (50, 170, 230, 4), (60, 520, 360, 4), (70, 820, 170, 4)]:
        diamond(d, x, y, s, str(st))
    for cx, cy, *_ in small: reserve(d, cx, cy)
    save(im, "layout_quan_dao.png")

spiral(); zigzag(); archipelago()
a, b, c = (Image.open(os.path.join(OUT, n)) for n in ("layout_xoan_oc.png", "layout_zic_zac.png", "layout_quan_dao.png"))
s = Image.new("RGB", (3 * 1024 + 40, 1024), (40, 40, 40))
for i, im in enumerate((a, b, c)): s.paste(im, (i * 1044, 0))
s.thumbnail((1800, 1800)); s.save(os.path.join(OUT, "..", "_soi_layouts2.png")); print("ok")
