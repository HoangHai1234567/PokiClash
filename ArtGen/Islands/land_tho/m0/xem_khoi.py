# Xem trước cột khói đảo Hỏa (IslandAnim.Plume, cùng công thức C#) trên ảnh nền thật: tờ 12 khung + GIF ở xem_khoi/.
# Chạy: py -3 -I xem_khoi.py
import math
import io
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vat_dong import TINH  # noqa: E402

ANIM = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Assets", "03 Art", "Islands", "Anim"))
OUT = os.path.join(HERE, "xem_khoi")
SC = 3  # phóng ảnh nền cho dễ xem


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hsh(seed, i):
    v = math.sin(seed * 12.9898 + i * 78.233) * 43758.547
    return v - math.floor(v)


def smooth(a, b, x):
    x = min(1, max(0, (x - a) / (b - a)))
    return x * x * (3 - 2 * x)


def frame(bg, plumes, big, small, t):
    im = bg.copy()
    for seed, (x, y), w0, ex in plumes:
        w = w0 * SC
        n = int(ex.get("n", 7))
        life = float(ex.get("l", 3.8))
        wind = float(ex.get("v", 1))
        low = hexc(ex.get("c", "#e0dbd1"))
        high = tuple(c + (1 - c) * 0.65 for c in low)
        for i in range(n):
            o = i / n * life + hsh(seed, i) * 0.25
            age = (t + o) % life
            k = age / life
            gen = math.floor((t + o) / life)
            r = hsh(seed, gen * 31 + i)
            sp = small if (i + gen) % 3 == 0 else big
            e = 1 - (1 - k) ** 1.8
            rise = e * w * 2.0
            drift = k ** 1.4 * w * 0.9 * wind + math.sin(age * 1.5 + r * 6.3) * w * 0.1 * (0.3 + k) + (r - 0.5) * w * 0.5 * k
            sc = (0.35 + 1.25 * (1 - (1 - k) ** 2)) * (0.75 + 0.5 * r)
            a = k / 0.1 if k < 0.1 else (1 if k < 0.45 else 1 - smooth(0, 1, (k - 0.45) / 0.55))
            m = smooth(0, 1, min(1, k * 1.4))
            col = tuple(low[j] + (high[j] - low[j]) * m for j in range(3))
            pw = max(2, int(w * sc))
            ph = max(2, int(pw * sp.height / sp.width))
            p = sp.resize((pw, ph), Image.LANCZOS).rotate(-((r - 0.5) * 30 + k * 20 * wind), expand=True, resample=Image.BICUBIC)
            px = p.load()
            q = Image.new("RGBA", p.size)
            qp = q.load()
            for yy in range(p.height):
                for xx in range(p.width):
                    R, G, B, A = px[xx, yy]
                    qp[xx, yy] = (int(R * col[0]), int(G * col[1]), int(B * col[2]), int(A * a * 0.95))
            cx, cy = x * SC + drift, y * SC - rise
            im.alpha_composite(q, (int(cx - q.width / 2), int(cy - q.height / 2)))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    src = Image.open(os.path.join(HERE, "..", "nen", "nen_be_vung_2.png")).convert("RGBA")
    big = Image.open(os.path.join(ANIM, "anim_smoke_big.png")).convert("RGBA")
    small = Image.open(os.path.join(ANIM, "anim_smoke_small.png")).convert("RGBA")
    plumes = [(i, t[1], t[2], t[3]) for i, t in enumerate(TINH) if t[0] == "plume"]
    views = {"lo_gom": (820, 160, 1000, 320)}
    for name, box in views.items():
        bg = src.crop(box).resize(((box[2] - box[0]) * SC, (box[3] - box[1]) * SC), Image.LANCZOS)
        loc = [(sd, (x - box[0], y - box[1]), w, ex) for sd, (x, y), w, ex in plumes if box[0] <= x <= box[2] and box[1] <= y <= box[3]]
        frames = [frame(bg, loc, big, small, 10 + f / 15) for f in range(60)]  # 4 giây, 15 hình/giây
        frames[0].save(os.path.join(OUT, name + ".gif"), save_all=True, append_images=frames[1:], duration=66, loop=0, disposal=2)
        th = [f.resize((f.width // 2, f.height // 2)) for f in frames[::5]]
        sheet = Image.new("RGBA", (th[0].width * 4, th[0].height * 3), "white")
        for j, f in enumerate(th):
            sheet.paste(f, ((j % 4) * f.width, (j // 4) * f.height))
        sheet.convert("RGB").save(os.path.join(OUT, name + "_12.png"))
        print(name, len(loc), "cột")


if __name__ == "__main__":
    main()
