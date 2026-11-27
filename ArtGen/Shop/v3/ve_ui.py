# Sprite giao diện màn cửa hàng bản 3 (người dùng 2026-11-27: "thiết kế shop như clash of critters, nền tối, gói IAP màu tươi nổi").
# Bản vẽ tay (người dùng 2026-11-27: "màn shop đẹp nhưng texture không phải kiểu vẽ tay, thêm các nét vẽ tay vào"; "cột bên trái màu trơn
# đơn điệu, trang trí thêm hình sao hoặc quái vật"): viền mực rung, dày mỏng không đều, có đoạn đi nét lặp như bút; nền tô bằng nét chì
# chéo + vân giấy (không còn mảng phẳng, không gradient trơn); tia nắng, sao nổ, caro thoi vẽ tay; cột trái nền chàm có hình vẽ tay (sao,
# lấp lánh, quái vật nhỏ, bi, trứng; tờ hình GPT 2.6 ở ArtGen/Shop/v3/hinh_cot/) lát dọc liền mép.
# Vẽ bằng PIL, không lấy hình của game khác. Các tấm xám (the_*, o_nen, o_tia, nut_gia, vien, o_mon) để code tô màu theo gói: trắng nhân
# màu thành màu đó, đen giữ đen (viền, dải tên) — nét mực vẽ màu gần đen, nét chì là độ xám nhạt hơn nền một chút.
# Chạy: py -3 -I ve_ui.py [--assets]  → out/ (xem trước) hoặc Assets/03 Art/Shop/v3/.
# Cỡ + viền 9 mảnh khớp bộ dựng Editor/ShopPageMenu.cs (assets-30 giữ): the_* 858×400 (40,110,40,40); o_nen/o_tia 276×420
# (34,104,34,34); muc_bang 858×100 (30); muc_chon 176×220 (30); nhan_gia_tri 320×74 (34,10,14,10); nut_gia(_an) 300×110 (36); vien 96×48
# (24); to_toi 300×300 (44); o_mon 128, cham_do 48, tia_xoay 256, nen_trang 96 (lát); cot_trai 190×768, vien_cot 8×128 (lát dọc).
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get("POKI_PROJ") or os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(PROJ, "Assets", "03 Art", "Shop", "v3") if "--assets" in sys.argv else os.path.join(HERE, "out")
DOODLE = os.path.join(PROJ, "ArtGen", "Shop", "v3", "hinh_cot")  # mảnh hình vẽ tay cho cột trái (cat_hinh_cot.py)
SS = 3  # vẽ to gấp 3 rồi thu cho mép mịn
INK = (22, 20, 42, 255)  # viền: xanh mực gần đen như thẻ mẫu


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def finish(im, w, h, name):
    im = im.resize((w, h), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, name + ".png"))
    print(name, w, h)


def gray_rgba(lum, alpha):
    return Image.merge("RGBA", (lum, lum, lum, alpha))


# ---------- nét tay ----------

class Wobble:
    """Độ lệch mượt theo quãng đường s (điểm ảnh cuối): tổng vài sóng sin bước dài, pha ngẫu nhiên."""

    def __init__(self, seed, amp, waves=((150, 1.0), (63, 0.55), (27, 0.25))):
        rnd = random.Random(seed)
        self.parts = [(lam, a * amp, rnd.uniform(0, 6.283)) for lam, a in waves]

    def __call__(self, s):
        return sum(a * math.sin(2 * math.pi * s / lam + ph) for lam, a, ph in self.parts)


def rr_path(x0, y0, x1, y1, r, step=1.5):
    """Điểm dọc viền chữ nhật bo góc (toạ độ cuối), theo chiều kim đồng hồ, kèm pháp tuyến hướng ra ngoài."""
    pts = []
    r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))

    def seg(ax, ay, bx, by, nx, ny):
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L / step))
        for i in range(n):
            t = i / n
            pts.append((ax + (bx - ax) * t, ay + (by - ay) * t, nx, ny))

    def arc(cx, cy, a0, a1):
        L = abs(a1 - a0) * r
        n = max(2, int(L / step))
        for i in range(n):
            a = a0 + (a1 - a0) * i / n
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r, math.cos(a), math.sin(a)))

    seg(x0 + r, y0, x1 - r, y0, 0, -1)
    arc(x1 - r, y0 + r, -math.pi / 2, 0)
    seg(x1, y0 + r, x1, y1 - r, 1, 0)
    arc(x1 - r, y1 - r, 0, math.pi / 2)
    seg(x1 - r, y1, x0 + r, y1, 0, 1)
    arc(x0 + r, y1 - r, math.pi / 2, math.pi)
    seg(x0, y1 - r, x0, y0 + r, -1, 0)
    arc(x0 + r, y0 + r, math.pi, 1.5 * math.pi)
    return pts


def poly_path(poly, step=1.5):
    """Điểm dọc đa giác kín (toạ độ cuối) kèm pháp tuyến (đa giác theo chiều kim đồng hồ trên ảnh: pháp tuyến ra ngoài)."""
    pts = []
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        L = math.hypot(bx - ax, by - ay)
        if L == 0:
            continue
        nx, ny = (by - ay) / L, -(bx - ax) / L
        k = max(1, int(L / step))
        for j in range(k):
            t = j / k
            pts.append((ax + (bx - ax) * t, ay + (by - ay) * t, nx, ny))
    return pts


