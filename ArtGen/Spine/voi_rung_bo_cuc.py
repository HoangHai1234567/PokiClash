# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của voi rừng (mã làm việc voi_rung, tướng thứ 5 đảo Mộc, 2026-11-12): hình phẳng tự vẽ bằng mã, đính cho GPT để
lấy chỗ đặt, cỡ, thứ tự chồng của từng bộ phận (dáng nghỉ dễ rig). Thiết kế là của mình; không dùng ảnh của game nào.

    py -3 -I ArtGen/Spine/voi_rung_bo_cuc.py        -> inbox/voi_rung_2/mau/bo_cuc.png (+ bo_cuc_luoi.png có kẻ lưới toạ độ)

Hình học ở đây cũng là nguồn toạ độ cho prompt (build_voi_rung.py) và cho rig (voi_rung.py): sửa một chỗ.
"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1536, 1024
DX, DY = -55, 0          # dời cả con cho cân khung
GROUND = 940

# màu (R, G, B)
DA = (140, 156, 168)       # da xám lam  #8C9CA8
VO = (122, 86, 56)         # vỏ cây      #7A5638
NGA = (242, 230, 192)      # ngà, móng   #F2E6C0
REU = (111, 174, 75)       # rêu         #6FAE4B
LA = (63, 138, 69)         # lá          #3F8A45
GAN = (46, 107, 54)        # gân lá      #2E6B36
HOA = (244, 194, 60)       # hoa         #F4C23C
NHUY = (232, 134, 46)      # nhuỵ        #E8862E
MAT = (240, 165, 58)       # mắt         #F0A53A
MUC = (43, 33, 24)         # mực         #2B2118


def hx(c):
    return "#%02X%02X%02X" % c


def P(pts):
    return [(x + DX, y + DY) for x, y in pts]


# ---- hình học (toạ độ khung 1536 x 1024, trước khi dời DX)
BODY = [(400, 520), (470, 430), (600, 372), (760, 338), (900, 362), (990, 430), (1030, 560), (1000, 690), (900, 760),
        (700, 785), (520, 770), (415, 700), (385, 600)]
MOSS_LOW = [(388, 585), (450, 610), (512, 575), (585, 615), (655, 578), (735, 618), (812, 578), (885, 604), (945, 560),
            (1000, 470)]     # mép dưới tấm rêu (lượn sóng), trái -> phải
TREE_TRUNK = [(712, 350), (700, 240), (735, 240), (758, 350)]
CANOPY = [(715, 165, 88), (648, 202, 60), (782, 198, 62)]
FLOWERS = [(520, 505), (648, 470), (858, 472)]
HEAD = [(950, 445), (975, 320), (1052, 248), (1150, 238), (1230, 300), (1260, 410),          # gáy -> đỉnh -> trán
        (1276, 520), (1300, 640), (1322, 735), (1360, 792), (1400, 778),                       # mép trước vòi
        (1432, 752), (1440, 800), (1400, 846),                                                 # chóp vòi (cong ra trước, hơi lên)
        (1318, 852), (1258, 792), (1226, 690), (1204, 612),                                    # mép sau vòi
        (1168, 644), (1108, 652), (1040, 612), (982, 540)]                                     # cằm -> má
TRUNK_AXIS = [(1228, 505), (1252, 620), (1274, 728), (1312, 806), (1372, 816), (1418, 786)]
HELMET = [(965, 345), (1035, 255), (1150, 238), (1230, 300), (1258, 392), (1180, 366), (1090, 372), (1005, 398)]
EYE = (1166, 440, 26)
TUSK_AXIS = [(1150, 588), (1238, 676), (1340, 688), (1414, 618), (1428, 525)]
TUSK_W = [70, 64, 52, 34, 6]
EAR = [(1028, 384), (1076, 468), (1066, 570), (1000, 662), (940, 602), (914, 500), (950, 410)]
EAR_FAR = [(968, 345), (950, 262), (1000, 206), (1052, 262), (1044, 305)]
LEGS = {  # tên: (x0, x1, y_tren, y_dat, phình đùi)
    "chan_gt": (885, 1015, 640, GROUND, 6),
    "chan_gs": (455, 595, 612, GROUND, 14),
    "chan_xt": (1016, 1114, 700, GROUND - 14, 0),
    "chan_xs": (602, 704, 700, GROUND - 14, 0),
}
TAIL = [(394, 582), (344, 650), (320, 722)]
TAIL_LEAVES = [(320, 722, 262, 800), (320, 722, 318, 822), (320, 722, 372, 792)]


