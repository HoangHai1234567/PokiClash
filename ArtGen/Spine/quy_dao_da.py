# -*- coding: utf-8 -*-
"""Quỷ lửa cầm đao lớn (quy_dao, tướng thứ 7 đảo Hỏa): MẢNH cho rig reskin trên con gốc monster_3655 (skill pokiclash-spine-rig mục 23).

Ba loại mảnh:
  1. GIỮ DÁNG (thân, hai tay, chân, đai, bàn tay, ngón): tờ hướng dẫn là CHÍNH các mảnh gốc cắt theo lưới (phóng to); GPT chỉ đổi da theo
     concept đã duyệt, giữ hình bóng + đường cấu trúc → manh/<vùng>.png đúng khung ảnh vùng × RES, lắp NGUYÊN lưới của họ.
  2. BỜM LỬA + RÂU (lưới + chuỗi xương của họ, nhưng hình bóng của mình có thêm lưỡi lửa nhọn): tờ L, mỗi búi một ô ở tỉ lệ sơ đồ bố cục, hình
     bóng = búi của rig + lưỡi lửa (cùng hạt giống với sơ đồ đã dùng để gen concept), tô lửa ba vùng bằng mã → GPT vẽ lại sạch, giữ hình bóng.
  3. ĐỔI DÁNG, mảnh cứng (đao, mặt nạ, hai sừng, giáp vai): gen "ĐÚNG CHỖ, ĐÚNG CỠ" từ concept đã duyệt (vẽ đủ phần khuất), mỗi lượt vài mảnh
     không chồng nhau.
Loại 2, 3 ghi chỗ đặt vào manh/dat_moi.json (rig gắn bằng lưới dày của mình bám theo lưới của họ).
Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu cho GPT, không đăng công khai.

    quy_dao_da.py to        tờ mảnh gốc A, B + tờ lửa L + prompt mọi lượt → mau/, gui_gpt/quy_dao_1/luot_2_*.txt, HUONG_DAN.md (nối thêm)
    quy_dao_da.py cat       cắt tờ D_A, D_B → manh/<vùng>.png (+ _so_<tờ>.png, _iou.json)
    quy_dao_da.py cat_lua   cắt tờ D_L → manh/<slot>.png + dat_moi.json
    quy_dao_da.py cat_moi   cắt M_DAO, M_MAT, M_SUNG → manh/<slot>.png + dat_moi.json (phép đồng dạng ảnh → hệ rig)
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_dao as G  # noqa: E402
import quy_dao_bo_cuc as BC  # noqa: E402

W, H = 1536, 1024
RES = 2
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "quy_dao_1")
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
INK = (43, 33, 24)
DA, SAT, VAI, SUNG = "#CEC4BA", "#3A3840", "#7C2A26", "#1E1C21"
LUA = ("#E0441F", "#F7902A", "#FFD45A")

TO = {
    "A": [[("shenti", 2.2), ("dabi_r", 2.2), ("dabi_l", 2.2)],
          [("yao", 2.2), ("xiaobi_r", 2.2), ("xiaobi_l", 2.2), ("jiajia_l", 2.2)]],
    "B": [[("datui_l", 2.9), ("datui_r", 2.9), ("xiaotui_l", 2.9), ("xiaotui_r", 2.9), ("yaojia_02", 2.9), ("shou_r", 2.9)],
          [("yaojia_01", 2.9), ("yaojia_03", 2.9), ("yaojia_04", 2.9), ("yaojia_05", 2.9), ("tuishi_01", 2.9), ("tuishi_02", 2.9), ("shou_l", 2.9)]],
    "C": [[("shouzhi_01", 5.5), ("shouzhi_02", 5.5), ("shouzhi_03", 5.5), ("shouzhi_04", 5.5), ("shouzhi_05", 5.5), ("hsouzhitou", 5.5)],
          [("damuzhi_l", 5.5), ("s_01", 5.5), ("s_02", 5.5), ("s_03", 5.5)]],
}
LUA_O = [["toufa_01", "toufa_03", "toufa_02"], ["toufa_07", "toufa_06", "huzi"]]      # tờ L: hàng → búi
Z_LUA = 1.12                                                                          # phóng so với sơ đồ bố cục


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vung():
    """{vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}; kể cả hình không bật mặc định (s_01..s_03)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in sorted(D["atts"], key=lambda q: q["order"]):
        r = a.get("region")
        if r in imgs and r not in out:
            out[r] = (a, G.part_goc(a))
    return out


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


