# -*- coding: utf-8 -*-
"""Vua robot (vua_may): tờ HÌNH HIỆU ỨNG cho ba chiêu (đề xuất người dùng duyệt 2026-11-17 "làm đi"), vẽ theo nét game (bút mực, sáp, tô phẳng).
Lưới 3 × 2 ô 512 px trên tờ 1536 × 1024, mỗi ô một hình:
  hàng 1: cung (vệt cung lửa của cú vụt trượng) | an (Ấn Mặt Trời nhìn từ trên xuống) | cot (cột sáng dựng đứng)
  hàng 2: tia (một đoạn tia mặt trời nằm ngang, nối được) | nhat_thuc (đĩa đen + vành nhật hoa) | duoi (đuôi lửa thiên thạch, đầu tròn bên phải)

    vua_may_fx.py to     file prompt → gui_gpt/vua_may_1/luot_5_fx.txt
    vua_may_fx.py cat    cắt tờ FX_1.png theo ô → inbox/vua_may_1/manh/fx_<tên>.png (1 px / đơn vị rig, cỡ do rig co lại)
"""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vua_may as G  # noqa: E402
import vua_may_manh as VM  # noqa: E402

O = [["cung", "an", "cot"], ["tia", "nhat_thuc", "duoi"]]
TA = {
    "cung": "a flaming ARC TRAIL left by a scepter swung overhead: a thick crescent (a curved band like a quarter-to-half moon, about 30 % as "
            "thick as it is long, thick in the middle, tapering to sharp points at both ends), made of THREE flat bands side by side: pale "
            "cream-white #FFF6D8 along its inner (concave) edge, bright yellow #FFC93C in the middle, orange #FF9A3D along its outer edge, "
            "the outer edge broken into small wavy flame tongues",
    "an": "a round royal SUN SEAL seen from straight above, filling the cell: an outer ring of small gold #F9B825 laurel leaves, a band of "
          "short straight light rays in pale yellow #FFE69A, an inner ring of round pearls, and in the centre a flat sun disc #FFC93C with "
          "eight short pointed rays; the space between rings pale cream #FFF6D8",
    "cot": "a tall vertical PILLAR OF LIGHT standing on the ground: a tall straight column about one fifth as wide as it is tall, wider at "
           "the bottom, its top splitting into a few pointed flame tips, made of flat vertical bands: pale cream-white #FFF6D8 core, bright "
           "yellow #FFC93C bands, thin orange #FF9A3D edges; at its foot a small flat burst of short pointed rays",
    "tia": "one horizontal SEGMENT of a thick SUN BEAM, running straight from the LEFT edge of the cell to the RIGHT edge (so that copies "
           "can be put end to end), about one third of the cell high, with straight cut ends: flat horizontal bands from the middle out: a "
           "pale cream-white #FFF6D8 core, bright yellow #FFC93C, orange #FF9A3D edges with small wavy flame tongues along the top and "
           "bottom edges",
    "nhat_thuc": "a total SOLAR ECLIPSE: a round flat very dark disc #2A2B33 (the Moon / Earth in front of the Sun) in the middle, and round "
                 "it a jagged CORONA ring of long and short pointed flame rays in pale cream-white #FFF6D8 with a thin pale yellow #FFE69A "
                 "inner rim",
    "duoi": "the burning TAIL of a falling meteor lying horizontally: an empty round space at the RIGHT end (where the meteor ball will be, "
            "leave it white, do not draw the ball) and a long flame trail streaming out to the LEFT from it, wide at the right, thinning "
            "to wavy flame tips at the far left, made of flat bands: bright yellow #FFC93C next to the ball, orange #FF9A3D, a few red "
            "#E2552E flame tongues on its outer edges",
}


def prompt():
    con = os.path.join(G.TAI, "L1_duyet.png")
    out = os.path.join(G.TAI, "FX_1.png")
    p = os.path.join(VM.GUI, "luot_5_fx.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {os.path.normpath(con)}: OUR approved robot king (a hand-drawn game character with a little Sun on his scepter): match "
         "its drawing style (wobbly dark-brown ink outline, flat colours with visible crayon hatching, no shading) and its golden palette.",
         "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
         "If a file with that name already exists, save as FX_1_2.png, FX_1_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: draw a SHEET OF SIX separate game EFFECT drawings for the robot king's sun attacks, on a landscape 1536x1024 pure-white "
         "canvas divided (invisibly, draw NO grid lines) into 3 columns x 2 rows of 512x512 cells. ONE drawing per cell, centred in its "
         "cell, as big as the cell allows but never touching the cell edges (keep at least 30 px of white all round; the beam segment of "
         "cell 4 is the only one that goes from the left edge to the right edge of its cell).", ""]
    k = 1
    for r, hang in enumerate(O):
        for c, ten in enumerate(hang):
            t.append(f"{k}. row {r + 1}, column {c + 1} (cell x {c * 512}..{c * 512 + 512}, y {r * 512}..{r * 512 + 512}): {TA[ten]}.")
            k += 1
    t += ["", "STYLE: hand-drawn on paper like image 1: a wobbly dark-brown ink outline (#2B2118, about 6 px) round every shape and every "
          "colour band, every area ONE flat colour with visible crayon hatching. Light is shown ONLY by the pale colours and the ray "
          "shapes: NO glow, NO soft halo, NO gradients, NO blur, NO sparkles, NO shadows. No text, no numbers, no grid lines, pure-white "
          "(#FFFFFF) background everywhere else."]
    VM.ghi(p, t)
    print(p)


def cat():
    from quai import anh
    path = anh.to_moi_nhat(G.TAI, "FX_1")
    A = np.asarray(Image.open(path).convert("RGB").resize((1536, 1024), Image.LANCZOS))
    os.makedirs(VM.MANH, exist_ok=True)
    for r, hang in enumerate(O):
        for c, ten in enumerate(hang):
            o = A[r * 512:(r + 1) * 512, c * 512:(c + 1) * 512]
            nen = VM.nen_trang(o.astype(np.int32))
            m = ~nen
            ys, xs = np.nonzero(m)
            if not len(ys):
                print(ten, "TRỐNG")
                continue
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            if ten == "tia":                                   # đoạn tia: cắt thẳng hai đầu cho nối liền
                x0, x1 = x0 + 12, x1 - 12
            al = (m[y0:y1, x0:x1] * 255).astype(np.uint8)
            im = Image.fromarray(np.dstack([o[y0:y1, x0:x1], al]), "RGBA")
            im.save(os.path.join(VM.MANH, f"fx_{ten}.png"))
            print(f"fx_{ten}.png", im.size)


if __name__ == "__main__":
    {"to": prompt, "cat": cat}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
