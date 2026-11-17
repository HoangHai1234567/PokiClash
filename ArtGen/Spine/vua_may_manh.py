# -*- coding: utf-8 -*-
"""Vua robot (vua_may, rig monster_3637): MẢNH theo concept B3 đã duyệt (inbox/vua_may_1/tai_ve/L1_duyet.png = L3_B: giáp vàng + bạc, áo
choàng đỏ viền lông trắng, dải xanh, vương miện nguyệt quế, mặt xám mắt vàng, râu bạc chẻ đôi, quyền trượng bạc đầu tháp vàng + MẶT TRỜI,
TRÁI ĐẤT / SAO HỎA / SAO THỦY lơ lửng, chân robot vàng bạc, bốn cánh lông vũ trắng ba tầng ngọn vàng, vòng hào quang nguyệt quế).

Concept thẳng mặt và hẹp thân hơn rig (lệch tới ~40 px ở tay, đầu cao hơn), nên làm như robot cổ:
  K1..K5: mảnh GIỮ HÌNH BÓNG GỐC (tờ = mảnh gốc cắt theo lưới, phóng to; GPT đổi da theo B3): áo choàng sau + trước, ngực | giáp vai, dải
          xanh | cẳng tay, bắp tay, khớp vai | lưng, bụng, khối hông, khớp cổ / eo | bàn tay, ngón, cổ tay, bánh răng + răng.
  G1..G8: mảnh ĐỔI DÁNG và mảnh MỚI, gen "đúng chỗ, đúng cỡ" trên concept: G1 vương miện, râu + ria, Mặt Trời, ba hành tinh | G2 mặt, cán
          trượng + đầu tháp | G3 hai bàn chân + hai đùi | G4 hai ống chân + vòng hào quang | G5 hai giáp gối + bốn tay cánh | G6 lông dài
          (tầng ngoài) bốn cánh | G7 tầng lông giữa | G8 tầng lông phủ. Toạ độ concept → thế giới (khung 0 idle đã nâng DY) qua phép căn mốc;
          đầu neo theo vương miện, trượng theo đầu tháp, Mặt Trời / hành tinh theo đúng mảnh của họ mà nó thay.

    vua_may_manh.py can        căn concept lên sơ đồ bố cục bằng mốc → mau/can.json
    vua_may_manh.py to         dựng mọi tờ K + file prompt K, G → mau/goc_K*.png, gui_gpt/vua_may_1/luot_4_*.txt
    vua_may_manh.py cat [K|G|<tờ>]   cắt ảnh về → manh/<vùng>.png, manh/moi.json, tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vua_may as G  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES (atlas họ 0,5 px / đơn vị → mình 1 px / đơn vị)
GUI = os.path.join(HERE, "gui_gpt", "vua_may_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
ROBOT_CO = os.path.join(HERE, "inbox", "robot_co_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
INK = (43, 33, 24)
MUC = "#2B2118"
# màu đo trên concept B3 (trung vị ô 7 × 7)
M = dict(vang="#F9B825", vang_toi="#D9961B", bac="#B4B4B7", bac_toi="#8E8E93", sat="#59585D", gang="#4A494E", do="#C72F2B",
         do_toi="#8E1F1F", long="#FDF3DE", xanh="#2167E3", mat="#7E7876", rau="#CBCCCD", mat_vang="#FFD24A")
MO_TA_CON = ("a majestic robot king seen in three-quarter view, gold and silver armour with ONE gold trim on each piece and very few "
             "rivets, a red royal cape with a white fur trim and a big gold gear emblem over the left shoulder, a blue sash with a gold gear "
             "emblem over the right shoulder, a gold crown with battlements and a gold laurel wreath, a grey face with yellow eyes, a silver "
             "moustache and a split silver beard, huge silver forearms with gold bands, dark steel gloved hands, a silver scepter with a gold "
             "tower top and a little Sun on it, small floating planets (Earth, Mars, Mercury), two sturdy robot legs with gold feet, four "
             "white feathered wings with gold tips and a laurel halo behind")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


# ================================================================ căn concept bằng mốc
# (px sơ đồ bố cục, px concept B3): mốc đọc trên ảnh kẻ lưới (vua_may_ghichu.md mục 8). Phép đồng dạng không xoay, bình phương tối thiểu.
MOC = {
    "mat_troi": ((652, 515), (598, 493)), "dau_thap": ((651, 571), (600, 545)), "nam_gan": ((614, 695), (622, 720)),
    "nam_xa": ((810, 660), (755, 640)), "vuong_mien": ((865, 414), (835, 350)), "hong": ((821, 815), (820, 830)),
    "cang_gan": ((513, 719), (510, 715)), "cang_xa": ((927, 683), (920, 680)),
}


def can():
    L = np.array([v[0] for v in MOC.values()], float)
    C = np.array([v[1] for v in MOC.values()], float)
    A = np.zeros((2 * len(L), 3))
    b = np.zeros(2 * len(L))
    A[0::2, 0], A[0::2, 1], b[0::2] = L[:, 0], 1, C[:, 0]
    A[1::2, 0], A[1::2, 2], b[1::2] = L[:, 1], 1, C[:, 1]
    a, tx, ty = np.linalg.lstsq(A, b, rcond=None)[0]
    J = json.load(open(os.path.join(G.MAU, "bo_cuc.json")))
    du = {k: (np.array(v[1]) - (a * np.array(v[0]) + [tx, ty])).round(1).tolist() for k, v in MOC.items()}
    out = dict(a=float(a), tx=float(tx), ty=float(ty), s=J["s"], cx=J["cx"], cy=J["cy"], DY=J["DY"], du=du)
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1, ensure_ascii=False)
    print("căn:", {k: v for k, v in out.items() if k != "du"})
    print("lệch từng mốc (px concept):", du)
    return out


def phep_can():
    """(T: thế giới khung 0 idle ĐÃ NÂNG → px concept, Ti: ngược lại, px concept / đơn vị)."""
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, a, tx, ty = j["s"], j["cx"], j["cy"], j["a"], j["tx"], j["ty"]

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        P = np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
        return a * P + np.array([tx, ty])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([tx, ty])) / a
        return np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return T, Ti, s * a


def tam_ho(slot):
    """tâm hình của part của họ ở khung 0 idle, thế giới ĐÃ NÂNG DY (mọi part của thân nằm dưới khối hông hoặc đầu trượng)."""
    D = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    DY = json.load(open(os.path.join(G.MAU, "can.json")))["DY"]
    for a in D["atts"]:
        if a["slot"] == slot and a.get("cur"):
            return np.array(a["xy"], float).reshape(-1, 2).mean(0) + [0, DY]
    raise KeyError(slot)


# ================================================================ K: mảnh giữ hình bóng gốc (tờ = mảnh gốc phóng to)
TO_K = {
    "K1": [[("pifenghou_01", 1.7), ("pifengqian", 1.7), ("xiongqiong", 1.7)]],
    "K2": [[("jianjia_r", 2.0), ("jianjia_l", 2.0), ("jian_l", 2.0), ("jian_r", 2.0)]],
    "K3": [[("xiaobi_r_02", 2.4), ("xiaobi_r_01", 2.4), ("xiaobi_l_02", 2.4), ("xiaobi_l_01", 2.4)],
           [("dabi_r_02", 2.0), ("dabi_r_03", 2.0), ("dabi_r_01", 2.0), ("dabi_l_01", 2.0), ("dabi_l", 2.0), ("dabi_l_02", 2.0)]],
    "K4": [[("beibu", 2.4), ("fubu", 2.4), ("xiabanshen_02", 2.4)],
           [("xiabanshen_01", 2.4), ("xiabanshen_05", 2.4), ("xiabanshen_04", 2.4), ("xiabanshen_06", 2.4), ("xiabanshen_07", 2.4)]],
    "K5": [[("shouzhang_r", 3.0), ("shouzhang_l", 3.0), ("damuzhi_r", 3.0), ("damuzhi_l", 3.0)],
           [("zhongzhi_r", 3.0), ("shizhi_r", 3.0), ("zhongzhi_l", 3.0), ("shizhi_l", 3.0), ("shouwan__r", 3.0), ("shouwan_l", 3.0)],
           [("fatiao", 3.0), ("fatiao_1", 3.0), ("fatiao_3", 6.0)]],
}
VI_K = {"K1": "áo choàng sau (dài), áo choàng trước (vắt vai), ngực",
        "K2": "giáp vai trái / phải, hai mảnh dải xanh",
        "K3": "hai cẳng tay (vỏ sau + vỏ trước), bắp tay, khớp vai, khớp khuỷu",
        "K4": "tấm lưng, tấm bụng chữ Y, khối hông, cột eo, các khớp cổ / eo nhỏ",
        "K5": "hai mu bàn tay, hai ngón cái, bốn ngón, hai cổ tay, bánh răng mặt trước / sau, một răng bánh răng"}
TOM_K = {"K1": "three big parts: the long back part of a royal cape, the front part of the cape that lies over the left shoulder, the "
               "barrel chest of the robot",
         "K2": "four parts: the big left shoulder pad, the right shoulder pad, two pieces of a diagonal sash",
         "K3": "top row: the back and the front shells of the left forearm, the back and the front shells of the right forearm; bottom row: "
               "six small arm parts (upper-arm cylinders, round shoulder balls, an elbow ball)",
         "K4": "top row: the back plate, the Y-shaped belly plate, the wide hip block; bottom row: the waist column and four small joint "
               "pieces",
         "K5": "top row: the back-of-hand plates and the two thumbs; middle row: four fingers and two round wrist balls; bottom row: a gear "
               "wheel (front face), the same gear (back face) and ONE gear tooth drawn very big"}
_ = M
MO_TA_K = {
    "pifenghou_01": f"the long BACK part of the royal CAPE hanging down: flat red {_['do']}; a wide fluffy WHITE FUR trim {_['long']} (simple "
                    "round scalloped tufts, each with an ink outline) along its long LEFT outer edge and along its BOTTOM edge; ONE big "
                    f"simple gold {_['vang']} gear shape (a ring with eight square teeth and a round hole) in its lower middle; nothing else.",
    "pifengqian": f"the FRONT part of the cape lying over the left shoulder: flat red {_['do']}; a white fur trim {_['long']} along its lower "
                  f"right edge; ONE big simple gold {_['vang']} gear emblem in its middle instead of the gold pattern of image 1; nothing "
                  "else.",
    "xiongqiong": f"the barrel CHEST: a broad chest plate of flat silver {_['bac']} with ONE gold {_['vang']} trim along its outer rim; the "
                  f"dark oval at its top (the neck opening) very dark steel {_['sat']}; the vent GRILLE: a gold frame with four dark "
                  "vertical slots; the small blue dot becomes a small round gold rivet; no other details.",
    "jianjia_r": f"the big LEFT SHOULDER PAD (a thick curved armour plate): flat silver {_['bac']}, its lower side face darker silver "
                 f"{_['bac_toi']}, ONE gold {_['vang']} trim along its outer rim, two small round gold rivets; nothing else.",
    "jianjia_l": "the RIGHT SHOULDER PAD: the same design as the left shoulder pad.",
    "jian_l": f"a piece of the diagonal SASH: flat royal blue {_['xanh']} with a thin gold {_['vang']} edge along both long sides and ONE simple "
              "gold gear emblem where image 1 has one; remove the yellow dashes.",
    "jian_r": "another piece of the SASH: the same design.",
    "xiaobi_r_02": f"the BACK shell of the LEFT FOREARM: a thick gold {_['vang']} cuff ring round a very dark steel {_['sat']} hollow (its "
                   f"inside), one darker gold {_['vang_toi']} rim line.",
    "xiaobi_r_01": f"the FRONT shell of the LEFT FOREARM (a big rounded armour shell): flat silver {_['bac']} with ONE wide gold {_['vang']} "
                   "band round its wrist end and a thin gold rim along its edge, two small gold rivets.",
    "xiaobi_l_02": "the BACK shell of the RIGHT FOREARM: the same design as the back shell of the left forearm.",
    "xiaobi_l_01": "the FRONT shell of the RIGHT FOREARM: the same design as the front shell of the left forearm.",
    "dabi_r_02": f"an UPPER-ARM cylinder: very dark steel {_['sat']}, one gold {_['vang']} ring line near its lower end; the small blue dot "
                 "becomes a small gold rivet.",
    "dabi_r_03": f"a dark steel {_['sat']} block (the upper arm behind the shoulder): plain, one rim line.",
    "dabi_r_01": f"a round SHOULDER JOINT BALL: flat gold {_['vang']} with a darker gold {_['vang_toi']} round disc on its face.",
    "dabi_l_01": "another round SHOULDER JOINT BALL: the same.",
    "dabi_l": "another UPPER-ARM cylinder: the same as the first one.",
    "dabi_l_02": f"a round ELBOW BALL: dark steel {_['sat']}, one small gold ring.",
    "beibu": f"the BACK PLATE (a rounded block, mostly hidden behind the chest): flat silver {_['bac']} with a gold {_['vang']} rim.",
    "fubu": f"the Y-shaped BELLY PLATE: a gold {_['vang']} outer frame with a plain silver {_['bac']} inset panel in its middle.",
    "xiabanshen_02": f"the wide HIP BLOCK (three boxes side by side): very dark steel {_['sat']}, each box with a thin gold {_['vang']} rim "
                     "line.",
    "xiabanshen_01": f"the WAIST COLUMN (a cylinder with a small block under it): very dark steel {_['sat']}, one gold {_['vang']} band.",
    "xiabanshen_05": f"a small NECK JOINT with gear teeth: very dark steel {_['sat']}, a small gold {_['vang']} hub.",
    "xiabanshen_04": "another small NECK JOINT with gear teeth: the same.",
    "xiabanshen_06": f"a small dark steel {_['sat']} block: plain.",
    "xiabanshen_07": f"a small dark steel {_['sat']} gear: a small gold {_['vang']} hub.",
    "shouzhang_r": f"a BACK-OF-HAND armour plate: flat gold {_['vang']}, one darker gold {_['vang_toi']} rim line.",
    "shouzhang_l": "another BACK-OF-HAND plate: the same.",
    "damuzhi_r": f"a THUMB (two segments): dark steel glove {_['gang']}; its gold base plate stays gold {_['vang']}.",
    "damuzhi_l": f"another THUMB: dark steel glove {_['gang']}.",
    "zhongzhi_r": f"a FINGER: dark steel glove {_['gang']}, one small gold {_['vang']} band.",
    "shizhi_r": "a FINGER: the same.",
    "zhongzhi_l": "a FINGER: the same.",
    "shizhi_l": "a FINGER: the same.",
    "shouwan__r": f"a round WRIST BALL: dark steel {_['sat']}.",
    "shouwan_l": "a round WRIST BALL: the same.",
    "fatiao": f"a GEAR WHEEL (front face): very dark steel {_['sat']} with a round gold {_['vang']} hub in its middle; keep every tooth.",
    "fatiao_1": f"the same GEAR WHEEL seen from the back: dark steel {_['gang']}, plain, keep every tooth.",
    "fatiao_3": f"ONE GEAR TOOTH (a small square block): very dark steel {_['sat']}.",
}


def vung():
    """{slot hoặc vùng: (att, ảnh part cắt theo lưới)} theo dáng gốc (att_goc)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    AG = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in AG["atts"]:
        if a.get("region") not in imgs:
            continue
        out.setdefault(a["region"], (a, G.part_goc(a)))
        out.setdefault(a["slot"], (a, G.part_goc(a)))
    return out