# ---------------------------------------------------------------- tờ mảnh gốc A, B
def to_goc():
    V = vung()
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o, cao = {}, []
        for h_ in hang:
            cs = [(r, z, V[r][1], int(round(V[r][1].width * z)), int(round(V[r][1].height * z))) for r, z in h_]
            cao.append((cs, max(c[4] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            if ke < 8:
                raise SystemExit(f"tờ {ma}: hàng quá rộng ({sum(c[3] for c in cs)} px)")
            x = ke
            for r, z, im, cw, ch in cs:
                y0 = y + (hh - ch) // 2
                can.alpha_composite(im.resize((cw, ch), Image.LANCZOS), (x, y0))
                o[r] = dict(hop=[x, y0, cw, ch], z=z)
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    return O


# ---------------------------------------------------------------- tờ lửa L: búi bờm + râu, hình bóng của rig + lưỡi lửa, tô ba vùng
def to_lua():
    SC, T0 = BC.khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(BC.ATT)
    by = {a["slot"]: a for a in atts}
    S2 = BC.S2
    cells = {}
    for sl in [s for h_ in LUA_O for s in h_]:
        al, _ = BC.lop(by[sl], T0)
        m = BC.bong(al, 3.5)
        if sl != "huzi":
            m = BC.them_luoi(m, T0, SC, sl)
        ys, xs = np.nonzero(m)
        pad = 10 * S2
        x0, y0, x1, y1 = xs.min() - pad, ys.min() - pad, xs.max() + pad, ys.max() + pad
        can = np.full((y1 - y0, x1 - x0, 3), 255, np.uint8)
        BC.to_lua(can, m[y0:y1, x0:x1], day=0.55 if sl == "huzi" else 1.0)
        im = Image.fromarray(can, "RGB").resize((int(round((x1 - x0) / S2 * Z_LUA)), int(round((y1 - y0) / S2 * Z_LUA))), Image.LANCZOS)
        cells[sl] = (im, x0 / S2, y0 / S2)                       # ảnh ô, góc trên trái của ô trên sơ đồ bố cục (px)
    g0 = T0(np.array([0.0, 0.0]))
    can = Image.new("RGB", (W, H), (255, 255, 255))
    o = {}
    cao = [max(cells[s][0].height for s in h_) for h_ in LUA_O]
    ke_y = (H - sum(cao)) // (len(cao) + 1)
    y = ke_y
    for h_, hh in zip(LUA_O, cao):
        ke = (W - sum(cells[s][0].width for s in h_)) // (len(h_) + 1)
        if ke < 8:
            raise SystemExit("tờ L: hàng quá rộng")
        x = ke
        for s in h_:
            im, bx, by_ = cells[s]
            y0 = y + (hh - im.height) // 2
            can.paste(im, (x, y0))
            # ô (x, y0) trên tờ ↔ thế giới rig: px tờ / Z_LUA + góc ô trên sơ đồ → (px sơ đồ − gốc) / SC
            o[s] = dict(hop=[x, y0, im.width, im.height], ti=1.0 / (SC * Z_LUA),
                        goc=[float((bx - g0[0]) / SC), float((g0[1] - by_) / SC)])
            x += im.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, "goc_L.png")
    can.save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


# ---------------------------------------------------------------- prompt
CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of the separate body PARTS of a 2D animation puppet (a hulking demon brute), each part drawn alone on "
    "white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same puppet. For "
    "EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet (if the new picture "
    "were laid over image 1, every part must coincide with the old one), and its main structural lines (the edges between plates, the "
    "lines between fingers, the edge where cloth or armour meets skin). Do NOT merge parts, do NOT add parts, do NOT move parts. Pure "
    "white (#FFFFFF) between the parts.")
STYLE = (
    "NEW LOOK (the same for all parts; see image 2, the approved picture of OUR character, for the exact colours and drawing style): an "
    "ASH-GREY FIRE DEMON. Hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {px} px) running all the way round every "
    "part exactly on its silhouette, thinner ink lines for the inner structural lines, and every area filled with ONE flat colour with "
    f"visible coloured-pencil / wax-crayon hatching. Colours: SKIN pale warm ash-grey ({DA}); ARMOUR (bracers, plates, knee caps, belt "
    f"pieces) black iron ({SAT}); CLOTH and leg wraps dark red ({VAI}); CLAWS black iron ({SAT}). The parts of image 1 are painted in a "
    "smooth digital cel style with salmon-red skin, glowing orange hexagon patterns, red runes on the armour and light / dark shading: "
    "do NOT copy that painting style, the red skin, the glowing patterns or the runes; no shading, no highlights, no gradients, no "
    "glow, no shadows, no cracks, no patterns: flat colour only, each area plain.")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."

MO_TA = {
    "A": [
        ("shenti", "CHEST (the biggest piece, two overlapping rounded masses): plain ash-grey skin; keep the one curved ink line where the "
                   "front mass overlaps the back one."),
        ("dabi_r", "NEAR UPPER ARM (a fat rounded muscle shape): plain ash-grey skin; remove the small glowing marks."),
        ("dabi_l", "FAR UPPER ARM (rounded): plain ash-grey skin."),
        ("yao", "BELLY (a rounded bowl shape): plain ash-grey skin."),
        ("xiaobi_r", "NEAR FOREARM WITH BRACER: the rounded forearm is ash-grey skin (remove the glowing hexagon pattern); the chunky "
                     "blocks wrapped around it are a BRACER of black iron: keep the edges of its blocks as ink lines, remove its red marks."),
        ("xiaobi_l", "FAR FOREARM (with a jagged torn edge at one end): plain ash-grey skin."),
        ("jiajia_l", "FAR ARM GUARD (a curved arc of armour plates with two hanging plates): black iron; keep the plate edges as ink lines; "
                     "remove the red rune lines."),
    ],
    "B": [
        ("datui_l", "FAR THIGH: where image 1 is red it is ash-grey skin; the dark ragged patches (torn shorts) become dark red cloth."),
        ("datui_r", "NEAR THIGH: the same: ash-grey skin, the dark ragged patches dark red cloth."),
        ("xiaotui_l", "FAR SHIN AND FOOT (small): dark red leg wrap."),
        ("xiaotui_r", "NEAR SHIN AND FOOT: dark red leg wrap; the blocks at its top black iron."),
        ("yaojia_02", "LOINCLOTH (a tapering block with a bright top): dark red cloth; its top part (bright yellow in image 1) becomes a "
                      "plain black-iron clasp."),
        ("shou_r", "BACK OF THE NEAR HAND (a rounded block): plain ash-grey skin; keep the knuckle lines."),
        ("yaojia_01", "BELT BUCKLE (a notched plate): black iron."),
        ("yaojia_03", "BELT PLATE: black iron."), ("yaojia_04", "BELT PLATE: black iron."), ("yaojia_05", "BELT PLATE: black iron."),
        ("tuishi_01", "KNEE CAP (a small block): black iron."), ("tuishi_02", "KNEE CAP: black iron."),
        ("shou_l", "FAR FIST (a fist with finger lines): ash-grey skin; keep the lines between the fingers."),
    ],
    "C": [
        ("shouzhi_01", "THUMB TIP of the near hand: ash-grey skin."),
        ("shouzhi_02", "FINGER with a claw: the finger ash-grey skin, the pointed claw at its tip (pale in image 1) black iron."),
        ("shouzhi_03", "FINGER with a claw: the same."), ("shouzhi_04", "FINGER with a claw: the same."),
        ("shouzhi_05", "FINGER with a claw: the same."),
        ("hsouzhitou", "FINGERTIP of the far hand: ash-grey skin."),
        ("damuzhi_l", "THUMB of the far hand, with a claw: ash-grey skin, the claw black iron."),
        ("s_01", "piece of the OPEN far hand: ash-grey skin, any claw tip black iron."),
        ("s_02", "piece of the OPEN far hand: the same."), ("s_03", "piece of the OPEN far hand: the same."),
    ],
}
VI = {"A": "ngực, bắp tay gần, bắp tay xa, bụng, cẳng tay gần liền bao tay, cẳng tay xa, giáp bắp tay xa",
      "B": "hai đùi, hai ống chân, khố, mu bàn tay gần; khoá đai, ba mảnh đai, hai giáp gối, nắm tay xa",
      "C": "ngón cái + bốn ngón vuốt tay gần, đầu ngón + ngón cái tay xa, ba mảnh bàn tay xa mở (phóng 5,5 lần)"}
KEEP_STYLE = ("the same wobbly dark-brown ink outline (#2B2118) and visible crayon hatching as image 1; completely flat colouring, no "
              "shading, no highlights, no glow, no shadow; pure-white background (#FFFFFF), no ground line, no text, no white border or "
              "sticker outline.")


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def prompt(O, OL):
    B = json.load(open(os.path.join(G.MAU, "bo_cuc.json"), encoding="utf-8"))
    gd = ["", "# Lượt 2: mảnh cho rig (2026-11-13, sau khi concept C sừng đen được chọn)", "",
          "Reskin trên con gốc `monster_3655`: tờ A, B là các mảnh GỐC cắt ra từ rig (phóng to), GPT vẽ lại da đúng chỗ, đúng cỡ, đúng hình bóng; "
          "tờ L là năm búi bờm lửa + râu (hình bóng của rig thêm lưỡi lửa, máy tô thô); M_DAO, M_MAT, M_SUNG là mảnh đổi dáng vẽ lại \"đúng chỗ, "
          "đúng cỡ\" từ concept. Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    ra = []
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out, save = luu(f"D_{ma}")
        p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: the separate body parts of the puppet, each drawn alone, at the exact size "
                   "and place to keep (" + ("seven big parts: chest, two upper arms, belly, forearm with bracer, forearm, a curved arm guard"
                                            if ma == "A" else "thirteen small parts in two rows: thighs, shins, loincloth, back of a hand; "
                                            "belt plates, knee caps, a fist" if ma == "B" else "ten very small finger and claw pieces of "
                                            "the two hands, drawn very big, in two rows") + ").",
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,2–5,5 lần: {VI[ma]}. Hình cel số da đỏ cam, giáp xám đen"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: an ash-grey fire demon with a mane of fire, a "
                       "black mask, black horns, black-iron armour, dark-red cloth and a giant dao. Take from it ONLY the colours, the "
                       "materials and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). Do NOT copy its shapes or "
                       "its pose: the shapes come from image 1.",
              "Concept đã duyệt của mình (bản C sừng đen, 1536 × 1024, nền trắng): chỉ lấy màu, chất liệu, nét vẽ tay")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += [""] + save + ["", CHUNG, "", STYLE.format(px={"A": "6", "B": "6", "C": "8"}[ma]), "",
                            "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        t += ["", BG]
        ghi(p, t)
        ra.append(p)
        gd += [f"## Tờ `{ma}`: {VI[ma]}", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)] + [""]
    # ---- tờ L
    mau = os.path.join(G.MAU, "goc_L.png")
    out, save = luu("D_L")
    p = os.path.join(GUI, "luot_2_lua_L.txt")
    ten = {"toufa_01": "the BIGGEST lock (the back of the mane, hanging low at the left)", "toufa_03": "a big lock from the top of the head",
           "toufa_02": "a big lock behind the shoulder", "toufa_07": "a lock over the top of the head", "toufa_06": "a small forelock",
           "huzi": "the short FIRE BEARD (small tongues pointing down-left)"}
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the FLAME SHEET, 1536x1024, white background: six separate flame shapes (the five locks of a mane of fire and "
         "a small beard of fire), each alone, coloured roughly by a computer in three nested zones (red-orange outside, orange, yellow "
         "inside) with a dark outline. Each shape is at the exact size, place and silhouette to keep.",
         f"image 2 = {Wp(CONCEPT)}: the APPROVED picture of OUR character (an ash-grey fire demon with a mane of fire), 1536x1024, white "
         "background: see how its fire mane is drawn (three flat colour zones with wavy flame-like borders, wobbly brown ink outline, crayon "
         "hatching, no glow). Take ONLY the colours and the drawing style of the fire from it."] + [""] + save + [
         "", "TASK: redraw image 1 as the SAME sheet, clean and hand-drawn: six separate FLAME pieces. For EVERY piece keep exactly its "
         "silhouette (the same outline with the same pointed tongues), its size, its orientation and its place on the sheet (if the new "
         "picture were laid over image 1, every piece must coincide with the old one). Do NOT merge pieces, do NOT add pieces or loose "
         "sparks, do NOT move pieces. Pure white between the pieces.", "",
         "EACH PIECE is one closed flame shape with a wobbly dark-brown ink outline (#2B2118, about 6 px) all the way round its silhouette, "
         f"filled with three nested flat colour zones that follow the shape: red-orange ({LUA[0]}) along the outer edge, orange ({LUA[1]}), "
         f"and a big yellow ({LUA[2]}) zone inside; the borders between the zones are wavy like flame tongues (no ink lines inside, at most a "
         "thin red-orange line between zones); visible crayon hatching. Flat colour only: NO glow, NO halo, NO gradients, NO white core, no "
         "shadow.", "", "THE PIECES (pixels on the 1536x1024 sheet):"]
    t += [f"{i}. ({cho(OL, s)}) {ten[s]}." for i, s in enumerate([s for h_ in LUA_O for s in h_], 1)]
    t += ["", BG]
    ghi(p, t)
    ra.append(p)
    gd += ["## Tờ `L`: năm búi bờm lửa + râu lửa", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}`.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
           f"| 1 | `{Wp(mau)}` | Tờ lửa máy tô (1536 × 1024, nền trắng): sáu hình lửa rời (năm búi bờm, một chòm râu), ba vùng màu đỏ cam / cam / vàng, viền sẫm |",
           f"| 2 | `{Wp(CONCEPT)}` | Concept đã duyệt: lấy cách vẽ lửa |", ""]
    # ---- mảnh đổi dáng "đúng chỗ, đúng cỡ" từ concept
    dao, S = B["dao"], B["slot"]
    MOI = {
        "M_DAO": ("the GIANT DAO (the huge single-edged chopping sabre on the demon's back)",
                  f"the WHOLE weapon alone, as one straight object about {dao['dai_px']} px long, lying along the same line as in image 1: the "
                  f"ring pommel at the top at about ({dao['chuoi'][0]}, {dao['chuoi'][1]}), the long wrapped handle running down-right, the "
                  f"small oval hand guard at about ({dao['chan'][0]}, {dao['chan'][1]}), and the blade running on to its tip at about "
                  f"({dao['mui'][0]}, {dao['mui'][1]}). In image 1 the middle of the weapon is hidden behind the fire mane, the head, the "
                  "body and the hands: DRAW IT COMPLETE. The handle is one straight wrapped bar from the ring pommel to the guard, with NO "
                  "hand on it. The blade starts at the guard about as wide as the guard and gets steadily wider toward the tip, exactly "
                  "continuing the part of the blade that is visible in image 1: thick straight back on the upper-right side with its one "
                  "square notch near the tip, the cutting edge on the lower-left side with its orange heated band running along the WHOLE "
                  "edge from the guard to the tip, the slanted clipped end. Same colours as in image 1.",
                  "the fire mane, the head, the horns, the body, both arms and hands, the legs: everything except the weapon",
                  "Đao trọn cây (khâu tròn, cán quấn, chắn tay, bản đao đủ từ chắn tay tới mũi), không có bàn tay"),
        "M_MAT": ("the MASK and the SHOULDER GUARD",
                  f"TWO separate pieces, each alone and COMPLETE: (1) the black demon MASK (about x = {S['lian_01'][0]} to x = {S['lian_01'][2]}, "
                  f"y = {S['lian_01'][1]} to y = {S['lian_01'][3]}) with its three-point crest and its two yellow eyes; in image 1 its lower "
                  "edge is hidden by the fire beard and its sides by the horns: draw the whole mask, the cheeks narrowing down to a pointed "
                  "chin, closed ink outline, NO mouth, no horns on it, no fire. (2) the round black-iron SHOULDER GUARD (about x = "
                  f"{S['jianjia'][0]} to x = {S['jianjia'][2]}, y = {S['jianjia'][1]} to y = {S['jianjia'][3]}) with its rim band, its round "
                  "boss and its one curved spike: draw it complete as one closed shape.",
                  "the fire mane, the beard, both horns, the body, the arms, the legs, the weapon: everything except those two pieces",
                  "Mặt nạ trọn (mào ba mũi, hai mắt vàng, cằm nhọn, không miệng) và giáp vai trọn (vành, núm, một gai)"),
        "M_SUNG": ("the TWO HORNS",
                   "TWO separate pieces, each alone and COMPLETE, and both RECOLOURED: if the horns are dark red in image 1, draw them DEEP "
                   "BLACK instead: one flat, very dark charcoal black (#1E1C21) over the whole horn, base and tip alike, no red, no "
                   "lighter base, no bands. (1) the big NEAR horn, from its thick base at about "
                   f"({B['sung_gan']['goc'][0]}, {B['sung_gan']['goc'][1]}) to its sharp tip; in image 1 its base touches the mask: draw the "
                   "base complete, ending in a rounded closed end. (2) the smaller FAR horn at the right of the mask, base at about "
                   f"({B['sung_xa']['goc'][0]}, {B['sung_xa']['goc'][1]}); in image 1 its base is hidden behind the mask: draw it complete "
                   "with a rounded closed base. Both deep black, flat, with a closed ink outline.",
                   "the mask, the fire mane, the beard, the shoulder guard, the body, the arms, the legs, the weapon: everything except the two horns",
                   "Hai sừng đen trọn (gốc bo tròn kín)"),
    }
    for ma, (la_gi, ve, bo, vi) in MOI.items():
        out, save = luu(ma)
        p = os.path.join(GUI, f"luot_2_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: the APPROVED picture of OUR character (an ash-grey fire demon with a mane of fire, a black mask, black "
             "horns, a round black-iron shoulder guard and a giant dao on its back, facing right), 1536x1024, white background. It is the "
             "picture to redraw from."] + [""] + save + [
             "", f"TASK: redraw image 1 with ONLY {la_gi}, in the SAME POSITION and at the SAME SIZE as in image 1 (same canvas 1536x1024; if "
             "the new picture were laid over image 1, the visible parts of these pieces must coincide), on a pure-white background.", "",
             f"DRAW: {ve}", "", f"REMOVE (leave pure white): {bo}.", "",
             "Every piece is ONE CLOSED SHAPE with a complete ink outline all the way round, drawn in exactly the look of image 1: "
             + KEEP_STYLE]
        ghi(p, t)
        ra.append(p)
        gd += [f"## `{ma}`: {vi}", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(CONCEPT)}` | Concept đã duyệt (1536 × 1024, nền trắng): quỷ lửa da tro, bờm lửa, mặt nạ + sừng đen, giáp vai vòm, đao lớn sau lưng |", ""]
    gd += ["## Kiểm lượt 2", "",
           "- Tờ A, B, L: mỗi mảnh ĐÚNG chỗ, đúng cỡ, đúng hình bóng (chồng lên tờ hướng dẫn phải trùng); đủ số mảnh, không dính nhau; da tro, "
           "giáp sắt đen, vải đỏ sẫm, vuốt đen; không còn da đỏ cam, hoa văn lục giác, chữ rune; tô phẳng.",
           "- M_*: mảnh nằm đúng chỗ như trên concept, vẽ đủ phần khuất, viền kín, mọi thứ khác đã xoá trắng.", "",
           "Cắt: `py -3 -I ArtGen/Spine/quy_dao_da.py cat`, `cat_lua`, `cat_moi`.", "",
           "| Sai | Gửi thêm (`--note`) |", "|---|---|",
           "| Mảnh lệch chỗ / đổi cỡ | `Every part must stay at exactly the same place and size as in image 1; lay your picture over image 1 and check.` |",
           "| Còn da đỏ, hoa văn sáng, rune | `Remove every red skin colour, glowing pattern and rune: plain ash-grey skin, plain black iron.` |",
           "| Tô khối, có bóng | `Flat colour only: no shading bands, no highlights, no gradients.` |"]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n# Lượt 2: mảnh cho rig")[0].rstrip("\n") if os.path.exists(hd) else ""
    ghi(hd, [cu] + gd)
    for p in ra:
        print(p)


# ---------------------------------------------------------------- cắt
def nen(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def khu_vien(rgb, mm, r=2):
    """dải mép r px của mảnh lấy màu TỐI NHẤT quanh nó (nét mực / màu mảnh): điểm khử răng cưa pha giấy trắng ở mép để lại viền sáng mảnh
    quanh mảnh sẫm (sừng đen, đao) khi đặt lên nền khác."""
    mm = mm.astype(bool)
    toi = cv2.erode(rgb, np.ones((2 * r + 1, 2 * r + 1), np.uint8))
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(r)).astype(bool)
    ngoai = cv2.dilate(mm.astype(np.uint8), el(2)).astype(bool) & ~mm
    out = rgb.copy()
    out[vien | ngoai] = toi[vien | ngoai]
    return out


def moi_nhat(tien_to):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(tien_to) and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def doc(p):
    return np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)


