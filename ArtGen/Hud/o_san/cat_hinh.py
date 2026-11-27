# Cắt hình cột phải sảnh kiểu ô vuông (GPT 2.6 qua Magnific 2026-11-27, to_a.png: lưới 2 x 2 ô 512; hang, sổ phép, đền; ô dưới phải trống)
# ra Assets/03 Art/Icons/san_<tên>.png (cạnh dài 400, giữ tỉ lệ; thư mục Icons/ có mipmap). Dùng trong ô vuông viền trắng
# (Shop/v3/o_san_nen + o_san_vien, ve_ui.py hub_tile) do Editor/HubTileMenu.cs dựng.
# py -3 -I cat_hinh.py
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Icons"))
LONG = 400
PICK = [("hang", "to_a.png", 0, 0), ("so_phep", "to_a.png", 1, 0), ("den", "to_a.png", 0, 1)]

os.makedirs(DST, exist_ok=True)
for name, sheet, cx, cy in PICK:
    im = np.array(Image.open(os.path.join(HERE, sheet)).convert("RGBA"))
    cell = im[cy * 512:(cy + 1) * 512, cx * 512:(cx + 1) * 512].copy()
    a = cell[..., 3]
    a[a < 10] = 0
    ys, xs = np.nonzero(a > 0)
    piece = Image.fromarray(cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    s = LONG / max(piece.size)
    piece = piece.resize((round(piece.width * s), round(piece.height * s)), Image.LANCZOS)
    piece.save(os.path.join(DST, f"san_{name}.png"))
    print(name, piece.size)
