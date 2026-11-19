# Ảnh con tàu và mặt biển cho bến tàu sảnh / chuyến tàu qua mây / màn tải (người dùng 2026-11-19).
# Vào: tau_3_huong_1.png (GPT: cùng một tàu nhìn từ sau = đi lên, từ trước = đi xuống, ngang = đi sang phải; nền trắng),
#      ben_tau_vung_1.png (vùng bến GPT vẽ, lấy nét sóng trắng).
# Ra Assets/03 Art/Ship/:
#   tau_len.png, tau_xuong.png, tau_ngang.png : tàu, cùng một tỉ lệ; gốc (0,5; 0,25) = giữa vòng nước ở mớn nước
#   tau_song_1..4.png                         : nét sóng trắng (cắt từ tranh, cỡ bằng sóng trên bản đồ sảnh)
#   tau_bot_1..3.png                          : cụm bọt sau đuôi tàu (vẽ bằng mã)
#   tau_vet.png, tau_vet_1..10.png            : vệt sóng chữ V sau đuôi, 10 khung động (đỉnh ở giữa cạnh trên, mờ dần xuống dưới)
#   tau_mui_1..6.png                          : sóng mũi tàu (nước rẽ ở mũi), 6 khung động; mũi ở giữa, gần cạnh trên (gốc 0,5; 0,8)
#   tau_bien.png                              : mặt biển 512 x 512 nối liền bốn phía (màu, vân chì sáp của biển trên bản đồ)
# py -3 -I cat_tau.py  [--soi]
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "Assets", "03 Art", "Ship")
SHEET = os.path.join(HERE, "tau_3_huong_1.png")
PIER = os.path.join(HERE, "ben_tau_vung_1.png")
MAP = os.path.join(os.path.dirname(HERE), "concept_I_ben_tau.png")
SIDE_W = 240  # bề ngang tàu nhìn ngang trên sảnh (đơn vị khung 1080; bản đồ ảnh 1024 hiện 1728)
PIVOT_Y = 0.25  # gốc tàu cách đáy ảnh 25 % chiều cao
WAVE_K = 1728 / 1024 / (1536 / 464)  # sóng trong ảnh vùng bến (phóng 3,31 lần) → cỡ trên sảnh


