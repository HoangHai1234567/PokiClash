# -*- coding: utf-8 -*-
"""Làm trơn mép lẹm (chỗ con gốc khoét cắm vây) của mảnh thân rồng vây, chỉ trong hộp chọn: viền ngoài làm trơn Gauss theo chiều dài,
hình bóng mới = cũ ngoài hộp, trơn trong hộp (lấp chỗ lõm, gọt bướu). Phần thêm tô màu thân (inpaint từ thịt kề bên), mực cũ lọt vào
trong tô lại màu thân, kẻ viền mực ở mép mới quanh chỗ đổi.
    va_than.py <vào.png> <ra.png> <sigma> x0,y0,x1,y1 [x0,y0,x1,y1 ...]"""
import sys, numpy as np, cv2
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
src, dst, sig = sys.argv[1], sys.argv[2], float(sys.argv[3])
boxes = [tuple(int(v) for v in b.split(",")) for b in sys.argv[4:]]
A = np.array(Image.open(src).convert("RGBA"))
H, W = A.shape[:2]
a = A[..., 3] > 128
rgb = A[..., :3].copy()
cs, _ = cv2.findContours(a.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
r = int(sig * 3)
k = np.exp(-0.5 * (np.arange(-r, r + 1) / sig) ** 2); k /= k.sum()
sm = np.stack([np.convolve(np.r_[c[-r:, i], c[:, i], c[:r, i]], k, "valid") for i in (0, 1)], 1)
smask = np.zeros((H, W), np.uint8)
cv2.fillPoly(smask, [np.round(sm).astype(np.int32)], 1)
roi = np.zeros((H, W), bool)
for x0, y0, x1, y1 in boxes:
    roi[y0:y1, x0:x1] = True
moi = np.where(roi, smask.astype(bool), a)
them, bot = moi & ~a, a & ~moi
dark = (rgb.max(axis=2) < 90) & a
dt = cv2.distanceTransform(a.astype(np.uint8), cv2.DIST_L2, 5)
ink = float(np.median(dt[dark & (dt > 0) & (dt < 15)]) * 2) if dark.any() else 6.0
ink = max(4.0, min(ink, 10.0))
doi = them | bot
gan = cv2.dilate(doi.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(ink * 5) | 1,) * 2)).astype(bool) & roi
dark2 = (rgb.max(axis=2) < 150) & a
thit = a & ~dark2 & ~cv2.dilate(dark2.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
base = rgb.copy(); base[~thit] = 0
fill = cv2.inpaint(base, (~thit).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)   # chỉ loang từ thịt thân (điểm trong suốt không được làm màu nguồn)
out = rgb.copy()
to = moi & gan
out[to] = fill[to]
dm = cv2.distanceTransform(np.pad(moi.astype(np.uint8), 1), cv2.DIST_L2, 5)[1:-1, 1:-1]
vien = moi & (dm <= ink) & gan
mm = np.median(rgb[dark & (dt <= ink)], axis=0)
out[vien] = mm.astype(np.uint8)
al = A[..., 3].copy()
al[bot & gan] = 0
al[bot & ~gan] = 0
al[roi & ~moi] = 0
al[them] = 255
edge = moi & gan & (dm < 1.6)
al[edge] = np.clip(dm[edge] * 160, 0, 255).astype(np.uint8)
Image.fromarray(np.dstack([out, al]).astype(np.uint8), "RGBA").save(dst)
print(f"{src.split('/')[-1]}: thêm {int(them.sum())} px, gọt {int(bot.sum())} px, nét mực ~{ink:.1f} px")
