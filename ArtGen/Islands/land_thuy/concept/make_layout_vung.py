# Bố cục đảo Thủy kiểu bản đồ vùng (GD_Claude/18, 2026-11-18): một đảo rộng chia 10 vùng cảnh, mỗi vùng một tướng / boss,
# đường nối thành mạng giữa các vùng kề nhau, cấp tăng từ bãi biển dưới lên đền rồng trên cùng. Ảnh 1536 x 864.
import os, math, random
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
W, H = 1536, 864
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
    w = 190 if s == 3 else 250; h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(215, 195, 155), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(32), anchor="mm")
def reserve(d, x, y):
    w = 180; h = w / 2; dm = [(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)]
    for a, b in zip(dm, dm[1:] + dm[:1]):
        for k in range(0, 10, 2):
            d.line([(a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10),
                    (a[0] + (b[0] - a[0]) * (k + 1) / 10, a[1] + (b[1] - a[1]) * (k + 1) / 10)], fill=(90, 90, 90), width=3)
    d.text((x, y), "R", fill=(90, 90, 90), font=font(26), anchor="mm")

# vùng: ải, tâm habitat, bán kính vùng, màu nền vùng (môi trường), cỡ habitat
REG = [(1, (770, 735), (230, 120), (226, 214, 150), 3),   # bãi biển nắng (bến vào)
       (5, (390, 690), (200, 130), (150, 175, 95), 3),    # đầm lá súng
       (10, (1170, 700), (210, 130), (190, 190, 175), 3), # mũi đá hải đăng
       (15, (1330, 455), (170, 130), (110, 200, 190), 3), # rạn sò nước nông
       (20, (190, 440), (170, 140), (205, 180, 130), 3),  # vịnh tàu đắm
       (30, (760, 470), (230, 120), (125, 140, 125), 3),  # cao nguyên giông
       (40, (1120, 230), (200, 120), (150, 175, 200), 3), # vịnh xương kình
       (50, (470, 250), (200, 125), (95, 95, 140), 4),    # vực hang sâu
       (60, (170, 170), (150, 120), (225, 235, 245), 4),  # vùng băng
       (70, (790, 120), (210, 105), (150, 200, 205), 4)]  # đền rồng, xoáy nước
EDGES = [(1, 5), (1, 10), (1, 30), (5, 20), (10, 15), (15, 30), (20, 30), (5, 30), (15, 40), (30, 40), (30, 50),
         (20, 50), (50, 60), (40, 70), (50, 70)]
C = {r[0]: r[1] for r in REG}
im = Image.new("RGB", (W, H), (120, 180, 220)); d = ImageDraw.Draw(im)
d.polygon(blob(768, 445, 745, 405, 0), fill=(236, 222, 170)); d.polygon(blob(768, 445, 725, 388, 0), fill=(170, 205, 130))
for st, (x, y), (rx, ry), col, s in REG:
    d.polygon(blob(x, y + 5, rx, ry, st * .37, p=.9), fill=col)
d.polygon(blob(950, 95, 70, 45, 2), fill=(120, 180, 220))   # vịnh xoáy nước cạnh đền
d.polygon(blob(240, 520, 60, 35, 3), fill=(110, 150, 190))  # nước vịnh tàu đắm
d.polygon(blob(1420, 520, 70, 60, 4), fill=(120, 190, 210)) # nước nông rạn sò
random.seed(7)
def bez(a, b, bend):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; L = math.dist(a, b) or 1
    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L; c = (mx + nx * bend, my + ny * bend)
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]) for t in [i / 30 for i in range(31)]]
roads = [bez(C[a], C[b], random.uniform(-40, 40)) for a, b in EDGES]
for r in roads: d.line(r, fill=(244, 232, 190), width=26, joint="curve")
d.line([(770, 864), (770, 760)], fill=(150, 105, 60), width=40)  # bến gỗ
for st, (x, y), (rx, ry), col, s in REG:
    diamond(d, x, y, s, str(st))
    # ải xen giữa của vùng: vài cờ nhỏ quanh habitat
    for k in range(4):
        a = random.uniform(0, 2 * math.pi); r = random.uniform(.55, .85)
        px, py = x + math.cos(a) * rx * r, y + math.sin(a) * ry * r
        if 20 < px < W - 20 and 20 < py < H - 20:
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(255, 255, 255), outline=(90, 70, 50))
reserve(d, 1350, 760); reserve(d, 600, 590); reserve(d, 1400, 160)
im.save(os.path.join(OUT, "layout_vung.png")); print("ok")
