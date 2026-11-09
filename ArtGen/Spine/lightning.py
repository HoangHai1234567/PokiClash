"""Ảnh hiệu ứng sinh bằng thuật toán theo luật vẽ tay của game (skill pokiclash-hero-fx, 2026-11-09): tô phẳng, vân chì gạch chéo,
viền mực nâu sẫm, không glow, không gradient.

- bolt(): tia sét gấp khúc (chia đoạn lệch điểm giữa) có nhánh rẽ; mỗi hạt giống một dáng, chớp đổi dáng từng khung là "sét giật".
  leader_frac: chỉ vẽ đoạn đầu (tia dẫn mọc từ mây xuống).
- crackle(): tia điện nhỏ lách tách (quanh người, ở chỗ sét đánh).
- clod(): cục đất, sỏi văng lên khi sét đánh xuống đất.
- storm_cloud(): mây giông từ ảnh mây có sẵn (tối màu, giữ viền).

Mỗi hàm trả (ảnh RGBA, điểm neo (x, y) theo pixel ảnh, y xuống): bolt neo ở đầu dưới (chỗ chạm đất), còn lại neo ở tâm.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

SS = 3  # vẽ to gấp 3 rồi thu nhỏ cho mép mượt
INK = (52, 32, 14)
YEL = (243, 214, 50)
YEL_HI = (248, 240, 122)
CORE = (253, 250, 214)


def _mpd(p0, p1, depth, rough, rng, decay=0.6):
    """chia đoạn lệch điểm giữa: mỗi lần chia, điểm giữa lệch vuông góc tỉ lệ theo độ dài đoạn."""
    pts = [np.array(p0, float), np.array(p1, float)]
    r = rough
    for _ in range(depth):
        out = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            seg = b - a
            ln = float(np.hypot(*seg))
            nrm = np.array([-seg[1], seg[0]]) / max(ln, 1e-6)
            out += [(a + b) / 2 + nrm * rng.uniform(-1, 1) * r * ln, b]
        pts = out
        r *= decay
    return pts


def _zig(p0, p1, segs, swing, rng, jitter=0.1):
    """đường gấp khúc kiểu sét: segs đoạn thẳng, mỗi đỉnh lệch ngang luân phiên trái phải (đôi khi cùng phía), góc gãy sắc;
    rồi chia nhỏ 2 lần lệch ít cho nét rung. swing: độ lệch tối đa (pixel) vuông góc đường p0-p1."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    ln = float(np.hypot(*d))
    u = d / max(ln, 1e-6)
    nrm = np.array([-u[1], u[0]])
    g = 1.0 / segs  # đỉnh rải đều có lệch, không dồn cục (đoạn quá ngắn gập thành nút)
    ts = np.clip(np.arange(1, segs) * g + rng.uniform(-0.3, 0.3, segs - 1) * g, 0.04, 0.96)
    ts = np.concatenate([[0.0], np.sort(ts), [1.0]])
    side = 1 if rng.uniform() < 0.5 else -1
    pts = [p0]
    off = 0.0
    for i, t in enumerate(ts[1:-1]):
        side = -side if rng.uniform() < 0.8 else side
        new = side * swing * rng.uniform(0.35, 1.0)
        lim = 1.1 * (t - ts[i]) * ln  # đoạn không nằm ngang quá (dốc ít nhất ~42°)
        off = off + max(-lim, min(lim, new - off))
        pts.append(p0 + u * ln * t + nrm * off)
    pts.append(p1)
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        out += _mpd(a, b, 2, jitter, rng, 0.6)[1:]
    return out


def _fit_x(paths, lo, hi, cx):
    """co lệch ngang quanh cx cho mọi đường nằm trong [lo, hi] (thay vì kẹp sát mép thành đoạn thẳng đứng)."""
    xs = np.concatenate([[p[0] for p in pts] for pts in paths])
    k = 1.0
    if xs.max() > hi:
        k = min(k, (hi - cx) / max(1e-6, xs.max() - cx))
    if xs.min() < lo:
        k = min(k, (cx - lo) / max(1e-6, cx - xs.min()))
    if k < 1:
        for pts in paths:
            for p in pts:
                p[0] = cx + (p[0] - cx) * k


