# -*- coding: utf-8 -*-
"""Voọc Tướng DẠNG 1 (kiem_si_non, khỉ voọc con không giáp, kiếm cũ cùn trong vỏ gỗ; concept duyệt 2026-11-13: tai_ve/L3_bao_go.png): mảnh.

Dạng 1 dùng CHUNG rig với dạng lớn (kiem_si_1). Mảnh lấy từ inbox/kiem_si_1/manh:
- ĐỔI MÀU bằng mã (giữ hình bóng, nét, vân): mọi mảnh LÔNG (than → xám của concept) và DA (bàn tay, bàn chân: nâu → hồng của concept).
  Mỗi mảnh đo trung vị màu của chính nó rồi nhân theo kênh cho trung vị về màu chuẩn; điểm mực (tối) và điểm kem (sáng) giữ nguyên.
- VẼ MỚI (ba tờ gen, mỗi ô là hình bóng của mảnh cũ, cùng khung ảnh để rig đặt đúng chỗ):
  tờ N1: đầu chibi có khăn trán (khung cũ nới lên trên cho đỉnh đầu tròn + chỏm tóc), hai đuôi khăn (thay hai lá mào, cùng chuỗi xương có lò xo),
         đai dây leo (thay đai thừng);
  tờ N2: hai cẳng tay lông (thay bao tay tre: giữ đúng hình bóng cho hai khớp), hai ống chân lông (thay giáp ống), váy lá (thay váy vải; khung
         cao sẵn bằng váy đã kéo dài của rig nên không bị giãn dọc);
  tờ S : vỏ gỗ, lưỡi cùn, chuôi quấn vải + kiếm cách gỗ (ngang, mũi bên trái như dạng lớn; giữ đúng bề ngang để rig đặt theo trục kiếm).
Không dùng: tấm vai, tua, giáp ngực, mũ, áo tơi, kiếm ngắn (rig dạng 1 bỏ hẳn slot).

    kiem_si_non_manh.py doi_mau     chép mảnh dạng lớn → inbox/kiem_si_non/manh (đổi màu lông, da) + dat.json
    kiem_si_non_manh.py to          ba tờ hướng dẫn mau/to_N1.png, to_N2.png, to_S.png (+ .json) và prompt gui_gpt/kiem_si_non/luot_4_*.txt
    kiem_si_non_manh.py cat         cắt tai_ve/N1.png, N2.png, S.png → manh/<tên>.png, sửa dat.json, tờ so manh/_so_moi.png
"""
import json
import math
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["KS_DANG"] = "1"
import kiem_si_manh as KM  # noqa: E402

LON = os.path.join(HERE, "inbox", "kiem_si_1", "manh")
BASE = os.path.join(HERE, "inbox", "kiem_si_non")
MANH = os.path.join(BASE, "manh")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
PK = os.path.join(HERE, "gui_gpt", "kiem_si_non")
DUYET = os.path.join(TAI, "L3_bao_go.png")
KIEM_TRAN = os.path.join(TAI, "L2_kiem_cun_6f6a63.png")      # concept có lưỡi cùn lộ ra (mẻ, gỉ, mũi gãy tròn)
W, H = 1536, 1024
INK = (43, 33, 24)

LONG = (119, 110, 102)          # lông xám của concept (đo trên L3_bao_go)
DA = (253, 173, 129)            # da mặt, tay, chân của concept
KEM = (244, 231, 200)
MAU_LONG = ["kp_gu", "kp_lung", "kp_bung", "kp_khuyu_x", "kp_bap_x", "kp_than", "kp_co", "kp_khuyu_g", "kp_bap_g", "than", "duoi", "dui1", "dui2"]
MAU_DA = ["kp_r31", "kp_r32", "kp_r33", "kp_r34", "kp_l31", "kp_l32", "kp_l33", "kp_l34", "ban_s", "ban_t"]