def cut_white(im):
    """Nền trắng nối mép → trong suốt; dải mép 2 px tách màu trắng (trừ ánh trắng còn dính quanh nét mực)."""
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    mn, mx = a.min(2), a.max(2)
    white = (mn > 228) & (mx - mn < 18)
    lab, _ = ndimage.label(white)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    alpha = np.where(bg, 0.0, 1.0)
    # dải mép: alpha theo độ "trắng" để khỏi viền trắng
    near = ndimage.binary_dilation(bg, iterations=2) & ~bg
    wness = np.clip((mn - 150) / (255 - 150), 0, 1)
    alpha[near] = np.clip(1 - wness[near], 0, 1)
    out = a.copy()
    m = near & (alpha > 0.02)
    for c in range(3):
        ch = out[..., c]
        ch[m] = np.clip((ch[m] - (1 - alpha[m]) * 255) / alpha[m], 0, 255)
    rgba = np.dstack([out, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def ring_box(rgba):
    """Vòng nước xanh ngọc ở mớn nước: (giữa x, giữa y)."""
    a = np.asarray(rgba, dtype=np.int16)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    m = (al > 128) & (g > 150) & (b > 170) & (r < 140)
    ys, xs = np.nonzero(m)
    # bỏ cờ đuôi nheo (cũng xanh ngọc) ở nửa trên ảnh
    keep = ys > rgba.height * 0.55
    xs, ys = xs[keep], ys[keep]
    return (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2


def ships():
    sheet = cut_white(Image.open(SHEET))
    # tách ba tàu theo mảng liền (đèn lồng tàu ngang vắt qua ranh một phần ba ảnh): mảng nhỏ về tàu gần nhất
    al = np.asarray(sheet.getchannel("A")) > 20
    lab, n = ndimage.label(al)
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(al, lab, range(1, n + 1))
    big = sorted(np.argsort(sizes)[-3:], key=lambda i: objs[i][1].start)
    centers = [(objs[i][1].start + objs[i][1].stop) / 2 for i in big]
    owner = np.zeros(n + 1, int)
    for i in range(n):
        cx = (objs[i][1].start + objs[i][1].stop) / 2
        owner[i + 1] = int(np.argmin([abs(cx - c) for c in centers])) + 1
    pix = np.asarray(sheet).copy()
    cols, boxes = [], []
    for j in range(3):
        mask = owner[lab] == j + 1
        one = pix.copy()
        one[..., 3] = np.where(mask, one[..., 3], 0)
        im = Image.fromarray(one, "RGBA")
        cols.append(im)
        boxes.append(im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    k = SIDE_W / (boxes[2][2] - boxes[2][0])
    names = ["tau_len", "tau_xuong", "tau_ngang"]
    out = []
    for c, bb, n in zip(cols, boxes, names):
        c = c.crop(bb)
        cx, cy = ring_box(c)
        c = c.resize((round(c.width * k), round(c.height * k)), Image.LANCZOS)
        cx, cy = cx * k, cy * k
        half = max(cx, c.width - cx) + 2
        below, above = c.height - cy, cy
        H = math.ceil(max(above / (1 - PIVOT_Y), below / PIVOT_Y)) + 2
        Wd = math.ceil(half * 2)
        canvas = Image.new("RGBA", (Wd, H), (0, 0, 0, 0))
        top = round(H * (1 - PIVOT_Y) - cy)
        canvas.paste(c, (round(Wd / 2 - cx), top), c)
        canvas.save(os.path.join(OUT, n + ".png"), optimize=True)
        out.append(canvas)
        print(n, canvas.size)
    return out


def waves():
    im = Image.open(PIER).convert("RGB")
    a = np.asarray(im, dtype=np.int16)
    mn = a.min(2)
    # vùng biển trống phía dưới bến
    y0, y1 = 700, 1000
    sub = mn[y0:y1]
    m = sub > 222
    lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=2))
    picks = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        fill = m[sl].mean()
        if 60 <= w <= 230 and 14 <= h <= 60 and w > 2.6 * h and fill < 0.42 and sl[1].start > 4 and sl[1].stop < im.width - 330:
            picks.append((w * h, sl))
    picks.sort(key=lambda p: -p[0])
    out = []
    for j, (_, sl) in enumerate(picks[:4]):
        ys = slice(sl[0].start + y0 - 4, sl[0].stop + y0 + 4)
        xs = slice(sl[1].start - 4, sl[1].stop + 4)
        crop = a[ys, xs]
        w = np.clip((crop.min(2) - 190) / (250 - 190), 0, 1)
        lab2 = (np.asarray(lab[sl[0].start - 4 if sl[0].start >= 4 else 0: sl[0].stop + 4, xs]) > 0)
        rgba = np.zeros(crop.shape[:2] + (4,), np.uint8)
        rgba[..., :3] = 255
        rgba[..., 3] = (w * 255).astype(np.uint8)
        img = Image.fromarray(rgba, "RGBA")
        img = img.resize((max(8, round(img.width * WAVE_K)), max(6, round(img.height * WAVE_K))), Image.LANCZOS)
        img.save(os.path.join(OUT, f"tau_song_{j + 1}.png"), optimize=True)
        out.append(img)
        print("song", j + 1, img.size)
    return out


def foam():
    rng = np.random.default_rng(7)
    out = []
    for j in range(3):
        S = 4  # vẽ to rồi thu cho mịn
        size = 56
        img = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        blobs = []
        for _ in range(4 + j):
            r = rng.uniform(8, 15) * S
            x = size * S / 2 + rng.uniform(-11, 11) * S
            y = size * S / 2 + rng.uniform(-7, 7) * S
            blobs.append((x, y, r))
        for x, y, r in blobs:  # viền ngọc nhạt
            d.ellipse([x - r - 2.5 * S, y - r * 0.8 - 2.5 * S, x + r + 2.5 * S, y + r * 0.8 + 2.5 * S], fill=(178, 238, 250, 255))
        for x, y, r in blobs:
            d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=(255, 255, 255, 255))
        img = img.resize((size, size), Image.LANCZOS)
        img.save(os.path.join(OUT, f"tau_bot_{j + 1}.png"), optimize=True)
        out.append(img)
    return out


def wake(n=10):
    """Vệt chữ V sau đuôi, n khung động: đoạn bọt trên hai tia trôi dần ra sau, tia gợn nhẹ, bọt giữa vệt nhấp nhô.
    Ra tau_vet_1..n.png (tau_vet.png = khung 1). Đỉnh chữ V ở giữa cạnh trên, mờ dần xuống dưới."""
    S = 3
    W, H = 220, 360
    first = None
    for f in range(n):
        ph = f / n
        img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        rng = np.random.default_rng(5)
        segs = []
        for sign in (-1, 1):
            pts = []
            for i in range(80):
                t = i / 79
                wob = 3.2 * math.sin(2 * math.pi * (t * 3.2 - ph)) * t  # gợn chạy dọc tia
                x = W / 2 + sign * (6 + 96 * t ** 0.8 + wob)
                y = 4 + (H - 10) * t
                pts.append((x * S, y * S, t))
            for i in range(len(pts) - 1):
                x0, y0, t = pts[i]
                x1, y1, _ = pts[i + 1]
                # đứt quãng dần về đuôi; mẫu đứt trôi theo pha (đoạn bọt chạy ra sau)
                u = (t * 9 - ph) % 1
                if t > 0.32 and u > 0.62 - 0.25 * (1 - t):
                    continue
                segs.append((x0, y0, x1, y1, t))
        for x0, y0, x1, y1, t in segs:
            w = (9 - 6 * t) * S
            d.line([(x0, y0), (x1, y1)], fill=(178, 238, 250, 255), width=int(w + 3 * S))
        for x0, y0, x1, y1, t in segs:
            w = (9 - 6 * t) * S
            d.line([(x0, y0), (x1, y1)], fill=(255, 255, 255, 255), width=int(w))
        # bọt giữa vệt: trôi ra sau theo pha, phồng xẹp
        for i in range(16):
            t = ((i + ph) / 15)
            if t > 1:
                continue
            r = (10 - 6 * t) * (0.85 + 0.25 * math.sin(2 * math.pi * (ph * 2 + i * 0.37))) * S
            x = W / 2 * S + rng.uniform(-6, 6) * S
            y = (10 + (H * 0.75) * t) * S
            d.ellipse([x - r - 2 * S, y - r * 0.7 - 2 * S, x + r + 2 * S, y + r * 0.7 + 2 * S], fill=(178, 238, 250, 255))
            d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(255, 255, 255, 255))
        img = img.resize((W, H), Image.LANCZOS)
        a = np.asarray(img).astype(np.float32)
        fade = np.clip(1.1 - np.linspace(0, 1, H) ** 0.9 * 1.1, 0, 1)[:, None]
        a[..., 3] *= fade
        out = Image.fromarray(a.astype(np.uint8), "RGBA")
        out.save(os.path.join(OUT, f"tau_vet_{f + 1}.png"), optimize=True)
        if first is None:
            first = out
            out.save(os.path.join(OUT, "tau_vet.png"), optimize=True)
    return first


