# -*- coding: utf-8 -*-
"""Sâu đất khổng lồ (sau_dat, tướng 7 đảo Thổ, rig monster_3643, concept A đã duyệt 2026-11-17): MẢNH theo cách tách của rig gốc
(skill pokiclash-spine-rig mục 00: "vẽ mảnh ĐÚNG KHUNG từng part"; "các khúc NỐI NHAU gen LIỀN một ảnh rồi cắt"). Bản bố cục GPT
(L2_bocuc) không theo được bố cục rig (chép lại concept, IoU 0,677) nên bỏ bước bố cục; ba loại mảnh:

- KHUNG PART (mỗi part một ô đúng khung ảnh vùng × z, hình bóng kín tô phẳng theo thiết kế của mình, GPT vẽ lại giữ hình bóng):
    R  = mười râu roi `A_chuxu_*` (7 ảnh vùng; slot 08/09 dùng ảnh 05, slot 010 dùng ảnh 01): roi nâu sẫm, ngạnh hổ phách ở ngọn
    T  = mười bốn tua `P_chuxu_01..11` + `P_hounao_01..03`: tua hồng đất có vòng như giun con
    S1 = năm phiến sau lưng `P_shitou_05..09`: đá phân tầng (vằn kem / son / gỉ)
    S2 = bốn tảng trước `P_shitou_01..04` (đất nâu sẫm, khe hổ phách) + ba cụm đế `P_dizuo_01..03` (gò cát, đá, hổ phách)
         + hai mảnh đá dẹt sát đất `P_xiazhi_01/02`
- LIỀN: cổ + thân giun `P_bozi_01..10` (gồm hai vòng giáp sau đầu `P_bozi_01/04`): một hình bóng hợp ở dáng gốc, vòng đốt vẽ ngang thân,
  GPT vẽ lại → nướng vào khung từng part qua lưới của nó.
- MẢNH CỨNG (đầu, hàm, lòng miệng, mắt, ngà, mào, gờ mày): cắt "đúng chỗ" từ concept (sau_dat_cung.py).

    sau_dat_part.py nhom_part [tờ...]      tờ hướng dẫn mau/part_<tờ>.png + .json
    sau_dat_part.py prompt [tờ...]         file prompt gui_gpt/sau_dat_1/luot_3_<tờ>.txt
    sau_dat_part.py cat_part <tờ|het> [ep] cắt tai_ve/N_<tờ>*.png → manh/part/<vùng>.png, in IoU
    sau_dat_part.py so_part [tờ...]        tờ so mau/so_part.png (đỏ = thiếu, xanh lá = thừa)
    sau_dat_part.py to_lien                tờ liền mau/lien_L.png + .json; prompt luot_3_L.txt
    sau_dat_part.py cat_lien               nướng tai_ve/N_L*.png vào khung từng part thân
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
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
import sau_dat  # noqa: E402,F401
import tho5  # noqa: E402
from quai.soi import _tris  # noqa: E402

G = tho5.dat("sau_dat")
W, H = 1536, 1024
INK = (43, 33, 24)
ATT = "att_goc.json"
MANH = os.path.join(G.BASE, "manh")
MAU, TAI = G.MAU, G.TAI
GUI = os.path.join(HERE, "gui_gpt", "sau_dat_1")
CONCEPT = os.path.join(TAI, "L1_duyet.png")
NET = 2.9                                    # bề dày nét mực đích (px ảnh vùng, 0,5 px / đơn vị) ≈ 5,8 đơn vị rig
PAL = dict(than=(211, 168, 102), ranh=(156, 116, 68), bung=(234, 215, 174), giap=(201, 154, 87), giap_toi=(158, 116, 66),
           rau=(78, 55, 38), ngach=(239, 163, 48), kem=(234, 215, 174), oc=(201, 154, 87), gi=(168, 95, 58),
           tang=(90, 64, 48), tang_ben=(63, 45, 34), nut=(239, 163, 48), tua=(201, 139, 120), tua_ranh=(168, 110, 94),
           cat=(226, 196, 140), da=(201, 154, 87), da_toi=(158, 116, 66), ho_phach=(239, 163, 48))

RAU = ["A_chuxu_01", "A_chuxu_02", "A_chuxu_03", "A_chuxu_04", "A_chuxu_05", "A_chuxu_06", "A_chuxu_07"]
TUA = [f"P_chuxu_{i:02d}" for i in range(1, 12)] + ["P_hounao_01", "P_hounao_02", "P_hounao_03"]
PHIEN = [f"P_shitou_{i:02d}" for i in (5, 6, 7, 8, 9)]
TANG = [f"P_shitou_{i:02d}" for i in (1, 2, 3, 4)]
DE = ["P_dizuo_01", "P_dizuo_02", "P_dizuo_03", "P_xiazhi_01", "P_xiazhi_02"]
TO = {"R": RAU, "T": TUA, "S1": PHIEN, "S2": TANG + DE}
THAN = [f"P_bozi_{i:02d}" for i in range(1, 11)]
COT = ["bone6", "bone7", "bone8", "bone9", "bone10", "bone11", "bone16"]      # trục thân (gốc → đầu)
VONG = ("P_bozi_01", "P_bozi_04")                                               # hai vòng giáp sau đầu
BUNG = ("P_bozi_05", "P_bozi_06", "P_bozi_07")                                  # cột bụng kem
Z_LIEN = 2.0


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


_BY = {}


def by():
    """part theo tên ẢNH VÙNG (ảnh dùng chung cho nhiều slot thì lấy slot đầu)."""
    if not _BY:
        G._C.pop("att", None)
        _, _, atts = G.nap(ATT)
        for a in atts:
            _BY.setdefault(a["region"], a)
            _BY.setdefault("slot:" + a["slot"], a)
    return _BY


def xuong():
    D = json.load(open(os.path.join(G.scan(), ATT), encoding="utf-8"))
    return {b["name"]: b for b in D["bones"]}


def vai(ten):
    if ten in RAU:
        return "rau"
    if ten in TUA:
        return "tua"
    if ten in PHIEN:
        return "phien"
    if ten in TANG:
        return "tang"
    if ten.startswith("P_dizuo"):
        return "de"
    if ten.startswith("P_xiazhi"):
        return "manh_dat"
    return "than"


def co_o(ten, z):
    _, imgs, _ = G.nap(ATT)
    im = imgs[ten]
    return int(round(im.width * z)), int(round(im.height * z))


def nguon(ten, z):
    w, h = co_o(ten, z)
    return np.asarray(G.part_goc(by()[ten]).resize((w, h), Image.LANCZOS)).astype(int)


_B = {}


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
        if ten.startswith("P_xiazhi"):                                      # rễ chẻ nhánh của họ → phiến đá dẹt (mảnh cứng, đổi dáng tự do)
            ys_, xs_ = np.nonzero(m)
            hu = cv2.convexHull(np.c_[xs_, ys_].astype(np.int32))
            m2 = np.zeros(m.shape, np.uint8)
            cv2.fillPoly(m2, [hu], 1)
            m2 = cv2.erode(m2, el(0.10 * min(m.shape)))
            m = cv2.GaussianBlur(m2 * 255, (0, 0), 1.5 * z) > 127
        _B[k] = m
    return _B[k]


def net(m, z):
    h, w = m.shape
    return max(1.5, min(NET * z, 0.14 * min(w, h)))


def truc(m):
    """trục dài của hình (PCA): tâm, vectơ đơn vị dọc, vectơ đơn vị ngang."""
    ys, xs = np.nonzero(m)
    P = np.c_[xs, ys].astype(float)
    c = P.mean(0)
    _, _, Vt = np.linalg.svd(P - c, full_matrices=False)
    u = Vt[0]
    return c, u, np.array([-u[1], u[0]])


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    m = bong(ten, z)
    h, w = m.shape
    v = vai(ten)
    im = np.full((h, w, 3), 255, np.uint8)
    nt = net(m, z)
    trong = cv2.erode(m.astype(np.uint8), el(nt)).astype(bool)
    ys, xs = np.mgrid[0:h, 0:w]
    if v == "rau":                                                        # roi nâu sẫm; ngạnh hổ phách = lòng mũi thoi ở ĐẦU TRÊN
        im[m] = PAL["rau"]
        hang = np.nonzero(m.any(1))[0]
        bc = np.median(m.sum(1)[m.sum(1) > 0])                              # bề ngang thân roi
        y0 = hang[0]
        thoi = m & (ys < y0 + 3.2 * bc)
        thoi = cv2.erode(thoi.astype(np.uint8), el(0.55 * nt)).astype(bool) & trong
        im[thoi] = PAL["ngach"]
    elif v == "tua":
        im[m] = PAL["tua"]
    elif v == "phien":                                                      # vằn phân tầng vuông góc trục dài, mép vằn hơi gợn
        c, u, n_ = truc(m)
        d = (xs - c[0]) * u[0] + (ys - c[1]) * u[1]
        e = (xs - c[0]) * n_[0] + (ys - c[1]) * n_[1]
        bw = max(14.0, 0.11 * np.ptp(d[m]))
        k = np.floor((d + 0.25 * bw * np.sin(e / (0.9 * bw) + 1.3 * (hash(ten) % 7))) / bw).astype(int) % 4
        mau = np.array([PAL["kem"], PAL["oc"], PAL["gi"], PAL["oc"]], np.uint8)
        im[m] = mau[k[m]]
    elif v in ("tang", "manh_dat"):
        im[m] = PAL["tang"]
        if v == "tang":                                                     # một khe hổ phách gấp khúc dọc giữa
            c, u, n_ = truc(m)
            d = (xs - c[0]) * u[0] + (ys - c[1]) * u[1]
            L = 0.32 * np.ptp(d[m])
            pts = []
            for i, t in enumerate(np.linspace(-L, L, 6)):
                o = (0.09 if i % 2 else -0.09) * L
                p = c + u * t + n_ * o
                pts.append([int(p[0]), int(p[1])])
            khe = np.zeros((h, w), np.uint8)
            cv2.polylines(khe, [np.array(pts, np.int32)], False, 1, max(2, int(round(1.1 * z))))
            khe = khe.astype(bool) & cv2.erode(m.astype(np.uint8), el(2.5 * nt)).astype(bool)
            im[khe] = PAL["nut"]
    elif v == "de":
        im[m] = PAL["da"]
    else:
        im[m] = PAL["than"]
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
    os.makedirs(MAU, exist_ok=True)
    for to, ds in TO.items():
        if chi and to not in chi:
            continue
        z = 6.0
        while xep(ds, z) is None:
            z = round(z - 0.05, 2)
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
        print(f"{to} (x{z}, nét ~{NET * z:.0f} px): " + ", ".join(f"{k} {v['w']}x{v['h']}@{v['x'] + v['w'] // 2},{v['y'] + v['h'] // 2}"
                                                              for k, v in khung.items()))


# mô tả từng loại ô cho prompt
MO_TA = {
    "rau": ("a long thin WHIP FEELER, dark brown #4E3726, ending in a small flat AMBER diamond-shaped barb #EFA330 (the barb is the amber "
            "patch already shown in the cell; keep it at the same end, same size)"),
    "tua": ("a short curved fleshy TENDRIL like a little earthworm: dusty rose #C98B78 with 4 to 7 thin darker rings #A86E5E across it "
            "(rings run ACROSS the tube, evenly spaced), a rounded blunt tip"),
    "phien": ("a tall upturned SLAB of LAYERED SANDSTONE: keep the coloured strata bands of the cell (flat bands of cream #EAD7AE, ochre "
              "#C99A57 and rust #A85F3A, with slightly wavy borders between bands, NO ink line between bands), the tip may become a "
              "little jagged like broken rock but stays INSIDE the cell's silhouette"),
    "tang": ("an angular broken EARTH CHUNK, dark brown #5A4030 with one or two flat darker side faces #3F2D22 separated by thin ink lines, "
             "and the thin AMBER crack #EFA330 already shown in the cell"),
    "de": ("a low pile of SANDSTONE ROCKS on a little sand mound: a few angular rocks in #C99A57 with darker side faces #9E7442, flat sand "
           "#E2C48C between them at the bottom, and one or two small flat AMBER crystals #EFA330"),
    "manh_dat": "a LOW FLAT dark-brown ROCK SHARD lying on the ground, #5A4030 with one darker side face #3F2D22",
}


def prompt(chi=None):
    for to, ds in TO.items():
        if chi and to not in chi:
            continue
        gd = os.path.join(MAU, f"part_{to}.png")
        K = json.load(open(os.path.join(MAU, f"part_{to}.json"), encoding="utf-8"))
        out = os.path.join(TAI, f"N_{to}.png")
        loai = sorted({vai(t) for t in ds})
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(gd)}: the GUIDE SHEET: {len(ds)} separate pieces of our character, each a closed silhouette roughly coloured by "
             "a machine (flat colours, a plain dark outline). It shows the EXACT shape, size and place of every piece.",
             f"image 2 = {Wp(CONCEPT)}: our APPROVED character (a colossal sandworm, hand-drawn: wobbly dark-brown ink line, crayon "
             "hatching, flat colours): copy its drawing style, colours and materials.", "",
             f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 cleanly in the hand-drawn style of image 2. KEEP EVERY SILHOUETTE EXACTLY: each piece keeps the same "
             "outline, the same size, the same angle and the same place on the sheet as in image 1 (if the new picture were laid over image "
             "1, every outline must coincide). Do not move, resize, rotate, merge, split, add or remove any piece. Each piece is ONE closed "
             "shape with a wobbly dark-brown ink outline (#2B2118, about 7 px at this size) running exactly along its edge, every area one "
             "flat colour with visible coloured-pencil / wax-crayon hatching. Keep the colours and patches already shown in image 1 where "
             "they are. No shading, no highlights, no gradients, no glow, no shadows, no sparkles. Keep the white gaps between pieces; no "
             "labels, no frame, pure white background (#FFFFFF).", "", "WHAT EACH PIECE IS:"]
        for lv in loai:
            n = sum(vai(x) == lv for x in ds)
            t.append(f"- {n} piece(s): {MO_TA[lv]}.")
        if to == "R":
            t.append("- The feelers are drawn STRAIGHT and UPRIGHT on this sheet on purpose (they will be bent by the animation): keep them "
                     "straight, the barb at the same end as in image 1.")
        if to == "T":
            t.append("- The tendrils keep exactly the curve of their silhouettes.")
        t += ["", "CANVAS: landscape 1536x1024, pure-white background."]
        p = os.path.join(GUI, f"luot_3_{to}.txt")
        ghi(p, t)
        print(p, len(K), "ô")


def zs():
    out = {}
    for f in os.listdir(MAU) if os.path.isdir(MAU) else []:
        if re.match(r"^part_\w+\.json$", f):
            for k, v in json.load(open(os.path.join(MAU, f), encoding="utf-8")).items():
                out[k] = v["z"]
    for t in THAN:
        out[t] = Z_LIEN
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
        hut = g & ~a & ~cv2.erode(g.astype(np.uint8), el(1.2 * z)).astype(bool)    # GPT vẽ hụt sát mép: lấy màu tờ hướng dẫn
        cell[hut, :3] = gd[y:y + h, x:x + w][hut]
        cell[hut, 3] = 255
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


# ================================================================ LIỀN (cổ + thân giun)
def bong_tg(a, T, S2=2, tron=3.0):
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3] > 90
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def to_lien():
    """tờ hướng dẫn liền cổ + thân → mau/lien_L.png + .json (px mỗi đơn vị rig, gốc toạ độ) + prompt luot_3_L.txt.
    Tô: sườn vàng cát, cột bụng kem, hai vòng giáp sau đầu sa thạch; vòng đốt là nét ngang thân theo khoảng cách dọc trục xương thân."""
    B = by()
    X = xuong()
    S2 = 2
    P = np.concatenate([np.array(B["slot:" + t]["xy"], float).reshape(-1, 2) for t in THAN])
    hop = (P[:, 0].min() - 10, P[:, 1].min() - 10, P[:, 0].max() + 10, P[:, 1].max() + 10)
    ti = min((H - 80) / (hop[3] - hop[1]), (W - 80) / (hop[2] - hop[0]))
    ox = W / 2 - (hop[0] + hop[2]) / 2 * ti
    oy = H / 2 + (hop[1] + hop[3]) / 2 * ti
    T2 = lambda p_: np.stack([ox + np.asarray(p_, float)[..., 0] * ti, oy - np.asarray(p_, float)[..., 1] * ti], -1)
    m = np.zeros((H * S2, W * S2), bool)
    vung = {}
    for t in THAN:
        mt = bong_tg(B["slot:" + t], T2)
        vung[t] = mt
        m |= mt
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(14))
    m = cv2.GaussianBlur(m * 255, (0, 0), 4) > 127
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    can[m] = PAL["than"]
    bung = np.zeros_like(m)
    for t in BUNG:
        bung |= vung[t]
    bung = cv2.erode(bung.astype(np.uint8), el(10)).astype(bool) & m
    can[bung] = PAL["bung"]
    vg = np.zeros_like(m)
    for t in VONG:
        vg |= vung[t]
    vg &= m & ~bung
    can[vg] = PAL["giap"]
    # vòng đốt: KHÔNG vẽ bằng mã (thử: vạch thành hình nêm ở chỗ thân cong); GPT tự vẽ vòng ngang thân như concept
    can[m & ~cv2.erode(m.astype(np.uint8), el(6)).astype(bool)] = INK
    Image.fromarray(can).resize((W, H), Image.LANCZOS).save(os.path.join(MAU, "lien_L.png"))
    json.dump({"ti": ti, "goc": [ox, oy]}, open(os.path.join(MAU, "lien_L.json"), "w"), indent=1)
    print(os.path.join(MAU, "lien_L.png"), f"{ti:.3f} px mỗi đơn vị rig")
    out = os.path.join(TAI, "N_L.png")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(os.path.join(MAU, 'lien_L.png'))}: the GUIDE: the NECK and BODY of our giant sandworm as ONE closed silhouette, "
         "roughly coloured by a machine: sand-ochre sides, a cream belly column down the middle and the sandstone armour collar at the top "
         "(behind where the head will sit; the head itself is NOT on this sheet). The ring segments are not drawn yet.",
         f"image 2 = {Wp(CONCEPT)}: our APPROVED character (hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours): copy its "
         "drawing style, colours and the look of its ring-segmented body.", "",
         f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_L_2.png, N_L_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: redraw image 1 cleanly in the hand-drawn style of image 2, KEEPING ITS SILHOUETTE EXACTLY (same outline, same size, same "
         "place: laid over image 1, the outline must coincide). It is ONE continuous surface: the dark-brown ink outline (#2B2118, about 7 "
         "px) runs ONLY round the outside; inside, draw the RING SEGMENTS of the worm like image 2: thin groove lines (about 4 px) running ACROSS "
         "the body, perpendicular to its long axis, one every 60 to 75 px, following the curve of the body (they fan out a little on the "
         "outside of the bends); in the collar at the top, two broad armour rings. Colours: sides sand-ochre #D3A866 with grooves #9C7444, belly column cream sand #EAD7AE, "
         "the armour collar at the top sandstone #C99A57 with a thin ink line at each ring edge. Every area one flat colour with visible "
         "coloured-pencil / wax-crayon hatching. No shading, no highlights, no gradients, no glow, no shadows. Nothing else on the sheet: no "
         "head, no feelers, no tendrils, no labels, pure white background (#FFFFFF).", "",
         "CANVAS: landscape 1536x1024, pure-white background."]
    p = os.path.join(GUI, "luot_3_L.txt")
    ghi(p, t)
    print(p)


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
    """nướng tờ liền (tai_ve/N_L*.png) vào khung từng part thân → manh/part/<vùng>.png."""
    from quai import anh
    B = by()
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    path = anh.to_moi_nhat(TAI, "N_L")
    if not path:
        print("N_L chưa có ảnh")
        return
    L = json.load(open(os.path.join(MAU, "lien_L.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, "_N_L_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=600, gop_px=10)
    rgba = tt.rgba.astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:4] / 255.0
    ti = L["ti"]
    ox, oy = L["goc"]
    print(os.path.basename(path))
    for t in THAN:
        a = B["slot:" + t]
        ten = a["region"]
        w, h = co_o(ten, Z_LIEN)
        Wd = _the_gioi_o(a, w, h)
        ok = ~np.isnan(Wd[..., 0])
        mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
        my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
        cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        al = cell[..., 3:4]
        cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
        # KHÔNG cắt theo hình bóng part gốc: các part cổ của họ có mép xẻ răng cưa (diềm), cắt theo đó thì lúc các khúc trượt lên nhau
        # (vươn cao) lộ khe răng cưa (soi runtime 2026-11-17). Mỗi part phủ đủ ảnh thân liền trong phạm vi lưới của nó (chồng mép rộng).
        out = np.clip(cell, 0, 255).astype(np.uint8)
        Image.fromarray(out, "RGBA").save(os.path.join(ra, ten + ".png"))
        phu = float((out[..., 3] > 127).sum()) / max(1, int(bong(ten, Z_LIEN).sum()))
        print(f"  {ten}: {w} x {h}, phủ {phu:.2f} hình bóng của part")


def main(a):
    lenh = a[0] if a else ""
    if lenh == "nhom_part":
        nhom_part(a[1:] or None)
    elif lenh == "prompt":
        prompt(a[1:] or None)
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
