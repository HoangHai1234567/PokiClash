# -*- coding: utf-8 -*-
"""Thú một sừng đảo Mộc (giac_moc, hướng A "thú cổ thụ" đã duyệt 2026-11-13): MẢNH theo đúng cách tách của rig gốc monster_3804
(skill pokiclash-spine-rig mục 00: "vẽ mảnh ĐÚNG KHUNG từng part", "các khúc NỐI NHAU gen LIỀN một ảnh rồi cắt").

Ba loại mảnh:
- THÂN LIỀN (mông, vai, cổ, đùi + ống + bàn của bốn chân): MỘT tờ hình bóng hợp ở dáng gốc → Codex vẽ lại → nướng vào khung từng part
  qua lưới của nó (`to_lien`, `cat_lien`). Không gen từng khúc, không xoá mực chỗ nối.
- KHUNG PART (mọi mảnh không nối liền màu: bờm lá, mào đầu, tinh thể, gai lưng, tấm vỏ ngực, sườn, vành, lá vành, lòng ngực, rêu, gai,
  ngón chân): mỗi part một ô đúng khung ảnh vùng × z, hình bóng kín tô phẳng theo thiết kế của mình (`nhom_part`, `cat_part`, `so_part`).
- MẢNH CỦA MÌNH: đầu liền sừng (cắt từ concept, làm ở giac_moc_rig.py), quả tim (ô thêm `tim` trên tờ F).

    giac_moc_manh.py nhom_part            tờ hướng dẫn mau/part_<tờ>.png + .json (tự chọn tỉ lệ phóng lớn nhất còn vừa tờ)
    giac_moc_manh.py cat_part <tờ> [ep]   cắt tai_ve/N_<tờ>*.png → manh/part/<vùng>.png, in IoU
    giac_moc_manh.py so_part              tờ so mau/so_part.png (đỏ = thiếu, xanh lá = thừa)
    giac_moc_manh.py to_lien              tờ thân liền mau/lien.png + lien.json
    giac_moc_manh.py cat_lien             nướng tai_ve/N_lien*.png vào khung từng part
"""
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import giac_moc as G  # noqa: E402
import giac_moc_bo_cuc as BC  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
INK = (43, 33, 24)
ATT = "att_goc.json"                         # dáng gốc của rig (gần trùng khung 0 idle; lưới gắn vào xương theo dáng này)
MANH = os.path.join(G.BASE, "manh")
MAU, TAI = G.MAU, G.TAI
PAL = dict(BC.HUONG["co_thu"], la_vanh=(130, 176, 80), re=(214, 188, 140), tim_vong=(232, 168, 56))
A_TL = 0.501                                 # px ảnh vùng của họ cho mỗi đơn vị rig
NET = 3.4                                    # bề dày nét mực đích, tính bằng px ảnh vùng (≈ 6,8 đơn vị rig, như concept)

