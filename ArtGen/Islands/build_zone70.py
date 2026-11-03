# Bản đồ dài đảo Thủy 70 ải: dựng ảnh bố cục và gói gửi GPT (ArtGen/Islands/PROMPTS.md, mục "Đảo Thủy 70 ải").
# Bản đồ ghép từ 3 ảnh GPT 1024 x 1536 xếp dọc; hai đoạn kề chồng nhau OV px: đoạn trên vẽ lại dải đỉnh của đoạn dưới ở đáy
# ảnh (bố cục của nó dán sẵn dải đó) để ghép liền. Cả bản đồ 1024 x 4288. Màn đảo hiện bản đồ rộng 1,27 màn như đảo 8 ải, nên
# chỉ thấy x 0,11..0,89 và 1 px ảnh thành DISPLAY px khung 1080.
# - Đường: dải cát rộng lượn chữ S, luôn đi lên (mỗi đường ngang cắt đường đúng một lần), từ mép nước ở đáy lên bãi đấu boss ở
#   đỉnh. Mỗi chặng là một nửa chữ S (một nửa sóng sin) từ ải tướng này tới ải tướng sau, lần lượt lượn trái, phải; nên mọi ải
#   tướng nằm ở chỗ đường cắt qua giữa bản đồ, hai bên còn trống cho địa danh.
# - 10 ải tướng: độ cao đặt tay (STAGE_Y) để địa danh tránh dải nối; biên độ từng chặng tính ngược từ chiều dài đường cần cho số
#   ải xen giữa của chặng (chấm ải cách GAP px khung 1080, cỡ bệ như ZoneScene, ZoneNode). Mỗi ải tướng là bãi tròn trên đường;
#   địa danh của chặng đứng sát bên, không chạm dải nối giữa hai đoạn.
# - Nước: biển ở đáy và đỉnh, suối chạy ngang qua cầu (chặng 3), vịnh hải đăng (5), hồ thác và suối (6), đầm (7), hồ (8),
#   hồ xoáy (10).
# Ghi: ArtGen/guides/L_zone70_thuy.png (bố cục cả bản đồ), ArtGen/guides/zone70_thuy.json (đường, ải tướng, địa danh; toạ độ
# 0..1 của bản đồ ghép, y từ trên), gói ArtGen/Islands/gui_gpt/zone_thuy_70/ (luot_k.txt, bo_cuc_k.png, HUONG_DAN.md).
# Chạy: py -3 -I ArtGen/Islands/build_zone70.py
# Duyệt đoạn k GPT đã lưu: py -3 -I ArtGen/Islands/build_zone70.py --duyet k [ảnh] (mặc định ảnh mới nhất zones/thuy70/tai_ve/doan_k*.png):
# lưu zones/thuy70/doan_k.png rồi dựng lại gói
# (có đoạn k thì có file prompt lượt k+1 và bố cục đoạn k+1 dán dải đỉnh của đoạn k). Mỗi lượt một file prompt luot_k.txt ghi
# đường dẫn đầy đủ của ảnh mẫu và chỗ GPT lưu ảnh: người dùng chỉ gửi GPT đường dẫn file đó.
import argparse
import bisect
import contextlib
import io
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/Islands
GUIDES = HERE.parent / "guides"
PACK = HERE / "gui_gpt" / "zone_thuy_70"
WORK = HERE / "zones" / "thuy70"  # tai_ve/: ảnh GPT trả về; doan_k.png: đoạn đã duyệt
REFS = [HERE / "refs" / "world_style.png", HERE / "zones" / "zone_thuy.png"]  # ảnh mẫu nét vẽ, đảo Thủy 8 ải
ASSETS = HERE.parent.parent / "Assets"
ART_OUT = ASSETS / "03 Art" / "Islands"  # zone_thuy.png, island_anim.json (khoá zone_thuy)
ZONES_JSON = ASSETS / "02 Data" / "Json" / "zones.json"  # đảo thuy: nodes, path, stops, plates

W, SH, NSEG, OV = 1024, 1536, 3, 160
H = SH * NSEG - OV * (NSEG - 1)
DISPLAY = 1080 * 1.27 / W
EDGE = 100  # địa danh nằm trong x EDGE..W-EDGE (màn hẹp cắt hai dải ngoài)
ROAD_W = 104
STREAM_W = 46
START = 170  # quãng từ đầu đường (dưới nước) tới ải 1 trên bãi cát
BEACH_Y, SEA_Y, TOP_SEA_Y = H - 250, H - 72, 56

# ải tướng và cỡ bệ (ZoneNode.Width, HeroHeight; chỗ chừa như ZoneScene.TrailLayout, bệ cỡ thật). Chặng ngắn (ải 1–19, 4–5 ải)
# giãn SHORT lần cho đoạn đáy đỡ chật địa danh.
HEADS = [1, 5, 10, 15, 20, 30, 40, 50, 60, 70]
KIND = "nnnnmmmmmb"
GAP, SHORT = 92, 1.0
# độ cao ải tướng (px từ trên; ải 1 trên bãi cát, ải 70 giữa bãi đấu boss), chặng đầu lượn sang FIRST (1 phải, -1 trái)
STAGE_Y = [H - START, H - START - 282, H - START - 564, H - START - 846, 2990, 2520, 2050, 1580, 1110, 450]
FIRST = 1
AMP_MAX = 290
NODE_W = {"n": 136, "m": 165, "b": 210}
NODE_H = {"n": 190, "m": 230, "b": 290}
CLEAR = {"n": 0.85, "m": 0.92, "b": 1.45}  # bán kính bãi trên đường, theo bề rộng đường (bệ rộng 101–157 px ảnh)

# địa danh từng chặng: tên chặng, kiểu chỗ (land xám, water xanh, bridge cầu qua suối, boss hồ xoáy sau bãi đấu), bán kính, câu cho GPT
SPOTS = {
    1: ("Bãi Vỏ Sò", "land", 100, "a beach of big pastel seashells beside the start of the road"),
    2: ("Vũng San Hô", "water", 95, "a small round tide pool full of pink and orange coral, ringed by rocks"),
    3: ("Cầu Gỗ Rêu", "bridge", 0, "the road crosses the stream on a wide mossy wooden bridge exactly as wide as the road; the bridge is "
                                  "part of the road and stays empty"),
    4: ("Làng Vỏ Ốc", "land", 105, "a little village of three snail-shell cottages with round wooden doors"),
    5: ("Ngọn Hải Đăng", "land", 95, "a white-and-red striped lighthouse on a rocky point at the inner end of the bay"),
    6: ("Thác Bạc", "land", 110, "a silver waterfall pouring from a tall rocky cliff into a round pool; the pool's stream runs off the "
                                "{edge} edge; no foam at the foot of the fall"),
    7: ("Rạn Ngọc Trai", "water", 110, "a shallow lagoon with coral rocks and a giant open clam holding a big shining pearl"),
    8: ("Hồ Gương", "water", 115, "a perfectly round, very still lake like a mirror, with pale reflections, ringed by smooth stones"),
    9: ("Đền Rùa Cổ", "land", 115, "an ancient mossy stone temple whose roof is a dome shaped like a turtle shell, with a stone turtle "
                                 "statue beside its steps"),
    10: ("Xoáy Nước Đinh Ba", "boss", 118, "the boss lair: the road ends in the big round empty arena; right behind it, a round rocky "
                                          "basin of calm deep-blue water (the whirlpool and the trident are added later)"),
}

