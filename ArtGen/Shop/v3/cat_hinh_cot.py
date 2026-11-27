# Cắt tờ hình vẽ tay nét trắng (hinh_cot_goc/to_hinh.png, GPT 2.6 2026-11-27: sao, lấp lánh, quái vật nhỏ, bi, trứng...) thành từng mảnh
# cho nền cột trái màn cửa hàng (ve_ui.py side_column). Bỏ quầng mờ bán trong suốt GPT vẽ quanh nét (giữ alpha > ~90), gom theo vùng liền,
# xếp theo lưới 5 × 4 của tờ, đặt tên theo hình. Ra hinh_cot/NN_<tên>.png.
# py -3 -I cat_hinh_cot.py
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hinh_cot_goc", "to_hinh.png")
DST = os.path.join(HERE, "hinh_cot")
sys.stdout.reconfigure(encoding="utf-8")
NAMES = [
    "sao_to", "sao_nho", "lap_lanh", "quai_sung", "quai_rong",
    "xoay", "tim", "vuong_mien", "kim_cuong", "bi",
    "trung", "dau_chan", "tia_set", "hop_qua", "lap_lanh_4",
    "quai_tai_dai", "quai_ma", "quai_bo", "quai_ca", "quai_long_xu",
]

im = np.array(Image.open(SRC).convert("RGBA"))
a = im[..., 3].astype(np.float32)
a = np.clip((a - 90) * 255 / 120, 0, 255).astype(np.uint8)
mask = (a > 40).astype(np.uint8)
grp = cv2.dilate(mask, np.ones((31, 31), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(grp, 8)
items = [(cen[i][1], cen[i][0], i) for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 1500]
H, W = mask.shape
items.sort(key=lambda t: (int(t[0] / (H / 4)), t[1]))
os.makedirs(DST, exist_ok=True)
for f in os.listdir(DST):
    if f.endswith(".png"):
        os.remove(os.path.join(DST, f))
for k, (cy, cx, i) in enumerate(items):
    x, y, w, h = st[i, :4]
    sel = (lab[y:y + h, x:x + w] == i)
    piece = np.zeros((h, w, 4), np.uint8)
    piece[..., :3] = 255
    piece[..., 3] = np.where(sel, a[y:y + h, x:x + w], 0)
    ys, xs = np.nonzero(piece[..., 3] > 10)
    piece = piece[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    name = NAMES[k] if k < len(NAMES) else f"hinh_{k}"
    Image.fromarray(piece).save(os.path.join(DST, f"{k:02d}_{name}.png"))
    print(f"{k:02d}_{name}", piece.shape[1], piece.shape[0])
print(len(items), "mảnh")
