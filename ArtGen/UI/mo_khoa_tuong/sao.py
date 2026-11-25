# Sao trắng viền mực cho màn mở khoá tướng (người dùng 2026-11-24: "có fx sao trắng khi nó bật ra"): sao 5 cánh bo tròn 128 px và
# lấp lánh 4 cánh 96 px, nét tay hơi rung, tô phẳng (không bóng, không quầng). Chạy: py -3 -I sao.py [thư mục ra]
# (mặc định Assets/03 Art/Shop của project chứa script).
import math, os, random, sys
from PIL import Image, ImageDraw

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "Assets", "03 Art", "Shop")
S = 8
INK = (43, 33, 24, 255)

def star(n, r_out, r_in, size, rot=-90):
    pts = []
    for k in range(n * 2):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(rot + k * 180 / n)
        pts.append((size / 2 + r * math.cos(a), size / 2 + r * math.sin(a)))
    return pts

def soften(pts, steps=6, amp=0.0, seed=3):
    # chia cạnh + rung nhẹ cho nét tay
    rnd = random.Random(seed)
    res = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        for j in range(steps):
            t = j / steps
            res.append((a[0] + (b[0] - a[0]) * t + rnd.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + rnd.uniform(-amp, amp)))
    return res

def draw(name, n, size, r_out, r_in, ink_w, round_r):
    img = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = [(x * S, y * S) for x, y in soften(star(n, r_out, r_in, size), amp=0.25)]
    # viền mực: vẽ hình to hơn bằng nét dày, rồi lòng trắng
    d.polygon(p, fill=INK)
    d.line(p + [p[0], p[1]], fill=INK, width=int(ink_w * 2 * S), joint="curve")
    for x, y in p:
        d.ellipse([x - ink_w * S, y - ink_w * S, x + ink_w * S, y + ink_w * S], fill=INK)
    pi = [(x * S, y * S) for x, y in soften(star(n, r_out - ink_w * 0.2, r_in - ink_w * 0.2, size), amp=0.2, seed=5)]
    d.polygon(pi, fill=(255, 255, 255, 255))
    d.line(pi + [pi[0], pi[1]], fill=(255, 255, 255, 255), width=int(round_r * S), joint="curve")
    img.resize((size, size), Image.LANCZOS).save(os.path.join(out, name))

draw("sao_trang.png", 5, 128, 50, 23, 5, 6)
draw("lap_lanh.png", 4, 96, 40, 11, 4, 4)
print("ok")
