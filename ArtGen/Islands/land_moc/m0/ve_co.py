# Vẽ cờ ải cho đảo vùng đất (góp ý 2026-11-18: "chia đều các ô ải ra, không cần hiện số, các ô này phải làm nổi bật",
# "có thể đổi sang dạng cờ cũng được"). Nét vẽ tay như ảnh mốc bản đồ: viền mực nâu hơi rung, tô chì có vân gạch chéo,
# tô phẳng (không mảng sáng tối, không bóng đổ, không điểm sáng).
# - co_vai_<k>.png: vải cờ đuôi én, 6 khung phấp phới; vẽ TRẮNG để game nhuộm theo trạng thái (LandFlag: chưa mở xanh, đã qua
#   vàng, đang đánh đỏ cam), vân chì xám nhạt thành vân màu đậm hơn khi nhuộm;
# - co_can.png: cán gỗ có núm vàng, chân nhọn cắm đất (giữ màu);
# - but_chi.png: bút chì màu bay vào tô màu vùng boss vừa mở (2026-11-18), nằm chéo, mũi chì ở góc dưới trái (pivot in ra);
# - co_o.png: ô đá dưới chân cờ, trắng để nhuộm nhạt theo màu cờ (chỗ cắm, không phải bóng).
# Đơn vị: "đơn vị bản đồ" ở cỡ chấm 104 (land.pip), ảnh vẽ gấp R = 2 điểm ảnh mỗi đơn vị. Cách gắn khớp LandFlag.cs (hằng số in ra).
# Chạy: py -3 -I ve_co.py        (xuất vào Assets/03 Art/Islands/Co và tờ soi m1/soi_co.png)
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Islands", "Co")
SOI = os.path.join(HERE, "..", "m1", "soi_co.png")

R = 2            # điểm ảnh mỗi đơn vị bản đồ
SS = 4           # vẽ phóng rồi thu nhỏ cho nét mượt
INK = (58, 40, 26, 255)
LINE = 5.5       # viền ngoài (đơn vị bản đồ)
FRAMES = 6
# vải: dài, cao, sâu khe đuôi én, biên độ sóng, bước sóng (đơn vị bản đồ)
CL, CH, NOTCH, AMP, LAM = 120.0, 72.0, 26.0, 9.0, 115.0
M = 14.0         # lề quanh vải (chứa sóng + viền)
# cán: cao từ chân tới đỉnh núm, rộng, bán kính núm
PH, PW, KR = 150.0, 9.0, 8.5
# ô đá
OW, OH = 92.0, 36.0


def px(v):
    return int(round(v * R * SS))


def wobble(pts, amp, seed, closed=True):
    """dời từng điểm theo pháp tuyến bằng nhiễu mượt (nét tay hơi rung)"""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    n = len(pts)
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        b = pts[(i + 1) % n] if closed or i < n - 1 else pts[i]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        t = i / max(1, n)
        d = amp * (0.6 * math.sin(t * 6.28 * 3 + ph[0]) + 0.3 * math.sin(t * 6.28 * 7 + ph[1]) + 0.2 * math.sin(t * 6.28 * 13 + ph[2]))
        out.append((x + nx * d, y + ny * d))
    return out


def hatch(size, poly, seed, alpha=(22, 44), step=4.2, ang=62):
    """vân chì: nét gạch chéo đứt quãng xám nâu nhạt trong đa giác"""
    W, H = size
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rnd = random.Random(seed)
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    diag = math.hypot(W, H)
    s = -diag
    while s < diag:
        t = -diag
        while t < diag:
            ln = rnd.uniform(0.25, 0.7) * diag * 0.25
            x0, y0 = W / 2 + vx * s + ux * t, H / 2 + vy * s + uy * t
            x1, y1 = x0 + ux * ln, y0 + uy * ln
            d.line([(x0, y0), (x1, y1)], fill=(70, 55, 40, rnd.randint(*alpha)), width=max(1, px(0.9)))
            t += ln + rnd.uniform(0.05, 0.25) * diag * 0.1
        s += px(step / 2) * rnd.uniform(0.8, 1.25)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.split()[3]), np.array(mask))))
    return lay