INK = (43, 33, 24)
GROUND = (178, 222, 170)
ROAD = (246, 230, 180)
SAND = (246, 228, 176)
WATER = (70, 160, 225)
SPOT = (205, 205, 205)
BRIDGE = (150, 100, 60)

warnings = []


def warn(msg):
    warnings.append(msg)
    print("  ! " + msg)


def seg_top(k):
    """y trên của đoạn k (0 = đoạn đáy) trong bản đồ"""
    return H - SH - k * (SH - OV)


BANDS = [(seg_top(k), seg_top(k) + OV) for k in range(NSEG - 1)]  # dải nối: đỉnh đoạn k = đáy đoạn k+1


def seg_of(y):
    for k in range(NSEG):
        if y >= seg_top(k):
            return k
    return NSEG - 1


def up(k):
    return NODE_H[k] * 0.5 + 8


def down(k):
    return NODE_W[k] * 0.32 + 8


# ---------- đường ----------

def chapter_len(c):
    """chiều dài đường (px ảnh) của chặng c: chỗ bệ hai đầu và các chấm ải xen giữa"""
    k = SHORT if HEADS[c + 1] <= 20 else 1
    return (up(KIND[c]) + down(KIND[c + 1]) + (HEADS[c + 1] - HEADS[c] - 1) * GAP * k) / DISPLAY


def half_wave(amp, dy, side, y0, n=None):
    """nửa sóng sin từ (giữa, y0) lên (giữa, y0 - dy), lượn sang side với biên độ amp"""
    n = n or max(8, int(dy / 4))
    return [(W / 2 + side * amp * math.sin(math.pi * i / n), y0 - dy * i / n) for i in range(n + 1)]


def arc(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def build_road():
    """tâm đường từ mép dưới lên bãi đấu boss; trả các điểm và quãng đường của 10 ải tướng"""
    pts = [(W / 2, H), (W / 2, STAGE_Y[0])]
    stops = [START]
    side = FIRST
    for c in range(9):
        dy, need = STAGE_Y[c] - STAGE_Y[c + 1], chapter_len(c)
        if need < dy:
            warn(f"chặng {c + 1} cần {need:.0f} px đường mà cao {dy:.0f} px: hạ độ cao ải {HEADS[c + 1]}")
        lo, hi = 0.0, 600.0  # dò biên độ cho đủ chiều dài
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if arc(half_wave(mid, dy, side, STAGE_Y[c])) < need else (lo, mid)
        if lo > AMP_MAX:
            warn(f"chặng {c + 1} cần biên độ {lo:.0f} px (tối đa {AMP_MAX}): giãn độ cao hai ải {HEADS[c]}, {HEADS[c + 1]}")
        pts += half_wave(lo, dy, side, STAGE_Y[c])[1:]
        stops.append(stops[-1] + need)
        side = -side
    return pts, stops


class Road:
    def __init__(self, pts):
        self.p = pts
        self.d = [0.0]
        for a, b in zip(self.p, self.p[1:]):
            self.d.append(self.d[-1] + math.dist(a, b))
        self.length = self.d[-1]
        self.arr = self.darr = None

    def at(self, s):
        s = min(max(s, 0), self.length)
        i = max(1, bisect.bisect_left(self.d, s))
        a, b = self.p[i - 1], self.p[i]
        t = (s - self.d[i - 1]) / (self.d[i] - self.d[i - 1]) if self.d[i] > self.d[i - 1] else 0
        return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t

    def normal(self, s):
        a, b = self.at(s - 4), self.at(s + 4)
        L = math.dist(a, b) or 1
        return -(b[1] - a[1]) / L, (b[0] - a[0]) / L

    def dist(self, q, skip=None):
        if self.arr is None:
            self.arr, self.darr = np.array(self.p), np.array(self.d)
        dd = np.hypot(self.arr[:, 0] - q[0], self.arr[:, 1] - q[1])
        if skip:
            dd = dd[(self.darr < skip[0]) | (self.darr > skip[1])]
        return float(dd.min())

    def x_at(self, y):
        """x của đường ở độ cao y (đường luôn đi lên)"""
        for a, b in zip(self.p, self.p[1:]):
            if min(a[1], b[1]) <= y <= max(a[1], b[1]) and a[1] != b[1]:
                return a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1])
        return self.p[-1][0]


def in_band(y0, y1, pad=10):
    return any(y1 > b0 - pad and y0 < b1 + pad for b0, b1 in BANDS)


# ---------- chỗ địa danh, nước ----------

def free(c, r, road, clears, obstacles, bottom=False):
    x, y = c
    if x - r < EDGE or x + r > W - EDGE or y - r < TOP_SEA_Y + 20:
        return False
    if (y > SEA_Y - 30 or y + r > H - 10) if bottom else y + r > BEACH_Y:
        return False
    if in_band(y - r, y + r):
        return False
    if road.dist(c) < ROAD_W / 2 + r + 14:
        return False
    if any(math.dist(c, q) < cr + r + 6 for q, cr in clears):
        return False
    return all(math.dist(c, q) >= qr + r + 10 for q, qr in obstacles)


def candidates(road, s0, r, clears, obstacles, bottom=False, keep=14):
    """các chỗ địa danh sát đường quanh quãng s0, điểm càng nhỏ càng tốt: ưu tiên ngay cạnh bãi ải, rồi dời vào trong chặng của
    nó (về sau), cuối cùng mới dời ngược về chặng trước"""
    out = []
    for ds in range(-240, 361, 30):
        p, n = road.at(s0 + ds), road.normal(s0 + ds)
        for side in (1, -1):
            for extra in range(0, 181, 10):
                off = ROAD_W / 2 + r + 16 + extra
                c = (p[0] + side * n[0] * off, p[1] + side * n[1] * off)
                if free(c, r, road, clears, obstacles, bottom):
                    out.append((abs(ds) * (1 if ds >= 0 else 1.6) + extra * 1.5, c))
                    break
    out.sort(key=lambda t: t[0])
    return out[:keep]


def assign(cands, radius):
    """chọn mỗi địa danh một chỗ, không chồng nhau, tổng điểm nhỏ nhất (tìm nhánh cận)"""
    nums = list(cands)
    best = [1e18, None]

    def go(i, total, chosen):
        if total >= best[0]:
            return
        if i == len(nums):
            best[:] = [total, dict(chosen)]
            return
        n = nums[i]
        for score, c in cands[n]:
            if all(math.dist(c, chosen[m]) >= radius[n] + radius[m] + 18 for m in chosen):
                chosen[n] = c
                go(i + 1, total + score, chosen)
                del chosen[n]

    go(0, 0, {})
    return best[1] or {}