# tờ khung part: {tờ: [vùng ảnh ...]}; tỉ lệ phóng tự chọn. Ô THÊM (không có trong rig gốc): xem THEM.
TO = {
    "A": ["B_beimao_02", "B_beimao_01", "B_beimao_06", "B_beimao_05", "B_beimao_03", "B_beimao_11"],
    "B": ["B_beimao_07", "B_beimao_08", "B_beimao_09", "B_beimao_10", "B_beimao_04", "P_beifa_1", "P_beifa_2"],
    "C": ["P_toufa3", "P_toufa2", "P_toufa4", "P_toufa5", "P_toufa1", "B_tou_B_01", "S_shitou_01", "S_shitou_02", "S_shitou_03",
          "S_shitou_04", "S_shitou_05", "P_bei_01", "P_bei_02", "P_bei_03", "P_bei_04", "P_bei_05"],
    "D": [f"B_bozi_C_{i:02d}" for i in range(1, 11)] + [f"B_bozi_B_{i:02d}" for i in range(1, 9)] + [f"B_bozi_F_{i:02d}" for i in range(1, 4)],
    "E": [f"B_bozi_D_{i:02d}" for i in range(1, 10)] + [f"B_bozi_E_{i:02d}" for i in range(1, 9)]
         + ["B_bozi_A_03", "P_bozi01", "P_bozi02", "P_bozi03", "P_tou2"],
    "F": ["P_shenti_02", "tim", "B_bozi_E_10", "B_bozi_E_11", "B_bozi_E_12", "B_bozi_A_04"],
    "H": ["P_tuimao_L01", "P_tuimao_L02", "P_tuimao_L03", "P_tuimao_R01", "P_tuimao_R02", "P_tuimao_R03", "P_tuimao_R04",
          "P_tuijiao_L01", "P_tuijiao_R01", "P_tuijiao_R02"],
    "G": [f"T{c}_tui{s}_3_{i}" for c in "HQ" for s in "LR" for i in range(1, 5)]
         + ["TH_tuiL_2_1", "TH_tuiL_2_2", "TH_tuiR_2_1", "TH_tuiR_2_2", "TQ_tuiL_2_2", "TQ_tuiR_2_2"],
}
THEM = {"tim": 106}                          # ô thêm: cạnh ô vuông tính bằng px ảnh vùng (quả tim đường kính ~212 đơn vị rig)
# part của họ KHÔNG dùng: hai cụm lỗ trên lòng ngực (thay bằng quả tim), đầu + sừng + sừng nhỏ (đầu liền sừng của mình cắt từ concept),
# hai region tí hon B_bozi_A_01/02
BO_PART = ("P_shenti_02_1", "P_shenti_02_2", "P_tou1", "P_tou_jiao_1", "P_tou_jiao_2", "B_bozi_A_01", "B_bozi_A_02")
LIEN = dict(gan=["P_shenti04", "P_shenti_01", "B_bozi_1", "TH_tuiR_1", "TH_tuiR_2", "TH_tuiR_3", "TQ_tuiR_1", "TQ_tuiR_2", "TQ_tuiR_3"],
            xa=[["TH_tuiL_1", "TH_tuiL_2", "TH_tuiL_3"], ["TQ_tuiL_1", "TQ_tuiL_2", "TQ_tuiL_3"]])
# chỗ GPT vẽ HỤT so với hình bóng chỉ tô bù (bằng màu tờ hướng dẫn) cho mảnh phải lấp kín; lá, rêu, tinh thể, gai... vẽ nhỏ hơn hình
# bóng một chút không sao, tô bù thì mép lá thành răng cưa nhoè của hình bóng gốc (lỗi soi 2026-11-13)
BU = ("long", "bung", "vo", "vo_nhat")
Z_LIEN = 1.6                                 # tỉ lệ ô của các part thân liền (px ô / px ảnh vùng)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def theo_vung():
    """{vùng ảnh: att đầu tiên dùng vùng đó} ở dáng gốc."""
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    out = {}
    for a in atts:
        out.setdefault(a["region"], a)
    return out


_BY = {}


def by():
    if not _BY:
        _BY.update(theo_vung())
    return _BY


def vai(ten):
    a = by()[ten]
    return BC.vai(a["slot"], a["region"])


def co_o(ten, z):
    if ten in THEM:
        return int(round(THEM[ten] * z)), int(round(THEM[ten] * z))
    _, imgs, _ = G.nap(ATT)
    im = imgs[ten]
    return int(round(im.width * z)), int(round(im.height * z))


_B = {}


def bong(ten, z):
    """hình bóng KÍN của part trong khung ảnh vùng × z (làm trơn nhẹ trên ảnh đã đệm viền: mép cắt thẳng không thành mấu)."""
    k = (ten, round(z, 3))
    if k not in _B:
        src = G.part_goc(by()[ten])
        w, h = co_o(ten, z)
        al = np.asarray(src.resize((w, h), Image.LANCZOS))[..., 3]
        d = int(round(3 * z)) + 2
        m = np.pad((al > 100).astype(np.uint8), d)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(1.0 * z))
        m = cv2.GaussianBlur(m * 255, (0, 0), 0.8 * z) > 127
        m = m[d:-d, d:-d]
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        if n > 2:
            m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        _B[k] = m
    return _B[k]


def net(m, z):
    """bề dày nét mực (px ô) cho một ô: NET × z, mảnh nhỏ thì mảnh bớt."""
    h, w = m.shape
    return max(1.5, min(NET * z, 0.14 * min(w, h)))