def o_ra(A, lab, st, fgG, d, pad=14):
    """mảnh trong ô d["hop"]: cụm liền nào chạm hình bóng tờ hướng dẫn (nới 10 px) thì lấy; trả RGBA đúng khung ô + mặt nạ."""
    x, y, cw, ch = d["hop"]
    x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
    gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
    sub = lab[y0:y1, x0:x1]
    ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
    m = np.isin(lab, ids)
    m[:y0] = m[y1:] = False
    m[:, :x0] = m[:, x1:] = False
    rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
    mm = m[y:y + ch, x:x + cw]
    rgb = khu_vien(rgb, mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = rgb.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    return Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA"), mm


def to_so(so, p):
    w_ = sum(max(s[0].width, s[1].width) + 10 for s in so)
    hh, h2 = max(s[0].height for s in so), max(s[1].height for s in so)
    out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
    xx = 10
    for vis, kh in so:
        out.paste(vis, (xx, 10))
        out.paste(kh, (xx, hh + 20), kh)
        xx += max(vis.width, kh.width) + 10
    out.save(p)
    print(p)


def cat():
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pi = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pi)) if os.path.exists(pi) else {}
    for ma in TO:
        src = moi_nhat(f"D_{ma}")
        if not src:
            print(f"tờ {ma}: chưa gen")
            continue
        A = doc(src)
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg, fgG = ~nen(A), Gd.min(2) < 238
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        for r, d in o.items():
            im, mm = o_ra(A, lab, st, fgG, d)
            x, y, cw, ch = d["hop"]
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            a2 = np.asarray(im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            a2[..., 3] = np.where(cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool), a2[..., 3], 0)      # giữ trong hình bóng gốc nới 3 px
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[mm & b] = (170, 170, 170)
            vis[b & ~mm] = (230, 60, 60)
            vis[mm & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), Image.fromarray(a2, "RGBA")))
            print(f"  {r:12s} IoU {iou:.3f}")
        to_so(so, os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(pi, "w"), indent=1)


