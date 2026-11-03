# Ghép ảnh đảo cho game từ các đảo gen rời (ArtGen/Islands/pieces/isle_*.png), ghi vào Assets/03 Art/Islands:
# - world.png (khung sảnh 1080 x 1920 cộng lề MARGIN mỗi phía, trong suốt ngoài bờ): đảo lớn của sảnh, kiểu ghép hình;
#   sảnh kéo được nên khối đất phải nằm trọn trong ảnh, ngoài lề là mây (Unity). Mỗi vùng là một đốm đất (tâm, bán kính);
#   đất liền = hợp các đốm, bo tròn, bờ rung nhiều tầng; ranh giới vùng = tâm gần nhất trên toạ độ đã uốn (cong như vẽ tay);
#   ruột vùng = phần đất bên trong của đảo gen tương ứng, chỗ không phủ tới lót bút chì cùng màu; bờ chung vẽ lại (rìa cát,
#   viền mực, bọt, bóng), đá ven bờ, đảo đá ngoài khơi, lối nét đứt từ làng vào từng vùng, 4 bãi tròn cho công trình.
# - sea_tile.png: biển lặp (SEA_Tile đã làm liền mép), game lát dưới cả sảnh và màn đảo hệ.
# - zone_<hệ>.png (trong suốt ngoài bờ): bản đồ đảo hệ. Có bản đồ gen (ArtGen/Islands/zones/zone_<hệ>.png: đảo dọc, đường đi lên,
#   mỗi ải một vòng tròn kem) thì cắt sát đảo, chừa lề ngang để đảo chiếm ISLE_W bề ngang ảnh (màn đảo hiện ảnh rộng 1,27 màn,
#   nên đảo vừa kín màn), dò các vòng tròn làm toạ độ ải theo thứ tự từ dưới lên (đếm vòng là số ải: muốn 12 ải thì gen 12 vòng).
#   Chưa có thì dựng tạm: đảo gen của sảnh phóng 1,25 lần, thêm đường cát qua ZONE_NODES.
#   Toạ độ ải (tỉ lệ trên ảnh) ghi vào ArtGen/guides/zone_nodes.json để chép vào ZONES[].nodes của bản web.
# Thêm vùng mới cho sảnh: gen đảo theo mẫu W (PROMPTS.md), thêm một dòng vào REGIONS, chạy lại.
# Chạy từ thư mục PokiWar: py -3 -I ArtGen/Islands/compose_islands.py [thư mục ảnh xem trước]
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIECES = HERE / "pieces"
ART = ROOT / "Assets/03 Art/Islands"
INK = np.array([43, 33, 24], np.float32)
SAND = (248, 228, 172)
SAND_DARK = (222, 192, 128)
ROCK = (150, 150, 156)

# ---------- sảnh ----------
FW, FH = 1080, 1920  # khung sảnh (màn); mọi toạ độ dưới đây tính theo khung này
MARGIN = 200  # lề quanh khung trong ảnh (prefab sảnh dựng lớp ảnh to hơn khung đúng chừng này)
W, H = FW + 2 * MARGIN, FH + 2 * MARGIN
# vùng: ảnh, tâm x, y, bán kính đất (khung 1080 x 1920)
REGIONS = [
    ("isle_hoa", 540, 300, 330),
    ("isle_moc", 230, 590, 340),
    ("isle_kim", 850, 590, 340),
    ("isle_thuy", 245, 1250, 360),
    ("isle_tho", 830, 1255, 360),
]
PLAZA = ("isle_lang", 540, 845, 112)  # quảng trường làng: ảnh, tâm, bán kính
PLAZA_LAND = 260
# 4 công trình (chỗ trong prefab sảnh: Trang trại, Đền Huy Hiệu, Hang Tiềm Năng, Cây bi): đất nền và bãi tròn nét đứt
BUILD_SPOTS = [(250, 908), (830, 908), (540, 1140), (250, 1138)]
SCALE = 0.82  # cỡ dán ảnh vùng (ảnh 1024)
RIM = 26  # bề rộng rìa cát trung bình

# ---------- bản đồ đảo hệ ----------
ZONE_MAPS = HERE / "zones"
# đảo có bản đồ dài riêng (build_zone70.py --xuat ghi zone_<hệ>.png, khoá zone_<hệ> trong island_anim.json và đường trong zones.json):
# script này không đè ảnh, phần động và toạ độ ải của đảo đó
LONG_MAPS = {"thuy": HERE / "zones" / "thuy70" / "zone_thuy70.png"}
ISLE_W = 0.77  # đảo chiếm 77% bề ngang ảnh bản đồ (màn thấy 1080 / 1372 = 79% giữa)
ZW, ZH, ZS = 1372, 1500, 1.25  # bản đồ dựng tạm: khổ ảnh, độ phóng đảo gen
# 8 ải theo thứ tự tên ải trong dữ liệu, toạ độ trên ảnh đảo gen 1024 (né landmark; ải 8 cạnh hang boss)
ZONE_NODES = {
    "thuy": [(480, 800), (760, 690), (600, 620), (390, 560), (400, 390), (560, 300), (800, 390), (610, 445)],
    "hoa": [(520, 845), (700, 770), (560, 700), (370, 700), (230, 610), (420, 600), (620, 610), (490, 505)],
    "kim": [(500, 860), (700, 790), (540, 710), (360, 720), (200, 650), (180, 540), (330, 630), (490, 610)],
    "moc": [(480, 860), (660, 800), (500, 745), (330, 720), (345, 610), (470, 600), (620, 640), (545, 520)],
    "tho": [(520, 860), (300, 760), (250, 620), (440, 620), (620, 700), (600, 520), (330, 370), (510, 420)],
}
ROAD = {"thuy": (246, 230, 180), "hoa": (205, 188, 170), "kim": (226, 224, 216), "moc": (226, 204, 152), "tho": (246, 232, 190)}