def xuong_duoi(ten, w, h):
    """hướng 'xuống đất' của thế giới (dáng gốc) tính trong hệ pixel của ô (vectơ đơn vị)."""
    a = by()[ten]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    A = np.c_[V, np.ones(len(V))]
    M, *_ = np.linalg.lstsq(A, U, rcond=None)            # thế giới → ô
    d = np.array([0.0, -1.0]) @ M[:2]
    return d / (np.linalg.norm(d) + 1e-9)


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    if ten in THEM:
        return o_them(ten, z)
    m = bong(ten, z)
    h, w = m.shape
    v = vai(ten)
    im = np.full((h, w, 3), 255, np.uint8)
    im[m] = PAL[{"khe": "la_vanh"}.get(v, v)]
    nt = net(m, z)
    trong = cv2.erode(m.astype(np.uint8), el(nt)).astype(bool)
    if ten.startswith("B_bozi_E_1"):                                  # ba dải vách xa của bầu ngực: vỏ cây sẫm
        im[m] = PAL["vo"]
    if re.match(r"^T[HQ]_tui[LR]_3_\d$", ten):                        # ngón chân: móng hổ phách ở đúng chỗ móng của họ
        src = np.asarray(G.part_goc(by()[ten]).resize((w, h), Image.LANCZOS)).astype(int)
        mong = (src[..., 3] > 100) & (src[..., 0] > 140) & (src[..., 2] > 160) & (src[..., 1] < np.minimum(src[..., 0], src[..., 2]) - 22)
        mong = cv2.morphologyEx(mong.astype(np.uint8), cv2.MORPH_CLOSE, el(1.2 * z))
        mong = cv2.morphologyEx(mong, cv2.MORPH_OPEN, el(0.8 * z)).astype(bool) & m
        im[mong] = PAL["tinh_the"]
        im[cv2.morphologyEx(mong.astype(np.uint8), cv2.MORPH_GRADIENT, el(0.5 * nt)).astype(bool) & trong] = INK
    if ten.startswith("B_bozi_C_"):                                   # tấm vỏ ngực: dải sáng hổ phách dọc mép DƯỚI (khe giữa các tấm)
        d = xuong_duoi(ten, w, h)
        k = 2.6 * z + nt
        M2 = np.float32([[1, 0, -d[0] * k], [0, 1, -d[1] * k]])
        lui = cv2.warpAffine(m.astype(np.uint8), M2, (w, h), flags=cv2.INTER_NEAREST).astype(bool)
        im[m & ~lui] = PAL["khe"]
    if ten == "P_shenti_02":                                          # lòng ngực: hốc sẫm, vài sợi rễ nhạt chạy dọc
        ys, xs = np.nonzero(m)
        for j, fx in enumerate((0.30, 0.52, 0.72)):
            pts = []
            for fy in np.linspace(0.06, 0.94, 9):
                y = ys.min() + (ys.max() - ys.min()) * fy
                row = xs[np.abs(ys - int(y)) <= 1]
                if len(row):
                    pts.append((int(row.min() + (row.max() - row.min()) * (fx + 0.06 * np.sin(5 * fy + j))), int(y)))
            if len(pts) > 2:
                cv2.polylines(im, [np.array(pts, np.int32)], False, PAL["re"], int(round(2.2 * z)), cv2.LINE_AA)
        im[~m] = 255
    im[m & ~trong] = INK
    im[~m] = 255
    return im, m


