"""Xuất ảnh hạt của bộ hiệu ứng lửa và nước (fire.py, water.py, hoặc ảnh GPT trong hat_gpt/ nếu có) thành PNG cho Unity:
Assets/03 Art/Fx/Hat/hat_<tên>.png. Lớp hạt C# (HatLua.cs) tìm ảnh theo tên; menu "PokiClash/Prefab/Sàn đấu: hạt lửa" gán vào
StageView. Tên có tiền tố hat_ để không trùng ảnh thay thế trong 03 Art/Fallback (fx_*).
Chạy: py -3 -I xuat_hat.py
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

import fire

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))
GPT = os.path.join(HERE, "hat_gpt")


def gpt_or(name, i, solid, make):
    f = os.path.join(GPT, f"{name}_s_{i}.png" if solid else f"{name}_{i}.png")
    return Image.open(f).convert("RGBA") if os.path.exists(f) else make()


def to_gray(im):
    """ảnh màu có viền mực -> xám nhuộm được: độ sáng < 90 (mực) giữ, còn lại kéo về 215..255."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    lum = a[..., :3].mean(axis=2)
    g = np.where(lum < 90, lum, 215 + (lum - 90) / 165 * 40)
    a[..., 0] = a[..., 1] = a[..., 2] = np.clip(g, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def ring_pair(size=512, band=0.05, ink=0.022):
    """vòng mỏng: dải xám nhuộm được + vòng mực đặc rộng hơn (vẽ dưới)."""
    S = size
    c = S / 2
    R = S * 0.47
    out = []
    for solid in (False, True):
        m = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(m)
        e = ink * S if solid else 0
        ro, ri = R + e, R - band * S - e
        d.ellipse([c - ro, c - ro, c + ro, c + ro], fill=255)
        d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=0)
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        im.paste(Image.new("RGBA", (S, S), (255, 255, 255, 255) if solid else (236, 236, 236, 255)), (0, 0), m)
        out.append(im)
    return out


