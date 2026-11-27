# Cắt icon thưởng vẽ tay từ tờ GPT 2.6 (Magnific, 2026-11-27; to_a.png, to_b.png: lưới 2 x 2 ô 512, ô dưới phải trống)
# ra Assets/03 Art/Icons/icon_<tên>.png vuông 384 (ArtLibrary.Icon lấy "icon_<tên>" trước icon SVG Fallback/Icons/<tên>).
# py -3 -I cat_icon.py
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Icons"))
SIZE, MARGIN = 384, 0.03
PICK = [("exp", "to_a.png", 0, 0), ("ball", "to_a.png", 1, 0), ("hammer", "to_b.png", 0, 1)]

os.makedirs(DST, exist_ok=True)
for name, sheet, cx, cy in PICK:
    im = np.array(Image.open(os.path.join(HERE, sheet)).convert("RGBA"))
    cell = im[cy * 512:(cy + 1) * 512, cx * 512:(cx + 1) * 512].copy()
    a = cell[..., 3]
    a[a < 10] = 0  # bỏ hạt mờ lác đác quanh hình
    ys, xs = np.nonzero(a > 0)
    piece = Image.fromarray(cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    inner = int(SIZE * (1 - 2 * MARGIN))
    s = inner / max(piece.size)
    piece = piece.resize((max(1, round(piece.width * s)), max(1, round(piece.height * s))), Image.LANCZOS)
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    out.alpha_composite(piece, ((SIZE - piece.width) // 2, (SIZE - piece.height) // 2))
    out.save(os.path.join(DST, f"icon_{name}.png"))
    print(name, piece.size, "->", os.path.join(DST, f"icon_{name}.png"))
