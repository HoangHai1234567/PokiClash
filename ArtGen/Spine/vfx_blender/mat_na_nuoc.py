# -*- coding: utf-8 -*-
"""Sinh bộ MẶT NẠ MỀM cho hiệu ứng nước (ảnh xám 512², trắng = nước đặc, nhoè dần ra mép) → vfx_blender/mat_na/*.png.
Học cách của repo abitofgamedev/water_vfx (skill vfx-petclash/hoc_water_vfx_abitofgamedev.md, mục 1): mặt nạ phải MỀM để ngưỡng tan
quét qua dải xám thì hình co lại dần mà mép vẫn sắc (nuocbl.mask_mat). Tự sinh bằng đốm Gauss + nhiễu, không dùng ảnh của repo
(không có giấy phép).
  loang_<k>  : mây loang lỗ chỗ, dày ở đáy, mép trên rách; LẶP NGANG (dán quanh vành / ống)
  botmep_<k> : chuỗi cục bọt dọc mép trên; lặp ngang
  cham_<k>   : cụm chấm toé (một chấm to giữa + chấm nhỏ toả ra), nền đen
  vung_<k>   : vết loang hình sao (vũng nước), nền đen
  dac_<k>    : khối đặc gần đều có gợn (thân cầu, cục nước); lặp ngang
  ngon_<k>   : ngón vương miện (chân đặc ở đáy ảnh, ngón dựng lên, đầu tròn); lặp ngang
    py -3 -I mat_na_nuoc.py
"""
import math
import os

import cv2
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mat_na")
S = 512
os.makedirs(OUT, exist_ok=True)


def blob(img, x, y, r, a=1.0, wrap=False):
    """Đốm Gauss tâm (x, y) bán kính r (px); wrap: lặp ngang (vẽ thêm bản dời ±S)."""
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    for dx in ((-S, 0, S) if wrap else (0,)):
        img += a * np.exp(-(((xx - x - dx) ** 2 + (yy - y) ** 2) / (2 * r * r)))


