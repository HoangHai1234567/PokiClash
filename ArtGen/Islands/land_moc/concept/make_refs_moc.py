# Ảnh mẫu cho concept đảo Mộc kiểu vùng đất (người dùng 2026-11-19: "làm tiếp tương tự đảo mộc theo đảo thủy, các hình dáng đảo và path
# đi có thể thay đổi"). Theo cách đảo Thủy (ArtGen/Islands/land_thuy/concept/make_refs.py, make_layout_vung2.py):
# - refs/heroes_moc.png: 10 boss của 10 ải tướng (dạng đầu, như trên bản đồ: evo → dạng 1), số ải trên đầu;
# - refs/layout_moc.png: bố cục 10 vùng, MỘT đường xoắn ốc từ bến (đáy) đi vòng ngoài ngược chiều kim đồng hồ rồi vào tim đảo, nơi
#   đứng Cây Thần Ngàn Năm (ải 70). Mỗi mảng màu là một vùng, ô thoi có số là habitat, chấm trắng là ải xen giữa. Ảnh 1536 x 864.
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
HEROES = [(1, "tien_la_1"), (5, "mam_u_1"), (10, "gac_da_1"), (15, "bom_la_1"), (20, "phong_linh_1"),
          (30, "gio_loc_1"), (40, "long_vuot_1"), (50, "tho_hoang_1"), (60, "giac_moc_1"), (70, "moc_vuong_d1")]
W, H = 1536, 864


def font(sz):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def hero_sheet():
    cw, ch = 300, 340
    im = Image.new("RGB", (cw * 5, ch * 2), (250, 246, 236))
    d = ImageDraw.Draw(im)
    for i, (st, hid) in enumerate(HEROES):
        x, y = (i % 5) * cw, (i // 5) * ch
        p = Image.open(os.path.join(RES, hid, hid + "_portrait.png")).convert("RGBA")
        p.thumbnail((270, 270))
        im.paste(p, (x + (cw - p.width) // 2, y + 50), p)
        d.text((x + cw // 2, y + 24), str(st), fill=(60, 40, 30), font=font(36), anchor="mm")
        d.rectangle([x + 4, y + 4, x + cw - 4, y + ch - 4], outline=(180, 160, 130), width=2)
    im.save(os.path.join(OUT, "heroes_moc.png"))


def blob(cx, cy, rx, ry, seed=0, p=.7, n=120):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        c, s = math.cos(a), math.sin(a)
        e = 1 + .05 * math.sin(a * 5 + seed) + .03 * math.sin(a * 11 + 1 + seed) + .04 * math.sin(a * 3 + 2 + seed)
        pts.append((cx + math.copysign(abs(c) ** p, c) * rx * e, cy + math.copysign(abs(s) ** p, s) * ry * e))
    return pts


def catmull(pts, k=14):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                   + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1])
    return out


def diamond(d, x, y, s, label):
    w = 190 if s == 3 else 250
    h = w / 2
    d.polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=(215, 195, 155), outline=(80, 55, 35), width=4)
    d.text((x, y), label, fill=(80, 30, 20), font=font(32), anchor="mm")


# ải, tâm habitat, bán kính vùng, màu môi trường, cỡ habitat
REG = [(1, (770, 735), (220, 110), (150, 172, 110), 3),    # Bờ Rêu: bến vào, đá phủ rêu, dương xỉ
       (5, (1135, 690), (200, 120), (214, 214, 120), 3),   # Đồng Hoa Sáng: đông nam
       (10, (1340, 440), (165, 140), (210, 140, 112), 3),  # Đồi Nấm: bờ đông
       (15, (1140, 190), (200, 115), (82, 140, 82), 3),    # Rừng Dây Leo: đông bắc
       (20, (790, 125), (200, 100), (160, 176, 170), 3),   # Hang Nanh Gió: bắc
       (30, (430, 185), (200, 115), (222, 180, 92), 3),    # Thung Lũng Lá: tây bắc
       (40, (185, 440), (165, 140), (150, 130, 112), 3),   # Vách Vuốt Rồng: bờ tây
       (50, (410, 690), (200, 120), (122, 200, 152), 4),   # Rừng Trúc Ngọc: tây nam
       (60, (560, 455), (150, 105), (88, 168, 122), 4),    # Hang Pha Lê Lục: đồi trong, phía tây tim đảo
       (70, (935, 425), (200, 135), (70, 120, 70), 4)]     # Cây Thần Ngàn Năm: tim đảo (lớn nhất)
C = {r[0]: r[1] for r in REG}
PATH = [(770, 880), (768, 805), C[1], (900, 760), (1000, 700), C[5], (1240, 640), (1300, 560), C[10], (1310, 320), (1240, 260),
        C[15], (1000, 165), (900, 215), C[20], (660, 165), (560, 230), C[30], (330, 260), (250, 330), C[40], (240, 560),
        (300, 640), C[50], (520, 640), (590, 560), C[60], (700, 430), (790, 360), (860, 400), C[70]]


def layout():
    im = Image.new("RGB", (W, H), (120, 180, 220))
    d = ImageDraw.Draw(im)
    d.polygon(blob(768, 445, 745, 405, 1.3), fill=(236, 222, 170))
    d.polygon(blob(768, 445, 725, 388, 1.3), fill=(150, 195, 120))
    for st, (x, y), (rx, ry), col, s in REG:
        d.polygon(blob(x, y + 5, rx, ry, st * .37, p=.9), fill=col)
    d.polygon(blob(1290, 790, 90, 45, 5), fill=(120, 180, 220))   # vịnh nhỏ đông nam (bờ đồng hoa)
    d.polygon(blob(80, 650, 70, 70, 4), fill=(120, 180, 220))     # vịnh tây nam dưới vách vuốt rồng
    d.polygon(blob(700, 560, 60, 35, 2), fill=(110, 170, 210))    # hồ nhỏ giữa đảo (suối trúc chảy vào)
    c = catmull(PATH)
    d.line(c, fill=(244, 232, 190), width=28, joint="curve")
    d.line([(770, 864), (768, 810)], fill=(150, 105, 60), width=40)  # bến gỗ
    acc, last = 0, c[0]
    for p in c[1:]:
        acc += math.dist(p, last)
        last = p
        if acc > 46 and all(math.dist(p, C[k]) > 105 for k in C):
            acc = 0
            d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(255, 255, 255), outline=(90, 70, 50))
    for st, (x, y), (rx, ry), col, s in REG:
        diamond(d, x, y, s, str(st))
    im.save(os.path.join(OUT, "layout_moc.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero_sheet()
    layout()
    print("ok", OUT)
