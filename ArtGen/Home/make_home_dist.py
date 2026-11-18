# Ảnh khoảng cách tới bờ cho sóng vỗ của Nhà (shader PokiClash/UIInkWater, cùng cách ArtGen/Islands/land_thuy/m0/build_land.py --xuat):
# kênh R = khoảng cách tới bờ x 4 (px ảnh nền home_base.png, trần 64), G = chỗ được vẽ sóng (biển nối ra rìa ảnh; hồ, suối bên trong
# không có sóng). Cùng cỡ với home_base.png nên shader lấy mẫu theo uv của ảnh nền.
# Ra: Assets/03 Art/Baked/Home/home_dist.png. Chạy: py -3 -I make_home_dist.py
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "Assets", "03 Art", "Home", "home_base.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Baked", "Home")
os.makedirs(OUT, exist_ok=True)

a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H0, W0 = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]
# biển vẽ tay: xanh dương sáng, có nét gạch trắng (bọt) xen kẽ
seaish = ndi.binary_closing((B > 170) & (B - R > 45) & (G > 120), iterations=2)
lab, n = ndi.label(seaish)
band = np.zeros_like(seaish)
band[-8:] = True
band[:, :8] = band[:, -8:] = True  # biển ở nửa dưới: chạm mép dưới, trái, phải
cnt = ndi.sum(seaish, lab, range(1, n + 1))
edge = {i for i in set(np.unique(lab[band & seaish])) - {0} if cnt[i - 1] > 2000}
sea = ndi.binary_opening(np.isin(lab, list(edge)), iterations=1)
# lỗ nhỏ trong biển (sóng trắng vẽ sẵn, đá) coi là biển để khoảng cách không đứt
holes = ndi.binary_fill_holes(sea) & ~sea
hl, hn = ndi.label(holes)
sizes = ndi.sum(holes, hl, range(1, hn + 1))
small = np.isin(hl, [i + 1 for i, s in enumerate(sizes) if s < 4000])
sfd = sea | small
dist = ndi.distance_transform_edt(np.pad(sfd, 100, constant_values=True))[100:-100, 100:-100]
draw = sea & ~ndi.binary_dilation(small, iterations=2)
rg = np.zeros((H0, W0, 3), np.uint8)
rg[..., 0] = np.clip(dist * 4, 0, 255)
rg[..., 1] = draw * 255
Image.fromarray(rg).save(os.path.join(OUT, "home_dist.png"))
print("ok", W0, H0, "biển", int(sea.sum()), "px")
