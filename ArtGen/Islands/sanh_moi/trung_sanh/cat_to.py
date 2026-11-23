# Cắt tờ sinh vật easter egg sảnh (to_sinh_vat_1.png, Magnific GPT 2.6, 2026-11-23) thành hình rời anim_<tên>.png
# Ra: trung_sanh/cat/anim_*.png (chép vào Assets/03 Art/Islands/Anim/). Chạy: py -3 -I cat_to.py [--chep]
import os
import shutil
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ANIM = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Assets", "03 Art", "Islands", "Anim"))
NAMES = [["ca", "ca_vang", "cua"], ["ca_voi", "duoi_ca_voi", "voi_phun"], ["chai", "da_lua", "rua"]]
MAXW = 180

im = Image.open(os.path.join(HERE, "to_sinh_vat_1.png")).convert("RGBA")
a = np.asarray(im)
H, W = a.shape[:2]
out = os.path.join(HERE, "cat")
os.makedirs(out, exist_ok=True)
for r in range(3):
    for c in range(3):
        x0, y0, x1, y1 = c * W // 3, r * H // 3, (c + 1) * W // 3, (r + 1) * H // 3
        sub = a[y0:y1, x0:x1].copy()
        al = sub[..., 3] > 24
        lab, n = ndimage.label(ndimage.binary_dilation(al, iterations=3))
        sizes = ndimage.sum(al, lab, range(1, n + 1))
        keep = np.isin(lab, np.where(sizes >= 30)[0] + 1)
        sub[~keep] = 0
        ys, xs = np.nonzero(sub[..., 3] > 8)
        p = 4
        crop = Image.fromarray(sub).crop((max(0, xs.min() - p), max(0, ys.min() - p), min(sub.shape[1], xs.max() + p + 1), min(sub.shape[0], ys.max() + p + 1)))
        if max(crop.size) > MAXW:
            k = MAXW / max(crop.size)
            crop = crop.resize((round(crop.width * k), round(crop.height * k)), Image.LANCZOS)
        name = "anim_" + NAMES[r][c] + ".png"
        crop.save(os.path.join(out, name))
        print(name, crop.size)
        if "--chep" in sys.argv:
            shutil.copy(os.path.join(out, name), os.path.join(ANIM, name))