def o_them(ten, z):
    w, h = co_o(ten, z)
    im = np.full((h, w, 3), 255, np.uint8)
    if ten == "tim":                                                  # quả tim: cầu vàng, một vòng hổ phách sát viền, dấu xoắn ở giữa
        c, r = (w // 2, h // 2), int(w * 0.47)
        nt = int(round(NET * z))
        cv2.circle(im, c, r, INK, -1, cv2.LINE_AA)
        cv2.circle(im, c, r - nt, PAL["tim_vong"], -1, cv2.LINE_AA)
        cv2.circle(im, c, r - nt - int(5 * z), PAL["tim"], -1, cv2.LINE_AA)
        pts = [(c[0] + 0.035 * w * t * np.cos(1.9 * t), c[1] + 0.035 * w * t * np.sin(1.9 * t)) for t in np.linspace(0.6, 5.2, 60)]
        cv2.polylines(im, [np.array(pts, np.int32)], False, PAL["tim_vong"], int(round(2.2 * z)), cv2.LINE_AA)
    return im, im.min(axis=2) < 236


def xep(ds, z, le=26):
    """xếp kệ (cao trước); trả {tên: (x, y, w, h)} hoặc None nếu không vừa tờ."""
    cs = sorted(ds, key=lambda t: -co_o(t, z)[1])
    x, y, hh, out = le, le, 0, {}
    for t in cs:
        w, h = co_o(t, z)
        if w + 2 * le > W:
            return None
        if x + w + le > W:
            x, y, hh = le, y + hh + le, 0
        if y + h + le > H:
            return None
        out[t] = (x, y, w, h)
        x += w + le
        hh = max(hh, h)
    return out


def nhom_part(chi=None):
    os.makedirs(MAU, exist_ok=True)
    for to, ds in TO.items():
        if chi and to not in chi:
            continue
        z = 8.0
        while xep(ds, z) is None:
            z = round(z - 0.1, 2)
        cho = xep(ds, z)
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        for ten in ds:
            x, y, w, h = cho[ten]
            cell, m = thiet_ke(ten, z)
            im[y:y + h, x:x + w] = cell[:h, :w]
            khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z}
        Image.fromarray(im).save(os.path.join(MAU, f"part_{to}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_{to}.json"), "w", encoding="utf-8"), indent=1)
        print(f"{to} (x{z}, nét ~{NET * z:.0f} px): " + ", ".join(f"{k} {v['w']}x{v['h']}@{v['x'] + v['w'] // 2},{v['y'] + v['h'] // 2}" for k, v in khung.items()))


def zs():
    out = {}
    for to in TO:
        p = os.path.join(MAU, f"part_{to}.json")
        if os.path.exists(p):
            for k, v in json.load(open(p, encoding="utf-8")).items():
                out[k] = v["z"]
    for ds in [LIEN["gan"]] + LIEN["xa"]:
        for t in ds:
            out[t] = Z_LIEN
    return out


