# -*- coding: utf-8 -*-
"""Xuất LỐC KHÍ (gói "Game VFX - Tornado Collection", prefab FX_AirTornado_Loop) vào game cho chiêu cuối rồng trúc (HatRong.NRongVan).

Nguồn: Editor/VfxPackShots.cs, menu "VFX gói lốc: chụp tách nền lốc khí AirTornado_Loop" → Temp/PokiShots/vfx_loc_nen/tor_FX_AirTornado_Loop/
f_###.png (nền trong: alpha tính từ hai ảnh nền đen / nền trắng), 24 khung/giây, tắt phát hạt ở khung 60 (2,5 s), info.txt có anchor (chân lốc).
Ra ba bộ khung (cùng khung cắt, cùng điểm neo) ở Assets/03 Art/Fx/Hat/:
    hat_fb_loc_khi_moc_NN  (12)  đoạn mọc 0–0,46 s
    hat_fb_loc_khi_lap_NN  (24)  đoạn thân LẶP LIỀN: lấy 30 khung 1,25–2,46 s, 6 khung đầu hoà với 6 khung cuối (nhân alpha) → nối không giật
    hat_fb_loc_khi_tan_NN  (≤22) đoạn tan sau khi tắt phát hạt (cắt bỏ khung đã gần trống)
In ba dòng FbDef để dán vào HatFlip.cs. Kèm ảnh soi trên nền sân: ArtGen/XemVfx/vfx_loc/loc_khi_soi.png
    py -3 -I ArtGen/XemVfx/vfx_loc/xuat_loc_khi.py [cạnh dài px, mặc định 300]
"""
import glob
import os
import re
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "Temp", "PokiShots", "vfx_loc_nen", "tor_FX_AirTornado_Loop")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Fx", "Hat")
MAXSIDE = int(sys.argv[1]) if len(sys.argv) > 1 else 300

fs = sorted(glob.glob(os.path.join(SRC, "f_*.png")))
info = open(os.path.join(SRC, "info.txt"), encoding="utf-8").read()
m = re.search(r"anchor=([\d.]+),([\d.]+)", info)
ax, ay = float(m.group(1)), float(m.group(2))
stop = int(re.search(r"stop=(\d+)", info).group(1))
fr = [np.asarray(Image.open(f).convert("RGBA")).astype(np.float32) / 255 for f in fs]
print(len(fr), "khung, neo", (ax, ay), "tắt phát ở", stop)
# bỏ quầng sáng của gói (luật game không quầng): tấm sáng vàng trên đỉnh lốc và vầng mờ to quanh lốc đều có alpha ≤ 7/255; dốc mềm từ 10/255
CUT = 10 / 255
for f in fr:
    f[..., 3] = np.clip((f[..., 3] - CUT) / (1 - CUT), 0, 1)


def premul(a):
    o = a.copy()
    o[..., :3] *= o[..., 3:4]
    return o


def unpremul(p):
    o = p.copy()
    al = o[..., 3:4]
    o[..., :3] = np.where(al > 1e-4, o[..., :3] / np.maximum(al, 1e-4), 0)
    return np.clip(o, 0, 1)


MOC = list(range(0, 12))
SRCLAP = list(range(30, 60))          # 30 khung trước lúc tắt phát
M = 6
lap = []
for k in range(24):
    if k < M:
        w = k / M
        lap.append(unpremul(premul(fr[SRCLAP[k]]) * w + premul(fr[SRCLAP[k + 24]]) * (1 - w)))
    else:
        lap.append(fr[SRCLAP[k]])
tan = [fr[i] for i in range(stop, len(fr))]
# bỏ khung tan đã gần trống (tổng alpha < 4 % khung đầu đoạn tan)
a0 = tan[0][..., 3].sum()
while len(tan) > 6 and tan[-1][..., 3].sum() < 0.04 * a0:
    tan.pop()