def spline(pts, n=14, closed=True):
    """Catmull-Rom qua các điểm."""
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = pts[(i - 1) % m] if closed or i > 0 else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if closed or i + 2 < m else pts[i + 1]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    if not closed:
        out.append(tuple(pts[-1]))
    return out


def ribbon(axis, widths):
    """dải thon dọc trục: trả đa giác."""
    ax = spline(axis, 12, closed=False)
    n = len(ax)
    L, R = [], []
    for i, (x, y) in enumerate(ax):
        x0, y0 = ax[max(i - 1, 0)]
        x1, y1 = ax[min(i + 1, n - 1)]
        d = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = -(y1 - y0) / d, (x1 - x0) / d
        u = i / (n - 1) * (len(widths) - 1)
        k = min(int(u), len(widths) - 2)
        w = (widths[k] * (1 - (u - k)) + widths[k + 1] * (u - k)) / 2
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    return L + R[::-1]


def leaf(x0, y0, x1, y1, wide=0.34):
    d = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    nx, ny = -uy, ux
    pts = []
    for t in [i / 16 for i in range(17)]:
        w = wide * d * math.sin(math.pi * t) ** 0.8
        pts.append((x0 + ux * d * t + nx * w, y0 + uy * d * t + ny * w))
    for t in [i / 16 for i in range(16, -1, -1)]:
        w = wide * d * math.sin(math.pi * t) ** 0.8
        pts.append((x0 + ux * d * t - nx * w, y0 + uy * d * t - ny * w))
    return pts


def leg_poly(x0, x1, yt, yb, bulge):
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    pts = []
    for a in range(180, 361, 12):       # chỏm tròn trên
        pts.append((cx + (r + bulge) * math.cos(math.radians(a)), yt + r * 0.75 + r * 0.75 * math.sin(math.radians(a))))
    pts += [(x1 + 2, yb - 60), (x1 + 12, yb - 14), (x1 + 10, yb), (x0 - 8, yb), (x0 - 10, yb - 14), (x0 - 2, yb - 60)]
    return pts


