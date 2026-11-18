# Ảnh mẫu bố cục concept Nhà, lần 2 (2026-11-18): isometric 2:1 đúng như Clash of Critters (ô thoi rộng gấp đôi cao, camera
# trực giao, góc nhìn vẽ sẵn trong ảnh). Đảo 48 x 48 ô, ô rừng 8 x 8 ô; công trình thường 4 x 4, nhà chính 6 x 6, giếng và cây bi 2 x 2.
# Ra: refs/iso_overview.png (toàn đảo thu nhỏ hết cỡ), refs/iso_screen.png (một màn), refs/iso_build.png (một màn, chế độ xây).
# Chạy: py -3 -I make_refs_iso.py
import os, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)

INK = (60, 40, 30)
SEA, SAND, GRASS, FOREST, FOREST2, HILLTOP, CLIFF, ORE, WATER, PATH, PAPER = (
    (120, 180, 222), (238, 222, 168), (178, 214, 128), (58, 120, 62), (40, 96, 46), (130, 180, 90), (150, 100, 70),
    (128, 118, 112), (90, 160, 220), (226, 204, 150), (250, 246, 236))
FACE_L, FACE_R, ROOF = (236, 214, 176), (214, 188, 146), (200, 90, 70)


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


class Iso:
    """Chiếu ô lưới (gx, gy) ra màn: gx đi xuống phải, gy đi xuống trái, ô rộng cw cao cw/2."""

    def __init__(self, ox, oy, cw):
        self.ox, self.oy, self.cw, self.ch = ox, oy, cw, cw / 2

    def p(self, gx, gy, z=0):
        return (self.ox + (gx - gy) * self.cw / 2, self.oy + (gx + gy) * self.ch / 2 - z)

    def quad(self, gx, gy, w, d, z=0):
        return [self.p(gx, gy, z), self.p(gx + w, gy, z), self.p(gx + w, gy + d, z), self.p(gx, gy + d, z)]


def box(d, iso, gx, gy, w, dd, h, top=ROOF, label=None, fs=24):
    """Khối hộp trên chân thoi: mặt trái, mặt phải, mặt trên (chỉ để chỉ góc nhìn, không phải màu thật)."""
    a, b, c, e = iso.quad(gx, gy, w, dd)  # trên, phải, dưới, trái
    at, bt, ct, et = iso.quad(gx, gy, w, dd, h)
    d.polygon([e, c, ct, et], fill=FACE_L, outline=INK)
    d.polygon([c, b, bt, ct], fill=FACE_R, outline=INK)
    d.polygon([at, bt, ct, et], fill=top, outline=INK)
    if label:
        cx = (at[0] + ct[0]) / 2
        cy = (at[1] + ct[1]) / 2
        d.text((cx, cy), label, fill=(255, 255, 255), font=font(fs), anchor="mm", stroke_width=2, stroke_fill=INK)


def flat(d, iso, gx, gy, w, dd, fill, label=None, fs=24, outline=INK):
    q = iso.quad(gx, gy, w, dd)
    d.polygon(q, fill=fill, outline=outline)
    if label:
        cx = (q[0][0] + q[2][0]) / 2
        cy = (q[0][1] + q[2][1]) / 2
        d.text((cx, cy), label, fill=(255, 255, 255), font=font(fs), anchor="mm", stroke_width=2, stroke_fill=INK)


def trees(d, iso, gx, gy, w, dd, step=1.6, r=None):
    """Rừng dày: tán tròn xếp kín trên chân thoi."""
    r = r or iso.cw * 0.55
    k = 0
    y = 0.4
    while y < dd:
        x = 0.4 + (k % 2) * step / 2
        while x < w:
            cx, cy = iso.p(gx + x, gy + y)
            d.ellipse([cx - r * 0.5, cy - r * 1.4, cx + r * 0.5, cy - r * 0.3], fill=FOREST2, outline=INK)
            x += step
        y += step * 0.8
        k += 1


