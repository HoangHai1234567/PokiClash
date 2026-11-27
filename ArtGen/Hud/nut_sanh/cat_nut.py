# Cắt tờ huy hiệu nút sảnh (nut_sanh_v1.png: Magnific GPT 2.6 nền trong, 3 huy hiệu một hàng, 2026-11-27; người dùng: icon nút
# bánh răng, Hang Tiềm Năng, Sổ Phép "bị chìm vào phần back, không đẹp và nhỏ quá, gen lại cho nổi bật hơn").
# Ba huy hiệu chạm nhau ở viền sticker: cắt ở cột ít điểm ảnh nhất giữa hai huy hiệu, rồi cắt tròn theo khung từng cái.
# Ra Assets/03 Art/Hud/{nut_so_tay,nut_hang,nut_so_phep}.png, 256 x 256 (hình tròn chạm mép, tâm giữa ảnh).
# Chạy: py -3 -I ArtGen/Hud/nut_sanh/cat_nut.py
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Hud")
NAMES = ["nut_so_tay", "nut_hang", "nut_so_phep"]
SIDE = 256

im = Image.open(os.path.join(HERE, "nut_sanh_v1.png")).convert("RGBA")
a = np.array(im)
alpha = a[..., 3]
col = (alpha > 16).sum(0)
w = a.shape[1]
cuts = [0]
for k in (1, 2):
    lo, hi = int(w * k / 3 - 60), int(w * k / 3 + 60)
    cuts.append(lo + int(col[lo:hi].argmin()))
cuts.append(w)
for i, name in enumerate(NAMES):
    x0, x1 = cuts[i], cuts[i + 1]
    s = a[:, x0:x1].copy()
    m = s[..., 3] > 16
    ys, xs = np.where(m)
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    r = max(ys.max() - ys.min(), xs.max() - xs.min()) / 2 + 1
    yy, xx = np.mgrid[0:s.shape[0], 0:s.shape[1]]
    d = np.hypot(yy - cy, xx - cx)
    s[..., 3] = (s[..., 3] * np.clip(r + 1 - d, 0, 1)).astype(np.uint8)  # bỏ phần sót của huy hiệu bên cạnh, mép mềm 1 px
    side = int(np.ceil(2 * r + 4))
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(Image.fromarray(s), (int(round(side / 2 - cx)), int(round(side / 2 - cy))))
    out = sq.resize((SIDE, SIDE), Image.LANCZOS)
    p = os.path.join(OUT, name + ".png")
    out.save(p, optimize=True)
    print(name, f"cột {x0}-{x1}, tâm ({cx + x0:.0f}, {cy:.0f}), bán kính {r:.0f} -> {p}")
