# -*- coding: utf-8 -*-
"""Texture dữ liệu cho shader nước trong game (PokiClash/UIWaterFx; người dùng 2026-11-24 chọn "c": toàn bộ bộ nước chạy bằng shader,
lốc nước giữ flipbook). Học shader repo abitofgamedev/water_vfx (skill vfx-petclash/hoc_water_vfx_abitofgamedev.md): mọi hình tan theo
step(ngưỡng, mặt_nạ_mềm × nhiễu) — ở đây nhiễu và mặt nạ là TEXTURE (rẻ trên điện thoại, không tính nhiễu thủ tục trong shader).
  Assets/03 Art/Fx/Nuoc/nuoc_nhieu.png   256² RGBA, LẶP LIỀN hai chiều: R = nhiễu mượt (vệt nước chảy), G = nhiễu vừa (tan theo ngưỡng),
                                          B = nhiễu mịn (tan lấm tấm), A = vân chì gạch chéo (nét vẽ tay)
  Assets/03 Art/Fx/Nuoc/nuoc_matna.png   1024² xám, atlas 4×4 ô 256²: mặt nạ mềm tự sinh (vfx_blender/mat_na/, mat_na_nuoc.py)
      hàng 0: ngon_0 ngon_1 ngon_2 dac_0      hàng 1: cham_0 cham_1 cham_2 dac_1
      hàng 2: vung_0 vung_1 vung_2 dac_2      hàng 3: loang_0 loang_1 botmep_0 botmep_1
  (ô đánh số chỉ số = hàng·4 + cột, hàng 0 ở TRÊN ảnh; shader đổi sang toạ độ UV Unity — v = 0 ở dưới.)
    py -3 -I tao_texture.py
"""
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Fx", "Nuoc"))
MASK = os.path.normpath(os.path.join(HERE, "..", "vfx_blender", "mat_na"))
os.makedirs(OUT, exist_ok=True)
S = 256


def tile_noise(rng, base, octaves, persist=0.5):
    """Nhiễu giá trị lặp liền hai chiều: lưới ngẫu nhiên tuần hoàn phóng bằng nội suy bậc ba có quấn biên, cộng nhiều tầng."""
    acc = np.zeros((S, S), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((n, n)).astype(np.float32)
        big = np.tile(g, (3, 3))                                   # quấn biên: phóng bản 3×3 rồi cắt giữa
        up = cv2.resize(big, (3 * S, 3 * S), interpolation=cv2.INTER_CUBIC)[S:2 * S, S:2 * S]
        acc += amp * up
        tot += amp
        amp *= persist
    a = acc / tot
    a -= a.min()
    return a / (a.max() + 1e-6)


rng = np.random.default_rng(24)
r = tile_noise(rng, 4, 3)            # mượt: vệt nước
g = tile_noise(rng, 8, 4)            # vừa: tan theo ngưỡng
b = tile_noise(rng, 32, 2, 0.6)      # mịn: lấm tấm
# A = VÂN CHÌ vẽ tay (người dùng 2026-11-24: "cần nổi khối hơn chút và có chút texture kiểu vẽ tay"): nét gạch chéo ~ −38° (skill
# vfx-petclash mục 1c), lặp liền (pháp tuyến nguyên (24, 30) trên ô 256 → cách nét ~6,7 px), đậm nhạt + đứt quãng theo nhiễu như sáp
# màu, thêm hạt giấy. 1 = không tối, nét chì ~0,35. Shader lấy theo toạ độ MÀN HÌNH (nét giữ cỡ, góc khi hình xoay).
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
ph = ((24 * xx + 30 * yy) / S) % 1.0                       # pha nét: lặp liền theo cả x, y
ln = np.clip(1 - np.abs(ph - 0.5) * 2 * 3.2, 0, 1) ** 1.6  # nét mảnh ~ 1/3,2 khoảng cách
ap = tile_noise(rng, 6, 3)                                 # lực ấn bút
gap = tile_noise(rng, 16, 2)                               # đứt quãng
grain = tile_noise(rng, 64, 1)                             # hạt giấy
dark = ln * (0.45 + 0.55 * ap) * (gap > 0.32) + 0.12 * (grain - 0.5)
hatch = np.clip(1 - 0.65 * dark, 0, 1)
img = np.dstack([b, g, r, hatch])    # cv2 ghi BGRA → R = r, A = vân chì
cv2.imwrite(os.path.join(OUT, "nuoc_nhieu.png"), (np.clip(img, 0, 1) * 255).astype(np.uint8))

CELLS = ["ngon_0", "ngon_1", "ngon_2", "dac_0",
         "cham_0", "cham_1", "cham_2", "dac_1",
         "vung_0", "vung_1", "vung_2", "dac_2",
         "loang_0", "loang_1", "botmep_0", "botmep_1"]
atlas = np.zeros((4 * S, 4 * S), np.uint8)
for i, name in enumerate(CELLS):
    m = cv2.imread(os.path.join(MASK, name + ".png"), cv2.IMREAD_GRAYSCALE)
    m = cv2.resize(m, (S, S), interpolation=cv2.INTER_AREA)
    rr, cc = divmod(i, 4)
    atlas[rr * S:(rr + 1) * S, cc * S:(cc + 1) * S] = m
cv2.imwrite(os.path.join(OUT, "nuoc_matna.png"), atlas)
print("ok", OUT)