def wavy(a, b, amp, seed, step=12):
    """đường lượn nhẹ từ a tới b"""
    L = math.dist(a, b)
    n = max(2, int(L / step))
    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
    ph = random.Random(seed).uniform(0, 6.28)
    out = []
    for i in range(n + 1):
        t = i / n
        w = amp * math.sin(t * math.pi) * math.sin(t * 5.5 + ph)
        out.append((a[0] + (b[0] - a[0]) * t + nx * w, a[1] + (b[1] - a[1]) * t + ny * w))
    return out


def check_water(name, pts, half, road, skip=None):
    y0, y1 = min(p[1] for p in pts) - half, max(p[1] for p in pts) + half
    if in_band(y0, y1):
        warn(f"{name} chạm dải nối")
    near = min(road.dist(p, skip) for p in pts[::2])
    if near < ROAD_W / 2 + half + 10:
        warn(f"{name} sát đường ({near:.0f} px)")


def layout():
    line, stops = build_road()
    road, gap = Road(line), GAP
    pts = [road.at(s) for s in stops]
    clears = [(p, CLEAR[KIND[i]] * ROAD_W) for i, p in enumerate(pts)]
    print(f"Bản đồ {W} x {H}, dải nối {BANDS}; đường {road.length:.0f} px ảnh = {road.length * DISPLAY:.0f} px khung 1080; "
          f"chấm ải cách nhau {gap:.0f} px khung 1080 (chặng ngắn {gap * SHORT:.0f})")
    print("  ải tướng:", ", ".join(f"{HEADS[i]} ({p[0]:.0f}, {p[1]:.0f})" for i, p in enumerate(pts)))
    spots, water = {}, {"streams": [], "pools": [], "bays": []}

    # 3: suối chạy ngang từ mép trái sang mép phải, qua đường ở cầu ngay trước bãi ải 10
    sx = stops[2] - 120
    X = road.at(sx)
    stream = wavy((-40, X[1] + 70), X, 22, 3)[:-1] + wavy(X, (W + 40, X[1] - 50), 22, 4)
    check_water("suối cầu gỗ", stream, STREAM_W / 2, road, (sx - 200, sx + 200))
    water["streams"].append(stream)
    n = road.normal(sx)
    spots[3] = {"bridge": X, "dir": (n[0], n[1])}

    # hồ xoáy (10) ngay sau bãi đấu boss; các địa danh khác chọn chỗ cùng lúc, né suối và hồ xoáy
    boss = (pts[9][0], pts[9][1] - (clears[9][1] + SPOTS[10][2] - 40))
    if boss[1] - SPOTS[10][2] < TOP_SEA_Y + 10:
        warn("hồ xoáy chạm biển trên")
    obstacles = [(p, STREAM_W / 2 + 6) for p in stream[::3]] + [(boss, SPOTS[10][2])]
    nums = [i + 1 for i in range(9) if SPOTS[i + 1][1] != "bridge"]
    radius = {n_: SPOTS[n_][2] for n_ in nums}
    cands = {n_: candidates(road, stops[n_ - 1], radius[n_], clears, obstacles, bottom=(n_ == 1)) for n_ in nums}
    for n_ in nums:
        if not cands[n_]:
            warn(f"không có chỗ cho địa danh {n_} ({SPOTS[n_][0]})")
    chosen = assign({n_: c for n_, c in cands.items() if c}, radius)
    chosen[10] = boss

    for i in range(10):
        num = i + 1
        name, kind, r, _ = SPOTS[num]
        if kind == "bridge" or num not in chosen:
            continue
        c = chosen[num]
        side = 1 if c[0] > road.x_at(c[1]) else -1
        spots[num] = {"c": c, "r": r, "kind": kind, "side": side}
        edge_x = W + 60 if side > 0 else -60
        if num == 5:  # vịnh biển từ mép cùng phía tới mũi đá hải đăng
            bay = wavy((edge_x, c[1] + 20), c, 26, 5)
            check_water("vịnh hải đăng", bay, 95, road)
            water["bays"].append(bay)
        if num == 6:  # hồ dưới chân thác, suối chảy ra mép cùng phía
            pool = (c[0] - side * r * 0.15, c[1] + r * 0.62)
            water["pools"].append((pool, r * 0.5))
            out = wavy(pool, (edge_x, pool[1] - 40), 18, 6)
            check_water("suối thác", out, STREAM_W / 2, road)
            water["streams"].append(out)
            spots[6]["edge"] = "right" if side > 0 else "left"
    for num, sp in sorted(spots.items()):
        if "c" in sp:
            c = sp["c"]
            print(f"  địa danh {num:2d} {SPOTS[num][0]}: ({c[0]:.0f}, {c[1]:.0f}) đoạn {seg_of(c[1]) + 1}, "
                  f"{'phải' if sp['side'] > 0 else 'trái'} đường")
    return road, stops, pts, gap, spots, water


# ---------- vẽ bố cục ----------

def font(size):
    for f in ("arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def hatch(d, box, base, seed, n):
    r = random.Random(seed)
    dark = tuple(max(0, c - 40) for c in base)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, L = r.uniform(x0 - 40, x1), r.uniform(y0, y1 + 40), r.uniform(24, 60)
        d.line([(x, y), (x + L * 0.42, y - L)], fill=dark + (r.randint(40, 90),), width=2)


def stamp_line(d, pts, w, col):
    for p in pts:
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)


def disc(d, c, r, fill, outline=INK, width=5):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=fill, outline=outline, width=width)


def dashed_circle(d, c, r, col, width=4, n=28):
    for k in range(n):
        a0, a1 = k * 2 * math.pi / n, (k + 0.55) * 2 * math.pi / n
        d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), math.degrees(a0), math.degrees(a1), fill=col, width=width)


def label(d, c, text, size=64):
    f = font(size)
    d.text(c, text, fill=INK, font=f, anchor="mm")


def shore(y, amp, k, ph):
    return [(x, y + amp * math.sin(x / k + ph)) for x in range(0, W + 1, 16)]


