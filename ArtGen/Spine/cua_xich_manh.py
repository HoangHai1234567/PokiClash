# -*- coding: utf-8 -*-
"""Tinh linh đuôi máy cưa (cua_xich, rig monster_3374): MẢNH theo concept D3 đã duyệt (inbox/cua_xich_1/tai_ve/L1_duyet.png).

Con gốc dựng bằng các mảnh chồng nhau, mỗi mảnh có viền riêng (thân tròn, mặt tròn, mũ trùm, găng tay, khúc chân, các tấm đuôi), nên
chia làm hai loại (skill pokiclash-spine-rig mục 00; memory reskin-theo-part-goc):
  K     : mảnh giữ hình bóng gốc: các tấm đuôi, đĩa cưa, thân, hai tay, bốn khúc chân, mắt (lòng, tròng, mắt nhắm), gai sau đầu. Tờ =
          CHÍNH mảnh gốc cắt theo lưới, phóng to; GPT đổi da theo concept, giữ hình bóng. Lắp bằng nguyên lưới của họ.
  R     : mảnh ĐỔI DÁNG, gen "đúng chỗ, đúng cỡ" trên concept, bỏ mọi thứ khác, vẽ đủ phần khuất: mai ba đốt (thay mũ trùm), mặt có mõm,
          sừng móc, cụm quặng (thay ba tinh thể), vòng dây giật (mảnh mới); sợi dây giật vẽ thẳng ở góc trống (dải lưới co giãn).
          Toạ độ concept → thế giới khung 0 idle qua phép căn.

    cua_xich_manh.py can        căn concept lên hình con gốc (phép đồng dạng khớp hình bóng nhất) → mau/can.json
    cua_xich_manh.py soi        viền từng part gốc chồng lên concept đã căn → mau/_part_tren_concept.png (soát chỗ trước khi chia)
    cua_xich_manh.py to         dựng mọi tờ hướng dẫn + file prompt → mau/goc_K*.png, gui_gpt/cua_xich_1/luot_4_*.txt
    cua_xich_manh.py cat [tờ]   cắt ảnh về (K / R) → manh/<vùng>.png, manh/moi.json (mảnh đổi dáng), tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cua_xich as G  # noqa: E402
from quai.soi import _tris  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES
DPU = 0.75                                # atlas của họ: 0,75 px ảnh vùng / đơn vị rig (đo mọi part)
GUI = os.path.join(HERE, "gui_gpt", "cua_xich_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
CHIEN_SAT = os.path.join(HERE, "inbox", "chien_sat_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
INK = (43, 33, 24)
MUC = "#2B2118"
FONT = "C:/Windows/Fonts/arial.ttf"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def mat_na(rgb, nguong=28):
    m = ((255 - rgb.astype(np.int16)).max(2) > nguong).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


# ================================================================ căn concept lên rig
def can():
    """phép đồng dạng (tỉ lệ a quanh tâm khung, dời d) đưa hình con gốc trùng hình bóng concept nhất; chỉ đo phần THÂN + ĐUÔI + CHÂN
    (mặt nạ dưới y 300): đầu của concept cố ý đổi dáng (mai, sừng, quặng) nên không được kéo phép căn."""
    g = mat_na(np.asarray(Image.open(os.path.join(G.MAU, "goc_ca_con.png")).convert("RGB")))
    c = mat_na(np.asarray(Image.open(CON).convert("RGB").resize((W, H))))
    k = 4
    gs = cv2.resize(g.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
    cs = cv2.resize(c.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA).astype(bool)
    C = np.array([W / 2, H / 2]) / k

    def thu(a, dx, dy, chi_duoi=True):
        M = np.array([[a, 0, C[0] - a * C[0] + dx / k], [0, a, C[1] - a * C[1] + dy / k]], np.float32)
        w = cv2.warpAffine(gs, M, (W // k, H // k), flags=cv2.INTER_NEAREST).astype(bool)
        if chi_duoi:
            w, c_ = w[300 // k:], cs[300 // k:]
        else:
            c_ = cs
        return (w & c_).sum() / max(1, (w | c_).sum())
    best = (0, 1.0, 0.0, 0.0)
    for a in np.arange(0.92, 1.081, 0.01):
        for dx in range(-48, 49, 4):
            for dy in range(-48, 49, 4):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    _, a0, x0, y0 = best
    for a in np.arange(a0 - 0.01, a0 + 0.0101, 0.0025):
        for dx in range(int(x0) - 4, int(x0) + 5):
            for dy in range(int(y0) - 4, int(y0) + 5):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    v, a, dx, dy = best
    gj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    out = dict(iou_duoi=round(float(v), 4), iou_ca=round(float(thu(a, dx, dy, False)), 4), a=float(a), dx=float(dx), dy=float(dy),
               s=gj["s"], cx=gj["cx"], cy=gj["cy"])
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("căn:", out)
    return out


def phep_can():
    """(T: thế giới khung 0 idle → px concept, Ti: ngược lại, px concept / đơn vị)."""
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, a, dx, dy = j["s"], j["cx"], j["cy"], j["a"], j["dx"], j["dy"]
    C = np.array([W / 2, H / 2])

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        P = np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
        return C + a * (P - C) + np.array([dx, dy])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([dx, dy]) - C) / a + C
        return np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return T, Ti, s * a


# ================================================================ dáng gốc: từng part trên khung concept
_CK = {}


def lop_goc():
    """{slot: (att, mặt nạ bool trên khung concept)} các hình đang bật ở khung 0 idle, theo thứ tự vẽ; + bản đồ slot trên cùng."""
    if "lop" in _CK:
        return _CK["lop"]
    T, _, _ = phep_can()
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    lop = {}
    top = np.full((H, W), -1, np.int32)
    for k, a in enumerate(atts):
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        m = np.asarray(lay)[..., 3] > 110
        lop[a["slot"]] = (a, m)
        top[m] = k
    _CK["lop"] = (lop, top, [a["slot"] for a in atts])
    return _CK["lop"]


MAU_SOI = [(230, 30, 30), (30, 120, 230), (20, 160, 60), (200, 120, 0), (160, 40, 200), (0, 160, 170)]


def soi():
    """viền từng part gốc (khung 0 idle, đã căn) chồng lên concept; mỗi part một màu, ghi số thứ tự vẽ."""
    lop, top, thu_tu = lop_goc()
    Cn = Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS)
    S = 2
    nen = Image.blend(Cn, Image.new("RGB", (W, H), "white"), 0.35).resize((W * S, H * S), Image.LANCZOS)
    A = np.asarray(nen).copy()
    nhan = []
    for k, s_ in enumerate(thu_tu):
        m = cv2.resize(lop[s_][1].astype(np.uint8), (W * S, H * S), interpolation=cv2.INTER_NEAREST)
        e = m & ~cv2.erode(m, el(2))
        A[e.astype(bool)] = MAU_SOI[k % len(MAU_SOI)]
        ys, xs = np.nonzero(m)
        nhan.append((k + 1, s_, int(xs.mean()), int(ys.mean()), MAU_SOI[k % len(MAU_SOI)]))
    o = Image.fromarray(A)
    d = ImageDraw.Draw(o)
    f = ImageFont.truetype(FONT, 26)
    for n, s_, x, y, c in nhan:
        d.text((x - 10, y - 12), str(n), fill=c, font=f, stroke_width=3, stroke_fill="white")
    y = 10
    for n, s_, _, _, c in nhan:
        d.text((10, y), f"{n} {s_}", fill=c, font=f, stroke_width=2, stroke_fill="white")
        y += 30
    p = os.path.join(G.MAU, "_part_tren_concept.png")
    o.save(p)
    print(p)


# ---------------------------------------------------------------- chép từ quy_xich_manh (import file đó sẽ đặt lại rig gốc chung của hoa_ho)
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


def tach_manh(rgb, tam):
    """tách các mảnh chạm viền nhau: lòng tô (không mực, không trắng) chia vùng liền; mỗi vùng về mảnh có tâm gần nhất; mọi điểm của hình
    (cả viền) về mảnh của lòng tô gần nhất. Trắng khép kín trong hình = lỗ (trong suốt). → {tên: mặt nạ bool}."""
    fg = ~nen_trang(rgb.astype(np.int32))
    lum = rgb.astype(np.int32).mean(2)
    trang = rgb.min(2) > 236
    # mực nâu sẫm (lum ~26–40, đỏ > lam rõ); sắt sẫm (lum ~70, xám trung tính) vẫn là lòng tô
    r_, b_ = rgb[..., 0].astype(np.int32), rgb[..., 2].astype(np.int32)
    muc = (lum < 50) | ((lum < 62) & (r_ - b_ > 22))
    long_ = fg & ~muc & ~trang
    long_ = cv2.erode(long_.astype(np.uint8), el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(long_.astype(np.uint8), 8)
    ten = list(tam)
    C = np.array([tam[k] for k in ten], float)
    gan = np.zeros(n, np.int32) - 1
    for i in range(1, n):
        if st[i, 4] < 25:
            continue
        gan[i] = int(np.argmin(np.hypot(*(C - cen[i]).T)))
    hop = (lab > 0) & (gan[lab] >= 0)
    _, lbl = cv2.distanceTransformWithLabels((~hop).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(hop)
    bang = np.full(lbl.max() + 1, -1, np.int32)
    bang[lbl[ys, xs]] = gan[lab[ys, xs]]
    thuoc = bang[lbl]
    out = {}
    for j, k in enumerate(ten):
        out[k] = fg & ~trang & (thuoc == j)
    return out


# ================================================================ màu (đo trên concept D3: trung vị vùng / cụm k-means)
MAU = dict(xam="#696868", xam_toi="#5C5A5A", quang_sang="#878482", gi="#D37432", mat="#D0C7BF", rang="#D9D9D9", vuot="#E2DAD0",
           long_mat="#FDE1A0", trong="#ED932F", vong="#D79F53", day="#84401D")
LO_DAY = (782, 808)          # lỗ dây giật trên bụng (px concept)
VONG = (780, 760)            # tâm vòng dây giật (px concept)


# ================================================================ K: mảnh giữ hình bóng gốc (tờ = mảnh gốc phóng to)
def vung():
    """{vùng: (att, ảnh part cắt theo lưới)} theo dáng gốc; lấy CẢ hình không bật mặc định (mắt nhắm)."""
    atlas, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    out = {}
    for a in D["atts"]:
        if a.get("region") in imgs and a["region"] not in out:
            out[a["region"]] = (a, G.part_goc(a))
    return out


TO_K = {
    "K1": [[("juzi_01", 3.3), ("weiba_04", 3.3), ("weiba_01", 3.3), ("shenti", 3.3)],
           [("weiba_03", 3.6), ("weiba_02", 4.6), ("youxiaotui", 3.6), ("youdatui", 3.6), ("zuoxiaotui", 3.6), ("zuodatui", 3.6)]],
    "K2": [[("youshou", 5.0), ("zuoshou", 5.0), ("yanjing_01", 5.0), ("yanjing_02", 5.0), ("yanjing_03", 5.0)]],
    # lớp đầu SAU (mặt xa của mũ, nằm sau tinh thể): người dùng 2026-11-16 "con gốc còn có 1 layer đầu sau nữa", quặng phải kẹp GIỮA hai lớp
    "K3": [[("youerduo", 5.0)]],
}
MO_TA_K = {
    "juzi_01": f"THE SAW DISC on the tail: a flat round disc with EIGHT blunt SQUARE TEETH evenly round its rim; the disc dark slate "
               f"{MAU['xam']}, the eight teeth pale steel {MAU['rang']}, each tooth with its own ink outline; a tiny dot in the centre. Keep "
               "the square teeth exactly (no pointed saw teeth).",
    "weiba_04": f"THE BACK PLATE of the saw (a rounded oblong plate that sits behind the disc): plain darker slate {MAU['xam_toi']}.",
    "weiba_01": f"THE SAW HOUSING (the front oblong plate of the tail, rounded at both ends, slanted): flat slate {MAU['xam']} with one thin "
                f"inner line along its long edge, and near its upper end the round HUB: a small darker round boss {MAU['xam_toi']} inside "
                f"a rust-orange ring {MAU['gi']}.",
    "shenti": f"THE BODY (a round ball): flat slate {MAU['xam']}, plain (no curved inner line), with ONE small dark round HOLE "
              "(about {d} px wide, filled dark brown ink colour) at about x = {x}, y = {y} on the sheet: a short cord will come out of it.",
    "weiba_03": f"THE TAIL BASE (a short thick bent piece joining the body to the saw): plain slate {MAU['xam']}.",
    "weiba_02": f"A SMALL JOINT PIECE of the tail: plain darker slate {MAU['xam_toi']}.",
    "youxiaotui": f"THE FAR SHIN (a short thick stick leg, its top end cut slanted): plain darker slate {MAU['xam_toi']}.",
    "youdatui": f"THE FAR THIGH (a small rounded leaf shape): plain slate {MAU['xam']}.",
    "zuoxiaotui": f"THE NEAR SHIN (a short thick stick leg): plain slate {MAU['xam']}.",
    "zuodatui": f"THE NEAR THIGH (a ribbed dome like a scallop shell): slate {MAU['xam']} with its thin RIB LINES fanning out from the lower "
                "left, exactly like the ribs drawn in image 1.",
    "youshou": f"THE NEAR PAW (a small mitten-shaped paw): flat slate {MAU['xam']}, with THREE small pointed ivory CLAWS {MAU['vuot']} at "
               "its lower end, each with an ink outline.",
    "zuoshou": f"THE FAR PAW (a small round mitten-shaped paw): flat slate {MAU['xam']}, with THREE small pointed ivory CLAWS "
               f"{MAU['vuot']} along its lower edge, curling down, each with an ink outline.",
    "yanjing_01": f"THE WHITE OF THE EYE (an egg-shaped oval): flat pale yellow {MAU['long_mat']} with a thick ink outline. Nothing inside it.",
    "yanjing_02": f"THE IRIS (a smaller upright oval): flat amber orange {MAU['trong']} with a thin vertical dark-brown SLIT PUPIL down its "
                  "middle and ONE tiny white dot at its upper right; a thin ink outline.",
    "youerduo": f"THE FAR SIDE OF THE HEAD SHELL (a curved pointed armour plate, seen behind the ore columns on the back of the head): "
                f"plain darker slate {MAU['xam_toi']}, one thin ink line following its curved edge. Nothing else on it.",
    "yanjing_03": "THE SQUEEZED-SHUT EYE (a sideways V, like the sign '>'): two thick dark-brown ink strokes meeting at the point, the same "
                  "shape as in image 1.",
}


def o_vung(a, P, w, h):
    """điểm thế giới P (khung 0 idle) → toạ độ trong ảnh vùng (w × h) của part a, qua lưới của nó (tam giác chứa hoặc gần nhất)."""
    uv, tr = G.luoi(a)
    im = G.part_goc(a)
    U = uv / np.array([im.width, im.height], float) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    P = np.asarray(P, float)
    tot, kq = -9.0, None
    for t in np.asarray(tr).reshape(-1, 3):
        A_, B_, C_ = V[t[0]], V[t[1]], V[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, P - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        if abs(den) < 1e-9:
            continue
        b1 = (v2[0] * v1[1] - v2[1] * v1[0]) / den
        b2 = (v0[0] * v2[1] - v0[1] * v2[0]) / den
        b0 = 1 - b1 - b2
        nho = min(b0, b1, b2)
        if nho > tot:
            tot, kq = nho, b0 * U[t[0]] + b1 * U[t[1]] + b2 * U[t[2]]
    return kq


def to_k():
    V = vung()
    lop, _, _ = lop_goc()
    _, Ti, spx = phep_can()
    out = {}
    for ma, hang in TO_K.items():
        can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for r, z in h_:
                im = V[r][1]
                cs.append((r, z, im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)))
            cao.append((cs, max(c[2].height for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, big in cs:
                y0 = y + (hh - big.height) // 2
                can_.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, big.width, big.height], z=z)
                x += big.width + ke
            y += hh + ke_y
        if "shenti" in o:                       # lỗ dây: concept → thế giới → ô của thân trên tờ
            a = lop["shenti"][0]
            x, y0, bw, bh = o["shenti"]["hop"]
            q = o_vung(a, Ti(LO_DAY)[0], bw, bh)
            o["shenti"]["lo"] = [int(round(x + q[0])), int(round(y0 + q[1])), int(round(18 / spx * DPU * o["shenti"]["z"]))]
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can_.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        print(p)
        out[ma] = o
    return out


def prompt_k(ma, o):
    mau = os.path.join(G.MAU, f"goc_{ma}.png")
    out = os.path.join(G.TAI, f"D_{ma}.png")
    p = os.path.join(GUI, f"luot_4_da_{ma}.txt")
    n = len(o)
    if ma == "K3":
        tom = "one part, drawn very big: the far side of the head shell (a curved pointed plate)"
    elif ma == "K1":
        tom = ("top row: the tail's saw disc with eight square teeth, the back plate of the saw, the saw housing with its hub, the round "
               "body; bottom row: the tail base, a small tail joint, the far shin, the far thigh, the near shin, the ribbed near thigh")
    else:
        tom = "one row: the near paw, the far paw, the white of the eye, the iris, the squeezed-shut eye; drawn very big"
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: {n} separate body parts of a 2D animation puppet (a small "
         f"creature), each drawn alone, at the exact size and place to keep: {tom}. They are painted in a smooth grey digital style.",
         f"image 2 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: a small fierce iron beast facing right: "
         "a dark slate armour shell of three bands over its head with a hooked horn, iron ore columns with rusty tops on the back of its "
         "head, a pale face with a short snout and a fang, one big amber slit-pupil eye, small slate paws with ivory claws, a ring-pull "
         "cord on the belly, short slate legs, and a tail with a slate saw housing and a disc with square teeth. Take from it the "
         "colours and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). The shapes come from image 1.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one). Do NOT merge parts, do NOT add parts, "
         "do NOT move parts. Pure white (#FFFFFF) between the parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): hand-drawn on paper: a wobbly dark-brown ink outline ({MUC}, "
         "about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the few inner lines, and "
         "every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. Do NOT copy the smooth digital "
         "painting of image 1: no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows: flat colour only. "
         "VERY SIMPLE: no extra details.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        mt = MO_TA_K[r]
        if r == "shenti":
            mt = mt.replace("{x}", str(d["lo"][0])).replace("{y}", str(d["lo"][1])).replace("{d}", str(d["lo"][2]))
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {mt}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p, mau, out


def cat_k():
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    so = []
    for ma in TO_K:
        path = anh.to_moi_nhat(G.TAI, f"D_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        print(f"{ma}:", os.path.basename(path))
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg = ~nen_trang(A)
        fgG = ~nen_trang(Gd)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        for r, d in o.items():
            x, y, cw, ch = d["hop"]
            pad = 14
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
            sub = lab[y0:y1, x0:x1]
            ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
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
            # vá chỗ GPT vẽ hụt, chỉ trong dải sát mép (≤ 5 px; mục 30)
            thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
            if thieu.any() and (a2[..., 3] >= 128).any():
                co = (a2[..., 3] >= 128).astype(np.uint8)
                _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                ys_, xs_ = np.nonzero(co)
                bang = np.zeros((lbl.max() + 1, 3), np.uint8)
                bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
                a2[thieu, :3] = bang[lbl[thieu]]
                a2[thieu, 3] = 255
            # nét mực dọc PHÍA TRONG mép hình bóng gốc: lưới của họ ôm sát hình bóng, nét viền của mình (nằm trên mép) bị lưới xén một
            # nửa → mép lởm chởm (skill mục 00, bước 4). Mắt nhắm là nét mực sẵn, bỏ qua.
            if r != "yanjing_03":
                vien_trong = ag & ~cv2.erode(ag.astype(np.uint8), el(2.5)).astype(bool)
                a2[vien_trong, :3] = INK
                a2[vien_trong, 3] = 255
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            ious[r] = round(iou, 3)
            so.append(Image.fromarray(a2, "RGBA"))
            print(f"  {r:12s} → {r}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    if so:
        _to_so(so, os.path.join(MANH, "_so_K.png"))


def vet_quay():
    """vệt quay mờ của đĩa (juzi_02, slot juzi_03): hình mờ của họ, đổi màu bằng mã (nét sẫm → mực của mình, mảng xám → xám nhạt)."""
    V = vung()
    goc = np.asarray(V["juzi_02"][1].convert("RGBA")).astype(np.float32)
    lum = goc[..., :3].mean(2)
    out = np.zeros_like(goc)
    muc = np.array([int(MUC[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    out[..., :3] = np.where((lum < 90)[..., None], muc, np.array([200, 198, 194], np.float32))
    out[..., 3] = np.where(lum < 90, goc[..., 3], goc[..., 3] * 0.8)
    im = Image.fromarray(out.astype(np.uint8), "RGBA")
    im = im.convert("RGBa").resize((im.width * RES, im.height * RES), Image.LANCZOS).convert("RGBA")
    os.makedirs(MANH, exist_ok=True)
    im.save(os.path.join(MANH, "juzi_02.png"))
    print(os.path.join(MANH, "juzi_02.png"), im.size)


# ================================================================ R: mảnh đổi dáng, gen đúng chỗ, đúng cỡ trên concept
# mỗi tờ: [(tên, slot của họ mà nó thay hoặc bám theo, tả tiếng Anh)]; mảnh đầu đều chồng nhau nên mỗi tờ một mảnh đầu
R = {
    "R1": [("mai_truoc", "to_02",
            "the FRONT PART OF THE HEAD SHELL: the MIDDLE armour band and the FRONT armour band together as ONE piece (the two big curved "
            "dark slate plates on the right of the head, with the ink line between them). The front band's lower edge is the thick "
            "BROW with its small downward notch, running across the top half of the eye, and the shell ends at the cheek in a short "
            "rounded edge above the snout. Draw it complete as one closed shape; its left edge, where it lies over the back band and the "
            "horn, is a clean curved band edge"),
           ("vong", None,
            f"the PULL RING of the starter cord under the left paw: a round ring {MAU['vong']} with a thick ink outline and a round hole "
            "in the middle, complete all round (the parts hidden behind the claws are drawn too), WITHOUT the paw and WITHOUT the cord"),
           ("day", None,
            f"ONE LONG STRAIGHT CORD lying HORIZONTALLY in the empty lower right of the canvas, from about x = 1000 to x = 1450 at about "
            f"y = 950: a plain rust-brown cord {MAU['day']} about 12 px thick with a thin ink outline, both ends rounded; this one is NOT "
            "in image 1, it is an extra piece for the animation (the cord that comes out when the creature pulls the ring)")],
    "R2": [("mai_sau", "to_02",
            "the BACK ARMOUR BAND OF THE HEAD SHELL: the rounded dark slate band at the back (left) of the head, the one the horn lies "
            "on, complete as one closed shape: the parts hidden behind the horn and behind the middle band are drawn too, continuing it "
            "as a plain band (its right part simply ends in a rounded edge under where the middle band was)")],
    "R3": [("sung", "zuoerduo",
            f"the HOOKED HORN: the short thick horn curving forward over the top of the head like a hook, dark slate on top and rust "
            f"orange {MAU['gi']} on its underside, complete down to its root (the root and the tip part that were hidden under the "
            "armour bands are drawn too, continuing its shape naturally)")],
    "R4": [("mat", "to_01",
            f"the FACE: the pale round head ball {MAU['mat']} with its short blunt SNOUT on the right (the small dark nostril dot near "
            "its tip, the closed mouth line along its underside and the ONE small white fang), and the TWO rust-orange marks on the "
            f"cheek {MAU['gi']}. Draw the WHOLE round head ball complete: its top, hidden under the shell in image 1, is plain pale skin. "
            "WITHOUT THE EYE: where the eye is in image 1 just paint plain pale skin (no eye, no eye outline). Without the shell, the "
            "horn, the ore, the paws and the ring")],
    "R5": [("quang", "tofa",
            f"the IRON ORE COLUMNS on the back of the head: the FOUR hexagonal ore columns (the tall one in the middle, the short one on "
            f"its left, the two on the right) with their rust-orange tops {MAU['gi']}, slate faces {MAU['xam']}, lighter faces "
            f"{MAU['quang_sang']} and darker faces {MAU['xam_toi']}, as ONE piece, complete down to their bases (the lower parts hidden "
            "behind the head shell are drawn too, continuing each column straight down)")],
    "R6": [("tay_trai", "zuoshou",
            f"the LEFT PAW (on the viewer's left, in front of the middle of the belly): the small rounded slate paw {MAU['xam']} whose "
            f"THREE small ivory CLAWS {MAU['vuot']} curl down over the pull ring, complete as one closed rounded mitten shape (the parts "
            "hidden behind other things drawn too), WITHOUT the ring and WITHOUT the cord"),
           ("tay_phai", "youshou",
            f"the RIGHT PAW (on the viewer's right, under the snout): the small rounded slate paw {MAU['xam']} with its THREE small "
            f"ivory CLAWS {MAU['vuot']} pointing down, complete as one closed rounded mitten shape (its top, hidden behind the face, "
            "drawn too)")],
}
VI_R = {"R1": "hai đốt mai trước (có gờ mày) + vòng dây giật + sợi dây thẳng ở góc trống", "R2": "đốt mai sau (vẽ đủ phần khuất)",
        "R3": "sừng móc (vẽ đủ gốc)", "R4": "mặt có mõm, nanh, hai vằn gỉ, KHÔNG mắt (vẽ đủ cả đầu tròn)",
        "R5": "bốn cột quặng (vẽ đủ chân cột)", "R6": "hai tay nhỏ có vuốt (đúng chỗ như D3, trước mặt)"}


def prompt_r():
    ps = []
    for ma, ds in R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_4_manh_{ma}.txt")
        mot = len(ds) == 1
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: a small fierce iron beast facing "
             "right: a dark slate armour shell of three bands over its head with a hooked horn, iron ore columns with rusty tops on the "
             "back of its head, a pale face with a short snout and a fang, one big amber slit-pupil eye, small slate paws with ivory "
             "claws holding a ring-pull cord on the belly, short slate legs, and a tail with a slate saw housing and a disc with square "
             "teeth.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", ""]
        if mot:
            t += ["TASK: redraw image 1 with ONLY the ONE piece described below, in the SAME POSITION and at the SAME SIZE as in image 1 "
                  "(if your picture were laid over image 1, the piece must sit exactly on its old place). REMOVE everything else and "
                  "leave pure white there. COMPLETE the piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of "
                  "it that were hidden behind other things in image 1 are drawn too, continuing its shape naturally.", "",
                  "THE PIECE:", f"{ds[0][2]}."]
        else:
            t += [f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as "
                  "in image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place), except the "
                  "extra piece that is not in image 1. REMOVE everything else and leave pure white there. COMPLETE every piece into ONE "
                  "CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden behind other things in "
                  "image 1 are drawn too. The pieces stay separate from each other.", "", "THE PIECES:"]
            t += [f"{i}. {mt}." for i, (_, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few "
              "inner lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no "
              "highlights, no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


# tâm từng mảnh trên tờ (px 1536 × 1024) khi một tờ có nhiều mảnh
TAM_R = {"R1": {"mai_truoc": (985, 520), "vong": VONG, "day": (1225, 950)}, "R6": {"tay_trai": (775, 735), "tay_phai": (912, 752)}}


def cat_r():
    """mỗi tờ M_R*: tách mảnh, ghi manh/<tên>.png (1 px / đơn vị rig) + moi.json (4 góc thế giới khung 0 idle của khung ảnh)."""
    _, Ti, spx = phep_can()
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    for ma, ds in R.items():
        path = anh.to_moi_nhat(G.TAI, f"M_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        print(f"{ma}:", os.path.basename(path))
        rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        if len(ds) > 1:
            ms = tach_manh(rgb, TAM_R[ma])
        else:
            fg = ~nen_trang(rgb.astype(np.int32))
            ms = {ds[0][0]: fg & ~(rgb.min(2) > 236)}
        for ten, sl, _ in ds:
            mm0 = ms.get(ten)
            if mm0 is None or mm0.sum() < 50:
                print(f"  {ten}: KHÔNG thấy mảnh")
                continue
            ys, xs = np.nonzero(mm0)
            pad = 4
            x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
            mm = mm0[y0:y1 + 1, x0:x1 + 1]
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
            k = DPU * RES / spx                      # px tờ → px ảnh mảnh (1,5 px / đơn vị rig, như ảnh vùng × RES)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            moi[ten] = dict(slot=sl, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=Ti(hop).tolist(), to=ma)
            print(f"  {ten:9s} hộp {x0},{y0}–{x1},{y1}  → {ten}.png {out.size}" + (f"  (thay {sl})" if sl else "  (mảnh mới)"))
    json.dump(moi, open(pj, "w"), indent=1)
    tai_xa()


def tai_xa(truc_x=883.0, toi=0.9):
    """TAI XA (slot youerduo của họ) = bản ĐỐI XỨNG của tai gần: lật ngang đúng mảnh đã vẽ của bên gần quanh trục x = truc_x (px concept;
    883 đưa tâm sừng gần x 735 về tâm tai xa của họ x 1031), tối đi chút (mặt xa). Người dùng 2026-11-16: "tai 2 bên không đồng bộ" (bên
    gần là sừng móc mặt dưới gỉ cam trên đốt mai sau, bên xa là tấm nhọn trơn). Hai bản để chọn: `tai_xa` (đốt mai sau + sừng), `tai_xa_s`
    (chỉ sừng). Ghi manh/<tên>.png + moi.json (4 góc thế giới của khung đã lật)."""
    _, Ti, spx = phep_can()
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    if "sung" not in moi or "mai_sau" not in moi:
        return
    k = DPU * RES / spx
    for ten, ds in (("tai_xa", ("mai_sau", "sung")), ("tai_xa_s", ("sung",))):
        hs = np.array([moi[d]["hop"] for d in ds], float)
        x0, y0, x1, y1 = hs[:, 0].min(), hs[:, 1].min(), hs[:, 2].max(), hs[:, 3].max()
        can_ = Image.new("RGBA", (int(round((x1 - x0) * k)) + 2, int(round((y1 - y0) * k)) + 2), (0, 0, 0, 0))
        for d in ds:
            im = Image.open(os.path.join(MANH, d + ".png")).convert("RGBA")
            can_.alpha_composite(im, (int(round((moi[d]["hop"][0] - x0) * k)), int(round((moi[d]["hop"][1] - y0) * k))))
        if len(ds) > 1:
            # LẤP KÍN lòng vòm (bao lồi của hình): dải mai sau là vòm rỗng; bên gần lòng vòm có mặt + mai lấp, bên xa không có gì sau nó nên
            # khi đầu cúi, tai đung đưa lệch nhịp là đuôi vòm rời đầu, lộ nền (người dùng 2026-11-16: "phần đuôi tai bị hở khi cúi đầu")
            C0 = np.asarray(can_).copy()
            m0 = (C0[..., 3] > 128).astype(np.uint8)
            cs, _ = cv2.findContours(m0, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            hull = cv2.convexHull(np.concatenate(cs))
            lum0 = C0[..., :3].astype(np.int32).mean(2)
            to_ = (m0 > 0) & (lum0 > 80) & (C0[..., 0].astype(np.int32) - C0[..., 2] < 30)      # điểm tô xám đá (không mực, không gỉ cam)
            mau_da = np.median(C0[to_][:, :3], 0) if to_.any() else np.array([105, 104, 104])
            nen = np.zeros_like(C0)
            cv2.fillConvexPoly(nen, hull, (int(mau_da[0]), int(mau_da[1]), int(mau_da[2]), 255), lineType=cv2.LINE_AA)
            cv2.polylines(nen, [hull], True, (INK[0], INK[1], INK[2], 255), 4, lineType=cv2.LINE_AA)
            lop = Image.fromarray(nen, "RGBA")
            lop.alpha_composite(can_)
            can_ = lop
        A = np.asarray(can_.transpose(Image.FLIP_LEFT_RIGHT)).astype(np.float32)
        lum = A[..., :3].mean(2, keepdims=True)
        A[..., :3] = np.where(lum > 80, A[..., :3] * toi, A[..., :3])        # tối phần tô, giữ nét mực
        Image.fromarray(A.astype(np.uint8), "RGBA").save(os.path.join(MANH, ten + ".png"))
        mx0, mx1 = 2 * truc_x - x1, 2 * truc_x - x0
        hop = np.array([[mx0, y0], [mx1, y0], [mx1, y1], [mx0, y1]], float)
        moi[ten] = dict(slot="youerduo", hop=[int(mx0), int(y0), int(mx1), int(y1)], the_gioi=Ti(hop).tolist(), to="lật " + "+".join(ds))
        print(f"  {ten}: lật {' + '.join(ds)} quanh x {truc_x:.0f} → hộp {mx0:.0f},{y0:.0f}–{mx1:.0f},{y1:.0f}")
    json.dump(moi, open(pj, "w"), indent=1)


# ================================================================ hướng dẫn
def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 4")[0].rstrip("\n")
    gd = ["", "## Lượt 4: mảnh theo concept D3 đã duyệt (2026-11-16)", "",
          "Người dùng chốt D3 (`tai_ve/L1_duyet.png`). Hai loại tờ (Claude tự gen và tự cắt; người dùng không cần làm gì). Ảnh mảnh gốc "
          "là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, rs, vi in ps:
        gd += [f"### {ten}", "", vi, "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {v} |" for i, (r, v) in enumerate(rs, 1)]
        gd += [""]
    gd += ["Kiểm: tờ K giữ đúng hình bóng từng mảnh gốc, đổi da theo D3 (đĩa vẫn 8 răng vuông); mảnh R đúng chỗ, đúng cỡ như concept, vẽ đủ "
           "phần khuất, mặt KHÔNG có mắt; tô phẳng; nền trắng. Cắt: `py -3 -I ArtGen/Spine/cua_xich_manh.py cat`.", "",
           "Câu sửa nhanh: \"keep every part exactly on its old silhouette\"; \"remove the eye from the face, plain pale skin there\"; "
           "\"flat colour only, no shading\"."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    ok = to_k()
    ps = []
    for ma, o in ok.items():
        p, gd, out = prompt_k(ma, o)
        vi = {"K1": "đĩa cưa, tấm lưng, vỏ cưa, thân (có lỗ dây), gốc đuôi, mấu nối, bốn khúc chân",
              "K2": "hai tay có vuốt, lòng mắt, tròng mắt, mắt nhắm", "K3": "lớp đầu sau (mặt xa của mai, nằm sau quặng)"}[ma]
        ps.append((f"Tờ mảnh giữ hình bóng {ma}", p, [(gd, f"Mảnh gốc cắt theo lưới, phóng 3,3–5 lần: {vi}"), (CON, "Concept D3 đã duyệt")],
                   f"{vi} → `{Wp(out)}`"))
    for ma, p, out in prompt_r():
        ps.append((f"Tờ mảnh đổi dáng {ma}", p, [(CON, "Concept D3 đã duyệt")], f"{VI_R[ma]} → `{Wp(out)}`"))
    huong_dan(ps)
    return ps


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "soi":
        soi()
    elif cmd == "to":
        to_het()
    elif cmd == "to_r":
        prompt_r()
    elif cmd == "tai_xa":
        tai_xa()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        if chi in ("", "K"):
            cat_k()
            vet_quay()
        if chi in ("", "R"):
            cat_r()
    else:
        print(__doc__)
