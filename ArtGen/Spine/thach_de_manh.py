# -*- coding: utf-8 -*-
"""Thổ Tinh (thach_de, final boss đảo Thổ, rig `monster_3802`): tờ MẢNH RỜI và cắt mảnh. Con gốc gần như toàn mảnh cứng một xương lơ
lửng (skill pokiclash-spine-rig mục 25) nên mảnh của mình là hình trọn, vẽ rời trên tờ, cùng tỉ lệ với concept `L1_duyet.png`; rig đặt
từng mảnh vào chỗ mảnh tương ứng của họ (thach_de_rig.py).

    thach_de_manh.py prompt       ba file prompt tờ mảnh → gui_gpt/thach_de_1/luot_4_manh_<A|B|C>.txt (+ HUONG_DAN.md)
    thach_de_manh.py cat [A B C]  cắt tờ tai_ve/M_<k>.png → manh/<tên>.png + manh/_soi.png (in số mảnh, dừng nếu thiếu)

Tờ A: hành tinh (không hố), mặt trăng to, mặt trăng nhỏ, bốn hố của hành tinh (hố là mảnh riêng: trôi ngang + co bề ngang về mép đĩa
= hành tinh tự quay, không cần mặt nạ). Tờ B: đầu, hai vỏ vai, hai khối cẳng tay, năm vệ tinh. Tờ C: tám lưỡi trăng, tám đốt tay, chân,
hông, mảnh vụn."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CODE = "thach_de"
BASE = os.path.join(HERE, "inbox", f"{CODE}_1")
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh")
DUYET = os.path.join(TAI, "L1_duyet.png")

DAU = ("IMAGES (attached in this order; open each from its path):\n"
       "image 1 = {duyet}: our approved character concept (1536x1024, white background): a stone planet with moon-rock fists, crescent "
       "shells, a crown of crescent blades and small orbiting moons. Match EXACTLY its drawing style: wobbly dark-brown ink outline "
       "(#2B2118, about 7 px), flat colours with visible coloured-pencil / wax-crayon hatching, one darker tone on side faces, no "
       "shading, no highlights, no gradients, no glow, no shadows.")
CHUNG = ("TASK: draw a PARTS SHEET for animating the character of image 1: the pieces listed below, as SEPARATE objects on a pure-white "
         "background. Rules: every piece is COMPLETE (the whole object, including what is hidden behind other things in image 1), has a "
         "closed ink outline all the way round, and is drawn at the SAME SCALE, with the same line weight, colours and hatching as in "
         "image 1. Pieces must NOT touch or overlap: leave at least 40 px of white between any two pieces. Draw ONLY the listed pieces, "
         "each exactly once, at the place given (x, y in pixels on the 1536x1024 sheet, x from the left, y from the top). No text, no "
         "labels, no numbers, no arrows, no frame, no ground line, no cast shadows, no sparkles.")
PAL = ("PALETTE (flat): planet bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F / umber #7A4A2E; moon rock #CFC8D6, its side "
       "faces #9D95AB, its craters #B3ABC0; tusks #F4EAD2; eyes amber #F6C443; ink #2B2118.")
TO = {
    "A": dict(
        vi="hành tinh (đĩa tròn trọn, KHÔNG hố), mặt trăng to, mặt trăng nhỏ, bốn hố rời của hành tinh",
        ds=["PLANET, centre about (330, 512): ONE perfect circle about 540 px across: the banded stone planet of image 1, the COMPLETE "
            "disc with nothing in front of it: seven flat horizontal bands of rock strata with gently wavy edges running across the "
            "whole disc from edge to edge (cream, ochre, terracotta, umber, in the order of image 1). NO craters, NO spots, NO marks "
            "on it at all.",
            "BIG MOON, centre about (850, 512): ONE perfect sphere of grey-lilac moon rock about 400 px across (the big left fist of "
            "image 1 WITHOUT its finger stones): a complete circle with five flat round craters of different sizes.",
            "SMALL MOON, centre about (1310, 250): ONE perfect sphere of the same moon rock about 290 px across (the right fist of "
            "image 1 WITHOUT its finger stones) with four flat round craters.",
            "FOUR PLANET CRATERS, in a 2 x 2 block inside x 1150-1470, y 560-940: four separate flat OVAL patches (wider than tall), "
            "each ONE flat umber-brown colour #8A5636 with an ink outline, sizes about 130x86, 104x68, 82x54 and 60x40 px. They are "
            "the craters of the planet, drawn loose."]),
    "B": dict(
        vi="đầu (mặt nạ thú + cặp sừng trăng lưỡi liềm), vỏ vai to, vỏ vai nhỏ, hai khối cẳng tay, năm vệ tinh",
        ds=["HEAD, centre about (260, 280): the horned beast mask of image 1 with its two horns that together make an upward crescent "
            "moon, COMPLETE, in the same three-quarter view facing right, about 340 px wide and 380 px tall: heavy angry brow, two "
            "amber eyes, closed scowling mouth, two big cream tusks. Nothing else attached to it.",
            "BIG SHOULDER SHELL, centre about (760, 290): the big thick crescent-shaped moon-rock shell of the LEFT shoulder of image "
            "1, COMPLETE (also the part that is hidden behind the planet in image 1), about 360 px wide and 480 px tall, with its sharp "
            "sickle tips and a few craters.",
            "SMALL SHOULDER SHELL, centre about (1260, 280): the crescent-shaped shell of the RIGHT shoulder of image 1, COMPLETE, "
            "about 260 px wide and 380 px tall.",
            "TWO FOREARM CHUNKS, centres about (190, 800) and (480, 810): two rounded half-moon chunks of moon rock with one or two "
            "craters each, about 220x230 px and 150x170 px.",
            "FIVE MOONLETS in a row, centres about (760, 800), (960, 800), (1130, 800), (1270, 800), (1390, 800): five small perfect "
            "spheres of moon rock, 140, 112, 90, 70 and 54 px across, each with two or three flat craters."]),
    "C": dict(
        vi="tám lưỡi trăng (dựng đứng, đế dưới, mũi trên cong sang phải), tám đốt tay, hai đùi, hai bàn chân, hai gối, hông, bốn mảnh vụn",
        ds=["ROW 1, y 40-340: EIGHT CRESCENT BLADES in a row from left to right (the sickle-shaped moon-rock blades of the crown on top "
            "of the planet in image 1), each one separate, standing UPRIGHT: wide rounded base at the bottom, sharp tip at the top "
            "curving to the RIGHT. Heights about 290, 265, 235, 205, 175, 145, 115 and 90 px; widths about half the height. One to three "
            "small craters each.",
            "ROW 2, y 420-610: EIGHT KNUCKLE STONES in a row: chunky rounded blocks of moon rock like the finger stones under the fists "
            "of image 1, plain (no craters), each a slightly different shape: two about 160 px, two about 135 px, two about 110 px and "
            "two about 85 px across.",
            "ROW 3, y 690-990, from left to right: TWO THIGH STONES (rounded upright blocks about 95x125 px); TWO FEET (stubby stone "
            "feet with a flat bottom and three toe bumps pointing right, about 120x100 px); TWO round KNEE STONES (about 55 px); ONE HIP "
            "BLOCK (a wide rounded block about 200x130 px with one crater); FOUR SHARDS (angular broken chips of moon rock, about 110, "
            "95, 80 and 65 px)."]),
}
# số mảnh mỗi tờ và tên theo thứ tự đọc (hàng trên → dưới, trái → phải)
TEN = {
    "A": ["hanh_tinh", "trang_to", "trang_nho", "ho_1", "ho_2", "ho_3", "ho_4"],
    "B": ["dau", "vo_to", "vo_nho", "cang_to", "cang_nho", "ve_1", "ve_2", "ve_3", "ve_4", "ve_5"],
    "C": [f"luoi_{i}" for i in range(1, 9)] + [f"dot_{i}" for i in range(1, 9)] +
         ["dui_1", "dui_2", "ban_1", "ban_2", "goi_1", "goi_2", "hong", "vun_1", "vun_2", "vun_3", "vun_4"],
}
HANG = {"A": None, "B": [520], "C": [380, 650]}        # ranh hàng (y) để xếp thứ tự đọc; A xếp riêng

# ---- lượt 5 (người dùng 2026-11-18: "tạo thêm hàm dưới", chiêu cuối "dang 2 tay ngửa lòng bàn tay ra (cần thì gen thêm)"): tờ D
DAU_D = os.path.join(MANH, "dau.png")
TO_D = dict(
    vi="đầu bỏ hàm dưới và nanh (hàm trên có răng nanh nhỏ), hàm dưới kèm lòng miệng, hai nanh rời, bàn tay to và nhỏ xoè ngửa",
    ds=["UPPER HEAD, centre about (230, 260): image 2 WITHOUT its lower jaw and WITHOUT its two big tusks: both crescent horns, the "
        "heavy brow, the two amber eyes, the nose and cheeks (everything ABOVE the mouth line) at EXACTLY the size, proportions and "
        "three-quarter view of image 2 (407 px wide). Its bottom edge is the UPPER LIP: a row of short pointed cream upper fangs hangs "
        "from it, a slightly bigger fang at each corner. Closed ink outline all the way round, also under the fangs.",
        "BIG OPEN HAND, centre about (850, 270), about 520 px wide and 380 px tall: the big LEFT fist of image 1 OPENED with the palm "
        "turned UP to the sky, seen from the front and a little above. The palm is a broad round dish of the same grey-lilac moon rock "
        "(side faces in the darker tone) with one big shallow round crater in its middle; four thick stubby fingers, each made of two "
        "chunky rounded stone segments like the knuckle stones under the fists of image 1, spread out to the LEFT and curl a little "
        "upward at the tips; a short thick stone thumb points UP from the near edge of the palm. The wrist side (RIGHT end) is a plain "
        "rounded edge. All fingers stay joined to the palm: ONE closed shape.",
        "LOWER JAW, centre about (230, 780), about 250 px wide and 270 px tall: the lower jaw of image 2 for an OPENING MOUTH, same "
        "three-quarter view facing right: at the bottom the chin and lower lip in the same grey-lilac rock and ink line (the part of "
        "image 2 below the mouth line); along the top of the lip a row of short blunt cream lower teeth; ABOVE the teeth the INSIDE of "
        "the mouth: one dark maroon area (#4A2228) with a rounded red-brown tongue (#A8505A) lying in it. This dark area rises about "
        "150 px above the teeth and its top is a smooth dome. NO tusks on this piece.",
        "TWO TUSKS, centres about (500, 780) and (620, 780): the two big curved cream tusks of image 2, each drawn ALONE as its own "
        "closed shape with an ink outline: the near one about 80 px wide and 140 px tall, the far one about 65 x 115 px; wide base at "
        "the bottom, tip at the top curving outward.",
        "SMALL OPEN HAND, centre about (1250, 740), about 400 px wide and 290 px tall: the same open palm-up hand for the RIGHT fist of "
        "image 1: a MIRROR of the big open hand (fingers spread to the RIGHT and curl up at the tips, thumb up, wrist on the LEFT), "
        "smaller. ONE closed shape."])
TEN["D"] = ["dau_tren", "tay_xoe_to", "ham", "nanh_1", "nanh_2", "tay_xoe_nho"]
HANG["D"] = [540]


def prompt_d():
    p_hd = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n")
    td = "## Lượt 5: tờ D, hàm dưới và bàn tay xoè (2026-11-18)"
    if td in hd:
        hd = hd[:hd.index(td) - 1]
    out = os.path.join(TAI, "M_D.png")
    p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "luot_5_manh_D.txt")
    lines = DAU.format(duyet=os.path.normpath(DUYET)).split("\n")
    lines += [f"image 2 = {os.path.normpath(DAU_D)}: the approved HEAD piece of that character (407x455 px, transparent background): "
              "horned beast mask, three-quarter view facing right, closed scowling mouth with two big cream tusks rising from the lower "
              "jaw. Shown at its real size: keep EXACTLY its size, drawing and colours.",
              "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
              "If a file with that name already exists, save as M_D_2.png, M_D_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", CHUNG.replace("image 1", "images 1 and 2", 1), "", "PIECES:"] + \
        [f"- {d}" for d in TO_D["ds"]] + ["", PAL + " Inside of the mouth: maroon #4A2228, tongue #A8505A.", "",
                                          "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF)."]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    hd += ["", td, "",
           "Người dùng: \"tạo thêm hàm dưới cho tướng\", chiêu cuối \"dang 2 tay ngửa lòng bàn tay ra (cần thì gen thêm)\".", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
           f"| 1 | `{os.path.normpath(DUYET)}` | Concept đã duyệt (hành tinh đá, nắm đấm mặt trăng), 1536x1024, nền trắng |",
           f"| 2 | `{os.path.normpath(DAU_D)}` | Mảnh đầu đã cắt (mặt nạ thú sừng trăng, miệng ngậm, hai nanh), 407x455, nền trong |", "",
           f"- **Tờ D**: {TO_D['vi']}. File prompt `{os.path.normpath(p)}`; ảnh lưu `{os.path.normpath(out)}`. Kiểm: đủ 6 mảnh rời, "
           "đầu trên KHÔNG còn cằm và nanh, lòng miệng nằm trên hàm dưới, hai bàn tay ngửa đủ bốn ngón + ngón cái, viền kín.",
           "- Sửa nhanh: \"keep the upper head exactly like image 2 above the mouth line\"; \"the open hands must show the palm facing "
           "up, fingers attached\"."]
    open(p_hd, "w", encoding="utf-8", newline="\n").write("\n".join(hd) + "\n")
    print(p)


def prompt():
    p_hd = os.path.join(HERE, "gui_gpt", f"{CODE}_1", "HUONG_DAN.md")
    hd = open(p_hd, encoding="utf-8").read().rstrip("\n").split("\n") if os.path.exists(p_hd) else []
    td = "## Lượt 4: ba tờ mảnh rời (2026-11-18)"
    if td in hd:
        hd = hd[:hd.index(td) - 1]
    hd += ["", td, "", "Concept đã chọn: `L1_duyet.png` (= `L3_B2Y.png`). Mảnh vẽ rời, trọn hình, cùng tỉ lệ concept; rig đặt vào chỗ "
           "mảnh tương ứng của con gốc. Ảnh mẫu 1: `" + os.path.normpath(DUYET) + "` (concept đã duyệt, 1536x1024, nền trắng).", ""]
    for k, t in TO.items():
        out = os.path.join(TAI, f"M_{k}.png")
        p = os.path.join(HERE, "gui_gpt", f"{CODE}_1", f"luot_4_manh_{k}.txt")
        lines = DAU.format(duyet=os.path.normpath(DUYET)).split("\n")
        lines += ["", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
                  f"If a file with that name already exists, save as M_{k}_2.png, M_{k}_3.png ... in the same folder. Do not edit, move "
                  "or delete any other file.", "", CHUNG, "", "PIECES:"] + [f"- {d}" for d in t["ds"]] + ["", PAL, "",
                  "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF)."]
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        hd += [f"- **Tờ {k}**: {t['vi']}. File prompt `{os.path.normpath(p)}`; ảnh lưu `{os.path.normpath(out)}`. Kiểm: đủ "
               f"{len(TEN[k])} mảnh, không mảnh nào chạm nhau, viền kín."]
        print(p)
    open(p_hd, "w", encoding="utf-8", newline="\n").write("\n".join(hd) + "\n")


def _moi_nhat(k):
    c = [f for f in os.listdir(TAI) if f == f"M_{k}.png" or (f.startswith(f"M_{k}_") and f.endswith(".png"))]
    c.sort(key=lambda f: os.path.getmtime(os.path.join(TAI, f)))
    return os.path.join(TAI, c[-1])


def cat(ks):
    from quai import anh
    os.makedirs(MANH, exist_ok=True)
    for k in ks:
        p = _moi_nhat(k)
        to = anh.doc_to(p, dien_tich_min=500, gop_px=14)
        ms = to.manh
        if k == "A":
            lon = sorted(ms, key=lambda m: -m["dt"])[:3]
            lon.sort(key=lambda m: m["x0"])
            nho = [m for m in ms if m not in lon]
            nho.sort(key=lambda m: -m["dt"])
            thu = lon + nho
        else:
            ranh = HANG[k]
            def hang(m):
                cy = (m["y0"] + m["y1"]) / 2
                return sum(cy > r for r in ranh)
            thu = sorted(ms, key=lambda m: (hang(m), m["x0"]))
        print(f"tờ {k} ({os.path.basename(p)}): {len(ms)} mảnh, cần {len(TEN[k])}")
        for m in thu:
            print("   ", m["x0"], m["y0"], m["x1"] - m["x0"], m["y1"] - m["y0"], m["dt"])
        if len(ms) != len(TEN[k]):
            raise SystemExit(f"tờ {k}: sai số mảnh, xem lại ảnh")
        anh.luu_manh(to, dict(zip(TEN[k], thu)), MANH)
    anh.to_soi(MANH, sorted(f[:-4] for f in os.listdir(MANH) if f.endswith(".png") and not f.startswith("_")))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "prompt":
        prompt()
    elif a[0] == "prompt_d":
        prompt_d()
    elif a[0] == "cat":
        cat(a[1:] or list(TO))
