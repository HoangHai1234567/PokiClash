# Dựng ảnh mẫu cho concept đảo Thủy kiểu vùng đất (GD_Claude/18): tờ 10 tướng, bố cục toàn đảo, bố cục một màn.
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
HEROES = [(1, "ti_tach_1"), (5, "thach_giai_1"), (10, "ca_den_1"), (15, "ha_ba_1"), (20, "so_ngoc_1"),
          (30, "giong_bao_1"), (40, "lien_kinh_1"), (50, "uyen_xa_1"), (60, "han_ngac_1"), (70, "hai_long_1")]

def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def hero_sheet():
    cw, ch = 300, 340
    im = Image.new("RGB", (cw * 5, ch * 2 + 0), (250, 246, 236))
    d = ImageDraw.Draw(im)
    for i, (st, hid) in enumerate(HEROES):
        x, y = (i % 5) * cw, (i // 5) * ch
        p = Image.open(os.path.join(RES, hid, hid + "_portrait.png")).convert("RGBA")
        p.thumbnail((270, 270))
        im.paste(p, (x + (cw - p.width) // 2, y + 50), p)
        d.text((x + cw // 2, y + 24), str(st), fill=(60, 40, 30), font=font(36), anchor="mm")
        d.rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], outline=(180, 160, 130), width=2)
    im.save(os.path.join(OUT, "heroes_thuy.png"))
    # tướng đồng hành (dạng tiến hóa của tướng khởi đầu)
    c = Image.open(os.path.join(RES, "ti_tach_2", "ti_tach_2_portrait.png")).convert("RGBA")
    bg = Image.new("RGB", c.size, (250, 246, 236)); bg.paste(c, (0, 0), c); bg.save(os.path.join(OUT, "companion.png"))

def diamond(cx, cy, w):
    h = w / 2
    return [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]

# Toàn đảo 1024 x 1536: điểm uốn đường (dưới lên), chỗ habitat (stage, x, y, cỡ 3/4)
PATH = [(520, 1530), (520, 1440), (600, 1340), (640, 1240), (520, 1150), (380, 1070), (400, 960), (560, 880),
        (660, 790), (600, 690), (430, 620), (360, 520), (470, 430), (620, 360), (600, 250), (520, 160)]
HABS = [(1, 330, 1390, 3), (5, 790, 1250, 3), (10, 270, 1120, 3), (15, 760, 990, 3), (20, 230, 880, 3),
        (30, 830, 760, 3), (40, 230, 640, 3), (50, 740, 520, 4), (60, 250, 380, 4), (70, 560, 130, 4)]
RESERVE = [(830, 1460), (180, 250), (870, 300)]
LAGOONS = [[(560, 1010), (640, 1030), (660, 1090), (600, 1110), (540, 1080)],
           [(110, 520), (200, 500), (250, 560), (180, 600), (100, 580)],
           [(620, 610), (700, 600), (720, 650), (650, 670)]]

def land_poly():
    pts = []
    for i in range(72):
        a = i / 72 * 2 * math.pi
        r = 1 + 0.035 * math.sin(a * 5) + 0.025 * math.sin(a * 9 + 1)
        pts.append((512 + 470 * r * math.cos(a), 790 + 740 * r * math.sin(a)))
    return pts

def layout(path, size, crop=None):
    W, H = 1024, 1536
    im = Image.new("RGB", (W, H), (120, 180, 220))
    d = ImageDraw.Draw(im)
    lp = land_poly()
    d.polygon([(x, y + 14) for x, y in lp], fill=(236, 222, 170))  # bờ cát
    d.polygon([(512 + (x - 512) * 0.93, 790 + (y - 790) * 0.95) for x, y in lp], fill=(170, 210, 130))
    d.rectangle([440, 1440, 600, 1536], fill=(236, 222, 170))  # bãi vào
    for lg in LAGOONS: d.polygon(lg, fill=(120, 180, 220), outline=(80, 120, 160))
    d.line(PATH, fill=(240, 226, 180), width=46, joint="curve")
    d.line(PATH, fill=(200, 180, 130), width=2)
    for i in range(1, len(PATH) - 1, 1):
        x, y = PATH[i]; d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(250, 250, 250), outline=(90, 70, 50))
    for st, x, y, s in HABS:
        w = 190 if s == 3 else 250
        d.polygon(diamond(x, y, w), fill=(210, 190, 150), outline=(80, 55, 35), width=4)
        d.text((x, y), str(st), fill=(80, 30, 20), font=font(34), anchor="mm")
    for x, y in RESERVE:
        dm = diamond(x, y, 230)
        for a, b in zip(dm, dm[1:] + dm[:1]):
            n = 10
            for k in range(0, n, 2):
                p = (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
                q = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
                d.line([p, q], fill=(90, 90, 90), width=3)
        d.text((x, y), "R", fill=(90, 90, 90), font=font(30), anchor="mm")
    if crop:
        im = im.crop(crop).resize(size, Image.LANCZOS)
    im.save(os.path.join(OUT, path))

hero_sheet()
layout("layout_overview.png", (1024, 1536))
# một màn điện thoại 9:16 quanh ải 1, 5, 10 (khung 1080 x 1920 ứng với ~ 0,55 bề ngang đảo)
layout("layout_screen.png", (1024, 1536), crop=(150, 960, 150 + 690, 960 + 1035 if 960 + 1035 <= 1536 else 1536))
print("ok")