def draw_guide(road, pts, spots, water):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im, "RGBA")
    hatch(d, (0, 0, W, H), GROUND, 70, 9000)
    # bãi cát đáy (điểm xuất phát)
    beach = shore(BEACH_Y, 14, 70, 0)
    d.polygon(beach + [(W, H), (0, H)], fill=SAND)
    d.line(beach, fill=INK, width=4)
    # nước: vịnh, suối, hồ (viền mực trước, mặt nước sau)
    for bay in water["bays"]:
        for w, col in ((190 + 10, INK), (190, WATER)):
            stamp_line(d, bay[:-3], w, col)
    for st in water["streams"]:
        for w, col in ((STREAM_W + 10, INK), (STREAM_W, WATER)):
            stamp_line(d, st, w, col)
    # đường và bãi ải: cả lớp viền mực trước, rồi cả lớp mặt đường
    for w, col in ((ROAD_W + 10, INK), (ROAD_W, ROAD)):
        stamp_line(d, road.p, w, col)
        for i, p in enumerate(pts):
            rad = CLEAR[KIND[i]] * ROAD_W + (5 if col == INK else 0)
            d.ellipse((p[0] - rad, p[1] - rad, p[0] + rad, p[1] + rad), fill=col)
    # biển đáy cắt ngang đầu đường; dải biển trên đỉnh
    sea = shore(SEA_Y, 10, 55, 1)
    d.polygon(sea + [(W, H), (0, H)], fill=WATER)
    d.line(sea, fill=INK, width=4)
    top = shore(TOP_SEA_Y, 12, 60, 2)
    d.polygon([(0, 0), (W, 0)] + top[::-1], fill=WATER)
    d.line(top, fill=INK, width=4)
    # cầu (chặng 3): thanh gỗ ngang mặt đường
    b = spots[3]
    (bx, by), (nx, ny) = b["bridge"], b["dir"]
    tx, ty = -ny, nx  # dọc đường
    hw, hl = ROAD_W / 2 + 18, 38
    poly = [(bx + nx * hw + tx * hl, by + ny * hw + ty * hl), (bx - nx * hw + tx * hl, by - ny * hw + ty * hl),
            (bx - nx * hw - tx * hl, by - ny * hw - ty * hl), (bx + nx * hw - tx * hl, by + ny * hw - ty * hl)]
    d.polygon(poly, fill=BRIDGE, outline=INK, width=5)
    label(d, (bx, by), "3", 52)
    # chỗ địa danh
    for num, sp in spots.items():
        if "c" not in sp:
            continue
        c, r = sp["c"], sp["r"]
        if sp["kind"] == "land":
            d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=SPOT)
            dashed_circle(d, c, r, INK)
        else:
            disc(d, c, r, WATER)
        label(d, (c[0], c[1] - (0.32 * r if num == 6 else 0)), str(num))
    # hồ dưới chân thác (6) đè lên nửa dưới chỗ thác
    for c, r in water["pools"]:
        disc(d, c, r, WATER)
    return im


# ---------- gói gửi GPT ----------

def edge_word(side):
    return "right" if side > 0 else "left"


def seg_spots(k, spots):
    out = []
    for num, sp in sorted(spots.items()):
        y = sp["c"][1] if "c" in sp else sp["bridge"][1]
        if seg_of(y) == k:
            out.append(num)
    return out


def spot_line(num, spots):
    text = SPOTS[num][3]
    if num == 6:
        text = text.format(edge=spots[6]["edge"])
    return f"{num} {text};"


def water_lines(k, spots):
    lines = []
    if k == 0:
        lines.append("the sea along the bottom edge behind a sandy beach (the journey starts at the water's edge);")
        lines.append("a stream that crosses the whole image from the left edge to the right edge and passes under the road at the bridge "
                     "of spot 3;")
        if 5 in spots:
            lines.append(f"a small bay of sea that cuts in from the {edge_word(spots[5]['side'])} edge to the rocky point of spot 5;")
        lines.append("spot 2 is a tide pool.")
    elif k == 1:
        if 6 in spots:
            lines.append(f"the round pool at the foot of the cliff of spot 6 and its stream running off the {spots[6]['edge']} edge;")
        lines.append("spot 7 is a lagoon.")
    else:
        lines.append("spot 8 is a round lake; spot 10 is a round rocky basin behind the top arena;")
        lines.append("a strip of sea along the top edge beyond the rocky northern tip of the island.")
    return "\n".join("- " + s for s in lines)


GROUND_TEXT = (
    "GROUND: no island outline on the sides: the land runs off the left and right edges. The ground is pale turquoise coloured-pencil "
    "hatching like the old Water island map, mixed with sandy patches and soft grass tufts. On both sides of the road, low raised "
    "terraces with short cliff faces (top in the ground colour, side in darker hatching) give the map depth. Clusters of palm trees, "
    "round tropical bushes, big ferns and grey rocks frame the road edges closely. Small props along the road edges: big shells, "
    "crates, fishing nets on poles, a beached rowboat, a wooden signpost without writing, little lanterns. Dense, but every tree, rock "
    "and prop is a chunky doodle with a clear silhouette; no tiny noisy details, no 3D, no realistic rendering.")

ROAD_TEXT = (
    "THE ROAD (the most important thing): a wide pale-sand road with a wobbly ink edge and light pencil hatching, about 104 px wide as "
    "in the sketch, winding up in big S curves. Where the sketch has a round widening, the road opens into a round clearing of the same "
    "sand. Keep the road and the clearings completely EMPTY: no rocks, no grass, no props, no circles, no markers on them; the game "
    "places the stage markers and the creatures there.")

CODES = ("The sketch is only a colour-coded plan: light green = ground, pale sand with an ink edge = road, blue = water, grey spot with "
         "a number = a landmark on land, blue spot with a number = a landmark in water, brown bar across the road = a bridge. Do not copy "
         "its flat colours, its numbers or its dashed outlines.")

RULES = ("Keep the road and the landmarks between x = 130 and x = 894 (narrow phones cut the outer strips); the outer strips have only "
         "ground, trees and rocks.\n"
         "Moving things are added later as animated sprites, so do NOT draw: foam splashes, breaking wave crests, a whirlpool, a trident.\n"
         "No text, no letters, no numbers, no signs with writing, no creatures, no people.")


def sketch_path(k):
    return PACK / f"bo_cuc_{k + 1}.png"


def prompt_path(k):
    return PACK / f"luot_{k + 1}.txt"


def save_path(k):
    return WORK / "tai_ve" / f"doan_{k + 1}.png"


def refs(k, spots):
    """ảnh mẫu GPT mở của lượt k: (đường dẫn, câu cho GPT, mô tả cho người dùng)"""
    if k == 0:
        return [(REFS[0], "the game's approved hand-drawn map: copy its RENDERING (wobbly dark-brown ink outlines, coloured-pencil "
                          "hatching on cream paper, chunky cute doodles), ignore its content",
                 "ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền biển xanh đặc): bản đồ sảnh vẽ tay, đảo lớn chia 5 vùng màu, viền mực nâu "
                 "hơi rung, tô chì màu gạch chéo; lấy nét, không lấy nội dung"),
                (REFS[1], "the old small map of this same Water island: copy its colours and the look of its objects (pale turquoise "
                          "hatched ground, sandy rims, grey rocks, palm trees, shells, lighthouse, waterfall); ignore its layout, its thin "
                          "path, its island outline, its dark background and its cream circles",
                 "bản đồ đảo Thủy 8 ải đang dùng (1024 × 1536, nền tối quầng xanh): đảo dọc nền ngọc lam gạch chì, đường mòn mảnh có 8 "
                 "vòng tròn kem, thác, suối, cầu gỗ, hải đăng, nhà vỏ ốc, san hô, vỏ sò, hồ tròn; lấy màu và dáng đồ vật"),
                (sketch_path(0), "the layout sketch of the image you draw now: follow it exactly",
                 "bố cục đoạn 1 (1024 × 1536, nền xanh lá nhạt): đường cát rộng lượn chữ S, bãi tròn ở mỗi ải tướng; " + seg_desc(0, spots))]
    return [(WORK / f"doan_{k}.png", f"part {k} of this map, already drawn and approved: copy its style, colours, line weight and objects "
                                     f"exactly, so all parts look like one picture",
             f"đoạn {k} đã duyệt (1024 × 1536)"),
            (sketch_path(k), f"the layout sketch of the image you draw now: follow it exactly; its bottom {OV} px strip is not a sketch "
                             f"but the top {OV} px of image 1, already painted",
             f"bố cục đoạn {k + 1} (1024 × 1536, nền xanh lá nhạt); dải {OV} px ở đáy là dải đỉnh của đoạn {k}; " + seg_desc(k, spots))]


