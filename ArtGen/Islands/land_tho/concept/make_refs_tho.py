# Ảnh mẫu cho concept đảo Thổ kiểu vùng đất (người dùng 2026-11-19: "làm tiếp đảo thổ"). Khung đường lấy của đảo Hỏa
# (ArtGen/Islands/land_hoa/concept/make_refs_hoa.py: chặng 9 cờ đã đủ dài khi dò), rút kinh nghiệm Mộc, Hỏa, Kim:
# - MỘT đường, không nhánh, không vòng, không lối cụt; bệ 1 chỉ nối bến và bệ 5; hẻm núi đỏ khô từ cao nguyên giữa ra biển ngăn
#   bệ 1 với 50 (thay sông dung nham của Hỏa);
# - màu theo chất đất: vàng đất, đỏ đất nung, nâu, sa thạch; xanh chỉ ở ngọc lục và tán cây sồi, keo (không đồng cỏ xanh mướt).
# Ra:
# - refs/heroes_tho.png: 10 boss của 10 ải tướng (dạng đầu), số ải trên đầu;
# - refs/layout_tho.png: bố cục 10 vùng, đường từ bến (đáy) đi vòng ngoài theo chiều kim đồng hồ (tây nam → tây → bắc → đông →
#   đông nam), rồi vào đồi lò gốm phía đông cao nguyên và leo xoắn lên kim tự viện trên cao nguyên giữa đảo (ải 70). Ảnh 1536 x 864.
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
HEROES = [(1, "cong_da_1"), (5, "than_lan_cat_1"), (10, "thu_da_1"), (15, "rong_cat_non"), (20, "quy_nui_1"),
          (30, "hat_de_1"), (40, "sau_dat_non"), (50, "quai_bun_1"), (60, "tinh_hach_non"), (70, "thach_de_non")]
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
    im.save(os.path.join(OUT, "heroes_tho.png"))


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
REG = [(1, (770, 745), (210, 100), (196, 186, 170), 3),    # Bãi Đá Cuội: bến vào, đá cuội xếp chồng, vỏ ốc
       (5, (420, 700), (200, 115), (160, 112, 72), 3),     # Hang Lửng: tây nam, gò hang lửng, cuốc xẻng, xe gỗ, chum
       (10, (195, 455), (160, 145), (150, 196, 140), 3),   # Đồi Ngọc Lục: bờ tây, đồi bậc thang có ngọc lục
       (15, (335, 205), (190, 110), (178, 132, 176), 3),   # Mỏ Pha Lê: tây bắc, cửa mỏ, pha lê hồng tím, xe goòng, mũi khoan
       (20, (660, 115), (190, 95), (206, 196, 164), 3),    # Đền Phù Văn: bắc, vòng đá phù văn, bàn thờ đá
       (30, (1040, 130), (200, 100), (140, 156, 86), 3),   # Rừng Sồi Già: đông bắc, cây sồi cổ khổng lồ, ao nhỏ
       (40, (1335, 380), (160, 150), (222, 194, 92), 3),   # Ruộng Bậc Thang: bờ đông, ruộng bậc thang vàng, chòi tranh
       (50, (1150, 705), (210, 110), (204, 102, 72), 4),   # Vách Kim Cương: đông nam, vách đá đỏ gắn kim cương xanh
       (60, (955, 470), (150, 110), (214, 128, 84), 4),    # Lò Gốm Đất Nung: đồi trong phía đông cao nguyên, lò gốm, chum
       (70, (700, 380), (230, 165), (222, 182, 112), 4)]   # Kim Tự Viện: cao nguyên giữa đảo, kim tự tháp bậc (lớn nhất)
C = {r[0]: r[1] for r in REG}
# điểm dẫn: chặng 9 cờ uốn lượn cho đủ dài; 60 → 70 leo xoắn quanh sườn núi lửa
PATH = [(770, 880), (770, 810), C[1],
        (640, 760), (520, 740), C[5],
        (330, 640), (240, 560), C[10],
        (200, 350), (250, 270), C[15],
        (450, 160), (540, 130), C[20],
        (760, 160), (800, 265), (880, 295), (945, 235), (960, 170), C[30],
        (1140, 185), (1170, 295), (1250, 305), (1290, 225), (1375, 270), C[40],
        (1400, 480), (1330, 560), (1380, 640), (1300, 720), C[50],
        (1040, 720), (1000, 640), (1100, 580), (1090, 500), C[60],
        (900, 560), (760, 590), (560, 560), (470, 470), (520, 330), (640, 300), C[70]]


def layout():
    im = Image.new("RGB", (W, H), (120, 180, 220))
    d = ImageDraw.Draw(im)
    d.polygon(blob(768, 445, 745, 405, 2.1), fill=(70, 66, 70))
    d.polygon(blob(768, 445, 725, 388, 2.1), fill=(150, 120, 100))
    for st, (x, y), (rx, ry), col, s in REG:
        d.polygon(blob(x, y + 5, rx, ry, st * .37, p=.9), fill=col)
    # hẻm núi đỏ khô từ cao nguyên ra biển, ngăn vùng bến (1) với vách kim cương (50): không có đường nào qua, trừ cầu gỗ chặng 60 → 70
    canyon = catmull([(760, 470), (800, 560), (880, 640), (940, 760), (960, 864)])
    d.line(canyon, fill=(120, 50, 30), width=26, joint="curve")
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
    im.save(os.path.join(OUT, "layout_tho.png"))
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
