"""Sóng âm vẽ chì (2026-11-19). Người dùng: "phần sóng âm vẫn chưa ổn đâu, làm đơn giản thôi, ... làm 1 vài nét vẽ tay tô chì màu xám
nhạt làm sóng âm". Mỗi ảnh là MỘT cung gồm 2–3 nét chì song song (nét chính dài, nét phụ ngắn, có chỗ đứt), thuôn hai đầu, vân giấy,
KHÔNG viền mực. Ảnh trắng (vân hơi xám), game nhuộm xám nhạt bằng Image.color.

Quy ước (giống kr_songam): cung lồi về +x, dây cung 86 % chiều cao khung, đỉnh lưng ở 62 % bề ngang khung, khung 384 x 384.
Ra ArtGen/Spine/hat_songchi/hat_kr_songchi_<i>.png (i = 0..3) và tờ thử xem.png (ghép lên ảnh trận thật nếu có).
    py -3 -I ArtGen/Spine/hat_songchi.py           # sinh + tờ thử
    py -3 -I ArtGen/Spine/hat_songchi.py --xuat    # chép thêm sang Assets/03 Art/Fx/Hat/
"""
import glob
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "hat_songchi")
ASSET = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))
SHOTS = os.path.normpath(os.path.join(HERE, "..", "..", "Temp", "PokiShots", "vfx_all", "truoc"))
N = 384
SS = 2                      # vẽ ở 768 rồi thu
S = N * SS
CHORD, APEX = 0.86, 0.62
TINT = (158, 154, 147)      # xám nhạt hơi ấm (màu game nhuộm, cũng là màu tờ thử)


def grain(seed):
    """vân chì: hạt giấy + vệt chì chéo, 0..1"""
    r = np.random.default_rng(seed)
    g1 = ndimage.gaussian_filter(r.random((S, S)), 1.0)
    g1 = (g1 - g1.min()) / (np.ptp(g1) + 1e-6)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    ang = math.radians(r.uniform(28, 40))
    u = xx * math.cos(ang) + yy * math.sin(ang)
    streak = 0.5 + 0.5 * np.sin(u / r.uniform(3.2, 4.2) + ndimage.gaussian_filter(r.random((S, S)), 6) * 9)
    return np.clip(0.35 + 0.65 * g1, 0, 1), streak


def stroke_mask(cx, cy, R, t0, t1, a, wmax, wob, phase, gaps, seed):
    """một nét chì dọc cung tròn tâm (cx, cy), bán kính R, góc từ -a đến +a (t0..t1 của độ dài), bề dày thuôn hai đầu"""
    r = np.random.default_rng(seed)
    m = np.zeros((S, S), np.float32)
    n = 260
    noise = ndimage.gaussian_filter1d(r.normal(0, 1, n), 9) * 3.0
    pts = []
    for k in range(n):
        t = t0 + (t1 - t0) * k / (n - 1)
        if any(g0 <= t <= g1 for g0, g1 in gaps):
            pts.append(None)
            continue
        th = -a + 2 * a * t
        rr = R + wob * math.sin(t * math.tau * 1.5 + phase) + noise[k]
        x, y = cx + rr * math.cos(th), cy + rr * math.sin(th)
        loc = (k / (n - 1))
        w = wmax * (math.sin(math.pi * loc) ** 0.75) * (0.85 + 0.15 * math.sin(k * 0.21 + phase))
        pts.append((x, y, max(0.6, w)))
    im = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(im)
    for p in pts:
        if p is None: continue
        x, y, w = p
        d.ellipse([x - w, y - w, x + w, y + w], fill=255)
    m = np.asarray(im, np.float32) / 255
    return ndimage.gaussian_filter(m, 0.9)