def ellipse_path(cx, cy, rx, ry, step=1.5):
    n = max(12, int(2 * math.pi * max(rx, ry) / step))
    return [(cx + math.cos(2 * math.pi * i / n) * rx, cy + math.sin(2 * math.pi * i / n) * ry,
             math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]


def hand_stroke(w, h, path, width, seed, wob=1.1, var=0.22, inner_only=False, double=True):
    """Nét mực vẽ tay dọc path: tâm nét rung ±wob, bề dày đổi ±var, vài đoạn đi lặp một nét mảnh lệch ra ngoài.
    Trả (mặt nạ nét L, mặt nạ hình kín L theo mép ngoài nét) ở cỡ SS."""
    off = Wobble(seed, wob)
    thick = Wobble(seed + 7, var, ((120, 1.0), (45, 0.5)))
    dbl = Wobble(seed + 13, 1.0, ((260, 1.0), (90, 0.4)))
    outer, inner, extra_o, extra_i = [], [], [], []
    s = 0.0
    prev = None
    for (x, y, nx, ny) in path:
        if prev:
            s += math.hypot(x - prev[0], y - prev[1])
        prev = (x, y)
        c = off(s)
        wd = width * (1 + thick(s))
        # tâm nét nằm trong hình (inner_only: mép ngoài nét bám path)
        base = -wd / 2 if inner_only else 0
        cx, cy = x + nx * (c + base), y + ny * (c + base)
        outer.append(((cx + nx * wd / 2) * SS, (cy + ny * wd / 2) * SS))
        inner.append(((cx - nx * wd / 2) * SS, (cy - ny * wd / 2) * SS))
        if double:
            k = dbl(s)
            ew = width * 0.32 if k > 0.45 else 0
            ex, ey = cx + nx * (wd / 2 + 1.2), cy + ny * (wd / 2 + 1.2)
            extra_o.append(((ex + nx * ew / 2) * SS, (ey + ny * ew / 2) * SS))
            extra_i.append(((ex - nx * ew / 2) * SS, (ey - ny * ew / 2) * SS))
    shape = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(shape).polygon(outer, fill=255)
    hole = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(hole).polygon(inner, fill=255)
    ring = ImageChops.subtract(shape, hole)
    if double:
        d = ImageDraw.Draw(ring)
        for i in range(len(extra_o) - 1):
            q = [extra_o[i], extra_o[i + 1], extra_i[i + 1], extra_i[i]]
            if abs(q[0][0] - q[3][0]) + abs(q[0][1] - q[3][1]) > 0.5:
                d.polygon(q, fill=200)
    return ring, shape


def ink_layer(mask, color=INK):
    layer = Image.new("RGBA", mask.size, color)
    layer.putalpha(mask)
    return layer


def hatch(w, h, seed, spacing=7.0, drop=(6, 16), angle=-58, jitter=9, length=(16, 52), width=(1.0, 1.8), base=255):
    """Nét chì chéo: nhiều nét ngắn song song lệch góc chút ít, tối hơn nền một khoảng drop. Ảnh L cỡ SS."""
    rnd = random.Random(seed)
    im = Image.new("L", (w * SS, h * SS), base)
    d = ImageDraw.Draw(im)
    a0 = math.radians(angle)
    ux, uy = math.cos(a0), math.sin(a0)
    vx, vy = -uy, ux
    diag = math.hypot(w, h)
    rows = int(diag / spacing) + 2
    for r in range(-rows, rows):
        off = r * spacing + rnd.uniform(-spacing * 0.3, spacing * 0.3)
        t = -diag
        while t < diag:
            L = rnd.uniform(*length)
            gap = rnd.uniform(2, 14)
            a = a0 + math.radians(rnd.uniform(-jitter, jitter) * 0.3)
            px, py = w / 2 + vx * off + ux * t, h / 2 + vy * off + uy * t
            qx, qy = px + math.cos(a) * L, py + math.sin(a) * L
            if -60 < px < w + 60 and -60 < py < h + 60:
                v = base - rnd.randint(*drop)
                d.line([(px * SS, py * SS), (qx * SS, qy * SS)], fill=max(0, v), width=max(1, int(rnd.uniform(*width) * SS)))
            t += L + gap
    return im.filter(ImageFilter.GaussianBlur(SS * 0.45))


def paper(w, h, amp, seed, wrap=False):
    """Vân giấy / sáp: nhiễu mịn quanh 128 (wrap: liền mép để lát)."""
    rnd = random.Random(seed)
    sw, sh = w // 2 + 1, h // 2 + 1
    small = Image.new("L", (sw, sh))
    small.putdata([128 + int(rnd.uniform(-amp, amp)) for _ in range(sw * sh)])
    if wrap:
        big = Image.new("L", (sw * 3, sh * 3))
        for i in range(3):
            for j in range(3):
                big.paste(small, (i * sw, j * sh))
        big = big.resize((sw * 3 * 2 * SS, sh * 3 * 2 * SS), Image.BILINEAR).filter(ImageFilter.GaussianBlur(SS * 0.6))
        x0, y0 = sw * 2 * SS, sh * 2 * SS
        return big.crop((x0, y0, x0 + w * SS, y0 + h * SS))
    return small.resize((w * SS, h * SS), Image.BILINEAR).filter(ImageFilter.GaussianBlur(SS * 0.6))


def add_grain(lum, g):
    return ImageChops.add(lum, g, 1, -128)


def tex_fill(w, h, seed, level=255, spacing=7.0, drop=(6, 16), grain_amp=8, angle=-58):
    """Nền tô chì: độ sáng level, nét chì chéo + vân giấy."""
    lum = hatch(w, h, seed, spacing=spacing, drop=drop, angle=angle, base=level)
    return add_grain(lum, paper(w, h, grain_amp, seed + 1))


def vgrad(w, h, stops):
    col = Image.new("L", (1, h * SS))
    px = []
    for y in range(h * SS):
        t = y / (h * SS - 1)
        for i in range(len(stops) - 1):
            t0, v0 = stops[i]
            t1, v1 = stops[i + 1]
            if t0 <= t <= t1:
                k = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                px.append(int(v0 + (v1 - v0) * k))
                break
        else:
            px.append(stops[-1][1])
    col.putdata(px)
    return col.resize((w * SS, h * SS))


def bottom_dark(w, h, start, full, seed=77):
    # hệ số tối ở đáy: 255 (không tối) tới ~14 — dải tên của thẻ. Chuyển bằng nét chì đậm dần như tô sáp (dày dần từ start tới full),
    # dưới full tối đặc; không phải mép cứng, không phải gradient trơn
    rnd = random.Random(seed)
    m = Image.new("L", (w * SS, h * SS), 255)
    d = ImageDraw.Draw(m)
    y0, y1 = start * h, full * h
    d.rectangle([0, int(y1 * SS), w * SS, h * SS], fill=14)
    n = int(w * (y1 - y0) / 6)
    for _ in range(n):
        y = rnd.uniform(y0, y1 + 6)
        k = min(1, max(0, (y - y0) / (y1 - y0)))
        if rnd.random() > 0.15 + 0.85 * k * k:
            continue
        x = rnd.uniform(-40, w)
        L = rnd.uniform(14, 34)
        v = int(14 + (1 - k) * rnd.uniform(60, 140))
        # nét chéo thoải (như nét tô sáp), không dựng đứng kẻo giống cỏ
        d.line([(x * SS, y * SS), ((x + L * 0.82) * SS, (y - L * 0.57) * SS)], fill=v, width=int(rnd.uniform(2.0, 3.4) * SS))
    return m.filter(ImageFilter.GaussianBlur(SS * 0.5))


def diamonds_hand(w, h, size, lo, hi, seed, wrap=False):
    """Caro thoi vẽ tay: đỉnh lưới rung chung (các ô khớp nhau), ô tối tô nét chì, đường kẻ chì mảnh dọc cạnh ô."""
    rnd = random.Random(seed)
    s = size
    m = Image.new("L", (w * SS, h * SS), hi)
    d = ImageDraw.Draw(m)
    nx, ny = int(w / s) + 3, int(h / s) + 3
    jit = {}

    def V(i, j):
        key = (i % nx, j % ny) if wrap else (i, j)
        if key not in jit:
            jit[key] = (rnd.uniform(-0.07, 0.07) * s, rnd.uniform(-0.07, 0.07) * s)
        jx, jy = jit[key]
        return ((i * s / 2 + jx) * SS, (j * s / 2 + jy) * SS)

    # như bản phẳng: thoi đặc tại các điểm lưới bước s (i, j chẵn), xen kẽ kiểu bàn cờ, nửa đường chéo s/2 (các thoi chạm nhau ở đỉnh);
    # đỉnh (i, j) là điểm lưới bước s/2, rung chung
    cells = []
    for j in range(-4, int(2 * h / s) + 6, 2):
        for i in range(-4, int(2 * w / s) + 6, 2):
            if ((i // 2) + (j // 2)) % 2:
                continue
            poly = [V(i, j - 1), V(i + 1, j), V(i, j + 1), V(i - 1, j)]
            d.polygon(poly, fill=lo)
            cells.append(poly)
    # viền chì mảnh, nhạt quanh mỗi thoi đặc
    line = Image.new("L", m.size, 255)
    dl = ImageDraw.Draw(line)
    for poly in cells:
        col = 255 - rnd.randint(12, 26)
        dl.line(poly + [poly[0]], fill=col, width=max(1, int(1.3 * SS)))
    m = ImageChops.multiply(m, line.filter(ImageFilter.GaussianBlur(SS * 0.4)))
    return m


def burst_poly(cx, cy, r_in, r_out, n, rot=0.0, jitter=0.0, seed=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n
        r = (r_out if i % 2 == 0 else r_in) * (1 + rnd.uniform(-jitter, jitter))
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return pts


def rough_poly(poly, seed, amp=1.6, step=4.0):
    """Đa giác mép rung: chia nhỏ cạnh, đẩy điểm theo pháp tuyến bằng Wobble (toạ độ cuối)."""
    path = poly_path(poly, step)
    wob = Wobble(seed, amp, ((70, 1.0), (24, 0.4)))
    out, s, prev = [], 0.0, None
    for (x, y, nx, ny) in path:
        if prev:
            s += math.hypot(x - prev[0], y - prev[1])
        prev = (x, y)
        o = wob(s)
        out.append((x + nx * o, y + ny * o))
    return out


def rays(w, h, cx, cy, n, R, alpha, seed, offset=0.1, width=1.0):
    """Tia nắng vẽ tay: mỗi tia một tam giác mép rung, độ đậm có nét chì (alpha dao động)."""
    rnd = random.Random(seed)
    a = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(a)
    for i in range(0, n, 2):
        a0 = math.pi * 2 * i / n + offset + rnd.uniform(-0.02, 0.02)
        a1 = a0 + math.pi * 2 / n * width * rnd.uniform(0.85, 1.1)
        tri = [(cx, cy), (cx + math.cos(a0) * R, cy + math.sin(a0) * R), (cx + math.cos(a1) * R, cy + math.sin(a1) * R)]
        d.polygon([(x * SS, y * SS) for x, y in rough_poly(tri, seed + i, 2.2, 6)], fill=alpha)
    # nét chì trong tia: alpha ± theo nét chéo
    hv = hatch(w, h, seed + 99, spacing=9, drop=(18, 40), angle=-35)
    return ImageChops.multiply(a, hv)


# ---------- thẻ ngang (ShopCard) ----------

def card(w=858, h=400, r=28, line=7):
    path = rr_path(line / 2 + 1.5, line / 2 + 1.5, w - line / 2 - 1.5, h - line / 2 - 1.5, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 11)
    dark = bottom_dark(w, h, 0.6, 0.86)
    lum = tex_fill(w, h, 11, level=255, spacing=7, drop=(8, 18))
    lum = ImageChops.multiply(lum, dark)
    base = gray_rgba(lum, shape)
    base.alpha_composite(ink_layer(ring))
    finish(base, w, h, "the_nen")
    inner = ImageChops.subtract(shape, ring)

    # mảng phải màu phụ: cắt chéo mép rung (nét chì đậm dọc vết cắt), caro thoi vẽ tay, cùng độ tối đáy
    cut = rough_poly([(w * 0.56, -10), (w + 10, -10), (w + 10, h + 10), (w * 0.44, h + 10)], 21, 2.5, 6)
    m = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in cut], fill=255)
    m = ImageChops.multiply(m, inner)
    lum = ImageChops.multiply(diamonds_hand(w, h, 70, 214, 255, 23), tex_fill(w, h, 24, level=255, spacing=8, drop=(5, 13)))
    lum = ImageChops.multiply(lum, dark)
    # vệt chì dọc vết cắt
    edge = Image.new("L", m.size, 255)
    ImageDraw.Draw(edge).line([(x * SS, y * SS) for x, y in cut[:len(cut) // 4 + 2]], fill=150, width=int(2.4 * SS))
    lum = ImageChops.multiply(lum, edge.filter(ImageFilter.GaussianBlur(SS * 0.5)))
    finish(gray_rgba(lum, m), w, h, "the_phai")

    # sao nổ sau hình (trái): tia vẽ tay mờ + khối sao kem viền mực mảnh, mờ dần xuống dải tên
    cx, cy = 0.27 * w, 0.43 * h
    a = rays(w, h, cx, cy, 18, w * 1.2, 72, 5)
    star = rough_poly(burst_poly(cx, cy, 120, 190, 13, 0.2, 0.12, 5), 31, 1.4, 4)
    sm = Image.new("L", a.size, 0)
    ImageDraw.Draw(sm).polygon([(x * SS, y * SS) for x, y in star], fill=255)
    starfill = ImageChops.multiply(sm, hatch(w, h, 41, spacing=7, drop=(20, 45), angle=-58, base=235))
    a = ImageChops.lighter(a, starfill)
    fade = vgrad(w, h, [(0, 255), (0.55, 255), (0.85, 0), (1, 0)])
    a = ImageChops.multiply(ImageChops.multiply(a, inner), fade)
    im = gray_rgba(Image.new("L", a.size, 255), a)
    sring, _ = hand_stroke(w, h, poly_path(star, 1.5), 2.4, 51, wob=0.6, double=False)
    sring = ImageChops.multiply(ImageChops.multiply(sring, inner), fade).point(lambda v: int(v * 0.7))
    im.alpha_composite(ink_layer(sring, (22, 20, 42, 255)))
    finish(im, w, h, "the_tia")


# ---------- ô lưới (ShopTile) ----------

def tile(w=276, h=420, r=24, line=6, strip=100):
    path = rr_path(line / 2 + 1.5, line / 2 + 1.5, w - line / 2 - 1.5, h - line / 2 - 1.5, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 61)
    lum = ImageChops.multiply(tex_fill(w, h, 23, spacing=7, drop=(8, 18)), diamonds_hand(w, h, 56, 230, 255, 29))
    base = gray_rgba(lum, shape)
    # dải nút đáy: đen mực, mép trên rung, nối thẳng vào viền
    wob = Wobble(67, 2.0)
    pts = [(0, h * SS)] + [(x * SS, (h - strip + wob(x)) * SS) for x in range(0, w + 1, 3)] + [(w * SS, h * SS)]
    sm = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(sm).polygon(pts, fill=255)
    base.alpha_composite(ink_layer(ImageChops.multiply(sm, shape)))
    base.alpha_composite(ink_layer(ring))
    finish(base, w, h, "o_nen")

    inner = ImageChops.subtract(shape, ring)
    cx, cy = 0.5 * w, 0.42 * h
    a = rays(w, h, cx, cy, 16, h * 1.2, 62, 9, offset=0)
    star = rough_poly(burst_poly(cx, cy, 82, 124, 11, 0.3, 0.12, 9), 71, 1.2, 4)
    smk = Image.new("L", a.size, 0)
    ImageDraw.Draw(smk).polygon([(x * SS, y * SS) for x, y in star], fill=255)
    a = ImageChops.lighter(a, ImageChops.multiply(smk, hatch(w, h, 73, spacing=7, drop=(20, 45), base=225)))
    cut = Image.new("L", a.size, 0)
    ImageDraw.Draw(cut).rectangle([0, 0, w * SS, (h - strip) * SS], fill=255)
    a = ImageChops.multiply(ImageChops.multiply(a, inner), cut)
    im = gray_rgba(Image.new("L", a.size, 255), a)
    sring, _ = hand_stroke(w, h, poly_path(star, 1.5), 2.2, 79, wob=0.5, double=False)
    im.alpha_composite(ink_layer(ImageChops.multiply(ImageChops.multiply(sring, inner), cut).point(lambda v: int(v * 0.7))))
    finish(im, w, h, "o_tia")


# ---------- băng tiêu đề mục, ô chọn cột trái ----------

def two_tone(w, h, mask, lo, hi, seed, spacing=6):
    """Hai màu thật theo mặt nạ (255 = hi) + nét chì của mỗi màu (sáng / tối hơn chút)."""
    hv = hatch(w, h, seed, spacing=spacing, drop=(10, 26), angle=-58)
    out = []
    for c in range(3):
        a = Image.new("L", mask.size, lo[c])
        b = Image.new("L", mask.size, hi[c])
        ch = Image.composite(b, a, mask)
        # nét chì: tối hơn theo hv (nhân), cộng vân giấy
        ch = ImageChops.multiply(ch, ImageChops.add(hv, Image.new("L", hv.size, 20)))
        out.append(add_grain(ch, paper(w, h, 6, seed + c)))
    return out


def band(w=858, h=100, r=20, line=6):
    lo, hi = hexc("#7a2be8"), hexc("#8a38f6")
    path = rr_path(line / 2 + 1, line / 2 + 1, w - line / 2 - 1, h - line / 2 - 1, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 81)
    m = diamonds_hand(w, h, 44, 0, 255, 83)
    rr_, gg, bb = two_tone(w, h, m, lo, hi, 85)
    im = Image.merge("RGBA", (rr_, gg, bb, shape))
    # vệt sáng mép trên: một nét chì sáng rung (không phải dải trơn)
    hl = Image.new("L", im.size, 0)
    wob = Wobble(87, 1.2)
    pts = [((line + 10 + x) * SS, (line + 6 + wob(x)) * SS) for x in range(0, w - 2 * line - 20, 3)]
    ImageDraw.Draw(hl).line(pts, fill=120, width=int(4 * SS), joint="curve")
    hl = ImageChops.multiply(hl, shape)
    im.alpha_composite(Image.merge("RGBA", (Image.new("L", hl.size, 210), Image.new("L", hl.size, 170), Image.new("L", hl.size, 255), hl)))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "muc_bang")


def nav_pick(w=176, h=220, r=24, line=5):
    # tím trên → lam dưới: chuyển màu như cũ nhưng tô bằng nét chì chéo + vân giấy (màu chì), viền mực tay
    top, bot = hexc("#a04cff"), hexc("#38d8ff")
    path = rr_path(line / 2 + 1, line / 2 + 1, w - line / 2 - 1, h - line / 2 - 1, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 91)
    t = vgrad(w, h, [(0, 0), (0.3, 0), (1, 255)])
    rr_, gg, bb = two_tone(w, h, t, top, bot, 95, spacing=6)
    im = Image.merge("RGBA", (rr_, gg, bb, shape))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "muc_chon")


# ---------- nhãn giá trị, nút giá, ô món ----------

def ribbon(w=320, h=74, line=5):
    notch = 26
    poly = [(3, 3), (w - 3, 3), (w - 3, h - 3), (3, h - 3), (notch, h / 2)]
    path = poly_path(poly, 1.5)
    ring, shape = hand_stroke(w, h, path, line, 101, wob=0.9, inner_only=True)
    m = vgrad(w, h, [(0, 255), (0.5, 255), (0.62, 0), (1, 0)])
    rr_, gg, bb = two_tone(w, h, m, hexc("#e8285a"), hexc("#ff3d6e"), 103, spacing=6)
    im = Image.merge("RGBA", (rr_, gg, bb, shape))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "nhan_gia_tri")


def button(name, w=300, h=110, r=30, line=6, body=224, lip=176):
    path = rr_path(line / 2 + 1, line / 2 + 1, w - line / 2 - 1, h - line / 2 - 1, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 111 if body > 200 else 113)
    lum = tex_fill(w, h, 115, level=body, spacing=6, drop=(6, 16))
    # môi tối dưới: mép trên rung
    wob = Wobble(117, 1.5)
    lip_m = Image.new("L", lum.size, 0)
    ImageDraw.Draw(lip_m).polygon([(0, h * SS)] + [(x * SS, (h - line - 14 + wob(x)) * SS) for x in range(0, w + 1, 3)] + [(w * SS, h * SS)], fill=255)
    lum = Image.composite(tex_fill(w, h, 119, level=lip, spacing=6, drop=(6, 14)), lum, lip_m)
    # viền sáng trong: nét chì sáng rung bám trong viền mực
    rim_path = rr_path(line + 4, line + 4, w - line - 4, h - line - 18, r - line - 3)
    rim, _ = hand_stroke(w, h, rim_path, 3.2, 121, wob=0.7, double=False)
    lum = Image.composite(Image.new("L", lum.size, 255), lum, ImageChops.multiply(rim, Image.new("L", rim.size, 200)))
    im = gray_rgba(lum, shape)
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, name)


def item_cell(w=128, h=128, r=20, line=5, strip=42):
    path = rr_path(line / 2 + 1, line / 2 + 1, w - line / 2 - 1, h - line / 2 - 1, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 131)
    lum = tex_fill(w, h, 133, level=255, spacing=6, drop=(5, 13))
    im = gray_rgba(lum, shape)
    wob = Wobble(135, 1.2)
    sm = Image.new("L", lum.size, 0)
    ImageDraw.Draw(sm).polygon([(0, h * SS)] + [(x * SS, (h - strip + wob(x)) * SS) for x in range(0, w + 1, 2)] + [(w * SS, h * SS)], fill=255)
    im.alpha_composite(ink_layer(ImageChops.multiply(sm, shape)))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "o_mon")