def bow_waves(n=6):
    """Sóng mũi: hai mào bọt cong từ mũi tạt ra sau (chữ V ngắn, dày), tia nước li ti trước mũi; mỗi khung mào phồng / tia đổi chỗ."""
    S = 3
    W, H = 150, 130
    ax, ay = W / 2, H * 0.2  # mũi tàu (đỉnh chữ V)
    out = []
    for f in range(n):
        rng = np.random.default_rng(100 + f)
        ph = f / n * 2 * math.pi
        img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        blobs = []
        for side in (-1, 1):
            for i in range(9):
                t = i / 8
                x = ax + side * (6 + 52 * t ** 0.85 + 4 * math.sin(ph + t * 5))
                y = ay + 8 + 78 * t
                r = (11 - 6 * t) * (1 + 0.12 * math.sin(ph * 2 + i))
                blobs.append((x, y, r))
        for _ in range(7):  # tia nước trước mũi
            x = ax + rng.uniform(-22, 22)
            y = ay - rng.uniform(2, 20)
            blobs.append((x, y, rng.uniform(2.2, 4.5)))
        for x, y, r in blobs:
            d.ellipse([(x - r - 2) * S, (y - r * 0.8 - 2) * S, (x + r + 2) * S, (y + r * 0.8 + 2) * S], fill=(178, 238, 250, 255))
        for x, y, r in blobs:
            d.ellipse([(x - r) * S, (y - r * 0.8) * S, (x + r) * S, (y + r * 0.8) * S], fill=(255, 255, 255, 255))
        img = img.resize((W, H), Image.LANCZOS)
        a = np.asarray(img).astype(np.float32)
        fade = np.clip(1.15 - np.linspace(0, 1, H) ** 1.2 * 1.15, 0, 1)[:, None]
        a[..., 3] *= fade
        im = Image.fromarray(a.astype(np.uint8), "RGBA")
        im.save(os.path.join(OUT, f"tau_mui_{f + 1}.png"), optimize=True)
        out.append(im)
    return out


