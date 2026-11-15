# -*- coding: utf-8 -*-
"""Hổ lửa đảo Hỏa (hoa_ho, concept A "bạch hổ mây lửa" đã duyệt 2026-11-14): MẢNH theo đúng cách tách của rig gốc monster_3645
(skill pokiclash-spine-rig mục 00: "vẽ mảnh ĐÚNG KHUNG từng part", "các khúc NỐI NHAU gen LIỀN một ảnh rồi cắt").

Hai loại mảnh:
- LIỀN (mỗi nhóm một hình bóng hợp ở dáng gốc, chỉ viền ngoài → Codex vẽ lại → nướng vào khung từng part qua lưới của nó):
    than = ngực + mông; mỗi chân một nhóm (đùi + ống + bàn); đuôi (hai đoạn). Hai tờ: LA (thân, đuôi, chân sau xa), LB (ba chân còn lại).
  Con gốc che chỗ nối chân – thân bằng mây và vòng cổ chân; mình giữ cách đó (mỗi chân có viền riêng, trong một chân không có nét nối).
- KHUNG PART (mọi mảnh không nối liền màu: 22 cụm mây lửa, hai chỏm lửa trán, ba mảnh mày, sáu vòng cổ chân, tám ngón chân gần, các
  mảnh đầu): mỗi part một ô đúng khung ảnh vùng × z, hình bóng kín tô phẳng theo thiết kế của mình.
BỎ: sừng, khuyên, chuông (người dùng dặn), hai chùm râu xoắn `P_L_huxu`, `P_R_huxu` (concept đã duyệt không có; vệt xoắn đỏ vẽ ngay trên
má). Mắt nhắm `P_biyan` do mã vẽ (hai nét mí).

    hoa_ho_manh.py nhom_part [tờ...]      tờ hướng dẫn mau/part_<tờ>.png + .json
    hoa_ho_manh.py cat_part <tờ|het> [ep] cắt tai_ve/N_<tờ>*.png → manh/part/<vùng>.png, in IoU
    hoa_ho_manh.py so_part [tờ...]        tờ so mau/so_part.png (đỏ = thiếu, xanh lá = thừa)
    hoa_ho_manh.py to_lien                tờ liền mau/lien_LA.png, lien_LB.png + .json
    hoa_ho_manh.py cat_lien [LA|LB]       nướng tai_ve/N_LA*.png, N_LB*.png vào khung từng part
    hoa_ho_manh.py biyan                  vẽ mắt nhắm → manh/part/P_biyan.png
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
import hoa_ho as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
INK = (43, 33, 24)
ATT = "att_goc.json"
MANH = os.path.join(G.BASE, "manh")
MAU, TAI = G.MAU, G.TAI
PAL = dict(long=(242, 236, 222), ban_chan=(226, 214, 196), may=(214, 64, 42), may_loi=(244, 150, 48), chom=(244, 150, 48),
           chom_loi=(248, 200, 74), vong=(226, 170, 62), nanh=(250, 246, 232), tai=(242, 236, 222), tai_trong=(238, 170, 150),
           mong=(58, 52, 56), mieng=(142, 36, 32), may_mat=(214, 64, 42), mat=(248, 196, 60), mi=(70, 52, 48), than_duoi=(90, 84, 88))
A_TL = 0.501                                 # px ảnh vùng của họ cho mỗi đơn vị rig
NET = 2.9                                    # bề dày nét mực đích (px ảnh vùng) ≈ 5,8 đơn vị rig, như concept

MAY = ["P_maofa_01", "P_maofa_02", "P_maofa_05", "P_maofa_06", "P_maofa_07", "P_maofa_08", "P_maofa_09", "P_maofa_10", "P_maofa_11",
       "P_maofa_12", "P_maofa_13", "P_maofa_14", "P_maofa_15", "P_maofa_16", "P_maofa_17", "P_maofa_19", "P_maofa_20", "P_maofa_21",
       "P_maofa_22", "P_maofa_23", "P_maofa_23_01", "P_maofa_24"]
TO = {
    "M1": [], "M2": [], "M3": [],            # mây: chia theo cỡ ở _chia_may()
    "D": ["P_tou", "P_zui", "P_zui_01", "P_yanjing", "liaoya_01", "liaoya_02", "P_ya_01", "P_ya_02", "P_L_erduo", "P_R_erduo",
          "P_maofa_03", "P_maofa_04", "P_meimao_01", "P_meimao_02", "P_meimao_03"],
    "E": [f"jiaphuan_{i:02d}" for i in range(1, 7)] + [f"P_R_jiaozhi_{i:02d}" for i in range(1, 5)]
         + [f"P_R_houjiaozhi_{i:02d}" for i in range(1, 5)],
}
BO_PART = ("P_jiao", "P_tiehuan", "P_lingdang", "P_L_huxu", "P_R_huxu")
NHOM = {
    "than": ["P_tun", "P_shenti_01"],
    "duoi": ["P_weiba_02", "P_weiba_01"],
    "chan_sau_xa": ["P_L_houdatui", "P_L_houxiaotui", "P_L_houxiaotui_02", "P_L_houjiao_01"],
    "chan_truoc_xa": ["P_L_datui", "P_L_xiaotui", "P_L_jiao"],
    "chan_sau_gan": ["P_R_houdatui", "P_R_houxiaotui", "P_R_houxiaotui_02", "P_R_houjiaozhang"],
    "chan_truoc_gan": ["P_R_datui", "P_R_xiaotui", "P_R_jiao"],
}
TO_LIEN = {"LA": ["chan_sau_xa", "than", "duoi"], "LB": ["chan_sau_gan", "chan_truoc_gan", "chan_truoc_xa"]}
BAN = ("P_L_houjiao_01", "P_L_jiao", "P_R_houjiaozhang", "P_R_jiao")       # bàn chân
BAN_MONG = ("P_L_houjiao_01", "P_L_jiao")                                   # bàn chân xa: móng vẽ liền trong ảnh
Z_LIEN = 2.0                                 # tỉ lệ ô của các part liền (px ô / px ảnh vùng)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_BY = {}


def by():
    if not _BY:
        G._C.pop("att", None)
        _, _, atts = G.nap(ATT)
        for a in atts:
            _BY.setdefault(a["region"], a)
    return _BY


def _chia_may():
    if TO["M1"]:
        return
    _, imgs, _ = G.nap(ATT)
    ds = sorted(MAY, key=lambda t: -imgs[t].width * imgs[t].height)
    TO["M1"], TO["M2"], TO["M3"] = ds[:6], ds[6:13], ds[13:]


def vai(ten):
    if ten in ("P_maofa_03", "P_maofa_04"):
        return "chom"
    if ten.startswith("P_meimao"):
        return "may_mat"
    if ten.startswith("P_maofa"):
        return "may"
    if ten.startswith("jiaphuan"):
        return "vong"
    if ten == "P_yanjing":
        return "mat"
    if ten.startswith("liaoya") or ten.startswith("P_ya"):
        return "nanh"
    if "erduo" in ten:
        return "tai"
    if "jiaozhi" in ten:
        return "ngon"
    return "long"


def co_o(ten, z):
    _, imgs, _ = G.nap(ATT)
    im = imgs[ten]
    return int(round(im.width * z)), int(round(im.height * z))


_B = {}


def nguon(ten, z):
    w, h = co_o(ten, z)
    return np.asarray(G.part_goc(by()[ten]).resize((w, h), Image.LANCZOS)).astype(int)


def bong(ten, z):
    """hình bóng KÍN của part trong khung ảnh vùng × z (làm trơn nhẹ trên ảnh đã đệm viền)."""
    k = (ten, round(z, 3))
    if k not in _B:
        al = nguon(ten, z)[..., 3]
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
    h, w = m.shape
    return max(1.5, min(NET * z, 0.14 * min(w, h)))


def loi(m, k):
    """phần lõi của hình: điểm cách mép hơn k lần bề dày lớn nhất."""
    d = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    return d > k * d.max()


def mong_goc(src, z):
    """vùng MÓNG trong ảnh part gốc: ngưỡng Otsu trên độ sáng bên trong hình (bỏ dải viền mực), lấy khối sẫm lớn nhất."""
    al = (src[..., 3] > 100).astype(np.uint8)
    trong = cv2.erode(al, el(2.2 * z)).astype(bool)
    g = cv2.GaussianBlur(src[..., :3].mean(axis=2).astype(np.float32), (0, 0), 0.8 * z)
    if trong.sum() < 20:
        return np.zeros(al.shape, bool)
    v = np.clip(g[trong], 0, 255).astype(np.uint8)
    thr, _ = cv2.threshold(v.reshape(-1, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    toi = (g < thr) & trong
    toi = cv2.morphologyEx(toi.astype(np.uint8), cv2.MORPH_OPEN, el(1.2 * z))
    toi = cv2.dilate(toi, el(2.2 * z)) & al
    toi = cv2.morphologyEx(toi, cv2.MORPH_CLOSE, el(2.0 * z))
    n, lab, st, _ = cv2.connectedComponentsWithStats(toi, 8)
    if n > 2:
        toi = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    return toi.astype(bool)


def tg_vao_o(ten, w, h):
    """ma trận afin thế giới (dáng gốc) → px ô của part (bình phương tối thiểu trên lưới)."""
    a = by()[ten]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    M, *_ = np.linalg.lstsq(np.c_[V, np.ones(len(V))], U, rcond=None)
    return M


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    m = bong(ten, z)
    h, w = m.shape
    v = vai(ten)
    im = np.full((h, w, 3), 255, np.uint8)
    nt = net(m, z)
    trong = cv2.erode(m.astype(np.uint8), el(nt)).astype(bool)

    def ranh(mm):
        im[cv2.morphologyEx(mm.astype(np.uint8), cv2.MORPH_GRADIENT, el(0.5 * nt)).astype(bool) & trong] = INK

    if v == "may":
        im[m] = PAL["may"]
        im[loi(m, 0.5) & trong] = PAL["may_loi"]
    elif v == "chom":
        im[m] = PAL["chom"]
        im[loi(m, 0.45) & trong] = PAL["chom_loi"]
    elif v == "may_mat":
        im[m] = PAL["may_mat"]
    elif v == "tai":
        im[m] = PAL["tai"]
        c = loi(m, 0.34)
        im[c] = PAL["tai_trong"]
        ranh(c)
    elif v == "mat":
        im[m] = PAL["mi"]
        c = loi(m, 0.30)
        im[c] = PAL["mat"]
    elif v == "ngon":
        im[m] = PAL["ban_chan"]
        mg = mong_goc(nguon(ten, z), z) & m
        im[mg] = PAL["mong"]
        ranh(mg)
    elif ten == "P_zui":                                              # hàm dưới: lòng miệng đỏ sẫm ở đúng chỗ của họ
        im[m] = PAL["long"]
        s = nguon(ten, z)
        mg = (s[..., 3] > 100) & (s[..., 0] - s[..., 2] > 45) & (s[..., 0] > 110)
        mg = cv2.morphologyEx(mg.astype(np.uint8), cv2.MORPH_OPEN, el(1.5 * z))
        mg = cv2.morphologyEx(mg, cv2.MORPH_CLOSE, el(2.0 * z)).astype(bool) & m
        im[mg] = PAL["mieng"]
        ranh(mg)
    elif ten == "P_tou":                                              # đầu trên: mảng đỏ ở đúng chỗ con mắt rời sẽ dán lên
        im[m] = PAL["long"]
        me = bong("P_yanjing", z)                                    # hình bóng con mắt rời, đưa sang khung của đầu (cùng cứng trên một xương)
        Ah = np.c_[tg_vao_o(ten, w, h), [0, 0, 1]].T                  # thế giới → ô đầu (3 × 3)
        Ae = np.c_[tg_vao_o("P_yanjing", me.shape[1], me.shape[0]), [0, 0, 1]].T
        T = Ah @ np.linalg.inv(Ae)
        mm = cv2.warpAffine(me.astype(np.uint8), T[:2].astype(np.float32), (w, h), flags=cv2.INTER_NEAREST).astype(bool)
        mm = cv2.dilate(mm.astype(np.uint8), el(1.2 * z)).astype(bool) & m
        im[mm] = PAL["may_mat"]
    else:
        im[m] = PAL[v]
    im[m & ~trong] = INK
    im[~m] = 255
    return im, m


def xep(ds, z, le=26):
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
    _chia_may()
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
    for f in os.listdir(MAU) if os.path.isdir(MAU) else []:
        if re.match(r"^part_\w+\.json$", f):
            for k, v in json.load(open(os.path.join(MAU, f), encoding="utf-8")).items():
                out[k] = v["z"]
    for ds in NHOM.values():
        for t in ds:
            out[t] = Z_LIEN
    out["P_biyan"] = 4.0
    return out


def cat_part(to, ep=False):
    """cắt tờ N_<tờ>: mỗi part lấy đúng Ô của nó, tách nền trắng → manh/part/<vùng>.png; đo IoU với hình bóng hướng dẫn; chỉ ghi đè khi
    bản mới khít hơn (ep: ghi đè). Dọn bằng mã (không vẽ): cắt sát hình bóng nới vài px; kẻ nét mực dọc phía trong mép lưới của họ."""
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
        cell = tt.rgba[y:y + h, x:x + w].copy()
        lab = tt.lab[y:y + h, x:x + w]
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[g].ravel().tolist()) - {0}:
            if i in ids:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & g).sum() / max(1, (a | g).sum())
        cu = SO.get(ten, [0, ""])
        if not ep and cu[1] and cu[0] >= iou:
            print(f"  {ten}: IoU {iou:.2f}, giữ bản cũ (IoU {cu[0]:.2f})")
            continue
        sat = cv2.dilate(g.astype(np.uint8), el(0.75 * z)).astype(bool)
        cell[..., 3][~sat] = 0
        at = by()[ten]
        hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
        hm = np.zeros(a.shape, np.uint8)
        cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
        dai = hm.astype(bool) & ~cv2.erode(hm, el(0.9 * z), borderValue=0).astype(bool)
        cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), os.path.basename(path)]
        Image.fromarray(cell, "RGBA").save(os.path.join(ra, ten + ".png"))
        if iou < 0.9:
            kem.append(f"{ten} {iou:.2f}")
        print(f"  {ten}: {cell.shape[1]} x {cell.shape[0]} (x{z}), IoU {iou:.2f}")
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)
    print("  IoU < 0,9:", ", ".join(kem) if kem else "không có")


def so_part(chi=None):
    cells = []
    for f in sorted(os.listdir(MAU)):
        mt = re.match(r"^part_(\w+)\.json$", f)
        if not mt or (chi and mt.group(1) not in chi):
            continue
        to = mt.group(1)
        Kh = json.load(open(os.path.join(MAU, f), encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for ten, v in Kh.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm):
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


# ================================================================ LIỀN
def bong_tg(a, T, mat_na=None, tron=3.0, S2=2):
    """hình bóng kín của một part đặt theo toạ độ thế giới dáng gốc qua phép T (thế giới → px tờ), phóng S2. mat_na: mặt nạ riêng
    (cỡ ảnh vùng) thay cho cả hình (vd. vùng móng)."""
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3] > 90 if mat_na is None else mat_na
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    if mat_na is None:
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def to_lien():
    """tờ hướng dẫn liền → mau/lien_<tờ>.png + .json (px mỗi đơn vị rig, gốc toạ độ từng nhóm)."""
    B = by()
    S2 = 2
    os.makedirs(MAU, exist_ok=True)
    for to, nhom in TO_LIEN.items():
        hop = []
        for n in nhom:
            P = np.concatenate([np.array(B[t]["xy"], float).reshape(-1, 2) for t in NHOM[n]])
            hop.append((P[:, 0].min() - 8, P[:, 1].min() - 8, P[:, 0].max() + 8, P[:, 1].max() + 8))
        cao = max(h[3] - h[1] for h in hop)
        kc = 60
        ti = min((H - 70) / cao, (W - 60 - kc * (len(hop) - 1)) / sum(h[2] - h[0] for h in hop))
        tong = sum((h[2] - h[0]) * ti for h in hop) + kc * (len(hop) - 1)
        x = (W - tong) / 2
        day = (H + cao * ti) / 2
        goc = {}
        can = np.full((H * S2, W * S2, 3), 255, np.uint8)
        for n, h in zip(nhom, hop):
            ox, oy = x - h[0] * ti, day + h[1] * ti                    # px = (ox + X·ti, oy − Y·ti)
            goc[n] = (ox, oy)
            x += (h[2] - h[0]) * ti + kc
            T2 = lambda p_, ox=ox, oy=oy: np.stack([ox + np.asarray(p_, float)[..., 0] * ti, oy - np.asarray(p_, float)[..., 1] * ti], -1)
            m = np.zeros((H * S2, W * S2), bool)
            ban = np.zeros_like(m)
            mong = np.zeros_like(m)
            for t in NHOM[n]:
                mt = bong_tg(B[t], T2)
                m |= mt
                if t in BAN:
                    ban |= mt
            m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(5)).astype(bool)
            can[m] = PAL["long"]
            can[ban & m] = PAL["ban_chan"]
            can[cv2.morphologyEx(ban.astype(np.uint8), cv2.MORPH_GRADIENT, el(2)).astype(bool) & m] = INK
            can[mong & m] = PAL["mong"]
            can[cv2.morphologyEx(mong.astype(np.uint8), cv2.MORPH_GRADIENT, el(2)).astype(bool) & m] = INK
            can[m & ~cv2.erode(m.astype(np.uint8), el(6)).astype(bool)] = INK
        Image.fromarray(can).resize((W, H), Image.LANCZOS).save(os.path.join(MAU, f"lien_{to}.png"))
        json.dump({"ti": ti, "goc": goc, "nhom": nhom}, open(os.path.join(MAU, f"lien_{to}.json"), "w"), indent=1)
        print(os.path.join(MAU, f"lien_{to}.png"), f"{ti:.3f} px mỗi đơn vị rig;", {n: [round(v) for v in goc[n]] for n in nhom})


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


def cat_lien(chi=None):
    """nướng tờ liền (tai_ve/N_LA*.png, N_LB*.png) vào khung từng mảnh → manh/part/<vùng>.png."""
    from quai import anh
    B = by()
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    for to in TO_LIEN:
        if chi and to not in chi:
            continue
        path = anh.to_moi_nhat(TAI, f"N_{to}")
        if not path:
            print(to, "chưa có ảnh")
            continue
        L = json.load(open(os.path.join(MAU, f"lien_{to}.json"), encoding="utf-8"))
        im = Image.open(path).convert("RGB")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
            path = os.path.join(MAU, f"_N_{to}_doi_co.png")
            im.save(path)
        tt = anh.doc_to(path, dien_tich_min=600, gop_px=10)
        rgba = tt.rgba.astype(np.float32)
        rgba[..., :3] *= rgba[..., 3:4] / 255.0
        ti = L["ti"]
        print(os.path.basename(path))
        for n in L["nhom"]:
            ox, oy = L["goc"][n]
            for ten in NHOM[n]:
                a = B[ten]
                w, h = co_o(ten, Z_LIEN)
                Wd = _the_gioi_o(a, w, h)
                ok = ~np.isnan(Wd[..., 0])
                mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
                my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
                cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
                al = cell[..., 3:4]
                cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
                sil = cv2.dilate(bong(ten, Z_LIEN).astype(np.uint8), el(0.7 * Z_LIEN)).astype(np.float32)
                sil = np.clip(cv2.GaussianBlur(sil, (0, 0), 0.45 * Z_LIEN) * 2.0 - 0.5, 0.0, 1.0)
                cell[..., 3] *= sil
                out = np.clip(cell, 0, 255).astype(np.uint8)
                Image.fromarray(out, "RGBA").save(os.path.join(ra, ten + ".png"))
                phu = float((out[..., 3] > 127).sum()) / max(1, int(bong(ten, Z_LIEN).sum()))
                print(f"  {ten}: {w} x {h}, phủ {phu:.2f} hình bóng của part")


def biyan():
    """mắt nhắm (slot P_biyan của họ: hai nét mí chữ V nằm ngang): vẽ lại bằng nét mực của mình trong đúng khung ảnh vùng × 4."""
    _, imgs, _ = G.nap(ATT)
    z = 4.0
    src = imgs["P_biyan"].convert("RGBA")
    w, h = int(round(src.width * z)), int(round(src.height * z))
    al = np.asarray(src.resize((w, h), Image.LANCZOS))[..., 3] > 90
    al = cv2.morphologyEx(al.astype(np.uint8), cv2.MORPH_CLOSE, el(1.0 * z))
    al = cv2.GaussianBlur(al * 255, (0, 0), 0.6 * z) > 127
    out = np.zeros((h, w, 4), np.uint8)
    out[al] = INK + (255,)
    os.makedirs(os.path.join(MANH, "part"), exist_ok=True)
    Image.fromarray(out, "RGBA").save(os.path.join(MANH, "part", "P_biyan.png"))
    print("P_biyan", w, h)


def mat():
    """con mắt (P_yanjing) vẽ bằng mã trong đúng hình bóng của họ: mí sẫm, mống hổ phách, con ngươi khe dọc, một chấm sáng nhỏ
    (Codex vẽ ô này thành một mảnh kem trơn, bỏ mống mắt)."""
    z = zs().get("P_yanjing", 3.7)
    m = bong("P_yanjing", z)
    h, w = m.shape
    S = 4
    M4 = cv2.resize(m.astype(np.uint8), (w * S, h * S), interpolation=cv2.INTER_LINEAR) > 0
    nt = max(2.0, 0.55 * NET * z) * S
    trong = cv2.erode(M4.astype(np.uint8), el(nt)).astype(bool)
    im = np.zeros((h * S, w * S, 4), np.uint8)
    im[M4] = INK + (255,)
    im[trong] = PAL["mat"] + (255,)
    d = cv2.distanceTransform(trong.astype(np.uint8), cv2.DIST_L2, 5)
    cy, cx = np.unravel_index(d.argmax(), d.shape)
    r = float(d.max())
    cv2.ellipse(im, (int(cx), int(cy)), (max(2, int(r * 0.34)), int(r * 1.25)), 0, 0, 360, INK + (255,), -1, cv2.LINE_AA)
    cv2.circle(im, (int(cx - r * 0.75), int(cy - r * 0.35)), max(2, int(r * 0.26)), (255, 250, 236, 255), -1, cv2.LINE_AA)
    im[~M4] = 0
    out = Image.fromarray(im, "RGBA").resize((w, h), Image.LANCZOS)
    out.save(os.path.join(MANH, "part", "P_yanjing.png"))
    print("P_yanjing", w, h)


def main(a):
    lenh = a[0] if a else ""
    if lenh == "nhom_part":
        nhom_part(a[1:] or None)
    elif lenh == "cat_part":
        _chia_may()
        for to in (a[1].split(",") if len(a) > 1 and a[1] != "het" else list(TO)):
            cat_part(to, ep=len(a) > 2)
    elif lenh == "so_part":
        so_part(a[1:] or None)
    elif lenh == "to_lien":
        to_lien()
    elif lenh == "cat_lien":
        cat_lien(a[1:] or None)
    elif lenh == "biyan":
        biyan()
    elif lenh == "mat":
        mat()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
