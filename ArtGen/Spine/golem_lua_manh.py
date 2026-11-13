# -*- coding: utf-8 -*-
"""Golem lõi lửa (golem_lua): mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt (người dùng chọn A = L1_da_tro.png → L1_duyet.png, 2026-11-13).

Mọi mảnh của rig gốc monster_3422 là mảnh CỨNG một xương, nên mỗi tờ Codex vẽ lại concept nhưng chỉ giữ vài mảnh KHÔNG chồng nhau, vẽ đủ
phần khuất. Lưỡi lửa là mảnh riêng (sẽ thành lưới có chuỗi xương, uốn lượn: người dùng dặn "phần lửa bốc ra cũng phải có animation uốn
lượn nhẹ nhàng"), vẽ đủ GỐC chui vào lỗ. Ba lửa lớn (vai, đỉnh lưng, trán) nằm SAU một vòng lỗ riêng (vòng rỗng giữa); bốn lửa nhỏ nằm
SAU tấm của nó (cổ lỗ vẽ liền tấm, lòng lỗ tô màu lửa).

    golem_lua_manh.py build     → gui_gpt/golem_lua_1/luot_2_manh_<A..H>.txt (+ HUONG_DAN.md mục lượt 2)
    golem_lua_manh.py lam       → inbox/golem_lua_1/manh/<tên>.png + dat.json + _so_ghep.png + _to.png
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golem_lua as G  # noqa: E402
import mat_lua_manh as ML  # noqa: E402  (hàm chung: nen, manh_rgba, doi_mau)

MANH = os.path.join(G.BASE, "manh")
DUYET = os.path.join(G.TAI, "L1_duyet.png")
PK = os.path.join(HERE, "gui_gpt", "golem_lua_1")

HOLE = "a small flat yellow-orange hole (yellow #FFD45A centre, orange #F7902A rim, ink outline), no flame"
FLAME_ROOT = ("Complete its ROOT: in image 1 its bottom disappears into a hole; continue it as a thick rounded flame base {r}, "
              "closed with the ink outline (the base is the same orange / yellow as the flame). Do NOT draw any small separate "
              "floating flame bits next to it.")

# mảnh: (tờ, tâm ước chừng trên concept để cắt, slot gốc (để khớp khung concept ↔ rig; None = không khớp), mô tả tiếng Anh)
P = {
    # ---- tờ A
    "lung": ("A", (705, 330), "P_toujia10",
             "THE BACK SLAB: the big rounded stone slab of the hunched back, behind everything at the top middle (its visible part is "
             "the stone around the top flame's dark ring, about x = 560 to x = 850, y = 180 to y = 500). In image 1 most of it is "
             "hidden behind the near shoulder, the top plate, the cheek plate, the brow and the chest: draw the WHOLE slab as one big "
             "rounded boulder-like block about x = 545 to x = 900, y = 175 to y = 520, its top edge as in image 1. Where the top "
             "flame comes out (centre about x = 700, y = 255), paint a round hole about 115 px wide and 65 px tall: " + HOLE +
             " (no dark ring)."),
    "tay_gan": ("A", (395, 810), "P_shouR2",
                "THE NEAR HAND: the huge rounded stone hand at the lower left (about x = 245 to x = 545, y = 640 to y = 975) with its "
                "one groove line, WITHOUT its three dark claws and WITHOUT the dark wrist block above it: where the claws are, "
                "complete the stone with a rounded bottom edge; where the wrist block covers its top, complete its rounded top."),
    "lua_tran": ("A", (1140, 390), None,
                 "THE FOREHEAD FLAME: the flame shooting out to the right from the dark ring above the eye (about x = 1030 to "
                 "x = 1255, y = 280 to y = 505). Remove the ring, the eye and the head. " +
                 FLAME_ROOT.format(r="about 50 px further down-left into the ring, to about x = 1035, y = 500")),
    "chan_xa_ban": ("A", (800, 945), "P_tuiiL3",
                    "THE FAR FOOT: the small square stone foot under the far orange knee (about x = 755 to x = 850, y = 890 to "
                    "y = 990), complete: its top, hidden behind the knee ball, is a flat rounded top."),
    "vuot_xa1": ("A", (1235, 790), "P_shouzhiL4",
                 "THE TOP-RIGHT CLAW of the far hand: the big curved dark claw at the far right (about x = 1175 to x = 1290, y = 715 "
                 "to y = 865), complete: its root, hidden in the hand, is a rounded end."),
    # ---- tờ B
    "vai": ("B", (535, 430), "P_toujia6",
            "THE NEAR SHOULDER: the big round boulder-like stone plate at the upper left (about x = 385 to x = 690, y = 290 to "
            "y = 575) that carries the big dark ring of the shoulder flame. Remove the big flame and the dark ring: exactly where "
            "the ring sits (outer edge about x = 420 to x = 615, y = 285 to y = 455) paint a round hole the size of the ring's "
            "inside, " + HOLE + ". Complete the shoulder where the flames covered it, as one rounded boulder."),
    "dau": ("B", (985, 400), "P_tou3",
            "THE HEAD, all its stone as ONE piece: the skull-like face at the front right (about x = 990 to x = 1145, y = 440 to "
            "y = 605) with its notched lower edge and its round eye socket (paint the socket as a flat dark charcoal #3F3B46 disc, "
            "NO eye in it), the stone of the head rising behind it (the part showing right of the brow, about x = 1000 to "
            "x = 1085, y = 290 to y = 450), and the big brow plate with its vertical groove line (about x = 830 to x = 1010, "
            "y = 190 to y = 505). Keep the small dark collar on the back of the head (about x = 1020 to x = 1075, y = 300 to "
            "y = 345) and paint its opening as " + HOLE + ". Remove the forehead flame and its dark ring (complete the stone "
            "under them), the small flame on the back of the head, the eye, the dark jaw, the cheek plate, the top plate, the core."),
    "tay_xa": ("B", (1130, 820), "P_shouL4",
               "THE FAR HAND: the huge rounded stone hand at the lower right (about x = 990 to x = 1290, y = 650 to y = 975) with its "
               "groove line, WITHOUT its three dark claws and WITHOUT the dark wrist above it; complete its rounded top and its "
               "bottom edge behind the claws."),
    "chan_gan_ban": ("B", (570, 950), "P_tuiiR3",
                     "THE NEAR FOOT: the small square stone foot under the near orange knee (about x = 520 to x = 620, y = 905 to "
                     "y = 990), complete with a flat rounded top."),
    # ---- tờ C
    "lua_vai": ("C", (440, 290), None,
                "THE BIG SHOULDER FLAME (about x = 315 to x = 560, y = 140 to y = 430), without the small separate floating flame "
                "bit at its upper left. " + FLAME_ROOT.format(r="down into the ring, reaching about x = 525, y = 415")),
    "dinh": ("C", (830, 270), "P_toujia9",
             "THE TOP PLATE: the stone plate at the top between the back slab and the brow (about x = 745 to x = 905, y = 170 to "
             "y = 350), with the small dark collar on its top (about x = 860 to x = 930, y = 175 to y = 215): remove the small flame "
             "and paint the collar's opening as " + HOLE + ". Complete the plate where the brow and the cheek plate cover it, as one "
             "rounded slab reaching about y = 380."),
    "loi": ("C", (875, 585), "P_xiongqiang3",
            "THE FIRE CORE: the round fire disc in the chest (visible about x = 790 to x = 960, y = 500 to y = 670). In image 1 part "
            "of it is hidden behind the chest stone and the jaw: draw the WHOLE core as one full circle about 190 px across, centre "
            "about x = 875, y = 585, with the same flat fire colours and the flame shape inside as in image 1."),
    "mat": ("C", (1036, 500), "P_yanjing3",
            "THE EYE: the small round glowing yellow eye with its dark pupil (about x = 1015 to x = 1058, y = 478 to y = 522): one "
            "full small circle with an ink outline, no socket and no ring around it."),
    "vuot_gan1": ("C", (352, 900), "P_shouzhiR1",
                  "THE LEFT CLAW of the near hand (about x = 300 to x = 405, y = 830 to y = 975), complete with a rounded root."),
    "chan_xa_goi": ("C", (805, 878), "P_tuiiL2",
                    "THE FAR KNEE: the round glowing orange-yellow knee ball of the far leg (about x = 755 to x = 855, y = 840 to "
                    "y = 915), complete as a full round ball."),
    # ---- tờ D
    "lua_dinh": ("D", (695, 150), None,
                 "THE TALL TOP FLAME (about x = 610 to x = 780, y = 25 to y = 280), without the small floating bit at its left. " +
                 FLAME_ROOT.format(r="reaching down to about y = 285")),
    "ma": ("D", (845, 405), "P_jiapian2",
           "THE CHEEK PLATE: the long blade-shaped stone plate with one diagonal groove line, sweeping from the upper left down to "
           "the right under the brow (about x = 690 to x = 1000, y = 315 to y = 495). Complete the part hidden under the brow as a "
           "tapered blade end."),
    "co_tay_gan": ("D", (390, 635), "P_shouR1",
                   "THE NEAR WRIST BLOCK: the dark charcoal block above the near hand (about x = 260 to x = 520, y = 545 to y = 725). "
                   "Remove the flame on its top and paint where the flame comes out (about x = 330 to x = 430, y = 560 to y = 600) "
                   "as " + HOLE + ". Complete its lower part hidden behind the hand as a rounded end."),
    "hong": ("D", (695, 800), "P_kua1",
             "THE HIP BLOCKS: the group of chunky stone blocks under the belly between the two legs (about x = 590 to x = 800, "
             "y = 690 to y = 905), drawn as ONE piece (keep the ink lines between the blocks), including the dark collar where the "
             "small hip flame comes out (about x = 640 to x = 760, y = 720 to y = 800): remove the flame and paint the collar's "
             "opening as " + HOLE + "."),
    "vuot_xa2": ("D", (1095, 920), "P_shouzhiL6",
                 "THE BOTTOM-LEFT CLAW of the far hand (about x = 1045 to x = 1145, y = 860 to y = 980), complete."),
    # ---- tờ E
    "vo_nguc": ("E", (790, 620), "P_xiongqiang4",
                "THE CHEST SHELL: the thick curved stone that wraps around the fire core on its left and bottom (about x = 640 to "
                "x = 1000, y = 440 to y = 775), drawn as ONE big letter-C shaped piece; inside the C, where the core is, leave the "
                "round opening PURE WHITE (empty). Remove the core, the jaw, the hands, the hips, the legs."),
    "lua_dinh_nho": ("E", (900, 160), None,
                     "THE SMALL TOP FLAME (about x = 845 to x = 960, y = 95 to y = 215). " +
                     FLAME_ROOT.format(r="reaching about y = 222 (into the collar)")),
    "lua_sau_dau": ("E", (1050, 255), None,
                    "THE BACK-OF-HEAD FLAME (about x = 995 to x = 1105, y = 185 to y = 330). " +
                    FLAME_ROOT.format(r="reaching about y = 338")),
    "chan_gan_goi": ("E", (580, 895), "P_tuiiR2",
                     "THE NEAR KNEE: the round glowing knee ball of the near leg (about x = 530 to x = 630, y = 865 to y = 925), "
                     "complete as a full round ball."),
    "vuot_gan2": ("E", (462, 882), "P_shouzhiR2",
                  "THE MIDDLE CLAW of the near hand (about x = 420 to x = 505, y = 810 to y = 955), complete."),
    # ---- tờ F
    "vong_vai": ("F", (517, 370), None,
                 "THE BIG SHOULDER RING: the thick dark charcoal ring on the near shoulder (outer edge about x = 420 to x = 615, "
                 "y = 285 to y = 455), drawn as one complete closed oval band about 35 px thick; its central opening is PURE WHITE "
                 "(empty). Remove the flame inside it."),
    "vong_dinh": ("F", (700, 252), None,
                  "THE TOP RING: the thick dark ring the tall top flame comes out of (about x = 630 to x = 770, y = 205 to y = 300), "
                  "one complete closed oval band; its central opening is PURE WHITE (empty)."),
    "ham": ("F", (1015, 590), "P_zuiiba3",
            "THE LOWER JAW: the dark charcoal jaw block under the face (about x = 900 to x = 1130, y = 520 to y = 650). Its upper "
            "part is hidden behind the face's notched lower edge: complete it straight up to about y = 520. Only the jaw: not the "
            "dark wrist and arm below it."),
    "chan_xa_dui": ("F", (792, 810), "P_tuiiL1",
                    "THE FAR THIGH: the short stone thigh block above the far knee (about x = 735 to x = 850, y = 750 to y = 870), "
                    "complete as a rounded block (its lower end hidden behind the knee ball)."),
    "vuot_gan3": ("F", (535, 815), "P_shouzhiR3",
                  "THE RIGHT CLAW of the near hand, the dark claw standing at the right edge of the near hand (about x = 490 to "
                  "x = 580, y = 745 to y = 885), complete."),
    "lua_hong": ("F", (677, 742), None,
                 "THE SMALL HIP FLAME between the legs (about x = 630 to x = 725, y = 675 to y = 810). " +
                 FLAME_ROOT.format(r="reaching about y = 812")),
    # ---- tờ G
    "nguc_trai": ("G", (600, 585), "P_xiongjia5",
                  "THE LEFT CHEST BLOCK: the big rounded stone block at the left of the chest, between the near shoulder and the "
                  "hips (about x = 495 to x = 710, y = 445 to y = 725), complete as one chunky block (its top hidden behind the near "
                  "shoulder, its bottom behind the hips and the near hand)."),
    "vong_tran": ("G", (1052, 482), None,
                  "THE FOREHEAD RING: the short dark charcoal tube / collar above the eye that the forehead flame shoots out of "
                  "(about x = 995 to x = 1110, y = 450 to y = 515), complete; its opening (facing up-right, where the flame comes "
                  "out) painted as " + HOLE + "."),
    "co_tay_xa": ("G", (1005, 715), "P_shouL3",
                  "THE FAR WRIST: the dark charcoal block that joins the far hand to the body, below the jaw (about x = 900 to "
                  "x = 1110, y = 600 to y = 830), complete (its top hidden behind the jaw and the core, its bottom behind the far "
                  "hand)."),
    "lua_co_tay": ("G", (372, 535), None,
                   "THE NEAR WRIST FLAME: the flame with two tongues on top of the near wrist block (about x = 305 to x = 440, "
                   "y = 455 to y = 615). " + FLAME_ROOT.format(r="reaching about y = 618")),
    "vuot_xa3": ("G", (1185, 895), "P_shouzhiL5",
                 "THE BOTTOM-RIGHT CLAW of the far hand (about x = 1135 to x = 1235, y = 830 to y = 960), complete."),
    # ---- tờ H
    "hong_lua": ("H", (1000, 545), "P_kouqiang3",
                 "THE THROAT: the glowing fire inside the mouth (in image 1 only a small orange sliver shows between the face and "
                 "the jaw, about x = 935 to x = 990, y = 500 to y = 550). Draw it as ONE rounded cavity shape about x = 920 to "
                 "x = 1080, y = 470 to y = 620: a flat orange (#F7902A) area with a yellow (#FFD45A) centre and a red-orange "
                 "(#E0441F) rim, ink outline; it is seen when the jaw opens."),
    "chan_gan_dui": ("H", (597, 828), "P_tuiiR1",
                     "THE NEAR THIGH: the short stone thigh block above the near knee (about x = 545 to x = 650, y = 770 to "
                     "y = 885), complete as a rounded block."),
}
TO = sorted({v[0] for v in P.values()})
LUA = ["lua_vai", "lua_dinh", "lua_tran", "lua_dinh_nho", "lua_sau_dau", "lua_co_tay", "lua_hong"]

MANH_CHUNG = ("TASK: redraw image 1, but keep ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the "
              "SAME SIZE as in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). "
              "REMOVE everything else and leave pure white (#FFFFFF) there. Every kept part must be ONE COMPLETE CLOSED SHAPE with "
              "the dark-brown ink outline running all the way around it: where a part is hidden behind another part in image 1, "
              "DRAW the hidden portion as described. The kept parts must NOT touch each other: clear white between them. Same "
              "wobbly ink line, same colours, same crayon hatching, same completely flat colouring as image 1. Do not add "
              "anything: no shadows, no glow, no sparks, no embers, no labels.")
FLAT = ("FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, crayon strokes only as texture; no shading, no cast shadow, "
        "no highlight, no glow around the flames, no gradient.")
BG = "Plain pure-white background (#FFFFFF), no paper colour, no border, no text."
MO_TA_EN = ("a fire-core stone golem facing right: warm pale ash-grey stone blocks (big back slab, round near shoulder, top plate, "
            "brow plate over a small skull-like face with one yellow eye, a blade-shaped cheek plate, chest stones around a round "
            "fire core, hip blocks), dark charcoal rings, collars, wrist blocks and jaw, flames bursting out of holes (big ones from "
            "the near shoulder, the top of the back and the forehead; small ones on the top plate, the back of the head, the near "
            "wrist and the hips), two huge stone hands with three dark claws each, two short legs with glowing orange knees.")
MO_TA_VI = ("golem lõi lửa đá xám tro (hướng A đã duyệt): lưng, vai gần có vòng lỗ, tấm đỉnh, tấm mày trên mặt đầu lâu một mắt vàng, tấm "
            "má, đá ngực ôm lõi lửa, hông; vòng / cổ lỗ / cổ tay / hàm than chì; 7 lưỡi lửa; hai bàn tay ba vuốt; hai chân gối cam")


def build():
    if not os.path.exists(DUYET):
        raise SystemExit("chưa có concept duyệt " + DUYET)
    os.makedirs(PK, exist_ok=True)
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-13, người dùng chọn A = `L1_da_tro.png` → `L1_duyet.png`)", "",
          "Mọi mảnh của rig là mảnh cứng. Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất, "
          "bỏ hết thứ khác (nền trắng). Lưỡi lửa vẽ đủ gốc (để rig uốn lượn). Ảnh mẫu duy nhất của mọi file:", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{os.path.normpath(DUYET)}` | Concept đã duyệt (1536 × 1024, nền trắng): {MO_TA_VI} |", ""]
    for ma in TO:
        ten = [k for k, v in P.items() if v[0] == ma]
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(PK, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {os.path.normpath(DUYET)}: the APPROVED picture of the creature, 1536x1024, white background: " + MO_TA_EN,
             "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "", MANH_CHUNG, "", "KEEP:"]
        t += [f"{i}. {P[k][3]}" for i, k in enumerate(ten, 1)]
        t += ["", f"Exactly {len(ten)} separate parts on the canvas, nothing else.", "", FLAT, BG]
        ML_ghi(p, t)
        gd += [f"- **`{ma}`** ({', '.join(ten)}): chỉ gửi GPT `{os.path.normpath(p)}`; ảnh lưu vào `{os.path.normpath(out)}`."]
    gd += ["", "Kiểm từng ảnh: đúng các mảnh đã kê, trùng chỗ concept, viền mực kín, không chạm nhau, phần khuất vẽ đủ, nền trắng, "
           "không bóng. Claude cắt bằng `golem_lua_manh.py lam`."]
    hd = os.path.join(PK, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    ML_ghi(hd, [cu] + gd)
    print(len(TO), "tờ,", len(P), "mảnh")


# tờ N (gen sau, 2026-11-13): bốn lửa nhỏ vẽ lại cho GỐC khít miệng lỗ trên tấm (lửa bản đầu rộng 95–136 px, miệng lỗ chỉ 42–78 px:
# lửa đè lên cổ lỗ, tách vành ra lộ mép cắt). (tên, tâm miệng lỗ, rộng miệng, đỉnh lửa y, rộng thân lửa tối đa, mô tả)
LUA_NHO = [("lua_dinh_nho", (887, 199), 46, 82, 95, "the small flame on the top plate"),
           ("lua_sau_dau", (1026, 312), 40, 170, 110, "the small flame on the back of the head"),
           ("lua_co_tay", (389, 590), 40, 455, 115, "the flame with two tongues on the near wrist block"),
           ("lua_hong", (690, 746), 66, 630, 95, "the small flame between the legs")]


def build_lua_nho():
    out = os.path.join(G.TAI, "M_N.png")
    p = os.path.join(PK, "luot_2_manh_N.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {os.path.normpath(DUYET)}: the APPROVED picture of the creature, 1536x1024, white background: " + MO_TA_EN,
         "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
         "If a file with that name already exists, save as M_N_2.png, M_N_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: on a pure-white 1536x1024 canvas draw ONLY the four small flames listed below, each at the given place, in exactly the "
         "same hand-drawn style, colours and flame shape as the flames of image 1 (dark-brown wobbly ink outline about 5 px, three "
         "nested flat colour zones: red-orange #E0441F outside, orange #F7902A, yellow #FFD45A inside near the base, crayon hatching, "
         "tips curling up and back to the viewer's left). Each flame comes OUT OF A SMALL ROUND HOLE: its ROOT at the bottom must be "
         "NARROW, exactly as wide as the hole, with a rounded bottom end, and the flame WIDENS gradually above the hole into its tongue "
         "shape. Each flame is ONE closed shape with its ink outline all the way around (also around the root). Nothing else: no "
         "stone, no hole, no ring, no body, no sparks, no glow, no separate floating flame bits. The four flames must not touch.", ""]
    for i, (ten, (cx, cy), w, top, ww, mo) in enumerate(LUA_NHO, 1):
        t.append(f"{i}. {mo.upper()}: root bottom centred at x = {cx}, y = {cy + 6}, root {w} px wide at the hole (from x = {cx - w // 2} "
                 f"to x = {cx + w // 2}); the flame rises straight up from there and widens to at most {ww} px, its highest tip at "
                 f"about y = {top}.")
    t += ["", "Exactly 4 separate flames on the canvas, nothing else.", "", FLAT, BG]
    ML_ghi(p, t)
    print(p)


def ML_ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- cắt
MAT_TAT = [((255, 212, 90), (120, 112, 108)), ((60, 40, 40), (52, 46, 50))]
LOI_TAT = [((224, 68, 31), (66, 56, 62)), ((247, 144, 42), (84, 66, 70)), ((255, 212, 90), (104, 76, 74))]


def cat_to(ma):
    import cv2
    p = os.path.join(G.TAI, f"M_{ma}.png")
    A = ML.doc(p)
    if A.shape[:2] != (1024, 1536):
        raise SystemExit(f"tờ {ma}: cỡ {A.shape[1]}x{A.shape[0]}, phải 1536x1024")
    fg = ~ML.nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, ML.el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    ra, da = {}, set()
    for ten, v in P.items():
        if v[0] != ma:
            continue
        cx, cy = v[1]
        best, bi = 1e18, -1
        for i in range(1, n):
            if st[i, 4] < 250 or i in da:
                continue
            x, y, w, h, _ = st[i]
            dx = max(x - cx, 0, cx - (x + w))
            dy = max(y - cy, 0, cy - (y + h))
            d = dx * dx + dy * dy + 0.02 * ((cen[i][0] - cx) ** 2 + (cen[i][1] - cy) ** 2)
            if d < best:
                best, bi = d, i
        if bi < 0:
            raise SystemExit(f"tờ {ma}: không thấy mảnh {ten}")
        da.add(bi)
        ra[ten] = (A, lab == bi)
    thua = [tuple(int(x) for x in st[i, :5]) for i in range(1, n) if i not in da and st[i, 4] >= 300]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA: {thua}" if thua else ""))
    return ra


DOI = {"vong_tran": (16, -36), "lua_co_tay": (35, 4)}  # vòng trán vẽ trùng chỗ con mắt; concept: vòng chếch trên-phải, mép dưới viền trên mắt như mày
LOI_TO = 1.28
NGUOI = ["lung", "dinh", "dau", "vai", "co_tay_gan", "hong", "chan_gan_goi", "chan_xa_goi", "vong_tran"]
LUA_NGUOI = [((224, 68, 31), (70, 60, 66)), ((247, 144, 42), (86, 72, 74)), ((255, 212, 90), (104, 90, 88))]                 # lõi Codex vẽ nhỏ hơn khe vỏ ngực: phóng cho lấp kín
# thứ tự vẽ sau → trước. Mỗi lỗ lửa hai lớp (người dùng 2026-11-13: "những lỗ lửa bạn tách 2 layer 1 trên 1 dưới thì lửa mới ở giữa lỗ
# được chứ"): nửa vành SAU (phía lửa bay ra) → lửa → nửa vành TRƯỚC. Vòng lớn: <vòng>_sau / <vòng>_truoc; cổ lỗ vẽ liền tấm: tấm (giữ
# nửa sau + lòng lỗ) → lửa → <tấm>_vanh (nửa trước cổ lỗ).
THU_TU = ["chan_xa_dui", "chan_xa_ban", "chan_xa_goi", "hong", "chan_gan_dui", "chan_gan_ban", "chan_gan_goi",
          "co_tay_xa", "tay_xa", "vuot_xa2", "vuot_xa3", "vuot_xa1",
          "loi_tat", "loi", "vo_nguc", "nguc_trai", "lua_hong", "hong_vanh", "hong_lua", "ham", "lung", "vong_dinh_sau", "lua_dinh", "vong_dinh_truoc",
          "dinh", "lua_dinh_nho", "dinh_vanh",
          "ma", "dau", "mat_tat", "mat", "lua_sau_dau", "dau_vanh", "vong_tran_sau", "lua_tran", "vong_tran_truoc",
          "vai", "vong_vai_sau", "lua_vai", "vong_vai_truoc",
          "co_tay_gan", "lua_co_tay", "co_tay_gan_vanh", "tay_gan", "vuot_gan1", "vuot_gan2", "vuot_gan3"]
# lửa → (mảnh lỗ, kiểu): "vong" = vòng riêng cắt đôi; "co" = cổ lỗ vẽ liền tấm (tách nửa trước thành <tấm>_vanh)
VANH = {"lua_vai": ("vong_vai", "vong"), "lua_dinh": ("vong_dinh", "vong"), "lua_tran": ("vong_tran", "vong"),
        "lua_dinh_nho": ("dinh", "co"), "lua_sau_dau": ("dau", "co"), "lua_co_tay": ("co_tay_gan", "co"), "lua_hong": ("hong", "co")}
# chỗ lửa chui vào lỗ trên khung concept (như golem_lua_rig.LUA)
LUA_GOC = {"lua_vai": (522, 405), "lua_dinh": (695, 272), "lua_tran": (1045, 492), "lua_dinh_nho": (898, 214),
           "lua_sau_dau": (1047, 330), "lua_co_tay": (413, 610), "lua_hong": (680, 800)}


def tach_vanh(anh_, dat, luu):
    """tách mỗi lỗ lửa thành nửa vành sau / trước theo hướng lửa (gốc → ngọn), cắt phần gốc lửa thò ra trước mép vành."""
    import cv2
    H, W = 1024, 1536

    def tren_khung(t, cot=3):
        a = np.asarray(anh_[t])[..., cot] if cot == 3 else np.asarray(anh_[t])
        gx, gy = dat[t]["goc"]
        M = np.zeros((H, W) + a.shape[2:], a.dtype)
        h, w = a.shape[:2]
        x0, y0 = max(0, gx), max(0, gy)
        x1, y1 = min(W, gx + w), min(H, gy + h)
        M[y0:y1, x0:x1] = a[y0 - gy:y1 - gy, x0 - gx:x1 - gx]
        return M

    def ve_lai(t, giu, ten_moi):
        """ảnh mới cùng cỡ, cùng chỗ với t, chỉ giữ các điểm có giu (mặt nạ khung concept)."""
        arr = np.asarray(anh_[t]).copy()
        gx, gy = dat[t]["goc"]
        h, w = arr.shape[:2]
        sub = np.zeros((h, w), bool)
        x0, y0 = max(0, gx), max(0, gy)
        x1, y1 = min(W, gx + w), min(H, gy + h)
        sub[y0 - gy:y1 - gy, x0 - gx:x1 - gx] = giu[y0:y1, x0:x1]
        arr[..., 3] = np.where(sub, arr[..., 3], 0)
        anh_[t if ten_moi is None else ten_moi] = Image.fromarray(arr, "RGBA")
        if ten_moi is not None:
            dat[ten_moi] = dict(goc=list(dat[t]["goc"]), co=list(dat[t]["co"]), slot=None)
        (anh_[t if ten_moi is None else ten_moi]).save(os.path.join(MANH, (t if ten_moi is None else ten_moi) + ".png"))

    yy, xx = np.mgrid[0:H, 0:W]
    for lua, (lo, kieu) in VANH.items():
        if lua not in anh_ or lo not in anh_:
            continue
        F = tren_khung(lua) > 0
        fy, fx = np.nonzero(F)
        gp = np.array(LUA_GOC[lua], float)
        k = np.argmin(np.hypot(fx - gp[0], fy - gp[1]))
        b = np.array([fx[k], fy[k]], float)
        k2 = np.argmax(np.hypot(fx - b[0], fy - b[1]))
        d = np.array([fx[k2], fy[k2]], float) - b
        d /= np.hypot(*d)
        if kieu == "vong":
            R = tren_khung(lo) > 0
            day = cv2.morphologyEx(R.astype(np.uint8), cv2.MORPH_CLOSE, ML.el(25))
            n_, lab_ = cv2.connectedComponents((1 - day).astype(np.uint8), connectivity=4)
            for i in range(1, n_):            # lấp lòng vòng (vùng không chạm mép khung)
                r = lab_ == i
                if not (r[0].any() or r[-1].any() or r[:, 0].any() or r[:, -1].any()):
                    day |= r.astype(np.uint8)
            day = day.astype(bool)
            cy_, cx_ = np.nonzero(day)
            c = np.array([cx_.mean(), cy_.mean()])
            truoc = ((xx - c[0]) * d[0] + (yy - c[1]) * d[1]) < 0
            cho = ((xx - c[0]) * d[0] + (yy - c[1]) * d[1]) < 4      # nửa trước chờm qua đường cắt 4 px: khỏi khe hở khi thu nhỏ / vẽ lưới
            ve_lai(lo, R & ~truoc, lo + "_sau")
            ve_lai(lo, R & cho, lo + "_truoc")
            del anh_[lo]
        else:
            S = tren_khung(lo, cot=None).astype(np.int32)
            al = S[..., 3] > 0
            lua_m = al & (S[..., 0] > 185) & (S[..., 0] - S[..., 2] > 90)
            n_, lab_ = cv2.connectedComponents(lua_m.astype(np.uint8), connectivity=8)
            best, hi = 1e18, 0
            for i in range(1, n_):
                ys_, xs_ = np.nonzero(lab_ == i)
                dd = np.hypot(xs_ - b[0], ys_ - b[1]).min()
                if dd < best:
                    best, hi = dd, i
            if hi == 0 or best > 70:
                print(f"  {lua}: không thấy lòng lỗ trên {lo} (gần nhất {best:.0f} px)")
                continue
            Hm = cv2.dilate((lab_ == hi).astype(np.uint8), ML.el(10)).astype(bool) & lua_m
            Hm = cv2.morphologyEx(Hm.astype(np.uint8), cv2.MORPH_CLOSE, ML.el(6)).astype(bool)
            n2, l2 = cv2.connectedComponents((~Hm).astype(np.uint8), connectivity=4)
            for i in range(1, n2):            # lấp lỗ kín trong lòng lỗ (nét mực vòng trong)
                r = l2 == i
                if r.sum() < 4000 and not (r[0].any() or r[-1].any() or r[:, 0].any() or r[:, -1].any()):
                    Hm |= r
            toi = al & (S[..., :3].max(2) < 125)
            vung = cv2.dilate(Hm.astype(np.uint8), ML.el(22)).astype(bool)
            K = toi & vung & ~Hm
            hy, hx = np.nonzero(Hm)
            c = np.array([hx.mean(), hy.mean()])
            # lửa và tấm gen ở hai tờ khác nhau nên gốc lửa có thể lệch lòng lỗ: dời cả lưỡi lửa cho gốc trùng tâm lòng lỗ
            dl = np.round(c - b).astype(int)
            if np.hypot(*dl) > 3:
                dat[lua]["goc"] = [int(dat[lua]["goc"][0] + dl[0]), int(dat[lua]["goc"][1] + dl[1])]
                F = tren_khung(lua) > 0
                b = b + dl
                print(f"  {lua}: dời ({dl[0]:+d}, {dl[1]:+d}) cho gốc lửa vào giữa lòng lỗ trên {lo}")
            truoc = ((xx - c[0]) * d[0] + (yy - c[1]) * d[1]) < 0
            cho = ((xx - c[0]) * d[0] + (yy - c[1]) * d[1]) < 4
            Kt = cv2.morphologyEx((K & cho).astype(np.uint8), cv2.MORPH_OPEN, ML.el(1)).astype(bool)
            ve_lai(lo, Kt, lo + "_vanh")
            day = cv2.dilate((Hm | K).astype(np.uint8), ML.el(2)).astype(bool)
            # lòng lỗ trên tấm tô một màu cam lửa (khỏi lộ vạch vàng / nét viền lòng lỗ ở chỗ gốc lửa không phủ kín)
            arr = np.asarray(anh_[lo]).copy()
            gx, gy = dat[lo]["goc"]
            hm = cv2.dilate(Hm.astype(np.uint8), ML.el(2)).astype(bool) & ~cv2.erode(K.astype(np.uint8), ML.el(1)).astype(bool)
            ys_, xs_ = np.nonzero(hm)
            ok = (ys_ - gy >= 0) & (ys_ - gy < arr.shape[0]) & (xs_ - gx >= 0) & (xs_ - gx < arr.shape[1])
            arr[ys_[ok] - gy, xs_[ok] - gx, :3] = (247, 144, 42)
            anh_[lo] = Image.fromarray(arr, "RGBA")
            anh_[lo].save(os.path.join(MANH, lo + ".png"))
        dat[lua]["goc_lua"] = [int(round(b[0])), int(round(b[1]))]
        # nét mực khép đáy lưỡi lửa nằm trong miệng lỗ: tô màu lõi lửa cho lửa liền vào lòng lỗ đang cháy (khỏi vệt ngang trong miệng lỗ)
        long_lo = day & ~((R if kieu == "vong" else K))
        long_lo = cv2.erode(long_lo.astype(np.uint8), ML.el(2)).astype(bool)
        arrF = np.asarray(anh_[lua]).copy()
        fgx, fgy = dat[lua]["goc"]
        ys_, xs_ = np.nonzero(long_lo)
        ly, lx = ys_ - fgy, xs_ - fgx
        ok = (ly >= 0) & (ly < arrF.shape[0]) & (lx >= 0) & (lx < arrF.shape[1])
        ly, lx = ly[ok], lx[ok]
        muc = (arrF[ly, lx, 3] > 0) & (arrF[ly, lx, :3].max(1) < 110)
        arrF[ly[muc], lx[muc], :3] = (255, 212, 90)
        anh_[lua] = Image.fromarray(arrF, "RGBA")
        anh_[lua].save(os.path.join(MANH, lua + ".png"))
        # lửa đè lên đai vành SAU sát đường chia: bỏ (để lửa nằm gọn trong lòng lỗ, đai vành sau lộ ra liền với nửa trước)
        dai_ = (R if kieu == "vong" else np.zeros_like(F)) & ~truoc
        V0 = (xx - c[0]) * d[0] + (yy - c[1]) * d[1]
        dvy, dvx = np.nonzero(day)
        tam_day = float(np.ptp(V0[dvy, dvx])) * 0.22
        de = F & dai_ & (V0 < tam_day)
        if de.any():
            F = F & ~de
            ve_lai(lua, F, None)
        # gốc lửa thò ra TRƯỚC mép trước của vành (trong bề ngang của vành): bỏ; ngoài bề ngang vành giữ nguyên (khỏi mép cắt thẳng)
        pe = np.array([-d[1], d[0]])
        U = (xx - c[0]) * pe[0] + (yy - c[1]) * pe[1]
        V = (xx - c[0]) * d[0] + (yy - c[1]) * d[1]
        dy_, dx_ = np.nonzero(day)
        ub = np.round(U[dy_, dx_] / 2).astype(int)
        vmin = {}
        for u_, v_ in zip(ub, V[dy_, dx_]):
            if v_ < vmin.get(u_, 1e9):
                vmin[u_] = v_
        fy2, fx2 = np.nonzero(F & ~day & truoc)
        thua = np.zeros_like(F)
        for y_, x_ in zip(fy2, fx2):
            u_ = int(round(U[y_, x_] / 2))
            if u_ in vmin and V[y_, x_] < vmin[u_]:
                thua[y_, x_] = True
        if thua.any():
            ve_lai(lua, F & ~thua, None)
        print(f"  {lua}: vành {kieu} tách theo hướng ({d[0]:+.2f}, {d[1]:+.2f}); bỏ {int(thua.sum())} điểm gốc lửa thò ra trước")


def lam():
    import cv2
    os.makedirs(MANH, exist_ok=True)
    C = ML.doc(DUYET)
    Pm = {}
    for ma in TO:
        if not os.path.exists(os.path.join(G.TAI, f"M_{ma}.png")):
            print(f"  chưa có tờ {ma}")
            continue
        Pm.update(cat_to(ma))
    pN = os.path.join(G.TAI, "M_N.png")
    if os.path.exists(pN):                    # bốn lửa nhỏ gốc khít miệng lỗ (tờ N) thay bản đầu
        AN = ML.doc(pN)
        fgN = ~ML.nen(AN)
        nN, labN, stN, _ = cv2.connectedComponentsWithStats(fgN.astype(np.uint8), 8)
        for ten, (cx, cy), w, top, ww, _ in LUA_NHO:
            best, bi = 1e18, -1
            for i in range(1, nN):
                if stN[i, 4] < 250:
                    continue
                x, y, wd, hh = stN[i, :4]
                dd = (x + wd / 2 - cx) ** 2 + (y + hh - cy) ** 2
                if dd < best:
                    best, bi = dd, i
            if bi > 0:
                Pm[ten] = (AN, labN == bi)
        print("  tờ N: thay", len(LUA_NHO), "lửa nhỏ")
    dat, anh_ = {}, {}

    def luu(ten, im, goc):
        if ten in DOI:                        # Codex đặt lệch concept: dời cả mảnh
            goc = (goc[0] + DOI[ten][0], goc[1] + DOI[ten][1])
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = im
        base = ten.replace("_tat", "").replace("_nguoi", "")
        dat[ten] = dict(goc=[int(goc[0]), int(goc[1])], co=[im.width, im.height], slot=P[base][2] if not ten.endswith("_tat") else None)

    import cv2
    for ten, (A, m) in Pm.items():
        if ten.startswith("vong"):            # lòng vòng: vùng trắng kín trong mảnh → trong suốt
            trang = (A.min(2) > 225) & m
            n_, lab_ = cv2.connectedComponents(trang.astype(np.uint8), connectivity=4)
            for i in range(1, n_):
                if (lab_ == i).sum() > 150:
                    m = m & ~cv2.dilate((lab_ == i).astype(np.uint8), ML.el(1)).astype(bool)
        if ten == "loi":                      # lõi lấp kín khe vỏ ngực: phóng quanh tâm
            ys, xs = np.nonzero(m)
            cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
            M = cv2.getRotationMatrix2D((cx, cy), 0, LOI_TO)
            A = cv2.warpAffine(A.astype(np.uint8), M, (A.shape[1], A.shape[0]), flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255)).astype(np.int32)
            m = cv2.warpAffine(m.astype(np.uint8), M, (m.shape[1], m.shape[0]), flags=cv2.INTER_NEAREST).astype(bool)
        Pm[ten] = (A, m)
    if "lua_tran" in Pm and "mat" in Pm:          # gốc lửa trán Codex vẽ tràn quanh mắt: bỏ phần quanh mắt (vòng trán che chỗ nối)
        A, m = Pm["lua_tran"]
        ys, xs = np.nonzero(Pm["mat"][1])
        ex, ey, er = xs.mean(), ys.mean(), (xs.max() - xs.min()) / 2
        yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        bo = (np.hypot(xx - ex, yy - ey) < er + 12) | ((yy > ey) & (xx < ex + er + 20))
        if "vong_tran" in Pm:                     # và phần nằm sau nửa trái vòng trán (sau khi dời vòng)
            vy, vx = np.nonzero(Pm["vong_tran"][1])
            dx_, dy_ = DOI.get("vong_tran", (0, 0))
            x0v, y0v, x1v = vx.min() + dx_, vy.min() + dy_, vx.max() + dx_
            bo |= (xx < (x0v + x1v) / 2) & (yy > y0v + 14)
        Pm["lua_tran"] = (A, m & ~bo)
    if "hong_lua" in Pm and "dau" in Pm and "ham" in Pm:   # họng chỉ nằm trong hình mặt + hàm lúc nghỉ (lộ ra khi hàm hạ)
        A, m = Pm["hong_lua"]
        Pm["hong_lua"] = (A, m & cv2.erode((Pm["dau"][1] | Pm["ham"][1]).astype(np.uint8), ML.el(4)).astype(bool))
    for ten, (A, m) in Pm.items():
        im, goc = ML.manh_rgba(A, m)
        if ten.startswith("vong"):            # manh_rgba lấp lỗ kín nhỏ: đục lại lòng vòng (trắng kín > 150 px) cho trong suốt
            arr = np.asarray(im).copy()
            tr = (arr[..., :3].min(2) > 222) & (arr[..., 3] > 0)
            n_, lab_ = cv2.connectedComponents(tr.astype(np.uint8), connectivity=4)
            for i in range(1, n_):
                r = lab_ == i
                if r.sum() > 150:
                    r = cv2.dilate(r.astype(np.uint8), ML.el(1)).astype(bool)
                    arr[r, 3] = 0
            im = Image.fromarray(arr, "RGBA")
        luu(ten, im, goc)
        if ten == "mat":
            luu("mat_tat", ML.doi_mau(im, MAT_TAT), goc)
        if ten == "loi":
            luu("loi_tat", ML.doi_mau(im, LOI_TAT), goc)
    # mảnh NGUỘI: vùng màu lửa (lòng lỗ, gối) của tấm đá đổi sang than tro, cắt sát; rig đặt ngay trên tấm, ẩn mặc định (die / appear)
    for ten in NGUOI:
        if ten not in anh_:
            continue
        arr = np.asarray(anh_[ten]).astype(np.int32)
        r_, g_, b_, a_ = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
        lua_ = (a_ > 0) & (r_ > 185) & (r_ - b_ > 90)
        if lua_.sum() < 30:
            continue
        mm = cv2.dilate(lua_.astype(np.uint8), ML.el(3)).astype(bool) & (a_ > 0)
        ys, xs = np.nonzero(mm)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        sub = Image.fromarray(arr[y0:y1, x0:x1].astype(np.uint8), "RGBA")
        sub = ML.doi_mau(sub, LUA_NGUOI)
        o = np.asarray(sub).copy()
        o[..., 3] = np.where(mm[y0:y1, x0:x1], o[..., 3], 0)
        g0 = dat[ten]["goc"]
        luu(ten + "_nguoi", Image.fromarray(o, "RGBA"), (g0[0] + x0 - DOI.get(ten, (0, 0))[0], g0[1] + y0 - DOI.get(ten, (0, 0))[1]))
        dat[ten + "_nguoi"]["slot"] = None
    tach_vanh(anh_, dat, luu)
    thu_tu = []
    for t in THU_TU:
        if t in anh_:
            thu_tu.append(t)
            ng = (t[:-4] if t.endswith("_sau") else t) + "_nguoi"
            if ng in anh_ and ng not in thu_tu:
                thu_tu.append(ng)
    dat["_thu_tu"] = thu_tu
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in thu_tu:
        if not t.endswith("_tat") and not t.endswith("_nguoi"):
            ghep.alpha_composite(anh_[t], tuple(dat[t]["goc"]))
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - C).max(2)
    print(f"  ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ")
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    x = y = 12
    hh = 0
    cho = []
    for t in thu_tu:
        im = anh_[t]
        if x + im.width + 12 > 2200:
            x, y, hh = 12, y + hh + 34, 0
        cho.append((t, x, y))
        x += max(im.width, 90) + 16
        hh = max(hh, im.height)
    to = Image.new("RGB", (2200, y + hh + 40), (150, 150, 150))
    dr = ImageDraw.Draw(to)
    for t, x, y in cho:
        to.paste(anh_[t], (x, y + 20), anh_[t])
        dr.text((x, y), t, fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(thu_tu), "mảnh")


def tam():
    """mảnh TẠM cắt thô từ concept theo khung ghi trong mô tả (chỉ để thử rig / clip trong lúc chờ Codex) → inbox/golem_lua_1/manh_tam/"""
    import re
    import cv2
    ra = os.path.join(G.BASE, "manh_tam")
    os.makedirs(ra, exist_ok=True)
    C = ML.doc(DUYET)
    trang = C.min(2) > 236
    lua_m = (C[..., 0] > 190) & (C[..., 2] < 140) & (C[..., 0] - C[..., 2] > 80)
    toi = C.max(2) < 95
    dat = {}
    for ten, (_, (cx, cy), slot, mo) in P.items():
        m_ = re.search(r"about x = (\d+) to x = (\d+), y = (\d+) to y = (\d+)", mo)
        x0, x1, y0, y1 = map(int, m_.groups())
        m = np.zeros(trang.shape, bool)
        if ten.startswith("lua_"):
            m[y0:y1, x0:x1] = lua_m[y0:y1, x0:x1]
            m = cv2.dilate(m.astype(np.uint8), ML.el(3)).astype(bool) & ~trang
        elif ten.startswith("vong") or ten in ("ham", "co_tay_gan", "co_tay_xa") or ten.startswith("vuot"):
            m[y0:y1, x0:x1] = (toi | ~lua_m)[y0:y1, x0:x1] & ~trang[y0:y1, x0:x1]
        else:
            m[y0:y1, x0:x1] = ~trang[y0:y1, x0:x1]
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        if n > 1:
            k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            m = lab == k
        im, goc = ML.manh_rgba(C, m)
        im.save(os.path.join(ra, ten + ".png"))
        dat[ten] = dict(goc=[int(goc[0]), int(goc[1])], co=[im.width, im.height], slot=slot)
        if ten in ("mat", "loi"):
            t2 = ten + "_tat"
            im2 = ML.doi_mau(im, MAT_TAT if ten == "mat" else LOI_TAT)
            im2.save(os.path.join(ra, t2 + ".png"))
            dat[t2] = dict(goc=dat[ten]["goc"], co=dat[ten]["co"], slot=None)
    dat["_thu_tu"] = [t for t in THU_TU if t in dat]
    json.dump(dat, open(os.path.join(ra, "dat.json"), "w", encoding="utf-8"), indent=1)
    print(ra, len(dat) - 1, "mảnh tạm")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "build":
        build()
    elif c == "lam":
        lam()
    elif c == "tam":
        tam()
    elif c == "lua_nho":
        build_lua_nho()
    else:
        print(__doc__)