def sea():
    # màu biển: trung vị điểm biển trên bản đồ (vùng trống phía nam bến), bỏ bọt trắng
    m = np.asarray(Image.open(MAP).convert("RGB"), dtype=np.int16)[1430:1470, 700:900].reshape(-1, 3)
    m = m[(m.min(1) < 200) & (m[:, 2] > m[:, 0] + 60)]
    base = np.median(m, 0)
    L = m.mean(1)
    lo, hi = m[np.argsort(L)[int(len(L) * 0.04)]], m[np.argsort(L)[int(len(L) * 0.96)]]
    print("màu biển", base.astype(int), "tối", lo.astype(int), "sáng", hi.astype(int))
    N = 512
    S = 2
    img = Image.new("RGB", (N * S, N * S), tuple(int(v) for v in base))
    d = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(11)
    ang = math.radians(-38)
    for _ in range(5200):
        x, y = rng.uniform(0, N * S), rng.uniform(0, N * S)
        L = rng.uniform(10, 34) * S
        t = ang + rng.normal(0, 0.12)
        dx, dy = math.cos(t) * L / 2, -math.sin(t) * L / 2
        c = lo if rng.random() < 0.5 else hi
        col = tuple(int(v) for v in c) + (int(rng.uniform(90, 170)),)
        w = int(rng.integers(1, 3)) * S
        for ox in (-N * S, 0, N * S):
            for oy in (-N * S, 0, N * S):
                d.line([(x - dx + ox, y - dy + oy), (x + dx + ox, y + dy + oy)], fill=col, width=w)
    img = img.resize((N, N), Image.LANCZOS)
    img.save(os.path.join(OUT, "tau_bien.png"), optimize=True)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    sh = ships()
    wv = waves()
    fm = foam()
    wk = wake()
    bw = bow_waves()
    se = sea()
    if "--soi" in sys.argv:
        bg = Image.new("RGBA", (1100, 700), (255, 255, 255, 255))
        tile = se.convert("RGBA")
        for x in range(0, 1100, 512):
            for y in range(0, 700, 512):
                bg.paste(tile, (x, y))
        x = 20
        for s in sh:
            bg.alpha_composite(s, (x, 40))
            d = ImageDraw.Draw(bg)
            px, py = x + s.width / 2, 40 + s.height * (1 - PIVOT_Y)
            d.ellipse([px - 4, py - 4, px + 4, py + 4], outline=(255, 0, 0, 255), width=2)
            x += s.width + 30
        x = 20
        bg.alpha_composite(wk, (800, 40))
        for j, b in enumerate(bw):
            bg.alpha_composite(b, (640 + (j % 3) * 150, 330 + (j // 3) * 130))
        for w in wv + fm:
            bg.alpha_composite(w, (x, 520))
            x += w.width + 30
        bg.convert("RGB").save(os.path.join(HERE, "soi_tau.png"))


if __name__ == "__main__":
    main()
