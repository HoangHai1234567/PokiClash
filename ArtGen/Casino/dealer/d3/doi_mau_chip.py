# Chồng chip 4 màu theo bậc cược (D3): tờ đồ bàn chỉ có chồng đỏ và chồng xanh dương; chồng xanh lá và vàng lấy từ chồng đỏ bằng xoay sắc
# độ (chỉ vùng màu đỏ của chip, giữ nét nâu và vạch kem). Ra do_ban/chong_la.png, chong_vang.png (cùng cỡ chong_do.png).
# Chạy: py -3 -I doi_mau_chip.py   (rồi dua_vao_unity.py)
import os, sys
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, "do_ban", "chong_do.png")).convert("RGBA")
a = np.array(src)
hsv = np.array(src.convert("RGB").convert("HSV")).astype(np.int16)
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
# vùng đỏ: sắc gần 0 (thang 0–255), đủ đậm
red = ((h < 18) | (h > 238)) & (s > 90) & (v > 80)
for name, hue, sat_k, val_k in (("chong_la", 88, 0.92, 0.82), ("chong_vang", 34, 1.0, 1.12)):
    o = hsv.copy()
    o[..., 0] = np.where(red, hue, h)
    o[..., 1] = np.where(red, np.clip(s * sat_k, 0, 255), s)
    o[..., 2] = np.where(red, np.clip(v * val_k, 0, 255), v)
    rgb = Image.fromarray(o.astype(np.uint8), "HSV").convert("RGB")
    out = np.dstack([np.array(rgb), a[..., 3]])
    Image.fromarray(out, "RGBA").save(os.path.join(HERE, "do_ban", name + ".png"))
    print(name, int(red.sum()), "px đổi màu")