def dot(w=48, h=48, line=5):
    ring, shape = hand_stroke(w, h, ellipse_path(w / 2, h / 2, w / 2 - line / 2 - 1, h / 2 - line / 2 - 1), line, 141, wob=0.6, double=False)
    red = hexc("#ff3b4f")
    hv = hatch(w, h, 143, spacing=5, drop=(14, 30))
    ch = [ImageChops.multiply(Image.new("L", hv.size, red[c]), ImageChops.add(hv, Image.new("L", hv.size, 15))) for c in range(3)]
    im = Image.merge("RGBA", (*ch, shape))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "cham_do")


def sheet_panel(w=300, h=300, r=34, line=7):
    # nền tờ popup / trang con: chàm thẫm caro thoi vẽ tay, viền mực tay (Sliced 44)
    lo, hi = hexc("#272247"), hexc("#2d2852")
    path = rr_path(line / 2 + 1.5, line / 2 + 1.5, w - line / 2 - 1.5, h - line / 2 - 1.5, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 151)
    m = diamonds_hand(w, h, 52, 0, 255, 153)
    rr_, gg, bb = two_tone(w, h, m, lo, hi, 155, spacing=7)
    im = Image.merge("RGBA", (rr_, gg, bb, shape))
    im.alpha_composite(ink_layer(ring))
    finish(im, w, h, "to_toi")


