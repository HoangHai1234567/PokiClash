# Ô cột nền trơn cho popup nhiều bậc / theo ngày (người dùng 2026-11-27: "làm màu trơn rồi trang trí hoa văn nhẹ nhàng thôi"): như o_nen của
# ve_ui.py (viền mực rung, tô chì) nhưng bỏ caro thoi để màu trơn, hoa văn do lớp hoa_van.png lo. Tấm xám để game tô màu.
# - o_tron_nut.png: có dải mực đáy cho nút giá (viền 9 mảnh 34,104,34,34 như o_nen);
# - o_tron.png: không dải đáy (ô ngày của Quà Nhập Môn; viền 34).
# Chạy: py -3 -I ArtGen/Shop/v3/ve_o_tron.py [--assets]  → out/ hoặc Assets/03 Art/Shop/v3/.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageChops, ImageDraw  # noqa: E402

import ve_ui as v  # noqa: E402


def plain_tile(name, w=276, h=420, r=24, line=6, strip=0):
    S = v.SS
    path = v.rr_path(line / 2 + 1.5, line / 2 + 1.5, w - line / 2 - 1.5, h - line / 2 - 1.5, r - line / 2)
    ring, shape = v.hand_stroke(w, h, path, line, 61 if strip else 63)
    lum = v.tex_fill(w, h, 23, spacing=8, drop=(5, 12))
    base = v.gray_rgba(lum, shape)
    if strip:
        wob = v.Wobble(67, 2.0)
        pts = [(0, h * S)] + [(x * S, (h - strip + wob(x)) * S) for x in range(0, w + 1, 3)] + [(w * S, h * S)]
        sm = Image.new("L", (w * S, h * S), 0)
        ImageDraw.Draw(sm).polygon(pts, fill=255)
        base.alpha_composite(v.ink_layer(ImageChops.multiply(sm, shape)))
    base.alpha_composite(v.ink_layer(ring))
    v.finish(base, w, h, name)


if __name__ == "__main__":
    plain_tile("o_tron_nut", strip=100)
    plain_tile("o_tron")
