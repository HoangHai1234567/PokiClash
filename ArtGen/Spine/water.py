"""Hình hạt NƯỚC sinh bằng thuật toán (bộ Thủy 2026-11-10), cùng quy ước fire.py: xám vân chì nhuộm được + bản trắng đặc cho lớp
mực, ngọn chĩa LÊN. Dùng tạm tới khi có ảnh GPT (build_hat.py gói hat_nuoc -> hat_gpt/wave_*, drop_*, crown_*, foam_*).

Nét nước của game (Assets/03 Art/Fx/tia_nuoc, no_nuoc, xoay_nuoc): dòng nước là các lưỡi sóng mập có MÀO CUỘN tròn kiểu sóng
đổ, bọt trắng ở mào, sọc xanh đậm / xanh trời / xanh nhạt chạy theo dòng, giọt hình giọt lệ.

- wave(seed): lưỡi sóng: chân tròn mập, thân dày, ngọn cuộn tròn sang một bên (mào sóng), có thể thêm cuộn nhỏ ở vai.
- drop(seed): giọt lệ, đuôi nhọn chĩa lên, bụng tròn ở dưới.
Bọt dùng fire.cloud, bong bóng dùng fire.blob.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from fire import SS, _down, _mask_to, _tongue_poly


def wave(seed, size=128, solid=False):
    rng = np.random.RandomState(9300 + seed)
    S = size * SS
    c = S / 2
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    side = 1 if seed % 2 == 0 else -1

    def tongue(x0, y0, length, ang0, hook, w0, base_r, pw=0.45):
        n = 32
        centre, widths = [], []
        x, y = x0, y0
        step = length / (n - 1)
        for i in range(n):
            t = i / (n - 1)
            ang = ang0 + hook * max(0.0, (t - 0.42) / 0.58) ** 1.4  # nửa trên cuộn lại như sóng đổ
            centre.append((x, y))
            widths.append(max(w0 * (1 - t) ** pw, w0 * 0.2))
            x += math.sin(ang) * step
            y -= math.cos(ang) * step
        d.polygon(_tongue_poly(centre, widths, S, base_r), fill=255)
        xe, ye = centre[-1]
        r = widths[-1]
        d.ellipse([xe - r, ye - r, xe + r, ye + r], fill=255)  # đầu mào tròn
        return centre, widths

    W0 = S * rng.uniform(0.16, 0.19)
    ctr, wid = tongue(c - side * S * 0.08, c + S * 0.3, S * 0.8, side * rng.uniform(0.0, 0.1), side * rng.uniform(2.3, 2.8), W0, W0 * 1.1)
    if rng.uniform() < 0.6:  # cuộn nhỏ ở vai, quay ra phía ngược lại
        i = int(len(ctr) * rng.uniform(0.2, 0.3))
        x, y = ctr[i]
        tongue(x - side * wid[i] * 0.5, y, S * rng.uniform(0.24, 0.3), -side * rng.uniform(0.5, 0.8), -side * rng.uniform(1.8, 2.3),
               wid[i] * 0.55, wid[i] * 0.4)
    return _down(_mask_to(m, solid), (c, c + S * 0.1))


def drop(seed, size=64, solid=False):
    rng = np.random.RandomState(9500 + seed)
    S = size * SS
    c = S / 2
    R = S * (0.2, 0.17, 0.19, 0.22)[seed % 4]
    tail = S * (0.42, 0.58, 0.5, 0.34)[seed % 4]
    cy = c + S * 0.18
    bend = rng.uniform(-0.06, 0.06) * S
    tip = (c + bend, cy - tail)
    pts = [(c + math.cos(a) * R, cy + math.sin(a) * R) for a in np.linspace(-0.45, math.pi + 0.45, 26)]
    lx, ly = pts[-1]
    rx, ry = pts[0]
    # hai cạnh hơi lõm về phía đuôi
    left = [(lx + (tip[0] - lx) * t + R * 0.18 * math.sin(math.pi * t), ly + (tip[1] - ly) * t) for t in (0.35, 0.7)]
    right = [(rx + (tip[0] - rx) * t - R * 0.18 * math.sin(math.pi * t), ry + (tip[1] - ry) * t) for t in (0.7, 0.35)]
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(pts + left + [tip] + right, fill=255)
    return _down(_mask_to(m, solid), (c, c))