def outline(d, pts, width, closed=True, col=INK):
    seq = pts + [pts[0]] if closed else pts
    w = px(width)
    d.line(seq, fill=col, width=w, joint="curve")
    r = w / 2
    for x, y in seq:
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def finish(img):
    W, H = img.size
    return img.resize((W // SS, H // SS), Image.LANCZOS)


def shape(fill, poly_pts, size, seed, line=LINE, hatch_kw=None):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    pts = wobble(poly_pts, px(0.55), seed)
    ImageDraw.Draw(img).polygon(pts, fill=fill)
    img.alpha_composite(hatch(size, pts, seed + 1, **(hatch_kw or {})))
    outline(ImageDraw.Draw(img), pts, line)
    return img, pts


def cloth(k):
    """vải đuôi én phấp phới: mép trên, dưới lượn sóng càng xa cán càng mạnh, đuôi co giãn nhẹ"""
    ph = 2 * math.pi * k / FRAMES
    W, H = px(CL + 2 * M + AMP), px(CH + 2 * M + 2 * AMP)
    sx = 1 - 0.05 * (0.5 + 0.5 * math.cos(ph))

    def dy(x):
        return AMP * (x / CL) ** 0.85 * math.sin(2 * math.pi * x / LAM - ph)

    top, bot = [], []
    n = 40
    for i in range(n + 1):
        x = CL * i / n
        X = M + x * sx
        top.append((px(X), px(M + AMP + dy(x))))
        bot.append((px(X), px(M + AMP + CH + dy(x))))
    xe = M + CL * sx
    mid = (px(xe - NOTCH * sx), px(M + AMP + CH / 2 + dy(CL - NOTCH)))
    poly = top + [mid] + bot[::-1]
    img, pts = shape((255, 255, 255, 255), poly, (W, H), 100 + k)
    # một nếp gấp mảnh theo chỗ trũng của sóng (nét mực, không tô tối)
    d = ImageDraw.Draw(img)
    xf = ((ph / (2 * math.pi)) * LAM + LAM * 0.75) % LAM
    if 0.25 * CL < xf < 0.8 * CL:
        X = M + xf * sx
        y0, y1 = M + AMP + dy(xf) + CH * 0.2, M + AMP + dy(xf) + CH * 0.62
        fold = [(px(X + 2 * math.sin(t * 3)), px(y0 + (y1 - y0) * t)) for t in np.linspace(0, 1, 8)]
        outline(d, fold, 1.6, closed=False, col=(58, 40, 26, 150))
    # chỗ gắn: góc trên trái của vải (mép cán), theo tỉ lệ ảnh
    return finish(img), (M / (CL + 2 * M + AMP), 1 - (M + AMP) / (CH + 2 * M + 2 * AMP))


def pole():
    W, H = px(PW + 2 * M), px(PH + M)
    cx = (PW + 2 * M) / 2
    top = M * 0.5 + 2 * KR - 2
    tip = PH + M * 0.5
    body = [(px(cx - PW / 2), px(top)), (px(cx + PW / 2), px(top)), (px(cx + PW / 2), px(tip - 12)), (px(cx), px(tip)),
            (px(cx - PW / 2), px(tip - 12))]
    img, _ = shape((181, 128, 74, 255), body, (W, H), 7, line=4.2, hatch_kw={"alpha": (30, 60)})
    knob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ky = M * 0.5 + KR
    circ = [(px(cx + KR * math.cos(a)), px(ky + KR * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
    kimg, _ = shape((240, 190, 72, 255), circ, (W, H), 9, line=4.2, hatch_kw={"alpha": (26, 50)})
    img.alpha_composite(kimg)
    # chân (pivot) ở mũi nhọn: tỉ lệ từ dưới ảnh
    return finish(img), (0.5, (M * 0.5) / (PH + M))


def stone():
    W, H = px(OW + 2 * M), px(OH + 2 * M)
    cx, cy = (OW + 2 * M) / 2, (OH + 2 * M) / 2
    ell = [(px(cx + OW / 2 * math.cos(a)), px(cy + OH / 2 * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)]
    img, _ = shape((255, 255, 255, 255), ell, (W, H), 21, line=4.6, hatch_kw={"alpha": (18, 36)})
    return finish(img)


# bút chì: dài, rộng, mũi (đơn vị bản đồ), góc nghiêng (độ, mũi chúc xuống trái)
BL, BW, ANG = 200.0, 30.0, 38.0


def pencil():
    """bút chì màu nằm chéo: mũi xanh ngọc, gỗ vót, thân vàng có sọc mực, đai bạc, tẩy hồng; trả (ảnh, pivot mũi chì)"""
    a = math.radians(ANG)
    ux, uy = -math.cos(a), math.sin(a)      # dọc bút, từ đuôi về mũi (mũi chúc xuống trái)
    vx, vy = -uy, ux                         # ngang bút
    span_x = BL * abs(ux) + BW * abs(vx)
    span_y = BL * abs(uy) + BW * abs(vy)
    W, H = px(span_x + 2 * M), px(span_y + 2 * M)
    tip = (M + (BL * abs(ux) if ux < 0 else 0) * 0 + 0.0, 0.0)
    # gốc: mũi chì đặt sao cho cả bút nằm trong khung
    tx = M + BW * abs(vx) / 2
    ty = M + BL * abs(uy) + BW * abs(vy) / 2
    if ux < 0:
        tx = M + BW * abs(vx) / 2
    def P(u, v):  # u: khoảng cách từ mũi về đuôi, v: lệch ngang
        return (px(tx - ux * u + vx * v), px(ty - uy * u + vy * v))
    hw = BW / 2
    parts = [
        ((47, 163, 140, 255), [P(0, 0), P(22, -hw * 0.45), P(22, hw * 0.45)]),                     # mũi chì
        ((236, 200, 150, 255), [P(22, -hw * 0.45), P(46, -hw), P(46, hw), P(22, hw * 0.45)]),       # gỗ vót
        ((246, 196, 52, 255), [P(46, -hw), P(162, -hw), P(162, hw), P(46, hw)]),                   # thân
        ((196, 202, 210, 255), [P(162, -hw), P(178, -hw), P(178, hw), P(162, hw)]),                # đai
        ((242, 150, 160, 255), [P(178, -hw), P(BL - 6, -hw * 0.92), P(BL, 0), P(BL - 6, hw * 0.92), P(178, hw)]),  # tẩy
    ]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, (c, poly) in enumerate(parts):
        lay, _ = shape(c, poly, (W, H), 300 + i, line=3.6, hatch_kw={"alpha": (20, 40)})
        img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    for v in (-hw * 0.33, hw * 0.33):  # sọc dọc thân bút
        outline(d, [P(48, v), P(160, v)], 1.8, closed=False, col=(58, 40, 26, 170))
    for u in (167, 173):               # khía đai
        outline(d, [P(u, -hw + 2), P(u, hw - 2)], 1.6, closed=False, col=(58, 40, 26, 190))
    out = finish(img)
    return out, (tx / (span_x + 2 * M), 1 - ty / (span_y + 2 * M))


def tinted(img, rgb):
    a = np.array(img).astype(np.float32)
    a[..., :3] *= np.array(rgb, np.float32)[None, None, :] / 255.0
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def main():
    os.makedirs(OUT, exist_ok=True)
    frames = []
    for k in range(FRAMES):
        img, piv = cloth(k)
        img.save(os.path.join(OUT, "co_vai_%d.png" % k))
        frames.append(img)
    p, ppiv = pole()
    p.save(os.path.join(OUT, "co_can.png"))
    o = stone()
    o.save(os.path.join(OUT, "co_o.png"))
    print("vải %s, chỗ gắn (pivot) %.4f, %.4f" % (frames[0].size, piv[0], piv[1]))
    print("cán %s, chân (pivot) %.4f, %.4f; đỉnh vải dưới núm: %.1f đơn vị trên chân" % (p.size, ppiv[0], ppiv[1], PH - 2 * KR - 1))
    print("ô đá %s" % (o.size,))
    b, bpiv = pencil()
    b.save(os.path.join(OUT, "but_chi.png"))
    print("bút chì %s, mũi (pivot) %.4f, %.4f" % (b.size, bpiv[0], bpiv[1]))

    # tờ soi: 3 trạng thái trên nền cát, cỏ, đá, tuyết (cỡ 1 điểm ảnh = 1 đơn vị bản đồ); hàng cuối: 6 khung phấp phới
    cols = {"chưa mở": (77, 114, 184), "đã qua": (244, 191, 58), "đang đánh": (255, 77, 58)}
    grounds = [(226, 205, 160), (150, 186, 110), (150, 140, 128), (236, 240, 244)]
    Z = 1.0 / R
    cw, chh = 200, 230
    sheet = Image.new("RGBA", (cw * 6, chh * len(grounds) + 150), (255, 255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    for gi, g in enumerate(grounds):
        dr.rectangle([0, gi * chh, cw * 6, gi * chh + chh], fill=g + (255,))

    def sz(im, k):
        return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)

    for gi, g in enumerate(grounds):
        for si, (nm, c) in enumerate(cols.items()):
            for half in range(2):
                X0, Y0 = (si * 2 + half) * cw, gi * chh
                foot = (X0 + 60, Y0 + chh - 26)
                sc = Z * (1.23 if nm == "đang đánh" else 1.0)
                ov = sz(tinted(o, tuple(int(255 - (255 - v) * 0.45) for v in c)), sc)
                sheet.alpha_composite(ov, (foot[0] - ov.width // 2, foot[1] - ov.height // 2))
                fr = sz(tinted(frames[(gi + si + half * 3) % FRAMES], c), sc)
                pp = sz(p, sc)
                ctop = foot[1] - int((PH - 2 * KR - 1) * R * sc)
                sheet.alpha_composite(fr, (foot[0] - int(fr.width * piv[0]), ctop - int(fr.height * (1 - piv[1]))))
                sheet.alpha_composite(pp, (foot[0] - pp.width // 2, foot[1] - int(pp.height * (1 - ppiv[1]))))
    for k in range(FRAMES):
        sheet.alpha_composite(sz(tinted(frames[k], (255, 77, 58)), Z), (20 + k * 195, chh * len(grounds) + 20))
    sheet.convert("RGB").save(SOI)
    print("tờ soi:", os.path.abspath(SOI))


if __name__ == "__main__":
    main()