def _hatch(size, base, hi, rng, gap=4, ang=-35, amt=0.55):
    """nền chì sáp: màu phẳng + nét gạch chéo nhạt hơn (hơi rung), vân giấy nhỏ."""
    w, h = size
    im = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(im)
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    step = gap * SS
    span = int(math.hypot(w, h)) + step
    for k in range(-span, span, step):
        jit = rng.uniform(-0.35, 0.35) * step
        x0, y0 = w / 2 + (k + jit) * -sa - span * ca, h / 2 + (k + jit) * ca - span * sa
        x1, y1 = w / 2 + (k + jit) * -sa + span * ca, h / 2 + (k + jit) * ca + span * sa
        c = tuple(int(base[i] + (hi[i] - base[i]) * amt * rng.uniform(0.6, 1.0)) for i in range(3))
        d.line([(x0, y0), (x1, y1)], fill=c, width=max(1, int(SS * rng.uniform(0.8, 1.4))))
    arr = np.asarray(im).astype(np.float32)
    arr *= (1 + rng.uniform(-0.035, 0.035, size=(h, w, 1))).astype(np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _stroke(d, pts, w0, w1):
    """nét dày thon dần từ w0 tới w1, khớp tròn."""
    n = len(pts)
    for i in range(n - 1):
        w = w0 + (w1 - w0) * (i + 0.5) / max(1, n - 1)
        a, b = pts[i], pts[i + 1]
        d.line([tuple(a), tuple(b)], fill=255, width=max(1, int(round(w))))
        r = w / 2
        d.ellipse([b[0] - r, b[1] - r, b[0] + r, b[1] + r], fill=255)
    r = w0 / 2
    d.ellipse([pts[0][0] - r, pts[0][1] - r, pts[0][0] + r, pts[0][1] + r], fill=255)


def _compose(size, strokes, ink, core_strokes, rng, fill=YEL, hi=YEL_HI, core=CORE):
    """strokes: [(pts, w0, w1)] theo pixel ảnh lớn; viền = nét nở thêm ink mỗi bên; lõi kem trên nét chính."""
    w, h = size
    m_out, m_fill, m_core = (Image.new("L", (w, h), 0) for _ in range(3))
    do, df, dc = ImageDraw.Draw(m_out), ImageDraw.Draw(m_fill), ImageDraw.Draw(m_core)
    for pts, w0, w1 in strokes:
        _stroke(do, pts, w0 + 2 * ink, w1 + 2 * ink)
        _stroke(df, pts, w0, w1)
    for pts, w0, w1 in core_strokes:
        _stroke(dc, pts, w0, w1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (w, h), INK + (255,)), (0, 0), m_out)
    out.paste(_hatch((w, h), fill, hi, rng).convert("RGBA"), (0, 0), m_fill)
    if core_strokes:
        out.paste(Image.new("RGBA", (w, h), core + (255,)), (0, 0), m_core)
    return out