def dashed_quad(d, q, fill=(245, 245, 235), width=2, dash=10):
    for a, b in zip(q, q[1:] + q[:1]):
        L = math.dist(a, b)
        n = max(2, int(L // dash))
        for s in range(0, n, 2):
            t0, t1 = s / n, (s + 1) / n
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=fill, width=width)


# ---------- toàn đảo: 48 x 48 ô = 6 x 6 ô rừng ----------
# K đã mở, R mạch quặng (có Mỏ), C đang dọn, S dọn được, L chưa mở, W hồ, H cao nguyên
LOTS = {}
for i in range(6):
    for j in range(6):
        LOTS[(i, j)] = "L"
for k in [(3, 3), (3, 4), (4, 3), (4, 4), (4, 5), (5, 4), (5, 5), (3, 5), (5, 3), (2, 3), (3, 2)]:
    LOTS[k] = "K"
LOTS.update({(2, 4): "R", (2, 2): "C", (1, 3): "S", (3, 1): "S", (4, 2): "S", (0, 0): "H", (0, 1): "H", (1, 0): "H", (1, 1): "W", (5, 0): "H", (0, 5): "W"})

# công trình theo ô lưới: số, gx, gy, rộng, sâu, cao (theo cw), nhãn
BUILD = [(1, 31, 31, 6, 6, 3.2), (2, 25, 37, 4, 4, 0.3), (3, 25, 42, 4, 4, 0.3), (7, 30, 41, 2, 2, 1.0), (5, 19, 26, 4, 4, 0.1),
         (6, 40, 26, 4, 4, 1.8), (9, 40, 33, 4, 4, 1.8), (8, 43, 39, 4, 4, 1.6), (12, 35, 25, 4, 4, 1.6), (10, 26, 26, 4, 4, 0.4),
         (11, 37, 38, 2, 2, 1.6), (4, 31, 44, 4, 4, 1.2), (13, 18, 34, 6, 6, 1.6)]


def overview():
    W, H = 1792, 1024
    im = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(im)
    iso = Iso(896, 96, 32)
    # dải phong cảnh xa ở trên, cao nguyên ôm hai cạnh trên, bãi cát ôm hai cạnh dưới
    d.rectangle([0, 0, W, 60], fill=(160, 200, 150))
    d.text((W / 2, 30), "far landscape strip (hills, river)", fill=INK, font=font(22), anchor="mm")
    top, right, bottom, left = iso.p(0, 0), iso.p(48, 0), iso.p(48, 48), iso.p(0, 48)
    d.polygon([(top[0], top[1] - 60), (right[0] + 110, right[1]), right, top, left, (left[0] - 110, left[1])], fill=HILLTOP, outline=INK)
    d.polygon([(left[0] - 110, left[1]), left, bottom, right, (right[0] + 110, right[1]), (bottom[0], bottom[1] + 110)], fill=SAND, outline=INK)
    for (i, j), k in sorted(LOTS.items(), key=lambda t: t[0][0] + t[0][1]):
        gx, gy = i * 8, j * 8
        if k == "K":
            flat(d, iso, gx, gy, 8, 8, GRASS, outline=None)
        elif k == "R":
            flat(d, iso, gx, gy, 8, 8, ORE, outline=None)
        elif k == "W":
            flat(d, iso, gx, gy, 8, 8, GRASS, outline=None)
            flat(d, iso, gx + 1.5, gy + 1.5, 5, 5, WATER, "W", 22)
        elif k == "H":
            box(d, iso, gx + 0.5, gy + 0.5, 7, 7, 40, HILLTOP, "H", 24)
        elif k == "C":
            flat(d, iso, gx, gy, 8, 8, (150, 180, 105), "C", 26)
        else:
            flat(d, iso, gx, gy, 8, 8, FOREST, outline=None)
            trees(d, iso, gx, gy, 8, 8)
            q = iso.quad(gx, gy, 8, 8)
            c = ((q[0][0] + q[2][0]) / 2, (q[0][1] + q[2][1]) / 2)
            d.text(c, k, fill=(255, 255, 255), font=font(26), anchor="mm", stroke_width=2, stroke_fill=INK)
    # ranh ô rừng (chỉ để đọc bố cục)
    for i in range(7):
        d.line([iso.p(i * 8, 0), iso.p(i * 8, 48)], fill=(240, 240, 230), width=1)
        d.line([iso.p(0, i * 8), iso.p(48, i * 8)], fill=(240, 240, 230), width=1)
    # suối từ cao nguyên H qua hồ W xuống ao 5
    d.line([iso.p(4, 12), iso.p(10, 14), iso.p(12, 20), iso.p(19, 27)], fill=WATER, width=10)
    # đường đất từ bến lên nhà chính
    d.line([iso.p(47.5, 47.5), iso.p(41, 41), iso.p(37, 37)], fill=PATH, width=12)
    for n, gx, gy, w, dd, h in sorted(BUILD, key=lambda b: b[1] + b[2]):
        box(d, iso, gx, gy, w, dd, h * iso.cw / 2, ROOF if h > 0.6 else (150, 110, 70), str(n), 20)
    # bến và thuyền ở mũi nam
    b = iso.p(48, 48)
    d.polygon([(b[0] - 8, b[1] - 4), (b[0] + 8, b[1] - 4), (b[0] + 40, b[1] + 70), (b[0] + 24, b[1] + 74)], fill=(150, 100, 60), outline=INK)
    d.text((b[0] + 70, b[1] + 60), "D", fill=INK, font=font(26), anchor="mm")
    d.polygon([(b[0] + 90, b[1] + 90), (b[0] + 150, b[1] + 90), (b[0] + 140, b[1] + 104), (b[0] + 100, b[1] + 104)], fill=(150, 100, 60), outline=INK)
    d.polygon([(b[0] + 120, b[1] + 40), (b[0] + 120, b[1] + 88), (b[0] + 150, b[1] + 88)], fill=(250, 250, 240), outline=INK)
    im.save(os.path.join(OUT, "iso_overview.png"))


# ---------- một màn: ô 96 px ở khung 1024 rộng (khoảng 10–11 ô ngang màn) ----------
def screen(build=False):
    W, H = 1024, 1820
    im = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(im)
    iso = Iso(512, 860 - 72 * 24, 96)  # ô (36, 36) nằm ở (512, 860)

    def at(gx, gy):
        return iso.p(gx, gy)

    # đất: mọi ô có gx, gy < 48; bãi cát ngoài hai cạnh dưới
    q = [iso.p(0, 0), iso.p(48, 0), iso.p(48, 48), iso.p(0, 48)]
    s = iso.p(48, 48)
    d.polygon([iso.p(48, 20), iso.p(51, 20), iso.p(51, 51), iso.p(20, 51), iso.p(20, 48)], fill=SAND, outline=INK)
    d.polygon(q, fill=GRASS, outline=INK)
    # ô rừng: (2,3) khoá ở trên trái, (3,2) dọn được ở trên phải
    for gx, gy, lab in [(16, 24, "L (padlock sign)"), (24, 16, "S (axe sign)")]:
        flat(d, iso, gx, gy, 8, 8, FOREST, outline=None)
        trees(d, iso, gx, gy, 8, 8, 1.4)
        c = iso.p(gx + 5, gy + 5)
        d.text(c, lab, fill=(255, 255, 255), font=font(30), anchor="mm", stroke_width=3, stroke_fill=INK)
    if build:
        # lưới thoi hiện lúc xây, trên đất đã mở
        for gx in range(24, 48):
            for gy in range(24, 48):
                dashed_quad(d, iso.quad(gx, gy, 1, 1), (245, 245, 235), 1, 8)
    # đường lát 1 ô từ bến lên nhà chính
    for t in range(37, 48):
        flat(d, iso, t, t, 1, 1, PATH, outline=None)
        flat(d, iso, t + 1, t, 1, 1, PATH, outline=None)
    items = [("1", 30, 30, 6, 6, 2.6), ("2", 31, 37, 4, 4, 0.25), ("3", 36, 42, 4, 4, 0.25), ("7", 33, 42, 2, 2, 1.0),
             ("5", 27, 39, 4, 4, 0.05), ("11", 38, 37, 2, 2, 1.5), ("9", 40, 31, 4, 4, 1.8), ("8", 42, 38, 4, 4, 1.6),
             ("P", 42, 44, 2, 2, 0.8)]
    for n, gx, gy, w, dd, h in sorted(items, key=lambda b: b[1] + b[2]):
        lift = 0
        if build and n == "9":
            flat(d, iso, gx, gy, w, dd, (120, 220, 120), None)  # chân xanh: đặt được
            lift = 50
        z0 = lift
        a = iso.quad(gx, gy, w, dd, z0)
        at_ = iso.quad(gx, gy, w, dd, z0 + h * 48)
        d.polygon([a[3], a[2], at_[2], at_[3]], fill=FACE_L, outline=INK)
        d.polygon([a[2], a[1], at_[1], at_[2]], fill=FACE_R, outline=INK)
        d.polygon(at_, fill=ROOF if h > 0.6 else (150, 110, 70), outline=INK)
        cx = (at_[0][0] + at_[2][0]) / 2
        cy = (at_[0][1] + at_[2][1]) / 2
        d.text((cx, cy), n, fill=(255, 255, 255), font=font(40), anchor="mm", stroke_width=3, stroke_fill=INK)
    if build:
        # ô đỏ: chỗ không đặt được (chồng nhà chính) để chỉ cách báo
        for gx, gy in [(34, 34), (35, 34), (34, 35)]:
            flat(d, iso, gx, gy, 1, 1, (230, 110, 100), None)
    # bến, thuyền
    d.polygon([(s[0] - 14, s[1] - 6), (s[0] + 14, s[1] - 6), (s[0] + 110, s[1] + 150), (s[0] + 80, s[1] + 160)], fill=(150, 100, 60), outline=INK)
    d.text((s[0] + 150, s[1] + 120), "D", fill=INK, font=font(40), anchor="mm")
    # khung UI
    d.rectangle([20, 20, 1004, 150], fill=PAPER, outline=INK, width=4)
    d.text((512, 85), "TOP BAR", fill=INK, font=font(34), anchor="mm")
    d.rectangle([20, 1640, 1004, 1800], fill=PAPER, outline=INK, width=4)
    d.text((512, 1720), "BUILD TRAY (building cards)" if build else "BOTTOM BUTTONS", fill=INK, font=font(34), anchor="mm")
    im.save(os.path.join(OUT, "iso_build.png" if build else "iso_screen.png"))


if __name__ == "__main__":
    overview()
    screen(False)
    screen(True)
    print("ok", OUT)
