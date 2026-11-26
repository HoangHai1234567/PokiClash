# Cắt tờ đồ bàn (do_ban_1k.png, Magnific GPT 2.6, nền trắng) thành từng món, nền trong suốt: lưng bài, mặt bài trắng, cỗ bài,
# 4 chip đơn (đỏ, vàng, xanh dương, xanh lá), chồng chip đỏ, chồng chip xanh. Ra do_ban/<tên>.png (cắt sát, chừa 4 px).
# Chạy: py -3 -I cat_do_ban.py
import os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "do_ban")
os.makedirs(OUT, exist_ok=True)

im = np.array(Image.open(os.path.join(HERE, "do_ban_1k.png")).convert("RGB")).astype(np.int16)
h, w, _ = im.shape
white = (im.min(axis=2) > 228) & (np.abs(im[..., 0] - im[..., 2]) < 18)
# nền = vùng trắng nối với mép ảnh
lab, _ = ndimage.label(white)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
fg = ~bg
fg = ndimage.binary_opening(fg, iterations=1)
objs, n = ndimage.label(fg)
boxes = ndimage.find_objects(objs)
items = []
for i, sl in enumerate(boxes):
    area = (objs[sl] == i + 1).sum()
    if area < 2000:
        continue
    ys, xs = sl
    items.append((ys.start, xs.start, ys.stop, xs.stop, i + 1))
# hai hàng: trên (3 món), dưới (6 món), trái sang phải
items.sort(key=lambda b: (0 if (b[0] + b[2]) / 2 < h / 2 else 1, b[1]))
names = ["la_lung", "la_mat", "co_bai", "chip_do", "chip_vang", "chip_xanh", "chip_la", "chong_do", "chong_xanh"]
print(len(items), "món")
rgb = np.array(Image.open(os.path.join(HERE, "do_ban_1k.png")).convert("RGB"))
for name, (y0, x0, y1, x1, k) in zip(names, items):
    m = ndimage.binary_fill_holes(objs == k)
    # mép mềm 1 px
    a = ndimage.gaussian_filter(m.astype(np.float32), 0.6)
    y0, x0 = max(0, y0 - 4), max(0, x0 - 4)
    y1, x1 = min(h, y1 + 4), min(w, x1 + 4)
    rgba = np.dstack([rgb[y0:y1, x0:x1], (np.clip(a[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, name + ".png"))
    print(name, x1 - x0, "x", y1 - y0)