def cat_part(to, ep=False):
    """cắt tờ N_<tờ>: mỗi part lấy đúng Ô của nó, tách nền trắng → manh/part/<vùng>.png. Đo IoU với hình bóng hướng dẫn; chỉ ghi đè khi
    bản mới khít hơn (ep: ghi đè). Dọn bằng mã (không vẽ): cắt sát hình bóng nới vài px; chỗ vẽ hụt lấy màu tô gần nhất của tờ hướng
    dẫn; kẻ nét mực dọc phía trong mép lưới của họ."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, f"N_{to}")
    if not path:
        print(to, "chưa có ảnh")
        return
    khung = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, f"_N_{to}_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=120, gop_px=10)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    ids = [i for m_ in tt.manh for i in m_["ids"]]
    print(os.path.basename(path))
    kem = []
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236
        d = 12 if ten in THEM else 0
        x0, y0, x1, y1 = max(0, x - d), max(0, y - d), min(W, x + w + d), min(H, y + h + d)
        cell = tt.rgba[y0:y1, x0:x1].copy()
        lab = tt.lab[y0:y1, x0:x1]
        gg = np.zeros(lab.shape, bool)
        gg[y - y0:y - y0 + h, x - x0:x - x0 + w] = g
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[gg].ravel().tolist()) - {0}:
            if i in ids:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & gg).sum() / max(1, (a | gg).sum())
        cu = SO.get(ten, [0, ""])
        if not ep and cu[1] and cu[0] >= iou:
            print(f"  {ten}: IoU {iou:.2f}, giữ bản cũ (IoU {cu[0]:.2f})")
            continue
        bu = 0
        if ten not in THEM:
            sat = cv2.dilate(g.astype(np.uint8), el(0.75 * z)).astype(bool)
            cell[..., 3][~sat] = 0
            a &= sat
            ho = g & ~a
            bu = int(ho.sum()) if vai(ten) in BU else 0
            if ho.any() and vai(ten) in BU:
                gc = gd[y:y + h, x:x + w]
                to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105)
                if to_.any():
                    _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                    tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                    tra[lb[to_]] = gc[to_]
                    cell[ho, :3] = tra[lb][ho]
                    cell[ho, 3] = 255
            at = by()[ten]
            hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
            dai = hm.astype(bool) & ~cv2.erode(hm, el(0.9 * z), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), os.path.basename(path)]
        Image.fromarray(cell, "RGBA").save(os.path.join(ra, ten + ".png"))
        if iou < 0.9 and ten not in THEM:
            kem.append(f"{ten} {iou:.2f}")
        print(f"  {ten}: {cell.shape[1]} x {cell.shape[0]} (x{z}), IoU {iou:.2f}" + (f", bù {bu} px" if bu else ""))
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)
    print("  IoU < 0,9:", ", ".join(kem) if kem else "không có")


def so_part(chi=None):
    cells = []
    for to in TO:
        pj = os.path.join(MAU, f"part_{to}.json")
        if not os.path.exists(pj) or (chi and to not in chi):
            continue
        Kh = json.load(open(pj, encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for ten, v in Kh.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm) or ten in THEM:
                continue
            x, y, w, h = v["x"], v["y"], v["w"], v["h"]
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 255, np.uint8)
            im[a] = c[..., :3][a]
            im[g & ~a] = (255, 0, 0)
            im[a & ~g] = (im[a & ~g] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            cells.append(im)
    Wd, x, y, hh, pos = 2200, 0, 0, 0, []
    for im in cells:
        h, w = im.shape[:2]
        if x + w > Wd:
            x, y, hh = 0, y + hh + 10, 0
        pos.append((x, y))
        x += w + 10
        hh = max(hh, h)
    S = np.full((y + hh, Wd, 3), 230, np.uint8)
    for im, (x, y) in zip(cells, pos):
        S[y:y + im.shape[0], x:x + min(im.shape[1], Wd - x)] = im[:, :Wd - x]
    p = os.path.join(MAU, "so_part" + ("_" + "".join(chi) if chi else "") + ".png")
    Image.fromarray(S).save(p)
    print(p, len(cells), "ô")


# ================================================================ THÂN LIỀN
def bong_tg(a, T, cao, rong, tron=3.0, S2=2):
    """hình bóng kín của một part đặt theo toạ độ thế giới dáng gốc qua phép T (thế giới → px tờ), phóng S2."""
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (rong * S2, cao * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def to_lien():
    """tờ hướng dẫn thân liền → mau/lien.png + lien.json (px mỗi đơn vị rig, gốc toạ độ từng nhóm)."""
    B = by()
    S2 = 2
    nhom = [LIEN["gan"]] + LIEN["xa"]
    hop = []
    for ds in nhom:
        P = np.concatenate([np.array(B[t]["xy"], float).reshape(-1, 2) for t in ds])
        hop.append((P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()))
    g = hop[0]
    rong_xa = sum(h[2] - h[0] for h in hop[1:])
    cao = max(h[3] - h[1] for h in hop)
    ti = min((H - 70) / cao, (W - 70 - 50 * len(hop)) / (g[2] - g[0] + rong_xa))
    thu_tu = [1, 0, 2]                           # [chân sau xa] [thân + chân gần] [chân trước xa]; đáy các nhóm cùng một đường
    tong = sum((hop[i][2] - hop[i][0]) * ti for i in thu_tu) + 50 * (len(thu_tu) - 1)
    x = (W - tong) / 2
    day = (H + cao * ti) / 2
    goc = {}
    for i in thu_tu:
        h = hop[i]
        goc[i] = (x - h[0] * ti, day + h[1] * ti)                    # px = (ox + X·ti, oy − Y·ti)
        x += (h[2] - h[0]) * ti + 50
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    for i, ds in enumerate(nhom):
        ox, oy = goc[i]
        T2 = lambda p_, ox=ox, oy=oy: np.stack([ox + np.asarray(p_, float)[..., 0] * ti, oy - np.asarray(p_, float)[..., 1] * ti], -1)
        ms = {t: bong_tg(B[t], T2, H, W) for t in ds}
        m = np.zeros((H * S2, W * S2), bool)
        ban = np.zeros_like(m)
        for t in ds:
            m |= ms[t]
            if t.endswith("_3"):
                ban |= ms[t]
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(5)).astype(bool)
        can[m] = PAL["than"]
        # bàn chân: rễ sẫm; chỗ bàn chân chồng lên ống chân thì nhường ống chân phần trên cổ chân (ranh là mép trên của mảnh bàn chân)
        can[ban & m] = PAL["ban_chan"]
        can[cv2.morphologyEx(ban.astype(np.uint8), cv2.MORPH_GRADIENT, el(3)).astype(bool) & m] = INK
        can[m & ~cv2.erode(m.astype(np.uint8), el(7)).astype(bool)] = INK
    os.makedirs(MAU, exist_ok=True)
    Image.fromarray(can).resize((W, H), Image.LANCZOS).save(os.path.join(MAU, "lien.png"))
    json.dump({"ti": ti, "goc": {str(i): goc[i] for i in goc}, "nhom": nhom}, open(os.path.join(MAU, "lien.json"), "w"), indent=1)
    print(os.path.join(MAU, "lien.png"), f"{ti:.3f} px mỗi đơn vị rig; nhóm:", [len(d) for d in nhom])


def _the_gioi_o(a, w, h):
    """toạ độ thế giới (dáng gốc) của từng pixel trong khung ảnh vùng (w × h) của một part, qua lưới của nó; NaN ngoài lưới."""
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    ys, xs = np.mgrid[0:h, 0:w]
    P = np.c_[xs.ravel() + 0.5, ys.ravel() + 0.5]
    Wd = np.full((len(P), 2), np.nan)
    tot_nhat = np.full(len(P), -9.0)
    for t in np.array(a["tris"]).reshape(-1, 3):
        A_, B_, C_ = U[t[0]], U[t[1]], U[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, P - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        den = den if abs(den) > 1e-9 else 1e-9
        b1 = (v2[:, 0] * v1[1] - v2[:, 1] * v1[0]) / den
        b2 = (v0[0] * v2[:, 1] - v0[1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        tol = 6.0 / max(1.0, float(np.sqrt(abs(den))))
        nho = np.minimum(np.minimum(b0, b1), b2)
        hon = (nho >= -tol) & (nho > tot_nhat)
        Wd[hon] = b0[hon, None] * V[t[0]] + b1[hon, None] * V[t[1]] + b2[hon, None] * V[t[2]]
        tot_nhat[hon] = nho[hon]
    return Wd.reshape(h, w, 2)


def cat_lien():
    """nướng tờ thân liền (tai_ve/N_lien*.png) vào khung từng mảnh → manh/part/<vùng>.png."""
    from quai import anh
    path = anh.to_moi_nhat(TAI, "N_lien")
    if not path:
        raise SystemExit("chưa có N_lien.png")
    L = json.load(open(os.path.join(MAU, "lien.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, "_N_lien_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=600, gop_px=10)
    rgba = tt.rgba.astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:4] / 255.0
    B = by()
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    ti = L["ti"]
    z_ = Z_LIEN
    print(os.path.basename(path))
    for i, ds in enumerate(L["nhom"]):
        ox, oy = L["goc"][str(i)]
        for ten in ds:
            a = B[ten]
            w, h = co_o(ten, z_)
            Wd = _the_gioi_o(a, w, h)
            ok = ~np.isnan(Wd[..., 0])
            mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
            my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
            cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            al = cell[..., 3:4]
            cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
            sil = cv2.dilate(bong(ten, z_).astype(np.uint8), el(0.7 * z_)).astype(np.float32)
            sil = np.clip(cv2.GaussianBlur(sil, (0, 0), 0.45 * z_) * 2.0 - 0.5, 0.0, 1.0)
            cell[..., 3] *= sil
            out = np.clip(cell, 0, 255).astype(np.uint8)
            Image.fromarray(out, "RGBA").save(os.path.join(ra, ten + ".png"))
            phu = float((out[..., 3] > 127).sum()) / max(1, int(bong(ten, z_).sum()))
            print(f"  {ten}: {w} x {h}, phủ {phu:.2f} hình bóng của part")


def main(a):
    lenh = a[0] if a else ""
    if lenh == "nhom_part":
        nhom_part(a[1:] or None)
    elif lenh == "cat_part":
        for to in (a[1].split(",") if len(a) > 1 and a[1] != "het" else list(TO)):
            cat_part(to, ep=len(a) > 2)
    elif lenh == "so_part":
        so_part(a[1:] or None)
    elif lenh == "to_lien":
        to_lien()
    elif lenh == "cat_lien":
        cat_lien()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