def ve(luoi=False, chi=None):
    """chi: tập nhóm cần vẽ (None = cả con): tai_x, nga_x, chan_x, duoi, cay, than, chan_g, dau, nga_g, tai_g (dựng mảnh thử cho rig)."""
    S = 2
    ok = lambda g: chi is None or g in chi  # noqa: E731
    im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    d = ImageDraw.Draw(im)

    def poly(pts, fill, out=6):
        pp = [(x * S, y * S) for x, y in P(pts)]
        d.polygon(pp, fill=fill)
        if out:
            d.line(pp + [pp[0]], fill=MUC, width=out * S, joint="curve")

    def circ(x, y, r, fill, out=6):
        x, y = x + DX, y + DY
        d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill, outline=MUC if out else None, width=out * S)

    def line(pts, col, w):
        d.line([(x * S, y * S) for x, y in P(pts)], fill=col, width=w * S, joint="curve")

    def nails(x0, x1, yb, n=3):
        step = (x1 - x0 + 14) / n
        for i in range(n):
            cx = x0 - 4 + step * (i + 0.5)
            d.pieslice([(cx - step * 0.36 + DX) * S, (yb - 34 + DY) * S, (cx + step * 0.36 + DX) * S, (yb + 30 + DY) * S], 180, 360,
                       fill=NGA, outline=MUC, width=4 * S)

    # tai xa, ngà xa
    if ok('tai_x'):
        poly(spline(EAR_FAR, 10), LA)
    far = [(x + 40, y - 40) for x, y in TUSK_AXIS]
    if ok('nga_x'):
        poly(ribbon(far, [w * 0.92 for w in TUSK_W]), NGA)
    # chân xa
    for n in (("chan_xs", "chan_xt") if ok('chan_x') else ()):
        x0, x1, yt, yb, bu = LEGS[n]
        poly(leg_poly(x0, x1, yt, yb, bu), DA)
        nails(x0, x1, yb)
    # đuôi
    if ok('duoi'):
        line(spline(TAIL, 10, closed=False), MUC, 30)
        line(spline(TAIL, 10, closed=False), DA, 18)
        for a in TAIL_LEAVES:
            poly(leaf(*a), LA, 5)
    # cây trên lưng
    if ok('cay'):
        poly(TREE_TRUNK, VO)
        for x, y, r in CANOPY:
            circ(x, y, r, LA)
        for x, y, r in CANOPY:
            circ(x, y, r - 5, LA, 0)
        for x, y in ((690, 150), (760, 190), (655, 215)):
            circ(x, y, 13, HOA, 4)
    # thân + rêu
    if ok('than'):
        body = spline(BODY, 14)
        poly(body, DA)
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon([(x * S, y * S) for x, y in P(body)], fill=255)
        moss = Image.new("L", im.size, 0)
        md = ImageDraw.Draw(moss)
        low = spline(MOSS_LOW, 10, closed=False)
        md.polygon([(x * S, y * S) for x, y in P([(360, 300), (1040, 300), (1040, 470)] + low[::-1])], fill=255)
        moss = ImageChops.multiply(moss, mask)
        im.paste(REU, (0, 0), moss)
        d = ImageDraw.Draw(im)
        line(low, MUC, 5)
        line(body + [body[0]], MUC, 6)
        for x, y in FLOWERS:
            for a in range(0, 360, 72):
                circ(x + 15 * math.cos(math.radians(a)), y + 15 * math.sin(math.radians(a)), 11, HOA, 3)
            circ(x, y, 9, NHUY, 3)
    # chân gần
    for n in (("chan_gs", "chan_gt") if ok('chan_g') else ()):
        x0, x1, yt, yb, bu = LEGS[n]
        poly(leg_poly(x0, x1, yt, yb, bu), DA)
        nails(x0, x1, yb)
    # đầu liền vòi
    if ok('dau'):
        head = spline(HEAD, 12)
        poly(head, DA)
        hm = Image.new("L", im.size, 0)
        ImageDraw.Draw(hm).polygon([(x * S, y * S) for x, y in P(head)], fill=255)
        hel = Image.new("L", im.size, 0)
        ImageDraw.Draw(hel).polygon([(x * S, y * S) for x, y in P(spline(HELMET, 10))], fill=255)
        hel = ImageChops.multiply(hel, hm)
        im.paste(VO, (0, 0), hel)
        d = ImageDraw.Draw(im)
        hl = spline(HELMET, 10)
        line(hl[len(hl) * 4 // 8 - 4:] + [hl[0]], MUC, 5)
        line(head + [head[0]], MUC, 6)
        for i in range(1, 5):   # nếp vòi
            u = i / 5
            ax = spline(TRUNK_AXIS, 12, closed=False)
            x, y = ax[int(u * (len(ax) - 1))]
            line([(x - 26, y + 4), (x + 4, y - 2)], (104, 118, 130), 4)
        ex, ey, er = EYE
        circ(ex, ey, er, MAT, 5)
        circ(ex + 3, ey + 1, 12, MUC, 0)
        circ(ex + 8, ey - 6, 4, (255, 255, 255), 0)
        line([(1112, 392), (1210, 420)], MUC, 10)      # mày xếch
        line([(1120, 630), (1168, 626)], MUC, 5)      # khe miệng
        circ(1424, 784, 9, MUC, 0)                    # lỗ vòi
    # ngà gần + đai vỏ ở gốc
    if ok('nga_g'):
        tusk = ribbon(TUSK_AXIS, TUSK_W)
        poly(tusk, NGA)
        poly(ribbon(spline(TUSK_AXIS, 10, closed=False)[:9], [70, 68]), VO, 5)
    # tai gần
    if ok('tai_g'):
        ear = spline(EAR, 12)
        poly(ear, LA)
        line([(1022, 402), (1010, 520), (1000, 640)], GAN, 5)
        for (a, b) in (((1014, 470), (960, 440)), ((1010, 530), (950, 520)), ((1012, 480), (1060, 470)), ((1008, 550), (1050, 560))):
            line([a, b], GAN, 4)
    im = im.resize((W, H), Image.LANCZOS)
    if luoi:
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
        for x in range(0, W, 50):
            d.line([(x, 0), (x, H)], fill=(255, 0, 0) if x % 100 == 0 else (255, 170, 170), width=1)
            if x % 100 == 0:
                d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=f)
        for y in range(0, H, 50):
            d.line([(0, y), (W, y)], fill=(255, 0, 0) if y % 100 == 0 else (255, 170, 170), width=1)
            if y % 100 == 0:
                d.text((2, y + 2), str(y), fill=(200, 0, 0), font=f)
    return im


def main():
    out = os.path.join(HERE, "inbox", "voi_rung_2", "mau")
    os.makedirs(out, exist_ok=True)
    ve().save(os.path.join(out, "bo_cuc.png"))
    ve(True).save(os.path.join(out, "bo_cuc_luoi.png"))
    print(os.path.join(out, "bo_cuc.png"))


if __name__ == "__main__":
    main()
