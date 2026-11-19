# Ảnh mẫu cho concept đảo Hỏa kiểu vùng đất (người dùng 2026-11-19: "làm tiếp đảo hỏa"). Theo cách đảo Mộc
# (ArtGen/Islands/land_moc/concept/make_refs_moc.py), rút kinh nghiệm Mộc ngay ở bố cục:
# - MỘT đường, không nhánh, không vòng; bệ 1 chỉ nối bến và bệ 5 (Mộc từng mọc đường 1↔50, phải gen lại);
# - chặng 9 cờ (20→30 … 60→70) đường dài, uốn lượn sẵn (Mộc phải gen thêm khúc cua tay áo cho 20→30);
# - mỗi vùng một mốc lớn, màu tương phản (tránh cả đảo một màu cam như bản đồ Hỏa cũ zone_hoa.png).
# Ra:
# - refs/heroes_hoa.png: 10 boss của 10 ải tướng (dạng đầu), số ải trên đầu;
# - refs/layout_hoa.png: bố cục 10 vùng, đường từ bến (đáy) đi vòng ngoài theo chiều kim đồng hồ (tây nam → tây → bắc → đông →
#   đông nam), rồi vào đồi hồng ngọc trong đảo và leo xoắn lên miệng núi lửa ở tim đảo (ải 70). Ảnh 1536 x 864.
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
HEROES = [(1, "quy_lava_1"), (5, "hoa_nhan_1"), (10, "kim_su_1"), (15, "nham_than_1"), (20, "rua_lua_non"),
          (30, "phap_lua_non"), (40, "quy_dao_non"), (50, "dat_nung_non"), (60, "hoa_ho_non"), (70, "nui_lua_non")]
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
    im.save(os.path.join(OUT, "heroes_hoa.png"))


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
REG = [(1, (770, 745), (210, 100), (105, 100, 108), 3),    # Bến Đá Đen: bến vào, bãi đá bazan đen
       (5, (420, 700), (200, 115), (236, 128, 62), 3),     # Suối Dung Nham: tây nam, suối dung nham, cầu đá
       (10, (195, 455), (160, 145), (150, 74, 62), 3),     # Rừng Than Hồng: bờ tây, cây cháy than đỏ
       (15, (335, 205), (190, 110), (180, 176, 170), 3),   # Sườn Núi Khói: tây bắc, lỗ phun hơi, khói
       (20, (660, 115), (190, 95), (214, 176, 92), 3),     # Lò Lửa Thiền: bắc, lò đồng lớn, thiền viện
       (30, (1040, 130), (200, 100), (120, 196, 160), 3),  # Chùa Liên Hoa: đông bắc, ao sen ngọc, chùa
       (40, (1335, 380), (160, 150), (122, 138, 166), 3),  # Lò Rèn Gai Thép: bờ đông, ống khói, đe, gai thép
       (50, (1150, 705), (210, 110), (172, 112, 206), 4),  # Rừng Lửa Ảo: đông nam, cây lửa tím
       (60, (955, 470), (150, 110), (206, 62, 84), 4),     # Hang Hồng Ngọc: đồi trong, phía đông núi lửa
       (70, (700, 380), (230, 165), (92, 54, 48), 4)]      # Miệng Núi Lửa: tim đảo (lớn nhất)
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
    # sông dung nham chảy từ núi lửa xuống biển, ngăn vùng bến (1) với rừng lửa ảo (50): không có đường nào qua
    lava = catmull([(760, 470), (800, 560), (880, 640), (940, 760), (960, 864)])
    d.line(lava, fill=(255, 140, 40), width=26, joint="curve")
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
    im.save(os.path.join(OUT, "layout_hoa.png"))
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
