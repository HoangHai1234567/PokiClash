# Xem nhanh đường đi viên bi (out/track.json do "chay.py dump" ghi): tờ khung nhìn nghiêng như trong game + đồ thị bán kính, độ nảy.
# py -3 -I xem_bi.py [gif]
import json, math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "out", "track.json")))
pts, dt = T["pts"], T["dt"]
R, K, KZ = 200, 0.6, 0.8
SLOTS = 26


def height(r):
    def lerp(a, b, t):
        return a + (b - a) * max(0, min(1, t))
    if r >= 0.90: return 0.20
    if r >= 0.80: return lerp(0.085, 0.14, (r - 0.80) / 0.10)
    if r >= 0.70: return lerp(0.03, 0.085, (r - 0.70) / 0.10)
    if r >= 0.61: return lerp(0.0, 0.03, (r - 0.61) / 0.09)
    if r >= 0.50: return 0.0
    return lerp(0.10, 0.0, max(0, r - 0.12) / 0.38)


def proj(x, y, z=0.0, cx=230, cy=190):
    r = math.hypot(x, y)
    return cx + R * x, cy - R * (K * y + KZ * (height(r) + z))


def ring(d, r, col, w=2, cx=230, cy=190):
    h = height(r - 1e-4)
    pp = [(cx + R * r * math.cos(a), cy - R * (K * r * math.sin(a) + KZ * h)) for a in [i * math.pi / 60 for i in range(121)]]
    d.line(pp, fill=col, width=w)


def frame(i):
    im = Image.new("RGB", (460, 380), (40, 48, 96))
    d = ImageDraw.Draw(im)
    x, y, z, rot = pts[i]
    for r, c in ((1.0, (150, 96, 48)), (0.90, (150, 96, 48)), (0.80, (120, 80, 40)), (0.70, (200, 170, 120)), (0.61, (90, 90, 90)), (0.50, (200, 170, 120))):
        ring(d, r, c)
    for k in range(8):
        a = (k + 0.5) * math.pi / 4
        px, py = proj(0.765 * math.cos(a), 0.765 * math.sin(a))
        d.ellipse([px - 5, py - 3, px + 5, py + 3], fill=(230, 190, 60))
    for j in range(SLOTS):
        a = rot + j * 2 * math.pi / SLOTS
        p0, p1 = proj(0.50 * math.cos(a), 0.50 * math.sin(a)), proj(0.61 * math.cos(a), 0.61 * math.sin(a))
        d.line([p0, p1], fill=(255, 255, 255) if j else (255, 80, 80), width=2)
    a = rot + (T["slot"] + 0.5) * 2 * math.pi / SLOTS
    q = proj(0.66 * math.cos(a), 0.66 * math.sin(a))
    d.ellipse([q[0] - 4, q[1] - 3, q[0] + 4, q[1] + 3], fill=(255, 220, 0))
    bx, by = proj(x, y, z)
    br = 0.040 * R
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 250, 235), outline=(60, 36, 20), width=2)
    d.text((6, 4), "%.2fs" % (i * dt), fill=(255, 255, 255))
    return im


if len(sys.argv) > 1 and sys.argv[1] == "gif":
    fr = [frame(i) for i in range(0, len(pts), 4)]
    fr[0].save(os.path.join(HERE, "out", "bi.gif"), save_all=True, append_images=fr[1:], duration=33, loop=0)
    print("out/bi.gif", len(fr), "khung")
# tờ khung: mỗi 0,25 s
idx = list(range(0, len(pts), 30))
cols = 8
rows = (len(idx) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 460, rows * 380 + 260), (20, 20, 30))
for n, i in enumerate(idx):
    sheet.paste(frame(i), ((n % cols) * 460, (n // cols) * 380))
# đồ thị: bán kính (trắng), độ nảy ×4 (vàng), vạch va chạm
d = ImageDraw.Draw(sheet)
y0 = rows * 380 + 250
W = cols * 460
n = len(pts)
for i in range(1, n):
    xa, xb = (i - 1) * W / n, i * W / n
    ra, rb = math.hypot(pts[i - 1][0], pts[i - 1][1]), math.hypot(pts[i][0], pts[i][1])
    d.line([xa, y0 - ra * 240, xb, y0 - rb * 240], fill=(255, 255, 255), width=2)
    d.line([xa, y0 - pts[i - 1][2] * 960, xb, y0 - pts[i][2] * 960], fill=(255, 220, 0), width=2)
for t, k, pw in T["hits"]:
    if k == 0: continue
    x = t / dt * W / n
    d.line([x, y0, x, y0 - 20 - 60 * pw], fill={1: (230, 120, 60), 2: (120, 200, 255), 3: (160, 160, 160), 4: (80, 255, 80)}[k], width=2)
for r in (0.868, 0.70, 0.555):
    d.line([0, y0 - r * 240, W, y0 - r * 240], fill=(90, 90, 110))
sheet.save(os.path.join(HERE, "out", "bi_to.jpg"), quality=80)
print("out/bi_to.jpg", sheet.size, "dur", T["duration"], "drop", T["drop"], "tries", T["tries"])