rng = np.random.default_rng(3)


def fbm(h, w, scale, seed, octaves=3):
    """nhiễu mượt nhiều tầng, trong khoảng -1..1"""
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        s = scale / (2 ** o)
        gh, gw = max(2, int(h / s) + 3), max(2, int(w / s) + 3)
        g = np.random.default_rng(seed * 31 + o).normal(0, 1, (gh, gw)).astype(np.float32)
        g = ndi.gaussian_filter(g, 0.8)
        out += amp * np.array(Image.fromarray(g).resize((w, h), Image.BICUBIC))
        tot += amp
        amp *= 0.5
    out /= tot
    return out / (np.abs(out).max() + 1e-6)


def hatch(size, base, dark, seed, density, alpha=90, slope=2.2, ss=2):
    """mảng tô bút chì: màu nền + nét gạch chéo mềm"""
    w, h = size[0] * ss, size[1] * ss
    im = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(im, "RGBA")
    r = random.Random(seed)
    light = tuple(min(255, c + 26) for c in base)
    for _ in range(density):
        x, y = r.uniform(-60 * ss, w), r.uniform(-60 * ss, h)
        L = r.uniform(26, 70) * ss
        col = (dark if r.random() < 0.45 else light) + (r.randint(alpha // 3, alpha),)
        dx = L / math.sqrt(1 + slope * slope)
        d.line([(x, y), (x + dx, y - dx * slope)], fill=col, width=r.choice([2, 3, 3, 4]) * ss // 2)
    return np.array(im.resize(size, Image.LANCZOS), np.float32)


def disc(h, w, cx, cy, r):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return np.hypot(xx - cx, yy - cy) < r


def piece_interior(name):
    """ảnh đảo gen: RGBA, mặt nạ ruột (bỏ rìa cát và đá ven bờ), tâm của ruột"""
    im = Image.open(PIECES / f"{name}.png").convert("RGBA")
    a = np.array(im)[:, :, 3] > 128
    a = ndi.binary_fill_holes(ndi.binary_opening(a, iterations=3))
    lab, n = ndi.label(a)
    if n > 1:
        sizes = ndi.sum(a, lab, range(1, n + 1))
        a = lab == (1 + int(np.argmax(sizes)))
    inner = ndi.distance_transform_edt(a) > 0.075 * im.width
    ys, xs = np.nonzero(inner)
    return im, inner, (xs.mean(), ys.mean())


def place(im, mask, scale, ox, oy, h, w):
    """đặt ảnh (và mặt nạ) đã thu phóng lên khung h x w, góc trên trái tại (ox, oy)"""
    sw, sh = int(im.width * scale), int(im.height * scale)
    rgba = np.array(im.convert("RGBA").resize((sw, sh), Image.LANCZOS), np.float32)
    m = np.array(Image.fromarray(mask.astype(np.uint8) * 255).resize((sw, sh), Image.BILINEAR), np.float32) / 255
    out = np.zeros((h, w, 4), np.float32)
    om = np.zeros((h, w), np.float32)
    x0, y0 = int(round(ox)), int(round(oy))
    sx0, sy0, dx0, dy0 = max(0, -x0), max(0, -y0), max(0, x0), max(0, y0)
    cw, ch = min(sw - sx0, w - dx0), min(sh - sy0, h - dy0)
    if cw > 0 and ch > 0:
        out[dy0:dy0 + ch, dx0:dx0 + cw] = rgba[sy0:sy0 + ch, sx0:sx0 + cw]
        om[dy0:dy0 + ch, dx0:dx0 + cw] = m[sy0:sy0 + ch, sx0:sx0 + cw]
    return out, om


def rock(d, x, y, s, r):
    """đá vẽ tay: khối xám viền mực, mảng tối bên dưới phải, chấm sáng"""
    pts = [(x + s * (1 + r.uniform(-0.18, 0.18)) * math.cos(t), y + s * 0.78 * (1 + r.uniform(-0.18, 0.18)) * math.sin(t))
           for t in [k * math.pi / 5 for k in range(10)]]
    d.polygon(pts, fill=ROCK + (255,))
    d.polygon([(x - s * 0.2, y + s * 0.1), (x + s * 0.9, y), (x + s * 0.7, y + s * 0.7), (x - s * 0.1, y + s * 0.75)], fill=(110, 110, 118, 255))
    d.line(pts + [pts[0]], fill=tuple(int(v) for v in INK) + (255,), width=max(3, int(s * 0.16)))
    d.ellipse((x - s * 0.45, y - s * 0.45, x - s * 0.15, y - s * 0.25), fill=(205, 205, 210, 255))


def dashed(d, pts, color, width, dash=16, gap=11):
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if (acc % (dash + gap)) < dash:
            d.line([a, b], fill=color, width=width)
        acc += seg


def bezier(a, b, bend, n=40):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = -(b[1] - a[1]), b[0] - a[0]
    l = math.hypot(nx, ny) or 1
    c = (mx + nx / l * bend, my + ny / l * bend)
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1])
            for t in [k / n for k in range(n + 1)]]