# mảnh vẽ mới: tên → (tờ, phóng, nới khung (trái, trên, phải, dưới) theo px ảnh cũ, màu tô hình bóng, kiểu)
# kiểu: "chat" giữ đúng hình bóng; "dau" hình bóng cũ làm mốc, được tràn lên vùng nới; "tu_do" hình hướng dẫn tự dựng (đuôi khăn)
MOI = {
    "dau": ("N1", 1.45, (20, 110, 20, 10), LONG, "dau"),
    "duoi_khan1": ("N1", 1.45, None, (95, 175, 90), "tu_do"),
    "duoi_khan2": ("N1", 1.45, None, (95, 175, 90), "tu_do"),
    "dai": ("N1", 1.3, (10, 10, 10, 10), (110, 154, 62), "chat"),
    "cang_g": ("N2", 1.55, (8, 8, 8, 8), LONG, "chat"),
    "cang_x": ("N2", 1.55, (8, 8, 8, 8), LONG, "chat"),
    "ong_s": ("N2", 1.55, (8, 8, 8, 8), LONG, "chat"),
    "ong_t": ("N2", 1.55, (8, 8, 8, 8), LONG, "chat"),
    "vay": ("N2", 1.3, (10, 10, 10, 24), (95, 168, 88), "vay"),
    "vo_a": ("S", 1.3, (0, 30, 0, 30), (162, 123, 84), "chat"),
    "luoi_a": ("S", 1.3, (0, 25, 0, 25), (154, 149, 138), "chat"),
    "chuoi_a": ("S", 1.3, (0, 70, 0, 70), (201, 180, 138), "chuoi"),   # nới ĐỀU trên dưới: trục kiếm ở giữa ảnh
}
# đuôi khăn: ảnh dọc, gốc (nút buộc) ở đáy giữa, ngọn ở đỉnh (như ảnh lá mào cũ: rig đặt chuỗi xương từ gốc tới ngọn)
KHAN = {"duoi_khan1": (120, 330), "duoi_khan2": (104, 270)}
VAY_TREN = 662                  # như kiem_si_rig.VAY_TREN: mép trên váy kéo dài tới đây (px concept dạng lớn)
XEP = {"N1": [["dau", "duoi_khan1", "duoi_khan2", "dai"]], "N2": [["cang_g", "cang_x", "vay"], ["ong_s", "ong_t"]],
       "S": [["vo_a"], ["luoi_a"], ["chuoi_a"]]}


def trung_vi(a, m):
    px = a[m][:, :3].astype(float)
    L = px @ np.array([0.299, 0.587, 0.114])
    px = px[(L > np.percentile(L, 30)) & (L < np.percentile(L, 85))]
    return np.median(px, 0)


def doi_mot(src, dst, dich, sang_max=175.0):
    a = np.asarray(Image.open(src).convert("RGBA")).astype(float)
    L = a[..., :3] @ np.array([0.299, 0.587, 0.114])
    w = np.clip((L - 48.0) / 26.0, 0, 1) * np.clip((sang_max - L) / 30.0, 0, 1)          # bỏ mực (tối) và kem / trắng (sáng)
    S = trung_vi(a, (a[..., 3] > 250) & (w > 0.99))
    k = np.array(dich, float) / np.maximum(S, 1.0)
    moi = np.clip(a[..., :3] * k, 0, 255)
    a[..., :3] = a[..., :3] * (1 - w[..., None]) + moi * w[..., None]
    Image.fromarray(a.astype(np.uint8), "RGBA").save(dst)
    return S


def doi_mau():
    os.makedirs(MANH, exist_ok=True)
    for f in os.listdir(LON):
        if f.endswith(".png") or f == "dat.json":
            shutil.copy2(os.path.join(LON, f), os.path.join(MANH, f))
    for n in MAU_LONG:
        S = doi_mot(os.path.join(LON, n + ".png"), os.path.join(MANH, n + ".png"), LONG)
        print(f"  lông {n:11s} {tuple(int(v) for v in S)} → {LONG}")
    for n in MAU_DA:
        S = doi_mot(os.path.join(LON, n + ".png"), os.path.join(MANH, n + ".png"), DA, sang_max=262.0)
        print(f"  da   {n:11s} {tuple(int(v) for v in S)} → {DA}")
    print("→", MANH)


def bong_anh(ten):
    """hình bóng kín (bool) và cỡ của ảnh mảnh dạng lớn."""
    al = np.asarray(Image.open(os.path.join(LON, ten + ".png")).convert("RGBA"))[..., 3] > 90
    al = cv2.morphologyEx(al.astype(np.uint8), cv2.MORPH_CLOSE, KM.el(3)).astype(bool)
    return al


