# -*- coding: utf-8 -*-
"""Sâu đất (sau_dat): MẢNH CỨNG của đầu cắt "ĐÚNG CHỖ, ĐÚNG CỠ" từ concept đã duyệt (tai_ve/L1_duyet.png), mỗi lượt vài mảnh KHÔNG chạm
nhau, vẽ đủ phần khuất (skill pokiclash-spine-rig mục 00, mục 25). Mảnh về nằm đúng toạ độ concept; rig đặt từng mảnh theo chỗ của nó
trên concept (khung concept trùng khung goc_ca_con: cùng tỉ lệ s, tâm cx, cy) rồi gắn vào xương đầu / hàm.

Mảnh → slot của họ:
    dau   → P_shange   (vòng giáp trước của đầu, nửa trên miệng + hàm răng trên; không mắt, không gờ mày, không hàm dưới)
    ham   → P_xiae_01  (hàm dưới + hàm răng dưới; không ngà)
    mieng → P_xiae_02  (lòng miệng đỏ đất nung + vòng răng trong, đĩa tròn đủ)
    mat   → P_jiao_05  (mắt hổ phách)
    may   → P_jiao_08  (gờ mày đá)
    nanh1 → P_jiao_07, nanh2 → P_jiao_09 (hai ngà; rig cho bám xương HÀM bone13)
    maoA  → P_jiao_03, maoB → P_jiao_02, maoC → P_jiao_01 (ba tấm mào quạt), vong → P_jiao_04 (vòng giáp thứ hai sau đầu)
    P_jiao_06 (gai nhỏ trên mõm của họ): concept không có, tạm ẩn (ghi trong ghi chú, báo người dùng)

    sau_dat_cung.py prompt       tờ viền mau/_vien_K*.png + file prompt gui_gpt/sau_dat_1/luot_4_K*.txt
    sau_dat_cung.py cat          cắt tai_ve/K*.png → manh/cung/<mảnh>.png + manh/cung/dat.json (hộp trên concept)
    sau_dat_cung.py mat          cắt mắt thẳng từ concept (không bị che) → manh/cung/mat.png
    sau_dat_cung.py ghep         ghép mảnh cứng lên concept mờ → mau/_ghep_cung.png
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
import sau_dat  # noqa: E402,F401
import tho5  # noqa: E402

G = tho5.dat("sau_dat")
W, H = 1536, 1024
MAU, TAI = G.MAU, G.TAI
CONCEPT = os.path.join(TAI, "L1_duyet.png")
GUI = os.path.join(HERE, "gui_gpt", "sau_dat_1")
CUNG = os.path.join(G.BASE, "manh", "cung")

# vùng thô của từng mảnh trên concept (px concept, đọc trên mau/_can_dau_concept.png): đa giác hoặc ("e", cx, cy, rx, ry)
VUNG = {
    "dau": [(845, 452), (880, 440), (950, 444), (1010, 466), (1048, 498), (1060, 540), (1040, 548), (1000, 505), (955, 498), (925, 522),
            (908, 560), (872, 578), (850, 562), (840, 505)],
    "ham": [(858, 572), (906, 560), (932, 606), (980, 614), (1028, 598), (1044, 578), (1052, 608), (1032, 640), (952, 652), (880, 636),
            (854, 602)],
    "mieng": ("e", 985, 556, 58, 62),
    "mat": ("e", 918, 508, 22, 15),
    "may": [(864, 466), (900, 457), (962, 470), (964, 496), (900, 492), (866, 490)],
    "nanh1": ("e", 908, 600, 17, 26),
    "nanh2": ("e", 1002, 610, 17, 28),
    "maoA": [(752, 262), (800, 250), (880, 262), (912, 300), (906, 352), (820, 346), (760, 332)],
    "maoB": [(620, 322), (680, 290), (760, 292), (800, 322), (790, 402), (700, 396), (630, 382)],
    "maoC": [(626, 402), (700, 392), (762, 402), (772, 470), (700, 482), (630, 480)],
    "vong": [(800, 372), (850, 356), (906, 380), (900, 450), (880, 520), (862, 600), (820, 602), (800, 520)],
}
SLOT = {"dau": "P_shange", "ham": "P_xiae_01", "mieng": "P_xiae_02", "mat": "P_jiao_05", "may": "P_jiao_08", "nanh1": "P_jiao_07",
        "nanh2": "P_jiao_09", "maoA": "P_jiao_03", "maoB": "P_jiao_02", "maoC": "P_jiao_01", "vong": "P_jiao_04"}
MO_TA = {
    "dau": ("the HEAD'S FRONT ARMOUR RING (upper part): the blunt sandstone head ring around the mouth, from the top of the ring down to "
            "the upper lip, with the row of UPPER TEETH along the top rim of the round mouth",
            "WITHOUT the eye (plain sandstone where it was), WITHOUT the heavy brow block above the eye (plain sandstone), WITHOUT the "
            "lower jaw, WITHOUT the tusks, WITHOUT the red inside of the mouth (the mouth opening stays EMPTY WHITE inside the teeth); its "
            "back end, hidden by the rings behind it, completed as a rounded edge"),
    "ham": ("the LOWER JAW: the lower part of the head ring under the round mouth, with the row of LOWER TEETH along its top rim",
            "WITHOUT the two tusks (plain jaw where their roots were); its back end, hidden behind the upper head, completed as a rounded "
            "hinge; the mouth opening above its teeth stays EMPTY WHITE"),
    "mieng": ("the INSIDE OF THE MOUTH as ONE complete round DISK: deep terracotta red #A2412E with a darker throat hole in the middle and "
              "one ring of small cream teeth pointing inwards",
              "complete it as a full closed disk a little BIGGER than the mouth opening (its rim would be hidden under the lips); no lips, "
              "no outer teeth, no head"),
    "mat": ("the EYE: narrow amber eye with its black slit pupil and one small white dot, with its dark-brown ink outline",
            "complete it as one closed almond shape"),
    "may": ("the heavy stone BROW BLOCK above the eye", "complete it as one closed rounded block (its lower edge straight)"),
    "nanh1": ("the LEFT TUSK (the one near the eye, at the lower left of the mouth)", "complete its root, hidden in the jaw, as a rounded base"),
    "nanh2": ("the RIGHT TUSK (at the lower right of the mouth)", "complete its root, hidden in the jaw, as a rounded base"),
    "maoA": ("the TOP CREST PLATE (the big rounded fan plate at the top middle, above the rings)",
             "complete it as one closed rounded fan plate: its lower part, hidden behind the rings, rounded too"),
    "maoB": ("the UPPER-LEFT CREST PLATE (the big rounded fan plate at the top left)",
             "complete it as one closed rounded fan plate: its right part, hidden behind the top plate and the rings, rounded too"),
    "maoC": ("the LOWER-LEFT CREST PLATE (the rounded fan plate at the left, below the upper-left one)",
             "complete it as one closed rounded fan plate: its right part, hidden behind the rings, rounded too"),
    "vong": ("the SECOND ARMOUR RING of the head (the broad ring band just behind the front ring with the mouth)",
             "complete it as one closed ring band: its front edge, hidden behind the front ring, continues as a rounded band; no feelers, "
             "no crest plates"),
}
# K4: ngà trái GPT vẽ chạm đáy vòng giáp → tách theo đường mực chung (vùng màu giữ / bỏ chọn bằng điểm px concept). Bản đầu cắt theo vòng
# tròn quanh ngà: xén mất mũi ngà, dính một mẩu vòng giáp (người dùng thấy "2 nanh dưới nhìn như lỗi layer", 2026-11-17).
_NGA1 = [(885, 590), (843, 620)]                 # lòng ngà (kem), hốc ngà (vàng đất)
_VONG = [(800, 470), (812, 560), (790, 400)]      # thân vòng giáp
TACH = {"nanh1": (_NGA1, _VONG), "vong": (_VONG, _NGA1)}


def tach_muc(rgb, mm, giu, bo):
    """tách một cụm GPT vẽ dính hai mảnh: bỏ nét mực (tối) thì các mảng màu là vùng rời; giữ các vùng chứa điểm `giu`, bỏ vùng chứa
    điểm `bo`; nét mực chia cho bên gần hơn (biến đổi khoảng cách), chỉ lấy mực trong 9 px quanh phần giữ."""
    toi = rgb.astype(int).mean(2) < 95
    mau = (mm & ~toi).astype(np.uint8)
    _, lab = cv2.connectedComponents(mau, connectivity=4)

    def vung(pts):
        m = np.zeros(mm.shape, bool)
        for x, y in pts:
            o = lab[max(0, y - 6):y + 7, max(0, x - 6):x + 7]
            ys, xs = np.nonzero(o)
            if len(ys):
                m |= lab == o[ys[0], xs[0]]
        return m

    g, b = vung(giu), vung(bo)
    dg = cv2.distanceTransform((~g).astype(np.uint8), cv2.DIST_L2, 5)
    db = cv2.distanceTransform((~b).astype(np.uint8), cv2.DIST_L2, 5)
    muc = mm & toi & (dg <= db) & (dg < 9)
    con = mm & ~toi & ~g & ~b & (dg < db)                                # mẩu màu nhỏ không có điểm chọn: theo bên gần hơn
    return g | muc | con
NHOM = {"K1": ["dau", "maoA"], "K2": ["ham", "maoB", "may"], "K3": ["mieng", "maoC"], "K4": ["nanh1", "nanh2", "vong"]}


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def mat_na(k):
    m = np.zeros((H, W), np.uint8)
    v = VUNG[k]
    if isinstance(v, tuple):
        cv2.ellipse(m, (v[1], v[2]), (v[3], v[4]), 0, 0, 360, 1, -1)
    else:
        cv2.fillPoly(m, [np.array(v, np.int32)], 1)
    return m.astype(bool)


def prompt():
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H)))
    for nh, ks in NHOM.items():
        m = np.zeros((H, W), bool)
        for k in ks:
            m |= mat_na(k)
        m2 = cv2.dilate(m.astype(np.uint8), el(10)).astype(bool)
        B = (A * 0.3 + 255 * 0.7).astype(np.uint8)
        B[m2] = A[m2]
        vien = cv2.dilate(m2.astype(np.uint8), el(3)).astype(bool) & ~m2
        B[vien] = (230, 30, 30)
        pv = os.path.join(MAU, f"_vien_{nh}.png")
        Image.fromarray(B).save(pv)
        out = os.path.join(TAI, f"{nh}.png")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: the APPROVED picture of our character (a colossal sandworm, hand-drawn: wobbly dark-brown ink "
             "line, crayon hatching, flat colours).",
             f"image 2 = {Wp(pv)}: the same picture with the parts to KEEP shown in full colour inside RED outlines (the outlines are rough: "
             "keep the WHOLE part named below, even where it pokes out of its outline); everything faded is to be removed.", "",
             f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as {nh}_2.png, {nh}_3.png ... in the same folder. Do not edit, move or delete "
             "any other file.", "",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as "
             "in image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else "
             "(pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way round "
             "it: where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, "
             "colours and flat crayon colouring. Same wobbly dark-brown ink line (about 7 px), same colours, completely flat colouring as "
             "image 1 (no shading, no highlights, no glow, no shadows). Do not move, resize, rotate or redesign anything. Do NOT draw the "
             "red outlines. Keep a clear white gap between the kept parts.", "", "KEEP:"]
        for i, k in enumerate(ks, 1):
            mt, kh = MO_TA[k]
            t.append(f"{i}. {mt}: {kh}.")
        t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles."]
        p = os.path.join(GUI, f"luot_4_{nh}.txt")
        os.makedirs(GUI, exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        print(p, ks)


def cat():
    """mỗi ảnh K*: tách nền trắng, gán cụm theo vùng thô (cụm phủ vùng nhiều nhất), lỗ trắng kín lớn (lòng miệng của dau / ham) đục trong."""
    from quai import anh
    os.makedirs(CUNG, exist_ok=True)
    pd = os.path.join(CUNG, "dat.json")
    DAT = json.load(open(pd, encoding="utf-8")) if os.path.exists(pd) else {}
    for nh, ks in NHOM.items():
        path = anh.to_moi_nhat(TAI, nh)
        if not path:
            print(nh, "chưa có ảnh")
            continue
        im = Image.open(path).convert("RGB")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
            path = os.path.join(MAU, f"_{nh}_doi_co.png")
            im.save(path)
        tt = anh.doc_to(path, dien_tich_min=150, gop_px=6)
        rgb = np.asarray(im)
        for k in ks:
            vm = mat_na(k)
            best, bs = None, 0
            for c in tt.manh:
                mm = np.isin(tt.lab, c["ids"])
                s = (mm & vm).sum() / max(1, vm.sum())
                if s > bs:
                    best, bs = c, s
            if best is None:
                print(f"  {k}: không thấy cụm")
                continue
            mm = np.isin(tt.lab, best["ids"])
            if k in TACH:                                               # hai mảnh GPT vẽ chạm nhau: tách theo ĐƯỜNG MỰC chung
                mm = tach_muc(rgb, mm, *TACH[k])
                mm = cv2.morphologyEx(mm.astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)     # gọt gai mực vụn ở mép tách
            a = tt.rgba[..., 3].astype(np.float32) / 255.0 * anh.gian(mm, 2)
            if k in ("dau", "ham"):                                     # lòng miệng để trắng: đục trong (giấy trắng kín, sáng, không vân)
                trang = (rgb.min(2) > 236) & cv2.dilate(mm.astype(np.uint8), el(3)).astype(bool)
                n, lab, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), 8)
                for i in range(1, n):
                    if st[i, cv2.CC_STAT_AREA] > 120:
                        a[cv2.dilate((lab == i).astype(np.uint8), el(1)).astype(bool)] = 0
            ys, xs = np.nonzero(a > 0.04)
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            out = np.dstack([rgb[y0:y1, x0:x1], (a[y0:y1, x0:x1] * 255).astype(np.uint8)])
            Image.fromarray(out, "RGBA").save(os.path.join(CUNG, k + ".png"))
            DAT[k] = {"slot": SLOT[k], "hop": [int(x0), int(y0), int(x1), int(y1)], "nguon": os.path.basename(path), "phu": round(float(bs), 2)}
            print(f"  {k} → {SLOT[k]}: hộp {x0},{y0}–{x1},{y1}, phủ vùng thô {bs:.2f}")
    json.dump(DAT, open(pd, "w", encoding="utf-8"), indent=1)


def mat():
    """mắt không bị che trên concept: cắt thẳng (vùng hổ phách + con ngươi + chấm sáng, nới ra lấy viền mực quanh nó)."""
    A = np.asarray(Image.open(CONCEPT).convert("RGB").resize((W, H))).astype(int)
    vm = cv2.dilate(mat_na("mat").astype(np.uint8), el(10)).astype(bool)
    hp = vm & (A[..., 0] > 225) & (A[..., 2] < 110) & (A[..., 0] - A[..., 2] > 140)   # hổ phách (gờ mày ochre không lọt)
    hp = cv2.morphologyEx(hp.astype(np.uint8), cv2.MORPH_CLOSE, el(4))
    n, lab, st, _ = cv2.connectedComponentsWithStats(hp, 8)
    hp = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    f = hp.astype(np.uint8).copy()
    h_, w_ = f.shape
    m2 = np.zeros((h_ + 2, w_ + 2), np.uint8)
    cv2.floodFill(f, m2, (0, 0), 2)
    trong = (f != 2)                                                                  # lấp con ngươi, chấm sáng
    ngoai = cv2.dilate(trong.astype(np.uint8), el(5)).astype(bool)                    # + viền mực
    a = cv2.GaussianBlur(ngoai.astype(np.float32), (0, 0), 0.8)
    ys, xs = np.nonzero(a > 0.04)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    out = np.dstack([A[y0:y1, x0:x1].astype(np.uint8), (np.clip(a[y0:y1, x0:x1] * 1.3, 0, 1) * 255).astype(np.uint8)])
    os.makedirs(CUNG, exist_ok=True)
    Image.fromarray(out, "RGBA").save(os.path.join(CUNG, "mat.png"))
    pd = os.path.join(CUNG, "dat.json")
    DAT = json.load(open(pd, encoding="utf-8")) if os.path.exists(pd) else {}
    DAT["mat"] = {"slot": SLOT["mat"], "hop": [int(x0), int(y0), int(x1), int(y1)], "nguon": "L1_duyet.png (cắt thẳng)", "phu": 1.0}
    json.dump(DAT, open(pd, "w", encoding="utf-8"), indent=1)
    print("mat", x0, y0, x1, y1)


def ghep():
    DAT = json.load(open(os.path.join(CUNG, "dat.json"), encoding="utf-8"))
    A = Image.open(CONCEPT).convert("RGB").resize((W, H))
    nen = Image.blend(Image.new("RGB", (W, H), "white"), A, 0.25).convert("RGBA")
    thu_tu = ["maoC", "maoB", "maoA", "vong", "mieng", "ham", "nanh1", "nanh2", "dau", "may", "mat"]
    for k in thu_tu:
        if k in DAT:
            x0, y0, _, _ = DAT[k]["hop"]
            nen.alpha_composite(Image.open(os.path.join(CUNG, k + ".png")), (x0, y0))
    c = Image.new("RGB", (W * 2 // 2, H), "white")
    c.paste(nen.convert("RGB"))
    c.crop((560, 220, 1120, 700)).resize((1120, 960), Image.LANCZOS).save(os.path.join(MAU, "_ghep_cung.png"))
    print(os.path.join(MAU, "_ghep_cung.png"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "prompt":
        prompt()
    elif a[0] == "cat":
        cat()
    elif a[0] == "ghep":
        ghep()
    elif a[0] == "mat":
        mat()