def spin_rays(w=256, h=256, n=12):
    # vầng tia sau icon ưu đãi ở sảnh: tia kem vẽ tay, mờ dần ra mép (xoay bằng Spin)
    cx, cy = w / 2, h / 2
    a = rays(w, h, cx, cy, n * 2, w, 255, 161, offset=0, width=0.9)
    fall = Image.new("L", a.size, 0)
    fd = ImageDraw.Draw(fall)
    steps = 40
    for k in range(steps):
        rr_ = (w * SS / 2) * (1 - k / steps)
        fd.ellipse([cx * SS - rr_, cy * SS - rr_, cx * SS + rr_, cy * SS + rr_], fill=int(230 * (k + 1) / steps))
    a = ImageChops.multiply(a, fall)
    col = Image.new("RGBA", a.size, hexc("#fff4c8"))
    col.putalpha(a)
    finish(col, w, h, "tia_xoay")


def pill(w=96, h=48):
    # viên thuốc trắng (tô màu lúc chạy: đồng hồ, số bi, nhãn góc, thanh Lọ Bi); Sliced 24; mép hơi rung, nét chì rất nhạt
    path = rr_path(1, 1, w - 1, h - 1, h / 2 - 1)
    _, shape = hand_stroke(w, h, path, 0.01, 171, wob=0.5, double=False)
    lum = tex_fill(w, h, 173, level=255, spacing=6, drop=(3, 8), grain_amp=4)
    finish(gray_rgba(lum, shape), w, h, "vien")