def fbm(rng, oct_=4, base=4, wrap=True):
    """Nhiễu giá trị lặp ngang (lưới ngẫu nhiên phóng to bằng nội suy bậc ba, cộng nhiều tầng)."""
    acc = np.zeros((S, S), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(oct_):
        n = base * 2 ** o
        g = rng.random((n, n)).astype(np.float32)
        if wrap:
            g = np.concatenate([g, g[:, :1]], 1)          # cột cuối = cột đầu → lặp ngang
            up = cv2.resize(g, (S + S // n, S), interpolation=cv2.INTER_CUBIC)[:, :S]
        else:
            up = cv2.resize(g, (S, S), interpolation=cv2.INTER_CUBIC)
        acc += amp * up
        tot += amp
        amp *= 0.5
    return acc / tot


def norm(a):
    a = a - a.min()
    return a / (a.max() + 1e-6)


def save(name, a):
    cv2.imwrite(os.path.join(OUT, name + ".png"), (np.clip(a, 0, 1) * 255).astype(np.uint8))


def soften(a, s):
    return cv2.GaussianBlur(a, (0, 0), s, borderType=cv2.BORDER_WRAP if False else cv2.BORDER_REFLECT)


def radial(a, r0=0.34, r1=0.49):
    """Tắt dần về 0 ngoài bán kính r0 → r1 (tỉ lệ cạnh ảnh): sprite không chạm mép ảnh."""
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    r = np.hypot(xx - S / 2, yy - S / 2) / S
    return a * np.clip((r1 - r) / (r1 - r0), 0, 1) ** 1.5


def hblur(a, s):
    """Nhoè giữ lặp ngang: dán ba bản cạnh nhau, nhoè, cắt giữa."""
    t = np.concatenate([a, a, a], 1)
    t = cv2.GaussianBlur(t, (0, 0), s)
    return t[:, S:2 * S]


for k in range(3):
    rng = np.random.default_rng(11 + k)
    # ---- loang: dày ở đáy (v nhỏ = gần tâm vành / gốc), thưa và rách lên trên
    a = np.zeros((S, S), np.float32)
    for _ in range(60):
        y = S * (0.35 + 0.65 * rng.random() ** 0.7)
        blob(a, rng.random() * S, y, rng.uniform(22, 60), rng.uniform(0.5, 1.0), wrap=True)
    for _ in range(26):                                     # cục rời ở nửa trên → mép trên rách
        blob(a, rng.random() * S, S * rng.uniform(0.08, 0.45), rng.uniform(12, 30), rng.uniform(0.4, 0.9), wrap=True)
    a = norm(a) * (0.55 + 0.45 * fbm(rng))
    a = hblur(norm(a), 9)
    yy = np.linspace(0, 1, S)[:, None]
    a = a * (0.35 + 0.65 * np.clip(yy * 1.4, 0, 1))         # trên (y nhỏ trong ảnh) mỏng hơn
    save(f"loang_{k}", norm(a) ** 0.8)
    # ---- botmep: chuỗi cục dọc mép trên (y ~ 0,12–0,32), cỡ lệch
    b = np.zeros((S, S), np.float32)
    x = rng.random() * 30
    while x < S:
        r = rng.uniform(14, 34)
        blob(b, x % S, S * rng.uniform(0.14, 0.3), r, rng.uniform(0.7, 1.0), wrap=True)
        if rng.random() < 0.5:
            blob(b, (x + rng.uniform(-20, 20)) % S, S * rng.uniform(0.3, 0.45), r * 0.55, 0.7, wrap=True)
        x += r * rng.uniform(1.3, 2.4)
    b = hblur(norm(b) * (0.6 + 0.4 * fbm(rng, base=8)), 5)
    save(f"botmep_{k}", norm(b))
    # ---- cham: chấm to giữa + 6–9 chấm nhỏ toả ra (vệt nối mờ)
    c = np.zeros((S, S), np.float32)
    blob(c, S / 2, S / 2, rng.uniform(55, 70), 1.0)
    n = rng.integers(6, 10)
    for i in range(n):
        ang = 2 * math.pi * i / n + rng.uniform(-0.3, 0.3)
        d = rng.uniform(110, 200)
        r = rng.uniform(18, 40) * (1.2 - d / 300)
        blob(c, S / 2 + d * math.cos(ang), S / 2 + d * math.sin(ang), r, rng.uniform(0.7, 1.0))
        blob(c, S / 2 + d * 0.55 * math.cos(ang), S / 2 + d * 0.55 * math.sin(ang), r * 0.6, 0.5)
    c = soften(norm(c) * (0.7 + 0.3 * fbm(rng, base=6, wrap=False)), 6)
    save(f"cham_{k}", radial(norm(c), 0.4, 0.5))
    # ---- vung: vết loang sao — thân tròn mềm + 5–8 thuỳ, mép gợn
    v = np.zeros((S, S), np.float32)
    blob(v, S / 2, S / 2, 85, 1.0)
    n = rng.integers(5, 9)
    for i in range(n):
        ang = 2 * math.pi * i / n + rng.uniform(-0.35, 0.35)
        d = rng.uniform(90, 160)
        blob(v, S / 2 + d * math.cos(ang), S / 2 + d * math.sin(ang), rng.uniform(40, 70), rng.uniform(0.6, 0.95))
        if rng.random() < 0.6:
            blob(v, S / 2 + (d + 70) * math.cos(ang), S / 2 + (d + 70) * math.sin(ang), rng.uniform(16, 28), 0.7)
    v = soften(norm(v) * (0.75 + 0.25 * fbm(rng, base=6, wrap=False)), 8)
    save(f"vung_{k}", norm(radial(norm(v))))
    # ---- ngon: ngón vương miện — dải chân đặc (đáy ảnh = chân vành) + 6–8 ngón dựng lên cao lệch, đầu ngón tròn to hơn thân;
    # ngưỡng lên thì ngón mảnh dần rồi đầu ngón đứt ra thành giọt. Lặp ngang.
    g = np.zeros((S, S), np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    g += np.clip((yy - S * 0.72) / (S * 0.2), 0, 1) ** 0.7          # chân đặc
    nf = rng.integers(6, 9)
    for i in range(nf):
        x0 = S * (i + rng.uniform(0.2, 0.8)) / nf
        top = S * rng.uniform(0.1, 0.45)
        w = rng.uniform(10, 18)
        for yv in np.linspace(S * 0.95, top, 40):
            q = (S * 0.95 - yv) / (S * 0.95 - top)
            blob(g, x0 + 10 * math.sin(q * 3 + i), yv, w * (1.15 - 0.55 * q), 0.55, wrap=True)
        blob(g, x0 + 10 * math.sin(3 + i), top, w * 1.15, 1.0, wrap=True)   # đầu ngón tròn
    g = hblur(norm(g), 4)
    save(f"ngon_{k}", norm(g) ** 0.75)
    # ---- dac: khối đặc gần đều (0,62 → 1) có gợn mềm — thân cầu / cục nước: lúc đầu đặc, ngưỡng lên thì tan lấm tấm. Lặp ngang.
    save(f"dac_{k}", 0.62 + 0.38 * norm(hblur(fbm(rng, base=6), 3)))
print("ok", sorted(os.listdir(OUT)))
