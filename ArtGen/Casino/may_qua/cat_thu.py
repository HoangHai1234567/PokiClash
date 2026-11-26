# Cắt hình chính (nửa trái tờ concept) của ba hướng ra PNG nền trong suốt cho trang thử chuyển động (xem.html).
# Nền giấy kem loang từ mép vào (flood fill), không đụng mảng kem bên trong máy. Chạy: py -3 -I cat_thu.py
import os, sys
from collections import deque
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {"A": "huong_A_chuong_vang.png", "B": "huong_B_hau_an.png", "C": "huong_C_hu_bi.png"}
X1 = 900  # hình chính nằm trong 0..X1

def cut(k, name):
    im = Image.open(os.path.join(HERE, "concept", name)).convert("RGB").crop((0, 0, X1, 1024))
    a = np.asarray(im).astype(np.int32)
    h, w, _ = a.shape
    bg = np.median(a[:12, :12].reshape(-1, 3), axis=0)
    d = np.abs(a - bg).sum(axis=2)
    paper = d < 60
    seen = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if paper[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if paper[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and paper[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True; q.append((yy, xx))
    alpha = np.where(seen, 0, 255).astype(np.uint8)
    out = np.dstack([a.astype(np.uint8), alpha])
    ys, xs = np.where(alpha > 0)
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    res = Image.fromarray(out, "RGBA").crop(box)
    os.makedirs(os.path.join(HERE, "thu"), exist_ok=True)
    res.save(os.path.join(HERE, "thu", "may_%s.png" % k))
    print(k, "box", box, "size", res.size)

for k, n in SRC.items():
    cut(k, n)
