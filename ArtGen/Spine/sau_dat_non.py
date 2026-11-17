# -*- coding: utf-8 -*-
"""Sa Trùng DẠNG 1 "Sa Trùng Nhi" (sau_dat_non; người dùng 2026-11-17: "tự nghĩ 1 mini version, cùng rig"). Cùng xương, lưới, clip với dạng 2
(sau_dat_rig.py, SD_DANG=non đổi tỉ lệ). Skill pokiclash-spine-rig "DẠNG KHÁC trên CÙNG rig gốc": tỉ lệ trước, concept sau (concept vẽ
trên bố cục rig dựng ra), rồi CHUYỂN DA (GPT vẽ lại mảnh của dạng 2, giữ hình bóng, đổi màu và chi tiết).

    sau_dat_non.py bocuc       ảnh bố cục rig dạng 1 (da dạng 2) khung 0 idle, 1536 × 1024 nền trắng → inbox/sau_dat_non/mau/bocuc.png
    sau_dat_non.py concept     file prompt concept hai hướng → gui_gpt/sau_dat_non/luot_1_concept_<A|B>.txt + HUONG_DAN.md
"""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H = 1536, 1024
BASE = os.path.join(HERE, "inbox", "sau_dat_non")
MAU, TAI = os.path.join(BASE, "mau"), os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "sau_dat_non")
CONCEPT2 = os.path.join(HERE, "inbox", "sau_dat_1", "tai_ve", "L1_duyet.png")
RONG_NON = os.path.join(HERE, "inbox", "rong_cat_non", "tai_ve", "L1_duyet.png")


def Wp(p):
    return os.path.normpath(p)


