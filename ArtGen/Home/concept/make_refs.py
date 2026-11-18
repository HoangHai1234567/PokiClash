# Dựng ảnh mẫu cho concept Nhà (GD_Claude/21_Nha_Home.md): tờ tướng làm việc, phác bố cục toàn đảo nhà, phác bố cục một màn.
# Chạy: py -3 -I make_refs.py (đường dẫn tính từ chỗ đặt file).
import os, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
os.makedirs(OUT, exist_ok=True)

# chữ cái, tướng, việc (theo GD_Claude/21_Nha_Home.md)
WORKERS = [("A", "mam_u_1"), ("B", "gac_da_1"), ("C", "ti_tach_1"), ("D", "hat_de_1"),
           ("E", "hoa_nhan_1"), ("F", "doc_giac_1"), ("G", "thach_giai_1")]


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def worker_sheet():
    cw, ch = 280, 320
    cols = 4
    rows = math.ceil(len(WORKERS) / cols)
    im = Image.new("RGB", (cw * cols, ch * rows), (250, 246, 236))
    d = ImageDraw.Draw(im)
    for i, (k, hid) in enumerate(WORKERS):
        x, y = (i % cols) * cw, (i // cols) * ch
        p = Image.open(os.path.join(RES, hid, hid + "_portrait.png")).convert("RGBA")
        p.thumbnail((250, 250))
        im.paste(p, (x + (cw - p.width) // 2, y + 55), p)
        d.text((x + cw // 2, y + 26), k, fill=(60, 40, 30), font=font(38), anchor="mm")
        d.rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], outline=(180, 160, 130), width=2)
    im.save(os.path.join(OUT, "workers.png"))


def diamond(cx, cy, hw, hh):
    return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]


def dashed(d, pts, fill, width=3, dash=14):
    for a, b in zip(pts, pts[1:] + pts[:1]):
        L = math.dist(a, b)
        n = max(1, int(L // dash))
        for s in range(0, n, 2):
            t0, t1 = s / n, min(1, (s + 1) / n)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=fill, width=width)


def blob(cx, cy, rx, ry, n=80, seed=0.0):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        r = 1 + 0.04 * math.sin(a * 5 + seed) + 0.025 * math.sin(a * 11 + 2 * seed)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


SEA, SAND, GRASS, FOREST, HILL, ORE, WATER, PATH, INK = (
    (120, 180, 222), (238, 222, 168), (178, 214, 128), (58, 120, 62), (150, 128, 108), (120, 110, 104),
    (90, 160, 220), (226, 204, 150), (60, 40, 30))

# Toàn đảo 1536 x 1024: lưới ô rừng 5 x 5 (mỗi ô rừng = 4 x 4 ô lưới), nhìn chéo
PW, PH = 135, 67.5
O = (768, 118)


def plot_c(i, j):
    return (O[0] + (i - j) * PW, O[1] + (i + j) * PH)


# K đã dọn, R mạch quặng (đã dọn, có Mỏ), C đang dọn, S dọn được, L chưa mở, H đồi đá
PLOTS = {
    (0, 0): "H", (0, 1): "H", (1, 0): "H", (0, 2): "L", (2, 0): "L", (1, 1): "L",
    (0, 3): "L", (3, 0): "L", (0, 4): "L", (4, 0): "L", (1, 4): "L", (4, 1): "L",
    (1, 2): "R", (2, 1): "C", (1, 3): "S", (3, 1): "S",
    (2, 2): "K", (2, 3): "K", (3, 2): "K", (2, 4): "K", (4, 2): "K", (3, 3): "K", (3, 4): "K", (4, 3): "K", (4, 4): "K",
}
FILL = {"K": GRASS, "R": ORE, "C": (140, 170, 100), "S": FOREST, "L": FOREST, "H": HILL}

# công trình (số, x, y, bán kính phác)
BUILDINGS = [(1, 768, 440, 70), (2, 600, 470, 42), (3, 615, 575, 42), (4, 690, 640, 38), (5, 465, 515, 46),
             (6, 960, 455, 40), (7, 530, 560, 18), (8, 850, 640, 34), (9, 880, 545, 34), (10, 1075, 515, 40),
             (11, 768, 560, 22), (12, 1000, 590, 30), (13, 633, 312, 46)]
STREAM = [(640, 150), (590, 205), (520, 250), (500, 320), (490, 400), (470, 470), (440, 560), (360, 620), (280, 670), (220, 700)]
PATHS = [[(768, 830), (768, 700), (768, 600), (768, 510)], [(768, 600), (680, 570), (560, 520)],
         [(768, 600), (860, 590), (960, 540), (1060, 540)], [(720, 470), (680, 380), (640, 345)]]


def island_layout():
    W, H = 1536, 1024
    im = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(im)
    top = (O[0], O[1] - PH)
    left = (O[0] - 5 * PW, O[1] + 4 * PH)
    right = (O[0] + 5 * PW, O[1] + 4 * PH)
    bottom = (O[0], O[1] + 9 * PH)
    # bờ: vành cát quanh lưới (rộng ở bờ nam), vành cỏ mỏng
    d.polygon([(top[0], top[1] - 40), (right[0] + 70, right[1]), (bottom[0], bottom[1] + 120), (left[0] - 70, left[1])], fill=SAND)
    d.polygon([(top[0], top[1] - 25), (right[0] + 40, right[1]), (bottom[0], bottom[1] + 40), (left[0] - 40, left[1])], fill=GRASS)
    for (i, j), k in PLOTS.items():
        c = plot_c(i, j)
        poly = diamond(c[0], c[1], PW, PH)
        d.polygon(poly, fill=FILL[k])
        if k in "SLCH":
            dashed(d, poly, (240, 240, 230), 3)
        if k == "L":
            # cây dày + biển khoá
            for t in range(9):
                tx = c[0] + (t % 3 - 1) * 55 + (t // 3 - 1) * 12
                ty = c[1] + (t // 3 - 1) * 22
                d.ellipse([tx - 18, ty - 18, tx + 18, ty + 14], fill=(40, 96, 46), outline=INK)
        if k != "K":
            d.text(c, k, fill=(255, 255, 255), font=font(30), anchor="mm")
    d.line(STREAM, fill=WATER, width=16)
    for p in PATHS:
        d.line(p, fill=PATH, width=14)
    # bến thuyền ở mũi nam, thuyền buồm
    d.rectangle([752, bottom[1] + 10, 784, bottom[1] + 110], fill=(150, 100, 60), outline=INK, width=2)
    d.polygon([(820, 850), (890, 850), (875, 865), (835, 865)], fill=(150, 100, 60), outline=INK)
    d.polygon([(855, 785), (855, 845), (895, 845)], fill=(250, 250, 240), outline=INK)
    d.text((768, bottom[1] + 60), "D", fill=(255, 255, 255), font=font(26), anchor="mm")
    for n, x, y, r in BUILDINGS:
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(250, 240, 220), outline=INK, width=3)
        d.text((x, y), str(n), fill=INK, font=font(26 if r > 20 else 18), anchor="mm")
    # dời xuống cho cân khung (bớt biển trống ở đáy)
    out = Image.new("RGB", (W, H), SEA)
    out.paste(im.crop((0, 0, W, H - 80)), (0, 80))
    out.save(os.path.join(OUT, "layout_island.png"))


def screen_layout():
    W, H = 1024, 1536
    im = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(im)
    # đất: phần nam của khoảnh đã dọn, bãi cát và biển ở đáy
    d.polygon([(0, 130), (1024, 130), (1024, 1060), (700, 1150), (300, 1150), (0, 1040)], fill=SAND)
    d.polygon([(0, 130), (1024, 130), (1024, 990), (690, 1070), (320, 1070), (0, 980)], fill=GRASS)
    # ô rừng: trên trái chưa mở (khoá), trên phải dọn được
    d.polygon([(0, 130), (330, 130), (190, 330), (0, 330)], fill=FOREST)
    dashed(d, [(0, 130), (330, 130), (190, 330), (0, 330)], (240, 240, 230))
    d.text((110, 220), "L", fill=(255, 255, 255), font=font(40), anchor="mm")
    d.polygon([(760, 130), (1024, 130), (1024, 420), (900, 380)], fill=FOREST)
    dashed(d, [(760, 130), (1024, 130), (1024, 420), (900, 380)], (240, 240, 230))
    d.text((930, 250), "S", fill=(255, 255, 255), font=font(40), anchor="mm")
    # ao cá trái, suối chảy ra biển
    d.ellipse([20, 560, 230, 720], fill=WATER, outline=INK, width=3)
    d.line([(60, 330), (90, 450), (110, 560)], fill=WATER, width=18)
    d.line([(100, 720), (60, 860), (20, 1000)], fill=WATER, width=18)
    # đường đất từ bến lên nhà chính, rẽ hai bên
    for p in [[(512, 1250), (512, 1060), (512, 760), (512, 420)], [(512, 760), (380, 700), (240, 640)], [(512, 760), (660, 700), (800, 560)]]:
        d.line(p, fill=PATH, width=26)
    # bến và thuyền
    d.rectangle([490, 1080, 534, 1290], fill=(150, 100, 60), outline=INK, width=3)
    d.polygon([(600, 1250), (720, 1250), (700, 1280), (620, 1280)], fill=(150, 100, 60), outline=INK)
    d.polygon([(660, 1130), (660, 1245), (730, 1245)], fill=(250, 250, 240), outline=INK)
    items = [("1", 512, 300, 120, 80), ("2", 300, 520, 90, 55), ("3", 330, 760, 90, 55), ("7", 430, 650, 26, 18),
             ("11", 560, 600, 34, 26), ("8", 760, 760, 70, 45), ("9", 820, 480, 70, 45), ("5", 125, 640, 0, 0),
             ("P", 512, 920, 90, 40), ("D", 512, 1180, 0, 0)]
    for n, x, y, rx, ry in items:
        if rx:
            d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(250, 240, 220), outline=INK, width=3)
        d.text((x, y), n, fill=INK if rx else (255, 255, 255), font=font(34), anchor="mm")
    # khung UI: thanh trên, khay dưới
    d.rectangle([20, 20, 1004, 120], fill=(250, 246, 236), outline=INK, width=4)
    d.text((512, 70), "TOP BAR", fill=INK, font=font(32), anchor="mm")
    d.rectangle([20, 1340, 1004, 1516], fill=(250, 246, 236), outline=INK, width=4)
    d.text((512, 1428), "BOTTOM BUTTONS", fill=INK, font=font(32), anchor="mm")
    im.save(os.path.join(OUT, "layout_screen.png"))


if __name__ == "__main__":
    worker_sheet()
    island_layout()
    screen_layout()
    print("ok", OUT)
