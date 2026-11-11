# -*- coding: utf-8 -*-
"""Sơ đồ bố cục đầu rắn sừng (dạng 1) để đính vào prompt lượt sửa: hướng quay ba phần tư sang phải nhìn từ trên xuống, chỗ đặt hai
mắt, mảng màu, đường miệng chữ U có khấc ở mõm, chỗ mọc hai sừng. Hình phẳng tự vẽ bằng mã (không phải ảnh của game nào); GPT chỉ
lấy bố cục, không lấy nét. Bố cục học từ cách dựng đầu của con gốc (ghi chú inbox/ran_sung_ghichu.md).

    py -3 -I ArtGen/Spine/ran_sung_bo_cuc.py        →  inbox/ran_sung_1/mau/dau_bo_cuc.png (700 × 700, nền trắng)
"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "inbox", "ran_sung_1", "mau", "dau_bo_cuc.png")
S = 3                       # vẽ to gấp 3 rồi thu lại cho mượt
W, H = 700, 700
OY = 70                     # dời xuống cho đủ chỗ vẽ sừng

BLUE, PALE, BLACK, AMBER, INK = (46, 111, 216), (221, 240, 247), (38, 37, 44), (255, 169, 46), (43, 33, 24)
GREY = (91, 91, 104)


def cr(pts, closed, n=16):
    """Đường Catmull-Rom qua các điểm."""
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = pts[(i - 1) % m] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if (closed or i + 2 < m) else p2
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)))
    if not closed:
        out.append(pts[-1])
    return out


def sc(pts):
    return [(x * S, (y + OY) * S) for x, y in pts]


def ellipse(cx, cy, rx, ry, deg, n=72):
    a = math.radians(deg)
    return [(cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a),
             cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
            for t in (2 * math.pi * i / n for i in range(n))]


def line(d, pts, w, col=INK):
    p = sc(pts)
    d.line(p, fill=col, width=w * S, joint="curve")
    r = w * S / 2
    for x, y in (p[0], p[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def main():
    im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    d = ImageDraw.Draw(im)

    # viền đầu: vòm rộng ở trên, rộng nhất ngang mắt, thon xuống mõm tù ở dưới phải
    head = cr([(340, 52), (470, 72), (565, 150), (612, 262), (624, 352), (606, 440), (556, 508), (478, 548), (392, 556),
               (300, 532), (190, 468), (104, 388), (62, 290), (82, 182), (150, 100), (240, 60)], True)
    # hai sừng (vẽ trước, đầu đè lên gốc sừng)
    horn_l = cr([(96, 196), (60, 120), (64, 30), (112, -52), (118, 10), (150, 62), (212, 96), (170, 150)], True)
    horn_r = cr([(492, 92), (520, 40), (566, 6), (604, -58), (628, 8), (622, 84), (590, 158), (540, 130)], True)
    for hp in (horn_l, horn_r):
        d.polygon(sc(hp), fill=BLACK)
        line(d, hp + hp[:1], 7)
    line(d, [(88, 96), (120, 80)], 3, GREY)
    line(d, [(82, 124), (132, 104)], 3, GREY)
    line(d, [(560, 74), (604, 66)], 3, GREY)
    line(d, [(552, 104), (608, 98)], 3, GREY)

    d.polygon(sc(head), fill=BLUE)

    # mảng nhạt: má dưới mắt gần (vòng lên mép trái mắt), môi trên, hàm dưới; mảng lam chạy xuống giữa hai mắt, đáy tròn trên miệng
    eye_l = ellipse(244, 360, 98, 92, -14)
    eye_r = ellipse(582, 352, 45, 88, 6)
    top = cr([(104, 388), (150, 430), (200, 452), (262, 462), (330, 448), (364, 442), (392, 470), (430, 490), (470, 490),
              (505, 470), (530, 442), (562, 438), (616, 422)], False)
    bot = [p for p in head if p[1] > 380]
    bot.sort(key=lambda p: -p[0])                     # từ phải sang trái dọc viền đáy
    d.polygon(sc(top + bot), fill=PALE)
    line(d, head + head[:1], 7)

    # mắt: hạnh to, mí lam dày xếch vào giữa mặt, con ngươi dọc nhìn xuống phải, một chấm sáng
    for eye, lid, pup, dot in (
            (eye_l, [(120, 306), (346, 380), (372, 240), (110, 240)], (270, 398, 13, 44), (236, 372)),
            (eye_r, [(528, 378), (636, 316), (650, 240), (516, 240)], (588, 396, 9, 40), (572, 368))):
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(sc(eye), fill=255)
        layer = Image.new("RGB", im.size, AMBER)
        ld = ImageDraw.Draw(layer)
        px, py, pw, ph = pup
        ld.ellipse([(px - pw) * S, (py + OY - ph) * S, (px + pw) * S, (py + OY + ph) * S], fill=(20, 18, 16))
        ld.ellipse([(dot[0] - 9) * S, (dot[1] + OY - 9) * S, (dot[0] + 9) * S, (dot[1] + OY + 9) * S], fill=(255, 255, 255))
        ld.polygon(sc(lid), fill=BLUE)
        ld.line(sc(lid[:2]), fill=INK, width=10 * S)
        im.paste(layer, (0, 0), mask)
        line(d, eye + eye[:1], 7)

    # miệng: đường cong chữ U ôm đáy mặt, khấc nhỏ ở mõm (lệch phải ~70 % bề ngang đầu); hàm dưới là vành nhạt mỏng bên dưới
    mouth_a = cr([(176, 458), (250, 500), (330, 528), (404, 538), (432, 532)], False)
    notch = [(432, 532), (456, 508), (482, 530)]
    mouth_b = cr([(482, 530), (530, 520), (584, 484), (614, 440)], False)
    line(d, mouth_a, 6)
    line(d, notch, 6)
    line(d, mouth_b, 6)
    # hai lỗ mũi khe
    line(d, [(430, 470), (438, 484)], 4)
    line(d, [(486, 468), (478, 482)], 4)

    im = im.resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    im.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