def khung_cu(ten):
    if ten in KHAN:
        return KHAN[ten]
    w, h = Image.open(os.path.join(LON, ten + ".png")).size
    if ten == "vay":                                   # váy cao sẵn bằng váy đã kéo dài lên tới VAY_TREN trong rig
        d = json.load(open(os.path.join(LON, "dat.json"), encoding="utf-8"))["vay"]
        gy = d["A"][1][2]
        h = int(round(gy + h - VAY_TREN))
    return w, h


def hinh_huong_dan(ten, z):
    """mặt nạ hình bóng hướng dẫn (bool) cỡ khung đã nới × z, và khung đã nới (px ảnh cũ)."""
    to_, _, noi, _, kieu = MOI[ten]
    w0, h0 = khung_cu(ten)
    if kieu == "tu_do":                                # đuôi khăn: dải vải cong nhẹ, thuôn, đầu ngọn xẻ đôi tua rách
        w, h = w0, h0
        im = Image.new("L", (int(w * z), int(h * z)), 0)
        d = ImageDraw.Draw(im)
        pts_l, pts_r = [], []
        for i in range(21):
            v = i / 20
            cx = w * (0.5 + 0.16 * math.sin(v * math.pi * 1.6))
            ban = w * (0.30 - 0.10 * v)
            y = h * (0.97 - 0.92 * v)
            pts_l.append(((cx - ban) * z, y * z))
            pts_r.append(((cx + ban) * z, y * z))
        # ngọn: chẻ chữ V (hai mũi nhô lên, khía ở giữa) nối từ mép trái sang mép phải
        (xl, yt), (xr, _) = pts_l[-1], pts_r[-1]
        ngon = [(xl, yt - 0.05 * h * z), ((xl + xr) / 2, yt + 0.06 * h * z), (xr, yt - 0.03 * h * z)]
        d.polygon(pts_l + ngon + pts_r[::-1], fill=255)
        return np.asarray(im) > 127, (w, h)
    l, t, r, b = noi
    m = bong_anh(ten)
    if kieu == "vay":
        h_moi = khung_cu("vay")[1]
        m = cv2.resize(m.astype(np.uint8) * 255, (m.shape[1], h_moi), interpolation=cv2.INTER_LINEAR) > 127
    m = np.pad(m, ((t, b), (l, r)))
    w, h = m.shape[1], m.shape[0]
    m = cv2.resize(m.astype(np.uint8) * 255, (int(round(w * z)), int(round(h * z))), interpolation=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m, (0, 0), 2.0) > 127
    return m, (w, h)


def to():
    os.makedirs(MAU, exist_ok=True)
    os.makedirs(PK, exist_ok=True)
    for to_, hangs in XEP.items():
        can = np.full((H, W, 3), 255, np.uint8)
        o = {}
        cells = [[(t, *hinh_huong_dan(t, MOI[t][1])) for t in hang] for hang in hangs]
        hh_ = [max(c[1].shape[0] for c in hang) for hang in cells]
        gap_y = (H - sum(hh_)) // (len(hh_) + 1)
        y = gap_y
        for hang, hh in zip(cells, hh_):
            tong = sum(c[1].shape[1] for c in hang)
            ke = (W - tong) // (len(hang) + 1)
            x = ke
            for ten, m, (wk, hk) in hang:
                ch, cw = m.shape
                y0 = y + (hh - ch) // 2
                sub = can[y0:y0 + ch, x:x + cw]
                kieu = MOI[ten][4]
                if kieu == "dau":                       # đầu: hình đầu cũ nhạt dần (chỗ mắt, mõm, bờm) + vùng nới chấm chấm
                    l, t, _, _ = MOI[ten][2]
                    z = MOI[ten][1]
                    cu = Image.open(os.path.join(LON, "dau.png")).convert("RGBA")
                    cu = cu.resize((int(round(cu.width * z)), int(round(cu.height * z))), Image.LANCZOS)
                    ca = np.asarray(cu).astype(float)
                    nhat = ca[..., :3] * 0.45 + 255 * 0.55
                    al = ca[..., 3:] / 255.0
                    ox, oy = int(round(l * z)), int(round(t * z))
                    vung = sub[oy:oy + cu.height, ox:ox + cu.width].astype(float)
                    sub[oy:oy + cu.height, ox:ox + cu.width] = (vung * (1 - al) + nhat * al).astype(np.uint8)
                    for yy in range(0, oy, 14):         # vùng nới phía trên: chấm xám (đỉnh đầu tròn + chỏm tóc được vẽ vào đây)
                        for xx in range(0, cw, 14):
                            cv2.circle(sub, (xx, yy), 2, (190, 190, 190), -1)
                    mp = np.pad(m, 12)
                    sub[(mp & ~cv2.erode(mp.astype(np.uint8), KM.el(3)).astype(bool))[12:-12, 12:-12]] = (150, 150, 150)
                else:
                    sub[m] = MOI[ten][3]
                    mp = np.pad(m, 12)
                    sub[(mp & ~cv2.erode(mp.astype(np.uint8), KM.el(5)).astype(bool))[12:-12, 12:-12]] = INK
                o[ten] = dict(hop=[x, y0, cw, ch], khung=[wk, hk], z=MOI[ten][1])
                x += cw + ke
            y += hh + gap_y
        p = os.path.join(MAU, f"to_{to_}.png")
        Image.fromarray(can).save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        print(p)
        viet_prompt(to_, o, p)


