# Bố cục đảo Thủy rộng ngang (GD_Claude/18, 2026-11-18): một đảo khoảng 3 màn ngang x 1,7 màn dọc,
# đường hành trình đi ngang ba lượt qua ba vùng cảnh, habitat rải hai bên đường. Ảnh 1536 x 864 (16:9).
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageChops
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
W, H = 1536, 864
def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()
def island(cx, cy, rx, ry, grow=0, n=160):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi; c, s = math.cos(a), math.sin(a)
        e = 1 + .05 * math.sin(a * 5) + .03 * math.sin(a * 11 + 1) + .04 * math.sin(a * 3 + 2)
        x = math.copysign(abs(c) ** .7, c) * (rx * e + grow); y = math.copysign(abs(s) ** .7, s) * (ry * e + grow)
        pts.append((cx + x, cy + y))
    return pts
def catmull(pts, k=12):
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                   + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1]); return out
def diamond(d, x, y, s, label):
    w = 205 if s == 3 else 270; h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(215, 195, 155), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(34), anchor="mm")
def reserve(d, x, y):
    w = 200; h = w / 2; dm = [(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)]
    for a, b in zip(dm, dm[1:] + dm[:1]):
        for k in range(0, 10, 2):
            d.line([(a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10),
                    (a[0] + (b[0] - a[0]) * (k + 1) / 10, a[1] + (b[1] - a[1]) * (k + 1) / 10)], fill=(90, 90, 90), width=3)
    d.text((x, y), "R", fill=(90, 90, 90), font=font(28), anchor="mm")

im = Image.new("RGB", (W, H), (120, 180, 220)); d = ImageDraw.Draw(im)
d.polygon(island(768, 445, 730, 400, 18), fill=(236, 222, 170))
# ba vùng cảnh theo dải ngang: dưới bờ biển nắng, giữa rạn và đầm, trên vực đá và băng
reg = Image.new("RGB", (W, H)); rd = ImageDraw.Draw(reg)
rd.rectangle([0, 0, W, H], fill=(178, 214, 128))
rd.polygon([(0, 0), (W, 0)] + [(x, 590 - 60 * math.sin(x / 210) - 30 * math.sin(x / 77)) for x in range(W, -1, -16)], fill=(120, 185, 150))
rd.polygon([(0, 0), (W, 0)] + [(x, 315 + 55 * math.sin(x / 180 + 1) + 25 * math.sin(x / 61)) for x in range(W, -1, -16)], fill=(185, 200, 215))
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(island(768, 445, 730, 400), fill=255)
im.paste(reg, (0, 0), mask); d = ImageDraw.Draw(im)
# vịnh xoáy nước cạnh đền boss, hồ nhỏ
d.polygon(island(1440, 300, 70, 60), fill=(120, 180, 220)); d.polygon(island(215, 590, 80, 50), fill=(120, 180, 220))
d.polygon(island(150, 170, 60, 45), fill=(120, 180, 220))
path = [(180, 880), (230, 770), (400, 720), (560, 660), (760, 700), (980, 655), (1180, 690), (1330, 640), (1400, 560),
        (1310, 470), (1180, 500), (1000, 440), (820, 470), (640, 425), (470, 470), (300, 430), (200, 350), (240, 255),
        (400, 225), (600, 260), (780, 210), (980, 235), (1180, 175)]
c = catmull(path); d.line(c, fill=(244, 232, 190), width=34, joint="curve")
acc, last = 0, c[0]
for p in c[1:]:
    acc += math.dist(p, last); last = p
    if acc > 52: acc = 0; d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(255, 255, 255), outline=(90, 70, 50))
for st, x, y, s in [(1, 470, 800, 3), (5, 880, 560, 3), (10, 1080, 790, 3), (15, 1200, 585, 3), (20, 1110, 360, 3),
                    (30, 600, 555, 3), (40, 410, 340, 3), (50, 520, 112, 4), (60, 790, 335, 4), (70, 1300, 160, 4)]:
    diamond(d, x, y, s, str(st))
reserve(d, 930, 100); reserve(d, 1330, 770); reserve(d, 140, 470)
im.save(os.path.join(OUT, "layout_rong.png")); print("ok")
