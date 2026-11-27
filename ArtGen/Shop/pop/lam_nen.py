# Thu banner về 1024 × 512, bo góc trong suốt và vẽ viền mực nâu (hơi rung) quanh mép: popup dùng thẳng, không cần mặt nạ.
# py -3 -I lam_nen.py  (đọc tai_ve/nen_<màu>.png, ghi out/pop_nen_<màu>.png)
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, R, LINE, SS = 1024, 512, 34, 7, 4
INK = (59, 42, 30, 255)

def wobble_path(w, h, r, step=6, amp=1.2, seed=1):
    rnd = random.Random(seed)
    pts = []
    def arc(cx, cy, a0, a1):
        n = 10
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    def line(x0, y0, x1, y1):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / (step * 8)))
        for i in range(1, n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    arc(r, r, 180, 270); line(r, 0, w - r, 0)
    arc(w - r, r, 270, 360); line(w, r, w, h - r)
    arc(w - r, h - r, 0, 90); line(w - r, h, r, h)
    arc(r, h - r, 90, 180); line(0, h - r, 0, r)
    out = []
    for (x, y) in pts:
        out.append((x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)))
    return out

for n in ["hong", "xanh", "tim", "cam"]:
    src = Image.open(os.path.join(HERE, "tai_ve", f"nen_{n}.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
    big = (W * SS, H * SS)
    inset = LINE / 2 + 1
    pts = [((x * (W - 2 * inset) / W + inset) * SS, (y * (H - 2 * inset) / H + inset) * SS) for x, y in wobble_path(W, H, R, seed=hash(n) & 0xffff)]
    mask = Image.new("L", big, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)
    src.putalpha(mask)
    ink = Image.new("RGBA", big, (0, 0, 0, 0))
    ImageDraw.Draw(ink).line(pts + [pts[0]], fill=INK, width=LINE * SS, joint="curve")
    ink = ink.resize((W, H), Image.LANCZOS)
    out = Image.alpha_composite(src, ink)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    out.save(os.path.join(HERE, "out", f"pop_nen_{n}.png"), optimize=True)
    print("out/pop_nen_%s.png" % n)