def cho(o, ten):
    x, y, cw, ch = o[ten]["hop"]
    return f"x = {x} to {x + cw}, y = {y} to {y + ch}"


LINE = ("LINE AND COLOUR: exactly the hand-drawn look of image 2: a wobbly dark-brown ink pen outline (#2B2118) about 6 px thick around every "
        "piece (about 4 px for small details inside); coloured-pencil and wax-crayon hatching visible inside every area, strokes thinner than "
        "the outline. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour; no shading, no darker underside, no shadows of any kind, no "
        "highlights or shine spots, no gloss, no glow, no gradients (only one tiny light dot in the eye). Plain pure-white background (#FFFFFF) "
        "between the pieces; the pieces do not touch each other; no labels, no numbers, no frame, nothing else on the sheet.")


def viet_prompt(to_, o, p_to):
    save = os.path.join(TAI, f"{to_}.png")
    dau = ["IMAGES (attached in this order; open each from its path):"]
    if to_ == "N1":
        dau += [f"image 1 = {p_to}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: the places and outlines of four "
                "separate pieces of a 2D animation rig: the HEAD (left, a faded old head drawing inside a grey outline, with a dotted area "
                "above it), two narrow green CLOTH TAILS (middle), and a green rope-like BELT (right).",
                f"image 2 = {DUYET}: the APPROVED character these pieces belong to, 1536x1024, white background: a cute chibi baby langur "
                "with soft grey fur, a cream whisker ruff, a peach face, one big round brown eye with a determined little brow, a green cloth "
                "headband whose knot has two flying tails, a green vine belt and a leaf skirt. Draw the pieces in exactly its design, colours "
                "and hand-drawn style."]
    elif to_ == "N2":
        dau += [f"image 1 = {p_to}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: FIVE flat silhouettes with a dark "
                "outline, pieces of a 2D animation rig: top row: the near FOREARM (grey, wide), the far FOREARM (grey, tall), the leaf "
                "SKIRT (green); bottom row: two SHINS (grey). The silhouettes are exact: outline, size, orientation and place must be kept.",
                f"image 2 = {DUYET}: the APPROVED character these pieces belong to, 1536x1024, white background: a cute chibi baby langur "
                "with soft grey fur, peach hands and feet, a green vine belt with a short skirt of big green leaves. Draw the pieces in "
                "exactly its design, colours and hand-drawn style."]
    else:
        dau += [f"image 1 = {p_to}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: THREE long flat horizontal "
                "silhouettes with a dark outline, the separate pieces of ONE sword for a 2D animation rig, each lying horizontally with its "
                "TIP at the LEFT: top: the SCABBARD (brown); middle: the BLADE (grey); bottom: the HILT (beige) with the GUARD at its left "
                "end. Their length, thickness, orientation and place must be kept.",
                f"image 2 = {DUYET}: the APPROVED character, 1536x1024, white background: a chibi baby langur holding the sword SHEATHED: "
                "see the plain old WOODEN scabbard (with a crack bound with frayed cloth), the small cracked round WOODEN guard and the "
                "HILT wrapped in frayed faded cloth with one loose end. Copy that design and its hand-drawn style.",
                f"image 3 = {KIEM_TRAN}: the same character holding the same sword UNSHEATHED: see the old BLUNT BLADE (dull grey iron with "
                "rust-brown patches, a few nicks chipped out of its edge, a rounded broken-off tip). Copy only the blade design."]
    dau += ["", f"SAVE: save it as a PNG to {save}",
            f"If a file with that name already exists, save as {to_}_2.png, {to_}_3.png ... in the same folder. Do not edit, move or delete "
            "any other file.", ""]
    if to_ == "N1":
        t = ["TASK: draw the four pieces on ONE sheet, each in the place and size of its guide in image 1, cleanly in the hand-drawn style "
             "of image 2. Each piece is ONE separate closed shape with its own ink outline; the pieces do not touch.", "",
             f"- HEAD ({cho(o, 'dau')}): the character's whole HEAD seen in three-quarter profile facing RIGHT, ALONE (no neck, no body, no "
             "arms): exactly the head of image 2: soft grey fur (#777066) on the back and top of the head, a fluffy round top with a small "
             "tuft of hair sticking up (it may use the dotted area above the old head), the round fluffy cream (#F4E7C8) whisker RUFF "
             "framing the face and ending in a short tufted chin, the bare peach (#FDAD81) FACE with a short rounded muzzle, two nostril "
             "dots, round cheeks and a small mouth in a firm little pout (no fang), ONE big round eye with a warm dark-brown iris, a big "
             "pupil, one tiny white dot and a short slanted determined brow. The green cloth HEADBAND (#5FA858) goes round the head just "
             "above the eye, with a small KNOT at the back of the head (on the left side of the head); do NOT draw its two long tails "
             "here (they are separate pieces). Keep the eye, the muzzle and the ruff where the faded old head has them (the faded drawing "
             "is only a placement guide: do not copy its stern face, its fang or its chin cord). The bottom of the ruff ends where the old "
             "head ends.",
             f"- TWO CLOTH TAILS ({cho(o, 'duoi_khan1')} and {cho(o, 'duoi_khan2')}): the two loose tails of the headband, each one long "
             "narrow strip of green cloth (#5FA858) fluttering, its BOTTOM end is where it comes out of the knot (cut straight there), its "
             "TOP end is frayed / ragged, as in image 2. Fill each guide shape; one or two thin fold lines inside.",
             f"- BELT ({cho(o, 'dai')}): the green VINE BELT of image 2 (#6E9A3E): a thick twisted vine rope with a knot at the front and "
             "two short hanging ends, filling EXACTLY the guide shape (same outline: the long band, the knot, the two hanging ends); a few "
             "small leaves may sit on the knot inside the outline.", "", LINE]
    elif to_ == "N2":
        t = ["TASK: redraw image 1 CLEANLY in the hand-drawn style of image 2. Keep EVERY silhouette exactly: the same outline, the same "
             "size, the same orientation, the same place on the sheet (laid over image 1, every shape must coincide with its silhouette). "
             "Each piece is ONE closed shape with the ink outline running all the way round exactly on the edge of its silhouette.", "",
             f"- TWO FOREARMS ({cho(o, 'cang_g')} and {cho(o, 'cang_x')}) and TWO SHINS ({cho(o, 'ong_s')} and {cho(o, 'ong_t')}): plain "
             "pieces of the monkey's FUR-covered limbs: fill each silhouette completely with the soft grey fur (#777066) of image 2 with "
             "crayon hatching and a few short curved fur ticks inside (thin darker pencil strokes); along the outline small, low fur tufts "
             "that stay ON the silhouette edge (they may dent it a little, never stick out). NO armour, no bands, no slats, no hands, no "
             "feet, no other colour.",
             f"- LEAF SKIRT ({cho(o, 'vay')}): the short skirt of image 2: FOUR or FIVE big pointed leaves (#5FA858, each with a darker "
             "centre vein and two or three side veins) hanging side by side and overlapping a little, their stems at the top edge, their "
             "pointed tips forming the lower edge. Fill the whole silhouette: the top edge stays straight, the lower edge may become the "
             "row of leaf tips but stays inside the silhouette.", "", LINE]
    else:
        t = ["TASK: draw the three pieces of the sword on ONE sheet, each lying HORIZONTALLY exactly in the place, length and thickness of "
             "its guide in image 1, cleanly in the hand-drawn style of image 2. Each piece spans the FULL length of its guide (from its "
             "left end to its right end), its long axis along the middle of the guide; the pieces do not touch.", "",
             f"- SCABBARD ({cho(o, 'vo_a')}): one long, slim, straight scabbard of plain old light-brown WOOD (#A27B54) with a few thin "
             "wood-grain lines (#7A5A3C, pencil), one small crack near its middle bound with two turns of frayed cloth (#C9B48A); its "
             "LEFT end is the closed TIP, neatly ROUNDED and closed (not broken, not split); its RIGHT end is the open MOUTH, cut straight. "
             "No lacquer, no metal, no bamboo bands.",
             f"- BLADE ({cho(o, 'luoi_a')}): the old BLUNT blade alone, as in image 3: a straight katana blade of dull old iron (#9A958A) "
             "with three or four rust-brown patches (#A8643A), three small nicks chipped out of its lower edge, a ROUNDED broken-off TIP "
             "at the LEFT, and at the RIGHT end a short narrow tang cut straight. Thin pencil line along the edge; no shine.",
             f"- HILT ({cho(o, 'chuoi_a')}): at its LEFT end the small cracked ROUND wooden GUARD (#8A6446), a disc seen edge-on, a bit "
             "taller than the grip; then the GRIP running to the RIGHT end, wrapped in frayed, faded cloth (#C9B48A) with a few wrap lines, "
             "a small round wooden pommel cap at the right end, and ONE loose frayed cloth end hanging DOWN from near the right end (it may "
             "hang below the guide shape). Its length and the line of its axis are those of the guide.", "", LINE]
    open(os.path.join(PK, f"luot_4_manh_{to_}.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(dau + t) + "\n")
    print(os.path.join(PK, f"luot_4_manh_{to_}.txt"))


def moi_nhat(to_):
    """ảnh mới nhất của tờ (N1.png, N1_2.png ...)."""
    ds = [f for f in os.listdir(TAI) if f == f"{to_}.png" or (f.startswith(f"{to_}_") and f[len(to_) + 1:-4].isdigit())]
    if not ds:
        raise SystemExit(f"chưa có tờ {to_}")
    ds.sort(key=lambda f: int(f[len(to_) + 1:-4]) if f != f"{to_}.png" else 1)
    return os.path.join(TAI, ds[-1])


# kiếm: rig đặt ảnh theo trục = đường giữa bề cao ảnh. GPT vẽ lệch trục (lưỡi lệch 25 px, vỏ 14, chuôi 18) và lưỡi dày gần bằng vỏ (85 / 90 px)
# → lưỡi nằm trong vỏ sẽ ló ra mép dưới. Canh: dời dọc cho trục về giữa; lưỡi ép dọc về bề dày lưỡi cũ (~60 px) quanh trục.
DAY_LUOI = 62.0


def truc_y(a, x0, x1):
    """trục dọc của mảnh: ở mỗi cột trong [x0, x1) lấy đoạn đặc gần giữa ảnh nhất, trả trung vị tâm và bề dày."""
    H = a.shape[0]
    tam, day = [], []
    for x in range(int(x0), int(x1), 4):
        c = a[:, x]
        d = np.diff(np.r_[0, c.astype(np.int8), 0])
        st, en = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
        if not len(st):
            continue
        i = int(np.argmin(np.abs((st + en) / 2 - H / 2)))
        tam.append((st[i] + en[i]) / 2)
        day.append(en[i] - st[i])
    return float(np.median(tam)), float(np.median(day))


def can_kiem():
    for ten, (u0, u1) in (("vo_a", (0.15, 0.85)), ("luoi_a", (0.15, 0.85)), ("chuoi_a", (0.30, 0.68))):
        p = os.path.join(MANH, ten + ".png")
        im = Image.open(p).convert("RGBA")
        a = np.asarray(im)[..., 3] > 120
        W_, H_ = im.size
        ty, dy = truc_y(a, u0 * W_, u1 * W_)
        k = DAY_LUOI / dy if ten == "luoi_a" and dy > DAY_LUOI else 1.0
        h2 = max(1, int(round(H_ * k)))
        im2 = im.resize((W_, h2), Image.LANCZOS) if k != 1.0 else im
        out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        out.paste(im2, (0, int(round(H_ / 2 - ty * k))), im2)
        out.save(p)
        a2 = np.asarray(out)[..., 3] > 120
        ty2, dy2 = truc_y(a2, u0 * W_, u1 * W_)
        print(f"  canh {ten:8s}: trục {ty:.0f} → {ty2:.0f} (giữa {H_ / 2:.0f}), dày {dy:.0f} → {dy2:.0f}")


# ĐUÔI dạng 1 (người dùng 2026-11-13: "đánh thường lỗi lộ đuôi"): gốc đuôi của dạng lớn nằm ngoài mép lưng (dạng lớn nấp trong áo tơi lá; dạng 1 chỉ có
# bắp tay gần che lúc đứng, giơ tay quật kiếm là gốc đuôi thò ra). Dời cả đuôi (ảnh + chuỗi khớp, CÙNG một phép) cho gốc vào sau mảng lưng kp_lung,
# nghiêng ngọn sang trái cho vòng cong khỏi chạm đầu. px khung concept dạng lớn (y xuống); quay quanh khớp gốc, dương = ngược kim đồng hồ trên màn.
DUOI_DOI = dict(dx=110.0, dy=-30.0, goc=10.0)
DUOI_J_LON = [(505, 465), (470, 350), (410, 240), (405, 140), (500, 68), (595, 150)]     # = kiem_si_rig.DUOI_J


def doi_diem_duoi(p):
    c = np.array(DUOI_J_LON[0], float)
    a = math.radians(DUOI_DOI["goc"])
    R = np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])
    return R @ (np.asarray(p, float) - c) + c + np.array([DUOI_DOI["dx"], DUOI_DOI["dy"]])


