# Ảnh mẫu cho concept đảo Kim kiểu vùng đất (người dùng 2026-11-19: "làm tiếp đảo kim"). Theo cách đảo Hỏa
# (ArtGen/Islands/land_hoa/concept/make_refs_hoa.py), rút kinh nghiệm Mộc, Hỏa ngay ở bố cục:
# - MỘT đường, không nhánh, không vòng, không lối cụt; bệ 1 chỉ nối bến và bệ 5; sông chảy từ núi giữa ra biển ngăn bệ 1 với 50;
# - chặng 9 cờ (20→30 … 60→70) đường dài, uốn lượn sẵn;
# - màu theo chất kim loại (thép, bạc, đồng thau, đồng đỏ, đá cẩm thạch); không dặn mảng cỏ xanh, nước xanh lá (Hỏa bị chê vì thế).
# Ra:
# - refs/heroes_kim.png: 10 boss của 10 ải tướng (dạng đầu), số ải trên đầu;
# - refs/layout_kim.png: bố cục 10 vùng, đường từ bến (đáy) đi vòng ngoài ngược chiều kim đồng hồ (đông nam → đông → bắc → tây →
#   tây nam), rồi vào đồi tổ pha lê phía tây núi giữa và leo xoắn lên tháp chuông trên đỉnh núi ở tim đảo (ải 70). Ảnh 1536 x 864.
# In độ dài đường từng chặng (đơn vị ảnh mẫu) để soát chặng 9 cờ đủ dài (>= 560).
import math
import sys
import os

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "refs")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
HEROES = [(1, "tinh_sat_1"), (5, "chien_sat_1"), (10, "quang_sat_1"), (15, "cua_xich_1"), (20, "quy_xich_1"),
          (30, "soi_giap_1"), (40, "robot_co_1"), (50, "ky_nguyen_1"), (60, "thu_phao_1"), (70, "vua_may_1")]
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
    im.save(os.path.join(OUT, "heroes_kim.png"))


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


# ải, tâm habitat, bán kính vùng, màu môi trường (chỉ để phân vùng trên ảnh mẫu), cỡ habitat
REG = [(1, (770, 745), (210, 100), (120, 130, 140), 3),    # Cảng Sắt: bến vào, cần cẩu, mỏ neo, thùng hàng
       (5, (1120, 700), (200, 115), (196, 160, 92), 3),    # Cầu Bánh Răng: đông nam, suối có cầu bánh răng đồng thau
       (10, (1340, 455), (160, 145), (128, 176, 180), 3),  # Rừng Lưỡi Liềm: bờ đông, cây lá lưỡi liềm thép xanh ngọc
       (15, (1190, 200), (190, 110), (150, 158, 170), 3),  # Tháp Canh Thép: đông bắc, tháp canh khung thép
       (20, (860, 115), (190, 95), (214, 176, 92), 3),     # Gác Chuông Đồng: bắc, gác chuông mái cong, chuông đồng
       (30, (480, 135), (200, 100), (196, 112, 76), 3),    # Xưởng Đúc Chuông: tây bắc, lò đúc, khuôn chuông
       (40, (195, 380), (160, 150), (96, 92, 104), 3),     # Mỏ Sắt Ngân: bờ tây, cửa mỏ, xe goòng, quặng bạc
       (50, (380, 700), (210, 110), (176, 168, 196), 4),   # Thành Ba Kiếm: tây nam, thành đá, ba thanh kiếm khổng lồ cắm đất
       (60, (575, 465), (150, 110), (150, 210, 214), 4),   # Tổ Cánh Pha Lê: đồi trong phía tây núi giữa, tổ có pha lê
       (70, (880, 395), (230, 165), (110, 116, 132), 4)]   # Tháp Thiên Chung: núi giữa đảo, tháp chuông trên đỉnh (lớn nhất)
C = {r[0]: r[1] for r in REG}
# điểm dẫn: chặng 9 cờ uốn lượn cho đủ dài; 60 → 70 leo xoắn quanh sườn núi giữa
PATH = [(770, 880), (770, 810), C[1],
        (900, 760), (1010, 735), C[5],
        (1240, 650), (1310, 570), C[10],
        (1340, 340), (1290, 260), C[15],
        (1080, 170), (990, 130), C[20],
        (760, 160), (720, 260), (640, 290), (590, 220), (560, 160), C[30],
        (380, 160), (350, 270), (270, 290), (230, 220), (150, 260), C[40],
        (140, 500), (210, 560), (150, 640), (230, 720), C[50],
        (500, 720), (540, 640), (440, 590), (450, 500), C[60],
        (680, 560), (840, 600), (1010, 560), (1080, 450), (1020, 320), (900, 290), C[70]]


def layout():
    im = Image.new("RGB", (W, H), (120, 180, 220))
    d = ImageDraw.Draw(im)
    d.polygon(blob(768, 445, 745, 405, 2.1), fill=(70, 66, 70))
    d.polygon(blob(768, 445, 725, 388, 2.1), fill=(150, 120, 100))
    for st, (x, y), (rx, ry), col, s in REG:
        d.polygon(blob(x, y + 5, rx, ry, st * .37, p=.9), fill=col)
    # sông chảy từ núi giữa ra biển phía tây bến, ngăn vùng bến (1) với thành ba kiếm (50): không có đường nào qua
    river = catmull([(760, 470), (700, 560), (640, 650), (610, 760), (600, 864)])
    d.line(river, fill=(90, 150, 220), width=26, joint="curve")
    # suối nhỏ vùng cầu bánh răng (đường 1 → 5 qua cầu bánh răng)
    d.line(catmull([(980, 600), (1000, 700), (990, 864)]), fill=(90, 150, 220), width=18, joint="curve")
    c = catmull(PATH)
    d.line(c, fill=(244, 232, 190), width=28, joint="curve")
    d.line([(770, 864), (770, 815)], fill=(150, 105, 60), width=40)  # bến gỗ
    acc, last = 0, c[0]
    for p in c[1:]:
        acc += math.dist(p, last)
        last = p
        if acc > 46 and all(math.dist(p, C[k]) > 105 for k in C):
            acc = 0
            d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=(255, 255, 255), outline=(90, 70, 50))
    for st, (x, y), (rx, ry), col, s in REG:
        diamond(d, x, y, s, str(st))
    im.save(os.path.join(OUT, "layout_kim.png"))
    # độ dài từng chặng (tâm bệ → tâm bệ, theo đường đã làm mượt)
    idx = []
    for st in C:
        idx.append(min(range(len(c)), key=lambda i: math.dist(c[i], C[st])))
    L = [0]
    for a, b in zip(c, c[1:]):
        L.append(L[-1] + math.dist(a, b))
    stg = list(C)
    for k in range(len(stg) - 1):
        print(f"{stg[k]} -> {stg[k + 1]}: {round(L[idx[k + 1]] - L[idx[k]])}  ({stg[k + 1] - stg[k] - 1} cờ)")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero_sheet()
    layout()
    print("ok", OUT)
