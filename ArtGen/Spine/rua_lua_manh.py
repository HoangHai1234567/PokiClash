# -*- coding: utf-8 -*-
"""Rùa golem lửa (rua_lua): mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt (người dùng chọn A, sửa hai sừng lành lặn + nối chân trước xa:
L1c_bazan.png → L1_duyet.png, 2026-11-13).

Mỗi tờ Codex vẽ lại concept nhưng chỉ giữ vài mảnh KHÔNG chồng nhau, vẽ đủ phần khuất. Mảnh đá của con gốc monster_3425 có cái cứng một
xương (cột đá, sừng, mặt, hàm, đùi), có cái là lưới trọng số (mai, bụng, đuôi, bốn ống chân): rig lo phần bám (rua_lua_rig.py). Bảy ngọn
lửa trên lưng là mảnh riêng, vẽ đủ GỐC (sẽ thành lưới có chuỗi xương, đung đưa nhẹ; chiêu cuối co lại từng ngọn). Mảnh KHUẤT hẳn trên
concept (ba đùi, lòng miệng) vẽ ở góc trống của tờ; rig đặt theo khung part của con gốc.

    rua_lua_manh.py build     → gui_gpt/rua_lua_1/luot_2_manh_<A..F>.txt (+ HUONG_DAN.md mục lượt 2)
    rua_lua_manh.py lam       → inbox/rua_lua_1/manh/<tên>.png + dat.json + _so_ghep.png + _to.png
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rua_lua as G  # noqa: E402
import mat_lua_manh as ML  # noqa: E402  (hàm chung: doc, nen, manh_rgba, doi_mau, el)

MANH = os.path.join(G.BASE, "manh")
DUYET = os.path.join(G.TAI, "L1_duyet.png")
PK = os.path.join(HERE, "gui_gpt", "rua_lua_1")

FLAME_ROOT = ("Complete its ROOT: in image 1 its bottom is hidden behind {sau}; continue the flame downward as a thick rounded flame "
              "base {r}, closed with the ink outline (the base is the same orange / yellow as the flame). Do NOT draw any small "
              "separate floating flame bits next to it.")
BOULDER = ("a simple rounded slate blue-grey stone boulder (the same colour, ink outline and crayon hatching as the leg blocks of "
           "image 1), with one short seam line")

# mảnh: (tờ, tâm ước chừng trên tờ để cắt, slot gốc, kiểu đặt, mô tả tiếng Anh)
#   kiểu: "c" = trùng chỗ concept (dùng làm mốc khớp khung concept ↔ rig nếu có slot); "k" = trùng chỗ concept nhưng KHÔNG làm mốc (hình
#   đổi dáng / gộp part); "r" = mảnh khuất vẽ ở chỗ trống, rig đặt theo khung part của con gốc
P = {
    # ---- tờ A
    # mai gen lại riêng ở tờ G (người dùng 2026-11-13: "phần mai bạn lại tính 1 phần chân là mai rùa nên nó khuyết mất 1 mảnh"): tờ A vẽ
    # mép dưới của mai lõm thành vòm ở chỗ chân trước gần đè lên + một cái móc thừa bên trái; lúc appear chỉ còn cái mai thì lộ chỗ khuyết
    "mai": ("G", (690, 570), "p_ke", "c",
            "THE SHELL: the big domed slate blue-grey stone shell with its seam lines (in image 1 its visible part is about x = 360 to "
            "x = 860, y = 385 to y = 785). Draw the WHOLE shell as ONE closed, SOLID dome-shaped piece, like half of a big boulder, "
            "with NOTHING missing. TOP EDGE: one smooth dome line that continues under the stone columns and under the flames "
            "(highest point about y = 385 near x = 770). RIGHT END: hidden behind the big horn and the face; continue it as a rounded "
            "end reaching about x = 1010 between y = 540 and y = 700. LEFT END: a simple rounded end at about x = 360, y = 630 (no "
            "hook, no curl, no lip). LOWER EDGE (very important): ONE continuous line that bulges gently DOWNWARD all the way, from "
            "the left end at about (360, 640) through about (520, 730) and (660, 775) to the pointed front flap whose tip is at about "
            "(790, 780), then up to the right end. In image 1 the near front leg and its thigh stand IN FRONT of the shell and cover "
            "part of this lower edge: the shell continues BEHIND them. Do NOT cut an arch, a notch, a bite or any opening for a leg "
            "out of the shell; there is no concave part anywhere on its outline. Keep the same few seam lines as in image 1 and "
            "continue them over the newly drawn parts. Remove the columns, the flames, both horns, the head, every leg, the tail and "
            "the belly: only the shell on a white canvas."),
    "ham": ("A", (1020, 815), "p_xiaba", "c",
            "THE LOWER JAW: the ivory jaw block under the face mask (visible about x = 940 to x = 1100, y = 775 to y = 885). Its top "
            "is hidden behind the zigzag lower edge of the mask: complete it upward as one block with a flat top at about y = 735 "
            "and rounded corners, from about x = 925 to x = 1095. Only the jaw: not the mask, not the leg next to it."),
    "dui_sau_xa": ("A", (160, 170), "p_datui05", "r",
                   "A HIDDEN THIGH BLOCK (not visible in image 1; draw it in the empty TOP-LEFT corner, centred at about x = 160, "
                   "y = 170): " + BOULDER + ", egg-shaped, about 150 px wide and 170 px tall, slightly leaning."),
    "dui_truoc_xa": ("A", (1370, 170), "p_datui02", "r",
                     "ANOTHER HIDDEN THIGH BLOCK (not visible in image 1; draw it in the empty TOP-RIGHT corner, centred at about "
                     "x = 1370, y = 170): " + BOULDER + ", oval, about 140 px wide and 180 px tall."),
    "hong": ("A", (170, 880), None, "r",
             "THE INSIDE OF THE MOUTH (not visible in image 1; it is seen when the jaw opens; draw it in the empty BOTTOM-LEFT corner, "
             "centred at about x = 170, y = 880): ONE rounded bean-shaped cavity about 170 px wide and 130 px tall, a flat orange "
             "(#F7902A) area with a yellow (#FFD45A) centre and a red-orange (#E0441F) rim, dark-brown ink outline, same crayon "
             "hatching; no teeth, no tongue."),
    # ---- tờ B
    "cot_gan": ("B", (610, 490), "p_kuangshi01", "c",
                "THE BIG COLUMN CLUSTER: the group of dark navy-charcoal hexagonal stone columns standing on the shell (about x = 450 "
                "to x = 770, y = 350 to y = 615), drawn as ONE piece (keep the ink lines between the columns). They are fully "
                "visible in image 1; close the bottom of the cluster with the ink outline where the columns stand on the shell. "
                "Remove the flames behind them and the shell."),
    "cot_xa": ("B", (985, 400), "p_kuangshi05", "c",
               "THE FAR COLUMN: the single dark stone column at the top right, behind the two small flames (visible about x = 940 to "
               "x = 1035, y = 320 to y = 440). Complete it downward, where the flames and the horn hide it, as a straight column "
               "with a flat bottom at about y = 490."),
    "sung_xa": ("B", (1150, 600), "p_jiao01_2", "k",
                "THE FAR HORN: the smaller ivory horn at the right, behind the face mask (visible about x = 1085 to x = 1222, "
                "y = 465 to y = 720), whole and pointed. Complete its BASE, hidden behind the mask: a thick rounded base that "
                "continues down-left to about x = 1040, y = 745."),
    "ong_truoc_gan": ("B", (630, 820), "p_xiaotui01", "c",
                      "THE NEAR FRONT LEG BLOCK: the big pillar leg in the foreground (about x = 515 to x = 745, y = 650 to y = 955) "
                      "with its seam lines and its three small orange crystals (two on its top left, one on its front). It is fully "
                      "visible in image 1: one complete piece, crystals included."),
    "duoi": ("B", (360, 780), "p_weiba", "c",
             "THE TAIL: the stone tail at the lower left with its small curved ivory spikes on its upper edge (visible about x = 240 to "
             "x = 345, y = 630 to y = 900). Most of it is hidden behind the near hind leg and under the shell: complete it as ONE "
             "thick tapering stone tail, its pointed tip at the left exactly as in image 1, its thick rounded root continuing to the "
             "right to about x = 500 (between about y = 690 and y = 850). Keep the spikes."),
    # ---- tờ C
    "sung_gan": ("C", (960, 520), "p_jiao01", "c",
                 "THE BIG NEAR HORN: the huge ivory horn (about x = 808 to x = 1135, y = 310 to y = 750): its thick angular base block "
                 "on the side of the head and the long curve sweeping up to the sharp tip. It is fully visible in image 1 (it lies in "
                 "front of the face mask): one complete piece with its outline all the way around."),
    "ong_sau_gan": ("C", (400, 840), "p_xiaotui04", "c",
                    "THE NEAR HIND LEG BLOCK: the pillar leg at the left (about x = 305 to x = 495, y = 725 to y = 945) with its seam "
                    "lines. It is fully visible in image 1: one complete piece."),
    "ong_truoc_xa": ("C", (1135, 830), "p_xiaotui02", "c",
                     "THE FAR FRONT LEG BLOCK: the pillar leg at the far right with its two small orange crystals (visible about "
                     "x = 1040 to x = 1245, y = 695 to y = 950). Its left side is hidden behind the jaw and the mask: complete it as "
                     "a pillar block like the other legs, its left edge at about x = 1005, with a rounded top at about y = 700. "
                     "Only this lower leg block: do NOT draw the part that rises behind the face."),
    # ---- tờ D
    "mat_so": ("D", (1010, 710), "p_lian", "c",
               "THE FACE MASK: the ivory skull-like stone mask (visible about x = 890 to x = 1130, y = 600 to y = 810) with its crack "
               "seam, its dark angular eye socket with the yellow eye and dark pupil, and its zigzag lower edge. Its upper-left part "
               "is hidden under the base of the big horn: complete it there as a smooth rounded forehead / cheek, reaching about "
               "x = 880 at y = 620 to y = 720. Remove both horns and the jaw."),
    "dui_truoc_gan": ("D", (620, 750), "p_datui01", "r",
                      "THE NEAR FRONT THIGH: the rounded slate block just behind the top of the near front leg, under the arch of the "
                      "shell (visible as an arch about x = 610 to x = 760, y = 615 to y = 765). Complete it as ONE rounded boulder "
                      "about x = 595 to x = 765, y = 610 to y = 795 (its lower part is hidden behind the leg block)."),
    "dui_sau_gan": ("D", (250, 280), "p_datui04", "r",
                    "A HIDDEN THIGH BLOCK (not visible in image 1; draw it in the empty UPPER-LEFT area, centred at about x = 250, "
                    "y = 280): " + BOULDER + ", egg-shaped, about 170 px wide and 190 px tall."),
    # ---- tờ E
    "bung": ("E", (760, 790), "p_xiongqiang", "k",
             "THE BELLY PLATE: the lighter blue-grey plate under the shell (visible between the legs, about x = 480 to x = 1020, "
             "y = 690 to y = 880). Complete it as ONE long flat stone plate from about x = 430 to x = 1060: its bottom edge exactly "
             "as in image 1 (about y = 870), its ends rounded, its top hidden under the shell, rounded, at about y = 650."),
    "lua_trai": ("E", (520, 370), None, "k",
                 "THE LEFT BIG FLAME (about x = 445 to x = 600, y = 258 to y = 450). " +
                 FLAME_ROOT.format(sau="the stone columns", r="about 70 px further down, to about x = 520 to x = 610, y = 520")),
    "lua_cao": ("E", (780, 250), None, "k",
                "THE TALLEST FLAME in the middle (about x = 678 to x = 880, y = 80 to y = 390). " +
                FLAME_ROOT.format(sau="the top edge of the shell", r="about 45 px further down, to about y = 435")),
    "lua_nho": ("E", (950, 455), None, "k",
                "THE SMALL FLAME just left of the big horn (about x = 900 to x = 1005, y = 372 to y = 520). " +
                FLAME_ROOT.format(sau="the big horn", r="about 40 px further down-right, to about y = 560")),
    # ---- tờ F
    "lua_duoi": ("F", (440, 480), None, "k",
                 "THE SMALL FLAME at the far left, above the tail (about x = 385 to x = 495, y = 385 to y = 545). " +
                 FLAME_ROOT.format(sau="the lowest stone column", r="about 45 px further down-right, to about x = 520, y = 585")),
    "lua_giua_trai": ("F", (660, 335), None, "k",
                      "THE SMALL FLAME between the left big flame and the tallest flame (about x = 608 to x = 715, y = 265 to "
                      "y = 385). " + FLAME_ROOT.format(sau="the tallest stone column", r="about 55 px further down, to about y = 440")),
    "lua_phai": ("F", (905, 335), None, "k",
                 "THE MEDIUM FLAME right of the tallest flame (about x = 850 to x = 955, y = 248 to y = 400). " +
                 FLAME_ROOT.format(sau="the shell and the far column", r="about 45 px further down, to about y = 445")),
    "lua_sung": ("F", (1030, 430), None, "k",
                 "THE SMALL FLAME at the right end, behind the big horn (about x = 985 to x = 1062, y = 355 to y = 480). " +
                 FLAME_ROOT.format(sau="the big horn", r="about 50 px further down, to about y = 530")),
    "ong_sau_xa": ("F", (815, 850), "p_xiaotui03", "c",
                   "THE FAR HIND LEG BLOCK: the pillar leg seen under the belly between the two near legs (visible about x = 745 to "
                   "x = 885, y = 850 to y = 945). Complete it as a pillar block like the other legs, with a rounded top at about "
                   "y = 745 (hidden behind the belly)."),
}
TO = sorted({v[0] for v in P.values()})
LUA = ["lua_sung", "lua_duoi", "lua_trai", "lua_giua_trai", "lua_cao", "lua_phai", "lua_nho"]

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
MO_TA_EN = ("a fire tortoise golem facing right: a big domed slate blue-grey stone shell with dark stone columns and seven flames on "
            "top, a lighter belly plate, four pillar legs (small orange crystals on the two front ones), a short tail with ivory "
            "spikes at the left, and at the front right an ivory skull-like face mask with one yellow eye, a jaw block under it, a "
            "huge curved near horn and a smaller far horn behind the mask.")
MO_TA_VI = ("rùa golem lửa đá bazan xám lam (hướng A đã duyệt): mai vòm có cụm cột đá chàm than và bảy ngọn lửa, bụng xám nhạt, bốn chân "
            "trụ (pha lê cam ở hai chân trước), đuôi ngắn gai ngà, mặt sọ ngà một mắt vàng, hàm, sừng gần to cong, sừng xa nhỏ sau mặt")


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def build():
    if not os.path.exists(DUYET):
        raise SystemExit("chưa có concept duyệt " + DUYET)
    os.makedirs(PK, exist_ok=True)
    gd = ["", "## Lượt 2: mảnh đúng chỗ, đúng cỡ (2026-11-13, người dùng chọn A; `L1c_bazan.png` → `L1_duyet.png`)", "",
          "Mỗi file vẽ lại concept đã duyệt nhưng chỉ giữ vài mảnh không chồng nhau, vẽ đủ phần khuất, bỏ hết thứ khác (nền trắng). "
          "Ngọn lửa vẽ đủ gốc (để rig đung đưa, co lại). Ba đùi khuất và lòng miệng vẽ ở góc trống. Ảnh mẫu duy nhất của mọi file:", "",
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
        t += [f"{i}. {P[k][4]}" for i, k in enumerate(ten, 1)]
        t += ["", f"Exactly {len(ten)} separate parts on the canvas, nothing else.", "", FLAT, BG]
        ghi(p, t)
        gd += [f"- **`{ma}`** ({', '.join(ten)}): chỉ gửi GPT `{os.path.normpath(p)}`; ảnh lưu vào `{os.path.normpath(out)}`."]
    gd += ["", "Kiểm từng ảnh: đúng các mảnh đã kê, trùng chỗ concept, viền mực kín, không chạm nhau, phần khuất vẽ đủ, nền trắng, "
           "không bóng. Claude cắt bằng `rua_lua_manh.py lam`."]
    hd = os.path.join(PK, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    ghi(hd, [cu] + gd)
    print(len(TO), "tờ,", len(P), "mảnh")


# ---------------------------------------------------------------- cắt
MAT_TAT = (112, 108, 104)
NGUOI = [((242, 138, 46), (88, 84, 96)), ((224, 68, 31), (70, 66, 78)), ((255, 212, 90), (108, 104, 112))]
# thứ tự vẽ sau → trước: theo slot của con gốc; mặt đè lên hàm (mép răng cưa của mặt là răng trên), lòng miệng nằm sau cả hai
# Bụng nằm SAU chân sau gần (con gốc để bụng trước chân sau gần, nhưng tấm bụng của mình vẽ đủ cả phần khuất, dài hơn hẳn: lúc bò thân hạ
# thấp nó phủ lên chân sau như cái đĩa)
THU_TU = ["lua_sung", "lua_duoi", "dui_sau_xa", "ong_sau_xa", "duoi", "cot_xa", "dui_truoc_xa", "ong_truoc_xa", "bung", "dui_sau_gan",
          "ong_sau_gan", "dui_truoc_gan", "mai", "sung_xa", "lua_trai", "lua_giua_trai", "lua_cao", "lua_phai", "lua_nho",
          "cot_gan", "hong", "ham", "mat_so", "mat_tat", "sung_gan", "ong_truoc_gan"]
DOI = {}
# chỉnh tay (dời x, dời y, tỉ lệ quanh tâm [, tỉ lệ dọc riêng]) cho mảnh Codex vẽ lệch concept. Đã thử dò tự động theo màu + nét mực: mảnh một màu nằm cạnh
# mảnh cùng màu (mặt ngà cạnh sừng ngà, mai cạnh chân) bị kéo lệch và phóng to, nên bỏ; phần lớn mảnh Codex đặt đúng sẵn (lệch 0–2 px).
# mai (tờ G, vòm kín): Codex vẽ thấp hơn concept ~55 px và mép dưới trùm gần hết bụng → dời lên, co dọc 0,90 (đỉnh ~366, mũi vạt trước ~790);
# bề ngang gần bằng mai của rig gốc (x 369–1154 trên khung concept) nên chân cột đá xa (đáy y 518) nấp sau mép mai, hết lơ lửng
CHINH = {"mai": (10, -60, 0.98, 0.90), "ham": (-4, -57, 0.72), "bung": (0, -55, 1.0), "lua_nho": (0, -22, 1.0), "lua_sung": (0, -6, 1.0)}
# mai: Codex vẽ thừa một cái móc cuộn ở mép dưới bên trái (gốc đuôi vẽ nhầm vào mai): cắt theo đường thẳng (toạ độ trên tờ M_A), kẻ lại mực
MAI_CAT = None           # tờ A cũ: ((396, 650), (478, 718)); tờ G vẽ mai kín nên không cắt nữa
MAI_O = None             # tờ A cũ: (539, 714), một điểm trong ô đá thừa dưới nét vành trái


def moi_nhat(ma):
    """tờ mới nhất của mã (M_<ma>.png, M_<ma>_2.png ...)."""
    c = [f for f in os.listdir(G.TAI) if f == f"M_{ma}.png" or (f.startswith(f"M_{ma}_") and f.endswith(".png"))]
    if not c:
        return None
    c.sort(key=lambda f: (0 if f == f"M_{ma}.png" else int(f[len(f"M_{ma}_"):-4])))
    return os.path.join(G.TAI, c[-1])


def cat_to(ma):
    import cv2
    p = moi_nhat(ma)
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
    print(f"  tờ {ma} ({os.path.basename(p)}): {len(ra)} mảnh" + (f"; cụm THỪA: {thua}" if thua else ""))
    return ra


def lam():
    import cv2
    os.makedirs(MANH, exist_ok=True)
    C = ML.doc(DUYET)
    Pm = {}
    for ma in TO:
        if moi_nhat(ma) is None:
            print(f"  chưa có tờ {ma}")
            continue
        Pm.update(cat_to(ma))
    dat, anh_ = {}, {}

    def luu(ten, im, goc, slot, kieu):
        if ten in DOI:
            goc = (goc[0] + DOI[ten][0], goc[1] + DOI[ten][1])
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = im
        dat[ten] = dict(goc=[int(goc[0]), int(goc[1])], co=[im.width, im.height], slot=slot, kieu=kieu)

    if "mai" in Pm and MAI_CAT:                  # cắt cái móc thừa ở mép dưới trái của mai, kẻ lại nét mực dọc đường cắt
        A, m = Pm["mai"]
        (x0, y0), (x1, y1) = MAI_CAT
        yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        duong = y0 + (xx - x0) * (y1 - y0) / (x1 - x0)
        bo = (xx < x1) & (yy > np.where(xx < x0, y0, duong))
        m2 = m & ~bo
        A2 = A.copy().astype(np.uint8)
        net = cv2.line(np.zeros(m.shape, np.uint8), (x0, y0), (x1, y1), 1, 7) > 0
        vanh = net & m & cv2.dilate(m2.astype(np.uint8), ML.el(5)).astype(bool)      # nét mực chỉ trong phần mai cũ, sát mép vừa cắt
        A2[vanh] = (43, 33, 24)
        m2 |= vanh
        Pm["mai"] = (A2.astype(np.int32), m2)
    for ten, (A, m) in Pm.items():
        im, goc = ML.manh_rgba(A, m)
        if ten == "mai" and MAI_O:               # bỏ luôn Ô đá thừa nằm dưới nét vành trái (giữa nét vành, đường cắt và vòm chân): mép mai
            arr = np.asarray(im).copy()          # bên trái là chính nét vành Codex đã vẽ, không còn mép cắt lởm chởm
            al = arr[..., 3] > 128
            muc = al & (arr[..., :3].max(2) < 95)
            n_, lab_, st_, _ = cv2.connectedComponentsWithStats((al & ~muc).astype(np.uint8), connectivity=4)
            k_ = lab_[MAI_O[1] - goc[1], MAI_O[0] - goc[0]]
            if k_ > 0:
                lon = np.array([i_ != k_ and i_ > 0 and st_[i_, 4] >= 400 for i_ in range(n_)])     # đốm sáng lọt trong nét mực không tính
                con = lon[lab_]
                giu = con | (muc & cv2.dilate(con.astype(np.uint8), ML.el(6)).astype(bool))
                arr[..., 3] = np.where(giu, arr[..., 3], 0)
                im = Image.fromarray(arr, "RGBA")
                print(f"    mai: bỏ ô thừa {int((lab_ == k_).sum())} px dưới nét vành trái")
        if ten in CHINH:                         # Codex vẽ lệch chỗ / lệch cỡ: co quanh tâm rồi dời (số đọc trên mau/_tho_tren_concept.png)
            dx, dy, sx = CHINH[ten][:3]
            sy = CHINH[ten][3] if len(CHINH[ten]) > 3 else sx
            cx, cy = goc[0] + im.width / 2, goc[1] + im.height / 2
            if abs(sx - 1.0) > 1e-6 or abs(sy - 1.0) > 1e-6:
                im = im.convert("RGBa").resize((max(2, round(im.width * sx)), max(2, round(im.height * sy))), Image.LANCZOS).convert("RGBA")
            goc = (int(round(cx - im.width / 2 + dx)), int(round(cy - im.height / 2 + dy)))
        luu(ten, im, goc, P[ten][2], P[ten][3])
        if ten.startswith("lua_"):               # điểm gốc lửa: tâm 10 % hàng thấp nhất của mảnh (chỗ gốc nấp sau đá)
            a = np.asarray(im)[..., 3] > 100
            ys, xs = np.nonzero(a)
            sel = ys >= ys.max() - 0.10 * (ys.max() - ys.min())
            dat[ten]["goc_lua"] = [int(goc[0] + xs[sel].mean()), int(goc[1] + ys[sel].mean())]
    # lòng miệng (vẽ ở góc tờ): đặt sau mặt và hàm, tâm ở chỗ mép răng cưa của mặt gặp hàm; chỉ giữ phần nằm trong hình mặt + hàm lúc
    # nghỉ (co 5 px) nên lúc ngậm khuất hẳn, hàm hạ xuống thì lộ ra trong khe
    if "hong" in anh_ and "mat_so" in anh_ and "ham" in anh_:
        Hc_, Wc_ = C.shape[:2]
        U = np.zeros((Hc_, Wc_), np.uint8)
        for t_ in ("mat_so", "ham"):
            a = np.asarray(anh_[t_])[..., 3] > 128
            gx, gy = dat[t_]["goc"]
            U[gy:gy + a.shape[0], gx:gx + a.shape[1]] |= a.astype(np.uint8)
        U = cv2.erode(U, ML.el(5)).astype(bool)
        hx, hy = dat["ham"]["goc"]
        hw, hh_ = dat["ham"]["co"]
        tw, th = int(hw * 0.95), int(hh_ * 0.80)
        hg = anh_["hong"].convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        px, py = int(hx + hw * 0.52 - tw / 2), int(hy + hh_ * 0.30 - th / 2)
        o = np.asarray(hg).copy()
        o[..., 3] = np.where(U[py:py + th, px:px + tw], o[..., 3], 0)
        # không thò ra bên phải mặt: chỉ tới đầu phải của mép răng cưa (30 % hàng dưới cùng của mặt), lùi 10 px
        am = np.asarray(anh_["mat_so"])[..., 3] > 128
        mx, my = dat["mat_so"]["goc"]
        duoi_ = am[int(am.shape[0] * 0.70):]
        x_phai = mx + int(np.nonzero(duoi_.any(0))[0].max()) - 10
        if x_phai - px < tw:
            o[:, max(0, x_phai - px):, 3] = 0
        luu("hong", Image.fromarray(o, "RGBA"), (px, py), None, "k")
    # mắt tắt: vùng mắt vàng của mặt đổi sang xám tro, cắt sát; slot ngay trên mặt, ẩn mặc định (die, appear)
    if "mat_so" in anh_:
        arr = np.asarray(anh_["mat_so"]).astype(np.int32)
        r_, g_, b_, a_ = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
        vang = (a_ > 0) & (r_ > 200) & (g_ > 150) & (b_ < 120)
        n_, lab_, st_, _ = cv2.connectedComponentsWithStats(vang.astype(np.uint8), 8)
        if n_ > 1:
            k = 1 + int(np.argmax(st_[1:, 4]))
            mm = cv2.dilate((lab_ == k).astype(np.uint8), ML.el(2)).astype(bool) & (a_ > 0)
            ys, xs = np.nonzero(mm)
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            o = arr[y0:y1, x0:x1].astype(np.uint8).copy()
            sang = (o[..., :3].max(2) >= 95) & mm[y0:y1, x0:x1]          # giữ nét mực và con ngươi, tròng vàng → xám tro phẳng
            o[..., :3][sang] = MAT_TAT
            o[..., 3] = np.where(mm[y0:y1, x0:x1], o[..., 3], 0)
            g0 = dat["mat_so"]["goc"]
            luu("mat_tat", Image.fromarray(o, "RGBA"), (g0[0] + x0, g0[1] + y0), None, "k")
            dat["mat_tat"]["tam_mat"] = [int(g0[0] + (x0 + x1) / 2), int(g0[1] + (y0 + y1) / 2)]
    # pha lê NGUỘI: vùng cam của hai ống chân trước đổi sang đá xám tím, cắt sát; slot ngay trên ống chân, ẩn mặc định (die)
    for ten in ("ong_truoc_gan", "ong_truoc_xa"):
        if ten not in anh_:
            continue
        arr = np.asarray(anh_[ten]).astype(np.int32)
        r_, g_, b_, a_ = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
        cam = (a_ > 0) & (r_ > 190) & (r_ - b_ > 90)
        if cam.sum() < 30:
            continue
        mm = cv2.dilate(cam.astype(np.uint8), ML.el(3)).astype(bool) & (a_ > 0)
        ys, xs = np.nonzero(mm)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        sub = ML.doi_mau(Image.fromarray(arr[y0:y1, x0:x1].astype(np.uint8), "RGBA"), NGUOI)
        o = np.asarray(sub).copy()
        o[..., 3] = np.where(mm[y0:y1, x0:x1], o[..., 3], 0)
        g0 = dat[ten]["goc"]
        luu(ten + "_nguoi", Image.fromarray(o, "RGBA"), (g0[0] + x0, g0[1] + y0), None, "k")
        dat[ten + "_nguoi"]["tren"] = ten
    thu_tu = []
    for t in THU_TU:
        if t in anh_:
            thu_tu.append(t)
            if t + "_nguoi" in anh_:
                thu_tu.append(t + "_nguoi")
    thieu = [t for t in anh_ if t not in thu_tu]
    if thieu:
        print("  CHƯA xếp thứ tự:", thieu)
    dat["_thu_tu"] = thu_tu
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in thu_tu:
        if dat[t]["kieu"] != "r" and not t.endswith("_tat") and not t.endswith("_nguoi"):
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


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "lam":
        lam()
    else:
        print(__doc__)
