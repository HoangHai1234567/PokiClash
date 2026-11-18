# Xem thử kiểu vẽ vùng boss chưa mở (người dùng 2026-11-18: "để làm phần tối cho đẹp chứ dùng kiểu đen đen shader kia không đẹp").
# Dựng trên ảnh đảo đã xuất (Assets/03 Art/Islands/land_thuy.png) và mặt nạ vùng (land_thuy_vung_<k>.png, khung trong zones.json):
# - A "phác chì": vùng khoá thành bản phác chưa tô màu: nét mực nâu giữ lại, phần tô thành giấy kem có vân chì gạch chéo theo độ đậm;
# - B "mây phủ": mây vẽ tay (land_thuy_may_1/2) chất kín vùng khoá.
# Ghi m0/xem_khoa.png: hàng trên A, hàng dưới B; cột trái tiến độ 23, cột phải tiến độ 45. Chạy: py -3 -I xem_khoa.py
import json
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Islands")
ZONES = os.path.join(ROOT, "Assets", "02 Data", "Json", "zones.json")
PW = 1500  # bề ngang ảnh xem

zs = json.load(open(ZONES, encoding="utf-8"))
zs = zs["zones"] if isinstance(zs, dict) else zs
land = next(z for z in zs if isinstance(z, dict) and z.get("id") == "thuy")["land"]
habs, secs = land["habs"], land["secs"]
img = Image.open(os.path.join(ART, "land_thuy.png")).convert("RGB")
img = img.resize((PW, round(PW * img.height / img.width)), Image.LANCZOS)
W, H = img.size
col = np.asarray(img).astype(np.float32) / 255


def lock_mask(prog):
    """vùng khoá theo ảnh trường vùng (Baked/Islands/land_thuy_vung.png), cùng công thức shader PokiClash/UILandSketch"""
    opened = 1 + sum(1 for h in habs[:-1] if prog >= h["stage"])
    fld = Image.open(os.path.join(ROOT, "Assets", "03 Art", "Baked", "Islands", "land_thuy_vung.png")).convert("RGB").resize((W, H), Image.BILINEAR)
    fa = np.asarray(fld).astype(np.float32)
    v = fa[..., 0] / 25.0
    t = np.clip((v - (opened - 0.72)) / 0.44, 0, 1)
    return (t * t * (3 - 2 * t)) * fa[..., 1] / 255


# ---------- A: phác chì chưa tô ----------
g = col @ np.array([0.3, 0.59, 0.11], np.float32)
loc = g - ndi.gaussian_filter(g, 1.6)
ink = np.clip((-loc - 0.025) * 14, 0, 1)
ink = np.maximum(ink, np.clip((0.3 - g) * 6, 0, 1))  # nét viền đậm sẵn có
yy, xx = np.mgrid[0:H, 0:W]
hatch = ((np.sin((xx + yy * 1.4) * 0.85) > 0.55).astype(np.float32) * np.clip((0.85 - g) * 1.1, 0, 0.7))
rng = np.random.default_rng(3)
grain = ndi.gaussian_filter(rng.random((H, W)).astype(np.float32), 0.8)
paper = np.array([0.955, 0.925, 0.855], np.float32)
inkc = np.array([0.36, 0.27, 0.20], np.float32)
fill = paper[None, None, :] * (1 - 0.32 * hatch[..., None]) * (0.97 + 0.06 * grain[..., None])
sketch = fill * (1 - ink[..., None] * 0.85) + inkc * ink[..., None] * 0.85


def style_a(prog):
    m = lock_mask(prog)[..., None]
    out = col * (1 - m) + sketch * m
    return Image.fromarray((out.clip(0, 1) * 255).astype(np.uint8))


# ---------- B: mây phủ ----------
clouds = [Image.open(os.path.join(ART, f"land_thuy_may_{i}.png")).convert("RGBA") for i in (1, 2)]