def coast(img, alpha, land, seed, rim=RIM):
    """bờ chung quanh mặt nạ đất: rìa cát (rộng rung), viền mực trong và ngoài, bọt, bóng dưới; ngoài bờ trong suốt"""
    h, w = land.shape
    d_in = ndi.distance_transform_edt(land)
    d_out = ndi.distance_transform_edt(~land)
    rim_w = rim + 9 * fbm(h, w, 120, seed + 5)
    shadow = np.roll(land, 14, axis=0) & ~land
    alpha[shadow] = np.maximum(alpha[shadow], 0.22)
    img[shadow] = np.array([20, 70, 90])
    sand = hatch((w, h), SAND, SAND_DARK, seed + 7, int(w * h / 230), 70)
    band = land & (d_in < rim_w)
    img[band] = sand[band]
    foam = (~land) & (d_out > 5) & (d_out < 11)
    img[foam] = [248, 252, 255]
    alpha[foam] = 0.9
    blue = (~land) & (d_out >= 11) & (d_out < 14)
    img[blue] = [110, 200, 235]
    alpha[blue] = 0.85
    ink = ((~land) & (d_out <= 3.2)) | (land & (d_in > rim_w) & (d_in < rim_w + 3.4))
    img[ink] = INK
    alpha[ink | land] = 1.0


WORLD = {"place": {}}  # world() ghi lại: chỗ dán từng đảo gen, nhãn vùng, mặt nạ đất (để đặt phần động)