def instructions(k, spots):
    nums = seg_spots(k, spots)
    out = save_path(k)
    head = ("Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as "
            "described under SAVE. Do not reply with text only.\n\n"
            "REFERENCE IMAGES (open each file from its full path; all are 1024 x 1536):\n")
    head += "".join(f"image {i + 1} = {path}: {text}\n" for i, (path, text, _) in enumerate(refs(k, spots)))
    head += (f"\nSAVE: save the finished image as a 1024 x 1536 PNG to\n{out}\nCreate the folder if it is missing. If that file already "
             f"exists, save it as {out.stem}_2.png, {out.stem}_3.png … in the same folder instead. Do not change, move or delete any other "
             f"file.\n\n")
    if k == 0:
        sketch = "image 3"
        what = ("WHAT THIS IS: part 1 of 3 (the bottom part) of one long vertical map of the Water island for a vertical mobile game. The "
                "player scrolls up the map from the beach at the bottom to the boss at the top. The three parts are drawn one after "
                f"another and stacked. Part 2 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px of this "
                "image plain: road, ground, a few bushes and rocks, no landmark, no water.\n\n"
                "Draw a vertical 1024 x 1536 image in the rendering of image 1 with the colours and objects of image 2; outlines and "
                "hatching as bold as in image 2.\n\n")
    else:
        sketch = "image 2"
        part = "the middle part" if k == 1 else "the top part"
        what = (f"WHAT THIS IS: part {k + 1} of 3 ({part}) of one long vertical map of the Water island for a vertical mobile game. "
                f"The player scrolls up the map from the beach at the bottom to the boss at the top; your image goes right above "
                f"image 1.\n\n"
                f"Draw a vertical 1024 x 1536 image in exactly the style of image 1.\n\n"
                f"JOIN: the bottom {OV} px of your image must show the same scene as the painted bottom strip of image 2, at the same "
                f"place: the road at the same position and width, the same ground, trees and rocks. Then continue the map upward "
                f"following the sketch, so image 1 and your image join into one picture without a seam. Where the painted strip "
                f"ends ({OV} px above the bottom edge) there must be no visible line or step: both edges of the road, the hatching, "
                f"the colours and any object crossing that height continue smoothly.\n")
        if k == 1:
            what += (f"Part 3 repeats the top {OV} px of this image as its bottom strip, so keep the top {OV} px plain: road, ground, a "
                     "few bushes and rocks, no landmark, no water.\n")
        what += "\n"
    lay = f"LAYOUT: copy {sketch} exactly: the same road path and width, the same round clearings, the same water shapes, every landmark on its numbered spot. {CODES}\n\n"
    road = ROAD_TEXT
    if k == 0:
        road += " The road starts at the water's edge on the beach at the bottom and leaves the top edge exactly where the sketch does."
    elif k == 1:
        road += " The road enters at the bottom and leaves the top edge exactly where the sketch does."
    else:
        road += " The road enters at the bottom and ends in the big round arena near the top."
    body = (f"{road}\n\n{GROUND_TEXT}\n\nWATER: deeper blue than the ground, with a wobbly ink bank, a thin sandy rim and white ripple "
            f"scribbles:\n{water_lines(k, spots)}\n\n"
            f"LANDMARKS: each stands on its numbered spot of {sketch}, right beside the road, about the size of that spot, and never "
            f"covers the road or a clearing:\n" + "\n".join("- " + spot_line(n, spots) for n in nums) + f"\n\n{RULES}\n\n"
            f"Remember: save the image to {out}\n")
    return head + what + lay + body


def ready(k):
    """lượt k có đủ ảnh mẫu chưa (lượt 2, 3 cần đoạn trước đã duyệt)"""
    return k == 0 or (WORK / f"doan_{k}.png").exists()


def build_pack(spots, guide):
    """mỗi lượt một file prompt (luot_k.txt) ghi đường dẫn ảnh mẫu và chỗ lưu; bố cục bo_cuc_k.png. Lượt 2, 3 chỉ dựng khi đoạn
    trước đã duyệt (bố cục dán dải đỉnh của đoạn đó)"""
    PACK.mkdir(parents=True, exist_ok=True)
    (WORK / "tai_ve").mkdir(parents=True, exist_ok=True)
    for k in range(NSEG):
        if not ready(k):
            continue
        crop = guide.crop((0, seg_top(k), W, seg_top(k) + SH))
        if k > 0:
            done = Image.open(WORK / f"doan_{k}.png").convert("RGB")
            crop.paste(done.crop((0, 0, W, OV)), (0, SH - OV))
        crop.save(sketch_path(k))
        prompt_path(k).write_text(instructions(k, spots), encoding="utf-8")
    (PACK / "HUONG_DAN.md").write_text(guide_md(spots), encoding="utf-8")


# ---------- hướng dẫn cho người dùng ----------

def seg_desc(k, spots):
    nums = seg_spots(k, spots)
    parts = []
    for n in nums:
        sp = spots[n]
        if n == 3:
            parts.append("thanh nâu số 3 ngang đường là cầu gỗ")
        elif sp["kind"] == "land":
            parts.append(f"chấm xám số {n} là chỗ {SPOTS[n][0]}")
        else:
            parts.append(f"chấm xanh số {n} là {SPOTS[n][0]}")
    extra = {0: "đáy là bãi cát và biển, đường bắt đầu từ mép nước; suối xanh chạy ngang từ mép trái sang mép phải, qua đường ở cầu"
                + (f"; vịnh biển ăn vào từ mép {'phải' if spots[5]['side'] > 0 else 'trái'} tới chỗ hải đăng" if 5 in spots else ""),
             1: "hồ tròn dưới chỗ thác và suối chảy ra mép " + ("phải" if spots.get(6, {}).get("edge") == "right" else "trái"),
             2: "đường kết thúc ở bãi đấu tròn lớn gần đỉnh; dải biển dọc mép trên"}[k]
    return f"{extra}; " + "; ".join(parts)


