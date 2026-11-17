# -*- coding: utf-8 -*-
"""Quái bùn (quai_bun, tướng 8 đảo Thổ, rig monster_3668; ghi chú inbox/quai_bun_ghichu.md): MẢNH của mình.

Concept duyệt (tai_ve/L1_duyet.png = L1_A, người dùng chọn "A" 2026-11-17) vẽ theo dáng rig 3668. Hai loại mảnh:

1. "ĐÚNG CHỖ, ĐÚNG CỠ" từ concept (tờ T1..T5, Magnific): mỗi tờ vài mảnh không chạm nhau, vẽ đủ phần bị che, rig bám HỢP lưới các part của họ
   (như rong_cat_non_manh):
     than        thân + đế vũng bùn (P_shenti2, P_shenti1, P_shenti1_1..3; bỏ mạch xanh P_shenti2_5)            T1
     vai_gan     u vai gần trên lưng, mang ba bong bóng bùn (P_shouR1)                                       T2
     tay_xa_tren bắp tay xa bên phải, sau thân (P_shouL1)                                                    T2
     dau         đầu = hàm trên + hàng răng trên + hai sừng đá, KHÔNG mắt (P_tou_2_02, 03, 01, 06)          T3
     tay_xa_duoi cẳng tay xa bên phải dưới (P_shouL2)                                                        T3
     ham         bụng = hàm dưới + hàng răng dưới (P_tou_2_05)                                               T4
     tay_gan     khối cẳng tay gần tròn to bên trái (P_shouR2)                                               T4
     long_mieng  lòng miệng hổ phách (P_tou_2_07, 04)                                                        T5
     mat         mắt mở cắt thẳng từ concept; mat_nham dựng từ mặt nạ mắt
2. "THEO KHUNG PART" của họ (tờ D_P, D_X, D_V, D_H, Magnific; như cung_lua_da): tờ hướng dẫn là chính các part gốc cắt theo lưới, phóng to;
   GPT đổi da, giữ hình bóng; rig dùng NGUYÊN lưới của họ:
     P  hai lòng bàn tay + 16 đốt ngón (ngón co 50–80° trong clip nên mỗi đốt một mảnh như họ) → đá cuội xám, lòng bàn tay bùn
     X  chín xúc tu → giọt bùn dựng đầu tròn
     V  tay co giãn G_shoudabi / G_shoubi / G_shouzhang → ống bùn + nắm đấm đá
     H  đầu hàm khổng lồ của skill_04 (P_tou_1_01..06) + mắt P_yanjing_1/2 → hàm bùn, lòng hổ phách, răng đá cuội

    quai_bun_manh.py to            tờ khung part (mau/goc_<P|X|V|H>.png + .json) + mọi file prompt → gui_gpt/quai_bun_1/luot_2_*.txt
    quai_bun_manh.py cat [tờ ...]  cắt tờ đã gen (tai_ve/M_T*.png, D_*.png) → manh/<tên>.png + manh/dat.json, manh/_iou.json, _so_*.png
    quai_bun_manh.py mat           mắt mở cắt từ concept + mắt nhắm → manh/mat*.png
    quai_bun_manh.py ghep          ghép mảnh concept theo thứ tự vẽ cạnh concept → manh/_ghep.png + IoU
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quai_bun  # noqa: E402,F401  (đăng ký mã quai_bun trong tho5.CON)
import tho5  # noqa: E402

G = tho5.dat("quai_bun")
W, H = 1536, 1024
DUYET = os.path.join(G.TAI, "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "quai_bun_1")
VUON_NUI = os.path.join(HERE, "inbox", "quy_nui_1", "tai_ve", "L1_duyet.png")
RES = 1.5                 # ảnh mảnh theo khung part = ảnh vùng của họ × RES
INK = (43, 33, 24)

# màu đo trên concept duyệt
MAU = dict(bun="#7D4B33", bun_toi="#623A24", bung="#A7744B", da="#A59482", da_toi="#7E7366", ho_phach="#F0A33F", vach="#CA6D1D",
           rang="#DECAB1", mat="#F2B33A")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a hulking MUD MONSTER built like a gorilla, turned to the "
        "right: dark chocolate-brown wet mud body, a big rounded shoulder hump on the back with three small mud bubbles, a big round near "
        "forearm at the left, mud drips standing up from the back and head, a heavy lumpy head with a thick brow ridge, two small fierce "
        "amber eyes and two short grey river-stone horns, a HUGE mouth opening downward from under the head across the chest (amber-ochre "
        "inside, rounded pale pebble teeth), a light-brown round belly that is the lower jaw, two fists made of big grey river stones, a "
        "wide flat mud puddle as its base. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
STYLE = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 (no "
         "shading, no highlights, no glow, no shadows).")
VIEN = ("complete it into ONE CLOSED SHAPE with the dark-brown ink outline all the way round; where it is hidden behind another part in "
        "image 1, draw the hidden portion as it would continue (plain mud of the same colour, same flat crayon colouring)")

# ================================================================ 1. tờ "đúng chỗ, đúng cỡ"
# tâm dự kiến (px concept) để gán cụm cắt ra đúng tên
TAM = {"than": (760, 640), "vai_gan": (640, 400), "tay_xa_tren": (1160, 600), "dau": (1000, 380), "tay_xa_duoi": (1150, 760),
       "ham": (900, 650), "tay_gan": (470, 560), "long_mieng": (1000, 560)}
NHOM = {
    "T1": [("than", "the BODY: the big rounded mass of mud that stays when BOTH ARMS, the HEAD, the light-brown BELLY, the open MOUTH and "
            "all the MUD DRIPS are taken away, plus the wide flat MUD PUDDLE base on the ground. Its rounded top (the back behind the "
            "shoulder hump) is at about y 290 between x 640 and x 980; it goes down behind the head and the mouth to its right side at "
            "about x 1120; its left side is at about x 600 (behind the big round near forearm); below the belly it narrows a little at "
            "about y 760 and melts into the PUDDLE, which spreads on the ground from the long tongue at the lower left (tip at about "
            "(275, 885)) to about x 1140, along y 790-915, with its wavy edge, a few drip blobs on its edge and the two small pebbles at "
            "about (520-560, 865)",
            "draw it WITHOUT the arms, the fists, the head, the belly, the mouth and the drips: where they cover the body, continue the "
            "plain chocolate-brown mud of the body (a smooth rounded outline, one or two mud bubbles at most); the top of the body is a "
            "plain rounded back (no drips, no hump), the right side goes on as a rounded edge behind where the head and mouth were; do "
            "NOT draw the loose flying drops around the creature")],
    "T2": [("vai_gan", "the NEAR SHOULDER HUMP: the big rounded top of the back on the left half, carrying the three small mud bubbles at "
            "about (780, 342), (723, 383) and (762, 432); it reaches from about x 440 to x 840 and from about y 250 (its rounded top, under "
            "the drips) down to about y 560",
            "draw it WITHOUT the mud drips standing on it (where a drip rises from it, keep its plain rounded top outline); its lower-left "
            "part, hidden behind the big round near forearm, continues as a rounded edge down to about y 560; its right end, towards the "
            "head, is a rounded edge at about x 840. " + VIEN),
           ("tay_xa_tren", "the FAR UPPER ARM at the right edge: the dark-brown rounded mass to the right of the open mouth, from behind "
            "the head at about (1100, 430) down to about y 760, its right edge at about x 1225",
            "its upper-left part, hidden behind the head, the mouth and the belly, continues as a rounded shoulder reaching left to "
            "about x 980; its lower end, hidden behind the far forearm, is rounded at about y 780. " + VIEN)],
    "T3": [("dau", "the HEAD = the UPPER JAW: the heavy lumpy mud head at the upper right with its thick overhanging brow ridge, its blunt "
            "rounded snout at the right (about x 1180), the two short grey river-stone horns on top (at about (1035-1085, 290-360) and "
            "(1125-1160, 320-370)), and the row of rounded pale pebble UPPER TEETH hanging down along the TOP edge of the mouth, from about "
            "(900, 455) to about (1140, 495); its lower-left part, the back of the head and cheek, comes down to about (850, 470)",
            "draw it WITHOUT the two eyes: where the amber eyes are (about (1030-1075, 425-460) and (1105-1135, 435-455)), plain mud face "
            "with the brow ridge kept above; WITHOUT any mud drip standing on it (keep its rounded top outline); WITHOUT the lower teeth, "
            "the amber inside of the mouth and the belly: the lower edge of the head in front is the row of upper teeth (outlined in ink); "
            "the back of the head behind is a rounded edge. " + VIEN),
           ("tay_xa_duoi", "the FAR FOREARM at the lower right: the dark-brown rounded part going down from about (1120, 620) to the far "
            "stone fist at about (1000-1150, 820-880), its right edge at about x 1225",
            "draw it WITHOUT the stone fist: the forearm ends in a plain rounded wrist of mud where the stones are; its top, hidden "
            "behind the belly, is rounded at about y 610. " + VIEN)],
    "T4": [("ham", "the BELLY = the LOWER JAW: the big light-brown round belly in the middle, from about (720, 500) to (1115, 800), with the "
            "row of rounded pale pebble LOWER TEETH standing along its rim on the LEFT and BOTTOM edges of the mouth (from about (885, 480) "
            "down to about (1110, 690))",
            "draw it WITHOUT the amber inside of the mouth (the rim of the belly with its teeth is the edge), WITHOUT the stone fists "
            "(continue the light-brown belly where the fists cover it, rounded bottom at about y 805) and WITHOUT the upper teeth. " + VIEN),
           ("tay_gan", "the NEAR FOREARM: the BIG ROUND mud bulge at the left, from about x 295 to x 650 and y 380 to y 700, and its lower "
            "part going down-right to the near stone fist at about (520-720, 560-800)",
            "draw it WITHOUT the stone fist: it ends in a plain rounded mud wrist where the stones are (at about (560-680, 640-760)); "
            "WITHOUT the mud drips; its top, the line where it meets the shoulder hump, is its own rounded outline. " + VIEN)],
    "T5": [("long_mieng", "the INSIDE OF THE MOUTH ONLY: the flat amber-ochre area between the teeth (about x 890-1110, y 450-690) with its "
            "darker orange back wall band on the right",
            "draw it WITHOUT any tooth, the head and the belly: continue the amber-ochre under every tooth and about 25 px beyond the rim "
            "all round, as one closed rounded shape with an ink outline; no tongue, no gums, no red flesh")],
}


def prompt_t():
    out_lines = []
    for nh, ds in NHOM.items():
        out, save = luu(f"M_{nh}")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(DUYET)}: {ANH1}", ""] + save + ["",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). " + STYLE + " Do not move, resize, rotate or redesign anything. Keep a clear white gap (at least 20 px) "
             "between the kept parts.",
             "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles, no loose drops."]
        ghi(p, t)
        out_lines.append((nh, ", ".join(x for x, _, _ in ds), p, out))
        print(p)
    return out_lines


# ================================================================ 2. tờ "theo khung part"
# tờ → các hàng [(slot, phóng)]; ảnh part lấy theo slot trong att_goc (mọi hình, kể cả hình không bật lúc dựng)
TO = {
    "P": [[("P_shouR3", 2.4), ("P_shouR3_1", 2.4), ("P_shouR3_2", 2.4), ("P_shouR3_3", 2.4), ("P_shouR3_4", 2.4), ("P_shouR3_5", 2.4)],
          [("P_shouR3_6", 2.4), ("P_shouR3_7", 2.4), ("P_shouR3_8", 2.4), ("P_shouL3", 2.4), ("P_shouL3_1", 2.4), ("P_shouL3_2", 2.4)],
          [("P_shouL3_3", 2.4), ("P_shouL3_4", 2.4), ("P_shouL3_5", 2.4), ("P_shouL3_6", 2.4), ("P_shouL3_7", 2.4), ("P_shouL3_8", 2.4)]],
    "X": [[("P_shenti2_2", 1.7), ("P_shenti2_3", 1.7), ("P_shenti2_4", 1.7), ("P_shouL1_1", 1.7)],
          [("P_shouR2_1", 1.7), ("P_shouR2_2", 1.7), ("P_shouR1_2", 1.7), ("P_shenti2_1", 1.7), ("P_shouR1_1", 1.7)]],
    "V": [[("G_shoudabi", 1.75), ("G_shouzhang", 1.75)], [("G_shoubi", 1.75)]],
    "H": [[("P_tou_1_01", 1.75), ("P_tou_1_02", 1.75)], [("P_tou_1_06", 1.75), ("P_tou_1_03", 1.75), ("P_tou_1_05", 1.75), ("P_tou_1_04", 1.75)],
          [("P_yanjing_1", 2.6), ("P_yanjing_2", 2.6)]],
}
STONE = (f"a big rounded GREY RIVER STONE: flat grey {MAU['da']}, with ONE darker grey {MAU['da_toi']} flat zone on its lower / side face "
         "(the face turned away), a smooth rounded outline following the silhouette")
MO_TA = {
    "P": ([("P_shouR3", f"NEAR PALM (the back of the near fist): wet chocolate-brown MUD {MAU['bun']}; its pale knuckle patch becomes "
            f"{STONE.replace('a big', 'a')} set in the mud")]
          + [(f"P_shouR3_{k}", f"NEAR FINGER segment: {STONE}") for k in range(1, 9)]
          + [("P_shouL3", f"FAR PALM: wet chocolate-brown MUD {MAU['bun']}; its pale knuckle patch becomes {STONE.replace('a big', 'a')} set in "
              "the mud")]
          + [(f"P_shouL3_{k}", f"FAR FINGER segment: {STONE}") for k in range(1, 9)]),
    "X": [(s, f"MUD DRIP standing up from the body: the same silhouette repainted as thick wet chocolate-brown MUD {MAU['bun']}; its wide "
              "flat tip (pink in image 1) becomes a heavy ROUND DROP of the same mud, drawn INSIDE the old tip area (a round blob, not a flat "
              "paddle, no pink); its thick base (the end that joins the body) stays plain mud with a rounded end")
          for s in ("P_shenti2_2", "P_shenti2_3", "P_shenti2_4", "P_shouL1_1", "P_shouR2_1", "P_shouR2_2", "P_shouR1_2", "P_shenti2_1",
                    "P_shouR1_1")],
    "V": [("G_shoudabi", f"STRETCHED UPPER ARM (a long thick tube of mud, the wide end at the left joins the shoulder, it narrows to the "
           f"right): wet chocolate-brown MUD {MAU['bun']}, a darker {MAU['bun_toi']} zone along its lower side; the little strand on its "
           "top (pink in image 1) becomes a small MUD DRIP with a round drop; the small white hole near its lower right edge stays white"),
          ("G_shouzhang", f"STRETCHED FIST at the end of the arm: the palm is chocolate-brown MUD {MAU['bun']}; each blocky finger and the "
           f"pale knuckle patch becomes {STONE.replace('a big', 'a')} (keep the lines between the fingers)"),
          ("G_shoubi", f"STRETCHED FOREARM (a very long tube of mud): wet chocolate-brown MUD {MAU['bun']}, a darker {MAU['bun_toi']} zone "
           "along its lower side; the two little strands on its top (pink in image 1) become two small MUD DRIPS with round drops")],
    "H": [("P_tou_1_01", f"GIANT UPPER JAW of the monster's head morphed into a huge open maw (the snout at the right, the back of the "
           f"head at the left, the jaw edge along the bottom): chocolate-brown MUD {MAU['bun']} with a thick lumpy brow ridge along its "
           f"top; the two big curved horns at the left (pink and dark in image 1) become TWO short blunt grey RIVER-STONE HORNS "
           f"{MAU['da']}; the row of pale teeth along the bottom edge become rounded pale PEBBLE TEETH {MAU['rang']}; no pink"),
          ("P_tou_1_02", f"GIANT LOWER JAW = the BELLY: light-brown {MAU['bung']} rounded belly, its rib lines become two or three soft mud "
           f"lines; the pale spots are removed; the teeth along its rim become rounded pale PEBBLE TEETH {MAU['rang']}"),
          ("P_tou_1_06", f"INSIDE OF THE GIANT MAW (the big rounded shape): flat warm AMBER-OCHRE {MAU['ho_phach']} (the glowing cyan and "
           f"its light streaks are REMOVED: one flat colour); the narrow band along its right edge becomes the darker orange back wall "
           f"{MAU['vach']}"),
          ("P_tou_1_03", f"INSIDE OF THE MAW, upper part: flat AMBER-OCHRE {MAU['ho_phach']}, no light streaks"),
          ("P_tou_1_05", f"SIDE WALL of the maw (a narrow curved piece): darker mud {MAU['bun_toi']} with a thin lighter mud rim"),
          ("P_tou_1_04", f"a short row of TEETH: rounded pale PEBBLE TEETH {MAU['rang']} on a thin mud gum"),
          ("P_yanjing_1", f"EYE FRAME (a thin dark frame round two small eyes): plain darker mud {MAU['bun_toi']}, keep the outline shape"),
          ("P_yanjing_2", f"TWO SMALL EYES: flat amber {MAU['mat']} with a small dark pupil and one small white dot each, no glow")],
}
TO_EN = {
    "P": "eighteen small parts of the two FISTS of the puppet, drawn big: two palms and sixteen finger segments",
    "X": "nine separate STRANDS of the puppet (long tendrils with a wide flat tip and a thick base)",
    "V": "three parts of a STRETCHED ARM of the puppet: a long upper arm tube, a fist, a very long forearm tube",
    "H": "the parts of the puppet's head morphed into a GIANT OPEN MAW: upper jaw, lower jaw / belly, two inside parts, a side piece, a "
         "short teeth strip, an eye frame and two small eyes",
}
TO_VI = {"P": "hai lòng bàn tay + 16 đốt ngón (phóng 2,4 lần)", "X": "chín xúc tu (phóng 1,7 lần)",
         "V": "tay co giãn: bắp tay, nắm đấm, ống cẳng tay (phóng 1,75 lần)", "H": "đầu hàm khổng lồ skill_04 + khung mắt, mắt"}


def vung():
    """{slot: (att, ảnh part cắt theo lưới)} cho MỌI hình trong att_goc (hình đầu tiên của mỗi slot)."""
    G._C.pop("att", None)
    G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in D["atts"]:
        if a.get("region") and a["slot"] not in out and a["region"] in G._C["imgs"]:
            out[a["slot"]] = (a, G.part_goc(a))
    return out


def to():
    V = vung()
    os.makedirs(G.MAU, exist_ok=True)
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for s, z in h_:
                im = V[s][1]
                cs.append((s, z, im, int(round(im.width * z)), int(round(im.height * z))))
            cao.append((cs, max(c[4] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        assert ke_y > 25, (ma, ke_y)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            assert ke > 25, (ma, ke)
            x = ke
            for s, z, im, cw, ch in cs:
                y0 = y + (hh - ch) // 2
                can.alpha_composite(im.resize((cw, ch), Image.LANCZOS), (x, y0))
                o[s] = dict(hop=[x, y0, cw, ch], z=z)
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    return O


def cho(o, s):
    x, y, cw, ch = o[s]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of separate PARTS of a 2D animation puppet, each part drawn alone on white. Redraw the SAME sheet "
    "with every part REPAINTED as described below, so that the parts can be put back on the same puppet. For EVERY part keep exactly: its "
    "silhouette (the same outline), its size, its orientation and its place on the sheet (if the new picture were laid over image 1, every "
    "part must coincide with the old one). Do NOT merge parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the parts.")
STYLE_D = (
    "NEW LOOK (see image 2, the approved picture of OUR character, for the exact colours, materials and drawing style): our MUD MONSTER. "
    "Hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {px} px) running all the way round every part exactly on its "
    "silhouette, thinner ink lines for the few inner lines, and every area filled with ONE flat colour with visible coloured-pencil / "
    "wax-crayon hatching. The parts of image 1 are painted in a smooth digital cel style with blue-grey goo, pink tips and glowing cyan: "
    "do NOT copy that painting style or those colours; no shading, no highlights, no gradients, no glow, no shadows: flat colour only.")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."


def prompt_d(O):
    out_lines = []
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out, save = luu(f"D_{ma}")
        p = os.path.join(GUI, f"luot_2_D_{ma}.txt")
        R = [(mau, f"the PARTS SHEET, 1536x1024, white background: {TO_EN[ma]}, each drawn alone at the exact size and place to keep."),
             (DUYET, "the APPROVED picture of OUR character, 1536x1024, white background: a hulking mud monster (chocolate-brown wet mud, "
                     "fists of big grey river stones, mud drips with round drops, amber-ochre inside of the mouth, pale pebble teeth, a "
                     "light-brown belly). Take from it ONLY the colours, the materials and the hand-drawn look (wobbly brown ink line, "
                     "crayon hatching, flat colour). Do NOT copy its shapes or its pose: the shapes come from image 1."),
             (VUON_NUI, "an approved hero of the same game, 1536x1024: the hand-drawn ink and crayon style to match. Do NOT copy its design.")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en) in enumerate(R, 1)]
        t += [""] + save + ["", CHUNG, "", STYLE_D.format(px="7" if ma == "P" else "6"), "",
                            "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        mt = dict(MO_TA[ma])
        t += [f"{i}. ({cho(o, s)}) {mt[s]}." for i, s in enumerate(o, 1)]
        t += ["", BG]
        ghi(p, t)
        out_lines.append((ma, TO_VI[ma], p, out))
        print(p)
    return out_lines


def huong_dan(T, D):
    gd = ["# Gói gen: quái bùn (`quai_bun`), tướng 8 đảo Thổ (ải 50)", "",
          "Con gốc của rig: `monster_3668` (game tham khảo). Ảnh part gốc trên các tờ D_* là của game đó: chỉ dùng trong máy, không đăng "
          "công khai. Ghi chú: `ArtGen/Spine/inbox/quai_bun_ghichu.md`.", "",
          "## Lượt 1: concept (xong, người dùng chọn A → `tai_ve/L1_duyet.png`)", "",
          "## Lượt 2: mảnh (Claude tự gen bằng Magnific GPT 2.6, 1k high, 95 credit / tờ: `py -3 -I ArtGen/Spine/gen_magnific.py <file>`)", "",
          f"Tờ T* (đúng chỗ, đúng cỡ trên concept): ảnh mẫu duy nhất là concept duyệt `{Wp(DUYET)}` (1536 × 1024, nền trắng, quái bùn nâu "
          "quay phải). Mỗi tờ vài mảnh không chạm nhau, vẽ đủ phần bị che.", ""]
    for nh, ds, p, out in T:
        gd += [f"- **{nh}** ({ds}): file prompt `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
    gd += ["", "Tờ D_* (theo khung part gốc): ảnh 1 = tờ part gốc cắt theo lưới (hình cel số xám lam, đầu xúc tu hồng, lòng miệng xanh "
           "sáng), ảnh 2 = concept duyệt (lấy màu, chất liệu), ảnh 3 = vượn núi đá (lấy nét).", ""]
    for ma, vi, p, out in D:
        gd += [f"- **D_{ma}** ({vi}; ảnh 1 = `{Wp(os.path.join(G.MAU, f'goc_{ma}.png'))}`): file prompt `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`."]
    gd += ["", "Kiểm: tờ T: mảnh trùng chỗ, cỡ với concept (`quai_bun_manh.py ghep`), phần che vẽ đủ, viền kín, đầu không mắt; tờ D: mỗi part "
           "trùng hình bóng part gốc (`cat` in IoU, dưới 0,9 thì gen lại), không còn xám lam / hồng / xanh sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"every part must stay at exactly the same place and size as in image 1\"; \"flat colour only, no shading\"; "
           "\"no pink, no cyan: mud brown, grey stones, amber inside only\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), gd)


# ================================================================ cắt
def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def nen(A, nguong=236):
    trang = (A.min(2) > nguong).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(G.TAI) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def khu_vien(rgb, mm, r=2):
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def rgba_tu(rgb, mm):
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    return Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")


def nap_dat():
    pd = os.path.join(MANH, "dat.json")
    return json.load(open(pd, encoding="utf-8")) if os.path.exists(pd) else {}


def ghi_dat(DATJ):
    os.makedirs(MANH, exist_ok=True)
    json.dump(DATJ, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)


def dong_lo(m, toi_da=6000):
    """đục giấy trắng khép kín (lỗ nhỏ giữa mảnh vẫn là thịt nếu nhỏ hơn toi_da px thì giữ; lỗ lớn là nền)."""
    inv = (~m).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    Hh, Ww = m.shape
    out = m.copy()
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            continue
        if a < toi_da:
            out |= lab == i
    return out


def cat_t(nh):
    DATJ = nap_dat()
    src = moi_nhat(f"M_{nh}")
    if not src:
        print(f"{nh}: chưa gen")
        return
    slots = [x for x, _, _ in NHOM[nh]]
    A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen(A)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    cum = [i for i in range(1, n) if st[i, 4] > 30]
    gan = {x: [] for x in slots}
    for i in cum:
        c = cen[i]
        best = min(slots, key=lambda x: np.hypot(c[0] - TAM[x][0], c[1] - TAM[x][1]))
        d = np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1])
        if (len(slots) == 1 and st[i, 4] > 400) or d < 300 or st[i, 4] > 20000:
            gan[best].append(i)
        else:
            print(f"  {nh}: bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {st[i, 4]} px")
    print(f"{nh} ({os.path.basename(src)}):")
    for x, ids in gan.items():
        if not ids:
            print(f"  {x:12s} KHÔNG THẤY MẢNH")
            continue
        m = np.isin(lab, ids)
        ys, xs = np.nonzero(m)
        x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
        im = rgba_tu(A[y0:y1, x0:x1].astype(np.uint8).copy(), m[y0:y1, x0:x1])
        os.makedirs(MANH, exist_ok=True)
        im.save(os.path.join(MANH, x + ".png"))
        DATJ[x] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=os.path.basename(src))
        big = max(ids, key=lambda i: st[i, 4])
        print(f"  {x:12s} hộp {(x0, y0, x1, y1)}, {len(ids)} cụm (to nhất {st[big, 4]} px)")
    ghi_dat(DATJ)


def cat_d(ma):
    src = moi_nhat(f"D_{ma}")
    if not src:
        print(f"D_{ma}: chưa gen")
        return
    V = vung()
    A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
    fg = ~nen(A, 238)
    fgG = ~nen(Gd, 238)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    pi = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pi)) if os.path.exists(pi) else {}
    so = []
    os.makedirs(os.path.join(MANH, "part"), exist_ok=True)
    print(f"D_{ma} ({os.path.basename(src)}):")
    for s, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 12
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(8)).astype(bool)
        sub = lab[y0:y1, x0:x1]
        ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 40]
        m = np.isin(lab, ids)
        m[:y0] = m[y1:] = False
        m[:, :x0] = m[:, x1:] = False
        m &= cv2.dilate(fgG.astype(np.uint8), el(10)).astype(bool)
        rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
        mm = m[y:y + ch, x:x + cw]
        b = fgG[y:y + ch, x:x + cw]
        # lỗ thủng của part gốc (khe giữa cánh tay và sợi bùn) giữ trong suốt: chỉ lấp lỗ nhỏ GPT để lọt trong mảnh
        mm = dong_lo(mm) & cv2.dilate(b.astype(np.uint8), el(3)).astype(bool)
        im = rgba_tu(rgb.copy(), mm)
        goc = V[s][1]
        tw, th = int(round(goc.width * RES)), int(round(goc.height * RES))
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
        out = Image.fromarray(a2, "RGBA")
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        cu = ious.get(s, 0.0)
        if iou >= cu - 0.005 or not os.path.exists(os.path.join(MANH, "part", s + ".png")):
            out.save(os.path.join(MANH, "part", s + ".png"))
            ious[s] = round(iou, 3)
            ghi_de = ""
        else:
            ghi_de = f" (giữ bản cũ {cu:.3f})"
        vis = np.full((ch, cw, 3), 255, np.uint8)
        vis[mm & b] = (170, 170, 170)
        vis[b & ~mm] = (230, 60, 60)
        vis[mm & ~b] = (60, 190, 60)
        so.append((Image.fromarray(vis), out))
        print(f"  {s:12s} IoU {iou:.3f}{ghi_de}")
    json.dump(ious, open(pi, "w"), indent=1)
    w_ = sum(max(v.width, k.width) + 10 for v, k in so)
    hh = max(v.height for v, _ in so)
    h2 = max(k.height for _, k in so)
    out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
    xx = 10
    for vis, kh in so:
        out.paste(vis, (xx, 10))
        out.paste(kh, (xx, hh + 20), kh)
        xx += max(vis.width, kh.width) + 10
    out.save(os.path.join(MANH, f"_so_{ma}.png"))
    print(os.path.join(MANH, f"_so_{ma}.png"))


def cat(chi=None):
    for nh in NHOM:
        if not chi or nh in chi:
            cat_t(nh)
    for ma in TO:
        if not chi or ma in chi:
            cat_d(ma)


# ================================================================ mắt, ghép
MAT_HOP = (1015, 410, 1145, 470)


def mat():
    """mắt mở cắt thẳng từ concept (bao lồi vùng vàng hổ phách + con ngươi, nới 5 px lấy vành mực); mắt nhắm: tô màu da mặt + một nét mực
    cong (mí khép) ngang giữa mỗi mắt."""
    DATJ = nap_dat()
    A = np.asarray(Image.open(DUYET).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = A[y0:y1, x0:x1]
    vang = (sub[..., 0] > 200) & (sub[..., 1] > 120) & (sub[..., 2] < 120) & (sub[..., 0] - sub[..., 2] > 110)
    vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, el(8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(vang, 8)
    ids = [i for i in range(1, n) if st[i, 4] > 40]
    m = np.zeros_like(vang)
    hulls = []
    for i in ids:
        ys, xs = np.nonzero(lab == i)
        hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        cv2.fillPoly(m, [hull], 1)
        hulls.append(hull.reshape(-1, 2) + np.array([x0, y0]))
    m = cv2.dilate(m, el(5)).astype(bool)
    full = np.zeros((H, W), bool)
    full[y0:y1, x0:x1] = m
    ys, xs = np.nonzero(full)
    hx0, hy0, hx1, hy1 = xs.min() - 3, ys.min() - 3, xs.max() + 4, ys.max() + 4
    im = rgba_tu(A[hy0:hy1, hx0:hx1].astype(np.uint8).copy(), full[hy0:hy1, hx0:hx1])
    os.makedirs(MANH, exist_ok=True)
    im.save(os.path.join(MANH, "mat.png"))
    DATJ["mat"] = dict(hop=[int(hx0), int(hy0), int(hx1), int(hy1)], nguon="L1_duyet.png (cắt thẳng)")
    print("mat", DATJ["mat"]["hop"], f"{len(ids)} cụm vàng")
    a = np.asarray(im).copy()
    vung_ = A[max(0, hy0 - 12):hy1 + 12, max(0, hx0 - 12):hx1 + 12].reshape(-1, 3)
    nau = vung_[(vung_[:, 0] > 95) & (vung_[:, 0] < 160) & (vung_[:, 2] < 80) & (vung_[:, 0] - vung_[:, 2] > 50)]
    da = np.median(nau, 0).astype(np.uint8) if len(nau) > 20 else np.array([125, 75, 51], np.uint8)
    al = a[..., 3] > 0
    trong = cv2.erode(al.astype(np.uint8), el(4)).astype(bool)
    a[trong, :3] = da
    can = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(can)
    for hull in hulls:
        hx = hull[:, 0] - hx0
        hy = hull[:, 1] - hy0
        xa, xb, ym = hx.min() + 1, hx.max() - 1, (hy.min() + hy.max()) / 2
        pts = [(xa + (xb - xa) * u, ym + 0.20 * (hy.max() - hy.min()) * np.sin(np.pi * u)) for u in np.linspace(0, 1, 12)]
        d.line(pts, fill=INK + (255,), width=5, joint="curve")
    can.save(os.path.join(MANH, "mat_nham.png"))
    DATJ["mat_nham"] = dict(hop=DATJ["mat"]["hop"], nguon=f"dựng từ mặt nạ mắt (tô da {da.tolist()} + mí)")
    ghi_dat(DATJ)


THU_TU = ["tay_xa_tren", "than", "tay_xa_duoi", "long_mieng", "ham", "dau", "mat", "vai_gan", "tay_gan"]


def ghep():
    DATJ = nap_dat()
    can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    thieu = []
    for x in THU_TU:
        if x not in DATJ:
            thieu.append(x)
            continue
        x0, y0, _, _ = DATJ[x]["hop"]
        can.alpha_composite(Image.open(os.path.join(MANH, x + ".png")).convert("RGBA"), (x0, y0))
    C = np.asarray(Image.open(DUYET).convert("RGB").resize((W, H))).astype(np.int32)
    Gp = np.asarray(can.convert("RGB")).astype(np.int32)
    a, b = ~nen(C), ~nen(Gp)
    iou = (a & b).sum() / max(1, (a | b).sum())
    so = np.full((H, W, 3), 255, np.uint8)
    so[a & b] = (175, 175, 175)
    so[a & ~b] = (230, 60, 60)
    so[b & ~a] = (60, 180, 60)
    out = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, im in enumerate([Image.fromarray(C.astype(np.uint8)), can.convert("RGB"), Image.fromarray(so)]):
        out.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    pp = os.path.join(MANH, "_ghep.png")
    out.save(pp)
    can.convert("RGB").save(os.path.join(MANH, "_ghep_to.png"))
    print(pp, f"IoU hình bóng {iou:.3f}", ("thiếu: " + ", ".join(thieu)) if thieu else "")


Y_DE, DE_THUA, DE_MO = 805, 18, 8     # px concept: mép trên vũng bùn; thân thừa xuống dưới mép; mép trên vũng bùn mờ dần


def tach_than():
    """như con gốc (thân P_shenti2 và vũng bùn P_shenti1_1..3 là mảnh rời, vũng bùn vẽ TRƯỚC thân): cắt mảnh than (một ảnh liền) thành
    than_sau (mọi điểm trên Y_DE + DE_THUA, mép dưới nấp sau vũng bùn) và vung_bun (dưới Y_DE, mép trên mờ dần DE_MO px trong lòng thân).
    Cùng một ảnh nên chỗ chồng trùng màu, không có nét nối; khi thân phình đè xuống vũng bùn (skill_04) thì đi SAU vũng bùn, không gập lưới."""
    DATJ = nap_dat()
    x0, y0, x1, y1 = DATJ["than"]["hop"]
    a = np.asarray(Image.open(os.path.join(MANH, "than.png")).convert("RGBA")).astype(np.float32)
    yy = (np.arange(a.shape[0]) + y0)[:, None].astype(np.float32)
    xx = (np.arange(a.shape[1]) + x0)[None, :].astype(np.float32)
    # đường tách: bên trái góc lõm (sườn thân gặp lưỡi vũng bùn ở ~(515, 800)) cả lưỡi vũng bùn và đoạn cuối sườn thuộc vũng bùn từ y 790;
    # bên phải tách ở Y_DE; chuyển trong x 525 → 545
    u = np.clip((xx - 525.0) / 20.0, 0, 1)
    yd = 780.0 * (1 - u) + Y_DE * u
    sau = a.copy()
    sau[..., 3] *= np.clip((yd + DE_THUA - yy) / 4.0, 0, 1)
    de = a.copy()
    de[..., 3] *= np.clip((yy - yd) / DE_MO, 0, 1)
    # cột thân lót (như P_shenti1 của họ vẽ sau thân): phần dưới thân (y 600 → mép vũng bùn, đủ bề ngang, giữ nét viền hai sườn), vẽ SAU
    # than_sau, bám cột thân P_shenti1: thân rướn cao / phình thì cột giãn lấp khoảng giữa thân và vũng bùn, góc lõm không hở
    lot = a.copy()
    yd_lot = 780.0 * (1 - u) + Y_DE * u                      # đáy cột lót KHÔNG hạ theo đường tách phía phải (ngoài lưới cột của họ thì văng)
    lot[..., 3] *= np.clip((yy - 600.0) / 40.0, 0, 1) * np.clip((yd_lot + DE_THUA + 30 - yy) / 6.0, 0, 1)
    for ten, b in (("than_sau", sau), ("vung_bun", de), ("than_lot", lot)):
        ys = np.flatnonzero(b[..., 3].max(1) > 1)
        c0, c1 = int(ys.min()), int(ys.max()) + 1
        Image.fromarray(b[c0:c1].astype(np.uint8), "RGBA").save(os.path.join(MANH, ten + ".png"))
        DATJ[ten] = dict(hop=[x0, y0 + c0, x1, y0 + c1], nguon=f"than.png tách ở y {Y_DE}")
        print(ten, DATJ[ten]["hop"])
    ghi_dat(DATJ)


def _lop_bun(a):
    """mặt nạ điểm màu bùn nâu (không mực, không đá xám, không hổ phách, không răng)."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (a[..., 3] > 0) & (r > 85) & (r < 200) & (r - b > 45) & (g < r - 20) & ((r - g) < (r - b))
    return m & ~((r > 200) & (g > 130))