sets = {"loc_khi_moc": [fr[i] for i in MOC], "loc_khi_lap": lap, "loc_khi_tan": tan}

# khung cắt chung (mọi bộ, alpha > 3/255), giữ điểm neo bên trong
allf = [f for v in sets.values() for f in v]
mask = np.zeros(allf[0].shape[:2], bool)
for f in allf:
    mask |= f[..., 3] > 3 / 255
ys, xs = np.nonzero(mask)
x0, x1 = min(xs.min(), int(ax)) - 2, max(xs.max(), int(ax)) + 3
y0, y1 = min(ys.min(), int(ay)) - 2, max(ys.max(), int(ay)) + 3
H0, W0 = allf[0].shape[:2]
x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W0, x1), min(H0, y1)
cw, ch = x1 - x0, y1 - y0
s = min(1.0, MAXSIDE / max(cw, ch))
W, H = max(1, round(cw * s)), max(1, round(ch * s))
px, py = (ax - x0) / cw, 1 - (ay - y0) / ch
print("cắt", (x0, y0, x1, y1), "→", (W, H), "neo px, py (py từ đáy)", round(px, 3), round(py, 3))
# dáng thân lốc (đoạn lặp, alpha trung bình > 0,25): nửa bề rộng theo độ cao, tính theo phần cao KHUNG (để chỉnh quỹ đạo lá trong HatRong)
am = np.mean([f[y0:y1, x0:x1, 3] for f in lap], axis=0)
for frac in (0.1, 0.25, 0.4, 0.55, 0.7, 0.85):
    yy = int(round((ay - y0) - frac * ch))
    if 0 <= yy < ch:
        xs_ = np.nonzero(am[yy] > 0.25)[0]
        hw = (xs_.max() - xs_.min()) / 2 / ch if len(xs_) else 0
        print(f"  cao {frac:.2f} khung: nửa rộng {hw:.3f} khung")
top = np.nonzero(am.max(axis=1) > 0.25)[0]
print("  đỉnh thân lốc ở", round(((ay - y0) - top.min()) / ch, 3), "khung tính từ neo")

for name, frames in sets.items():
    for old in glob.glob(os.path.join(OUT, f"hat_fb_{name}_*.png")):
        n = int(old.rsplit("_", 1)[1][:-4])
        if n >= len(frames):   # bộ ngắn lại thì xoá khung dư (kèm .meta)
            os.remove(old)
            if os.path.exists(old + ".meta"):
                os.remove(old + ".meta")
    for i, f in enumerate(frames):
        im = Image.fromarray((np.clip(f[y0:y1, x0:x1], 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
        im = im.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA")   # nhân alpha trước khi thu: không viền tối
        im.save(os.path.join(OUT, f"hat_fb_{name}_{i:02d}.png"), optimize=True)
    loop = "true" if name == "loc_khi_lap" else "false"
    print(f'            {{ "{name}", new FbDef({len(frames)}, {W}, {H}, {px:.3f}f, {py:.3f}f, {loop}) }},')

# ảnh soi: 12 khung (4 mọc, 4 lặp, 4 tan) trên nền sân cát sáng và nền tối
pick = [sets["loc_khi_moc"][i] for i in (2, 5, 8, 11)] + [lap[i] for i in (0, 6, 12, 18)] + \
       [tan[min(len(tan) - 1, i)] for i in (0, 5, 10, 16)]
sheet = Image.new("RGB", (W * 6, H * 2), (232, 217, 176))
for k, f in enumerate(pick):
    im = Image.fromarray((np.clip(f[y0:y1, x0:x1], 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA").resize((W, H), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), (232, 217, 176, 255) if k % 2 == 0 else (70, 90, 70, 255))
    bg.alpha_composite(im)
    sheet.paste(bg.convert("RGB"), ((k % 6) * W, (k // 6) * H))
sheet.save(os.path.join(HERE, "loc_khi_soi.png"))
print("ok", {k: len(v) for k, v in sets.items()})
