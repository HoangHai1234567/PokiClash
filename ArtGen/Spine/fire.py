"""Ảnh hạt lửa, khói sinh bằng thuật toán theo luật vẽ tay (skill pokiclash-hero-fx): tô phẳng, vân chì gạch chéo, viền mực.

Lửa và khói vẽ theo kiểu "chồng lớp": mỗi hạt là MỘT hình tròn méo, game vẽ nó nhiều lần ở các lớp khác nhau (mực -> đỏ -> cam ->
vàng -> kem), lớp sau nhỏ hơn lớp trước. Các hạt chồng nhau thì cùng màu hoà làm một khối, chỉ khối ngoài cùng có viền mực: luồng lửa
mềm, liền, không rời rạc từng cục. Vì vậy ảnh blob là ảnh XÁM (nhuộm bằng Image.color), ảnh viền là ảnh trắng đặc (nhuộm màu mực).

- blob(seed): tròn méo xám có vân chì (nhuộm thành đỏ, cam, vàng, kem, khói).
- blob_solid(seed): đúng dáng blob, trắng đặc (lớp mực bên dưới, phóng to hơn một chút).
- tongue(seed): lưỡi lửa giọt nước nhọn đầu (xám, có vân), bốc lên ở mép luồng.
- streak(seed): tia lửa văng, vệt thuôn vàng có viền mực (tự đủ màu, không nhuộm).
- ember(seed): than nhỏ có viền.

Mỗi hàm trả (ảnh RGBA, neo (x, y)), neo ở tâm (streak: đầu nhọn phía sau, đầu tròn phía trước = bên phải).
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from lightning import SS, _down, _hatch

INK = (43, 33, 24)  # #2B2118
GRAY = (246, 246, 246)  # nền; nét chì sẫm hơn (HATCH_LO) như tranh tướng
HATCH_LO = (196, 196, 196)


def _pencil(size, seed):
    """nền chì sáp nhuộm được: xám rất nhạt, nét gạch chéo sẫm hơn thấy rõ (màu ra = màu nhuộm × 0,96, nét × 0,77)."""
    return _hatch(size, GRAY, HATCH_LO, np.random.RandomState(seed), gap=3, ang=-38, amt=0.85).convert("RGBA")  # nền xám nhuộm được: màu ra = màu nhuộm × 0,89, nét chì = màu nhuộm × 1
GRAY_HI = HATCH_LO  # tên cũ, giữ cho mã cũ


def _blob_poly(rng, S, n=18, wob=0.10, sq=1.0):
    c = S / 2
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rad = 1 + wob * np.convolve(rng.uniform(-1, 1, n + 4), [0.15, 0.2, 0.3, 0.2, 0.15], "valid")[:n]
    R = S * 0.42
    return [(c + math.cos(a) * r * R, c + math.sin(a) * r * R * sq) for a, r in zip(ang, rad)]


def blob(seed, size=96):
    rng = np.random.RandomState(5000 + seed)
    S = size * SS
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(_blob_poly(rng, S), fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(_pencil((S, S), 5000 + seed), (0, 0), m)
    return _down(out, (S / 2, S / 2))


def blob_solid(seed, size=96):
    rng = np.random.RandomState(5000 + seed)
    S = size * SS
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(out).polygon(_blob_poly(rng, S), fill=(255, 255, 255, 255))
    return _down(out, (S / 2, S / 2))


def tongue(seed, size=96, solid=False):
    """lưỡi lửa: đáy tròn, đầu nhọn cong lệch về một bên, chĩa LÊN (game xoay)."""
    rng = np.random.RandomState(6000 + seed)
    S = size * SS
    c = S / 2
    R = S * 0.26
    bend = rng.uniform(-0.18, 0.18) * S
    pts = []
    for a in np.linspace(0, math.pi, 12):  # nửa tròn đáy
        pts.append((c + math.cos(a) * R, c + S * 0.18 + math.sin(a) * R))
    tip = (c + bend, c - S * 0.44)
    left = [(c - R, c + S * 0.18), (c - R * 0.7 + bend * 0.3, c - S * 0.12), tip]
    right = [tip, (c + R * 0.7 + bend * 0.5, c - S * 0.08), (c + R, c + S * 0.18)]
    poly = pts + left[1:] + right[1:-1]
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    if solid:
        out.paste(Image.new("RGBA", (S, S), (255, 255, 255, 255)), (0, 0), m)
    else:
        out.paste(_hatch((S, S), GRAY, GRAY_HI, rng, gap=5, ang=-35, amt=0.9).convert("RGBA"), (0, 0), m)
    return _down(out, (c, c + S * 0.1))


def streak(seed, length=72, width=13, ink=2.2):
    """vệt tia lửa: đuôi nhọn bên trái, đầu tròn bên phải; vàng, lõi kem, viền mực."""
    rng = np.random.RandomState(7000 + seed)
    W, H = int(length * SS), int((width + 2 * ink + 4) * SS)
    cy = H / 2
    r = width * SS / 2
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    e = ink * SS
    hx = W - r - 2 * e
    def poly(rr, x0):
        top = [(x0, cy)] + [(hx + math.cos(a) * rr, cy + math.sin(a) * rr) for a in np.linspace(-math.pi / 2, math.pi / 2, 12)]
        return top
    d.polygon(poly(r + e, 0), fill=INK + (255,))
    d.polygon(poly(r, 2.5 * e), fill=(246, 200, 64, 255))
    d.polygon(poly(r * 0.45, W * 0.45), fill=(253, 244, 206, 255))
    return _down(out, (W / 2, cy))


def ember(seed, size=28, ink=2.0):
    rng = np.random.RandomState(8000 + seed)
    S = size * SS
    c = S / 2
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    poly = _blob_poly(rng, S * 0.8, n=7, wob=0.25)
    off = S * 0.1
    poly = [(x + off, y + off) for x, y in poly]
    d.polygon(poly, fill=INK + (255,))
    k = 0.62
    d.polygon([(c + (x - c) * k, c + (y - c) * k) for x, y in poly], fill=(244, 170, 56, 255))
    return _down(out, (c, c))


def erode_frames(seed, n=6, size=96, ink=2.4, kind="blob"):
    """tan kiểu hoạt hình (học từ tờ khung Epic Toon FX): hình phẳng bị một hình tròn lệch tâm 'cắn' dần từ một phía:
    tròn đặc -> lưỡi liềm -> cung mảnh -> hết; không mờ alpha. Trả [(ruột xám nhuộm được, viền trắng đặc)] cho n khung,
    khung 0 là hình nguyên. Viền = ruột nở thêm ink px (giãn hình thái), nên lớp mực dưới khớp đúng hình đã bị cắn."""
    from PIL import ImageFilter
    rng = np.random.RandomState(9000 + seed)
    S = size * SS
    base = Image.new("L", (S, S), 0)
    poly = _blob_poly(np.random.RandomState(5000 + seed), S) if kind == "blob" else None
    ImageDraw.Draw(base).polygon(poly, fill=255)
    tex = _hatch((S, S), GRAY, GRAY_HI, np.random.RandomState(5000 + seed), gap=5, ang=-35, amt=0.9).convert("RGBA")
    a = rng.uniform(0, 2 * math.pi)  # hướng cắn
    out = []
    for i in range(n):
        k = i / max(1, n - 1)
        m = base.copy()
        if k > 0:
            R = S * (0.30 + 0.32 * k)  # vết cắn to dần, tâm tiến vào
            d = S * (0.62 - 0.55 * k)
            cx, cy = S / 2 + math.cos(a) * d, S / 2 + math.sin(a) * d
            ImageDraw.Draw(m).ellipse([cx - R, cy - R, cx + R, cy + R], fill=0)
        fill = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        fill.paste(tex, (0, 0), m)
        e = int(ink * SS) * 2 + 1
        rim = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        rim.paste(Image.new("RGBA", (S, S), (255, 255, 255, 255)), (0, 0), m.filter(ImageFilter.MaxFilter(e)))
        out.append((_down(fill, (S / 2, S / 2))[0], _down(rim, (S / 2, S / 2))[0]))
    return out


# ---------- bộ Hỏa (2026-11-10): thêm kiểu lửa nhọn, xoắn, dung nham, aura, lên cấp, thiên thạch ----------
def _mask_to(m, solid):
    """mặt nạ L -> ảnh RGBA: trắng đặc (lớp mực) hoặc xám có vân chì (nhuộm được)."""
    S = m.size[0]
    out = Image.new("RGBA", m.size, (0, 0, 0, 0))
    src = Image.new("RGBA", m.size, (255, 255, 255, 255)) if solid else _pencil(m.size, S)
    out.paste(src, (0, 0), m)
    return out


def _tongue_poly(centre, widths, S, base_r, licks=()):
    """đa giác lưỡi lửa từ đường giữa (danh sách điểm từ đáy lên ngọn) và bề rộng nửa; pháp tuyến tính theo đường giữa thật
    (không thì ngọn cong gắt bị kẹp thành sợi mảnh). licks: [(chỉ số điểm, bên +1/-1, dài, ngả lên)] thêm lưỡi nhọn ở mép."""
    n = len(centre)
    L, R = [], []
    for i in range(n):
        x0, y0 = centre[max(0, i - 1)]
        x1, y1 = centre[min(n - 1, i + 1)]
        tx, ty = x1 - x0, y1 - y0
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        w = widths[i]
        x, y = centre[i]
        L.append((x - nx * w, y - ny * w))
        R.append((x + nx * w, y + ny * w))
        for (li, side, length, up) in licks:
            if li == i:
                tgt = (L if side < 0 else R)
                ox, oy = (-nx if side < 0 else nx), (-ny if side < 0 else ny)
                apex = (x + ox * (w + length) + tx / ln * length * up, y + oy * (w + length) + ty / ln * length * up)
                tgt.append(apex)
                tgt.append((x + ox * w * 0.6 + tx / ln * length * 0.35, y + oy * w * 0.6 + ty / ln * length * 0.35))
    bx, by = centre[0]
    base = [(bx + math.cos(t) * base_r, by + math.sin(t) * base_r * 0.9) for t in np.linspace(0, math.pi, 12)]
    return R[::-1] + base + L


def hook(seed, size=96, solid=False):
    """lưỡi lửa móc câu (kiểu tranh lửa nhọn): đáy tròn mập, thân cong chữ S, ngọn nhọn quặp nhẹ sang một bên. Ngọn chĩa LÊN.
    (2026-11-10: ngọn cũ quặp gắt và thon về 0 quá sớm nên thừa một sợi mảnh lệch bên; giờ quặp ít, ngọn thon đều.)"""
    rng = np.random.RandomState(6500 + seed)
    S = size * SS
    c = S / 2
    side = 1 if seed % 2 == 0 else -1
    bend = rng.uniform(0.05, 0.1) * S * side
    curl = rng.uniform(0.1, 0.15) * S * side
    R = S * rng.uniform(0.17, 0.2)
    y0, y1 = c + S * 0.28, c - S * 0.42
    centre, widths = [], []
    for i in range(23):
        t = i / 22
        centre.append((c + bend * math.sin(math.pi * t * 0.9) + curl * max(0.0, (t - 0.6) / 0.4) ** 1.6, y0 + (y1 - y0) * t))
        widths.append(R * (1 - t) ** 0.6 * (1 + 0.2 * math.sin(math.pi * t)))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(_tongue_poly(centre, widths, S, R), fill=255)
    return _down(_mask_to(m, solid), (c, c + S * 0.08))


def flame_lobes(seed, size=128, solid=False):
    """lưỡi lửa kiểu tranh tướng (người dùng 2026-11-10: phun lửa phải hợp nét tướng và game): chân tròn mập, thân cong, 2-3 ngọn
    nhọn quặp (ngọn chính + 1-2 ngọn phụ mọc từ hai vai, ngả ra rồi quặp lên), như lửa ở bờm Kim Sư, đuôi Hỏa Tinh. Vân chì sáp
    SẪM hơn nền (nét gạch chéo thấy rõ như tranh tướng). Ngọn chính chĩa LÊN. Neo: gần chân."""
    rng = np.random.RandomState(7300 + seed)
    S = size * SS
    c = S / 2
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    side = 1 if seed % 2 == 0 else -1

    def tongue(x0, y0, length, ang0, ang1, w0, hook, base_r):
        n = 28
        centre, widths = [], []
        x, y = x0, y0
        step = length / (n - 1)
        for i in range(n):
            t = i / (n - 1)
            ang = ang0 + (ang1 - ang0) * t + hook * max(0.0, (t - 0.6) / 0.4) ** 1.5  # ngọn quặp
            centre.append((x, y))
            widths.append(w0 * (1 - t) ** 0.7 * (1 + 0.18 * math.sin(math.pi * t)))
            x += math.sin(ang) * step
            y -= math.cos(ang) * step
        d.polygon(_tongue_poly(centre, widths, S, base_r), fill=255)
        return centre, widths

    W0 = S * rng.uniform(0.17, 0.2)
    lean = rng.uniform(0.05, 0.15) * side
    ctr, wid = tongue(c, c + S * 0.26, S * 0.66, lean, lean * 0.4, W0, side * rng.uniform(0.9, 1.3), W0 * 1.15)
    for sd in ([-side, side] if rng.uniform() < 0.6 else [-side]):  # ngọn phụ ở vai
        i = int(len(ctr) * rng.uniform(0.18, 0.32))
        x, y = ctr[i]
        tongue(x + sd * wid[i] * 0.55, y, S * rng.uniform(0.26, 0.36), sd * rng.uniform(0.7, 1.0), sd * rng.uniform(0.15, 0.35),
               wid[i] * rng.uniform(0.6, 0.75), sd * rng.uniform(0.8, 1.3), wid[i] * 0.5)
    if solid:
        out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        out.paste(Image.new("RGBA", (S, S), (255, 255, 255, 255)), (0, 0), m)
    else:
        out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        out.paste(_hatch((S, S), (246, 246, 246), (196, 196, 196), np.random.RandomState(S + seed), gap=3, ang=-38, amt=0.85)
                  .convert("RGBA"), (0, 0), m)
    return _down(out, (c, c + S * 0.12))


def cloud(seed, size=128, solid=False):
    """cụm khói kiểu mây vẽ tay của game (mây trên nền sân, mây xoắn của Lân Hỏa): 5-7 bướu tròn to nhỏ chồng nhau quanh một
    khối giữa, mép cuộn lồi lõm. Xám vân chì hoặc trắng đặc. Neo: tâm."""
    rng = np.random.RandomState(8800 + seed)
    S = size * SS
    c = S / 2
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    R = S * 0.22
    d.ellipse([c - R * 1.25, c - R * 1.05, c + R * 1.25, c + R * 1.05], fill=255)
    n = rng.randint(5, 8)
    a0 = rng.uniform(0, 2 * math.pi)
    for i in range(n):
        a = a0 + 2 * math.pi * i / n + rng.uniform(-0.25, 0.25)
        r = R * rng.uniform(0.55, 0.95)
        dist = R * rng.uniform(0.95, 1.25)
        x, y = c + math.cos(a) * dist * 1.15, c + math.sin(a) * dist * 0.9
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return _down(_mask_to(m, solid), (c, c))


def burst(seed, size=128, solid=False):
    """chớp nổ kiểu truyện tranh vẽ tay: sao gai 9-11 cánh nhọn dài ngắn xen kẽ, hơi lệch. Xám vân chì hoặc trắng đặc. Neo: tâm."""
    rng = np.random.RandomState(8900 + seed)
    S = size * SS
    c = S / 2
    n = rng.randint(9, 12)
    pts = []
    a0 = rng.uniform(0, 2 * math.pi)
    for i in range(n):
        a = a0 + 2 * math.pi * i / n + rng.uniform(-0.08, 0.08)
        ro = S * 0.47 * (rng.uniform(0.92, 1.0) if i % 2 == 0 else rng.uniform(0.68, 0.8))
        ri = S * 0.47 * rng.uniform(0.42, 0.5)
        pts.append((c + math.cos(a) * ro, c + math.sin(a) * ro))
        b = a + math.pi / n
        pts.append((c + math.cos(b) * ri, c + math.sin(b) * ri))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return _down(_mask_to(m, solid), (c, c))


def curl(seed, size=96, width=4.5):
    """vòng xoắn trang trí (nét trơn, nhuộm màu đỏ sẫm): xoắn ốc 1,3 vòng có đuôi kéo ra. Neo: tâm."""
    rng = np.random.RandomState(6800 + seed)
    S = size * SS
    c = S / 2
    turns = rng.uniform(1.1, 1.5)
    a0 = rng.uniform(0, 2 * math.pi)
    side = 1 if seed % 2 else -1
    pts = []
    for i in range(60):
        t = i / 59
        th = a0 + side * t * turns * 2 * math.pi
        r = S * (0.04 + 0.26 * t)
        pts.append((c + math.cos(th) * r, c + math.sin(th) * r))
    th = a0 + side * turns * 2 * math.pi
    tail = [(pts[-1][0] + math.cos(th + side * 1.5) * S * 0.12 * k, pts[-1][1] + math.sin(th + side * 1.5) * S * 0.12 * k)
            for k in (0.5, 1.0)]
    pts += tail
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    for i in range(len(pts) - 1):
        w = width * SS * (0.45 + 0.55 * min(1, i / 25)) * (0.5 if i > len(pts) - 4 else 1)
        d.line([pts[i], pts[i + 1]], fill=255, width=max(1, int(w)))
        d.ellipse([pts[i + 1][0] - w / 2, pts[i + 1][1] - w / 2, pts[i + 1][0] + w / 2, pts[i + 1][1] + w / 2], fill=255)
    return _down(_mask_to(m, True), (c, c))


def ring(thick=0.16, size=128, solid=False):
    """vòng tròn (game bóp dẹt thành elip dưới chân): solid=True là vòng mực rộng hơn, False là dải màu xám có vân. Neo: tâm."""
    S = size * SS
    c = S / 2
    R = S * 0.46
    t = thick * R
    e = 2.6 * SS if solid else 0
    ro, ri = R + e, R - t - e
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([c - ro, c - ro, c + ro, c + ro], fill=255)
    d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=0)
    return _down(_mask_to(m, solid), (c, c))


def lava_crack(seed, size=220, ink=2.4):
    """khe nứt dung nham dưới đất (nhìn nghiêng, dẹt): mảng cháy sẫm, các khe toả ra tô cam có lõi vàng, viền mực. Neo: tâm."""
    from lightning import _zig
    rng = np.random.RandomState(3300 + seed)
    W, Hh = size * SS, int(size * 0.42) * SS
    c = np.array([W / 2, Hh / 2])
    out = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    n = 16
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rad = 1 + 0.2 * np.convolve(rng.uniform(-1, 1, n + 2), [0.25, 0.5, 0.25], "valid")
    d.polygon([(c[0] + math.cos(a) * r * W * 0.27, c[1] + math.sin(a) * r * Hh * 0.27) for a, r in zip(ang, rad)],
              fill=(70, 40, 30, 170))
    lines = []
    for j in range(rng.randint(6, 9)):
        a = 2 * math.pi * j / 7.5 + rng.uniform(-0.3, 0.3)
        e = c + np.array([math.cos(a) * W * rng.uniform(0.33, 0.47), math.sin(a) * Hh * rng.uniform(0.33, 0.46)])
        pts = _zig(c + (e - c) * 0.08, e, 4, float(np.hypot(*(e - c))) * 0.1, rng, 0.05)
        lines.append([tuple(p) for p in pts])
    for wd, col in ((5.5, INK), (3.6, (232, 96, 34)), (1.6, (252, 214, 96))):
        for pts in lines:
            d.line(pts, fill=col + (255,), width=int(wd * SS), joint="curve")
    return _down(out, tuple(c))


def lava_rock(seed, size=60, ink=2.4):
    """đá dung nham: khối góc cạnh tím than có vân chì, khe nứt cam lõi vàng, viền mực. Neo: tâm."""
    from lightning import _zig
    rng = np.random.RandomState(2600 + seed)
    S = size * SS
    c = S / 2
    n = rng.randint(5, 8)
    R = S * 0.38
    rad = R * rng.uniform(0.62, 1.0, n)
    ang = np.sort((np.arange(n) + rng.uniform(-0.3, 0.3, n)) * 2 * math.pi / n)
    poly = [(c + math.cos(t) * r, c + math.sin(t) * r * 0.85) for t, r in zip(ang, rad)]
    m_out, m_fill = Image.new("L", (S, S), 0), Image.new("L", (S, S), 0)
    ImageDraw.Draw(m_out).polygon(poly, fill=255)
    ImageDraw.Draw(m_out).line(poly + [poly[0]], fill=255, width=int(2 * ink * SS))
    ImageDraw.Draw(m_fill).polygon(poly, fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (S, S), INK + (255,)), (0, 0), m_out)
    out.paste(_hatch((S, S), (72, 58, 70), (98, 82, 96), rng, gap=3, amt=0.5).convert("RGBA"), (0, 0), m_fill)
    d = ImageDraw.Draw(out)
    for _ in range(rng.randint(1, 3)):
        a0 = rng.uniform(0, 2 * math.pi)
        p0 = (c + math.cos(a0) * R * 0.7, c + math.sin(a0) * R * 0.6)
        pts = [tuple(p) for p in _zig(p0, (c + rng.uniform(-0.15, 0.15) * R, c + rng.uniform(-0.15, 0.15) * R), 3, R * 0.12, rng, 0.05)]
        d.line(pts, fill=(236, 104, 36, 255), width=int(2.6 * SS), joint="curve")
        d.line(pts, fill=(252, 214, 96, 255), width=int(1.0 * SS), joint="curve")
    return _down(out, (c, c))


def star4(seed, size=48, ink=2.0):
    """sao 4 cánh phẳng (lấp lánh khi lên cấp): vàng, lõi kem, viền mực. Neo: tâm."""
    S = size * SS
    c = S / 2
    def poly(R, r):
        pts = []
        for i in range(8):
            a = -math.pi / 2 + i * math.pi / 4
            rr = R if i % 2 == 0 else r
            pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
        return pts
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.polygon(poly(S * 0.47, S * 0.17), fill=INK + (255,))
    d.polygon(poly(S * 0.47 - ink * SS * 1.6, S * 0.17 - ink * SS * 0.8), fill=(248, 206, 72, 255))
    d.polygon(poly(S * 0.2, S * 0.07), fill=(254, 244, 206, 255))
    return _down(out, (c, c))


def heat_ribbon(phase, length=120, amp=9, width=7, ink=2.0):
    """dải sóng nhiệt dọc (vẽ tay): nét lượn chữ S thon hai đầu, ruột kem cam, viền mực. phase 0..1 đổi pha sóng. Neo: tâm."""
    W, Hh = int((2 * amp + width + 2 * ink + 6) * SS), int(length * SS)
    cx = W / 2
    pts = []
    for i in range(40):
        t = i / 39
        y = Hh * (0.04 + 0.92 * t)
        x = cx + amp * SS * math.sin(2 * math.pi * (1.6 * t + phase)) * math.sin(math.pi * t) ** 0.5
        pts.append((x, y, math.sin(math.pi * t) ** 0.8))
    out = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    for extra, col in ((2 * ink, INK), (0, (250, 196, 104))):
        for (x0, y0, w0), (x1, y1, w1) in zip(pts[:-1], pts[1:]):
            w = (width * (w0 + w1) / 2 + extra) * SS
            d.line([(x0, y0), (x1, y1)], fill=col + (255,), width=max(1, int(w)))
            d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=col + (255,))
    return _down(out, (W / 2, Hh / 2))


def ash(seed, size=24):
    """mảnh tro: đa giác méo 3-5 đỉnh trắng đặc (game nhuộm đen than hoặc xám tro), không viền (nhỏ quá viền thành vết bẩn)."""
    rng = np.random.RandomState(8600 + seed)
    S = size * SS
    c = S / 2
    n = rng.randint(3, 6)
    ang = np.sort(rng.uniform(0, 2 * math.pi, n))
    sq = rng.uniform(0.35, 0.7)  # mảnh dẹt: lật lá thì trông như lấp loá
    poly = [(c + math.cos(a) * S * rng.uniform(0.25, 0.46), c + math.sin(a) * S * rng.uniform(0.25, 0.46) * sq) for a in ang]
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(out).polygon(poly, fill=(255, 255, 255, 255))
    return _down(out, (c, c))


def needle(seed=0, size=128, solid=False):
    """kim lửa: gai dài nhọn chĩa LÊN, phần mập ở 70% chiều dài, đáy tròn, hai mép hơi lượn như lưỡi lửa. Neo: tâm."""
    rng = np.random.RandomState(7700 + seed)
    S = size * SS
    c = S / 2
    tip, wide, bot = S * 0.03, S * 0.72, S * 0.94
    hw = S * rng.uniform(0.13, 0.15)
    L, R = [], []
    for i in range(25):
        t = i / 24
        y = tip + (wide - tip) * t
        w = hw * t ** 0.75 * (1 + 0.06 * math.sin(t * 9 + seed))
        L.append((c - w, y))
        R.append((c + w, y))
    base = [(c + math.cos(a) * hw, wide + math.sin(a) * (bot - wide)) for a in np.linspace(0, math.pi, 12)]
    poly = R + base + L[::-1]
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return _down(_mask_to(m, solid), (c, c))


def ellipse_solid(size=96):
    """elip/tròn trắng đặc (bóng dưới đất, chớp kem, vũng). Neo: tâm."""
    S = size * SS
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([S * 0.04, S * 0.04, S * 0.96, S * 0.96], fill=(255, 255, 255, 255))
    return _down(out, (S / 2, S / 2))


def sheet(path):
    tiles = [blob(s)[0] for s in range(4)] + [blob_solid(0)[0]] + [tongue(s)[0] for s in range(3)]
    tiles += [hook(s)[0] for s in range(3)] + [curl(s)[0] for s in range(2)] + [ring()[0], lava_rock(0)[0], star4(0)[0]]
    tiles += [streak(s)[0] for s in range(2)] + [ember(s)[0] for s in range(2)]
    W = sum(t.width + 12 for t in tiles) + 12
    out = Image.new("RGBA", (W, 130), (233, 238, 228, 255))
    x = 12
    for t in tiles:
        out.alpha_composite(t, (x, 12))
        x += t.width + 12
    out.save(path)


if __name__ == "__main__":  # tờ xem thử: py -3 -I fire.py <ra.png>
    import sys
    sheet(sys.argv[1] if len(sys.argv) > 1 else "fire_sheet.png")
