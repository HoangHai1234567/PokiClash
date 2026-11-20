# Mặt nạ tự sáng của công trình Nhà về đêm (GD_Claude/22_Critters_Home.md mục 5–6: cách Critters _EmissiveTex, bỏ quầng sáng).
# Đọc Assets/03 Art/Home/home_b_<def>.png, ghi home_e_<def>.png cùng cỡ: chỉ giữ chỗ vốn là nguồn sáng, alpha theo mặt nạ.
#   glass : kính cửa sổ xanh nhạt → tô màu đèn ấm, giữ nét chì (sáng tối của nét)
#   fire  : lửa, than trong lò (cam, vàng chói) → giữ màu gốc
#   gem   : pha lê sáng màu (xanh, hồng, tím) → giữ màu gốc
#   lamp  : đèn lồng (đỏ, trắng) → tô màu đèn ấm
# Game vẽ ảnh này ở lớp "tu_sang" trên lớp nhuộm đêm (shader PokiClash/UIIslandEmit tự đọc _PokiNight), nên chỗ này không bị tối.
# Chạy: py -3 -I ArtGen/Home/night/home_emit.py [--xem]  (--xem: ghi tờ soi ArtGen/Home/night/soi_emit.png, không ghi Assets)
import colorsys
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Home")
LAMP = np.array([1.0, 0.84, 0.47])  # màu đèn ấm (tô phẳng)

# def → [(khung x0, y0, x1, y1 theo tỉ lệ ảnh, y từ trên; kiểu)]
EMIT = {
    "main": [((0.03, 0.28, 0.97, 0.88), "glass")],
    "storage": [((0.50, 0.22, 0.97, 0.68), "glass")],
    "waterwheel": [((0.48, 0.38, 0.97, 0.82), "glass")],
    "kitchen": [((0.46, 0.42, 0.72, 0.74), "fire")],  # miệng lò, nồi; không lấy mái tranh, khung gỗ
    "forge": [((0.14, 0.55, 0.40, 0.72), "fire")],    # than trong lò
    "mine": [((0.0, 0.0, 1.0, 1.0), "gem"), ((0.70, 0.50, 0.80, 0.68), "lamp")],
}


def hsv(a):
    rgb = a[..., :3] / 255.0
    mx, mn = rgb.max(-1), rgb.min(-1)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, s, v


def mask_of(a, kind):
    R, G, B = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    h, s, v = hsv(a.astype(float))
    if kind == "glass":
        return (B > R + 25) & (B > 140) & (G > 120)
    if kind == "fire":
        return (((h < 42) | (h > 345)) & (s > 0.6) & (v > 0.88))
    if kind == "gem":
        return (h > 170) & (h < 335) & (s > 0.45) & (v > 0.75)
    if kind == "lamp":
        return (((h < 15) | (h > 340)) & (s > 0.45) & (v > 0.6)) | ((s < 0.15) & (v > 0.85))
    raise ValueError(kind)


def grow(m, it=1):
    out = m.copy()
    for _ in range(it):
        o = out.copy()
        o[1:] |= out[:-1]; o[:-1] |= out[1:]; o[:, 1:] |= out[:, :-1]; o[:, :-1] |= out[:, 1:]
        out = o
    return out


def shrink(m, it=1):
    return ~grow(~m, it)


def build(defn):
    src = os.path.join(ART, "home_b_%s.png" % defn)
    a = np.asarray(Image.open(src).convert("RGBA"))
    H, W = a.shape[:2]
    rgb = a[..., :3].astype(float) / 255
    alpha = a[..., 3].astype(float) / 255
    out = np.zeros((H, W, 4))
    for (x0, y0, x1, y1), kind in EMIT[defn]:
        box = np.zeros((H, W), bool)
        box[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
        m = mask_of(a, kind) & box & (alpha > 0.5)
        m = grow(shrink(m, 1), 1)  # bỏ đốm lẻ một điểm ảnh
        if kind in ("glass", "lamp"):
            lum = rgb.mean(-1, keepdims=True)
            ref = np.median(lum[m]) if m.any() else 0.8
            col = np.clip(LAMP * (0.82 + 0.35 * (lum - ref)), 0, 1)
        else:
            col = rgb
        out[m, :3] = col[m]
        out[m, 3] = np.maximum(out[m, 3], alpha[m])
    return a, out


def main():
    xem = "--xem" in sys.argv
    tiles = []
    for d in EMIT:
        a, e = build(d)
        n = int((e[..., 3] > 0).sum())
        print(d, a.shape[1], "x", a.shape[0], "điểm sáng", n)
        img = Image.fromarray((e * 255 + 0.5).astype(np.uint8), "RGBA")
        if not xem:
            img.save(os.path.join(ART, "home_e_%s.png" % d))
        # soi: ngày | đêm không đèn | đêm có đèn
        day = Image.fromarray(a)
        night = a.astype(float).copy()
        night[..., :3] *= np.array([0.42, 0.46, 0.68])
        nimg = Image.fromarray(night.clip(0, 255).astype(np.uint8))
        lit = nimg.copy(); lit.alpha_composite(img)
        tiles.append((d, [day, nimg, lit]))
    if xem:
        th = 260
        rows = []
        for d, ims in tiles:
            ims = [im.resize((int(im.width * th / im.height), th)) for im in ims]
            w = sum(im.width for im in ims) + 20
            row = Image.new("RGBA", (w, th + 20), (40, 40, 48, 255))
            x = 0
            for im in ims:
                row.alpha_composite(im, (x, 20)); x += im.width + 10
            ImageDraw.Draw(row).text((4, 4), d, fill=(255, 255, 0, 255))
            rows.append(row)
        W = max(r.width for r in rows)
        sheet = Image.new("RGBA", (W, sum(r.height for r in rows)), (40, 40, 48, 255))
        y = 0
        for r in rows:
            sheet.alpha_composite(r, (0, y)); y += r.height
        sheet.convert("RGB").save(os.path.join(HERE, "soi_emit.png"))
        print("tờ soi", os.path.join(HERE, "soi_emit.png"))


if __name__ == "__main__":
    main()