def world(preview):
    global REGIONS, PLAZA, BUILD_SPOTS
    M = MARGIN  # chuyển toạ độ khung sang toạ độ ảnh có lề
    REGIONS = [(n, x + M, y + M, r) for n, x, y, r in REGIONS]
    PLAZA = (PLAZA[0], PLAZA[1] + M, PLAZA[2] + M, PLAZA[3])
    BUILD_SPOTS = [(x + M, y + M) for x, y in BUILD_SPOTS]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # đất: hợp các đốm, bo tròn, rồi rung bờ nhiều tầng trên trường khoảng cách
    blobs = np.zeros((H, W), np.float32)
    for i, (_, cx, cy, r) in enumerate(REGIONS):
        blobs = np.maximum(blobs, disc(H, W, cx, cy, r))
    blobs = np.maximum(blobs, disc(H, W, PLAZA[1], PLAZA[2], PLAZA_LAND))
    for bx, by in BUILD_SPOTS:
        blobs = np.maximum(blobs, disc(H, W, bx, by, 150))
    smooth = ndi.gaussian_filter(blobs, 75)  # bo mềm chỗ nối: cả khối thành một dáng đảo, không lộ từng đốm tròn
    sdf = ndi.distance_transform_edt(smooth > 0.42) - ndi.distance_transform_edt(smooth <= 0.42)
    # bờ rung ba tầng (fbm chuẩn hoá theo cực đại nên biên độ thật khoảng 40%): vịnh và mũi đất, khúc lượn, răng cưa
    land = (sdf + 110 * fbm(H, W, 300, 11) + 45 * fbm(H, W, 90, 12) + 14 * fbm(H, W, 28, 13)) > 0
    land = ndi.binary_fill_holes(ndi.binary_opening(land, iterations=2))
    # chia vùng trên toạ độ đã uốn: ranh giới cong như vẽ tay
    wx, wy = 75 * fbm(H, W, 260, 21), 75 * fbm(H, W, 260, 22)
    score = [np.hypot(xx + wx - cx, yy + wy - cy) / r for (_, cx, cy, r) in REGIONS]
    label = np.argmin(np.stack(score), axis=0)
    _, px, py, pr = PLAZA
    plaza = disc(H, W, px, py, pr)
    label[plaza] = len(REGIONS)
    label[~land] = -1

    img = np.zeros((H, W, 3), np.float32)
    alpha = np.zeros((H, W), np.float32)
    for i, (name, cx, cy, r) in enumerate(list(REGIONS) + [PLAZA]):
        cell = label == i
        if not cell.any():
            continue
        im, inner, (icx, icy) = piece_interior(name)
        base = np.median(np.array(im.convert("RGB"))[inner], axis=0)
        under = hatch((W, H), tuple(int(v) for v in base), tuple(max(0, int(v) - 45) for v in base), 50 + i, 14000)
        img[cell] = under[cell]
        if i == len(REGIONS):  # quảng trường: tâm vòng đá (màu kem) vào tâm làng
            rgb = np.array(im.convert("RGB"), np.float32)
            stone = ndi.binary_opening(inner & (np.abs(rgb - [236, 222, 186]).sum(axis=2) < 70), iterations=4)
            sy, sx = np.nonzero(stone)
            icx, icy = sx.mean(), sy.mean()
            scale = (r * 0.92) / math.sqrt(stone.sum() / math.pi)
        else:
            scale = SCALE
        prgba, pm = place(im, inner, scale, cx - icx * scale, cy - icy * scale, H, W)
        WORLD["place"][name] = (i, cx, cy, icx, icy, scale)
        pm = ndi.gaussian_filter(pm, 2) * cell
        img = img * (1 - pm[..., None]) + prgba[..., :3] * pm[..., None]

    coast(img, alpha, land, 30)
    WORLD["label"], WORLD["land"] = label, land
    # ranh giới vùng và vòng làng
    edge = np.zeros_like(land)
    for dy, dx in ((1, 0), (0, 1)):
        edge |= (label != np.roll(np.roll(label, dy, 0), dx, 1)) & land & np.roll(np.roll(land, dy, 0), dx, 1)
    edge = ndi.binary_dilation(edge, iterations=2) & (ndi.distance_transform_edt(land) > 2)
    img[edge] = INK
    img += rng.normal(0, 5, (H, W, 1))

    out = Image.fromarray(np.dstack([np.clip(img, 0, 255), alpha * 255]).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(out, "RGBA")
    r = random.Random(4)
    ink = tuple(int(v) for v in INK)
    # lối nét đứt từ làng vào từng vùng
    for i, (_, cx, cy, _) in enumerate(REGIONS):
        a = (px + (cx - px) * pr / math.dist((px, py), (cx, cy)), py + (cy - py) * pr / math.dist((px, py), (cx, cy)))
        b = (px + (cx - px) * 0.62, py + (cy - py) * 0.62)
        dashed(d, bezier(a, b, r.choice((-1, 1)) * 30), ink + (200,), 5)
    # bãi tròn nét đứt cho công trình
    for bx, by in BUILD_SPOTS:
        pts = [(bx + 70 * math.cos(t), by + 62 * math.sin(t)) for t in [k * math.pi / 40 for k in range(81)]]
        d.polygon(pts, fill=(196, 232, 150, 255))
        for k in range(14):
            gx, gy = bx + r.uniform(-48, 48), by + r.uniform(-38, 38)
            d.line([(gx, gy), (gx + 6, gy - 14)], fill=(96, 168, 70, 200), width=3)
        dashed(d, pts, ink + (255,), 5, 12, 9)
    # đá ven bờ và đảo đá ngoài khơi
    dist_out = ndi.distance_transform_edt(~land)
    ring = np.argwhere((dist_out > 2) & (dist_out < 26))
    for _ in range(26):
        y, x = ring[r.randrange(len(ring))]
        rock(d, x, y, r.uniform(14, 26), r)
    sea_far = np.argwhere((dist_out > 70) & (dist_out < 140))
    for _ in range(5):
        y, x = sea_far[r.randrange(len(sea_far))]
        if not (40 < x < W - 40 and 60 < y < H - 60):
            continue
        d.ellipse((x - 40, y - 22, x + 40, y + 24), fill=SAND + (255,), outline=ink + (255,), width=4)
        rock(d, x - 10, y - 6, 18, r)
        rock(d, x + 16, y + 2, 12, r)
    out.save(ART / "world.png")
    print("Đã ghép", ART / "world.png")
    if preview:
        sea = sea_tile()
        bg = Image.new("RGBA", (W, H))
        for y in range(0, H, sea.height):
            for x in range(0, W, sea.width):
                bg.paste(sea, (x, y))
        bg.alpha_composite(out)
        pv = ImageDraw.Draw(bg, "RGBA")
        for x, y in [(x + M, y + M) for x, y in ((540, 455), (195, 740), (865, 760), (250, 1395), (755, 1410))]:
            pv.rounded_rectangle((x - 192, y - 57, x + 192, y + 57), 14, fill=(251, 244, 226, 200), outline=ink + (255,), width=4)
        pv.rounded_rectangle((540 + M - 140, 965 + M - 45, 540 + M + 140, 965 + M + 45), 12, fill=(251, 244, 226, 200), outline=ink + (255,), width=3)
        pv.rectangle((M, M, M + FW, M + FH), outline=(255, 0, 255, 255), width=4)  # khung màn
        for x, y in BUILD_SPOTS:
            pv.rounded_rectangle((x - 105, y - 30, x + 105, y + 30), 10, fill=(251, 244, 226, 170), outline=ink + (255,), width=3)
        bg.save(Path(preview) / "world_pv.png")


def seamless(t):
    """trộn ô với bản dời nửa ô: gần mép lấy bản dời (mà giữa nó vốn liền), nên lát không lộ đường nối"""
    h, w = t.shape[:2]
    shifted = np.roll(np.roll(t, h // 2, 0), w // 2, 1)
    ey = np.minimum(np.arange(h), np.arange(h)[::-1]) / (h / 2)
    ex = np.minimum(np.arange(w), np.arange(w)[::-1]) / (w / 2)
    m = np.clip(1 - np.minimum.outer(ey, ex) / 0.35, 0, 1)[..., None]
    return t * (1 - m) + shifted * m


def sea_tile():
    t = np.array(Image.open(PIECES / "SEA_Tile.png").convert("RGB").resize((512, 512), Image.LANCZOS), np.float32)
    return Image.fromarray(np.clip(seamless(t), 0, 255).astype(np.uint8), "RGB")


def spline(pts, n=24):
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def stage_circles(a):
    """vòng tròn kem đánh dấu ải trên bản đồ gen: tâm (x, y), xếp từ dưới lên"""
    r, g, b, al = (a[..., k].astype(int) for k in range(4))
    m = (r > 236) & (g > 228) & (b > 200) & ((r - b) < 50) & (al > 200)
    m = ndi.binary_fill_holes(ndi.binary_opening(m, iterations=2))
    lab, n = ndi.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if len(xs) >= 1200 and len(xs) / (w * h) > 0.6 and 0.75 < w / h < 1.33:
            out.append((xs.mean(), ys.mean()))
    return sorted(out, key=lambda t: -t[1])


def zone_from_map(zid):
    """bản đồ gen: cắt sát đảo, chừa lề ngang, dò ải. Trả ảnh và toạ độ ải (tỉ lệ)"""
    a = np.array(Image.open(ZONE_MAPS / f"zone_{zid}.png").convert("RGBA"))
    ys, xs = np.nonzero(a[..., 3] > 20)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    crop = Image.fromarray(a[y0:y1, x0:x1])
    w = int(round(crop.width / ISLE_W))
    h = crop.height + 48
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ox, oy = (w - crop.width) // 2, 24
    canvas.alpha_composite(crop, (ox, oy))
    pts = [(x - x0 + ox, y - y0 + oy) for x, y in stage_circles(a)]
    return canvas, pts


def zones(preview):
    nodes_out = {}
    for zid, nodes in ZONE_NODES.items():
        if zid in LONG_MAPS and LONG_MAPS[zid].exists():
            print(f"zone_{zid}: bản đồ dài, bỏ qua (build_zone70.py --xuat)")
            continue
        if (ZONE_MAPS / f"zone_{zid}.png").exists():
            canvas, pts = zone_from_map(zid)
            canvas.save(ART / f"zone_{zid}.png")
            nodes_out[zid] = [[round(x / canvas.width, 3), round(y / canvas.height, 3)] for x, y in pts]
            print(f"zone_{zid}: bản đồ gen {canvas.size}, {len(pts)} ải", nodes_out[zid])
            continue
        im = Image.open(PIECES / f"isle_{zid}.png").convert("RGBA").resize((int(1024 * ZS), int(1024 * ZS)), Image.LANCZOS)
        canvas = Image.new("RGBA", (ZW, ZH), (0, 0, 0, 0))
        ox, oy = (ZW - im.width) // 2, (ZH - im.height) // 2
        canvas.alpha_composite(im, (ox, oy))
        pts = [(ox + x * ZS, oy + y * ZS) for x, y in nodes]
        # đường: mặt nạ dải tròn dọc spline, tô bút chì màu đường, viền mực ở mép
        line = spline(pts)
        mimg = Image.new("L", (ZW, ZH), 0)
        md = ImageDraw.Draw(mimg)
        for x, y in line:
            md.ellipse((x - 34, y - 34, x + 34, y + 34), fill=255)
        for k in (3, 7):  # chỗ phình cho mini boss và boss
            x, y = pts[k]
            rr = 52 if k == 3 else 62
            md.ellipse((x - rr, y - rr, x + rr, y + rr), fill=255)
        m = np.array(mimg) > 127
        edge = m & ~ndi.binary_erosion(m, iterations=5)
        fill = hatch((ZW, ZH), ROAD[zid], tuple(max(0, c - 40) for c in ROAD[zid]), 60, 2200, 80)
        arr = np.array(canvas).astype(np.float32)
        arr[m, :3] = fill[m]
        arr[edge, :3] = INK
        arr[m, 3] = 255
        canvas = Image.fromarray(arr.astype(np.uint8), "RGBA")
        canvas.save(ART / f"zone_{zid}.png")
        nodes_out[zid] = [[round(x / ZW, 3), round(y / ZH, 3)] for x, y in pts]
        print(f"zone_{zid}: 8 ải", nodes_out[zid])
        if preview:
            sea = sea_tile()
            bg = Image.new("RGBA", (ZW, ZH))
            for y in range(0, ZH, sea.height):
                for x in range(0, ZW, sea.width):
                    bg.paste(sea, (x, y))
            bg.alpha_composite(canvas)
            pv = ImageDraw.Draw(bg)
            for k, (x, y) in enumerate(pts):
                rr = 52 if k in (3, 7) else 40
                pv.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(251, 244, 226), outline=(43, 33, 24), width=5)
                pv.text((x - 4, y - 6), str(k + 1), fill=(43, 33, 24))
            bg.resize((ZW // 3, ZH // 3)).save(Path(preview) / f"zone_{zid}_pv.png")
    (ROOT / "ArtGen/guides/zone_nodes.json").write_text(json.dumps(nodes_out, indent=1), encoding="utf-8")


# ---------- bệ ải (màn đảo hệ): gò đất nhìn chéo từ trên, mặt trên màu đất của đảo, thành bên màu đất đậm ----------
PEDESTAL = {  # hệ: (mặt trên, thành bên)
    "thuy": ((236, 220, 168), (196, 160, 112)),
    "hoa": ((226, 104, 72), (118, 70, 58)),
    "kim": ((188, 194, 206), (118, 124, 140)),
    "moc": ((134, 202, 92), (150, 104, 70)),
    "tho": ((236, 190, 96), (188, 118, 70)),
}


def pedestal(top, side, boss, seed):
    """bệ vẽ tay: ảnh RGBA 320 x 200 (boss 400 x 250), mặt trên là elip, thành bên dày bên dưới, viền mực, cỏ, đá"""
    W, H = (400, 250) if boss else (320, 200)
    S = 2  # vẽ gấp đôi rồi thu nhỏ
    w, h = W * S, H * S
    cx, cy, rx, ry, depth = w / 2, h * 0.38, w * 0.45, h * 0.27, h * 0.2
    ink = tuple(int(v) for v in INK) + (255,)
    lw = 7 * S
    top_e = [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in [k * math.pi / 90 for k in range(180)]]
    lower = [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in [k * math.pi / 90 for k in range(0, 91)]]
    body = [(x, y + depth) for x, y in lower] + list(reversed(lower))
    m_side = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m_side).polygon(body, fill=255)
    m_top = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m_top).polygon(top_e, fill=255)
    arr = np.zeros((h, w, 4), np.float32)
    sh = hatch((w, h), side, tuple(max(0, c - 40) for c in side), seed, 900, 90, ss=1)
    th = hatch((w, h), top, tuple(max(0, c - 34) for c in top), seed + 1, 1100, 80, ss=1)
    ms, mt = np.array(m_side) > 127, np.array(m_top) > 127
    arr[ms, :3], arr[ms, 3] = sh[ms], 255
    arr[mt, :3], arr[mt, 3] = th[mt], 255
    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # bóng mềm dưới chân bệ
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((cx - rx * 1.02, cy + depth + ry * 0.55, cx + rx * 1.02, cy + depth + ry * 1.25), fill=(20, 60, 80, 70))
    shadow.alpha_composite(im)
    im = shadow
    d = ImageDraw.Draw(im, "RGBA")
    if boss:  # vòng vàng trong mặt trên
        d.ellipse((cx - rx * 0.78, cy - ry * 0.78, cx + rx * 0.78, cy + ry * 0.78), outline=(240, 196, 70, 255), width=6 * S)
    d.line(body + [body[0]], fill=ink, width=lw, joint="curve")
    d.line(top_e + [top_e[0]], fill=ink, width=lw, joint="curve")
    r = random.Random(seed)
    for k in range(7 if boss else 5):  # cỏ trên mép sau
        t = math.pi + r.uniform(0.15, 0.85) * math.pi
        x, y = cx + rx * 0.82 * math.cos(t), cy + ry * 0.82 * math.sin(t)
        for dx in (-6, 0, 6):
            d.line([(x + dx * S, y), (x + dx * S * 1.6, y - r.uniform(10, 18) * S)], fill=(90, 160, 66, 255), width=3 * S)
    rocks = 7 if boss else 2
    for k in range(rocks):  # đá ven mép trước (boss: cả vòng)
        t = (k / rocks) * 2 * math.pi if boss else r.uniform(0.15, 0.85) * math.pi
        x, y = cx + rx * 0.97 * math.cos(t), cy + ry * 0.97 * math.sin(t) + (depth * 0.5 if math.sin(t) > 0 else 0)
        rock(d, x, y, r.uniform(13, 18) * S, r)
    return im.resize((W, H), Image.LANCZOS)


def pedestals():
    for zid, (top, side) in PEDESTAL.items():
        for boss in (False, True):
            pedestal(top, side, boss, 70 + len(zid) + boss).save(ART / f"be_{zid}{'_boss' if boss else ''}.png")
    # vầng sáng dưới bệ ải đang đánh: elip vàng mờ dần ra mép
    g = np.zeros((160, 320), np.float32)
    yy, xx = np.mgrid[0:160, 0:320]
    d = np.hypot((xx - 160) / 158, (yy - 80) / 78)
    g = np.clip(1 - d, 0, 1) ** 1.4
    glow = np.zeros((160, 320, 4), np.uint8)
    glow[..., 0], glow[..., 1], glow[..., 2] = 255, 226, 120
    glow[..., 3] = (g * 230).astype(np.uint8)
    Image.fromarray(glow, "RGBA").save(ART / "be_glow.png")
    print("Đã vẽ bệ ải: be_<hệ>.png, be_<hệ>_boss.png, be_glow.png")


# ---------- phần động: cắt sheet A1 (inbox/ANIM_Sheet.png, lưới 4 x 4) thành Assets/03 Art/Islands/Anim/anim_<tên>.png ----------
ANIM_NAMES = ["smoke_big", "smoke_small", "flame_a", "flame_b", "embers", "gear_big", "gear_small", "bell",
              "whirlpool", "trident", "wave", "ripple", "foam", "sparkle", "leaf", "wind"]


def anim_sheet():
    sheet = Image.open(HERE / "inbox/ANIM_Sheet.png").convert("RGBA")
    out = ART / "Anim"
    out.mkdir(parents=True, exist_ok=True)
    cw, ch = sheet.width // 4, sheet.height // 4
    for i, name in enumerate(ANIM_NAMES):
        cell = sheet.crop(((i % 4) * cw, (i // 4) * ch, (i % 4 + 1) * cw, (i // 4 + 1) * ch))
        a = np.array(cell)[..., 3]
        ys, xs = np.nonzero(a > 10)
        box = (max(0, xs.min() - 4), max(0, ys.min() - 4), min(cw, xs.max() + 5), min(ch, ys.max() + 5))
        cell.crop(box).save(out / f"anim_{name}.png")
    print("Đã cắt", len(ANIM_NAMES), "ảnh phần động vào", out)


# ---------- chỗ đặt phần động (Unity: IslandAnim đọc Assets/03 Art/Islands/island_anim.json) ----------
# Mỗi món: (kiểu, x, y, cỡ) theo toạ độ ảnh gốc (đảo gen 1024 x 1024, bản đồ gen 1024 x 1536); cỡ là bề ngang ảnh động (px gốc).
# Kiểu: smoke (khói bốc), flame (lửa lật hai hình), gear / gear2 (bánh răng xoay xuôi / ngược), bell (chuông lắc),
# whirlpool (xoáy nước + đinh ba), foam (bọt phập phồng), sparkle (lấp lánh), leaf (lá rơi), wind (gió cuộn),
# ripple (gợn nước tại chỗ), wave (sóng ngoài biển). Sông (lava / stream) dò theo màu trong khung (x0, y0, x1, y1),
# đốm lửa hoặc gợn nước chạy dọc từ trên xuống; dò không ra (suối nhạt màu) thì khai báo tay danh sách điểm thay cho khung.
ISLE_ANIM = {
    "isle_hoa": {"items": [("smoke", 516, 230, 110), ("flame", 327, 367, 46), ("flame", 693, 353, 46), ("flame", 560, 547, 46),
                           ("sparkle", 516, 205, 40)],
                 "rivers": [("lava", (380, 220, 900, 760))]},
    "isle_kim": {"items": [("bell", 500, 400, 80), ("gear", 287, 492, 96), ("gear2", 703, 568, 80), ("sparkle", 500, 330, 34)],
                 "rivers": []},
    "isle_moc": {"items": [("leaf", 573, 300, 40), ("leaf", 600, 330, 34), ("foam", 433, 240, 60), ("sparkle", 727, 527, 34),
                           ("sparkle", 470, 420, 30)],
                 "rivers": [("stream", (195, 200, 520, 690))]},
    "isle_tho": {"items": [("sparkle", 507, 210, 40), ("ripple", 707, 453, 60), ("sparkle", 690, 445, 30), ("wind", 330, 560, 80)],
                 "rivers": []},
    "isle_thuy": {"items": [], "rivers": []},  # xoáy nước dò theo màu (whirl_spot)
}
ZONE_ANIM = {
    "thuy": {"items": [("whirlpool", 532, 239, 150), ("foam", 395, 513, 80), ("foam", 331, 1013, 60), ("sparkle", 439, 661, 34),
                       ("ripple", 758, 432, 70), ("sparkle", 637, 1282, 34), ("sparkle", 734, 927, 30)],
             "rivers": [("stream", (180, 520, 480, 1140))]},
    "hoa": {"items": [("smoke", 621, 100, 130), ("smoke", 387, 330, 80), ("flame", 452, 782, 60), ("flame", 315, 975, 40),
                      ("sparkle", 637, 419, 36), ("sparkle", 621, 65, 40)],
            "rivers": [("lava", (500, 110, 900, 1450))]},
    "kim": {"items": [("bell", 761, 120, 70), ("bell", 424, 700, 60), ("gear", 258, 1080, 96), ("gear2", 379, 1095, 84),
                      ("smoke", 755, 320, 70), ("sparkle", 702, 387, 34)],
            "rivers": [("stream", [(250, 500), (290, 565), (242, 629), (210, 694), (194, 758), (145, 839), (129, 903)])]},
    "moc": {"items": [("leaf", 669, 120, 40), ("leaf", 620, 170, 34), ("leaf", 720, 160, 34), ("wind", 694, 742, 90),
                      ("foam", 476, 161, 60), ("sparkle", 645, 573, 34), ("ripple", 306, 726, 70)],
            "rivers": [("stream", (150, 150, 520, 1300))]},
    "tho": {"items": [("sparkle", 492, 65, 40), ("sparkle", 723, 500, 34), ("ripple", 758, 839, 70), ("wind", 185, 903, 90),
                      ("wind", 734, 1065, 80)],
            "rivers": []},
}


def water_mask(a, kind):
    """mặt nạ dòng chảy theo màu: lava cam vàng sáng; stream xanh lam (đậm hơn nền đảo xanh ngọc)"""
    r, g, b = (a[..., k].astype(int) for k in range(3))
    al = ndi.distance_transform_edt(a[..., 3] > 200) > 50  # bỏ viền bọt và rìa cát ven bờ (cũng xanh lam)
    if kind == "lava":
        return al & (r > 230) & (g > 160) & (b < 120)
    return al & (b > 185) & (r < 150) & (b - r > 70) & (g < 205)


def river_line(a, kind, box, step=14):
    """đường giữa dòng chảy: mỗi hàng lấy tâm đoạn liền gần tâm hàng trước, từ trên xuống.
    Trả (danh sách (x, y) toạ độ ảnh, bề rộng dòng: trung vị bề ngang các đoạn đã chọn)"""
    x0, y0, x1, y1 = box
    m = ndi.binary_opening(water_mask(a, kind), iterations=1)
    m = ndi.binary_closing(m, iterations=6)  # lấp các vệt sáng trong lòng dòng chảy để đo đủ bề rộng
    pts, last, widths = [], None, []
    for y in range(y0, min(y1, m.shape[0]), step):
        xs = np.nonzero(m[y, x0:x1])[0]
        if len(xs) == 0:
            continue
        runs = [r for r in np.split(xs, np.nonzero(np.diff(xs) > 3)[0] + 1) if len(r) >= 5]
        if not runs:
            continue
        cand = [(x0 + r.mean(), len(r)) for r in runs]
        if last is None:
            cx, cw = max(cand, key=lambda c: c[1])
        else:
            cx, cw = min(cand, key=lambda c: abs(c[0] - last))
            if abs(cx - last) > 60:
                continue
        pts.append((float(cx), float(y)))
        widths.append(cw)
        last = cx
    if len(pts) < 3:
        return [], 0.0
    # làm trơn, thưa lại mỗi khoảng 36 px
    xs = ndi.gaussian_filter1d(np.array([p[0] for p in pts]), 1.5)
    out = [(float(xs[0]), pts[0][1])]
    for (x, y), sx in zip(pts[1:], xs[1:]):
        if math.dist(out[-1], (sx, y)) >= 36:
            out.append((float(sx), y))
    return out, float(np.median(widths))


def whirl_spot(a):
    """xoáy nước trên đảo Thủy: khối xanh lam đậm tròn lớn nhất"""
    r, g, b = (a[..., k].astype(int) for k in range(3))
    m = ndi.binary_opening((a[..., 3] > 200) & (b > 150) & (r < 70) & (g < 140), iterations=2)
    lab, n = ndi.label(m)
    if n == 0:
        return None
    sizes = ndi.sum(m, lab, range(1, n + 1))
    ys, xs = np.nonzero(lab == 1 + int(np.argmax(sizes)))
    return float(xs.mean()), float(ys.mean()), float(xs.max() - xs.min())


def sea_waves(alpha, count, box, seed, min_dist=60):
    """điểm sóng ngoài biển (alpha = 0), cách bờ ít nhất min_dist, trong khung box"""
    far = ndi.distance_transform_edt(alpha < 0.05)
    x0, y0, x1, y1 = box
    cand = [(x, y) for y, x in np.argwhere(far > min_dist) if x0 < x < x1 and y0 < y < y1]
    r = random.Random(seed)
    out = []
    for _ in range(count * 40):
        if not cand or len(out) >= count:
            break
        x, y = cand[r.randrange(len(cand))]
        if all(math.dist((x, y), o) > 220 for o in out):
            out.append((x, y))
    return [("wave", float(x), float(y), 90.0) for x, y in out]


def anim_entry(items, rivers, w, h):
    """chuẩn hoá về tỉ lệ ảnh: toạ độ (u, v) chia cho w, h; cỡ và bề rộng dòng chảy chia cho w"""
    return {
        "items": [{"k": k, "x": round(x / w, 4), "y": round(y / h, 4), "s": round(sz / w, 4)} for k, x, y, sz in items],
        "rivers": [{"k": k, "w": round(rw / w, 4), "pts": [[round(x / w, 4), round(y / h, 4)] for x, y in pts]}
                   for k, pts, rw in rivers if len(pts) >= 3],
    }


def anims(preview):
    data = {}
    label = WORLD["label"]

    def to_world(name, x, y):
        """toạ độ đảo gen -> ảnh world; ok khi điểm nằm trong đúng vùng của đảo đó"""
        i, cx, cy, icx, icy, sc = WORLD["place"][name]
        wx, wy = cx + (x - icx) * sc, cy + (y - icy) * sc
        ok = 0 <= int(wy) < H and 0 <= int(wx) < W and label[int(wy), int(wx)] == i
        return wx, wy, sc, ok

    items, rivers = [], []
    for name, spec in ISLE_ANIM.items():
        a = np.array(Image.open(PIECES / f"{name}.png").convert("RGBA"))
        its = list(spec["items"])
        if name == "isle_thuy":
            spot = whirl_spot(a)
            if spot:
                its.append(("whirlpool", spot[0], spot[1], spot[2] * 0.95))
        for k, x, y, sz in its:
            wx, wy, sc, ok = to_world(name, x, y)
            if ok:
                items.append((k, wx, wy, sz * sc))
        for k, box in spec["rivers"]:
            line, width = river_line(a, k, box)
            seg, best = [], []
            for wx, wy, sc, ok in [to_world(name, x, y) for x, y in line]:
                if ok:  # đoạn liền dài nhất nằm trong vùng
                    seg = seg + [(wx, wy)]
                    best = seg if len(seg) > len(best) else best
                else:
                    seg = []
            rivers.append((k, best, width * WORLD["place"][name][5]))
    alpha = np.array(Image.open(ART / "world.png"))[..., 3] / 255.0
    items += sea_waves(alpha, 7, (MARGIN - 120, MARGIN + 160, MARGIN + FW + 120, MARGIN + 1640), 5)
    data["world"] = anim_entry(items, rivers, W, H)

    # bản đồ đảo hệ: toạ độ ảnh gen -> ảnh đã cắt (cùng phép cắt của zone_from_map); đảo có bản đồ dài giữ khoá cũ trong json
    old = json.loads((ART / "island_anim.json").read_text(encoding="utf-8")) if (ART / "island_anim.json").exists() else {}
    for zid, spec in ZONE_ANIM.items():
        if zid in LONG_MAPS and LONG_MAPS[zid].exists():
            if f"zone_{zid}" in old:
                data[f"zone_{zid}"] = old[f"zone_{zid}"]
            continue
        src = ZONE_MAPS / f"zone_{zid}.png"
        if not src.exists():
            continue
        a = np.array(Image.open(src).convert("RGBA"))
        ys, xs = np.nonzero(a[..., 3] > 20)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        cw, chh = int(round((x1 - x0) / ISLE_W)), y1 - y0 + 48
        ox, oy = (cw - (x1 - x0)) // 2, 24

        def T(x, y):
            return x - x0 + ox, y - y0 + oy

        its = [(k,) + T(x, y) + (sz,) for k, x, y, sz in spec["items"]]
        rv = []
        for k, box in spec["rivers"]:
            line, width = (box, 30.0) if isinstance(box, list) else river_line(a, k, box)  # suối khai báo tay: rộng khoảng 30 px
            rv.append((k, [T(x, y) for x, y in line], width))
        zalpha = np.array(Image.open(ART / f"zone_{zid}.png"))[..., 3] / 255.0
        its += sea_waves(zalpha, 4, (0, 120, cw, chh - 60), 7, 40)
        data[f"zone_{zid}"] = anim_entry(its, rv, cw, chh)

    (ART / "island_anim.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Đã ghi chỗ đặt phần động:", ", ".join(f"{k} {len(v['items'])} món {len(v['rivers'])} sông" for k, v in data.items()))
    if preview:  # ảnh soát: khoanh món, vẽ sông lên ảnh
        for key, v in data.items():
            im = Image.open(ART / f"{key}.png").convert("RGBA")
            bg = Image.new("RGBA", im.size, (40, 120, 150, 255))
            bg.alpha_composite(im)
            d = ImageDraw.Draw(bg)
            w, h = im.size
            for rv in v["rivers"]:
                d.line([(x * w, y * h) for x, y in rv["pts"]], fill=(255, 0, 255, 255), width=max(2, int(rv["w"] * w)))
            for it in v["items"]:
                x, y, rr = it["x"] * w, it["y"] * h, max(8, it["s"] * w / 2)
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 255, 0, 255), width=4)
                d.text((x - rr, y - rr - 12), it["k"], fill=(255, 255, 0, 255))
            bg.convert("RGB").resize((w // 2, h // 2)).save(Path(preview) / f"anim_{key}.png")


if __name__ == "__main__":
    pv = sys.argv[1] if len(sys.argv) > 1 else None
    ART.mkdir(parents=True, exist_ok=True)
    sea_tile().save(ART / "sea_tile.png")
    world(pv)
    zones(pv)
    pedestals()
    anim_sheet()
    anims(pv)