def _down(im, anchor):
    w, h = im.size
    small = im.resize((max(1, w // SS), max(1, h // SS)), Image.LANCZOS)
    return small, (anchor[0] / SS, anchor[1] / SS)


def _path_len(pts):
    return sum(float(np.hypot(*(b - a))) for a, b in zip(pts[:-1], pts[1:]))


def _cut(pts, frac):
    """đoạn đầu dài frac tổng độ dài (tia dẫn)."""
    if frac >= 1:
        return pts
    tot, acc, out = _path_len(pts), 0.0, [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        ln = float(np.hypot(*(b - a)))
        if acc + ln >= tot * frac:
            out.append(a + (b - a) * ((tot * frac - acc) / max(ln, 1e-6)))
            return out
        out.append(b)
        acc += ln
    return out


def bolt(seed, h=330, w=150, width=(13.0, 9.0), branches=3, top_dx=None, leader_frac=None, core=True, ink=3.0, segs=None):
    """tia sét dài h px (đầu trên ở mây, đầu dưới chạm đất ở giữa đáy), rộng w px. Neo: đầu dưới."""
    rng = np.random.RandomState(seed)
    W, Hh = w * SS, h * SS
    pad = 10 * SS
    m = 12 * SS
    top = (W / 2 + (top_dx if top_dx is not None else rng.uniform(-0.15, 0.15) * w) * SS, pad)
    bot = (W / 2, Hh - pad)
    main = _zig(top, bot, segs or rng.randint(7, 10), w * SS * rng.uniform(0.13, 0.2), rng, 0.08)
    w0, w1 = width[0] * SS, width[1] * SS
    strokes, cores = [], []
    tot = len(main)
    lo, hi = 0.15, 0.62  # gốc nhánh rải đều trong khoảng, mỗi nhánh một ô
    cells = rng.permutation(branches)
    for b in range(branches):
        k = int((lo + (hi - lo) * (cells[b] + rng.uniform(0.15, 0.85)) / max(1, branches)) * tot)
        p = main[k]
        d = main[min(tot - 1, k + 6)] - p
        d /= max(1e-6, float(np.hypot(*d)))
        side = 1 if (b % 2 == 0) == (rng.uniform() < 0.5) else -1
        a = math.radians(rng.uniform(25, 50)) * side
        dr = np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a)])
        ln = (Hh - p[1]) * rng.uniform(0.25, 0.45)
        e = p + dr * ln
        e[1] = min(Hh - m, e[1])
        br = _zig(p, e, rng.randint(3, 5), ln * 0.16, rng, 0.08)
        bw = (w0 + (w1 - w0) * k / tot) * 0.5
        frac = None
        if leader_frac is not None:  # tia dẫn: nhánh chỉ hiện nếu gốc nhánh đã mọc tới
            if k / tot > leader_frac:
                continue
            frac = min(1.0, (leader_frac - k / tot) * 2.2)
            br = _cut(br, frac)
        strokes.append((br, bw, 0.9 * SS))
        if rng.uniform() < 0.55 and len(br) > 6:  # nhánh con
            j = int(rng.uniform(0.3, 0.6) * len(br))
            q = br[j]
            d2 = br[-1] - q
            d2 /= max(1e-6, float(np.hypot(*d2)))
            a2 = math.radians(rng.uniform(25, 45)) * -side
            dr2 = np.array([d2[0] * math.cos(a2) - d2[1] * math.sin(a2), d2[0] * math.sin(a2) + d2[1] * math.cos(a2)])
            e2 = q + dr2 * ln * rng.uniform(0.3, 0.5)
            e2[1] = min(Hh - m, e2[1])
            sub = _zig(q, e2, 3, ln * 0.08, rng, 0.08)
            strokes.append((sub, bw * 0.55, 0.8 * SS))
    _fit_x([main] + [s[0] for s in strokes], m, W - m, W / 2)
    mp = main if leader_frac is None else _cut(main, leader_frac)
    lw = 0.62 if leader_frac is not None else 1.0
    strokes.append((mp, w0 * lw, (w0 + (w1 - w0) * min(1.0, leader_frac or 1.0)) * lw))
    if core and leader_frac is None:
        cores.append((main, w0 * 0.34, w1 * 0.3))
    im = _compose((W, Hh), strokes, ink * SS, cores, rng)
    return _down(im, bot)


def crackle(seed, size=90, width=5.0, ink=2.6):
    """tia điện nhỏ lách tách: 1 tia gấp khúc ngắn chéo qua ô + 1–2 nhánh. Neo: tâm."""
    rng = np.random.RandomState(1000 + seed)
    S = size * SS
    m = 10 * SS
    a = rng.uniform(0, math.pi)
    r = (S / 2 - m) * rng.uniform(0.8, 1.0)
    c = np.array([S / 2, S / 2])
    p0 = c + np.array([math.cos(a), math.sin(a)]) * r
    p1 = c - np.array([math.cos(a), math.sin(a)]) * r
    main = _zig(p0, p1, rng.randint(4, 6), r * 0.35, rng, 0.06)
    strokes = [(main, width * SS, width * 0.65 * SS)]
    for _ in range(rng.randint(1, 3)):
        k = rng.randint(2, len(main) - 3)
        q = main[k]
        b = rng.uniform(0, 2 * math.pi)
        e = q + np.array([math.cos(b), math.sin(b)]) * r * rng.uniform(0.4, 0.65)
        e = np.clip(e, m, S - m)
        strokes.append((_zig(q, e, 3, r * 0.15, rng, 0.06), width * 0.6 * SS, 0.9 * SS))
    _fit_x([s[0] for s in strokes], m, S - m, S / 2)
    im = _compose((S, S), strokes, ink * SS, [], rng)
    return _down(im, (S / 2, S / 2))


def clod(seed, size=60, kind="dirt", ink=2.4):
    """cục đất (nâu) hoặc sỏi (xám nâu): đa giác méo bo tròn, vân chì, viền mực. Neo: tâm."""
    rng = np.random.RandomState(2000 + seed)
    S = size * SS
    c = S / 2
    n = rng.randint(5, 8)  # ít đỉnh, lệch nhiều: mảnh vỡ góc cạnh (tròn thì cộng viền trắng sticker thành viên bi)
    R = S * 0.38
    rad = R * rng.uniform(0.6, 1.0, n)
    ang = np.sort((np.arange(n) + rng.uniform(-0.3, 0.3, n)) * 2 * math.pi / n)
    sq = rng.uniform(0.55, 0.8)
    tilt = rng.uniform(0, math.pi)
    poly = []
    for t, r in zip(ang, rad):
        x, y = math.cos(t) * r, math.sin(t) * r * sq
        poly.append((c + x * math.cos(tilt) - y * math.sin(tilt), c + x * math.sin(tilt) + y * math.cos(tilt)))
    base, hi = {"dirt": ((136, 92, 52), (168, 122, 78)), "dark": ((112, 74, 42), (146, 104, 64)),
                "pebble": ((150, 138, 118), (182, 172, 152))}[kind]
    m_out, m_fill = Image.new("L", (S, S), 0), Image.new("L", (S, S), 0)
    ImageDraw.Draw(m_out).polygon(poly, fill=255)
    ImageDraw.Draw(m_out).line(poly + [poly[0]], fill=255, width=int(2 * ink * SS))
    ImageDraw.Draw(m_fill).polygon(poly, fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (S, S), INK + (255,)), (0, 0), m_out)
    out.paste(_hatch((S, S), base, hi, rng, gap=3, ang=rng.uniform(-50, -25), amt=0.5).convert("RGBA"), (0, 0), m_fill)
    # một hai vết nứt ngắn màu sẫm (không chấm tròn: hai chấm trông như mắt)
    d = ImageDraw.Draw(out)
    for _ in range(rng.randint(1, 3)):
        a0 = rng.uniform(0, 2 * math.pi)
        x, y = c + math.cos(a0) * R * 0.55, c + math.sin(a0) * R * 0.55 * sq
        pts = _zig((x, y), (c + rng.uniform(-0.2, 0.2) * R, c + rng.uniform(-0.2, 0.2) * R), 3, R * 0.12, rng, 0.05)
        d.line([tuple(p) for p in pts], fill=tuple(int(v * 0.62) for v in base) + (255,), width=int(1.3 * SS))
    return _down(out, (c, c))


