# Bản tuyết của viền cỏ ô lát màn Nhà (lip_grass_*, cor_grass_*: răng cỏ xanh lấn sang ô đất / cát / đá người chơi lát). Nền Nhà mùa Noel
# phủ tuyết nên răng cỏ cũng thành tuyết: đổi điểm xanh sang trắng ngả xanh xám (giữ vân chì theo độ sáng gốc), nét mực giữ nguyên.
# py -3 -I tuyet_o_lat.py -> out/noel/<tên>.png (xuat_map.py chép vào game)
import os, sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TILES = os.path.join(PROJ, "Assets", "03 Art", "Home", "tiles")
OUT = os.path.join(HERE, "out", "noel")
os.makedirs(OUT, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

NAMES = [f"{k}_grass_{i}" for k in ("lip", "cor") for i in range(4)]
SNOW_DARK = np.array([206, 218, 232], np.float32)  # vân chì tối của tuyết (xanh xám nhạt)
SNOW_LIGHT = np.array([250, 252, 255], np.float32)


def run(name):
    im = np.array(Image.open(os.path.join(TILES, name + ".png")).convert("RGBA"))
    rgb = im[..., :3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    green = (h >= 25) & (h <= 90)
    # mức "cỏ" của điểm: điểm xanh rõ = 1, điểm pha mực ở mép = theo độ sáng (nét mực tối giữ nguyên)
    w = np.clip((v - 0.35) / 0.35, 0, 1) * np.clip(s / 0.25, 0, 1) * green
    vv = v[green & (w > 0.9)]
    lo, hi = (np.percentile(vv, 5), np.percentile(vv, 95)) if vv.size > 20 else (0.6, 0.95)
    t = np.clip((v - lo) / max(1e-3, hi - lo), 0, 1)[..., None]
    snow = SNOW_DARK + (SNOW_LIGHT - SNOW_DARK) * t
    out = rgb.astype(np.float32) * (1 - w[..., None]) + snow * w[..., None]
    res = np.dstack([np.clip(out, 0, 255).astype(np.uint8), im[..., 3]])
    Image.fromarray(res).save(os.path.join(OUT, name + ".png"), optimize=True)
    print(f"{name}: {int((w > 0.5).sum())} điểm cỏ → tuyết")


for n in NAMES:
    run(n)
