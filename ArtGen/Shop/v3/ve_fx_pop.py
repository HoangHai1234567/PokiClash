# Sprite hiệu ứng cho popup bán bản 4 (người dùng 2026-11-27: "thêm fx glow ánh sáng các kiểu vào cho đẹp"; "thay vì dùng cột thì làm thành
# hướng mũi tên ngày 1 -> ngày 2 -> ngày 3 theo hình tam giác"):
# - quang.png 256: quầng sáng tròn mềm, trắng (game tô màu ấm, phập phồng) — người dùng xin glow riêng cho popup bán;
# - lap_lanh.png 64: sao bốn cánh lõm, lõi trắng, mép mềm (Twinkle rải quanh hình gói / huy hiệu);
# - vong_song.png 256: vòng sóng sáng mềm, trắng (chạm trúng ở minigame câu cá: vòng toả từ kim, 2026-11-27 "click chuẩn có ít fx bloom");
# - mui_ten.png 220×200: mũi tên cong vẽ tay (vàng hai tông, viền mực rung), đi lên rồi rẽ phải; xoay -90° thành rẽ xuống.
# Chạy: py -3 -I ArtGen/Shop/v3/ve_fx_pop.py [--assets]  → out/ hoặc Assets/03 Art/Shop/v3/.
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

import ve_ui as v  # noqa: E402


def glow(n=256):
    im = Image.new("L", (n, n), 0)
    px = im.load()
    c = (n - 1) / 2
    for y in range(n):
        for x in range(n):
            d = math.hypot(x - c, y - c) / c
            px[x, y] = int(255 * max(0.0, 1 - d) ** 2.2)
    out = Image.merge("RGBA", (Image.new("L", (n, n), 255),) * 3 + (im,))
    os.makedirs(v.OUT, exist_ok=True)
    out.save(os.path.join(v.OUT, "quang.png"))
    print("quang", n, n)


def ring(n=256):
    im = Image.new("L", (n, n), 0)
    px = im.load()
    c = (n - 1) / 2
    for y in range(n):
        for x in range(n):
            d = math.hypot(x - c, y - c) / c
            px[x, y] = int(255 * math.exp(-((d - 0.78) / 0.09) ** 2)) if d <= 1 else 0
    out = Image.merge("RGBA", (Image.new("L", (n, n), 255),) * 3 + (im,))
    out.save(os.path.join(v.OUT, "vong_song.png"))
    print("vong_song", n, n)


def sparkle(n=64):
    S = 4
    big = Image.new("L", (n * S, n * S), 0)
    c = n * S / 2
    pts = []
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        r = (n * S / 2 - 2) if i % 2 == 0 else n * S * 0.1
        pts.append((c + math.cos(a) * r, c + math.sin(a) * r))
    ImageDraw.Draw(big).polygon(pts, fill=255)
    a = big.resize((n, n), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.merge("RGBA", (Image.new("L", (n, n), 255),) * 3 + (a,))
    out.save(os.path.join(v.OUT, "lap_lanh.png"))
    print("lap_lanh", n, n)


def chaikin(pts, n=2):
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % len(pts)]
            out += [(ax * 0.75 + bx * 0.25, ay * 0.75 + by * 0.25), (ax * 0.25 + bx * 0.75, ay * 0.25 + by * 0.75)]
        pts = out
    return pts


def arrow(w=220, h=200, band=38, line=5):
    cx, cy, r = 140, 180, 108
    pts = []
    # mép ngoài cung (trái → trên), mũi tên, mép trong cung (trên → trái): chiều kim đồng hồ trên ảnh
    for i in range(0, 31):
        t = math.pi + (math.pi / 2) * i / 30
        pts.append((cx + (r + band / 2) * math.cos(t), cy + (r + band / 2) * math.sin(t)))
    ex, ey = cx, cy - r
    pts += [(ex, ey - band / 2 - 22), (ex + 62, ey), (ex, ey + band / 2 + 22)]
    for i in range(30, -1, -1):
        t = math.pi + (math.pi / 2) * i / 30
        pts.append((cx + (r - band / 2) * math.cos(t), cy + (r - band / 2) * math.sin(t)))
    pts = v.rough_poly(chaikin(pts, 3), 401, amp=0.9, step=3.0)
    ring, shape = v.hand_stroke(w, h, v.poly_path(pts, 1.5), line, 403, wob=0.7, inner_only=True)
    m = v.vgrad(w, h, [(0, 255), (0.55, 255), (0.62, 0), (1, 0)])
    rr, gg, bb = v.two_tone(w, h, m, v.hexc("#ffb21a"), v.hexc("#ffd84a"), 405, spacing=6)
    body = Image.merge("RGBA", (rr, gg, bb, shape))
    body.alpha_composite(v.ink_layer(ring))
    # viền trắng kiểu sticker bên ngoài (nổi trên nền tối)
    rim = shape.filter(ImageFilter.MaxFilter(31))  # ~5 px ở cỡ cuối (vẽ to gấp 3)
    im = Image.merge("RGBA", (Image.new("L", rim.size, 255),) * 3 + (rim,))
    im.alpha_composite(body)
    v.finish(im, w, h, "mui_ten")


if __name__ == "__main__":
    glow()
    ring()
    sparkle()
    arrow()