def to_k(ten):
    V = vung()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    cao = []
    for h_ in TO_K[ten]:
        cs = []
        for r, z in h_:
            im = V[r][1]
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, z, big))
        cao.append((cs, max(c[2].height for c in cs)))
    ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
    y = ke_y
    for cs, hh in cao:
        ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
        assert ke > 12 and ke_y > 12, (ten, ke, ke_y)
        x = ke
        for r, z, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z, vung=V[r][0]["region"])
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, f"goc_{ten}.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(ten, o):
    mau = os.path.join(G.MAU, f"goc_{ten}.png")
    out = os.path.join(G.TAI, f"D_{ten}.png")
    p = os.path.join(GUI, f"luot_4_da_{ten}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: {TOM_K[ten]} of a 2D animation puppet (a big robot king), "
         "each drawn alone, at the exact size and place to keep. They are painted in a smooth digital style with glossy yellow gold, olive "
         "brown metal, a pink-red cape and a blue sash.",
         f"image 2 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}. Take from it the "
         "colours, the materials and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). The shapes come from "
         "image 1.",
         f"image 3 = {Wp(ROBOT_CO)}: another approved hero of the same game: the hand-drawn ink and crayon style to match. Do NOT copy "
         "its design.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ten}_2.png, D_{ten}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one). Do NOT merge parts, do NOT add parts, "
         "do NOT move parts. Pure white (#FFFFFF) between the parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): hand-drawn on paper: a wobbly dark-brown ink outline ({MUC}, "
         "about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the inner lines, and every "
         "area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. Do NOT copy the painting style of image 1 "
         "(no glossy gold, no olive brown, no soft light and dark planes, no shine spots); no shading, no highlights, no white shine "
         "streaks, no gradients, no glow, no shadows: flat colour only. SIMPLE and CLEAN like image 2: big plain areas, no extra rivets, "
         "no engravings, no scratches.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {MO_TA_K[r]}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p, mau, out


def nen_trang(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def _to_so(ims, p):
    w_ = sum(i.width + 10 for i in ims) + 10
    h_ = max(i.height for i in ims) + 20
    o = Image.new("RGB", (w_, h_), (150, 150, 150))
    x = 10
    for i in ims:
        o.paste(i, (x, 10), i)
        x += i.width + 10
    o.save(p)
    print(p)


def cat_k(ten):
    path = anh.to_moi_nhat(G.TAI, f"D_{ten}")
    if not path:
        print(f"{ten}: chưa gen")
        return
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print(f"{ten}:", os.path.basename(path))
    o = json.load(open(os.path.join(G.MAU, f"goc_{ten}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ten}.png")).convert("RGB")).astype(np.int32)
    fg = ~nen_trang(A)
    fgG = ~nen_trang(Gd)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    so = []
    for r, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 14
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
        sub = lab[y0:y1, x0:x1]
        ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 30]
        m = np.isin(lab, ids)
        m[:y0] = m[y1:] = False
        m[:, :x0] = m[:, x1:] = False
        rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
        mm = m[y:y + ch, x:x + cw]
        al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
        vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
        sang = rgb.min(2).astype(np.float32)
        al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
        im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
        goc = V[r][1]
        tw, th = goc.width * RES, goc.height * RES
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
        thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
        if thieu.any() and (a2[..., 3] >= 128).any():
            co = (a2[..., 3] >= 128).astype(np.uint8)
            _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys_, xs_ = np.nonzero(co)
            bang = np.zeros((lbl.max() + 1, 3), np.uint8)
            bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
            a2[thieu, :3] = bang[lbl[thieu]]
            a2[thieu, 3] = 255
        Image.fromarray(a2, "RGBA").save(os.path.join(MANH, d["vung"] + ".png"))
        b = fgG[y:y + ch, x:x + cw]
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        ious[r] = round(iou, 3)
        so.append(Image.fromarray(a2, "RGBA"))
        print(f"  {r:14s} → {d['vung']}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, f"_so_{ten}.png"))


# ================================================================ G: mảnh đổi dáng + mảnh mới, gen đúng chỗ, đúng cỡ trên concept
# mỗi mảnh: (tên, nhóm gán (vung: hộp px concept để gán cụm), slot của họ mà nó thay (None = mảnh mới), xương bám, neo, tả tiếng Anh)
# neo: "dau" = cả cụm đầu neo theo vương miện (touguan); "<slot>" = tâm mảnh neo vào tâm part đó của họ; None = phép căn chung
TOP_GAN, TOP_XA = (0, 0, 760, 440), (760, 0, 1536, 440)
DUOI_GAN, DUOI_XA = (0, 440, 760, 760), (760, 440, 1536, 760)
GTO = {
    "G1": [("vuong_mien", (700, 220, 990, 425), "touguan", "touguan", "dau",
            "the CROWN: the gold crown with its battlements, its gold LAUREL wreath and its row of pearls, complete (its back rim too)"),
           ("rau", (720, 420, 960, 560), "toufa_01", "toufa_01", "dau",
            "the silver MOUSTACHE and the split silver BEARD under it, as ONE piece, complete (the part of the beard hidden behind the "
            "crown or the cape drawn too)"),
           ("mat_troi", (540, 435, 660, 550), "fazhang_06", "fazhang_06", "fazhang_06",
            "the little SUN on top of the scepter: the yellow ball with its ring of orange flame points, complete"),
           ("trai_dat", (520, 220, 650, 345), "fazhang_05", "fazhang_05", "fazhang_05",
            "the EARTH: the round blue planet with green continents and white clouds, complete"),
           ("sao_hoa", (550, 340, 630, 400), "fazhang_04", "fazhang_04", "fazhang_04",
            "MARS: the small round rusty red planet with darker craters, complete"),
           ("sao_thuy", (560, 395, 625, 445), "fazhang_03", "fazhang_03", "fazhang_03",
            "MERCURY: the smallest round grey planet with darker craters, complete")],
    "G2": [("mat", (720, 330, 960, 560), "bizi", "xiabanshen_04", "dau",
            "the FACE of the robot king WITHOUT the crown and WITHOUT the moustache and beard: the grey face plate with the two yellow eyes "
            "and the nose guard, complete as one closed rounded head shape (the top of the head that is hidden under the crown and the "
            "lower face hidden behind the beard are drawn too, plain grey)"),
           ("truong", (560, 500, 650, 1000), "fazhang_01", "fazhang_01", "fazhang_02",
            "the SCEPTER WITHOUT the Sun on top: the gold tower-shaped top and the long silver SHAFT with its gold rings, complete from "
            "the tower top down to its gold foot cap on the ground (the part hidden behind the glove drawn too)")],
    "G3": [("chan_gan_ban", (520, 900, 790, 1010), None, "ban_gan", None,
            "the LEFT robot FOOT (the gold foot with its blunt toes, on the left), complete (its top part hidden under the shin drawn too)"),
           ("chan_xa_ban", (800, 900, 1100, 1010), None, "ban_xa", None,
            "the RIGHT robot FOOT (the gold foot with its blunt toes, on the right), complete"),
           ("chan_gan_dui", (600, 760, 790, 880), None, "dui_gan", None,
            "the LEFT THIGH: the upper part of the left leg from the hip down to the knee (silver and gold armour), complete (its top "
            "hidden under the body and the cape drawn too, and its lower end hidden under the knee guard)"),
           ("chan_xa_dui", (800, 760, 1000, 880), None, "dui_xa", None,
            "the RIGHT THIGH: the upper part of the right leg from the hip down to the knee, complete")],
    "G4": [("chan_gan_ong", (600, 820, 790, 960), None, "ong_gan", None,
            "the LEFT SHIN: the lower part of the left leg from the knee down to the ankle (silver with gold bands), complete (its top "
            "hidden under the knee guard and its bottom hidden in the foot drawn too)"),
           ("chan_xa_ong", (800, 820, 1000, 960), None, "ong_xa", None,
            "the RIGHT SHIN: the lower part of the right leg from the knee down to the ankle, complete"),
           ("hao_quang", (450, 0, 1100, 520), None, "hao_quang", None,
            "the round HALO behind the king (the gold laurel ring with its light rays and pearls), complete as a FULL CIRCLE: the parts "
            "hidden behind the crown, the head, the body and the wings are drawn too")],
    "G5": [("chan_gan_goi", (600, 760, 790, 900), None, "ong_gan", None,
            "the LEFT KNEE GUARD (the big round armour cap on the left knee), complete"),
           ("chan_xa_goi", (800, 760, 1020, 900), None, "ong_xa", None,
            "the RIGHT KNEE GUARD (the big round armour cap on the right knee), complete"),
           ("canh_tren_gan_tay", TOP_GAN, None, "cw_tren_gan_tay", None,
            "the ARM of the UPPER LEFT wing (the silver frame with its gold jewels along the top edge of the wing), complete"),
           ("canh_tren_xa_tay", TOP_XA, None, "cw_tren_xa_tay", None,
            "the ARM of the UPPER RIGHT wing, complete"),
           ("canh_duoi_gan_tay", DUOI_GAN, None, "cw_duoi_gan_tay", None,
            "the ARM of the LOWER LEFT wing, complete"),
           ("canh_duoi_xa_tay", DUOI_XA, None, "cw_duoi_xa_tay", None,
            "the ARM of the LOWER RIGHT wing, complete")],
    "G6": [(f"canh_{k}_ngoai", hop, None, f"cw_{k}_ngoai", None,
            f"the OUTER tier of the {vi} wing: its row of very LONG flight feathers with gold tips, complete (their bases hidden under the "
            "middle tier and the arm drawn too, reaching up to the wing arm)")
           for k, hop, vi in (("tren_gan", TOP_GAN, "UPPER LEFT"), ("tren_xa", TOP_XA, "UPPER RIGHT"), ("duoi_gan", DUOI_GAN, "LOWER LEFT"),
                              ("duoi_xa", DUOI_XA, "LOWER RIGHT"))],
    "G7": [(f"canh_{k}_giua", hop, None, f"cw_{k}_giua", None,
            f"the MIDDLE tier of the {vi} wing: its row of medium feathers, complete (their bases hidden under the small top feathers and "
            "the arm drawn too)")
           for k, hop, vi in (("tren_gan", TOP_GAN, "UPPER LEFT"), ("tren_xa", TOP_XA, "UPPER RIGHT"), ("duoi_gan", DUOI_GAN, "LOWER LEFT"),
                              ("duoi_xa", DUOI_XA, "LOWER RIGHT"))],
    "G8": [(f"canh_{k}_phu", hop, None, f"cw_{k}_phu", None,
            f"the INNER tier of the {vi} wing: its row of small rounded covert feathers right under the wing arm, complete (the part "
            "hidden under the arm drawn too)")
           for k, hop, vi in (("tren_gan", TOP_GAN, "UPPER LEFT"), ("tren_xa", TOP_XA, "UPPER RIGHT"), ("duoi_gan", DUOI_GAN, "LOWER LEFT"),
                              ("duoi_xa", DUOI_XA, "LOWER RIGHT"))],
}
VI_G = {"G1": "vương miện, râu + ria, Mặt Trời, Trái Đất, Sao Hỏa, Sao Thủy", "G2": "mặt (không vương miện, không râu), cán trượng + đầu tháp",
        "G3": "hai bàn chân, hai đùi", "G4": "hai ống chân, vòng hào quang (đủ vòng)", "G5": "hai giáp gối, bốn tay cánh",
        "G6": "tầng lông dài (ngoài) bốn cánh", "G7": "tầng lông giữa bốn cánh", "G8": "tầng lông phủ (trong) bốn cánh"}


def prompt_g():
    ps = []
    for ma, ds in GTO.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_4_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: {MO_TA_CON}.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} piece{'s' if len(ds) > 1 else ''} listed below, each in the SAME POSITION, at "
             "the SAME SIZE and with the SAME colours as in image 1 (if your picture were laid over image 1, every piece must sit exactly "
             "on its old place). REMOVE everything else (the body, the other parts, everything not listed) and leave pure white there. "
             "COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden "
             "behind other things in image 1 are drawn too, continuing its shape naturally." +
             (" The pieces stay separate from each other (leave a little white gap between them, do not merge them)." if len(ds) > 1
              else ""), "", "THE PIECE" + ("S:" if len(ds) > 1 else ":")]
        t += [f"{i}. {mt}." for i, (_, _, _, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the inner "
              "lines (feather quills, trims), every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No "
              "shading, no highlights, no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


def cat_g(ma):
    """tờ M_<ma>: mỗi cụm liền (trên nền trắng) về mảnh có hộp gán chứa tâm cụm (nhiều mảnh cùng hộp: gần tâm hộp nhất); ghi
    manh/<tên>.png (1 px / đơn vị rig) + moi.json (4 góc thế giới khung 0 idle đã nâng, slot thay, xương)."""
    T, Ti, spx = phep_can()
    path = anh.to_moi_nhat(G.TAI, f"M_{ma}")
    if not path:
        print(f"{ma}: chưa gen")
        return []
    print(f"{ma}:", os.path.basename(path))
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
    fg = (~nen_trang(rgb.astype(np.int32))).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
    ds = GTO[ma]
    gan = {d[0]: [] for d in ds}
    for i in range(1, n):
        if st[i, 4] < 150:
            continue
        cx, cy = cen[i]
        ung = [d for d in ds if d[1][0] <= cx < d[1][2] and d[1][1] <= cy < d[1][3]]
        if not ung:
            print(f"  cụm {i} tâm ({cx:.0f},{cy:.0f}) {st[i, 4]} px: không thuộc mảnh nào, bỏ")
            continue
        d = min(ung, key=lambda d: np.hypot(cx - (d[1][0] + d[1][2]) / 2, cy - (d[1][1] + d[1][3]) / 2))
        gan[d[0]].append(i)
    k = 1.0 / spx                                           # px tờ → 1 px / đơn vị rig
    dau = None
    so = []
    for ten, hop, sl, bn, neo, _ in ds:
        if not gan[ten]:
            print(f"  {ten}: KHÔNG thấy mảnh")
            continue
        mm0 = np.isin(lab, gan[ten])
        trong = (rgb.min(2) > 236) & mm0                    # giấy trắng KHÉP KÍN trong mảnh (lòng vòng hào quang): trong suốt
        mm0 = cv2.morphologyEx(mm0.astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
        if ten == "hao_quang":
            nt = nen_trang(rgb.astype(np.int32)) | (rgb.min(2) > 236)
            n2, l2, s2, _ = cv2.connectedComponentsWithStats((rgb.min(2) > 236).astype(np.uint8), 4)
            for j in range(1, n2):
                if s2[j, 4] > 2000:
                    mm0 &= ~(l2 == j)
        ys, xs = np.nonzero(mm0)
        pad = 4
        x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
        mm = mm0[y0:y1 + 1, x0:x1 + 1]
        al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
        rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
        out = Image.fromarray(rgba, "RGBA").convert("RGBa")
        out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(MANH, ten + ".png"))
        hop4 = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
        tg = Ti(hop4)
        tam_c = Ti([[(x0 + x1) / 2, (y0 + y1) / 2]])[0]
        lech = np.zeros(2)
        if neo == "dau":                                     # cả cụm đầu theo vương miện: tâm vương miện concept → tâm touguan của họ
            if dau is None:
                if "_dau" in moi:
                    dau = np.array(moi["_dau"], float)
                elif ten == "vuong_mien":
                    dau = tam_ho("touguan") - tam_c
                    moi["_dau"] = dau.tolist()
            lech = dau if dau is not None else lech
        elif neo:
            lech = tam_ho(neo) - Ti([np.array(MOC_TAM[ten])])[0] if ten in MOC_TAM else tam_ho(neo) - tam_c
        tg = tg + lech
        moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=tg.tolist(), to=ma,
                        lech=lech.round(1).tolist())
        so.append(out)
        print(f"  {ten:18s} hộp {x0},{y0}–{x1},{y1} → {ten}.png {out.size}  (thay {sl}, xương {bn}, neo {neo}, lệch {lech.round(0)})")
    json.dump(moi, open(pj, "w"), indent=1)
    if so:
        _to_so(so, os.path.join(MANH, f"_so_{ma}.png"))
    return so


# tâm neo đọc trên concept (px) cho mảnh neo theo part của họ mà tâm hình KHÔNG trùng tâm part (trượng: neo đầu tháp)
MOC_TAM = {"truong": (600, 545), "mat_troi": (598, 493), "trai_dat": (585, 285), "sao_hoa": (590, 370), "sao_thuy": (590, 420)}


def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 4")[0].rstrip("\n")
    gd = ["", "## Lượt 4: mảnh theo concept B3 đã duyệt (2026-11-17)", "",
          "Claude tự gen và tự cắt; người dùng không cần làm gì. Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, vi in ps:
        gd += [f"- **{ten}** ({vi}): chỉ gửi GPT đường dẫn `{Wp(p)}`."]
    gd += ["", "Cắt: `py -3 -I ArtGen/Spine/vua_may_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    ps = []
    for ten in TO_K:
        p, _, _ = prompt_k(ten, to_k(ten))
        ps.append((ten, p, VI_K[ten]))
    for ma, p, _ in prompt_g():
        ps.append((ma, p, VI_G[ma]))
    huong_dan(ps)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ten in TO_K:
            if chi in ("", "K", ten):
                cat_k(ten)
        for ma in GTO:
            if chi in ("", "G", ma):
                cat_g(ma)
    else:
        print(__doc__)


# ================================================================ tách mảnh dính nhau trên tờ G1 (vương miện + râu; Mặt Trời + ba hành tinh)
TACH_G1 = {"vuong_mien": (835, 345), "rau": (835, 500), "trai_dat": (585, 270), "sao_hoa": (588, 352), "sao_thuy": (588, 402),
           "mat_troi": (595, 478)}


def tach_g1():
    """vùng lòng tô (không mực, không trắng) chia theo tâm gần nhất; mọi điểm của hình (cả viền) về lòng tô gần nhất → ghi đè mảnh G1."""
    T, Ti, spx = phep_can()
    path = anh.to_moi_nhat(G.TAI, "M_G1")
    rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
    A = rgb.astype(np.int32)
    fg = ~nen_trang(A)
    lum = A.mean(2)
    trang = rgb.min(2) > 236
    muc = (lum < 60) | ((lum < 75) & (A[..., 0] - A[..., 2] > 22))
    long_ = fg & ~muc & ~trang
    long_ = cv2.erode(long_.astype(np.uint8), el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(long_.astype(np.uint8), 8)
    ten = list(TACH_G1)
    C = np.array([TACH_G1[k] for k in ten], float)
    gan = np.full(n, -1)
    for i in range(1, n):
        if st[i, 4] >= 12:
            gan[i] = int(np.argmin(np.hypot(*(C - cen[i]).T)))
    hop = (lab > 0) & (gan[lab] >= 0)
    _, lbl = cv2.distanceTransformWithLabels((~hop).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(hop)
    bang = np.full(lbl.max() + 1, -1)
    bang[lbl[ys, xs]] = gan[lab[ys, xs]]
    thuoc = bang[lbl]
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    ds = {d[0]: d for d in GTO["G1"]}
    k = 1.0 / spx
    so = []
    for j, t in enumerate(ten):
        mm0 = fg & (thuoc == j)
        nn, ll, ss, _ = cv2.connectedComponentsWithStats(mm0.astype(np.uint8), 8)
        if nn < 2:
            print(f"  {t}: KHÔNG thấy")
            continue
        k0 = 1 + int(np.argmax(ss[1:, 4]))
        mm0 = ll == k0
        ys, xs = np.nonzero(mm0)
        x0, y0, x1, y1 = xs.min() - 4, ys.min() - 4, xs.max() + 4, ys.max() + 4
        mm = mm0[y0:y1 + 1, x0:x1 + 1]
        al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
        rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
        out = Image.fromarray(rgba, "RGBA").convert("RGBa")
        out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
        out.save(os.path.join(MANH, t + ".png"))
        _, _, sl, bn, neo, _ = ds[t]
        hop4 = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
        tam_c = Ti([[(x0 + x1) / 2, (y0 + y1) / 2]])[0]
        if neo == "dau":
            if t == "vuong_mien":
                moi["_dau"] = (tam_ho("touguan") - tam_c).tolist()
            lech = np.array(moi["_dau"], float)
        else:
            lech = tam_ho(neo) - Ti([np.array(MOC_TAM.get(t, ((x0 + x1) / 2, (y0 + y1) / 2)))])[0]
        moi[t] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=(Ti(hop4) + lech).tolist(), to="G1",
                      lech=lech.round(1).tolist())
        so.append(out)
        print(f"  {t:12s} hộp {x0},{y0}–{x1},{y1} → {t}.png {out.size} lệch {lech.round(0)}")
    # mặt dùng chung phép neo đầu (đã ghi lại theo vương miện mới)
    if "mat" in moi and "_dau" in moi:
        d = moi["mat"]
        hop4 = np.array([[d["hop"][0], d["hop"][1]], [d["hop"][2], d["hop"][1]], [d["hop"][2], d["hop"][3]], [d["hop"][0], d["hop"][3]]], float)
        d["the_gioi"] = (Ti(hop4) + np.array(moi["_dau"])).tolist()
        d["lech"] = np.round(moi["_dau"], 1).tolist()
    json.dump(moi, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, "_so_G1.png"))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "tach_g1":
    tach_g1()


# ================================================================ G9: vẽ lại hai bàn chân (người dùng 2026-11-17: "lòng bàn chân xấu quá")
GTO["G9"] = [("chan_gan_ban", (480, 880, 800, 1024), None, "ban_gan", None,
              "the LEFT FOOT, REDESIGNED as a solid heavy ROBOT BOOT seen from the front: a wide rounded GOLD toe cap divided into THREE "
              f"broad segments by two ink lines (no separate rounded toes), a plain silver {M['bac']} ankle plate on top of it (its top part "
              f"goes up under the leg guard), and a thick flat dark steel {M['sat']} SOLE along the whole bottom; same place, same width and "
              "the same bottom line as the old foot, a little taller (its top hidden under the leg guard)"),
             ("chan_xa_ban", (800, 880, 1120, 1024), None, "ban_xa", None,
              "the RIGHT FOOT, REDESIGNED in exactly the same way (the same robot boot design)")]
VI_G["G9"] = "vẽ lại hai bàn chân thành ủng giáp robot (mũi vàng ba múi, tấm cổ chân bạc, đế thép sẫm)"