def van_chi(size=128, ss=3):
    """ô vân chì LẶP ĐƯỢC cho mảng nước liền (HatMang.cs): nền xám nhạt, nét gạch chéo sẫm theo đường 3x + 4y = 32k (lặp sau 128 px
    cả hai chiều); 4 kiểu nét (đậm nhạt, dày mỏng, lệch) xoay vòng nên vẫn lặp. Không trong suốt."""
    S = size * ss
    im = Image.new("RGB", (3 * S, 3 * S), fire.GRAY)
    d = ImageDraw.Draw(im)
    rng = np.random.RandomState(31)
    var = [(rng.uniform(-5, 5), rng.uniform(0.55, 1.0), rng.uniform(0.9, 1.5)) for _ in range(4)]
    for k in range(-80, 200):
        jit, amt, wd = var[k % 4]
        c = (32 * k + jit) * ss
        col = tuple(int(fire.GRAY[i] + (fire.HATCH_LO[i] - fire.GRAY[i]) * amt) for i in range(3))
        # 3x + 4y = c trên khung 3S: hai đầu ở x = -S và x = 4S
        d.line([(-S, (c + 3 * S) / 4), (4 * S, (c - 12 * S) / 4)], fill=col, width=max(1, int(wd * ss)))
    return im.crop((S, S, 2 * S, 2 * S)).resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    items = {}
    for i in range(4):
        items[f"blob_{i}"] = gpt_or("blob", i, False, lambda i=i: fire.blob(i, size=128)[0])
        items[f"solid_{i}"] = gpt_or("blob", i, True, lambda i=i: fire.blob_solid(i, size=128)[0])
        items[f"sblob_{i}"] = gpt_or("sblob", i, False, lambda i=i: fire.cloud(i, size=128)[0])  # khói dạng mây cuộn
        items[f"ssolid_{i}"] = gpt_or("sblob", i, True, lambda i=i: fire.cloud(i, size=128, solid=True)[0])
        items[f"burst_{i}"] = fire.burst(i, size=160)[0]  # chớp nổ sao gai
        items[f"bursts_{i}"] = fire.burst(i, size=160, solid=True)[0]
        items[f"lobe_{i}"] = gpt_or("lobe", i, False, lambda i=i: fire.flame_lobes(i, size=128)[0])  # lưỡi lửa kiểu tranh tướng
        items[f"lobes_{i}"] = gpt_or("lobe", i, True, lambda i=i: fire.flame_lobes(i, size=128, solid=True)[0])
        items[f"hook_{i}"] = gpt_or("hook", i, False, lambda i=i: fire.hook(i, size=128)[0])
        items[f"hooks_{i}"] = gpt_or("hook", i, True, lambda i=i: fire.hook(i, size=128, solid=True)[0])
        items[f"rock_{i}"] = gpt_or("rock", i, False, lambda i=i: fire.lava_rock(i, size=72)[0])
        items[f"crack_{i}"] = fire.lava_crack(i, size=260)[0]
        items[f"ash_{i}"] = fire.ash(i, size=24)[0]
    for i in range(3):
        items[f"curl_{i}"] = fire.curl(i, size=96)[0]
    for i in range(2):
        items[f"streak_{i}"] = fire.streak(i, length=80, width=14)[0]
        items[f"ember_{i}"] = fire.ember(i, size=32)[0]
        # bản xám nhuộm được theo màu chủ đề của tướng (viền mực giữ tối, ruột về trắng xám)
        items[f"streakg_{i}"] = to_gray(items[f"streak_{i}"])
        items[f"emberg_{i}"] = to_gray(items[f"ember_{i}"])
    items["starg_0"] = to_gray(fire.star4(0, size=48)[0])
    items["star_0"] = fire.star4(0, size=48)[0]
    items["needle_0"] = fire.needle(0, size=160)[0]
    items["needles_0"] = fire.needle(0, size=160, solid=True)[0]
    items["ell"] = fire.ellipse_solid(size=128)[0]
    items["ring"], items["rings"] = ring_pair()
    # cung xoáy của lốc: 12 góc đầu (mỗi 30°), dài 150°, trên vòng tròn (game bóp dẹt thành elip, không xoay ảnh); bản xám + bản mực
    S = 384
    for a in range(0, 360, 30):
        for solid in (False, True):
            im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            pad = 18
            bw = 16 + (10 if solid else 0)
            box = [pad, pad, S - pad, S - pad]
            d.arc(box, a, a + 150, fill=(255, 255, 255, 255) if solid else (236, 236, 236, 255), width=bw)
            if not solid:  # đầu cung tròn cho mềm
                pass
            items[f"arc{'s' if solid else ''}_{a // 30}"] = im
    # bộ Thủy (2026-11-10): lưỡi sóng cuộn, giọt, vương miện nước / nước toé, bọt; ảnh GPT trong hat_gpt (thiếu thì hình water.py)
    import water

    def small(im, side):
        if max(im.size) > side:
            im = im.resize((round(im.width * side / max(im.size)), round(im.height * side / max(im.size))), Image.LANCZOS)
        return im
    for i in range(4):
        items[f"wave_{i}"] = small(gpt_or("wave", i, False, lambda i=i: water.wave(i)[0]), 256)
        items[f"waves_{i}"] = small(gpt_or("wave", i, True, lambda i=i: water.wave(i, solid=True)[0]), 256)
        items[f"drop_{i}"] = small(gpt_or("drop", i, False, lambda i=i: water.drop(i)[0]), 128)
        items[f"drops_{i}"] = small(gpt_or("drop", i, True, lambda i=i: water.drop(i, solid=True)[0]), 128)
        items[f"foam_{i}"] = small(gpt_or("foam", i, False, lambda i=i: fire.cloud(i, size=128)[0]), 192)
        items[f"foams_{i}"] = small(gpt_or("foam", i, True, lambda i=i: fire.cloud(i, size=128, solid=True)[0]), 192)
        f = os.path.join(GPT, f"crown_{i}.png")
        if os.path.exists(f):
            im = Image.open(f).convert("RGBA")
            bb = im.getbbox()
            print(f"crown_{i}: rộng {(bb[2] - bb[0]) / im.width:.3f} cao {(bb[3] - bb[1]) / im.height:.3f} (HatNuoc.cs CrownF)")
            items[f"crown_{i}"] = small(im, 384)
            items[f"crowns_{i}"] = small(Image.open(os.path.join(GPT, f"crown_s_{i}.png")).convert("RGBA"), 384)
    for k, im in items.items():
        im.save(os.path.join(OUT, f"hat_{k}.png"), optimize=True)
    van_chi().save(os.path.join(OUT, "van_chi.png"), optimize=True)
    print(len(items), "ảnh ->", OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