def bg_tile(w=96, h=96):
    # nền vùng trang (lát): chàm, lưới chéo bằng nét chì rung liền mép (vẽ cả bản sao lệch một ô để khớp khi lát)
    base, line = hexc("#3b3558"), hexc("#46406a")
    im = Image.new("RGBA", (w * SS, h * SS), base)
    d = ImageDraw.Draw(im)
    for k in (-1, 0, 1):
        for sgn, seed in ((1, 181), (-1, 183)):
            wob = Wobble(seed, 0.9, ((48, 1.0), (24, 0.4)))  # bước sóng chia hết 96: liền mép
            pts = []
            for t in range(0, 101):
                u = t / 100
                x = (k + u) * w if sgn > 0 else (k + 1 - u) * w
                y = u * h
                o = wob(u * w * 1.41421)
                pts.append(((x + o * 0.7) * SS, (y - o * 0.7 * sgn) * SS))
            d.line(pts, fill=line, width=int(2.6 * SS), joint="curve")
    g = paper(w, h, 5, 185, wrap=True)
    lum = Image.merge("RGBA", [add_grain(c, g) for c in im.split()[:3]] + [im.split()[3]])
    finish(lum, w, h, "nen_trang")


def side_edge(w=8, h=128):
    # mép phải cột trái: nét mực tay dọc, lát dọc liền mép (sóng chia hết 128)
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    wob = Wobble(191, 0.9, ((128, 1.0), (64, 0.5), (32, 0.25)))
    thick = Wobble(193, 0.9, ((128, 1.0), (64, 0.4)))
    pts_l, pts_r = [], []
    for y in range(0, h + 1):
        c = w / 2 + wob(y)
        wd = 4.6 + thick(y)
        pts_l.append(((c - wd / 2) * SS, y * SS))
        pts_r.append(((c + wd / 2) * SS, y * SS))
    ImageDraw.Draw(im).polygon(pts_l + pts_r[::-1], fill=INK)
    finish(im, w, h, "vien_cot")