def doi_duoi(d2, dat_lon):
    A = np.array(dat_lon["duoi"]["A"], float)
    c = np.array(DUOI_J_LON[0], float)
    a = math.radians(DUOI_DOI["goc"])
    R = np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])
    A2 = np.c_[R @ A[:, :2], R @ (A[:, 2] - c) + c + np.array([DUOI_DOI["dx"], DUOI_DOI["dy"]])]
    d2["duoi"]["A"] = A2.tolist()
    d2["duoi"]["doi"] = dict(DUOI_DOI)


def duoi():
    """chỉ ghi lại chỗ đặt đuôi trong dat.json dạng 1 (không cắt lại tờ)."""
    dat = json.load(open(os.path.join(LON, "dat.json"), encoding="utf-8"))
    d2 = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    doi_duoi(d2, dat)
    json.dump(d2, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("đuôi dời", DUOI_DOI)


def cat():
    dat = json.load(open(os.path.join(LON, "dat.json"), encoding="utf-8"))
    so = []
    for to_ in XEP:
        o = json.load(open(os.path.join(MAU, f"to_{to_}.json"), encoding="utf-8"))
        A = KM.doc(moi_nhat(to_))
        if A.shape[:2] != (H, W):
            A = np.asarray(Image.fromarray(A).resize((W, H), Image.LANCZOS))
        G = KM.doc(os.path.join(MAU, f"to_{to_}.png"))
        bg = KM.nen(A, 10 ** 9)
        for ten, d in o.items():
            x, y, cw, ch = d["hop"]
            z = d["z"]
            wk, hk = d["khung"]
            pad = 14 if ten != "chuoi_a" else 60
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            m = ~bg[y0:y1, x0:x1]
            n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
            if n > 1:
                giu = 1 + int(np.argmax(st[1:, 4]))
                lon = st[giu, 4]
                m = np.isin(lab, [i for i in range(1, n) if st[i, 4] >= 0.08 * lon])     # cụm lớn nhất + mẩu kề đáng kể (tua vải)
            full = np.zeros(bg.shape, bool)
            full[y0:y1, x0:x1] = m
            im, goc = KM.manh_rgba(A, full)
            o_ = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
            o_.paste(im, (goc[0] - x, goc[1] - y), im)
            ra = o_.resize((wk, hk), Image.LANCZOS)
            ra.save(os.path.join(MANH, ten + ".png"))
            a_ = np.asarray(o_)[..., 3] > 120
            b_ = G[y:y + ch, x:x + cw].min(2) < 238
            iou = float((a_ & b_).sum()) / max(1, (a_ | b_).sum())
            print(f"  {to_} {ten:11s} IoU {iou:.3f}  khung {wk} × {hk}")
            so.append((ten, ra))
    # dat.json của dạng 1: khung nới thì dời gốc affine; váy cao sẵn; đuôi khăn thay hai lá mào
    d2 = json.loads(json.dumps(dat))
    for ten in ("dau", "dai", "cang_g", "cang_x", "ong_s", "ong_t", "vo_a", "luoi_a", "chuoi_a"):
        l, t, r, b = MOI[ten][2]
        if isinstance(dat[ten].get("A"), list):          # mảnh kiếm không có A: rig đặt theo trục kiếm (giữa bề cao ảnh)
            Aff = np.array(dat[ten]["A"], float)
            Aff[:, 2] = Aff[:, 2] - Aff[:, :2] @ np.array([l, t], float)
            d2[ten]["A"] = Aff.tolist()
        w0, h0 = Image.open(os.path.join(LON, ten + ".png")).size
        d2[ten]["co"] = [w0 + l + r, h0 + t + b]
        d2[ten]["noi"] = [l, t, r, b]
    l, t, r, b = MOI["vay"][2]
    gx, gy = dat["vay"]["A"][0][2], dat["vay"]["A"][1][2]
    w0, h0 = Image.open(os.path.join(LON, "vay.png")).size
    hv = khung_cu("vay")[1]
    d2["vay"]["A"] = [[1.0, 0.0, gx - l], [0.0, 1.0, gy + h0 - hv - t]]
    d2["vay"]["co"] = [w0 + l + r, hv + t + b]
    d2["vay"]["noi"] = [l, t, r, b]
    # đuôi khăn: nút buộc ở sau đầu (mép trái ảnh đầu, cao 1/3) bay ra sau sang trái; theo khung concept dạng lớn (px)
    Ad = np.array(dat["dau"]["A"], float)
    wd, hd = Image.open(os.path.join(LON, "dau.png")).size
    nut = Ad @ np.array([0.10 * wd, 0.30 * hd, 1.0])
    for ten_moi, ten_cu, (dx, dy) in (("duoi_khan1", "la_to", (-250.0, -60.0)), ("duoi_khan2", "la_nho", (-205.0, 40.0))):
        wk, hk = KHAN[ten_moi]
        goc = nut + np.array([0.0, 6.0 if ten_moi == "duoi_khan2" else -6.0])
        ngon = goc + np.array([dx, dy])
        Aff = KM.aff_hai_diem((wk / 2, hk * 0.97), (wk / 2, hk * 0.05), goc, ngon)
        d2[ten_cu] = dict(anh=ten_moi, co=[wk, hk], nhom="roi", goc=[float(v) for v in goc], ngon=[float(v) for v in ngon],
                          A=np.asarray(Aff, float).tolist())
    doi_duoi(d2, dat)
    json.dump(d2, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    can_kiem()
    # tờ so mảnh mới
    cell = 220
    out = Image.new("RGB", (cell * len(so), cell + 20), (150, 150, 150))
    dr = ImageDraw.Draw(out)
    for i, (ten, im) in enumerate(so):
        s = min((cell - 10) / im.width, (cell - 10) / im.height)
        t_ = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        out.paste(t_, (i * cell + 5, 18), t_)
        dr.text((i * cell + 5, 3), ten, fill=(0, 0, 0))
    out.save(os.path.join(MANH, "_so_moi.png"))
    print(os.path.join(MANH, "_so_moi.png"), "; dat.json dạng 1 đã ghi")


if __name__ == "__main__":
    {"doi_mau": doi_mau, "to": to, "cat": cat, "duoi": duoi}[sys.argv[1]]()
