# Tách nền lều Vòng Xoay (nen_leu_xoay_2k.jpg: Magnific GPT 2.6 1k high, phóng classic 2k) thành hai lớp cho scene có dealer:
# nền (cả ảnh, Lão Mực đứng trước) và bàn (thanh gỗ mép bàn + khay chip + nỉ, đè lên hông Lão Mực).
# Đường cắt bám nét mực trên cùng của thanh gỗ (cung đo tay: dò tự động bị nét chì gạch chéo gây nhiễu), cắt cao hơn 3 px để giữ nét.
# Ra: nen_leu_xoay.jpg, ban_leu_xoay.png (RGBA, cùng cỡ, phần trên trong suốt), tach_lop_xem.jpg, tach_lop.json.
# Chạy: py -3 -I tach_lop.py
import json, os
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, "nen_leu_xoay_2k.jpg")).convert("RGB")
W, H = src.size
# mép trên nét mực của thanh gỗ (px ảnh 2k), đo tay trên ảnh phóng to
TOP = [(0, 757), (60, 742), (120, 729), (200, 713), (280, 700), (340, 693), (420, 688), (572, 684), (724, 688), (800, 692), (860, 698),
       (940, 710), (1020, 725), (1090, 741), (1144, 754)]
xs = np.array([p[0] for p in TOP], float)
ys = np.array([p[1] for p in TOP], float)
top = np.interp(np.arange(W), xs, ys)
cut = top - 3.0
yy = np.arange(H)[:, None]
alpha = np.clip(yy - cut[None, :] + 0.5, 0, 1)
rgba = np.dstack([np.asarray(src), (alpha * 255).astype(np.uint8)])
Image.fromarray(rgba, "RGBA").save(os.path.join(HERE, "ban_leu_xoay.png"))
src.save(os.path.join(HERE, "nen_leu_xoay.jpg"), quality=92)
pv = src.copy()
d = ImageDraw.Draw(pv)
d.line([(x, float(cut[x])) for x in range(0, W, 2)], fill=(255, 0, 255), width=2)
pv.crop((0, 640, W, 880)).resize((W * 2, 480), Image.LANCZOS).save(os.path.join(HERE, "tach_lop_xem.jpg"), quality=88)
info = {"size": [W, H], "rim_top_center": 684, "tray": {"x0": 322, "x1": 818, "top": 703, "bottom": 830},
        "stacks_x": [425, 522, 620, 716], "felt_top_center": 839}
json.dump(info, open(os.path.join(HERE, "tach_lop.json"), "w"), indent=1)
print(info)
