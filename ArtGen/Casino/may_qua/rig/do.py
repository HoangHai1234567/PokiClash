# Đo nhanh các tờ gen (in khung từng cụm) để viết chuan_bi.py. Chạy: py -3 -I do.py
import os, sys
import numpy as np, cv2
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

def key(path):
    a = np.asarray(Image.open(os.path.join(HERE, path)).convert("RGB")).astype(float)
    bg = np.median(a[:20, :20].reshape(-1, 3), axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(2))
    return a, np.clip((d - 60) / 40, 0, 1), bg

def comps(al, minarea=300, dil=1):
    m = (al > 0.5).astype(np.uint8)
    if dil > 1: m = cv2.dilate(m, np.ones((dil, dil), np.uint8))
    n, lab, st, ce = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, ar = st[i]
        if ar >= minarea: out.append((int(x), int(y), int(x + w), int(y + h), int(ar)))
    return sorted(out, key=lambda c: (c[1] // 100, c[0]))

for p in ("L1_goc.png", "L2_than.png", "L3_chi.png", "L4_mat.png", "L5_mieng.png"):
    a, al, bg = key(p)
    print(p, "nền", bg.round().tolist())
    for c in comps(al, dil=9 if p.startswith(("L4", "L5")) else 1): print("   ", c)
# IoU thân L2 trong L1
a1, al1, _ = key("L1_goc.png"); a2, al2, _ = key("L2_than.png")
m1, m2 = al1 > 0.5, al2 > 0.5
print("L2 nằm trong L1:", round((m1 & m2).sum() / m2.sum(), 4))
d = np.abs(a1 - a2).sum(2)
same = (d < 60) & m2
print("điểm thân trùng màu L1:", round(same.sum() / m2.sum(), 3))
# ô cuộn: vùng kem trong khung (L2)
r, g, b = a2[..., 0], a2[..., 1], a2[..., 2]
cream = (r > 235) & (g > 215) & (b > 150) & (b < 215) & m2
n, lab, st, ce = cv2.connectedComponentsWithStats(cream.astype(np.uint8), 8)
for i in range(1, n):
    if st[i, 4] > 8000: print("kem", st[i].tolist())
yellow = (r > 230) & (g > 190) & (b < 90) & m2