def _lop_bung(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (a[..., 3] > 0) & (r > 150) & (r < 215) & (g > 100) & (g < 150) & (b > 50) & (b < 105)


def can_mau():
    """mỗi tờ Magnific tô một sắc nâu hơi khác: dời điểm màu bùn của từng mảnh khung part về trung vị bùn của thân (mảnh concept `than`),
    điểm màu bụng (hàm dưới khổng lồ) về trung vị bụng của `ham`. Ghi manh/part_can/ (rig ưu tiên dùng)."""
    A = lambda p: np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)  # noqa: E731
    th, hm = A(os.path.join(MANH, "than.png")), A(os.path.join(MANH, "ham.png"))
    chuan_bun = np.median(th[_lop_bun(th)][:, :3], 0)
    chuan_bung = np.median(hm[_lop_bung(hm)][:, :3], 0)
    ra = os.path.join(MANH, "part_can")
    os.makedirs(ra, exist_ok=True)
    for f in sorted(os.listdir(os.path.join(MANH, "part"))):
        a = A(os.path.join(MANH, "part", f))
        out = a.copy()
        msg = []
        s = f[:-4]
        lops = []
        if s.startswith(("G_", "P_shenti2_")) or s in ("P_shouL1_1", "P_shouR1_1", "P_shouR1_2", "P_shouR2_1", "P_shouR2_2", "P_shouL3",
                                                       "P_shouR3", "P_tou_1_01", "P_tou_1_05"):
            lops.append((_lop_bun, chuan_bun, "bùn"))
        if s == "P_tou_1_02":
            lops.append((_lop_bung, chuan_bung, "bụng"))
        for lop, chuan, ten in lops:
            m = lop(a)
            if m.sum() < 300:
                continue
            d = chuan - np.median(a[m][:, :3], 0)
            mm = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)[..., None]
            out[..., :3] = np.clip(out[..., :3] + mm * d, 0, 255)
            msg.append(f"{ten} {np.round(d).astype(int).tolist()}")
        Image.fromarray(out.astype(np.uint8), "RGBA").save(os.path.join(ra, f))
        if msg:
            print(f"  {f:20s} " + "; ".join(msg))
    print(f"chuẩn bùn {np.round(chuan_bun).astype(int).tolist()}, chuẩn bụng {np.round(chuan_bung).astype(int).tolist()}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can_mau":
        can_mau()
        sys.exit(0)
    if cmd == "tach_than":
        tach_than()
        sys.exit(0)
    if cmd == "to":
        O = to()
        huong_dan(prompt_t(), prompt_d(O))
    elif cmd == "cat":
        cat(sys.argv[2:] or None)
    elif cmd == "mat":
        mat()
    elif cmd == "ghep":
        ghep()
    else:
        print(__doc__)


# ================================================================ 3. tờ quả bóng + gai (người dùng 2026-11-17: chiêu cuối nuốt đối thủ, phồng
# thành quả bóng tròn mặt căng, gai đất đâm xuyên thân; appear cục đất tròn rơi, nảy, bung ra thành tướng)
B_TAM = {"bong_mat": (430, 520), "bong_dat": (930, 560), "gai_0": (1300, 300), "gai_1": (1300, 520), "gai_2": (1300, 740)}


def prompt_bong():
    out, save = luu("M_B1")
    p = os.path.join(GUI, "luot_3_bong.txt")
    t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {Wp(DUYET)}: {ANH1}",
         f"image 2 = {Wp(VUON_NUI)}: an approved hero of the same game, 1536x1024: the hand-drawn ink and crayon style to match. Do NOT copy "
         "its design.", ""] + save + ["",
         "TASK: draw FIVE separate objects for our mud monster of image 1 (same character, same colours, same hand-drawn style), each alone "
         "on a pure-white 1536x1024 canvas, with a clear white gap (at least 40 px) between them. Wobbly dark-brown ink outline (#2B2118, about "
         "7 px) all the way round every object, thinner ink lines for the few inner lines, every area ONE flat colour with visible "
         "coloured-pencil / wax-crayon hatching; no shading, no highlights, no gradients, no glow, no shadows.",
         "",
         "1. LEFT, big (about x 170-690, y 260-780, a circle about 520 px wide): THE MUD MONSTER OF image 1 SWOLLEN INTO A BIG ROUND BALL, "
         "as if it has just swallowed an enemy and is holding it inside its belly. The whole body is ONE round ball of chocolate-brown mud "
         f"{MAU['bun']} (a darker {MAU['bun_toi']} crescent along its lower-left edge), a big light-brown {MAU['bung']} round belly patch on its "
         "lower front. Its FACE is on the upper right of the ball, turned to the right like image 1: the thick lumpy overhanging brow ridge, the "
         "two short blunt grey river-stone horns on top of the ball, TWO amber eyes BULGING WIDE OPEN and strained (round, small dark pupils, "
         "one small white dot each), the MOUTH PRESSED TIGHTLY SHUT: a thick wavy lumpy line with puffed-out cheeks on both sides and one "
         "pale pebble tooth peeking out at one corner. The two big grey river-stone FISTS are small now, pressed against the lower left and "
         "lower right sides of the ball, as if holding the belly in. Two or three short mud drips with round drops on top of the ball. "
         "Straining, struggling to keep something inside, determined, a bit funny but fierce. No arms, no legs, no puddle.",
         "2. MIDDLE (about x 760-1110, y 380-740, a circle about 350 px wide): A PLAIN ROUND BALL OF WET EARTH AND MUD, the same chocolate "
         f"brown {MAU['bun']} with a darker {MAU['bun_toi']} crescent along its lower-left edge, three small grey river pebbles {MAU['da']} "
         "stuck in it and two short mud drips on top. NO face, no eyes, no mouth, no limbs.",
         "3. RIGHT COLUMN (about x 1150-1500), THREE EARTH SPIKES lying horizontally one under the other, each pointing to the RIGHT: a rough, "
         "slightly irregular cone of hard packed earth and stone, a wide broken base on the left, a long straight body and a SHARP TIP on the "
         f"right; flat sandy-grey stone {MAU['da']} with a darker {MAU['da_toi']} flat zone along its lower side and one or two facet lines. "
         "Spike A (top, about y 250-350) long: about 340 px long, 80 px thick at the base. Spike B (middle, about y 470-570) about 280 px "
         "long, 72 px thick. Spike C (bottom, about y 690-790) about 220 px long, 64 px thick.",
         "", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no numbers, no frame, no shadows, no sparkles."]
    ghi(p, t)
    print(p)


def cat_bong():
    src = moi_nhat("M_B1")
    if not src:
        print("M_B1: chưa gen")
        return
    DATJ = nap_dat()
    A = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen(A)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    gan = {k: [] for k in B_TAM}
    for i in range(1, n):
        if st[i, 4] < 30:
            continue
        c = cen[i]
        k = min(B_TAM, key=lambda q: np.hypot(c[0] - B_TAM[q][0], c[1] - B_TAM[q][1]))
        if st[i, 4] < 1500:                                  # giọt bùn rời bay quanh bóng: để VFX làm
            continue
        gan[k].append(i)
    for k, ids in gan.items():
        if not ids:
            print(f"  {k}: KHÔNG THẤY")
            continue
        m = np.isin(lab, ids)
        ys, xs = np.nonzero(m)
        x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(W, xs.max() + 4), min(H, ys.max() + 4)
        mm = dong_lo(m[y0:y1, x0:x1])
        rgba_tu(A[y0:y1, x0:x1].astype(np.uint8).copy(), mm).save(os.path.join(MANH, k + ".png"))
        DATJ[k] = dict(hop=[int(x0), int(y0), int(x1), int(y1)], nguon=os.path.basename(src))
        print(f"  {k:9s} hộp {(int(x0), int(y0), int(x1), int(y1))}, {len(ids)} cụm")
    ghi_dat(DATJ)


if __name__ == "__main__" and sys.argv[1:2] == ["bong"]:
    prompt_bong()
if __name__ == "__main__" and sys.argv[1:2] == ["cat_bong"]:
    cat_bong()
