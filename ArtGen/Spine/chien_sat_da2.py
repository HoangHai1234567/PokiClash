# -*- coding: utf-8 -*-
"""Chiến binh sắt DẠNG 2 (chien_sat_2): mảnh da cho rig dạng 2 (cùng rig dạng 1, tỉ lệ đổi ở chien_sat_rig.py CS_DANG=2).
Concept đã duyệt: hướng B (thép xám thẫm + viền bạc + đỏ; cánh thép bên trái mũ; giáp vai hai lớp; khiên núm gai + bốn đinh; giáo to bản).

Ba loại mảnh:
1. GIỮ HÌNH BÓNG (đổi da): tờ hướng dẫn = CHÍNH mảnh dạng 1 đã xong xếp đúng ô; Codex đổi màu, thêm viền bạc, giữ hình bóng. Cắt theo ô.
   Tờ A2: mào, mặt nạ + đĩa, vòm sau mũ, khiên, vạt áo. Tờ B2: ngực, váy giáp, giáp vai xa, hai ống chân, ba mảnh bàn tay.
2. ĐỔI DÁNG / MẢNH MỚI (mảnh cứng một xương): gen "đúng chỗ, đúng cỡ" từ concept (ảnh 1 = concept, chỉ giữ mảnh đó, vẽ đủ phần khuất),
   đặt vào rig bằng toạ độ concept → thế giới khung 0 idle (bố cục dạng 2 là ảnh mẫu của concept: mau/bo_cuc.json).
   Lượt W1: cánh thép bên trái mũ + cây giáo (hai mảnh không chồng nhau). Lượt W2: giáp vai gần (hai lớp, nhô trên khiên).
3. GIỮ NGUYÊN ẢNH dạng 1: đùi, đũng, bắp tay, cổ (áo lót đen), cẳng tay quấn vải đỏ.

    chien_sat_da2.py to       tờ hướng dẫn A2, B2 + prompt; prompt W1, W2 → gui_gpt/chien_sat_2/
    chien_sat_da2.py cat      cắt mọi tờ đã về → inbox/chien_sat_2/manh/ (+ _so_*.png, _iou.json, moi.json: mảnh mới, chỗ trên concept)
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chien_sat_da as D  # noqa: E402

W, H = 1536, 1024
RES = D.RES
MANH1 = D.MANH                                                     # mảnh dạng 1 đã xong (cỡ ảnh vùng × RES)
BASE2 = D.BASE2
MAU2, TAI2 = D.MAU2, D.TAI2
MANH2 = os.path.join(BASE2, "manh")
GUI2 = D.GUI2
CONCEPT2 = os.path.join(TAI2, "L1_duyet.png")
GIU = ("datui_l_01", "datui_r_01", "dang_01", "dabi_r_01", "bozi_01", "xiaobi_r_02")    # dùng nguyên ảnh dạng 1
TO2 = {
    "A2": [[("guan_01", 2.5), ("hujing_01", 2.5), ("tou_01", 2.5)], [("dun_01", 2.5), ("qizi_01", 2.5)]],
    "B2": [[("st_01", 4.0), ("qunbai_01", 4.0), ("hujian_r_01", 4.0), ("xiaotui_l_01", 4.0), ("xiaotui_r_01", 4.0)],
           [("xiaobi_r_01", 5.5), ("sizhi_01", 5.5), ("damz_01", 5.5)]],
}
PX = {"A2": "6", "B2": "9 (about 12 on the three hand pieces of the bottom row)"}
MAU_B = ("steel plates #777A82, faces turned away / thick edges darker steel #5E6068, a narrow bright SILVER trim #C8CAD0 along the "
         "rims listed below, crimson #BF2F3A with darker crimson #95252C, under-suit near-black #26272B, steel gauntlets #6E717A")
MO_TA2 = {
    "A2": [
        ("guan_01", "THE HELMET CREST (big curved fan): keep everything, crimson horsehair #C1303C with the darker #95252C inner band, the same "
                    "strand lines."),
        ("hujing_01", "THE HELMET FACE-PLATE with the round disc: plate steel #777A82, the narrow side band on its right darker #5E6068; a "
                      "narrow silver trim #C8CAD0 along its top rim and its outer edge; the eye slits flat dark charcoal #22252B; the round "
                      "disc steel #777A82 with a silver rim."),
        ("tou_01", "THE ROUND BACK DOME: one flat darker steel #4E5058; the knob on top crimson #95252C."),
        ("dun_01", "THE KITE SHIELD: the raised border frame bright silver #C8CAD0 (same shape); the inner field steel #6D717B; the thick side "
                   "edge #59595F; the top band steel #777A82. In the middle of the inner field: one round steel boss with a short blunt "
                   "conical spike pointing at the viewer (light steel #BCBEC5), and four small round silver studs around it (above, below, "
                   "left, right). Nothing else."),
        ("qizi_01", "THE TABARD: flat crimson #BF2F3A, a silver #C8CAD0 band near its bottom (where the dark band is)."),
    ],
    "B2": [
        ("st_01", "CHEST PLATE: steel #777A82, the face turned away #5E6068, its rim bands bright silver #C8CAD0."),
        ("qunbai_01", "SHORT ARMOURED SKIRT: steel #777A82, plates turned away #5E6068, trims bright silver #C8CAD0."),
        ("hujian_r_01", "SHOULDER PLATE (spear side): steel #777A82, its rim bright silver #C8CAD0."),
        ("xiaotui_l_01", "SHIN AND BOOT (near leg): steel #777A82, the boot toe band and the face turned away #5E6068; keep the plate lines."),
        ("xiaotui_r_01", "SHIN AND BOOT (far leg): the same."),
        ("xiaobi_r_01", "PALM behind the spear shaft (drawn very big): steel gauntlet #6E717A, plain."),
        ("sizhi_01", "FINGERS in front of the spear shaft (drawn very big): steel gauntlet #6E717A, keep the lines between the fingers."),
        ("damz_01", "THUMB (drawn very big): steel gauntlet #6E717A."),
    ],
}
VI2 = {"A2": "mào, mặt nạ + đĩa, vòm sau mũ, khiên, vạt áo (mảnh dạng 1)",
       "B2": "ngực, váy giáp, giáp vai xa, hai ống chân, lòng bàn tay, ngón tay, ngón cái (mảnh dạng 1)"}
SO2 = {"A2": "Five parts: top row a big curved crimson crest, the helmet face-plate with eye slits and a round disc, the round back dome; "
             "bottom row a big kite shield with a round boss and four rivets, a narrow crimson tabard.",
       "B2": "Eight parts: top row a chest plate, a short armoured skirt, a shoulder plate, two shins with boots; bottom row three gauntlet "
             "pieces of the spear hand (palm, fingers, thumb), drawn very big."}
# mảnh mới / đổi dáng, gen đúng chỗ từ concept: (lượt, tên, tả tiếng Anh, tả Việt)
MOI = {
    "W1": [("canh_mu", "THE SWEPT-BACK STEEL WING on the LEFT side of the helmet (three stacked feather-like metal blades pointing up and back "
                       "to the left, steel #AAABB3 with darker #777A82 undersides): draw it COMPLETE as ONE closed shape: its root, hidden "
                       "behind the round disc of the helmet, ends in a rounded base about where the disc is; its lower part, hidden behind "
                       "the shoulder plate, drawn complete too.",
            "cánh thép bên trái mũ (vẽ đủ phần nấp sau đĩa tròn và giáp vai)"),
           ("giao", "THE WHOLE SPEAR on the right: the long broad leaf-shaped steel spearhead (#BCBEC5, one central ridge line), the silver "
                    "collar, the crimson tassel, the long dark steel shaft (#565860) and the small pointed butt cap at the bottom: draw it "
                    "COMPLETE as ONE closed shape, the part of the shaft hidden behind the fist drawn too (straight, same width), NO hand.",
            "cả cây giáo (vẽ đủ đoạn cán nấp sau nắm tay, không có tay)")],
    "W2": [("vai_gan", "THE BIG NEAR SHOULDER PLATE (on the left, the rounded two-layer steel plate that rises above the top edge of the "
                       "shield, steel #787A82 with silver #C8CAD0 rims): draw it COMPLETE as ONE closed shape, its lower part hidden behind "
                       "the shield drawn complete too (the plates curve down and end in a rounded lower edge).",
            "giáp vai gần hai lớp (vẽ đủ phần nấp sau khiên)")],
}


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def to():
    os.makedirs(MAU2, exist_ok=True)
    O = {}
    for ma, hang in TO2.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for r, z in h_:
                g = Image.open(os.path.join(MANH1, r + ".png")).convert("RGBA")
                big = g.resize((int(round(g.width / RES * z)), int(round(g.height / RES * z))), Image.LANCZOS)
                cs.append((r, z, big))
            cao.append((cs, max(c[2].height for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, big in cs:
                y0 = y + (hh - big.height) // 2
                can.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, big.width, big.height], z=z, xoay=0)
                x += big.width + ke
            y += hh + ke_y
        p = os.path.join(MAU2, f"huong_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    prompt(O)


def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


def prompt(O):
    gd = ["", "## Lượt 2: mảnh da dạng 2 (concept B đã duyệt 2026-11-16)", "",
          "Tờ A2, B2: tờ hướng dẫn là CHÍNH mảnh dạng 1 đã xong xếp đúng ô; GPT đổi da theo concept B, giữ hình bóng. Lượt W1, W2: mảnh mới / đổi "
          "dáng gen \"đúng chỗ, đúng cỡ\" từ concept B (chỉ giữ mảnh đó, vẽ đủ phần khuất).", ""]
    for ma, o in O.items():
        mau = os.path.join(MAU2, f"huong_{ma}.png")
        out = os.path.join(TAI2, f"D_{ma}.png")
        p = os.path.join(GUI2, f"luot_2_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: the separate body parts of OUR first-form knight puppet, each drawn alone, "
                   "at the exact size and place to keep. " + SO2[ma],
              f"Tờ mảnh dạng 1 (1536 × 1024, nền trắng): {VI2[ma]}"),
             (CONCEPT2, "the APPROVED picture of the EVOLVED second form of this character, 1536x1024, white background: darker steel armour "
                        "with narrow bright silver trims, a crimson horsehair crest, a swept-back steel wing on the left of the helmet, a "
                        "silver-framed kite shield with a spiked boss and four studs, a crimson tabard, a long broad-bladed spear. Take from "
                        "it the colours, the trims and the hand-drawn look. The shapes come from image 1.",
              "Concept dạng 2 đã duyệt (hướng B): lấy màu, viền bạc, nét vẽ")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: RESKIN. Image 1 is a sheet of the separate body PARTS of a 2D animation puppet (a chubby armoured knight), each part "
              "drawn alone on white. Redraw the SAME sheet with every part REPAINTED for the evolved form (image 2), so that the parts fit "
              "the same puppet. For EVERY part keep exactly: its silhouette, its size, its orientation, its place on the sheet (laid over "
              "image 1 every part must coincide) and its structural lines. Do NOT merge, add or move parts. Pure white between the parts.",
              "",
              f"NEW LOOK (see image 2): {MAU_B}. Hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {PX[ma]} px) all the "
              "way round every part, thinner ink lines for the inner structural lines, every area ONE flat colour with visible "
              "coloured-pencil / wax-crayon hatching. No shading, no highlights, no gradients, no glow, no shadows: flat colour only. "
              "SIMPLE: no extra rivets, engravings or patterns beyond what is listed.", "",
              "THE PARTS (coordinates are pixels on the 1536x1024 sheet):"]
        t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA2[ma], 1)]
        t += ["", D.BG2]
        ghi(p, t)
        print(p)
        gd += [f"### Tờ `{ma}`: {VI2[ma]}", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    for ma, ds in MOI.items():
        out = os.path.join(TAI2, f"M_{ma}.png")
        p = os.path.join(GUI2, f"luot_2_moi_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT2)}: the APPROVED picture of our evolved iron knight, 1536x1024, white background.", "",
             f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 keeping ONLY the piece(s) listed below, each in the SAME POSITION, at the SAME SIZE and the SAME ANGLE as "
             "in image 1 (laid over image 1 they must coincide); REMOVE everything else (helmet, crest, shield, body, arms, legs, every "
             "other piece): pure white there. COMPLETE each kept piece into ONE closed shape with a dark-brown ink outline all the way "
             "round, drawing the parts that are hidden in image 1 as described:", ""]
        t += [f"- {en}" for _, en, _ in ds]
        t += ["", "Same drawing style and colours as image 1: wobbly dark-brown ink outline (about 7 px), flat colours with crayon hatching, "
              "no shading, no highlights, no glow. Pure-white background, nothing else on the canvas, no labels."]
        ghi(p, t)
        print(p)
        gd += [f"### Lượt `{ma}`: " + "; ".join(vi for _, _, vi in ds), "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh mẫu duy nhất: concept dạng 2 `{Wp(CONCEPT2)}`; ảnh lưu vào `{Wp(out)}`.", ""]
    gd += ["Kiểm: tờ A2, B2 mỗi mảnh đúng chỗ, đúng cỡ, đúng hình bóng tờ hướng dẫn; lượt W1, W2 mảnh trùng chỗ concept, vẽ đủ phần khuất, "
           "không dính mảnh khác. Cắt: `py -3 -I ArtGen/Spine/chien_sat_da2.py cat`."]
    hd = os.path.join(GUI2, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def cat():
    os.makedirs(MANH2, exist_ok=True)
    for r in GIU:
        shutil.copy(os.path.join(MANH1, r + ".png"), os.path.join(MANH2, r + ".png"))
    V = D.vung()
    pj = os.path.join(MANH2, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    for ma in TO2:
        fs = sorted([f for f in os.listdir(TAI2) if f.startswith(f"D_{ma}") and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(TAI2, f)))
        if not fs:
            print(f"tờ {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(os.path.join(TAI2, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        o = json.load(open(os.path.join(MAU2, f"huong_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(MAU2, f"huong_{ma}.png")).convert("RGB")).astype(np.int32)
        fg, fgG = ~D.nen(A), ~D.nen(Gd)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        print(f"tờ {ma}: {fs[-1]}")
        for r, d in o.items():
            x, y, cw, ch = d["hop"]
            pad = 14
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), D.el(10)).astype(bool)
            ids = [i for i in np.unique(lab[y0:y1, x0:x1][gm]) if i > 0 and st[i, 4] > 60]
            m = np.isin(lab, ids)
            m[:y0] = m[y1:] = False
            m[:, :x0] = m[:, x1:] = False
            rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
            mm = m[y:y + ch, x:x + cw]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), D.el(2)).astype(bool)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - rgb.min(2).astype(np.float32)) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            a2 = np.asarray(im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            a2[..., 3] = np.where(cv2.dilate(ag.astype(np.uint8), D.el(3)).astype(bool), a2[..., 3], 0)
            thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), D.el(5)).astype(bool)
            if thieu.any():
                co = (a2[..., 3] >= 128).astype(np.uint8)
                _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                ys_, xs_ = np.nonzero(co)
                bang = np.zeros((lbl.max() + 1, 3), np.uint8)
                bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
                a2[thieu, :3] = bang[lbl[thieu]]
                a2[thieu, 3] = 255
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH2, r + ".png"))
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            ious[r] = round(iou, 3)
            print(f"  {r:12s} IoU {iou:.3f}")
    json.dump(ious, open(pj, "w"), indent=1)
    # mảnh mới: mỗi mảnh một cụm liền (lớn nhất trong vùng tả), lưu ảnh cắt sát + khung trên concept (px 1536 × 1024)
    moi = {}
    pm = os.path.join(MANH2, "moi.json")
    if os.path.exists(pm):
        moi = json.load(open(pm))
    VUNG = {"canh_mu": (380, 150, 900, 640), "giao": (900, 0, 1250, 1024), "vai_gan": (380, 380, 900, 800)}
    for ma, ds in MOI.items():
        fs = sorted([f for f in os.listdir(TAI2) if f.startswith(f"M_{ma}") and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(TAI2, f)))
        if not fs:
            print(f"lượt {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(os.path.join(TAI2, fs[-1])).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~D.nen(A)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        for ten, _, _ in ds:
            x0, y0, x1, y1 = VUNG[ten]
            cand = [i for i in range(1, n) if st[i, 4] > 300 and x0 <= st[i, 0] + st[i, 2] / 2 <= x1 and y0 <= st[i, 1] + st[i, 3] / 2 <= y1]
            if not cand:
                print(f"  {ten}: KHÔNG thấy cụm")
                continue
            i = max(cand, key=lambda j: st[j, 4])
            m = lab == i
            x, y, w, h = st[i, :4]
            rgb = A[y:y + h, x:x + w].astype(np.uint8)
            mm = m[y:y + h, x:x + w]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH2, ten + ".png"))
            moi[ten] = dict(hop=[int(x), int(y), int(w), int(h)], nguon=fs[-1])
            print(f"  {ten:12s} khung trên concept {x},{y} {w}×{h}  ({fs[-1]})")
    json.dump(moi, open(pm, "w"), indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "to":
        to()
    elif cmd == "cat":
        cat()
    else:
        print(__doc__)
