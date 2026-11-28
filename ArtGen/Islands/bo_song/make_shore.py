# Mặt nạ sóng gần bờ cho sảnh và đảo Casino (người dùng 2026-11-27: "làm thêm shader sóng gần bờ như của home cho đảo chính và đảo
# casino"). Cùng kiểu mặt nạ của Nhà (ArtGen/Home/sea/make_home_sea.py, shader PokiClash/UIHomeSea): R dải mờ rộng, G dải vừa, B dải
# sắc sát bờ (1 ở bờ, 0 ra xa), A = 1 khắp nơi (lớp bien_bo nằm dưới các đảo, chỗ đất bị đảo che). Dải đo theo đơn vị màn, cùng cỡ
# dải của Nhà (Nhà đo px ảnh nền, 1 px = 3,156 đơn vị: rộng 230 px, vừa 105 px, sắc 3..24 px).
# - Sảnh: ghép kênh alpha các ảnh đảo theo hub_map.json (view, islands[].rect) -> sanh_bo.png.
# - Casino: kênh alpha casino_dao.png (khung 2048 x 1360) -> casino_bo.png.
# Mỗi mặt nạ phủ khung ảnh nới ra PAD đơn vị mỗi bên (dải bờ không chạm mép lớp); menu "PokiClash/Prefab/Sảnh và đảo/Sóng bờ: sảnh,
# Casino" (Editor/ShoreWaveMenu.cs) đặt lớp theo đúng khung đó. Ra: Assets/03 Art/Baked/Shore/. Chạy: py -3 -I make_shore.py [--preview]
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art")
OUT = os.path.join(ART, "Baked", "Shore")
os.makedirs(OUT, exist_ok=True)

PAD = 640    # đơn vị màn, nới mỗi bên (phải khớp ShoreWaveMenu.Pad)
S = 0.4      # px mặt nạ / đơn vị màn
K = 3.156    # đơn vị màn / px ảnh nền Nhà
WIDE, MID, SHARP0, SHARP1 = 230 * K, 105 * K, 3 * K, 24 * K


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def paste_alpha(canvas, path, x0, y0, w, h, top_cut=0):
    """dán kênh alpha ảnh (phóng vừa khung w x h đơn vị màn, góc trên trái x0, y0) vào canvas (px mặt nạ), lấy max;
    top_cut: bỏ bấy nhiêu px ảnh trên cùng (Casino: dãy núi xa vẽ ở mép trên, dính liền đảo)"""
    a = Image.open(path).convert("RGBA").split()[3]
    if top_cut:
        a = a.copy()
        a.paste(0, (0, 0, a.size[0], top_cut))
    pw, ph = max(1, int(round(w * S))), max(1, int(round(h * S)))
    a = np.asarray(a.resize((pw, ph), Image.BILINEAR), np.float32) / 255
    px, py = int(round(x0 * S)), int(round(y0 * S))
    H, W = canvas.shape
    xa, ya, xb, yb = max(0, px), max(0, py), min(W, px + pw), min(H, py + ph)
    if xb <= xa or yb <= ya:
        return
    canvas[ya:yb, xa:xb] = np.maximum(canvas[ya:yb, xa:xb], a[ya - py:yb - py, xa - px:xb - px])


def land_hub():
    d = json.load(open(os.path.join(ART, "Islands", "hub_map.json"), encoding="utf-8"))
    W, H = d["view"]
    canvas = np.zeros((int(round((H + 2 * PAD) * S)), int(round((W + 2 * PAD) * S))), np.float32)
    for it in d["islands"]:
        u0, v0, u1, v1 = it["rect"]
        paste_alpha(canvas, os.path.join(ART, "Islands", it["sprite"] + ".png"), PAD + u0 * W, PAD + v0 * H, (u1 - u0) * W, (v1 - v0) * H)
    return canvas, (W, H)


