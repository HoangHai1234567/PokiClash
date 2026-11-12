# -*- coding: utf-8 -*-
"""Hình hạt GAI cho chiêu mana "Gồng Gai" của Cầu Gai (suất tien_la, đảo Mộc; 2026-11-12). Cùng quy ước với fire.py / la.py: ảnh xám
có vân chì nhuộm bằng Image.color + bản trắng đặc làm lớp mực, mũi chĩa LÊN.

- thorn: một cái gai (nón mập gốc tròn một mũi nhọn, như gai kem của tướng);
- tuft:  cụm gai trồi từ đất (đế thấp, 4–6 gai xoè như vương miện);
- shard: dăm gai gãy.

Ảnh GPT (gói hat_gai của build_hat.py, nhập bằng `build_hat.py --nhap hat_gai` về hat_gpt/thorn_*, tuft_*, shard_*) có thì dùng, thiếu
thì dùng hình thuật toán ở đây. Lúc xuất mọi hình được ĐẶT LẠI trong khung vuông theo một quy ước để game khỏi phải đo:
  thorn, tuft: hình cao hoặc rộng tối đa 92% khung, canh giữa ngang, ĐÁY hình nằm ở 96% chiều cao khung (game cắm đáy xuống đất);
  shard: canh giữa.

    py -3 -I ArtGen/Spine/gai.py            ghi hat_thorn_<i>, hat_thorns_<i>, hat_tuft_<i>, hat_tufts_<i>, hat_shard_<i>, hat_shards_<i>
                                            vào Assets/03 Art/Fx/Hat (không đụng ảnh hạt khác)
    py -3 -I ArtGen/Spine/gai.py xem <ra>   tờ xem thử (nhuộm kem trên nền xám)
Sau đó chạy lại hai menu Unity gán ảnh hạt: "PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)" và "…Hộp chi tiết tướng: hạt lửa + nút Mana".
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fire  # noqa: E402
from lightning import SS, _down  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Fx", "Hat"))
GPT = os.path.join(HERE, "hat_gpt")
DAY = 0.96   # đáy hình ở chỗ này của khung (thorn, tuft)
LAP = 0.92   # hình chiếm tối đa chừng này khung


def _gai_poly(goc, mui, rong, cong=0.0, n=14):
    """đa giác một cái gai: gốc (x, y) giữa đáy, mũi (x, y), bề rộng đáy; gốc phình tròn, thon nhanh về mũi; cong = độ lệch giữa thân."""
    gx, gy = goc
    mx, my = mui
    dx, dy = mx - gx, my - gy
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    tr, ph = [], []
    for i in range(n + 1):
        t = i / n
        w = rong / 2 * (1 - t) ** 0.72 * min(1.0, 0.72 + 2.2 * t)                          # gốc bo vào một chút, thân nón hơi phồng
        lech = cong * L * math.sin(math.pi * t) * 0.5
        cx, cy = gx + ux * L * t + nx * lech, gy + uy * L * t + ny * lech
        tr.append((cx + nx * w, cy + ny * w))
        ph.append((cx - nx * w, cy - ny * w))
    return tr + ph[::-1]


def _mask(S, polys, tron=()):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon(p, fill=255)
    for (x, y, r) in tron:
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return m


def thorn(seed, size=96, solid=False):
    S = size * SS
    c = S / 2
    cao = S * (0.62, 0.86, 0.74, 0.50)[seed % 4]
    rong = S * (0.34, 0.15, 0.24, 0.34)[seed % 4]
    cong = (0.0, 0.03, 0.22, -0.06)[seed % 4]
    y0 = c + cao / 2
    p = _gai_poly((c, y0), (c + cong * cao * 0.3, y0 - cao), rong, cong)
    m = _mask(S, [p], [(c, y0 - rong * 0.02, rong * 0.37)])
    return _down(fire._mask_to(m, solid), (c, c))


def tuft(seed, size=128, solid=False):
    rng = np.random.RandomState(9100 + seed)
    S = size * SS
    c = S / 2
    cao, be, nga = ((0.84, 0.44, 0.0), (0.50, 0.84, 0.0), (0.72, 0.62, -0.22), (0.72, 0.62, 0.22))[seed % 4]
    y0 = c + S * cao / 2
    k = (5, 6, 5, 5)[seed % 4]
    polys, tron = [], []
    for i in range(k):
        t = (i + 0.5) / k * 2 - 1                                  # -1 .. 1 từ trái sang phải
        gx = c + t * S * be * 0.20
        goc = t * (1.0 if be > cao else 0.5) + nga * 1.5            # góc xoè (rad), ngả theo cụm
        dai = S * cao * (1.0 - 0.42 * abs(t) ** 1.3) * rng.uniform(0.9, 1.0) * (0.96 if i % 2 else 1.0)
        mui = (gx + math.sin(goc) * dai, y0 - math.cos(goc) * dai)
        rong = S * min(be, cao) * 0.26 * rng.uniform(0.85, 1.0)
        polys.append(_gai_poly((gx, y0 - S * 0.03), mui, rong, 0.05 * t))
        tron.append((gx, y0 - S * 0.02, rong * 0.42))
    m = _mask(S, polys, tron)
    d = ImageDraw.Draw(m)
    d.rectangle([0, y0, S, S], fill=0)                               # đáy phẳng (cắm xuống đất)
    return _down(fire._mask_to(m, solid), (c, c))


def shard(seed, size=64, solid=False):
    rng = np.random.RandomState(9300 + seed)
    S = size * SS
    c = S / 2
    if seed % 4 == 0:      # đầu gai gãy: mũi nhọn, đầu kia nham nhở
        p = [(c, c - S * 0.36), (c + S * 0.14, c + S * 0.14), (c + S * 0.05, c + S * 0.30), (c - S * 0.03, c + S * 0.18), (c - S * 0.15, c + S * 0.28)]
    elif seed % 4 == 1:    # dăm mảnh hai đầu nhọn
        p = [(c + S * 0.04, c - S * 0.40), (c + S * 0.09, c), (c - S * 0.03, c + S * 0.40), (c - S * 0.08, c + S * 0.02)]
    elif seed % 4 == 2:    # mẩu ba góc dày
        p = [(c - S * 0.04, c - S * 0.30), (c + S * 0.28, c + S * 0.20), (c - S * 0.26, c + S * 0.24)]
    else:                  # mảnh cong ngắn
        p = [(c - S * 0.20, c + S * 0.30), (c - S * 0.06, c - S * 0.10), (c + S * 0.24, c - S * 0.32), (c + S * 0.08, c + S * 0.02), (c - S * 0.04, c + S * 0.26)]
    p = [(x + rng.uniform(-1, 1) * S * 0.012, y + rng.uniform(-1, 1) * S * 0.012) for x, y in p]
    return _down(fire._mask_to(_mask(S, [p]), solid), (c, c))


HINH = {"thorn": (thorn, 128, True), "tuft": (tuft, 256, True), "shard": (shard, 96, False)}   # (hàm, cỡ xuất, cắm đáy)


def _dat(im, co, day):
    """đặt hình vào khung vuông co x co theo quy ước ở đầu file."""
    im = im.convert("RGBA")
    bb = im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not bb:
        return Image.new("RGBA", (co, co), (0, 0, 0, 0))
    im = im.crop(bb)
    k = LAP * co / max(im.size)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    out = Image.new("RGBA", (co, co), (0, 0, 0, 0))
    y = round(DAY * co) - im.height if day else (co - im.height) // 2
    out.paste(im, ((co - im.width) // 2, y))
    return out


def lay(ten, i, solid):
    """ảnh GPT trong hat_gpt nếu có, không thì hình thuật toán; đã đặt theo quy ước."""
    ham, co, day = HINH[ten]
    f = os.path.join(GPT, f"{ten}_s_{i}.png" if solid else f"{ten}_{i}.png")
    im = Image.open(f) if os.path.exists(f) else ham(i, solid=solid)[0]
    return _dat(im, co, day), os.path.exists(f)


def xuat():
    for ten in HINH:
        for i in range(4):
            for solid in (False, True):
                im, gpt = lay(ten, i, solid)
                f = os.path.join(OUT, f"hat_{ten}{'s' if solid else ''}_{i}.png")
                im.save(f, optimize=True)
        print(ten, "GPT" if gpt else "thuật toán", HINH[ten][1])


def xem(ra):
    os.makedirs(ra, exist_ok=True)
    sh = Image.new("RGB", (4 * 200 + 20, 3 * 210 + 10), (150, 150, 150))
    for r, ten in enumerate(HINH):
        for i in range(4):
            f, s = lay(ten, i, False)[0], lay(ten, i, True)[0]
            f, s = f.resize((180, 180), Image.LANCZOS), s.resize((180, 180), Image.LANCZOS)
            big = s.resize((188, 188))
            ink = Image.new("RGBA", big.size, (43, 33, 24, 255))
            sh.paste(ink, (10 + i * 200 - 4, 10 + r * 210 - 4), big)
            t = np.asarray(f).astype(np.float32)
            t[..., :3] = t[..., :3] * np.array((244, 232, 190)) / 255.0
            t = Image.fromarray(t.astype(np.uint8), "RGBA")
            sh.paste(t, (10 + i * 200, 10 + r * 210), t)
    sh.save(os.path.join(ra, "gai_xem.png"))
    print(os.path.join(ra, "gai_xem.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:2] == ["xem"]:
        xem(sys.argv[2])
    else:
        xuat()