def side_column(w=190, h=768):
    """Nền cột trái (lát dọc): chàm thẫm tô chì + hình vẽ tay rải đều (sao, lấp lánh, quái vật, bi, trứng), màu lavender nhạt, vài
    ngôi sao vàng nhạt; mảnh nằm sát mép trên / dưới được vẽ lặp ở mép kia nên lát liền."""
    bg = hexc("#1b163e")
    lum = tex_fill(w, h, 201, level=255, spacing=7, drop=(10, 22), grain_amp=6)
    # nền chàm: nhân màu với độ sáng nét chì (nét chì làm chàm thẫm thêm chút)
    chans = [ImageChops.multiply(Image.new("L", lum.size, bg[c]), lum) for c in range(3)]
    # làm sáng nhẹ để nét chì thấy được trên nền tối: cộng nét chì đảo (sáng) rất nhạt
    inv = ImageChops.invert(lum)
    chans = [ImageChops.add(chans[c], ImageChops.multiply(inv, Image.new("L", inv.size, (40, 34, 80)[c]))) for c in range(3)]
    im = Image.merge("RGBA", (*chans, Image.new("L", lum.size, 255)))
    pieces = []
    if os.path.isdir(DOODLE):
        for f in sorted(os.listdir(DOODLE)):
            if f.endswith(".png"):
                pieces.append((f, Image.open(os.path.join(DOODLE, f)).convert("RGBA")))
    if not pieces:
        print("  (chưa có mảnh hình ở", DOODLE, "): cột trái chỉ có nền tô chì")
    rnd = random.Random(203)
    lav, gold = (150, 134, 226), (255, 222, 120)
    # rải theo lưới so le để đều, lệch ngẫu nhiên; mỗi mảnh xoay nhẹ
    rows = 9
    order = pieces[:]
    rnd.shuffle(order)
    k = 0
    for r_ in range(rows):
        cols = 2 if r_ % 2 == 0 else 1
        for c_ in range(cols):
            if not order:
                break
            name, p = order[k % len(order)]
            k += 1
            star = "sao" in name or "lap_lanh" in name
            size = (rnd.uniform(50, 60) if cols == 2 else rnd.uniform(64, 78)) if not star else rnd.uniform(32, 44)
            sc = size / max(p.width, p.height)
            q = p.resize((max(1, int(p.width * sc * SS)), max(1, int(p.height * sc * SS))), Image.LANCZOS)
            q = q.rotate(rnd.uniform(-18, 18), resample=Image.BICUBIC, expand=True)
            col = gold if (star and rnd.random() < 0.6) else lav
            alpha_k = 0.72 if col == gold else 0.6
            a = q.split()[3].point(lambda v: int(v * alpha_k))
            tint = Image.new("RGBA", q.size, col + (255,))
            tint.putalpha(a)
            cx = (w * (0.27 if cols == 2 and c_ == 0 else 0.73 if cols == 2 else 0.5) + rnd.uniform(-10, 10)) * SS
            cy = ((r_ + 0.5) * h / rows + rnd.uniform(-16, 16)) * SS
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            for dy in (-h * SS, 0, h * SS):  # vẽ lặp lệch một chiều cao để lát dọc liền (paste nhận toạ độ âm, cắt ngoài khung)
                layer.paste(tint, (int(cx - q.width / 2), int(cy - q.height / 2 + dy)), tint)
            im.alpha_composite(layer)
    # rắc thêm sao / lấp lánh vàng nhỏ xen giữa
    small = [p for n_, p in pieces if "sao_nho" in n_ or "lap_lanh" in n_]
    for _ in range(8 if small else 0):
        p = rnd.choice(small)
        size = rnd.uniform(16, 26)
        sc = size / max(p.width, p.height)
        q = p.resize((max(1, int(p.width * sc * SS)), max(1, int(p.height * sc * SS))), Image.LANCZOS).rotate(rnd.uniform(-25, 25), resample=Image.BICUBIC, expand=True)
        tint = Image.new("RGBA", q.size, gold + (255,))
        tint.putalpha(q.split()[3].point(lambda v: int(v * 0.6)))
        cx, cy = rnd.uniform(0.12, 0.88) * w * SS, rnd.uniform(0, h) * SS
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        for dy in (-h * SS, 0, h * SS):
            layer.paste(tint, (int(cx - q.width / 2), int(cy - q.height / 2 + dy)), tint)
        im.alpha_composite(layer)
    finish(im, w, h, "cot_trai")


