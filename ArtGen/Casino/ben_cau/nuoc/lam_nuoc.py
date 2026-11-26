# Mặt nạ nước cho scene Bến câu (GD_Claude/32_BenCau_Scene.md mục 3, shader PokiClash/UIPondWater).
# Vào: ArtGen/Casino/ben_cau/nen_A.png (nền sạch cảnh A, 1024 x 1536, Magnific).
# Ra (Assets/03 Art/Casino/BenCau/):
#  - ben_cau_nen.png: nền (chép nguyên).
#  - ben_cau_nuoc.png (cùng cỡ): R = mặt nước được shader vẽ (1 nước, 0 bờ, đá, lá súng, lau sậy, bến);
#    G = khoảng cách tới bờ / DIST_MAX (1 ở xa bờ), để vẽ vạch bọt quanh bờ, đá, cọc bến;
#    B = vùng câu theo khoảng cách tới chỗ cậu đứng: 1/3 Gần bờ, 2/3 Xa bờ, 1 Rạn đá (0 ngoài nước);
#    A = 1.
#  - ben_cau_nuoc_cpu.bytes: mặt nạ nước 1/4 cỡ cho code (xem dưới).
#  - xem_nuoc.png (ở đây): ảnh soát, tô màu ba vùng + viền mặt nạ lên nền.
# Chạy: py -3 -I lam_nuoc.py
import os, sys, json
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(HERE, "..", "nen_A.png")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Casino", "BenCau")
os.makedirs(OUT, exist_ok=True)

CROSS = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
DIST_MAX = 48.0
# chỗ cậu đứng (px ảnh nền) và bán kính ranh vùng câu
STAND = (512, 1300)
R_NEAR, R_FAR = 400.0, 790.0
SEED = (512, 800)


def fill_holes(m):
    ff = np.pad(m.astype(np.uint8), 1)
    cv2.floodFill(ff, None, (0, 0), 2)
    return ff[1:-1, 1:-1] != 2


def main():
    a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    h, w = R.shape
    waterish = (B > 150) & (B - R > 40) & (G > 90)
    waterish = cv2.morphologyEx(waterish.astype(np.uint8), cv2.MORPH_CLOSE, CROSS, iterations=2) > 0
    n, lab = cv2.connectedComponents(waterish.astype(np.uint8), connectivity=4)
    pond = lab == lab[SEED[1], SEED[0]]
    # lỗ nhỏ (vạch sóng trắng, nét chì đậm) là nước; lỗ lớn (đá, lá súng) giữ là bờ. Lỗ chạm mép ảnh (lau sậy) xét riêng
    holes = ~pond
    hn, hl, hs, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), connectivity=4)
    small = [i for i in range(1, hn) if hs[i, cv2.CC_STAT_AREA] < 1800]
    pond = pond | np.isin(hl, small)
    pond = cv2.morphologyEx(pond.astype(np.uint8), cv2.MORPH_OPEN, CROSS, iterations=1) > 0
    # bờ nước hơi lùi vào để vạch bọt không đè nét bờ
    dist = cv2.distanceTransform(pond.astype(np.uint8), cv2.DIST_L2, 5)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - STAND[0], (yy - STAND[1]) * 1.15)
    zone = np.where(r < R_NEAR, 1 / 3, np.where(r < R_FAR, 2 / 3, 1.0)) * pond
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0] = pond * 255
    out[..., 1] = (np.clip(dist / DIST_MAX, 0, 1) * 255).astype(np.uint8)
    out[..., 2] = (zone * 255).astype(np.uint8)
    out[..., 3] = 255
    Image.fromarray(out, "RGBA").save(os.path.join(OUT, "ben_cau_nuoc.png"))
    Image.open(SRC).convert("RGB").save(os.path.join(OUT, "ben_cau_nen.png"))
    # bản nhỏ cho code (FishingPanel tra chỗ có nước để thả phao, cho bóng cá bơi): 4 byte rộng, 4 byte cao (little endian), rồi
    # mỗi ô 1 byte (0 bờ, 1 nước), cỡ 1/4 ảnh nền, hàng trên cùng trước
    small = cv2.resize(cv2.erode(pond.astype(np.uint8), CROSS, iterations=3), (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    with open(os.path.join(OUT, "ben_cau_nuoc_cpu.bytes"), "wb") as f:
        f.write(np.array([w // 4, h // 4], "<i4").tobytes())
        f.write((small > 0).astype(np.uint8).tobytes())
    # ảnh soát
    prev = a.astype(float).copy()
    tint = {1 / 3: (80, 220, 120), 2 / 3: (250, 210, 60), 1.0: (240, 90, 90)}
    for z, c in tint.items():
        m = np.isclose(zone, z) & pond
        prev[m] = prev[m] * 0.6 + np.array(c) * 0.4
    edge = pond ^ (cv2.erode(pond.astype(np.uint8), CROSS, iterations=2) > 0)
    prev[edge] = (255, 0, 255)
    Image.fromarray(prev.clip(0, 255).astype(np.uint8)).save(os.path.join(HERE, "xem_nuoc.png"))
    meta = {"size": [w, h], "stand": STAND, "rNear": R_NEAR, "rFar": R_FAR, "yScale": 1.15, "distMax": DIST_MAX,
            "waterFrac": round(float(pond.mean()), 3)}
    json.dump(meta, open(os.path.join(HERE, "nuoc.json"), "w"), indent=1)
    print("nước", meta)


if __name__ == "__main__":
    main()