def bocuc():
    os.environ["SD_DANG"] = "non"
    os.environ["SD_DA2"] = "1"
    import sau_dat_rig as R
    from quai import hoat, soi
    sk, info = R.dung()
    clips = R.lam_clip(sk, info)
    P = hoat.nuong(sk, clips[1])[0]
    ve = soi.Ve(sk)
    x0, y0, x1, y1 = ve.bao(P)
    s = min(800 / (y1 - y0), 1250 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (cx - W / 2 / s, cy - H / 2 / s, cx + W / 2 / s, cy + H / 2 / s)
    im = ve.ve(P, box, s, bg=None, ss=2).resize((W, H), Image.LANCZOS)
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    out.alpha_composite(im)
    os.makedirs(MAU, exist_ok=True)
    p = os.path.join(MAU, "bocuc.png")
    out.convert("RGB").save(p)
    import json
    json.dump({"s": s, "cx": cx, "cy": cy}, open(p[:-4] + ".json", "w"), indent=1)       # px bố cục ↔ thế giới rig (khung 0 idle dạng 1)
    print(p, f"{s:.3f} px / đơn vị")


STYLE = ("DRAWING STYLE (very important): exactly the hand-drawn style of images 1 and 2: a wobbly dark-brown INK outline (#2B2118, about 7 "
         "px) round every piece, thinner ink lines (about 4 px) for the few inner lines, every area ONE flat colour with visible "
         "coloured-pencil / wax-crayon hatching. No shading, no highlights, no gradients, no glow, no shadows: flat colour only.")

TASK = ("TASK: draw the BABY FORM (the first, younger evolution stage) of our sandworm hero of image 2, in EXACTLY the POSE, the LAYOUT and "
        "the PROPORTIONS of image 1: image 1 is our own rig already posed at the baby proportions (big head, short thick body, small crest, "
        "short feelers, three small rock slabs, small rubble); every piece must stay at the same place, the same size and the same angle as "
        "in image 1 (laid over image 1, the outlines must almost coincide). Only the LOOK changes: younger, smaller, rounder and cuter, but "
        "still a brave little fighter (determined frowning eyes, never a happy mascot). Same species and identity as image 2: ring-segmented "
        "worm body, armoured head rings round a round mouth full of teeth, fan crest plates, whip feelers with amber barbs, strata slabs, "
        "dark earth chunks with amber cracks, earthworm tendrils, sand mound.")

HUONG = {
    "A": ("giữ bảng màu dạng 2, non hơn",
          "cùng màu vàng cát / kem / nâu sẫm như dạng 2 nhưng nhạt hơn một chút; vòng giáp đầu tròn mềm hơn, mắt hổ phách TO tròn (chấm sáng), "
          "răng nhỏ hơn và thưa hơn, hai ngà ngắn tù, mào tròn trơn",
          ["Colours like image 2 but a little lighter and softer: body rings pale sand #E2C08A with grooves #B08A55, belly cream #F1E2C0, head "
           "rings light sandstone #D6AA68, crest plates #E5C88E with one flat ochre edge band.",
           "Head: the same armour rings but rounder and softer, a BIG round amber eye (#F6C443, black pupil, one white dot) under a short "
           "frowning brow; the round mouth slightly open with FEWER, SMALLER, blunter cream teeth; two short stubby tusks.",
           "Everything else as in image 1 with the colours of image 2 (feelers dark brown with small amber barbs, slabs in strata bands, dark "
           "earth chunks with amber cracks, dusty-rose tendrils, sand mound)."]),
    "B": ("giun non hồng đất",
          "thân vòng đốt hồng đất nhạt như giun non, đầu là vỏ sa thạch mỏng màu kem, mắt hổ phách to, miệng tròn răng sữa nhỏ, mào là hai ba "
          "vảy kem nhỏ, râu nâu nhạt đầu hạt hổ phách",
          ["A YOUNG EARTHWORM look: body rings soft earthy pink #D9A08A with grooves #B07766, belly pale cream-pink #F2D8C8.",
           "Head: thin, still-soft armour rings of pale cream sandstone #E8D2A2 (darker #C9A874 on faces turned away), a BIG round amber eye "
           "(#F6C443, black pupil, one white dot) under a short frowning brow; the round mouth slightly open with a ring of small milk teeth "
           "#FBF3DF, inside terracotta #A2412E; two tiny tusk nubs.",
           "Crest plates small pale cream #EADBB6; feelers light brown #8C6A48 with tiny amber bead tips #EFA330; slabs in strata bands as in "
           "image 2; earth chunks dark brown with amber cracks; tendrils pink #D59A86; sand mound pale."]),
}


def concept():
    os.makedirs(GUI, exist_ok=True)
    bc = os.path.join(MAU, "bocuc.png")
    R = [(bc, "our own rig posed at the BABY proportions (drawn with the adult skin for now), 1536x1024, white background: copy its POSE, "
               "LAYOUT and PROPORTIONS exactly.", "Bố cục rig dạng 1 (tỉ lệ mini, tạm mặc da dạng 2), khung 0 idle"),
         (CONCEPT2, "our APPROVED adult form of the same hero (hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours): keep its "
                    "species, identity, materials and drawing style.", "Concept dạng 2 đã duyệt (Sa Trùng)")]
    hd = ["# Gói GPT: Sa Trùng Nhi (`sau_dat_non`), dạng 1 tướng 7 đảo Thổ", "",
          "Người dùng 2026-11-17: \"tự nghĩ 1 mini version, cùng rig\". Cùng rig `monster_3643` với dạng 2 (xương, lưới, chuyển động của nhà phát hành "
          "game gốc: dùng nội bộ). Ảnh 1 là bố cục rig ở tỉ lệ mini; concept vẽ lại đúng bố cục đó. Gen qua Magnific (GPT 2.6, 1k high, 95 credit).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", TASK, "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", STYLE, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow, the character at the same place "
              "and size as in image 1. No sparkles, no glow, no dust cloud, no labels, no frame."]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
        print(p)
    hd += ["", "Kiểm: đúng bố cục ảnh 1 (đầu to, thân ngắn, mào nhỏ, râu ngắn, ba phiến nhỏ), cùng loài với dạng 2, mặt quả quyết, mắt có chấm sáng; "
           "nét bút mực rung, vân sáp, tô phẳng; nền trắng."]
    open(os.path.join(GUI, "HUONG_DAN.md"), "w", encoding="utf-8", newline="\n").write("\n".join(hd) + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "bocuc":
        bocuc()
    elif a[0] == "concept":
        concept()