# ---------- ô vuông hai cột sảnh (người dùng 2026-11-27: "to rõ ràng, hình vuông bo tròn, có viền trắng" như cột icon máy bi của
# Clash of Critters) ----------

def hub_tile(w=320, h=320, r=62, line=7, band=20):
    # o_san_vien: viền mực tay ngoài + dải trắng giấy dày + nét mực mảnh trong (không tô màu); o_san_nen: lòng ô (code tô màu theo ô):
    # nét chì chéo + caro thoi mờ + tia sáng nhạt từ giữa trên, đáy hơi tối (chỗ chữ tên / đồng hồ)
    path = rr_path(line / 2 + 1.5, line / 2 + 1.5, w - line / 2 - 1.5, h - line / 2 - 1.5, r - line / 2)
    ring, shape = hand_stroke(w, h, path, line, 201)
    ins = line + band
    ipath = rr_path(ins, ins, w - ins, h - ins, r - band - line * 0.6)
    iring, ishape = hand_stroke(w, h, ipath, 3.2, 203, wob=0.7, var=0.18, double=False)
    white = ImageChops.subtract(shape, ishape)
    wl = tex_fill(w, h, 205, level=255, spacing=6, drop=(2, 6), grain_amp=4)
    vien = Image.merge("RGBA", (wl, wl, wl.point(lambda v: max(0, v - 6)), white))
    vien.alpha_composite(ink_layer(iring))
    vien.alpha_composite(ink_layer(ring))
    finish(vien, w, h, "o_san_vien")

    lum = ImageChops.multiply(tex_fill(w, h, 207, level=236, spacing=7, drop=(10, 22)), diamonds_hand(w, h, 64, 222, 255, 209))
    a = rays(w, h, w / 2, h * 0.42, 14, w * 0.9, 255, 211, offset=0)
    lum = ImageChops.lighter(lum, ImageChops.multiply(a, vgrad(w, h, [(0, 70), (0.5, 60), (1, 0)])).point(lambda v: v * 4 if v * 4 < 256 else 255))
    dark = bottom_dark(w, h, 0.6, 0.84, 213).point(lambda v: int(140 + v * 115 / 255))
    lum = ImageChops.multiply(lum, dark)
    finish(gray_rgba(lum, ishape), w, h, "o_san_nen")

    # o_san_day: lớp đen mờ đáy lòng ô dưới chữ tên / đồng hồ (người dùng 2026-11-27: "text có 1 lớp đen mờ ở dưới để đọc được"):
    # đúng dáng lòng ô (bo hai góc dưới), mép trên mờ dần; đặt trên hình, dưới chữ
    fade = vgrad(w, h, [(0, 0), (0.5, 0), (0.68, 150), (1, 160)])
    tex = tex_fill(w, h, 215, level=255, spacing=7, drop=(10, 26), grain_amp=6)
    a = ImageChops.multiply(ImageChops.multiply(fade, ishape), tex)
    day = Image.new("RGBA", a.size, (14, 12, 28, 255))
    day.putalpha(a)
    finish(day, w, h, "o_san_day")


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    jobs = {
        "card": card, "tile": tile, "band": band, "nav_pick": nav_pick, "ribbon": ribbon,
        "nut_gia": lambda: button("nut_gia"), "nut_gia_an": lambda: button("nut_gia_an", body=196, lip=160),
        "item_cell": item_cell, "dot": dot, "sheet_panel": sheet_panel, "spin_rays": spin_rays, "pill": pill,
        "bg_tile": bg_tile, "side_edge": side_edge, "side_column": side_column, "hub_tile": hub_tile,
    }
    for k, f in jobs.items():
        if not only or k in only:
            f()
