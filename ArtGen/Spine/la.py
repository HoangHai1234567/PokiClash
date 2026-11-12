# -*- coding: utf-8 -*-
"""Hình hạt LÁ cho bộ Mộc của lớp hạt chồng lớp phẳng (2026-11-12, tướng tinh linh rừng: chiêu mana há mồm phun lá).
Cùng quy ước với fire.py / water.py: ảnh xám có vân chì nhuộm bằng Image.color + bản trắng đặc làm lớp mực, ngọn chĩa LÊN.

- leaf(seed): lá bầu nhọn đầu, hơi lệch, có gân giữa sẫm hơn (nhuộm xong thành gân đậm).

    py -3 -I ArtGen/Spine/la.py            ghi thẳng hat_leaf_<i>.png, hat_leafs_<i>.png vào Assets/03 Art/Fx/Hat (không đụng ảnh hạt khác)
    py -3 -I ArtGen/Spine/la.py xem <ra>   tờ xem thử (nhuộm lục trên nền xám)
Sau đó chạy lại hai menu Unity gán ảnh hạt: "PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)" và "…Hộp chi tiết tướng: hạt lửa + nút Mana".
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fire  # noqa: E402
from lightning import SS, _down  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))


def leaf(seed, size=64, solid=False):
    rng = np.random.RandomState(7300 + seed)
    S = size * SS
    c = S / 2
    L = S * (0.80, 0.72, 0.84, 0.76)[seed % 4]              # dài
    Wd = S * (0.36, 0.40, 0.32, 0.38)[seed % 4]             # rộng
    lech = (0.10, -0.08, 0.06, -0.12)[seed % 4]             # sống lá cong lệch
    y0, y1 = c + L / 2, c - L / 2                           # cuống ở dưới, ngọn ở trên
    n = 28
    mid = [(c + lech * S * math.sin(math.pi * t) * 0.5, y0 + (y1 - y0) * t) for t in np.linspace(0, 1, n)]
    wid = [Wd / 2 * (math.sin(math.pi * t ** 0.78) ** 0.9) for t in np.linspace(0, 1, n)]     # bầu ở nửa dưới, thon nhọn về ngọn
    left = [(x - w, y) for (x, y), w in zip(mid, wid)]
    right = [(x + w * rng.uniform(0.92, 1.0), y) for (x, y), w in zip(mid, wid)]
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    d.polygon(left + right[::-1], fill=255)
    d.line([mid[0], (mid[0][0], y0 + S * 0.07)], fill=255, width=max(2, int(S * 0.035)))      # cuống ngắn
    im = fire._mask_to(m, solid)
    if not solid:                                           # gân giữa + hai gân bên: sẫm hơn nền (nhuộm xong vẫn thấy)
        g = ImageDraw.Draw(im)
        g.line(mid[2:-3], fill=(150, 150, 150, 255), width=max(2, int(S * 0.028)))
        for t, s in ((0.34, 1), (0.34, -1), (0.58, 1), (0.58, -1)):
            i = int(t * (n - 1))
            x, y = mid[i]
            g.line([(x, y), (x + s * wid[i] * 0.62, y - S * 0.10)], fill=(168, 168, 168, 255), width=max(2, int(S * 0.02)))
        a = np.asarray(im).copy()
        a[..., 3] = np.asarray(m)
        im = Image.fromarray(a, "RGBA")
    return _down(im, (c, c))


def xuat():
    for i in range(4):
        for ten, solid in ((f"hat_leaf_{i}.png", False), (f"hat_leafs_{i}.png", True)):
            im = leaf(i, solid=solid)[0]
            if max(im.size) > 128:
                im = im.resize((round(im.width * 128 / max(im.size)), round(im.height * 128 / max(im.size))), Image.LANCZOS)
            im.save(os.path.join(OUT, ten), optimize=True)
            print(os.path.join(OUT, ten), im.size)


def xem(ra):
    os.makedirs(ra, exist_ok=True)
    sh = Image.new("RGB", (4 * 150 + 20, 330), (150, 150, 150))
    for i in range(4):
        f, s = leaf(i)[0], leaf(i, solid=True)[0]
        for j, col in enumerate(((62, 140, 88), (156, 204, 92))):
            big = s.resize((s.width + 8, s.height + 8))
            ink = Image.new("RGBA", big.size, (43, 33, 24, 255))
            sh.paste(ink, (10 + i * 150 - 4, 10 + j * 160 - 4), big)
            t = np.asarray(f).astype(np.float32)
            t[..., :3] = t[..., :3] * np.array(col) / 255.0
            t = Image.fromarray(t.astype(np.uint8), "RGBA")
            sh.paste(t, (10 + i * 150, 10 + j * 160), t)
    sh.save(os.path.join(ra, "la_xem.png"))
    print(os.path.join(ra, "la_xem.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:2] == ["xem"]:
        xem(sys.argv[2])
    else:
        xuat()