def guide_md(spots):
    p = lambda *a: str(Path(*a))
    lines = [
        "# Gói gửi GPT: bản đồ dài đảo Thủy 70 ải (`zone_thuy_70`)",
        "",
        f"Sinh bằng `{p(HERE, 'build_zone70.py')}`, đừng sửa tay (chạy lại script sẽ ghi đè). Bản đồ đảo Thủy mới cho 70 ải: một bản đồ "
        f"dọc dài ghép từ 3 ảnh GPT 1024 × 1536 (đoạn dưới, giữa, trên), cả bản đồ {W} × {H}. Đường cát rộng lượn chữ S từ bãi biển "
        f"lên bãi đấu boss, 10 bãi tròn trên đường cho 10 ải tướng, địa danh của từng chặng đứng sát đường. Không vẽ vòng tròn ải: game "
        f"đặt bệ tướng và chấm ải lên đường.",
        "",
        "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. "
        "Đoạn sau phải nối liền đoạn trước, nên làm lần lượt: GPT lưu xong thì nhắn Claude \"duyệt đoạn <k>\"; Claude soi, lưu bản "
        "duyệt và dựng file prompt của lượt sau. Nên làm cả 3 lượt trong cùng một chat để GPT giữ nét.",
        "",
        "| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |",
        "|---|---|---|---|",
    ]
    names = ("đoạn dưới", "đoạn giữa", "đoạn trên")
    for k in range(NSEG):
        nums = ", ".join(map(str, seg_spots(k, spots)))
        prompt = f"`{prompt_path(k)}`" + ("" if ready(k) else f" (chưa có: Claude dựng khi duyệt đoạn {k})")
        imgs = "; ".join(f"{i + 1} `{path}`: {desc}" + ("" if Path(path).exists() or ready(k) else " (chưa có)")
                         for i, (path, _, desc) in enumerate(refs(k, spots)))
        lines.append(f"| {k + 1}: {names[k]}, địa danh {nums} | {prompt} | {imgs} | `{save_path(k)}` |")
    lines += ["", f"Bản duyệt Claude lưu ở `{p(WORK, 'doan_<k>.png')}`. Không để ảnh vào `{p(HERE, 'inbox')}` (menu nhập ảnh sẽ "
              f"chép nguyên khổ vào game).", ""]
    lines += [
        "## Soi trước khi nhắn Claude",
        "",
        "- Đường cát rộng đúng chỗ như bố cục, mép trên (lượt 1, 2) ra đúng chỗ; mặt đường và các bãi tròn **trống**.",
        "- Địa danh đúng số, đứng sát đường, không đè lên đường.",
        "- Lượt 2, 3: dải đáy giống dải đỉnh của đoạn trước (đường cùng chỗ, cùng bề rộng).",
        f"- Lượt 1, 2: dải {OV} px trên cùng chỉ có đường, đất, bụi, đá.",
        "- Không chữ, không số, không sinh vật, người; không viền đảo ở hai bên; không xoáy nước, đinh ba, bọt sóng.",
        "",
        "## Sửa nhanh (gõ vào chat)",
        "",
        "| Lỗi | Gõ |",
        "|---|---|",
        "| Có vòng tròn, đá, cỏ trên đường | `Same image, but keep the road and the round clearings completely empty: remove everything "
        "standing on them.` |",
        "| Đường lệch bố cục hoặc hẹp lại | `Same image, but put the road exactly on the path and width of the sketch, with the same round "
        "clearings.` |",
        "| Có số, chữ | `Same image without any numbers, letters or text.` |",
        "| Có viền đảo hai bên | `Same image, but no island outline on the sides: the land runs off the left and right edges.` |",
        f"| Dải đáy không nối với đoạn trước | `Redraw it so the bottom {OV} px show exactly the same scene as the painted bottom strip of "
        "the sketch: same road position and width, same trees and rocks.` |",
        "| Quá vụn, kiểu 3D | `Too detailed and too realistic. Redraw it as a hand-drawn notebook map: pencil hatching on cream paper, "
        "wobbly ink outlines, every tree and rock a chunky doodle with a clear silhouette. Keep the same layout.` |",
        "",
    ]
    return "\n".join(lines)


# ---------- toạ độ cho game ----------

def save_json(road, stops, pts, gap, spots):
    path = [road.at(s) for s in range(0, int(road.length) + 1, 24)] + [road.p[-1]]
    stages = []
    for i, p in enumerate(pts):
        st = {"idx": HEADS[i], "x": round(p[0] / W, 4), "y": round(p[1] / H, 4), "road": round(stops[i] / road.length, 4)}
        sp = spots.get(i + 1, {})
        if "c" in sp:
            st["spot"] = [round(sp["c"][0] / W, 4), round(sp["c"][1] / H, 4), round(sp["r"] / W, 4)]
            st["spotSide"] = sp["side"]
        stages.append(st)
    data = {
        "note": "Bố cục dự kiến của bản đồ dài đảo Thủy (build_zone70.py); x, y từ 0 tới 1 theo bản đồ ghép, y từ trên. Có ảnh thật "
                "thì dò lại đường.",
        "map": [W, H], "segments": NSEG, "overlap": OV, "displayWidth": 1.27, "roadWidth": round(ROAD_W / W, 4),
        "pipGap": round(gap, 1),
        "path": [[round(x / W, 4), round(y / H, 4)] for x, y in path],
        "stages": stages,
    }
    (GUIDES / "zone70_thuy.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- ghép 3 đoạn đã duyệt ----------

SEAM_BAND, TONE_BAND = 64, 48  # số hàng phía trên mép dải nối được nắn mép đường, được chỉnh màu


def sand_mask(a):
    """mặt đường cát (tô chì vàng nhạt) trong ảnh GPT"""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 215) & (g > 190) & (b > 110) & (b < 195) & (r - b > 50)


def road_run(mask_row, cx, lo=60, hi=300):
    """đoạn cát liền gần tâm đường dự kiến cx: (mép trái, mép phải) hoặc None"""
    xs = np.flatnonzero(mask_row)
    if not len(xs):
        return None
    runs = np.split(xs, np.flatnonzero(np.diff(xs) > 3) + 1)
    best = None
    for r_ in runs:
        if lo <= r_[-1] - r_[0] <= hi and r_[0] - 20 <= cx <= r_[-1] + 20:
            if best is None or abs((r_[0] + r_[-1]) / 2 - cx) < abs((best[0] + best[1]) / 2 - cx):
                best = (r_[0], r_[-1])
    return best


def warp_row(row, tx, sx):
    """kéo một hàng ảnh: điểm tx của hàng mới lấy từ điểm sx của hàng cũ, nội suy tuyến tính"""
    src = np.interp(np.arange(W), tx, sx)
    x0 = np.floor(src).astype(int).clip(0, W - 1)
    x1 = (x0 + 1).clip(0, W - 1)
    f = (src - x0)[:, None]
    return row[x0] * (1 - f) + row[x1] * f


