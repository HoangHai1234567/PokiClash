# Hậu kỳ 32 khung tàu 3D (render_32.py) cho game:
# - cắt phần thân chìm: dưới mép trước của đường mớn nước (lát cắt ngang thân ở mặt nước, Blender chiếu lên từng khung) là trong suốt;
# - vẽ đường bọt trắng viền ngọc nhạt theo mép trước đường mớn nước;
# - phủ vân chì nhẹ (gạch chéo -38 độ) cho hợp nét vẽ tay; cắt chung một khung cho mọi hướng (gốc đứng yên), thu về cỡ sảnh;
# - ra Assets/03 Art/Ship/3d/tau_hd_00..31.png và tau_hd.json (cỡ ảnh, gốc, góc hướng trên màn, mũi, đèn lồng: px trên ảnh ra).
# py -3 -I hau_ky.py [--soi]
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import ConvexHull

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hd")
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "Assets", "03 Art", "Ship", "3d"))
SIDE_LEN = 250  # chiều dài thân khi nhìn ngang trên sảnh (px = đơn vị UI), như ảnh tàu vẽ tay cũ (259)


def hull_lower(points, w):
    """Mép dưới (y lớn nhất theo từng cột x) của bao lồi các điểm mớn nước. Trả mảng y theo x (nan ngoài vùng)."""
    pts = np.array(points, dtype=np.float64)
    hull = pts[ConvexHull(pts).vertices]
    poly = Image.new("L", (w, w), 0)
    ImageDraw.Draw(poly).polygon([tuple(p) for p in hull], fill=255)
    m = np.asarray(poly) > 0
    low = np.full(w, np.nan)
    for x in range(w):
        ys = np.nonzero(m[:, x])[0]
        if len(ys):
            low[x] = ys.max()
    return low, hull


def hatch(size, seed=3):
    rng = np.random.default_rng(seed)
    S = 2
    img = Image.new("L", (size * S, size * S), 0)
    d = ImageDraw.Draw(img)
    ang = math.radians(-38)
    for _ in range(int(size * size / 90)):
        x, y = rng.uniform(0, size * S), rng.uniform(0, size * S)
        L = rng.uniform(8, 22) * S
        dx, dy = math.cos(ang) * L / 2, -math.sin(ang) * L / 2
        d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=int(rng.uniform(60, 140)), width=S)
    return np.asarray(img.resize((size, size), Image.LANCZOS), dtype=np.float32) / 255


def main():
    meta = json.load(open(os.path.join(SRC, "meta.json")))
    res = meta["res"]
    frames = []
    for f in meta["frames"]:
        im = np.asarray(Image.open(os.path.join(SRC, f"hd_{f['k']:02d}.png")).convert("RGBA")).astype(np.float32)
        low, hull = hull_lower(f["waterline"], res)
        # cắt phần chìm (dưới mép trước đường mớn nước), mép mềm 1 px
        yy = np.arange(res)[:, None]
        cut = np.where(np.isnan(low)[None, :], 0, np.clip((yy - low[None, :]) / 1.5, 0, 1))
        im[..., 3] *= (1 - cut)
        img = Image.fromarray(im.clip(0, 255).astype(np.uint8), "RGBA")
        # bọt theo mép trước: các điểm mép dưới bao lồi trong vùng có thân
        xs = [x for x in range(res) if not np.isnan(low[x])]
        line = [(x, low[x]) for x in xs[::2]]
        foam = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(foam)
        if len(line) > 1:
            d.line(line, fill=(178, 238, 250, 255), width=9, joint="curve")
            d.line(line, fill=(255, 255, 255, 255), width=5, joint="curve")
        img = Image.alpha_composite(foam, img) if False else Image.alpha_composite(img, foam)
        frames.append((f, img))
    # khung chung cho mọi hướng
    boxes = [im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox() for _, im in frames]
    x0 = min(b[0] for b in boxes) - 4
    y0 = min(b[1] for b in boxes) - 4
    x1 = max(b[2] for b in boxes) + 4
    y1 = max(b[3] for b in boxes) + 4
    # tỉ lệ: khung nhìn ngang (hướng 0) dài SIDE_LEN
    side = next(im for f, im in frames if f["k"] == 0)
    sb = side.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    k = SIDE_LEN / (sb[2] - sb[0])
    W, H = round((x1 - x0) * k), round((y1 - y0) * k)
    os.makedirs(OUT, exist_ok=True)
    hat = hatch(max(W, H))
    out_meta = {"size": [W, H], "frames": []}

    def tp(p):
        return [round((p[0] - x0) * k, 2), round((p[1] - y0) * k, 2)]

    for f, im in frames:
        c = im.crop((x0, y0, x1, y1)).resize((W, H), Image.LANCZOS)
        a = np.asarray(c).astype(np.float32)
        h = hat[:H, :W, None]
        a[..., :3] *= 1 - 0.10 * h  # vân chì nhẹ
        Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA").save(os.path.join(OUT, f"tau_hd_{f['k']:02d}.png"), optimize=True)
        out_meta["frames"].append({"angle": f["angle"], "pivot": tp(f["pivot"]), "bow": tp(f["bow"]), "lantern": tp(f["lantern"])})
    json.dump(out_meta, open(os.path.join(OUT, "tau_hd.json"), "w"), indent=1)
    print("ra", OUT, len(frames), "khung", W, "x", H)
    if "--soi" in sys.argv:
        sheet = Image.new("RGBA", (W * 8, H * 4), (40, 170, 220, 255))
        for i in range(len(frames)):
            sheet.alpha_composite(Image.open(os.path.join(OUT, f"tau_hd_{i:02d}.png")), ((i % 8) * W, (i // 8) * H))
        sheet.convert("RGB").save(os.path.join(HERE, "soi_hau_ky.png"))


if __name__ == "__main__":
    main()