def land_casino():
    W, H = 2048, 1360  # khung ảnh đảo (anh_nen_casino / dat)
    canvas = np.zeros((int(round((H + 2 * PAD) * S)), int(round((W + 2 * PAD) * S))), np.float32)
    paste_alpha(canvas, os.path.join(ART, "Casino", "casino_dao.png"), PAD, PAD, W, H, top_cut=100)
    return canvas, (W, H)


CROSS = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))


def fill_holes(mask):
    ff = np.pad(mask.astype(np.uint8), 1)
    cv2.floodFill(ff, None, (0, 0), 2)
    return ff[1:-1, 1:-1] != 2


def build(alpha, min_area, largest=False):
    land = alpha > 0.5
    # nét mảnh vẽ trên mặt nước (vệt sóng trắng, dãy núi xa ở mép trên ảnh Casino): mở ảnh bỏ nét mảnh, rồi chỉ giữ khối đất lớn
    land = cv2.morphologyEx(land.astype(np.uint8), cv2.MORPH_OPEN, CROSS, iterations=3) > 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(land.astype(np.uint8), connectivity=4)
    keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= min_area]
    if largest and keep:
        keep = [max(keep, key=lambda i: st[i, cv2.CC_STAT_AREA])]
    land = np.isin(lab, keep)
    # đảo có thể bị mở mòn mép: lấy lại đúng mép ảnh trong vùng gần khối đã giữ
    near = cv2.dilate(land.astype(np.uint8), CROSS, iterations=4) > 0
    land = (alpha > 0.5) & near | land
    land = fill_holes(land)  # hồ trong đảo (lỗ trong suốt) coi là đất: không dải, không bọt, chỉ biển trơn
    d = cv2.distanceTransform((~land).astype(np.uint8), cv2.DIST_L2, 5) / S  # đơn vị màn từ biển tới đất gần nhất
    r = 1 - smooth(0, WIDE, d)
    g = 1 - smooth(0, MID, d)
    b = 1 - smooth(SHARP0, SHARP1, d)
    r[land] = g[land] = b[land] = 0  # trong đất (dưới ảnh đảo, hồ): biển trơn
    a = np.ones_like(d)
    m = np.stack([r, g, b, a], -1)
    return Image.fromarray((np.clip(m, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA"), land


def preview(name, mask, land):
    m = np.asarray(mask).astype(np.float32) / 255
    rgb = np.zeros(m.shape[:2] + (3,), np.float32)
    rgb[:] = (0.06, 0.86, 0.98)
    edge = np.clip((m[..., 1] - m[..., 2] - 0.43) / 0.04, 0, 1) * (1 - (m[..., 2] > 0.72)) * 0.35
    rgb = rgb * (1 - edge[..., None]) + np.array([0.62, 0.89, 0.95]) * edge[..., None]
    foam = (m[..., 2] > 0.72) * 0.55
    rgb = rgb * (1 - foam[..., None]) + foam[..., None]
    rgb[land] = (0.45, 0.7, 0.35)
    Image.fromarray((rgb * 255).astype(np.uint8)).save(os.path.join(HERE, "preview_" + name + ".png"))


def main():
    # sảnh: chỉ giữ khối đảo lớn từ 20000 px mặt nạ (người dùng 2026-11-28: bỏ sóng bờ quanh đá nhỏ, san hô, thuyền; trước là 400 px nên
    # 6 khối vật nhỏ trên biển quanh đảo Thủy, lớn nhất 3326 px, cũng có dải bờ); Casino: một đảo, giữ khối lớn nhất
    for name, fn, min_area, largest in (("sanh_bo", land_hub, 20000, False), ("casino_bo", land_casino, 400, True)):
        alpha, (W, H) = fn()
        mask, land = build(alpha, min_area, largest)
        mask.save(os.path.join(OUT, name + ".png"))
        print(f"{name}: khung {W} x {H} đơn vị, nới {PAD}, mặt nạ {mask.size[0]} x {mask.size[1]} px, đất {land.mean() * 100:.1f}%")
        if "--preview" in sys.argv:
            preview(name, mask, land)


if __name__ == "__main__":
    main()