def fix_seam(img, seam, road):
    """mép dải nối nằm trong đoạn trên (ở trên là GPT vẽ, từ seam trở xuống là dải dán từ đoạn dưới): nắn mép đường SEAM_BAND hàng
    phía trên cho khớp mép đường ngay dưới mép dải, kéo màu TONE_BAND hàng phía trên về màu dưới mép dải, làm mềm vạch cắt"""
    mask = sand_mask(img.astype(int))
    cx = road.x_at(seam)
    below = [road_run(mask[seam + k], cx) for k in range(4)]
    below = [b for b in below if b]
    above = road_run(mask[seam - 1], cx)
    jump = None
    if below and above:
        Lb, Rb = np.mean([b[0] for b in below]), np.mean([b[1] for b in below])
        dL, dR = Lb - above[0], Rb - above[1]
        jump = (round(dL), round(dR))
        for k in range(1, SEAM_BAND + 1):
            y = seam - k
            run = road_run(mask[y], road.x_at(y))
            if not run:
                continue
            w = 1 - (k - 1) / SEAM_BAND
            L, R = run
            L2, R2 = L + dL * w, R + dR * w
            tx = [0, max(1, min(L, L2) - 80), L2, R2, min(W - 2, max(R, R2) + 80), W - 1]
            sx = [0, tx[1], L, R, tx[4], W - 1]
            if all(b > a for a, b in zip(tx, tx[1:])):
                img[y] = warp_row(img[y], tx, sx)
    # màu: lệch màu giữa hai bên mép dải (làm trơn theo bề ngang) đẩy dần vào các hàng phía trên
    diff = img[seam:seam + 4].mean(0) - img[seam - 4:seam].mean(0)
    kern = np.ones(41) / 41
    diff = np.stack([np.convolve(np.pad(diff[:, c], 20, mode="edge"), kern, mode="valid") for c in range(3)], 1)
    for k in range(1, TONE_BAND + 1):
        img[seam - k] += diff * (1 - (k - 1) / TONE_BAND)
    # vạch cắt: trộn nhẹ 4 hàng quanh mép dải
    for y in (seam - 2, seam - 1, seam, seam + 1):
        img[y] = (img[y - 1] + 2 * img[y] + img[y + 1]) / 4
    return jump


def ghep():
    """ghép doan_1..3 đã duyệt thành bản đồ W x H (zones/thuy70/zone_thuy70.png), nắn hai mép dải nối"""
    segs = [np.array(Image.open(WORK / f"doan_{k + 1}.png").convert("RGB")).astype(float) for k in range(NSEG)]
    img = np.zeros((H, W, 3))
    for k in range(NSEG - 1, -1, -1):  # đoạn trên trước; đoạn dưới bỏ dải đỉnh (trùng dải đáy của đoạn trên)
        top = seg_top(k)
        skip = 0 if k == NSEG - 1 else OV
        img[top + skip:top + SH] = segs[k][skip:]
    road = Road(build_road()[0])
    for k in range(NSEG - 1):
        seam = seg_top(k)  # mép dải dán trong đoạn k+1 = đỉnh đoạn k
        before = np.abs(img[seam] - img[seam - 1]).mean()
        jump = fix_seam(img, seam, road)
        after = np.abs(img[seam] - img[seam - 1]).mean()
        print(f"  chỗ nối y {seam}: mép đường lệch (trái, phải) {jump} px đã nắn; chênh hàng {before:.1f} -> {after:.1f}")
    out = WORK / "zone_thuy70.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    # đường thật so với đường dự kiến: cắt ngang mặt đường theo phương vuông góc, mỗi 12 px đường (cắt theo hàng ngang thì ở khúc
    # chéo dính cả mảng cát bên cạnh)
    mask = sand_mask(img.astype(int))
    ts = np.arange(-130, 131)
    dev, n_all = [], 0
    for s in np.arange(START, road.length, 12):
        n_all += 1
        p, nv = road.at(s), road.normal(s)
        xs = np.clip(np.round(p[0] + nv[0] * ts).astype(int), 0, W - 1)
        ys = np.clip(np.round(p[1] + nv[1] * ts).astype(int), 0, H - 1)
        idx = np.flatnonzero(mask[ys, xs])
        if not len(idx):
            continue
        runs = np.split(idx, np.flatnonzero(np.diff(idx) > 4) + 1)
        best = min(runs, key=lambda r: 0 if r[0] <= 130 <= r[-1] else min(abs(r[0] - 130), abs(r[-1] - 130)))
        if 60 <= best[-1] - best[0] <= 260:
            dev.append(abs((ts[best[0]] + ts[best[-1]]) / 2))
    print(f"Đã ghi {out} ({W} x {H}); tâm đường thật lệch đường dự kiến (vuông góc): TB {np.mean(dev):.1f} px, 95% dưới "
          f"{np.percentile(dev, 95):.1f} px, lớn nhất {max(dev):.1f} px ({len(dev)}/{n_all} chỗ cắt dò được)")


# ---------- xuất sang Unity ----------

def sea_alpha(a):
    """kênh alpha: biển nối với mép trên, mép dưới ảnh thành trong suốt (game có biển lặp riêng, như các đảo khác); suối, hồ,
    vịnh, dải cát và bọt bờ giữ nguyên"""
    from PIL import ImageFilter
    L = lambda m: Image.fromarray(np.where(m, 255, 0).astype("uint8")).copy()  # bản sao: ảnh dựng từ mảng chỉ đọc, tô loang không ghi được
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    blue = (b > r + 80) & (b > g)
    near = np.array(L(blue).filter(ImageFilter.MaxFilter(9))) > 0
    white = (r > 200) & (g > 200) & (b > 200) & near  # vệt sóng trắng giữa biển
    band = np.zeros(blue.shape, bool)
    band[:150] = band[-170:] = True
    m = L((blue | white) & band)
    for y in (0, m.height - 1):  # tô loang từ mép trên, mép dưới: chỉ giữ biển nối với mép
        for x in range(0, m.width, 4):
            if m.getpixel((x, y)) == 255:
                ImageDraw.floodfill(m, (x, y), 128)
    sea = L(np.array(m) == 128).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))  # lấp lỗ nhỏ
    alpha = Image.fromarray(255 - np.array(sea)).filter(ImageFilter.GaussianBlur(1.2))
    return np.array(alpha) / 255.0


def anim_spec(spots, water):
    """phần động trên ảnh (IslandAnim, khoá zone_thuy): xoáy nước và đinh ba ở hồ xoáy, bọt chân thác, lấp lánh và gợn ở hồ,
    đầm, vũng; gợn chạy dọc hai suối; sóng ngoài biển và trong vịnh. Toạ độ chia W, H; cỡ và bề rộng dòng chia W"""
    items = []
    c, r = spots[10]["c"], spots[10]["r"]
    items.append(("whirlpool", c[0], c[1], 2 * r * 0.85))
    (pc, pr) = water["pools"][0]
    items.append(("foam", pc[0], pc[1] - pr * 0.3, 70))
    for n, offs in ((8, ((-0.35, -0.2), (0.3, 0.25))), (7, ((0.0, -0.3),)), (2, ((0.2, 0.1),))):
        c, r = spots[n]["c"], spots[n]["r"]
        items += [("sparkle", c[0] + dx * r, c[1] + dy * r, 30) for dx, dy in offs]
    c, r = spots[8]["c"], spots[8]["r"]
    items.append(("ripple", c[0] + 0.15 * r, c[1] - 0.05 * r, 70))
    s5 = spots[5]["c"]
    items += [("wave", 230, H - 30, 90), ("wave", 790, H - 40, 90), ("wave", 300, 24, 80),
              ("wave", (W - 80) if spots[5]["side"] > 0 else 80, s5[1] + 10, 80)]
    rivers = []
    for st in water["streams"]:
        pts = [(min(max(x, 2), W - 2), y) for x, y in st[::3]]
        rivers.append(("stream", pts, STREAM_W))
    return {
        "items": [{"k": k, "x": round(x / W, 4), "y": round(y / H, 4), "s": round(sz / W, 4)} for k, x, y, sz in items],
        "rivers": [{"k": k, "w": round(rw / W, 4), "pts": [[round(x / W, 4), round(y / H, 4)] for x, y in pts]} for k, pts, rw in rivers],
    }


