# -*- coding: utf-8 -*-
"""Cổ Vương Nhi (tuong_cot_non, dạng 1 của Cổ Vương; rig monster_3273): mảnh "ĐÚNG CHỖ, ĐÚNG CỠ" gen từ concept đã duyệt (tai_ve/L1_duyet.png
= hướng A, người dùng chọn 2026-11-17: thân tròn đá xám lục, vương miện đá hai tầng + hai rễ lá như tai, một mắt xanh hẹp dưới gờ mày, hốc
bụng là cụm pha lê lá trong vòng rễ, hai nắm tay đá quấn rễ, hai chân đá ngắn).

Mảnh (bên = theo NGƯỜI XEM)  → part / xương của họ
    than      thân tròn + gờ mày + miệng + đai eo + vòng rễ quanh hốc (hốc tối, KHÔNG pha lê, KHÔNG mắt)   ← P_shenti + P_neibu (shenti)
    mu        vương miện đá hai tầng + hai rễ cong có lá                                                ← P_bashou (bone8 + shenti)
    loi       cụm pha lê lá trong hốc bụng                                                              ← shenti
    mat       mắt mở (tròng xanh, con ngươi, chấm trắng)                                                ← P_yanjing01 (bone9) / shenti
    mat_nham  mắt nhắm (vẽ ở góc trống, đặt trùng chỗ mat)                                              ← đổi hình lúc trúng đòn / chết
    tay_trai  nắm tay đá bên trái tranh (trước thân) + vòng rễ cổ tay                                   ← P_shou01 (bone6)
    tay_phai  nắm tay đá bên phải tranh (sau thân) + vòng rễ                                            ← P_shou02 (bone7)
    chan_trai / chan_phai  chân đá ngắn                                                                 ← P_tui01 (bone3) / P_tui02 (bone4)

    tuong_cot_non_manh.py can | prompt | cat [nhóm] | ghep
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402
import quy_nui_manh as Q  # noqa: E402

tho5.CON["tuong_cot_non"] = ("monster_3273", 6, 30)
G = tho5.dat("tuong_cot_non")
W, H = 1536, 1024
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "tuong_cot_non_1")
Q.G, Q.CONCEPT, Q.MANH, Q.GUI = G, CONCEPT, MANH, GUI

TAM = {"than": (780, 620), "mu": (770, 260), "loi": (805, 640), "mat": (870, 440), "mat_nham": (1330, 160),
       "tay_trai": (470, 620), "tay_phai": (1080, 615), "chan_trai": (620, 835), "chan_phai": (870, 835)}

NHOM = {
    "N1": [("than", "the ROUND STONE BODY (around x 540-1020, y 360-875) with its thick carved stone BROW slab over the eye, the short "
            "mouth line, the carved band round the waist and the brown ROOT RING round the belly socket, but WITHOUT the green crystals "
            "and WITHOUT the eye",
            "complete it as one closed round body: where the green crystals were, draw a darker stone hollow inside the root ring; where "
            "the green eye was, draw plain grey-green stone (keep the brow above it); the parts hidden behind the fists, the crown, the "
            "root horns and the feet continue as the same stone; NO crown, NO root horns, NO fists, NO feet")],
    "N2": [("mu", "the HEADPIECE: the small pointed two-tier stone CROWN on top (around x 700-910, y 85-370) together with the TWO curved "
            "brown ROOT HORNS with their green leaves at its left (around x 480-700, y 140-410) and its right (around x 935-1065, y 155-370)",
            "keep the crown and the two root horns exactly; complete their bottoms (hidden by the body) as short rounded ends"),
           ("loi", "the cluster of green CRYSTALS in the belly socket (around x 725-885, y 545-725)",
            "keep only the crystals, completed into one closed cluster shape (no root ring, no stone)"),
           ("mat", "the open green EYE under the brow (around x 815-925, y 405-470)", "keep only the eye shape (green iris, dark pupil, small "
            "white dot) with its ink outline, completed as a closed almond shape (its top edge as if the brow were not there)"),
           ("mat_nham", "a NEW small piece: the SAME EYE but tightly CLOSED in a fierce squint (a short thick dark curved line on a small "
            "almond patch of the body stone colour, the same size as the open eye). Draw it in the EMPTY top-right corner (around x 1260-1400, "
            "y 110-210), NOT on the face", "one closed almond shape the same size as the open eye"),
           ("tay_trai", "the LEFT stone FIST with its root wrap (around x 370-585, y 510-725)", "complete its side hidden by the body as a "
            "rounded wrist end"),
           ("tay_phai", "the RIGHT stone FIST with its root wrap (around x 995-1160, y 505-725)", "complete its side hidden by the body as "
            "a rounded wrist end"),
           ("chan_trai", "the LEFT stubby stone FOOT (around x 575-665, y 785-875)", "complete its top hidden by the body as a rounded end"),
           ("chan_phai", "the RIGHT stubby stone FOOT (around x 835-905, y 795-875)", "complete its top hidden by the body as a rounded end")],
}

ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a small round ancient stone statue spirit turned to the "
        "right: a round grey-green stone body with a carved waist band, a small two-tier pointed stone crown on top with two curved brown "
        "root horns ending in green leaves, one narrow fierce green eye under a thick stone brow, a short firm mouth, a cluster of green "
        "crystals held by a brown root ring in a round belly socket, two round stone fists wrapped by roots at its sides, two stubby stone "
        "feet. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")


def prompt():
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ từ concept đã chọn (2026-11-17; người dùng chọn A = `L1_duyet.png`)", "",
          f"Ảnh mẫu duy nhất (ảnh 1) = `{tho5.Wp(CONCEPT)}`. Gen bằng Magnific (GPT 2.6).", ""]
    for nh, ds in NHOM.items():
        out, save = Q.luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {tho5.Wp(CONCEPT)}: {ANH1}", ""] + save + ["",
             "CANVAS: landscape 1536x1024, the same frame as image 1.", "",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + Q.STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between the "
             "kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "Plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        Q.ghi(p, t)
        gd += [f"- **{nh}** ({', '.join(s for s, _, _ in ds)}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}`."]
        print(p)
    Q.ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def cat(chi=None):
    Q.TAM = TAM
    Q.NHOM = NHOM
    Q.cat(chi)
    # mắt nhắm: đặt trùng tâm mắt mở
    DATJ = Q.nap_dat()
    if "mat" in DATJ and "mat_nham" in DATJ:
        a, b = DATJ["mat"]["hop"], DATJ["mat_nham"]["hop"]
        cx, cy = (a[0] + a[2]) / 2, (a[1] + a[3]) / 2
        w, h = b[2] - b[0], b[3] - b[1]
        x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
        DATJ["mat_nham"]["hop"] = [x0, y0, x0 + w, y0 + h]
        Q.ghi_dat(DATJ)
        print("mat_nham đặt trùng tâm mat", DATJ["mat_nham"]["hop"])


THU_TU = ["chan_phai", "chan_trai", "tay_phai", "than", "loi", "mu", "mat", "tay_trai"]


def ghep():
    Q.THU_TU = THU_TU
    Q.ghep()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        Q.can()
    elif cmd == "prompt":
        prompt()
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)
