# -*- coding: utf-8 -*-
"""Vong Kỵ Nhi (DẠNG 1 NON của kỵ sĩ cổ đại bị nguyền): MẢNH theo concept C đã duyệt (inbox/ky_nguyen_non/tai_ve/L1_duyet.png: mũ thùng
sứt quá cỡ móp góc, khe chữ thập, lửa lách ra mép mũ, giáp vai hai tấm răng cưa, ngực trơn có khía, một mũi tên ở cẳng tay gần, áo choàng
đỏ rượu rách tua ngắn, đá đen nứt xanh). Người dùng chọn C 2026-11-17 (máy D).

Dùng lại hàm của ky_nguyen_manh.py (tờ K giữ hình bóng, tờ R gen đúng chỗ trên concept, cắt), chỉ thay (mẫu quy_xich_non_manh.py):
  - phép căn concept ↔ thế giới: theo hình bố cục rig non (ky_nguyen_rig.py bo_cuc → mau/bo_cuc.json, ky_nguyen_non.py khung →
    bo_cuc_khung.json), tinh chỉnh (a, dx, dy) bằng hình bóng đã mở (bỏ mũi tên / giáo mảnh của da dạng 2 trên bố cục); C vẽ to hơn ~8 %;
  - hình bóng từng part ở dáng gốc của rig NON (đỉnh lưới gốc qua xương đã đổi tỉ lệ);
  - bảng màu, prompt, danh sách mảnh.
Gen mới: K1 áo choàng + vạt trước (đỏ rượu, tua ngắn, KHÔNG viền vàng); K2 giáp vai (hai tấm răng cưa), giáp ngực (trơn, một khía), cẳng tay
gần (lỗ vòng xanh chỗ mũi tên cắm, không ấn Ø), năm viên đá → đá đen nứt xanh (mảnh lưới, giữ hình bóng); R1 mũ thùng sứt (kèm vòng cổ vàng).
Mắt cắt thẳng từ concept C. Dùng lại từ dạng 2 (inbox/ky_nguyen_1/manh): khoảng rỗng, lửa trên mũ, lửa sau gáy, hai găng + ngón, giáp tay xa,
mảnh giáp nhỏ; mảnh cứng kiếm gãy + phần vá hồn (chiêu cuối) + mũi tên P_ci04 ghi "he": "lon" (gắn theo thế giới dạng 2: co cùng xương).
Ẩn ở rig non (ky_nguyen_rig.py AN_NON): 12 mũi tên / giáo / dằm còn lại.

    ky_nguyen_non_manh.py can        → mau/can.json (+ mau/_so_can.png)
    ky_nguyen_non_manh.py to         tờ K1, K2, R1 + prompt → gui_gpt/ky_nguyen_non/luot_2_*.txt; chép mảnh dùng lại + moi.json phần dùng lại
    ky_nguyen_non_manh.py cat [K1|K2|R|MAT]
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

os.environ["KN_DANG"] = "non"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ky_nguyen as G  # noqa: E402
import ky_nguyen_manh as M  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = M.W, M.H
BASE1 = G.BASE
MANH1 = os.path.join(BASE1, "manh")
BASE = os.path.join(HERE, "inbox", "ky_nguyen_non")
G.BASE, G.MAU, G.TAI = BASE, os.path.join(BASE, "mau"), os.path.join(BASE, "tai_ve")
M.MANH = os.path.join(BASE, "manh")
M.GUI = os.path.join(HERE, "gui_gpt", "ky_nguyen_non")
M.CON = os.path.join(G.TAI, "L1_duyet.png")
MUC = M.MUC

# màu đo trên concept C (trung vị ô 7 × 7); giáp tối, lửa nhạt, lông tên lấy của dạng 2 (C cùng bảng)
M.MAU = dict(giap="#5E5959", giap_toi="#45403F", ri="#C55E21", vang="#CF954A", void="#242A20", lua="#8DD86F", lua_nhat="#D3F495",
             mat="#86E93A", ao="#6D1E29", go="#9B5F37", long_ten="#B8B5B5", mui="#9E9B9C", gang="#514D4F", gang_toi="#3A3637",
             da="#34353A", da_toi="#26272C")
C_ = M.MAU

DUNG_LAI = ("P_shenti_1", "P_shenti_9", "P_z_dabi", "P_y_dabi",                      # khoảng rỗng
            "P_yumao00", "P_yumao01", "P_yumao02", "P_yumao03", "P_yumao04",         # lửa trên mũ (xương lửa đã thu ở rig)
            "P_shenti_2", "P_shenti_3", "P_shenti_4", "P_shenti_5", "P_shenti_6", "P_shenti_7", "P_shenti_8",   # lửa sau gáy
            "P_y_shou", "P_y_shouzhi00", "P_y_shouzhi01", "P_y_shouzhi02", "P_y_shouzhi03", "P_y_shouzhi04",
            "P_z_shou", "P_z_shouzhi00", "P_z_shouzhi01", "P_z_shouzhi02", "P_z_shouzhi03", "P_z_shouzhi04", "P_z_shouzhi05",
            "P_z_shouzhi06", "P_z_xiaobi", "P_xiongjia00")
MOI_LON = ("kiem", "hon_va", "kt_ci04")                  # mảnh cứng dạng 2 dùng lại, gắn theo thế giới dạng 2 ("he": "lon")

M.R_CON = ("the APPROVED picture of OUR character, 1536x1024, white background: a young cursed knight floating with no legs, turned to "
           "the right: a hollow suit of blackened iron armour with a few rust patches and worn gold rims, a slightly too big flat-topped "
           "BUCKET helm dented at its upper right corner with a cross-shaped eye slit and two green eyes, small green soul-fire tongues "
           "slipping out along the top rim of the helm, a gold collar ring under the helm, two small saw-tooth shoulder plates, wide gaps "
           "between the plates showing the dark void with green fire tongues, a plain breastplate with a small notch in its upper edge, "
           "one broken arrow in the near forearm, a short torn wine-red cape, a gauntlet holding a broken rusty sword with a ring "
           "crossguard and a green gem in the pommel, an open iron hand on the right, small black rocks with green cracks floating below. "
           "It gives the design, the colours, the ink line and the crayon hatching.")

_GIAP = f"blackened iron {C_['giap']} (faces turned away darker {C_['giap_toi']}) with only ONE or TWO small flat rust patches {C_['ri']}"
_DA = (f"a small floating BLACK ROCK of exactly this shape: flat near-black stone {C_['da']} (the side turned away darker {C_['da_toi']}) "
       f"with ONE thin jagged GREEN CRACK line {C_['lua']} across it, ink outline all round")
M.TO_K = {
    "K1": [[("P_pifeng01", 1.9), ("P_pifeng00", 2.6)]],
    "K2": [[("P_jianjia", 2.1), ("P_xiongjia01", 2.3), ("P_y_xiaobi", 2.1)],
           [("P_shitou00", 3.2), ("P_shitou01", 3.2), ("P_shitou02", 3.2), ("P_shitou03", 3.2), ("P_shitou04", 3.2)]],
}
M.MO_TA_K.update({
    "P_pifeng01": f"THE BIG TORN CAPE (hanging from behind the shoulders): dark WINE-RED cloth {C_['ao']}, its lower edge torn into SHORT "
                  "ragged tatters exactly along the outline, a few thin fold lines where image 1 has them. NO gold border, no pattern, no "
                  "purple, no gradient. Keep every ragged strip and hole exactly.",
    "P_pifeng00": f"THE TABARD (a long narrow cloth strip hanging down, its lower end torn): dark wine-red {C_['ao']}, the lower end torn "
                  "into a few short tatters; NO gold border, no pattern, no sigil.",
    "P_jianjia": f"THE BIG SHOULDER PAULDRON: TWO overlapping curved iron plates (an upper plate and a lower plate following the outline), "
                 f"the lower edge of EACH plate a JAGGED SAW-TOOTH line with a thin worn gold rim {C_['vang']} along it; {_GIAP} on each "
                 "plate; the leaf-shaped flanges at the back become plain iron plate edges inside the same outline. No white, no leaves, "
                 "no crystals, no arrows.",
    "P_xiongjia01": f"THE CHEST PLATE (a breastplate with a pointed lower edge): plain {_GIAP}, a thin worn gold rim {C_['vang']} round "
                    "its edge, and ONE small V-shaped NOTCH in the middle of its upper edge. No cut, no crack, no fire, no emblem.",
    "P_y_xiaobi": f"THE BIG NEAR VAMBRACE (an armoured forearm, flanges at its top, a cuff at its lower end): {_GIAP}, worn gold bands "
                  f"{C_['vang']} at its top rim and its lower cuff; NO rune, no mark, no white.",
    "P_shitou00": _DA + ".", "P_shitou01": _DA + ".", "P_shitou02": _DA + ".", "P_shitou03": _DA + ".", "P_shitou04": _DA + ".",
})
M.VI_K = {"K1": "áo choàng lớn + vạt trước (đỏ rượu, rách tua ngắn, không viền vàng)",
          "K2": "giáp vai hai tấm răng cưa, giáp ngực trơn có khía, cẳng tay gần (lỗ vòng xanh chỗ mũi tên), năm viên đá đen nứt xanh"}
M.TA_K = {"K1": "two parts: on the left a big torn cape, on the right a long narrow cloth strip",
          "K2": "eight parts: top row a big shoulder pauldron, a chest plate, a big armoured forearm; bottom row five small stones"}

M.R = {"R1": [("mu", "P_tou", "bone5",
               "the HELMET: the flat-topped iron BUCKET helm (a little too big), with the DENT in its upper right corner, its rust patches "
               "and the cross-shaped eye slit; draw the eye slit as a plain near-black gap WITHOUT the green eyes; WITHOUT the green flames "
               "on its top rim (the top edge is a plain closed edge); and the worn gold COLLAR RING at its lower edge round the neck, "
               "complete all round")]}
M.VI_R = {"R1": "mũ thùng sứt (khe chữ thập tối, không mắt, không lửa) + vòng cổ vàng"}
M.TAM_R = {"R1": {"mu": (915, 285)}}
M.CHINH = {}
MAT_HOP = (845, 238, 1000, 300)                          # khung khe mắt trên concept C (đọc bằng mắt)


# ================================================================ căn: thế giới dáng gốc NON → px concept
def _bo_cuc():
    b = json.load(open(os.path.join(G.MAU, "bo_cuc.json")))
    k = json.load(open(os.path.join(G.MAU, "bo_cuc_khung.json")))
    return b["box"][0], b["box"][3], b["scale"], k["k"], k["ox"], k["oy"]


def _mo(m, r=6):
    """hình bóng đã mở (bỏ mũi tên, giáo, dằm mảnh)."""
    return cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, M.el(r)).astype(bool)


def can():
    """(a, dx, dy) quanh tâm khung để hình bóng đã mở của bố cục trùng concept nhất (thô ở 1/4, mịn ở 1/2)."""
    g = _mo(M.mat_na(np.asarray(Image.open(os.path.join(G.MAU, "bo_cuc_khung.png")).convert("RGB"))))
    c = _mo(M.mat_na(np.asarray(Image.open(M.CON).convert("RGB").resize((W, H)))))
    best = (0, 1.0, 0, 0)

    def thu(k, a, dx, dy):
        gs = cv2.resize(g.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
        cs = cv2.resize(c.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA).astype(bool)
        C = np.array([W / 2, H / 2]) / k
        Mx = np.float32([[a, 0, C[0] - a * C[0] + dx / k], [0, a, C[1] - a * C[1] + dy / k]])
        w = cv2.warpAffine(gs, Mx, (W // k, H // k), flags=cv2.INTER_NEAREST).astype(bool)
        return (w & cs).sum() / max(1, (w | cs).sum())
    for a in np.arange(0.96, 1.181, 0.01):
        for dx in range(-64, 65, 4):
            for dy in range(-64, 65, 4):
                v = thu(4, a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    _, a0, x0_, y0_ = best
    best = (0, a0, x0_, y0_)
    for a in np.arange(a0 - 0.01, a0 + 0.0101, 0.0025):
        for dx in range(int(x0_) - 4, int(x0_) + 5, 2):
            for dy in range(int(y0_) - 4, int(y0_) + 5, 2):
                v = thu(2, a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    x0, y1, sc, k, ox, oy = _bo_cuc()
    out = dict(iou=round(float(best[0]), 4), a=float(best[1]), dx=float(best[2]), dy=float(best[3]), x0=x0, y1=y1, sc=sc, k=k, ox=ox, oy=oy)
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("căn:", out)
    # tờ soi: viền bố cục đã căn chồng lên concept
    Cn = np.asarray(Image.open(M.CON).convert("RGB").resize((W, H))).copy()
    a, dx, dy = best[1], best[2], best[3]
    Cc = np.array([W / 2, H / 2])
    Mx = np.float32([[a, 0, Cc[0] - a * Cc[0] + dx], [0, a, Cc[1] - a * Cc[1] + dy]])
    gm = M.mat_na(np.asarray(Image.open(os.path.join(G.MAU, "bo_cuc_khung.png")).convert("RGB")))
    w = cv2.warpAffine(gm.astype(np.uint8), Mx, (W, H), flags=cv2.INTER_NEAREST)
    vien = cv2.morphologyEx(w, cv2.MORPH_GRADIENT, M.el(2)).astype(bool)
    Cn[vien] = (230, 30, 30)
    Image.fromarray(Cn).save(os.path.join(G.MAU, "_so_can.png"))
    return out


def phep_can():
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    C = np.array([W / 2, H / 2])

    def P0(V):
        V = np.asarray(V, float).reshape(-1, 2)
        return np.stack([j["ox"] + j["k"] * (V[:, 0] - j["x0"]) * j["sc"], j["oy"] + j["k"] * (j["y1"] - V[:, 1]) * j["sc"]], 1)

    def T(V):
        return C + j["a"] * (P0(V) - C) + np.array([j["dx"], j["dy"]])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([j["dx"], j["dy"]]) - C) / j["a"] + C
        return np.stack([j["x0"] + (P[:, 0] - j["ox"]) / (j["k"] * j["sc"]), j["y1"] - (P[:, 1] - j["oy"]) / (j["k"] * j["sc"])], 1)
    return T, Ti, j["k"] * j["sc"] * j["a"]


# ================================================================ hình bóng từng part ở dáng gốc NON
_CK = {}


def lop_goc():
    if "lop" in _CK:
        return _CK["lop"]
    os.environ["KN_MANH"] = MANH1                        # chỉ cần xương đã đổi tỉ lệ: dựng tạm bằng da dạng 2
    import ky_nguyen_rig as R
    sk, _ = R.dung()
    Wi = sk.the_gioi()
    T, _, _ = phep_can()
    G._C.pop("att", None)
    _, imgs, atts_idle = G.nap("att_idle0.json")
    hien = [a["slot"] for a in atts_idle if a.get("region")]
    by = {a["slot"]: a for a in R.AG["atts"]}
    lop, top, thu_tu = {}, np.full((H, W), -1, np.int32), []
    for k_, sl in enumerate(hien):
        a = dict(by[sl])
        ws = a.get("w")
        xy = np.array(a["xy"], float).reshape(-1, 2)
        V = []
        for i, p in enumerate(xy):
            lst = [(R.NB[b], w) for b, w in ws[i] if w > 0] if ws else [(a["bone"], 1.0)]
            tong = sum(w for _, w in lst)
            v = np.zeros(2)
            for bn, w in lst:
                bn2 = "move" if bn == "root" else bn
                lp = np.linalg.solve(R.WG[bn], np.array([p[0], p[1], 1.0]))
                v += w / tong * (Wi[bn2] @ lp)[:2]
            V.append(v)
        a["xy"] = np.array(V).ravel().tolist()
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(V)), uv, tr)
        m = np.asarray(lay)[..., 3] > 110
        lop[sl] = (a, m)
        top[m] = k_
        thu_tu.append(sl)
    _CK["lop"] = (lop, top, thu_tu)
    return _CK["lop"]


M.phep_can = phep_can
M.lop_goc = lop_goc


# ================================================================ lỗ mũi tên trên tờ K2
def lo_ten():
    """(x, y) trên tờ K2 (ảnh vùng cẳng tay gần) của chỗ mũi tên P_ci04 cắm vào: đầu cắm của mũi tên dạng 2 (thế giới khung 0 idle) chiếu
    vào lưới cẳng tay ở khung 0 idle."""
    o = json.load(open(os.path.join(BASE1, "mau", "goc_KT.json"), encoding="utf-8"))["P_ci04"]
    x, y, _, _ = o["hop"]
    z, P = o["z"], M.PAD_KT
    gw = np.array([o["x0w"] + (o["goc"][0] - x - P) / z, o["y1w"] - (o["goc"][1] - y - P) / z])
    G._C.pop("att", None)
    _, _, atts = G.nap("att_idle0.json")
    a = next(a for a in atts if a["slot"] == "P_y_xiaobi")
    im = G.part_goc(a)
    Wd = M._the_gioi_o(a, im.width, im.height)
    d = np.hypot(Wd[..., 0] - gw[0], Wd[..., 1] - gw[1])
    d = np.where(np.isnan(d), 1e9, d)
    al = np.asarray(im)[..., 3] > 60
    d = np.where(al, d, d + 1e6)                         # chỉ điểm có hình
    py_, px_ = np.unravel_index(int(np.argmin(d)), d.shape)
    k2 = json.load(open(os.path.join(G.MAU, "goc_K2.json"), encoding="utf-8"))["P_y_xiaobi"]
    G._C.pop("att", None)
    return k2["hop"][0] + px_ * k2["z"], k2["hop"][1] + py_ * k2["z"], float(d[py_, px_])


def sua_ten():
    """mũi tên dạng 2 (kt_ci04) chuyển sang slot P_ci03 (vẽ TRƯỚC cẳng tay gần, cũng là con bone8) và dời cho đầu cắm trùng tâm lỗ vòng
    xanh GPT vẽ trên cẳng tay (manh/P_y_xiaobi.png). Ở slot P_ci04 (vẽ SAU cẳng tay) mũi tên chui ra ở mép, rời khỏi lỗ."""
    pj = os.path.join(M.MANH, "moi.json")
    moi = json.load(open(pj))
    d = moi["kt_ci04"]
    d0 = json.load(open(os.path.join(MANH1, "moi.json")))["kt_ci04"]
    Vw = np.array(d0["the_gioi"], float)
    # tâm lỗ: lòng tối được vòng xanh bao, trong ảnh vùng cẳng tay của mình
    A = np.asarray(Image.open(os.path.join(M.MANH, "P_y_xiaobi.png")).convert("RGBA")).astype(np.int32)
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    xanh = (A[..., 3] > 128) & (g > 150) & (g - r > 40) & (g - b > 40)
    n, lab, st, cen = cv2.connectedComponentsWithStats(xanh.astype(np.uint8), 8)
    j = 1 + int(np.argmax(st[1:, 4]))
    cx, cy = cen[j]
    G._C.pop("att", None)
    _, _, atts = G.nap("att_idle0.json")
    a = next(a for a in atts if a["slot"] == "P_y_xiaobi")
    Wd = M._the_gioi_o(a, A.shape[1], A.shape[0])
    lo = Wd[int(round(cy)), int(round(cx))]
    # đầu cắm của mũi tên: đầu trục chính gần gốc xương bone19 nhất (ảnh kt_ci04 → thế giới qua 4 góc)
    im = np.asarray(Image.open(os.path.join(M.MANH, "kt_ci04.png")).convert("RGBA"))
    ys, xs = np.nonzero(im[..., 3] > 120)
    P = np.c_[xs, ys].astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    pr = (P - c) @ vt[0]
    hw, hh = im.shape[1], im.shape[0]

    def tg(q):
        u, v = q[0] / hw, q[1] / hh
        return Vw[0] * (1 - u) * (1 - v) + Vw[1] * u * (1 - v) + Vw[2] * u * v + Vw[3] * (1 - u) * v
    e1, e2 = tg(c + vt[0] * pr.min()), tg(c + vt[0] * pr.max())
    D = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    gb = next(np.array([b_["x"], b_["y"]]) for b_ in D["bones"] if b_["name"] == "bone19")
    goc = e1 if np.hypot(*(e1 - gb)) < np.hypot(*(e2 - gb)) else e2
    dv = lo - goc
    d.update(slot="P_ci03", xuong="bone20", the_gioi=(Vw + dv).tolist(), he="lon")
    moi["kt_ci04"] = d
    json.dump(moi, open(pj, "w"), indent=1)
    G._C.pop("att", None)
    print(f"mũi tên → slot P_ci03 (trước cẳng tay), dời ({dv[0]:+.1f}, {dv[1]:+.1f}) đơn vị cho đầu cắm vào lỗ ({cx:.0f}, {cy:.0f}) px")


# ================================================================ mắt: cắt thẳng từ concept C
def cat_mat():
    T, Ti, spx = phep_can()
    Cn = np.asarray(Image.open(M.CON).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = MAT_HOP
    sub = Cn[y0:y1, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    xanh = (g > 150) & (g - r > 40) & (g - b > 60)
    xanh = cv2.morphologyEx(xanh.astype(np.uint8), cv2.MORPH_OPEN, M.el(1))
    n, lab, st, _ = cv2.connectedComponentsWithStats(xanh, 8)
    keep = [i for i in range(1, n) if st[i, 4] > 30]
    xanh = np.isin(lab, keep)
    m = cv2.dilate(xanh.astype(np.uint8), M.el(3)).astype(bool)
    ys, xs = np.nonzero(m)
    a0, b0, a1, b1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    mm = m[b0:b1, a0:a1]
    al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.7) * 1.2, 0, 1)
    rgba = np.dstack([sub[b0:b1, a0:a1].astype(np.uint8), (al * 255).astype(np.uint8)])
    k = 1.0 / spx * (M.RES * 0.5)
    out = Image.fromarray(rgba, "RGBA").convert("RGBa")
    out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
    os.makedirs(M.MANH, exist_ok=True)
    out.save(os.path.join(M.MANH, "mat.png"))
    hop = np.array([[a0, b0], [a1, b0], [a1, b1], [a0, b1]], float) + np.array([x0, y0])
    if "mu" in M.CHINH:
        c_ = M.CHINH["mu"]
        hop = hop + np.array([c_.get("dx", 0.0), c_.get("dy", 0.0)])
    pj = os.path.join(M.MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    moi["mat"] = dict(slot="P_mat", xuong="bone5", hop=[int(v) for v in hop[0].tolist() + hop[2].tolist()], the_gioi=Ti(hop).tolist(),
                      to="MAT", moi_slot=True, sau="P_tou")
    json.dump(moi, open(pj, "w"), indent=1)
    print("MAT → mat.png", out.size, f"{len(keep)} cụm xanh")


# ================================================================ chép phần dùng lại
def chep_dung_lai():
    os.makedirs(M.MANH, exist_ok=True)
    for r in DUNG_LAI:
        shutil.copy(os.path.join(MANH1, r + ".png"), os.path.join(M.MANH, r + ".png"))
    moi1 = json.load(open(os.path.join(MANH1, "moi.json")))
    pj = os.path.join(M.MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    for ten in MOI_LON:
        d = dict(moi1[ten])
        d["he"] = "lon"
        moi[ten] = d
        shutil.copy(os.path.join(MANH1, ten + ".png"), os.path.join(M.MANH, ten + ".png"))
    json.dump(moi, open(pj, "w"), indent=1)
    print(f"chép {len(DUNG_LAI)} mảnh lưới + {len(MOI_LON)} mảnh cứng (he lon) từ dạng 2")


def huong_dan(ps):
    p = os.path.join(M.GUI, "HUONG_DAN.md")
    cu = open(p, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip() if os.path.exists(p) else ""
    t = [cu, "", "## Lượt 2: mảnh theo concept C đã duyệt (2026-11-17)", "",
         "Claude tự gen bằng Codex và tự cắt; người dùng không cần làm gì. Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, vi, pr, ims, out in ps:
        t += [f"### {ten}", "", f"{vi} → `{M.Wp(out)}`", "", f"**Chỉ gửi GPT đường dẫn:** `{M.Wp(pr)}`.", "",
              "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        t += [f"| {i} | `{M.Wp(a)}` | {b} |" for i, (a, b) in enumerate(ims, 1)]
        t += [""]
    t += ["Kiểm: mỗi mảnh đúng hình bóng, chỗ, cỡ như tờ mẫu (tờ K); mũ đúng chỗ, đúng cỡ như concept (tờ R); tô phẳng, không bóng, nền "
          "trắng tinh.", "",
          "Câu sửa nhanh: \"keep every part exactly the same outline, size and place as in image 1\"; \"flat colours only, no shading, no "
          "glow\"; \"no gold border on the cape\"; \"draw the helmet only, without the eyes and without the flames\"."]
    M.ghi(p, t)
    print(p)


def to_het():
    can()
    lop_goc()
    ps = []
    for ma in ("K1", "K2"):
        o = M.to_k(ma)
        if ma == "K2":
            x, y, dd = lo_ten()
            print(f"  lỗ mũi tên trên tờ K2: ({x:.0f}, {y:.0f}), lệch lưới {dd:.1f} đơn vị")
            M.MO_TA_K["P_y_xiaobi"] = M.MO_TA_K["P_y_xiaobi"].replace(
                "NO rune", f"and at about x = {x:.0f}, y = {y:.0f} on the sheet ONE small round dark HOLE with a thin flat green "
                           f"{C_['lua']} ring round it (an arrow will stick in there: draw NO arrow); NO rune")
        p, mau, out = M.prompt_k(ma, o)
        ps.append((f"Tờ mảnh giữ hình bóng {ma}", M.VI_K[ma], p,
                   [(mau, f"Mảnh gốc cắt theo lưới, phóng to: {M.VI_K[ma]}"), (M.CON, "Concept C dạng 1 đã duyệt"),
                    (M.SOI_GIAP, "Sói giáp sắt: chỉ lấy nét, cách tô sắt")], out))
    for ma, p, out in M.prompt_r():
        ps.append((f"Tờ mảnh đổi dáng {ma}", M.VI_R[ma], p, [(M.CON, "Concept C dạng 1 đã duyệt")], out))
    huong_dan(ps)
    chep_dung_lai()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        for ma in ("K1", "K2"):
            if chi in ("", ma):
                M.cat_k(ma)
        if chi in ("", "K2", "TEN"):
            sua_ten()
        if chi in ("", "R"):
            M.cat_r()
        if chi in ("", "MAT"):
            cat_mat()
    else:
        print(__doc__)