def scorch(seed, size=160, ink=2.4):
    """vết cháy nứt dưới đất chỗ sét đánh: mảng nâu sẫm dẹt (nhìn nghiêng), vết nứt gấp khúc toả ra. Neo: tâm."""
    rng = np.random.RandomState(3000 + seed)
    W, Hh = size * SS, int(size * 0.42) * SS
    c = np.array([W / 2, Hh / 2])
    n = 14
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rad = 1 + 0.18 * np.convolve(rng.uniform(-1, 1, n + 2), [0.25, 0.5, 0.25], "valid")
    poly = [(c[0] + math.cos(a) * r * W * 0.3, c[1] + math.sin(a) * r * Hh * 0.3) for a, r in zip(ang, rad)]
    out = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.polygon(poly, fill=(92, 62, 36, 150))
    for j in range(rng.randint(5, 8)):  # nứt toả ra, dẹt theo nhìn nghiêng
        a = 2 * math.pi * j / 7 + rng.uniform(-0.3, 0.3)
        e = c + np.array([math.cos(a) * W * rng.uniform(0.34, 0.47), math.sin(a) * Hh * rng.uniform(0.34, 0.46)])
        pts = _zig(c + (e - c) * 0.15, e, 3, float(np.hypot(*(e - c))) * 0.12, rng, 0.05)
        d.line([tuple(p) for p in pts], fill=INK + (255,), width=int(ink * SS), joint="curve")
    return _down(out, tuple(c))


