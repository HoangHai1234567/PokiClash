# Huy hiệu giá trị sao nổ của popup chọn một gói (người dùng 2026-11-27, ảnh popup nạp đầu Clash of Critters: "giá trị phải để thẳng trên đầu
# luôn làm nổi bật"): sao nổ nhiều cánh tù, hồng đỏ hai tông có nét chì, viền mực rung, viền sáng trong như sticker; chữ "×N" / "GIÁ TRỊ" do
# game viết (OfferPopColumn.Badge). Dùng lại nét tay của ve_ui.py (bộ v3, phiên khác giữ), không sửa ve_ui.py.
# Chạy: py -3 -I ArtGen/Shop/v3/ve_huy_hieu.py [--assets]  → out/ hoặc Assets/03 Art/Shop/v3/huy_hieu.png (232×200, không viền 9 mảnh).
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageChops  # noqa: E402

import ve_ui as v  # noqa: E402


def chaikin(pts, n=2):
    """Bo tròn đỉnh đa giác kín (mũi cánh nhọn làm nét mực tràn gai ra ngoài)."""
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % len(pts)]
            out += [(ax * 0.75 + bx * 0.25, ay * 0.75 + by * 0.25), (ax * 0.25 + bx * 0.75, ay * 0.25 + by * 0.75)]
        pts = out
    return pts


def badge(w=232, h=200, line=6):
    cx, cy = w / 2, h / 2
    rx = w / 2 - line - 2
    # sao nổ 14 cánh tù, ép dọc theo tỉ lệ khung
    pts = v.burst_poly(cx, cy, rx * 0.8, rx * 1.03, 14, rot=-math.pi / 2, jitter=0.035, seed=201)
    k = (h / 2 - line - 2) / rx
    pts = chaikin([(x, cy + (y - cy) * k) for x, y in pts], 3)
    path = v.poly_path(v.rough_poly(pts, 203, amp=1.2, step=3.0), 1.5)
    ring, shape = v.hand_stroke(w, h, path, line, 205, wob=0.8, inner_only=True)
    m = v.vgrad(w, h, [(0, 255), (0.52, 255), (0.62, 0), (1, 0)])
    r, g, b = v.two_tone(w, h, m, v.hexc("#e01f63"), v.hexc("#ff3f86"), 207, spacing=6)
    im = Image.merge("RGBA", (r, g, b, shape))
    # viền sáng trong (sticker): nét chì hồng nhạt bám trong viền mực
    inner = [(cx + (x - cx) * 0.86, cy + (y - cy) * 0.86) for x, y in pts]
    rim, _ = v.hand_stroke(w, h, v.poly_path(v.rough_poly(inner, 209, amp=0.9, step=3.0), 1.5), 3.0, 211, wob=0.6, double=False)
    im.alpha_composite(v.ink_layer(ImageChops.multiply(rim, Image.new("L", rim.size, 170)), v.hexc("#ffd3e4")))
    im.alpha_composite(v.ink_layer(ring))
    v.finish(im, w, h, "huy_hieu")


if __name__ == "__main__":
    badge()