def make(i):
    r = np.random.default_rng(100 + i)
    H = S
    a = math.radians(r.uniform(44, 52))
    R = CHORD * H / (2 * math.sin(a))
    cx, cy = APEX * S - R, S / 2
    ph = r.uniform(0, 6.28)
    gaps_main = [(0.52, 0.57)] if i in (1, 3) else []
    main = stroke_mask(cx, cy, R, 0.0, 1.0, a, r.uniform(34, 38), r.uniform(3, 6), ph, gaps_main, 10 + i)
    inner = stroke_mask(cx, cy, R - r.uniform(50, 58), r.uniform(0.12, 0.2), r.uniform(0.8, 0.88), a, r.uniform(22, 26), 3, ph + 1.3,
                        [(0.4, 0.45)] if i in (0, 2) else [], 20 + i)
    parts = [main, inner]
    if i in (2, 3):  # nét thứ ba ngắn bên ngoài
        parts.append(stroke_mask(cx, cy, R + r.uniform(44, 50), 0.32, 0.62, a, 15, 2, ph + 2.1, [], 30 + i))
    cov = np.clip(sum(parts), 0, 1)
    g, streak = grain(200 + i)
    # mép xơ như chì: phần mép mỏng bị hạt giấy ăn bớt
    rag = np.clip((cov - (1 - g) * 0.55) / 0.45, 0, 1)
    alpha = rag * (0.82 + 0.18 * streak) * (0.88 + 0.12 * g)
    lum = 255 - 46 * (1 - streak) * cov - 20 * (1 - g)
    rgba = np.zeros((S, S, 4), np.float32)
    rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = np.clip(lum, 0, 255)
    rgba[..., 3] = np.clip(alpha * 255, 0, 255)
    im = Image.fromarray(rgba.astype(np.uint8), "RGBA").resize((N, N), Image.LANCZOS)
    return im


def tinted(im, col, a=1.0):
    arr = np.asarray(im, np.float32).copy()
    for c in range(3): arr[..., c] = arr[..., c] * col[c] / 255
    arr[..., 3] *= a
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def preview(ims):
    # nền: một khung chiêu gầm của Rồng Trúc ở bản TRƯỚC (vùng sân), không có thì nền cát
    strip = os.path.normpath(os.path.join(HERE, "..", "XemVfx", "anh", "truoc", "thanh_long_mana.jpg"))
    if os.path.exists(strip):  # tấm khung của trang so sánh: lưới 10 cột, mỗi ô 360 x 395
        k = 3
        bg = Image.open(strip).convert("RGB").crop((k * 360, 0, k * 360 + 360, 395)).resize((720, 790))
    else:
        bg = Image.new("RGB", (720, 790), (243, 226, 184))
    W = 720 + 4 * 200
    sheet = Image.new("RGB", (W, 790), (40, 42, 46))
    sheet.paste(bg, (0, 0))
    base = bg.convert("RGBA")
    # ghép thử: 3 cung nở dần từ miệng tướng mình (dưới phải) về phía đối thủ (trên trái)
    mouth, foe = np.array([520, 520]), np.array([240, 300])
    d = foe - mouth
    ang = math.degrees(math.atan2(d[1], d[0]))
    for k, f in enumerate((0.25, 0.55, 0.85)):
        size = int(120 + 260 * f)
        im = tinted(ims[k % 4], TINT, 0.95 - 0.25 * f).resize((size, size), Image.LANCZOS).rotate(-ang, expand=True, resample=Image.BICUBIC)
        p = mouth + d * f
        base.alpha_composite(im, (int(p[0] - im.width / 2), int(p[1] - im.height / 2)))
    sheet.paste(base.convert("RGB"), (0, 0))
    for i, im in enumerate(ims):
        cell = Image.new("RGBA", (200, 395), (120, 170, 210, 255))
        cell.alpha_composite(tinted(im, TINT).resize((190, 190)), (5, 10))
        cell2 = Image.new("RGBA", (190, 190), (243, 226, 184, 255))
        cell2.alpha_composite(tinted(im, TINT).resize((190, 190)))
        cell.paste(cell2, (5, 200))
        sheet.paste(cell.convert("RGB"), (720 + i * 200, 0))
    sheet.save(os.path.join(OUT, "xem.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    ims = [make(i) for i in range(4)]
    for i, im in enumerate(ims):
        im.save(os.path.join(OUT, f"hat_kr_songchi_{i}.png"))
    preview(ims)
    print("ghi", OUT)
    if "--xuat" in sys.argv:
        for i in range(4):
            shutil.copy2(os.path.join(OUT, f"hat_kr_songchi_{i}.png"), ASSET)
        print("chép sang", ASSET)


if __name__ == "__main__":
    main()