def plate_side(i, p, spots):
    """bên đặt bảng tên của ải tướng thứ i (1 phải, -1 trái; 0 = game tự chọn, cho ải boss): bên chồng ít lên địa danh hơn (vòng
    địa danh nới 40 px vì hình vẽ tràn ra ngoài); bằng nhau thì ngược phía địa danh của chặng. Bảng tên của ZoneNode: rộng 250,
    cao 86 px khung 1080, cách tâm bệ từ 50 tới 300 px, hơi cao hơn tâm bệ"""
    if HEADS[i] == HEADS[-1]:
        return 0
    k = 1 / DISPLAY
    over = {}
    for side in (1, -1):
        xs = np.linspace(p[0] + side * 50 * k, p[0] + side * 300 * k, 26)
        ys = np.linspace(p[1] - 85 * k, p[1] + 5 * k, 10)
        X, Y = np.meshgrid(xs, ys)
        hit = np.zeros(X.shape, bool)
        for sp in spots.values():
            if "c" in sp:
                hit |= np.hypot(X - sp["c"][0], Y - sp["c"][1]) < sp["r"] + 40
        over[side] = hit.mean()
    own = spots.get(i + 1, {}).get("side", 0)
    if abs(over[1] - over[-1]) < 0.02:
        return -own if own else (1 if over[1] <= over[-1] else -1)
    return 1 if over[1] < over[-1] else -1


def xuat():
    """đưa bản đồ đã ghép vào game: Assets/03 Art/Islands/zone_thuy.png (biển hai mép trong suốt), khoá zone_thuy trong
    island_anim.json, đảo thuy trong zones.json (nodes = 10 ải tướng; path = tâm đường; stops = chỗ 10 ải tướng theo tỉ lệ chiều dài
    đường; plates = bên đặt bảng tên của từng ải tướng, ngược phía địa danh, 0 = để game tự chọn). Sau đó chạy menu Unity
    PokiClash/Nhập dữ liệu."""
    src = WORK / "zone_thuy70.png"
    a = np.array(Image.open(src).convert("RGB"))
    alpha = sea_alpha(a)
    rgba = np.dstack([a, (alpha * 255).round().astype("uint8")])
    Image.fromarray(rgba, "RGBA").save(ART_OUT / "zone_thuy.png")
    print(f"Đã ghi {ART_OUT / 'zone_thuy.png'} ({W} x {H}); biển trong suốt {(alpha < 0.5).mean() * 100:.1f}% ảnh")

    with contextlib.redirect_stdout(io.StringIO()):
        road, stops, pts, gap, spots, water = layout()
    anim_path = ART_OUT / "island_anim.json"
    anim = json.loads(anim_path.read_text(encoding="utf-8"))
    anim["zone_thuy"] = anim_spec(spots, water)
    nl = "\r\n" if b"\r\n" in anim_path.read_bytes() else "\n"  # giữ kiểu xuống dòng của file (compose_islands.py ghi)
    anim_path.write_text(json.dumps(anim, ensure_ascii=False, indent=1), encoding="utf-8", newline=nl)
    print(f"Đã ghi khoá zone_thuy trong {anim_path}: {len(anim['zone_thuy']['items'])} món, {len(anim['zone_thuy']['rivers'])} suối")

    data = json.loads(ZONES_JSON.read_text(encoding="utf-8"))
    z = next(z for z in data["zones"] if z["id"] == "thuy")
    path = [road.at(s) for s in np.arange(0, road.length, 32)] + [road.p[-1]]
    plates = [plate_side(i, p, spots) for i, p in enumerate(pts)]
    new = {}
    for k, v in z.items():  # giữ thứ tự khoá, thêm path, stops, plates ngay sau nodes
        if k in ("path", "stops", "plates"):
            continue
        new[k] = v
        if k == "nodes":
            new["nodes"] = [[round(x / W, 4), round(y / H, 4)] for x, y in pts]
            new["path"] = [[round(x / W, 4), round(y / H, 4)] for x, y in path]
            new["stops"] = [round(s / road.length, 5) for s in stops]
            new["plates"] = plates
    data["zones"][data["zones"].index(z)] = new
    ZONES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Đã ghi đảo thuy trong {ZONES_JSON}: 10 ải tướng, đường {len(path)} điểm, bảng tên {plates}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="K [ANH]",
                    help="lưu đoạn K (1..3) GPT trả về (mặc định ảnh mới nhất tai_ve/doan_K*.png) rồi dựng lại gói")
    ap.add_argument("--ghep", action="store_true", help="ghép 3 đoạn đã duyệt thành zones/thuy70/zone_thuy70.png")
    ap.add_argument("--xuat", action="store_true", help="đưa bản đồ đã ghép vào Assets (ảnh, phần động, zones.json)")
    a = ap.parse_args()
    if a.ghep:
        ghep()
        return
    if a.xuat:
        xuat()
        return
    if a.duyet:
        k = int(a.duyet[0])
        if len(a.duyet) > 1:
            src = Path(a.duyet[1])
        else:
            found = sorted((WORK / "tai_ve").glob(f"doan_{k}*.png"), key=lambda f: f.stat().st_mtime)
            if not found:
                sys.exit(f"Không thấy ảnh doan_{k}*.png trong {WORK / 'tai_ve'}")
            src = found[-1]
        print(f"Duyệt đoạn {k}: {src}")
        im = Image.open(src).convert("RGB")
        if im.size != (W, SH):
            print(f"  ! ảnh {im.size[0]} x {im.size[1]}, đưa về {W} x {SH}")
            im = im.resize((W, SH), Image.LANCZOS)
        WORK.mkdir(parents=True, exist_ok=True)
        im.save(WORK / f"doan_{k}.png")
        print(f"Đã lưu {WORK / f'doan_{k}.png'}")
    road, stops, pts, gap, spots, water = layout()
    guide = draw_guide(road, pts, spots, water)
    GUIDES.mkdir(exist_ok=True)
    guide.save(GUIDES / "L_zone70_thuy.png")
    save_json(road, stops, pts, gap, spots)
    build_pack(spots, guide)
    print(f"Đã ghi {GUIDES / 'L_zone70_thuy.png'}, {GUIDES / 'zone70_thuy.json'}, gói {PACK}")
    if warnings:
        print(f"{len(warnings)} cảnh báo, xem trên")


if __name__ == "__main__":
    main()
