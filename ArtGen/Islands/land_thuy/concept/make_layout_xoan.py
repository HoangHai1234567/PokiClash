# Bố cục đảo Thủy một đường xoắn ốc (GD_Claude/18, 2026-11-18): vòng ngoài men bờ qua ải 1 → 40,
# rồi cuộn vào khối núi giữa đảo: 50 chân núi, 60 sườn băng, 70 đền rồng trên đỉnh. Ảnh 1536 x 1024 (3:2).
import os, math, random
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
W, H = 1536, 1024
def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()
def blob(cx, cy, rx, ry, seed=0, p=.7, n=120):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi; c, s = math.cos(a), math.sin(a)
        e = 1 + .05 * math.sin(a * 5 + seed) + .03 * math.sin(a * 11 + 1 + seed) + .04 * math.sin(a * 3 + 2 + seed)
        pts.append((cx + math.copysign(abs(c) ** p, c) * rx * e, cy + math.copysign(abs(s) ** p, s) * ry * e))
    return pts
def diamond(d, x, y, s, label):
    w = {3: 190, 4: 250, 5: 300}[s]; h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(215, 195, 155), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(32), anchor="mm")
def reserve(d, x, y):
    w = 180; h = w / 2; dm = [(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)]
    for a, b in zip(dm, dm[1:] + dm[:1]):
        for k in range(0, 10, 2):
            d.line([(a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10),
                    (a[0] + (b[0] - a[0]) * (k + 1) / 10, a[1] + (b[1] - a[1]) * (k + 1) / 10)], fill=(90, 90, 90), width=3)
    d.text((x, y), "R", fill=(90, 90, 90), font=font(26), anchor="mm")

CX, CY, RX, RY = 768, 520, 545, 330
def ring(th, r):  # th độ, tăng = đi ngược kim (y xuống): dưới → trái → trên → phải
    t = math.radians(th); w = 1 + .045 * math.sin(t * 3) + .025 * math.sin(t * 7 + 1)
    return (CX + RX * r * w * math.cos(t), CY + RY * r * w * math.sin(t))
def rad(th):  # bán kính đường theo góc: vòng ngoài 1, từ 365° cuộn vào
    return 1.0 if th <= 365 else max(0.0, 1.0 - (th - 365) / 250 * 0.95)
path = [(890, 1030), (880, 930)] + [ring(th, rad(th)) for th in range(70, 600, 6)]
# habitat: (ải, góc, lệch ra ngoài +px / vào trong -px, cỡ, màu vùng, bán kính vùng)
HAB = [(1, 100, 105, 3, (226, 214, 150), (230, 110)), (5, 142, 110, 3, (150, 175, 95), (200, 130)),
       (10, 182, 110, 3, (190, 190, 175), (170, 150)), (15, 224, 110, 3, (110, 200, 190), (200, 130)),
       (20, 270, 105, 3, (205, 180, 130), (220, 110)), (30, 318, 110, 3, (125, 140, 125), (210, 130)),
       (40, 4, 115, 3, (150, 175, 200), (170, 160))]
im = Image.new("RGB", (W, H), (120, 180, 220)); d = ImageDraw.Draw(im)
d.polygon(blob(768, 515, 755, 490, 0), fill=(236, 222, 170)); d.polygon(blob(768, 515, 735, 470, 0), fill=(170, 205, 130))
pos = {}
for st, th, off, s, col, (rx, ry) in HAB:
    x, y = ring(th, 1); t = math.radians(th)
    nx, ny = math.cos(t) / RX, math.sin(t) / RY; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    hx, hy = x + nx * off, y + ny * off; pos[st] = (hx, hy, s)
    d.polygon(blob(hx, hy, rx, ry, st * .37, p=.9), fill=col)
# khối núi giữa đảo: chân núi tối (vực hang), sườn băng, đỉnh đền
d.polygon(blob(768, 520, 360, 200, 5, p=.9), fill=(95, 95, 140))
d.polygon(blob(700, 470, 240, 130, 6, p=.9), fill=(225, 235, 245))
d.polygon(blob(780, 500, 150, 80, 7, p=.9), fill=(150, 200, 205))
c = path; d.line(c, fill=(244, 232, 190), width=30, joint="curve")
acc, last = 0, c[0]
for p in c[1:]:
    acc += math.dist(p, last); last = p
    if acc > 50: acc = 0; d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(255, 255, 255), outline=(90, 70, 50))
d.line([(890, 1024), (885, 960)], fill=(150, 105, 60), width=40)  # bến gỗ
for st, (hx, hy, s) in pos.items(): diamond(d, hx, hy, s, str(st))
diamond(d, *ring(440, rad(440) - .28), 4, "50")
diamond(d, *ring(520, rad(520) + .30), 4, "60")
diamond(d, 780, 505, 5, "70")
reserve(d, 1250, 860); reserve(d, 470, 335); reserve(d, 1400, 330)
im.save(os.path.join(OUT, "layout_xoan.png")); print("ok")