def dat_moi(cap):
    p = os.path.join(MANH, "dat_moi.json")
    D = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    D.update(cap)
    json.dump(D, open(p, "w", encoding="utf-8"), indent=1)


def cat_lua():
    os.makedirs(MANH, exist_ok=True)
    src = moi_nhat("D_L")
    A = doc(src)
    o = json.load(open(os.path.join(G.MAU, "goc_L.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, "goc_L.png")).convert("RGB")).astype(np.int32)
    fg, fgG = ~nen(A), Gd.min(2) < 238
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    so, cap = [], {}
    for s, d in o.items():
        im, mm = o_ra(A, lab, st, fgG, d, pad=20)
        x, y, cw, ch = d["hop"]
        im.save(os.path.join(MANH, s + ".png"))
        b = fgG[y:y + ch, x:x + cw]
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        vis = np.full((ch, cw, 3), 255, np.uint8)
        vis[mm & b] = (170, 170, 170)
        vis[b & ~mm] = (230, 60, 60)
        vis[mm & ~b] = (60, 190, 60)
        so.append((Image.fromarray(vis), im))
        cap[s] = dict(anh=s, goc=d["goc"], ti=d["ti"], px=0.62, buoc=24.0)
        print(f"  {s:10s} IoU {iou:.3f}")
    to_so(so, os.path.join(MANH, "_so_L.png"))
    dat_moi(cap)


# mảnh đổi dáng: tờ → [(slot rig, tâm ước chừng trên concept để nhận cụm)]
MOI_SLOT = {"M_DAO": ["wuqi_02"], "M_MAT": ["lian_01", "jianjia"], "M_SUNG": ["dajiao_r", "dajiao_l"]}


def the_gioi_mau():
    """hình của MÌNH trong hệ rig (như sơ đồ bố cục): khung từng mảnh đổi dáng + hai điểm mốc của đao."""
    B = json.load(open(os.path.join(G.MAU, "bo_cuc.json"), encoding="utf-8"))
    sc, g0 = float(B["_sc"]), B["_goc"]
    hop = {s: [(b[0] - g0[0]) / sc, (g0[1] - b[3]) / sc, (b[2] - g0[0]) / sc, (g0[1] - b[1]) / sc] for s, b in B["slot"].items()}   # x0, y0, x1, y1 (y lên)
    G._C.pop("att", None)
    _, _, atts = G.nap(BC.ATT)
    V = np.array(next(a for a in atts if a["slot"] == "wuqi_02")["xy"], float).reshape(-1, 2)
    chuoi, mui = (V[1] + V[2]) / 2, (V[0] + V[3]) / 2
    Ld = float(np.linalg.norm(mui - chuoi))
    ax = (mui - chuoi) / Ld
    song = np.array([-ax[1], ax[0]])
    ku, _, kr = BC.DAO_KHAU
    return hop, dict(dau_chuoi=chuoi + ax * ((ku - kr) * Ld), mui=chuoi + ax * Ld + song * (-0.062 * Ld))


def cat_moi():
    """mỗi mảnh đổi dáng: cắt cụm của nó trên tờ M_*, đặt vào rig bằng phép đồng dạng ảnh → thế giới (dat_moi.json "M"):
    - đao: hai điểm (mép ngoài khâu tròn ở chuôi, mũi đao) ↔ đúng hai điểm đó của đao trên rig (khớp trục, chiều dài của rig);
    - mảnh khác: khung bao ↔ khung bao của mảnh đó trên sơ đồ bố cục (tỉ lệ đều, tâm trùng tâm). Concept vẽ to hơn sơ đồ ~15 %."""
    os.makedirs(MANH, exist_ok=True)
    B = json.load(open(os.path.join(G.MAU, "bo_cuc.json"), encoding="utf-8"))
    hopW, dao = the_gioi_mau()
    cap = {}
    for ma, slots in MOI_SLOT.items():
        src = moi_nhat(ma)
        if not src:
            print(f"{ma}: chưa gen")
            continue
        A = doc(src)
        fg = ~nen(A)
        fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1))
        n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
        big = [i for i in range(1, n) if st[i, 4] > 1500]
        k_c = 1.15                                                   # concept so với sơ đồ (ước chừng, chỉ để nhận cụm)
        gc = np.array([(B["_khung"][0] + B["_khung"][2]) / 2, (B["_khung"][1] + B["_khung"][3]) / 2])
        for s in slots:
            hx = B["slot"][s]
            c0 = gc + (np.array([(hx[0] + hx[2]) / 2, (hx[1] + hx[3]) / 2]) - gc) * k_c
            if not big:
                print(f"  {s}: không thấy cụm nào")
                continue
            i = min(big, key=lambda i: np.hypot(*(cen[i] - c0)) - 0.25 * np.sqrt(st[i, 4]))
            big.remove(i)
            m = lab == i
            m = cv2.dilate(m.astype(np.uint8), el(12)).astype(bool) & fg.astype(bool) | m      # mẩu rời sát mảnh nhập vào
            x, y, w, h = cv2.boundingRect(m.astype(np.uint8))
            x, y = max(0, x - 4), max(0, y - 4)                       # chừa 4 px trong suốt quanh mảnh (mép ảnh chạm mảnh thì atlas lem điểm ảnh bên cạnh)
            w, h = min(W - x, w + 8), min(H - y, h + 8)
            rgb = A[y:y + h, x:x + w].astype(np.uint8)
            mm = cv2.morphologyEx(m[y:y + h, x:x + w].astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
            cs, _ = cv2.findContours(mm.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            day = np.zeros(mm.shape, np.uint8)
            cv2.drawContours(day, cs, -1, 1, -1)                                                 # lấp lỗ trắng kín trong mảnh
            if s == "wuqi_02":                                                                   # lòng khâu tròn ở chuôi phải rỗng (lỗ giấy trắng)
                lo = day.astype(bool) & (rgb.min(2) > 232)                                  # giấy trắng khép kín trong khâu (nen() chỉ bỏ trắng nối mép ảnh)
                nn, ll, ss, cc = cv2.connectedComponentsWithStats(lo.astype(np.uint8), 4)
                for j in range(1, nn):
                    if ss[j, 4] > 120:
                        day[ll == j] = 0
            rgb = khu_vien(rgb, day)
            al = cv2.GaussianBlur(day.astype(np.float32), (0, 0), 0.8)
            vien = day.astype(bool) & ~cv2.erode(day, el(2)).astype(bool)
            sang = rgb.min(2).astype(np.float32)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            im.save(os.path.join(MANH, s + ".png"))
            ys, xs = np.nonzero(cv2.drawContours(np.zeros(mm.shape, np.uint8), cs, -1, 1, -1))
            if s == "wuqi_02":
                P = np.stack([xs, ys], 1).astype(float)
                c = P.mean(0)
                _, _, vt = np.linalg.svd(P - c, full_matrices=False)
                d = vt[0]
                t = (P - c) @ d
                nrm = (P - c) @ np.array([-d[1], d[0]])
                lo_, hi_ = t.min(), t.max()
                Lp = hi_ - lo_
                r_lo, r_hi = np.ptp(nrm[t < lo_ + 0.3 * Lp]), np.ptp(nrm[t > hi_ - 0.3 * Lp])
                if r_lo > r_hi:                                       # đầu rộng là bản đao: cho t tăng về phía mũi
                    t = -t
                z1 = P[np.argmin(t)]                                  # mép ngoài khâu tròn
                z2 = P[np.argmax(t)]                                  # mũi đao
                w1, w2 = dao["dau_chuoi"], dao["mui"]
                za, zb = complex(z1[0], -z1[1]), complex(z2[0], -z2[1])
                a_ = (complex(*w2) - complex(*w1)) / (zb - za)
                b_ = complex(*w1) - a_ * za
                M = [[a_.real, a_.imag, b_.real], [a_.imag, -a_.real, b_.imag]]
                ghi_ = f"hai điểm chuôi {z1.round()} → mũi {z2.round()}, tỉ lệ {abs(a_):.3f} đơn vị/px, xoay {np.degrees(np.angle(a_)):.1f}°"
            else:
                x0, y0, x1, y1 = hopW[s]
                pw, ph = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
                sc_ = float(min((x1 - x0) / pw, (y1 - y0) / ph))            # không to hơn khung của mảnh trên sơ đồ (concept vẽ khác tỉ lệ ngang / dọc)
                cx, cy = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
                wx, wy = (x0 + x1) / 2, (y0 + y1) / 2
                neo = "tâm khung"
                if s == "lian_01":                                   # mặt nạ: neo theo HAI MẮT (vàng) ↔ giữa hai mắt trên rig
                    vang = day.astype(bool) & (rgb[..., 0] > 200) & (rgb[..., 1] > 150) & (rgb[..., 2] < 120)
                    if vang.sum() > 40:
                        yy, xx = np.nonzero(vang)
                        cx, cy = float(xx.mean()), float(yy.mean())
                        wx, wy = float(np.mean([m_[0][0] for m_ in BC.MAT])), float(np.mean([m_[0][1] for m_ in BC.MAT]))
                        neo = "hai mắt"
                elif s == "jianjia":                                 # giáp vai: đáy vòm ↔ đáy khung, giữa theo bề ngang
                    cy, wy = float(ys.max()), y0
                    neo = "đáy vòm"
                elif s == "dajiao_r":                                # sừng gần: GỐC sừng ↔ mép trên trái mặt nạ (neo theo mũi thì gốc phủ lên mắt)
                    sc_ = min(sc_, 1.08)
                    day_ = ys > ys.max() - 0.10 * ph
                    cx, cy = float(xs[day_].mean()), float(ys[day_].mean())
                    wx, wy = 152.0, 486.0
                    neo = "gốc sừng"
                elif s == "dajiao_l":                                # sừng xa: mũi nhọn ↔ mũi sừng trên rig (gốc nấp sau mặt nạ)
                    sp = BC.SUNG_XA
                    cx, cy = float(xs[ys == ys.min()].mean()), float(ys.min())
                    wx, wy = float(sp["p"][2][0]), float(sp["p"][2][1])
                    neo = "mũi sừng"
                M = [[sc_, 0.0, wx - sc_ * cx], [0.0, -sc_, wy + sc_ * cy]]
                ghi_ = f"khung {pw}×{ph} px ↔ {x1 - x0:.0f}×{y1 - y0:.0f} đơn vị, tỉ lệ {sc_:.3f} (ngang {(x1 - x0) / pw:.3f}, dọc {(y1 - y0) / ph:.3f}), neo {neo}"
            cap[s] = dict(anh=s, M=M, px=0.62 if s == "wuqi_02" else 0.72, buoc=60.0 if s == "wuqi_02" else 40.0)
            print(f"  {s:10s} cụm {w}×{h} ở ({x}, {y})  ← {os.path.basename(src)}; {ghi_}")
    dat_moi(cap)


if __name__ == "__main__":
    cmd = sys.argv[1:2]
    if cmd == ["to"]:
        os.makedirs(G.MAU, exist_ok=True)
        os.makedirs(GUI, exist_ok=True)
        prompt(to_goc(), to_lua())
    elif cmd == ["cat"]:
        cat()
    elif cmd == ["cat_lua"]:
        cat_lua()
    elif cmd == ["cat_moi"]:
        cat_moi()
    else:
        print(__doc__)