def style_b(prog):
    m = lock_mask(prog)
    out = img.convert("RGBA")
    # nền mây kem dưới đám mây (chỗ hở giữa các đám không lộ cảnh)
    base = np.zeros((H, W, 4), np.uint8)
    base[..., :3] = (253, 245, 231)
    base[..., 3] = (np.clip((m - 0.35) * 2.2, 0, 1) * 255).astype(np.uint8)
    out.alpha_composite(Image.fromarray(base))
    r = random.Random(7)
    pts = []
    step = 46
    for y in range(0, H, step):
        for x in range(0, W, step):
            jx, jy = x + r.uniform(-18, 18), y + r.uniform(-14, 14)
            if 0 <= int(jy) < H and 0 <= int(jx) < W and m[int(jy), int(jx)] > 0.45:
                pts.append((jy, jx))
    pts.sort()
    for jy, jx in pts:
        c = clouds[r.randrange(2)]
        w = int(r.uniform(95, 150))
        c2 = c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)
        if r.random() < 0.5:
            c2 = c2.transpose(Image.FLIP_LEFT_RIGHT)
        out.alpha_composite(c2, (int(jx - c2.width / 2), int(jy - c2.height / 2)))
    return out.convert("RGB")


def style_c(prog):
    """kết hợp (bản làm thật): phác chì dưới, mây phủ theo dữ liệu xuất (land.secs[k].clouds) trên"""
    opened = 1 + sum(1 for h in habs[:-1] if prog >= h["stage"])
    out = style_a(prog).convert("RGBA")
    c = Image.open(os.path.join(ART, land.get("cloud", "land_thuy_may_2") + ".png")).convert("RGBA")
    for k, sec in enumerate(secs):
        if k < opened:
            continue
        for x, y, w, fl in sec.get("clouds", []):
            ww = max(4, int(w * W))
            c2 = c.resize((ww, max(2, int(ww * c.height / c.width))), Image.LANCZOS)
            if fl:
                c2 = c2.transpose(Image.FLIP_LEFT_RIGHT)
            out.alpha_composite(c2, (int(x * W - c2.width / 2), int(y * H - c2.height / 2)))
    return out.convert("RGB")


if "--c" in sys.argv:
    f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
    pa, pb = style_c(23), style_c(45)
    sheet = Image.new("RGB", (W * 2 + 12, H + 34), "white")
    d = ImageDraw.Draw(sheet)
    sheet.paste(pa, (0, 34)); sheet.paste(pb, (W + 12, 34))
    d.text((6, 4), "phác chì + mây phủ, tiến độ 23", fill=(0, 0, 0), font=f)
    d.text((W + 18, 4), "tiến độ 45", fill=(0, 0, 0), font=f)
    sheet.save(os.path.join(HERE, "xem_khoa_c.png"))
    print("đã ghi xem_khoa_c.png")
    sys.exit(0)

f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
panels = [("A phác chì, tiến độ 23", style_a(23)), ("A phác chì, tiến độ 45", style_a(45)),
          ("B mây phủ, tiến độ 23", style_b(23)), ("B mây phủ, tiến độ 45", style_b(45))]
sheet = Image.new("RGB", (W * 2 + 12, (H + 34) * 2), "white")
d = ImageDraw.Draw(sheet)
for i, (nm, im) in enumerate(panels):
    x, y = (i % 2) * (W + 12), (i // 2) * (H + 34)
    sheet.paste(im, (x, y + 34))
    d.text((x + 6, y + 4), nm, fill=(0, 0, 0), font=f)
sheet.save(os.path.join(HERE, "xem_khoa.png"))
panels[0][1].crop((W // 3, H // 6, W * 5 // 6, H * 4 // 5)).save(os.path.join(HERE, "xem_khoa_A_gan.png"))
panels[2][1].crop((W // 3, H // 6, W * 5 // 6, H * 4 // 5)).save(os.path.join(HERE, "xem_khoa_B_gan.png"))
print("đã ghi", os.path.join(HERE, "xem_khoa.png"))
