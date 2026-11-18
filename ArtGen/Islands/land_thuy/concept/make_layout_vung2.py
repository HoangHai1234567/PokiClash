# Bố cục đảo Thủy 10 vùng, MỘT đường (GD_Claude/18, 2026-11-18): giữ dáng đảo và kiểu vùng của concept C,
# đường lượn tự nhiên, đi thẳng vào giữa từng vùng tới habitat của boss (không đi vòng ngoài vùng).
# Giữ chỗ vùng 1, 5, 30, 70; đổi chỗ 6 vùng còn lại để đường không cắt nhau. Ảnh 1536 x 864.
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
def catmull(pts, k=14):
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                   + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1]); return out
def diamond(d, x, y, s, label):
    w = 190 if s == 3 else 250; h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(215, 195, 155), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(32), anchor="mm")
def reserve(d, x, y):
    w = 170; h = w / 2; dm = [(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)]
    for a, b in zip(dm, dm[1:] + dm[:1]):
        for k in range(0, 10, 2):
            d.line([(a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10),
                    (a[0] + (b[0] - a[0]) * (k + 1) / 10, a[1] + (b[1] - a[1]) * (k + 1) / 10)], fill=(90, 90, 90), width=3)
    d.text((x, y), "R", fill=(90, 90, 90), font=font(26), anchor="mm")

# ải, tâm habitat, bán kính vùng, màu môi trường, cỡ
REG = [(1, (770, 735), (230, 120), (226, 214, 150), 3),   # bãi biển nắng, bến vào (giữ chỗ)
       (5, (390, 690), (200, 130), (150, 175, 95), 3),    # đầm lá súng (giữ chỗ)
       (10, (190, 440), (170, 140), (190, 190, 175), 3),  # mũi đá hải đăng, bờ tây
       (15, (175, 170), (160, 120), (110, 200, 190), 3),  # rạn san hô, góc tây bắc
       (20, (480, 245), (190, 125), (205, 180, 130), 3),  # vịnh tàu đắm, bờ bắc
       (30, (760, 470), (230, 125), (125, 140, 125), 3),  # cao nguyên giông, giữa đảo (giữ chỗ)
       (40, (1170, 700), (210, 130), (150, 175, 200), 3), # vịnh xương kình, đông nam
       (50, (1335, 455), (170, 135), (95, 95, 140), 4),   # vực hang, bờ đông
       (60, (1125, 225), (200, 120), (225, 235, 245), 4), # vùng băng, đông bắc
       (70, (790, 120), (210, 105), (150, 200, 205), 4)]  # đền rồng, đỉnh bắc (giữ chỗ)
C = {r[0]: r[1] for r in REG}
PATH = [(770, 880), (765, 805), C[1], (670, 790), (590, 720), (500, 765), C[5], (320, 640), (250, 590), (290, 520), C[10],
        (260, 360), (150, 300), (120, 240), C[15], (290, 160), (330, 230), (400, 300), C[20], (600, 290), (580, 370),
        (670, 390), C[30], (860, 520), (900, 610), (1010, 580), (1060, 680), C[40], (1280, 680), (1300, 600), (1230, 530), C[50],
        (1300, 360), (1210, 320), C[60], (1030, 280), (990, 200), (900, 170), C[70]]
im = Image.new("RGB", (W, H), (120, 180, 220)); d = ImageDraw.Draw(im)
d.polygon(blob(768, 445, 745, 405, 0), fill=(236, 222, 170)); d.polygon(blob(768, 445, 725, 388, 0), fill=(170, 205, 130))
for st, (x, y), (rx, ry), col, s in REG: d.polygon(blob(x, y + 5, rx, ry, st * .37, p=.9), fill=col)
d.polygon(blob(950, 92, 70, 45, 2), fill=(120, 180, 220))    # vịnh xoáy nước cạnh đền
d.polygon(blob(470, 95, 90, 45, 3), fill=(110, 150, 190))    # nước vịnh tàu đắm
d.polygon(blob(90, 150, 70, 60, 4), fill=(120, 190, 210))    # nước nông rạn san hô
d.polygon(blob(1260, 760, 80, 45, 5), fill=(120, 180, 220))  # vịnh kình
c = catmull(PATH); d.line(c, fill=(244, 232, 190), width=28, joint="curve")
d.line([(770, 864), (768, 810)], fill=(150, 105, 60), width=40)  # bến gỗ
acc, last = 0, c[0]
for p in c[1:]:
    acc += math.dist(p, last); last = p
    if acc > 46 and all(math.dist(p, C[k]) > 105 for k in C):
        acc = 0; d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(255, 255, 255), outline=(90, 70, 50))
for st, (x, y), (rx, ry), col, s in REG: diamond(d, x, y, s, str(st))
reserve(d, 590, 590); reserve(d, 1000, 395); reserve(d, 1400, 790)
im.save(os.path.join(OUT, "layout_vung2.png")); print("ok")