def puff(seed, size=80, ink=2.4):
    """cụm bụi đất: 3–4 tròn chồng nhau màu đất nhạt, vân chì, viền mực. Neo: tâm."""
    rng = np.random.RandomState(4000 + seed)
    S = size * SS
    c = S / 2
    m_out, m_fill = Image.new("L", (S, S), 0), Image.new("L", (S, S), 0)
    do, df = ImageDraw.Draw(m_out), ImageDraw.Draw(m_fill)
    for _ in range(rng.randint(3, 5)):
        r = S * rng.uniform(0.17, 0.26)
        x, y = c + rng.uniform(-0.18, 0.18) * S, c + rng.uniform(-0.1, 0.12) * S
        e = ink * SS
        do.ellipse([x - r - e, y - r - e, x + r + e, y + r + e], fill=255)
        df.ellipse([x - r, y - r, x + r, y + r], fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (S, S), INK + (255,)), (0, 0), m_out)
    out.paste(_hatch((S, S), (214, 194, 154), (232, 218, 186), rng, gap=4, amt=0.6).convert("RGBA"), (0, 0), m_fill)
    return _down(out, (c, c))


def storm_cloud(im):
    """mây giông từ ảnh mây sẵn có: kéo về xám tím sẫm, giữ viền mực (điểm tối giữ nguyên)."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    lum = rgb.mean(axis=2, keepdims=True)
    tgt = np.array([96, 98, 128], np.float32)
    k = np.clip((lum - 70) / 120, 0, 1)  # viền tối (lum thấp) giữ nguyên
    out = rgb * (1 - k) + (tgt + (lum - 180) * 0.35) * k
    return Image.fromarray(np.clip(np.concatenate([out, al], axis=2), 0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":  # tờ xem thử: py -3 -I lightning.py <ra.png>
    import sys
    tiles = [bolt(s)[0] for s in range(6)] + [bolt(0, leader_frac=f)[0] for f in (0.4, 0.75)] + \
            [bolt(10 + s, h=300, w=90, width=(6, 4.5), branches=1)[0] for s in range(3)]
    small = [crackle(s)[0] for s in range(5)] + [clod(s, kind=k)[0] for s, k in enumerate(("dirt", "dark", "dirt", "pebble"))]
    W = sum(t.width + 10 for t in tiles) + 10
    sheet = Image.new("RGBA", (W, 460), (233, 238, 228, 255))
    x = 10
    for t in tiles:
        sheet.alpha_composite(t, (x, 10))
        x += t.width + 10
    x = 10
    for t in small:
        sheet.alpha_composite(t, (x, 350))
        x += t.width + 12
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else "lightning_sheet.png")
