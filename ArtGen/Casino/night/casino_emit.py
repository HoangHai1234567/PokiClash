# Mặt nạ tự sáng của công trình đảo Casino về đêm (GD_Claude/29 C8 "đèn đêm cho công trình, mặt nạ tự sáng như màn Nhà", 2026-11-27;
# cách làm như ArtGen/Home/night/home_emit.py: bỏ quầng sáng, chỉ chỗ vốn là nguồn sáng giữ màu trên lớp nhuộm đêm).
# Đọc Assets/03 Art/Casino/casino_ct_<mã>.png, ghi casino_e_<mã>.png cùng cỡ (chỉ giữ nguồn sáng, alpha theo mặt nạ):
#   lantern : đèn lồng giấy vàng. Cờ đuôi nheo cùng màu vàng nên lọc thêm theo hình: giữ đốm tròn (đầy khung >= 0,62, dài/rộng <= 2),
#             bỏ đốm tam giác (cờ đầy khung ~0,5) và đốm quá nhỏ / quá lớn
#   fire    : lửa đuốc (cam, vàng chói) trong khung → giữ màu gốc
#   glass   : mái kính xanh nhạt → tô màu đèn ấm, giữ nét chì
# Game vẽ ảnh này ở lớp "tu_sang" trên lớp nhuộm đêm (shader PokiClash/UIIslandEmit tự đọc _PokiNight), menu
# "PokiClash/Prefab/Đảo Casino/Đảo: dựng màn" (Editor/CasinoSceneMenu.cs, CasinoNightGlow bám theo công trình).
# Chạy: py -3 -I ArtGen/Casino/night/casino_emit.py [--xem]  (--xem: chỉ ghi tờ soi ArtGen/Casino/night/soi_emit.png, không ghi Assets)
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Casino")
LAMP = np.array([1.0, 0.84, 0.47])  # màu đèn ấm (như Nhà)

# mã → [(khung x0, y0, x1, y1 theo tỉ lệ ảnh, y từ trên; kiểu)]
# ba lều: chỉ hai cột đèn lồng hai bên (không lấy mảng vàng của bánh xe, quả chanh trên máy quả, sọc mái)
SIDES = [((0.0, 0.3, 0.26, 0.68), "lantern"), ((0.74, 0.3, 1.0, 0.68), "lantern")]
EMIT = {
    "cho": [((0.0, 0.0, 1.0, 1.0), "lantern")],
    "leu_blackjack": SIDES,
    "leu_roulette": SIDES,
    "leu_slot": SIDES,
    "hang": [((0.0, 0.0, 0.3, 0.42), "fire"), ((0.7, 0.0, 1.0, 0.42), "fire")],
    # tháp máy bi: tấm kính trắng xám (đèn trong tháp) + hàng bóng đèn tròn quanh mái vòm
    "thap": [((0.22, 0.27, 0.78, 0.68), "glass"), ((0.08, 0.12, 0.92, 0.30), "lantern")],
}


def hsv(a):
    rgb = a[..., :3] / 255.0
    mx, mn = rgb.max(-1), rgb.min(-1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, s, mx


def label(mask):
    """Gắn nhãn đốm liền (4 hướng), không cần scipy."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1
        stack = [(y0, x0)]
        lab[y0, x0] = n
        while stack:
            y, x = stack.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n
                    stack.append((yy, xx))
    return lab, n


def lantern_mask(a, box):
    h, s, v = hsv(a)
    yel = (h > 38) & (h < 62) & (s > 0.35) & (v > 0.72) & (a[..., 3] > 200) & box
    lab, n = label(yel)
    keep = np.zeros_like(yel)
    area_img = yel.shape[0] * yel.shape[1]
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        area = len(ys)
        if area < 25 or area > area_img * 0.02:
            continue
        bh, bw = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
        fill = area / float(bh * bw)
        if fill >= 0.62 and max(bh, bw) / max(1, min(bh, bw)) <= 2.0:
            keep[ys, xs] = True
    return keep


def fire_mask(a, box):
    h, s, v = hsv(a)
    return (((h < 50) | (h > 345)) & (s > 0.45) & (v > 0.75) & (a[..., 3] > 160)) & box


def glass_mask(a, box):
    # kính trắng xám hoặc xanh nhạt (ít màu, sáng); bi màu trong tháp không lấy
    h, s, v = hsv(a)
    pale = (s < 0.16) & (v > 0.72)
    blue = (h > 165) & (h < 225) & (s < 0.45) & (v > 0.72)
    return (pale | blue) & (a[..., 3] > 200) & box


def build(code):
    src = Image.open(os.path.join(ART, f"casino_ct_{code}.png")).convert("RGBA")
    a = np.asarray(src).astype(np.float32)
    H, W = a.shape[:2]
    out = np.zeros_like(a)
    for (x0, y0, x1, y1), kind in EMIT[code]:
        box = np.zeros((H, W), bool)
        box[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
        m = {"lantern": lantern_mask, "fire": fire_mask, "glass": glass_mask}[kind](a, box)
        # nới 1 px rồi làm mềm mép (không thành quầng: chỉ 1–2 px)
        mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
        alpha = np.minimum(np.asarray(mi).astype(np.float32), a[..., 3])
        if kind == "glass":
            lum = a[..., :3].mean(-1, keepdims=True) / 255.0
            col = LAMP[None, None, :] * (0.55 + 0.45 * lum) * 255
        elif kind == "lantern":
            col = np.minimum(255, a[..., :3] * 1.06 + 8)
        else:
            col = a[..., :3]
        sel = alpha > out[..., 3]
        out[..., :3] = np.where(sel[..., None], col, out[..., :3])
        out[..., 3] = np.maximum(out[..., 3], alpha)
    return src, Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def main():
    xem = "--xem" in sys.argv
    tiles = []
    for code in EMIT:
        src, emit = build(code)
        n = int((np.asarray(emit)[..., 3] > 128).sum())
        print(f"{code:14s} {src.size}  điểm sáng {n}")
        if not xem:
            emit.save(os.path.join(ART, f"casino_e_{code}.png"), optimize=True)
        # tờ soi: ảnh gốc nhuộm đêm + lớp sáng
        dark = np.asarray(src).astype(np.float32)
        dark[..., :3] *= np.array([0.32, 0.36, 0.55])
        night = Image.fromarray(dark.astype(np.uint8), "RGBA")
        night.alpha_composite(emit)
        both = Image.new("RGBA", (src.width * 2, src.height), (30, 30, 50, 255))
        both.alpha_composite(src, (0, 0))
        both.alpha_composite(night, (src.width, 0))
        k = 260 / both.height
        tiles.append(both.resize((int(both.width * k), 260)))
    sheet = Image.new("RGB", (sum(t.width for t in tiles) + 10 * len(tiles), 260), (30, 30, 50))
    x = 0
    for t in tiles:
        sheet.paste(t.convert("RGB"), (x, 0))
        x += t.width + 10
    sheet.save(os.path.join(HERE, "soi_emit.png"))
    print("tờ soi", os.path.join(HERE, "soi_emit.png"))


if __name__ == "__main__":
    main()
