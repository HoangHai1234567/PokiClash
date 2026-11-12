# -*- coding: utf-8 -*-
"""Hươu gỗ cổ dài (mã làm việc huou_go; con gốc của rig: monster_3504, game tham khảo). Tướng thứ 4 đảo Mộc.

Người dùng 2026-11-12: "concept sinh vật lai hươu và hươu cao cổ, thân gỗ, lông là lá cây, kết hợp pha lê, đá...; điểm khác với con
gốc con này bạn làm thêm mồm cho tôi há/đóng được". Con gốc nhìn sang PHẢI (đầu quay ba phần tư, lộ một mắt): không lật.
Rig gốc: 107 xương, 34 mảnh lưới có trọng số (đầu, pha lê là mảnh cứng một xương), 12 clip.

    huou_go.py part_goc          ảnh từng part của con gốc cắt theo lưới → <SXS>/scan/monster_3504/parts/ (chỉ để xem, nội bộ)
    huou_go.py bo_cuc [hướng]    sơ đồ bố cục phẳng 1536 × 1024 (he | thu) → inbox/huou_go_2/mau/bo_cuc_<hướng>.png
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "huou_go"
K = int(os.environ.get("HG_DANG", "2"))        # dạng: 2 = hươu cổ dài (monster_3504, mặc định), 1 = khúc gỗ non (monster_3304)
MON = {1: "monster_3304", 2: "monster_3504"}[K]
BASE = os.path.join(HERE, "inbox", f"{CODE}_{K}")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
W, H = 1536, 1024
INK = (43, 33, 24)
ATT = "att_goc.json"
S2 = 2
# bảng màu ĐỀ XUẤT của Claude (người dùng dặn: thân gỗ, lông là lá cây, pha lê, đá), chờ duyệt concept
PALS = {
    "he": dict(go=(205, 166, 112),               # gỗ thân (gỗ sồi sáng) #CDA670
               dom=(142, 98, 60),                # mảng vỏ cây kiểu đốm hươu cao cổ #8E623C
               sung=(112, 76, 48),               # gạc: cành cây sẫm #704C30
               la=(86, 150, 70),                 # lá (bờm, đuôi, túm chân) #569646
               la_nhat=(146, 196, 88),           # lá non (tai, lá nhỏ) #92C458
               reu=(98, 156, 72),                # rêu ở chân cụm pha lê
               pha_le=(242, 180, 62),            # pha lê hổ phách (nhựa cây) #F2B43E
               pha_le_dam=(214, 134, 32),        # mặt cắt đậm #D68620
               da=(140, 136, 124)),              # đá (móng, đế cụm pha lê) #8C887C
    "thu": dict(go=(226, 214, 186),              # gỗ bạch dương #E2D6BA
                dom=(124, 92, 64),               # mảng vỏ sẫm #7C5C40
                sung=(124, 92, 64),
                la=(214, 108, 50),               # lá phong đỏ cam #D66C32
                la_nhat=(240, 172, 62),          # lá vàng #F0AC3E
                reu=(98, 156, 72),
                pha_le=(64, 206, 150),           # pha lê lục bảo #40CE96
                pha_le_dam=(30, 150, 110),       # #1E966E
                da=(140, 136, 124)),
}


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


def rig_goc():
    return os.path.join(sxs(), "web", "assets", "Monster", MON)


def scan():
    return os.path.join(sxs(), "scan", MON)


def loai1(ten):
    """dạng 1 (monster_3304): khúc gỗ non."""
    if ten in ("JiaoR_01", "JiaoL_01"):
        return "sung"                            # hai cành gạc
    if ten.startswith("Jiao"):
        return "la_nhat" if ten in ("JiaoL_03", "JiaoR_02") else "la"      # lá trên gạc
    if ten.startswith("Weiba"):
        return "la_nhat" if ten == "Weiba_02" else "la"                  # ba lá đuôi
    return "go"                                  # P_tou (khúc gỗ), P_shenti, chân, hai ụ mắt


def loai(ten):
    """nhóm thiết kế của một part (tên hình của con gốc)."""
    if K == 1:
        return loai1(ten)
    if "jingshi" in ten:
        return "pha_le"
    if "jiao" in ten:
        return "sung"
    if ten.endswith("_er") or ten in ("P_weiba", "P_weiba2"):
        return "la_nhat"
    if ten in ("P_toufa", "P_weiba3", "P_y_houmaofa"):
        return "la"
    if "maofa" in ten:
        return "reu"
    return "go"                                  # P_tou, P_bozi, P_shenti, chân, P_weiba1 (cán đuôi)


MONG = (("P_tuiL_H_2", "P_tuiR_H_2", "P_tuiL_Q_2", "P_tuiR_Q_2") if K == 1 else
        ("P_y_qianzhi", "P_z_qianzhi1", "P_y_houzhi2", "P_z_houzhi2"))      # khúc chân dưới: phần đáy là móng đá


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


_C = {}


def nap():
    if not _C:
        atlas, imgs = to_manh.nap(rig_goc(), MON)
        D = json.load(open(os.path.join(scan(), ATT), encoding="utf-8"))
        atts = sorted([a for a in D["atts"] if a.get("region") in imgs and a["cur"]], key=lambda a: a["order"])
        _C.update(atlas=atlas, imgs=imgs, atts=atts, bones=D["bones"])
    return _C["atlas"], _C["imgs"], _C["atts"]


def luoi(a):
    _, imgs, _ = nap()
    im = imgs[a["region"]]
    return np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3)


def part_goc(a):
    """ảnh một part của con gốc cắt đúng theo lưới của nó."""
    _, imgs, _ = nap()
    im = imgs[a["region"]].convert("RGBA")
    uv, tr = luoi(a)
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    d = ImageDraw.Draw(m)
    for t in tr:
        d.polygon([tuple(uv[i] * 4) for i in t], fill=255, outline=255)
    A = np.asarray(im).copy()
    A[..., 3] = (A[..., 3].astype(np.float32) * np.asarray(m.resize(im.size, Image.LANCZOS)) / 255.0).astype(np.uint8)
    return Image.fromarray(A, "RGBA")


def khung_T():
    """(hàm đổi toạ độ rig → pixel khung concept, tỉ lệ)."""
    _, _, atts = nap()
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    sc = min(1180 / (x1 - x0), (760 if K == 1 else 900) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * sc
    oy = (H + (y1 - y0) * sc) / 2 + y0 * sc
    return (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * sc, oy - np.asarray(p, float)[..., 1] * sc], -1)), sc


def bong_khung(a, T, tron=5.0):
    """hình bóng KÍN của một part đặt đúng chỗ dáng gốc trên khung concept (phóng S2), làm trơn: chỉ còn khối."""
    src = part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4))
    m = cv2.GaussianBlur(m * 255, (0, 0), tron) > 127
    return m


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def dom(m, seed, n, r0, r1):
    """vài mảng vỏ cây góc cạnh (kiểu đốm hươu cao cổ) rải trong một mảnh, cách mép."""
    rng = np.random.default_rng(seed)
    trong = cv2.erode(m.astype(np.uint8), el(12)).astype(bool)
    ys, xs = np.nonzero(trong)
    out = np.zeros(m.shape, np.uint8)
    if not len(ys):
        return out.astype(bool)
    tam = []
    for _ in range(400):
        if len(tam) >= n:
            break
        i = rng.integers(len(ys))
        c = np.array([xs[i], ys[i]], float)
        r = rng.uniform(r0, r1)
        if all(np.hypot(*(c - c2)) > (r + r2) * 1.25 for c2, r2 in tam):
            tam.append((c, r))
    for c, r in tam:
        k = rng.integers(5, 7)
        g = np.sort(rng.uniform(0, 2 * np.pi, k))
        pts = [c + r * rng.uniform(0.75, 1.1) * np.array([np.cos(t), np.sin(t)]) for t in g]
        cv2.fillPoly(out, [np.array(pts, np.int32)], 1, cv2.LINE_AA)
    return out.astype(bool) & trong


# đầu của mình trên khung concept (px, chưa nhân S2): sọ tròn ở chỗ đầu con gốc, mõm dài hơn chĩa xuống phải
SO = ((905, 338), (92, 88))                      # tâm, bán kính sọ
MOM = [(868, 392), (930, 372), (1000, 404), (1034, 452), (1026, 500), (984, 520), (930, 512), (880, 470)]    # mõm + hàm dưới
DUONG_MIENG = [(1030, 470), (990, 478), (950, 474), (916, 458)]      # khe miệng (ngậm): từ chóp mõm lùi về khoé
MAT = (892, 358)                                 # tâm cung mắt nhắm (một mắt lộ như con gốc)
MUI = (1012, 440)


def dau_moi():
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.ellipse(m, (SO[0][0] * S2, SO[0][1] * S2), (SO[1][0] * S2, SO[1][1] * S2), 0, 0, 360, 1, -1)
    cv2.fillPoly(m, [np.array(MOM, np.int32) * S2], 1)
    m = cv2.GaussianBlur(m * 255, (0, 0), 9) > 127
    return m


def net_mat(can):
    cv2.polylines(can, [np.array(DUONG_MIENG, np.int32) * S2], False, INK, 9, cv2.LINE_AA)
    cv2.ellipse(can, (MAT[0] * S2, MAT[1] * S2), (27 * S2, 17 * S2), -12, 195, 345, INK, 10, cv2.LINE_AA)     # mắt nhắm: cung cong
    cv2.circle(can, (MUI[0] * S2, MUI[1] * S2), 8, INK, -1, cv2.LINE_AA)


HOC = (74, 54, 38)                               # lòng hốc mắt gỗ (dạng 1, kiểu "mat")


def bo_cuc(kieu="he", luu=True):
    """sơ đồ bố cục: khối từng mảnh đặt đúng chỗ dáng gốc, tô phẳng theo nhóm màu của THIẾT KẾ MÌNH.
    Dạng 2: kieu = he | thu (bảng màu). Dạng 1 (màu hướng thu đã chọn): kieu = mat (hai ụ mắt là hốc gỗ rỗng) | khong_mat (ụ mắt
    thành mấu cành cụt có vân vòng, thêm tấm vỏ sẫm trên trán)."""
    PAL = PALS["thu" if K == 1 else kieu]
    _, _, atts = nap()
    T, sc = khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    for i, a in enumerate(atts):
        ten = a["att"]
        nh = loai(ten)
        nho = nh in ("pha_le",) or ten in ("P_weiba", "P_weiba2", "P_z_jingshi1")
        m = bong_khung(a, T, 2.4 if nho else 4.5)
        if not m.any():
            continue
        if ten == "P_tou" and K == 2:                                # đầu của MÌNH: sọ tròn + mõm dài chĩa xuống phải, có mồm
            m = dau_moi()
        if K == 1 and ten == "zuiba":                                # mồm dạng 1: khe răng cưa kẻ thẳng lên khúc gỗ
            ys, xs = np.nonzero(m)
            x0, x1, yy = xs.min() + 8, xs.max() - 8, int((ys.min() + ys.max()) / 2)
            n = 6
            pts = [(int(x0 + (x1 - x0) * j / n), yy + (16 if j % 2 else -16)) for j in range(n + 1)]
            cv2.polylines(can, [np.array(pts, np.int32)], False, INK, 9, cv2.LINE_AA)
            hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
            continue
        ys, xs = np.nonzero(m)
        can[m] = PAL[nh]
        if K == 2 and ten in ("P_bozi", "P_shenti", "P_y_houzhi", "P_y_qianzhi1", "P_z_qianzhi"):
            can[dom(m, 7 + i, {"P_bozi": 6, "P_shenti": 4}.get(ten, 1), 40, 70)] = PAL["dom"]
        if K == 1 and ten in ("P_tou", "P_shenti"):
            can[dom(m, 3 + i, 5 if ten == "P_tou" else 2, 44, 80)] = PAL["dom"]
        if K == 1 and ten == "YanR_01":                              # lòng ụ mắt gần
            can[m] = HOC if kieu == "mat" else PAL["go"]
            if kieu != "mat":                                        # mấu cành cụt: vân vòng
                cx, cy = int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2)
                for r in (0.55, 0.25):
                    cv2.ellipse(can, (cx, cy), (int((xs.max() - xs.min()) * r / 2), int((ys.max() - ys.min()) * r / 2)), 0, 0, 360, PAL["dom"], 5, cv2.LINE_AA)
        if K == 1 and ten == "P_tou" and kieu != "mat":              # tấm vỏ sẫm trên trán, mép dưới xếch xuống phía trước (phải)
            Y, X = np.mgrid[0:m.shape[0], 0:m.shape[1]]
            y_mep = ys.min() + (ys.max() - ys.min()) * (0.13 + 0.14 * (X - xs.min()) / max(1, xs.max() - xs.min()))
            can[m & (Y < y_mep)] = PAL["dom"]
        if ten in MONG:                                              # móng đá: 30% đáy
            Y = np.arange(m.shape[0])[:, None]
            can[m & (Y > ys.max() - (ys.max() - ys.min()) * 0.30)] = PAL["da"]
        if nh == "pha_le":
            X = np.arange(m.shape[1])[None, :]
            can[m & (X > (xs.min() + xs.max()) / 2)] = PAL["pha_le_dam"]
        can[vien(m, 4 if nho else 6)] = INK
        if ten == "P_tou" and K == 2:
            net_mat(can)
        hop[ten + "@" + a["slot"] if ten in hop else ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(MAU, exist_ok=True)
        out.save(os.path.join(MAU, f"bo_cuc_{kieu}.png"))
        json.dump(dict(hop=hop, sc=sc), open(os.path.join(MAU, "bo_cuc_hop.json"), "w"), indent=0)
        print(os.path.join(MAU, f"bo_cuc_{kieu}.png"), "tỉ lệ", round(sc, 4))
        for k, v in hop.items():
            print(f"  {k:16s} x {v[0]}-{v[2]}  y {v[1]}-{v[3]}")
    return out


# ================================================================ MẢNH THEO KHUNG PART (skill pokiclash-spine-rig mục 00)
MANH = os.environ.get("HG_MANH") or os.path.join(BASE, "manh")
PAL1 = dict(PALS["thu"], hoc=(74, 54, 38), kem=(244, 238, 220))
# tờ hướng dẫn: {tờ: (tỉ lệ phóng ảnh vùng, [ô ...])}; ô là tên hình của rig hoặc ô THÊM (mảnh của mình, rig gốc không có)
TO_K = {1: {"A": (4.0, ["P_tou", "P_shenti", "YanR_02", "YanL_01", "YanR_01"]),
            "B": (5.0, ["JiaoR_01", "JiaoL_01", "JiaoR_03", "JiaoR_02", "JiaoL_02", "JiaoL_03", "JiaoL_04"]),
            "C": (5.0, ["Weiba_01", "Weiba_02", "Weiba_03", "zuiba", "mieng_ha", "pha_le", "mat_xa"]),
            "D": (6.0, ["P_tuiR_H_1", "P_tuiR_H_2", "P_tuiL_H_1", "P_tuiL_H_2", "P_tuiR_Q_1", "P_tuiR_Q_2", "P_tuiL_Q_1", "P_tuiL_Q_2"])},
        # dạng 2: pha lê + túm lông ở vai của họ BỎ (người dùng: rêu và pha lê ra sau lưng); đầu, hàm dưới, cụm pha lê lưng là mảnh
        # của mình cắt thẳng từ concept (tờ E1, E2: "đúng chỗ, đúng cỡ"), không nằm trên tờ khung part
        2: {"A": (3.6, ["P_toufa", "P_bozi"]),
            "B": (3.0, ["P_shenti", "P_y_jiao1", "P_z_jiao1", "P_y_jiao", "P_z_jiao"]),
            "C": (4.0, ["P_y_er", "P_z_er", "P_weiba3", "P_weiba1", "P_weiba", "P_weiba2", "P_y_houmaofa"]),
            "D": (4.2, ["P_y_houzhi", "P_y_houzhi1", "P_y_houzhi2", "P_z_houzhi", "P_z_houzhi1", "P_z_houzhi2",
                        "P_y_qianzhi1", "P_y_qianzhi", "P_z_qianzhi", "P_z_qianzhi1"])}}
TO = TO_K[K]
THEM = {"mat_xa": (150, 270), "mieng_ha": (300, 250), "pha_le": (250, 290)} if K == 1 else {}     # cỡ ô (px trên tờ) của ô thêm
KHONG_SAT = tuple(THEM) + ("zuiba",)
# mảng vỏ sẫm trên khúc gỗ / mông: (u, v tâm theo khung ô, bán kính theo bề rộng ô, hạt giống)
DOM1 = {"P_tou": [(0.52, 0.60, 0.13, 3), (0.24, 0.76, 0.12, 5), (0.76, 0.86, 0.11, 8), (0.80, 0.56, 0.07, 11)],
        "P_shenti": [(0.36, 0.42, 0.16, 4)]}


def theo_ten():
    _, _, atts = nap()
    return {a["att"]: a for a in atts}


def co_o(ten, z):
    _, imgs, _ = nap()
    im = imgs[theo_ten()[ten]["region"]]
    return int(round(im.width * z)), int(round(im.height * z))


def bong(ten, z):
    """hình bóng KÍN của part trong khung ảnh vùng × z (làm trơn nhẹ; làm trên ảnh đã đệm viền để mép cắt thẳng không thành mấu)."""
    src = part_goc(theo_ten()[ten])
    w, h = co_o(ten, z)
    al = np.asarray(src.resize((w, h), Image.LANCZOS))[..., 3]
    d = int(round(3 * z))
    m = np.pad((al > 100).astype(np.uint8), d)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(1.0 * z))
    m = cv2.GaussianBlur(m * 255, (0, 0), 0.8 * z) > 127
    m = m[d:-d, d:-d]
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:
        m = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return m


def da_giac(c, r, seed):
    rng = np.random.default_rng(seed)
    k = int(rng.integers(5, 7))
    g = np.sort(rng.uniform(0, 2 * np.pi, k)) + rng.uniform(0, 1)
    return np.array([c + r * rng.uniform(0.8, 1.1) * np.array([np.cos(t), np.sin(t)]) for t in g], np.int32)


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    PAL = PAL1
    m = bong(ten, z)
    h, w = m.shape
    im = np.full((h, w, 3), 255, np.uint8)
    vien = 1.3 * z
    nh = loai(ten)
    if ten == "zuiba":                                               # mồm ngậm: chỉ một nét răng cưa (không tô)
        n = 8
        pts = [(int(w * (0.08 + 0.84 * j / n)), int(h * (0.50 + (0.10 if j % 2 else -0.10)))) for j in range(n + 1)]
        cv2.polylines(im, [np.array(pts, np.int32)], False, INK, int(round(1.5 * z)), cv2.LINE_AA)
        return im, im.min(axis=2) < 236
    if ten == "YanR_01":                                             # mắt gần: tròng nâu sẫm, một chấm kem lệch lên trái (mắt lác)
        im[m] = PAL["hoc"]
        cv2.circle(im, (int(w * 0.30), int(h * 0.27)), int(w * 0.14), PAL["kem"], -1, cv2.LINE_AA)
    else:
        im[m] = PAL[nh]
    if K == 2 and nh == "go" and ten != "P_weiba1":                  # dạng 2: mảng vỏ kiểu đốm hươu cao cổ rải trong mảnh gỗ
        dt = float(m.sum())
        # đốm TO, sáu cạnh như trên concept đã duyệt (bản đầu: nhiều mảnh nhỏ hình tam giác → GPT vẽ theo, khác concept)
        r0 = 0.17 * float(np.sqrt(dt))
        n = int(np.clip(round(dt / (r0 * r0 * 22.0)), 1, 3)) + (3 if ten == "P_bozi" else 0)
        rng = np.random.default_rng(11 + sum(map(ord, ten)))
        trong = cv2.erode(m.astype(np.uint8), el(r0 * 0.62)).astype(bool)
        ys_, xs_ = np.nonzero(trong)
        tam = []
        for _ in range(600):
            if len(tam) >= n or not len(ys_):
                break
            i_ = int(rng.integers(len(ys_)))
            c_ = np.array([xs_[i_], ys_[i_]], float)
            if all(np.hypot(*(c_ - c2)) > 2.45 * r0 for c2 in tam):
                tam.append(c_)
        mk = np.zeros((h, w), np.uint8)
        for c_ in tam:
            g0 = rng.uniform(0, np.pi / 3)
            pts = [c_ + r0 * rng.uniform(0.86, 1.06) * np.array([np.cos(g0 + q * np.pi / 3 + rng.uniform(-0.16, 0.16)),
                                                                 np.sin(g0 + q * np.pi / 3 + rng.uniform(-0.16, 0.16))]) for q in range(6)]
            cv2.fillPoly(mk, [np.array(pts, np.int32)], 1, cv2.LINE_AA)
        im[mk.astype(bool) & cv2.erode(m.astype(np.uint8), el(2.2 * z)).astype(bool)] = PAL["dom"]
    for (u, v, r, sd) in DOM1.get(ten, []) if K == 1 else []:
        mk = np.zeros((h, w), np.uint8)
        cv2.fillPoly(mk, [da_giac(np.array([u * w, v * h]), r * w, sd)], 1, cv2.LINE_AA)
        im[mk.astype(bool) & cv2.erode(m.astype(np.uint8), el(2.2 * z)).astype(bool)] = PAL["dom"]
    if ten in MONG:                                                  # móng đá: 36% đáy khúc chân dưới, có vạch mực ngăn
        ys, xs = np.nonzero(m)
        yk = int(ys.max() - (ys.max() - ys.min()) * 0.36)
        Y = np.arange(h)[:, None]
        im[m & (Y > yk)] = PAL["da"]
        im[m & (np.abs(Y - yk) <= 0.5 * z)] = INK
    im[m & ~cv2.erode(m.astype(np.uint8), el(vien)).astype(bool)] = INK
    im[~m] = 255
    return im, m


def o_them(ten):
    """ô không phải part của rig, vẽ phẳng bằng mã để Codex vẽ lại."""
    PAL = PAL1
    w, h = THEM[ten]
    im = np.full((h, w, 3), 255, np.uint8)
    if ten == "mat_xa":                                              # ụ mắt xa nhìn chếch: vành gỗ bầu dục đứng, tròng sẫm, chấm kem ở dưới
        cv2.ellipse(im, (w // 2, h // 2), (w // 2 - 8, h // 2 - 8), 0, 0, 360, INK, -1, cv2.LINE_AA)
        cv2.ellipse(im, (w // 2, h // 2), (w // 2 - 15, h // 2 - 15), 0, 0, 360, PAL["go"], -1, cv2.LINE_AA)
        cv2.ellipse(im, (int(w * 0.54), h // 2), (int(w * 0.27), int(h * 0.34)), 0, 0, 360, INK, -1, cv2.LINE_AA)
        cv2.ellipse(im, (int(w * 0.54), h // 2), (int(w * 0.27) - 6, int(h * 0.34) - 6), 0, 0, 360, PAL["hoc"], -1, cv2.LINE_AA)
        cv2.circle(im, (int(w * 0.60), int(h * 0.72)), int(w * 0.10), PAL["kem"], -1, cv2.LINE_AA)
    elif ten == "mieng_ha":                                          # mồm há: hốc sẫm, mép trên và mép dưới răng cưa (răng gỗ)
        n = 5
        cg = lambda j: 1.0 - (j / n - 1.0) ** 2                       # 0 ở hai khoé, 1 ở giữa: miệng hình thấu kính
        tren = [(int(w * (0.06 + 0.88 * j / (2 * n))), int(h * (0.50 - 0.36 * cg(j) + (0.0 if j % 2 == 0 else 0.15 * cg(j)))))
                for j in range(2 * n + 1)]
        duoi = [(int(w * (0.94 - 0.88 * j / (2 * n))), int(h * (0.50 + 0.36 * cg(j) - (0.0 if j % 2 == 0 else 0.15 * cg(j)))))
                for j in range(1, 2 * n)]
        cv2.fillPoly(im, [np.array(tren + duoi, np.int32)], PAL["hoc"], cv2.LINE_AA)
        cv2.polylines(im, [np.array(tren + duoi, np.int32)], True, INK, 7, cv2.LINE_AA)
    elif ten == "pha_le":                                            # nụ pha lê: hai lăng trụ nhỏ trên túm rêu
        cv2.ellipse(im, (w // 2, int(h * 0.80)), (int(w * 0.44), int(h * 0.15)), 0, 0, 360, INK, -1, cv2.LINE_AA)
        cv2.ellipse(im, (w // 2, int(h * 0.80)), (int(w * 0.44) - 7, int(h * 0.15) - 7), 0, 0, 360, PAL["reu"], -1, cv2.LINE_AA)
        for pts, lech in (([(0.30, 0.78), (0.24, 0.30), (0.40, 0.08), (0.56, 0.30), (0.52, 0.78)], 0.40),
                          ([(0.56, 0.80), (0.58, 0.48), (0.70, 0.36), (0.80, 0.50), (0.76, 0.80)], 0.70)):
            P = np.array([(int(x * w), int(y * h)) for x, y in pts], np.int32)
            cv2.fillPoly(im, [P], PAL["pha_le"], cv2.LINE_AA)
            Q = np.array([(int(lech * w), P[2][1])] + [tuple(q) for q in P[3:]] + [(int(lech * w), P[-1][1])], np.int32)
            cv2.fillPoly(im, [Q], PAL["pha_le_dam"], cv2.LINE_AA)
            cv2.polylines(im, [P], True, INK, 7, cv2.LINE_AA)
    return im, im.min(axis=2) < 236


def nhom_part():
    """tờ hướng dẫn: mỗi part một ô ĐÚNG KHUNG ảnh vùng của nó (× tỉ lệ của tờ), trong ô là hình bóng kín tô phẳng theo thiết kế của
    mình, viền sẫm đúng mép. Ghi mau/part_<tờ>.png và .json ({ô: x, y, w, h, z})."""
    os.makedirs(MAU, exist_ok=True)
    for to, (z, ds) in TO.items():
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        le = 30
        x, y, hh = le, le, 0
        for ten in ds:
            cell, m = o_them(ten) if ten in THEM else thiet_ke(ten, z)
            h, w = m.shape
            if x + w + le > W:
                x, y, hh = le, y + hh + le, 0
            if y + h + le > H:
                raise SystemExit(f"tờ {to}: ô {ten} không vừa (y = {y}, cao {h})")
            im[y:y + h, x:x + w] = cell
            khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z}
            x += w + le
            hh = max(hh, h)
        Image.fromarray(im).save(os.path.join(MAU, f"part_{to}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_{to}.json"), "w", encoding="utf-8"), indent=1)
        print(f"{to} (x{z}):", ", ".join(f"{k} {v['w']}x{v['h']} @ {v['x'] + v['w'] // 2},{v['y'] + v['h'] // 2}" for k, v in khung.items()))


def cat_part(to, ep=False):
    """cắt tờ N_<tờ>: mỗi part lấy đúng Ô của nó trên tờ, tách nền trắng → manh/part/<hình>.png (cỡ ô trên tờ; rig tự co). Đo IoU với
    hình bóng hướng dẫn; chỉ ghi đè khi bản mới khít hơn (ep=True: ghi đè). Dọn bằng mã (không vẽ): cắt sát hình bóng nới vài px; chỗ
    vẽ hụt lấy màu tô gần nhất của tờ hướng dẫn; kẻ nét mực dọc phía trong mép lưới."""
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
    tt = anh.doc_to(path, dien_tich_min=200, gop_px=12)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    by = theo_ten()
    pso = os.path.join(ra, "_iou.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    ids = [i for m_ in tt.manh for i in m_["ids"]]
    print(os.path.basename(path))
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236                       # hình bóng trên tờ hướng dẫn
        d = 14 if ten in THEM else 0                                     # ô thêm: lấy rộng ra quanh ô
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
        if ten not in KHONG_SAT:
            sat = cv2.dilate(g.astype(np.uint8), el(0.75 * z)).astype(bool)
            cell[..., 3][~sat] = 0
            a &= sat
            ho = g & ~a
            bu = int(ho.sum())
            if ho.any():                                                  # vẽ hụt trong hình bóng: lấy màu tô gần nhất của tờ hướng dẫn
                gc = gd[y:y + h, x:x + w]
                to_ = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (gc.max(axis=2) > 105)
                if to_.any():
                    _, lb = cv2.distanceTransformWithLabels((~to_).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                    tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
                    tra[lb[to_]] = gc[to_]
                    cell[ho, :3] = tra[lb][ho]
                    cell[ho, 3] = 255
            at = by[ten]                                                  # nét mực dọc phía trong mép lưới của họ
            hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
            hm = np.zeros(a.shape, np.uint8)
            cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
            dai = hm.astype(bool) & ~cv2.erode(hm, el(1.0 * z), borderValue=0).astype(bool)
            cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), os.path.basename(path)]
        Image.fromarray(cell, "RGBA").save(os.path.join(ra, ten + ".png"))
        print(f"  {ten}: {cell.shape[1]} x {cell.shape[0]} (x{z}), IoU {iou:.2f}" + (f", bù {bu} px" if bu else ""))
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)


def so_part():
    """tờ so từng part đã cắt với hình bóng hướng dẫn: ĐỎ = hình bóng mà mảnh không phủ, XANH LÁ = vẽ thừa → mau/so_part.png."""
    cells = []
    for to in TO:
        pj = os.path.join(MAU, f"part_{to}.json")
        if not os.path.exists(pj):
            continue
        Kh = json.load(open(pj, encoding="utf-8"))
        gd = np.asarray(Image.open(os.path.join(MAU, f"part_{to}.png")).convert("RGB"))
        for ten, v in Kh.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm) or ten in KHONG_SAT:
                continue
            x, y, w, h = v["x"], v["y"], v["w"], v["h"]
            g = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 255, np.uint8)
            im[a] = c[..., :3][a]
            im[g & ~a] = (255, 0, 0)
            im[a & ~g] = (im[a & ~g] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            cv2.putText(im, f"{to} {ten}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cells.append(im)
    Wd, x, y, hh, pos = 1900, 0, 0, 0, []
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
    Image.fromarray(S).save(os.path.join(MAU, "so_part.png"))
    print(os.path.join(MAU, "so_part.png"), len(cells), "ô")


# ================================================================ THÂN LIỀN: các khúc NỐI NHAU gen LIỀN một ảnh rồi cắt
# (skill pokiclash-spine-rig mục 00 "Các khúc NỐI NHAU thì gen LIỀN một ảnh rồi cắt"; người dùng 2026-11-12 sau khi tôi gen mỗi khúc
# một ô rồi vá chỗ nối bằng cách xoá nét: "trong skill tôi đã note là gen cả rồi cắt ra để lúc nối cho match cơ mà").
# gan: các mảnh thân + chân phía gần, hợp lại thành MỘT hình bóng ở dáng gốc của rig (chỉ viền ngoài, không nét ở chỗ nối);
# xa: từng chân phía xa (nằm sau thân) là một hình liền riêng, dời ra hai bên tờ. Sau khi gen, mỗi mảnh lấy điểm ảnh của tờ này qua
# lưới của nó (thế giới dáng gốc → tờ): hai mảnh chồng nhau lấy CÙNG điểm ảnh nên đốm, vân, màu khớp tuyệt đối, không có nét ở khớp.
LIEN_K = {1: dict(gan=["P_tou", "P_shenti", "P_tuiR_H_1", "P_tuiR_H_2", "P_tuiR_Q_1", "P_tuiR_Q_2", "P_tuiL_Q_1", "P_tuiL_Q_2"],
                  xa=[["P_tuiL_H_1", "P_tuiL_H_2"]], dom=4),
          2: dict(gan=["P_bozi", "P_shenti", "P_y_houzhi", "P_y_houzhi1", "P_y_houzhi2", "P_y_qianzhi1", "P_y_qianzhi"],
                  xa=[["P_z_houzhi", "P_z_houzhi1", "P_z_houzhi2"], ["P_z_qianzhi", "P_z_qianzhi1"]], dom=9)}
LIEN = LIEN_K[K]


def _nhom_lien():
    return [LIEN["gan"]] + LIEN["xa"]


def to_lien():
    """tờ hướng dẫn thân liền → mau/lien.png + lien.json (tỉ lệ px mỗi đơn vị rig, gốc toạ độ từng nhóm)."""
    by = theo_ten()
    T, sc = khung_T()
    PAL = PAL1
    nhom = _nhom_lien()
    hop = []
    for ds in nhom:
        P = np.concatenate([np.array(by[t]["xy"], float).reshape(-1, 2) for t in ds])
        hop.append((P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()))
    g = hop[0]
    rong_xa = sum(h[2] - h[0] for h in hop[1:])
    ti = min((H - 70) / (g[3] - g[1]), (W - 70 - 50 * len(hop)) / (g[2] - g[0] + rong_xa))
    # xếp ngang: [chân xa 1] [thân gần] [chân xa 2]; đáy các nhóm cùng nằm trên một đường
    thu_tu = ([1] if len(hop) > 1 else []) + [0] + list(range(2, len(hop)))
    tong = sum((hop[i][2] - hop[i][0]) * ti for i in thu_tu) + 50 * (len(thu_tu) - 1)
    x = (W - tong) / 2
    goc = {}
    for i in thu_tu:
        h = hop[i]
        goc[i] = (x - h[0] * ti, (H + (g[3] - g[1]) * ti) / 2 + g[1] * ti)      # px = (ox + X·ti, oy − Y·ti)
        x += (h[2] - h[0]) * ti + 50
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    rng = np.random.default_rng(5 + K)
    for i, ds in enumerate(nhom):
        ox, oy = goc[i]
        T2 = lambda p_, ox=ox, oy=oy: np.stack([ox + np.asarray(p_, float)[..., 0] * ti, oy - np.asarray(p_, float)[..., 1] * ti], -1)
        ms = {t: bong_khung(by[t], T2, 3.0) for t in ds}
        m = np.zeros((H * S2, W * S2), bool)
        for t in ds:
            m |= ms[t]
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(5)).astype(bool)
        can[m] = PAL["go"]
        # đốm sáu cạnh: tránh chỗ hai mảnh chồng nhau (khớp), tránh móng
        chong = np.zeros(m.shape, np.uint8)
        for t in ds:
            chong += ms[t].astype(np.uint8)
        dt = float(m.sum())
        r0 = (0.085 if i == 0 else 0.16) * float(np.sqrt(dt))
        mong = np.zeros(m.shape, bool)
        for t in ds:
            if t in MONG:
                ys, xs = np.nonzero(ms[t])
                Y = np.arange(m.shape[0])[:, None]
                mong |= ms[t] & (Y > ys.max() - (ys.max() - ys.min()) * (0.36 if K == 1 else 0.30))
        # mỗi đốm phải nằm TRỌN trong phần riêng của MỘT mảnh (không chạm vùng hai mảnh chồng nhau, không chạm mảnh khác): mảnh nào
        # cử động thì mang nguyên đốm theo, không có đốm bị xẻ đôi ở khớp (bản đầu chỉ tránh vùng chồng một ít: đốm bị xẻ khi chân nhấc).
        # Cỡ đốm theo từng mảnh (mảnh chân nhỏ thì đốm nhỏ), số đốm theo diện tích phần riêng của mảnh.
        khong_mong = ~cv2.dilate(mong.astype(np.uint8), el(r0 * 0.6)).astype(bool)
        for t in ds:
            if K == 1 and t.startswith("P_tui"):                     # dạng 1: chân ngắn, để gỗ trơn
                continue
            rieng = ms[t] & (chong == 1) & m & khong_mong
            if K == 1 and t == "P_tou":                              # dạng 1: mặt (mắt, mồm) ở nửa trên khúc gỗ: để gỗ trơn
                ys, xs = np.nonzero(ms[t])
                Y = np.arange(m.shape[0])[:, None]
                rieng &= Y > ys.min() + (ys.max() - ys.min()) * 0.47
            dtr = float(rieng.sum())
            if dtr < 1:
                continue
            rt = min(r0, 0.27 * float(np.sqrt(dtr)))
            cho = cv2.erode(rieng.astype(np.uint8), el(rt * 1.12)).astype(bool)
            ys_, xs_ = np.nonzero(cho)
            n_t = int(np.clip(round(dtr / (rt * rt * 11.0)), 0, 7))
            tam = []
            for _ in range(900):
                if len(tam) >= n_t or not len(ys_):
                    break
                j = int(rng.integers(len(ys_)))
                c_ = np.array([xs_[j], ys_[j]], float)
                if all(np.hypot(*(c_ - c2)) > 2.45 * rt for c2 in tam):
                    tam.append(c_)
            for c_ in tam:
                g0 = rng.uniform(0, np.pi / 3)
                pts = [c_ + rt * rng.uniform(0.86, 1.06) * np.array([np.cos(g0 + q * np.pi / 3 + rng.uniform(-0.16, 0.16)),
                                                                     np.sin(g0 + q * np.pi / 3 + rng.uniform(-0.16, 0.16))]) for q in range(6)]
                cv2.fillPoly(can, [np.array(pts, np.int32)], PAL["dom"], cv2.LINE_AA)
        can[mong] = PAL["da"]
        can[cv2.morphologyEx(mong.astype(np.uint8), cv2.MORPH_GRADIENT, el(3)).astype(bool) & m] = INK
        can[vien(m, 8)] = INK
    os.makedirs(MAU, exist_ok=True)
    Image.fromarray(can).resize((W, H), Image.LANCZOS).save(os.path.join(MAU, "lien.png"))
    json.dump({"ti": ti, "goc": {str(i): goc[i] for i in goc}, "nhom": nhom}, open(os.path.join(MAU, "lien.json"), "w"), indent=1)
    print(os.path.join(MAU, "lien.png"), f"{ti:.3f} px mỗi đơn vị rig; nhóm:", [len(d) for d in nhom])


def prompt_lien():
    """file prompt gen tờ thân liền → gui_gpt/huou_go_<K>/luot_2_than_lien.txt (ảnh lưu tai_ve/N_lien.png)."""
    duyet = os.path.join(TAI, "L1_duyet.png")
    gd = os.path.join(MAU, "lien.png")
    out = os.path.join(TAI, "N_lien.png")
    pk = os.path.join(HERE, "gui_gpt", f"{CODE}_{K}")
    p = os.path.join(pk, "luot_2_than_lien.txt")
    n_xa = len(LIEN["xa"])
    con = ("a small forest log-fawn: an upright log of pale birch wood with dark bark patches, big dopey dark eyes, a zigzag mouth, "
           "twig antlers with autumn leaves, a small rump, four stubby legs with grey stone hooves" if K == 1 else
           "a forest stag-giraffe of pale birch wood with big dark brown hexagonal bark patches, an eyeless spotted head with jagged "
           "wooden jaws, branch antlers, a mane of red-orange maple leaves, emerald crystals on its back, four legs with grey stone "
           "hooves, a leaf-tuft tail")
    than = ("the upright log (head and chest in one), the small rump behind it and three of its legs" if K == 1 else
            "the long neck with the round chest, the barrel of the body and the two NEAR legs (the near hind leg at the left with its "
            "thigh, the near front leg at the right)")
    xa = ("ONE separate leg stands at the left of the canvas: the far hind leg" if n_xa == 1 else
          "TWO separate legs stand at the left and at the right of the canvas: the far hind leg (left) and the far front leg (right)")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {os.path.normpath(duyet)}: the APPROVED creature, 1536x1024, white background: {con}. It gives the design, the "
         "colours, the ink line, the crayon hatching and the look of the wood and of its bark patches.",
         f"image 2 = {os.path.normpath(gd)}: BODY GUIDE, 1536x1024, white background, drawn by computer: in the middle ONE big flat "
         f"silhouette = the creature's wooden BODY WITHOUT its head parts and decorations: {than}, all fused into one shape; {xa}, "
         "complete from its top to its hoof. Pale = wood, dark brown hexagons = bark patches, grey = stone hooves. It gives the exact "
         "silhouettes, sizes and positions.",
         "", f"SAVE: save it as a PNG to {os.path.normpath(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY "
         "every silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, "
         "the shapes must coincide). This sheet will be cut by a program into the body parts of a 2D animation rig.", "",
         "VERY IMPORTANT, ONE CONTINUOUS SURFACE: the big shape in the middle is ONE piece of wood. Draw the dark-brown ink outline "
         "ONLY around the OUTSIDE of each silhouette. INSIDE a silhouette draw NO outline lines at all: no line where a leg joins "
         "the body, no line between the neck and the body, no line between the parts of a leg, no folds, no creases. The wood "
         "colour, the crayon hatching and the wood grain run across the whole shape without any break.", "",
         "- WOOD: pale birch wood (#E2D6BA) with loose diagonal crayon hatching and a few thin wavy grain lines (thin darker "
         "pencil lines, not ink) that follow the length of the neck, the body and the legs.",
         "- BARK PATCHES: the dark brown (#7C5C40) six-sided patches of the giraffe pattern, exactly WHERE and as BIG as image 2 "
         "shows them, each a slightly irregular hexagon with rounded corners and a thin ink outline, as on image 1. Do not add "
         "patches, do not move them.",
         "- HOOVES: the lower end of every leg is a chunky hoof of grey stone (#8C887C), exactly where image 2 shows grey, with one "
         "ink line between the wood and the stone and one tiny chip line on the stone.",
         "- OUTLINE: dark-brown ink (#2B2118), about 7 px thick on this canvas, wobbly like a real pen, closed around each "
         "silhouette and lying just INSIDE its edge.",
         "- The separate leg" + ("" if n_xa == 1 else "s") + " at the side: drawn the same way (wood, one or two bark patches where "
         "shown, stone hoof), each with its own closed outline.",
         "Draw nothing else: no head, no face, no eyes, no mouth, no leaves, no crystals, no moss, no tail, no ground.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no "
         "darker side, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no "
         "frames, no guide lines."]
    os.makedirs(pk, exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    hd = os.path.join(pk, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2b:")[0].rstrip("\n") if os.path.exists(hd) else ""
    gdm = ["", "## Lượt 2b: tờ THÂN LIỀN (thay các ô cổ / thân / chân của lượt 2; 2026-11-12)", "",
           "Người dùng: các khúc nối nhau phải gen LIỀN một ảnh rồi cắt (skill `pokiclash-spine-rig` mục 00), không gen mỗi khúc một ô.",
           f"**Chỉ gửi GPT đường dẫn:** `{os.path.normpath(p)}`. Ảnh lưu vào `{os.path.normpath(out)}` (trùng tên thì `_2`, `_3`…).", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
           f"| 1 | `{os.path.normpath(duyet)}` | Concept đã duyệt (1536 × 1024, nền trắng). Lấy thiết kế, màu, nét, vân sáp |",
           f"| 2 | `{os.path.normpath(gd)}` | Tờ hướng dẫn tự dựng (1536 × 1024, nền trắng): ở giữa MỘT hình bóng phẳng = thân gỗ liền với "
           "các chân phía gần (gỗ sáng, đốm nâu sáu cạnh, móng xám), viền sẫm chỉ ở ngoài; chân phía xa đứng riêng ở hai bên |", "",
           "Kiểm: hình bóng trùng tờ hướng dẫn; **trong hình không có nét mực nào** ở chỗ chân nối thân, cổ nối thân; đốm đúng chỗ; nền trắng.",
           f"Claude cắt bằng `HG_DANG={K} py -3 -I ArtGen/Spine/huou_go.py cat_lien` (nướng tờ này vào khung từng mảnh qua lưới của rig)."]
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gdm) + "\n")
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
        tol = 6.0 / max(1.0, float(np.sqrt(abs(den))))               # nới ra ngoài lưới vài px (nét viền nằm sát mép lưới)
        nho = np.minimum(np.minimum(b0, b1), b2)
        hon = (nho >= -tol) & (nho > tot_nhat)                        # điểm ngoài lưới: theo tam giác mà nó nằm gần nhất
        Wd[hon] = b0[hon, None] * V[t[0]] + b1[hon, None] * V[t[1]] + b2[hon, None] * V[t[2]]
        tot_nhat[hon] = nho[hon]
    return Wd.reshape(h, w, 2)


def cat_lien():
    """nướng tờ thân liền (tai_ve/N_lien*.png) vào khung từng mảnh → manh/part/<hình>.png (đè lên ô gen riêng của lượt 2)."""
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
    rgba[..., :3] *= rgba[..., 3:4] / 255.0                           # nhân sẵn alpha để lấy mẫu song tuyến không loang trắng
    by = theo_ten()
    zs = {t: z_ for to, (z_, ds) in TO.items() for t in ds}
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    ti = L["ti"]
    print(os.path.basename(path))
    for i, ds in enumerate(L["nhom"]):
        ox, oy = L["goc"][str(i)]
        for ten in ds:
            a = by[ten]
            w, h = co_o(ten, zs[ten])
            Wd = _the_gioi_o(a, w, h)
            ok = ~np.isnan(Wd[..., 0])
            mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
            my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
            cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            al = cell[..., 3:4]
            cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
            # mỗi mảnh chỉ lấy trong HÌNH BÓNG của chính nó (nới 0,7·z px, mép mềm): lấy cả khung lưới thì mảnh mang theo mép thẳng của
            # lưới và mẩu viền của mảnh bên cạnh, lúc cử động lộ thành vết cắt thẳng
            z_ = zs[ten]
            sil = cv2.dilate(bong(ten, z_).astype(np.uint8), el(0.7 * z_)).astype(np.float32)
            sil = np.clip(cv2.GaussianBlur(sil, (0, 0), 0.45 * z_) * 2.0 - 0.5, 0.0, 1.0)
            cell[..., 3] *= sil
            out = np.clip(cell, 0, 255).astype(np.uint8)
            Image.fromarray(out, "RGBA").save(os.path.join(ra, ten + ".png"))
            phu = float((out[..., 3] > 127).sum()) / max(1, int(bong(ten, zs[ten]).sum()))
            print(f"  {ten}: {w} x {h}, phủ {phu:.2f} hình bóng của part")


def cat_cong():
    """tách ảnh cánh cổng rừng (tai_ve/cong*.png của dạng 1, dùng chung hai dạng) thành hai lớp → inbox/huou_go_1/manh/cong/:
    cong_sau.png (cả cổng: vành + lòng xoáy, vẽ SAU con vật), cong_truoc.png (nửa vành bên TRÁI, phía gần người xem, vẽ TRƯỚC con
    vật). Lòng cổng = vùng màu lục liền lớn nhất (trên vành không có gì lục ngoài vân nhựa, pha lê)."""
    from quai import anh
    goc = os.path.join(HERE, "inbox", f"{CODE}_1")
    path = anh.to_moi_nhat(os.path.join(goc, "tai_ve"), "cong")
    tt = anh.doc_to(path, dien_tich_min=400, gop_px=40)
    rgba = tt.rgba.copy()
    al = rgba[..., 3] > 127
    r, g, b = [rgba[..., i].astype(int) for i in range(3)]
    luc = al & (g > r + 22) & (g > b + 8)
    luc = cv2.morphologyEx(luc.astype(np.uint8), cv2.MORPH_CLOSE, el(9))
    n, lab, st, _ = cv2.connectedComponentsWithStats(luc, 8)
    trong = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    trong = cv2.morphologyEx(trong.astype(np.uint8), cv2.MORPH_CLOSE, el(25)).astype(bool)
    ys, xs = np.nonzero(al)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    tx, _ = np.nonzero(trong.T.any(axis=1, keepdims=True))
    cx = int((np.nonzero(trong.any(axis=0))[0].min() + np.nonzero(trong.any(axis=0))[0].max()) / 2)
    truoc = rgba.copy()
    X = np.arange(rgba.shape[1])[None, :]
    truoc[..., 3] = np.where(al & ~cv2.dilate(trong.astype(np.uint8), el(3)).astype(bool) & (X < cx), rgba[..., 3], 0)
    ra = os.path.join(goc, "manh", "cong")
    os.makedirs(ra, exist_ok=True)
    Image.fromarray(rgba[y0:y1, x0:x1], "RGBA").save(os.path.join(ra, "cong_sau.png"))
    Image.fromarray(truoc[y0:y1, x0:x1], "RGBA").save(os.path.join(ra, "cong_truoc.png"))
    json.dump({"tam_x": (cx - x0) / (x1 - x0), "rong": int(x1 - x0), "cao": int(y1 - y0)}, open(os.path.join(ra, "cong.json"), "w"))
    print(ra, f"{x1 - x0} x {y1 - y0}, tâm lòng cổng ở {100 * (cx - x0) / (x1 - x0):.0f}% bề ngang; lòng {int(trong.sum())} px")


def xuat_part_goc():
    ra = os.path.join(scan(), "parts")
    os.makedirs(ra, exist_ok=True)
    _, _, atts = nap()
    for a in atts:
        part_goc(a).save(os.path.join(ra, f"{a['order']:02d}_{a['att']}.png"))
    print(ra, len(atts), "part")


def main(a):
    if a[:1] == ["part_goc"]:
        xuat_part_goc()
    elif a[:1] == ["nhom_part"]:
        nhom_part()
    elif a[:1] == ["cat_part"]:
        for to in (a[1:2] or list(TO)):
            cat_part(to, ep="ep" in a[2:])
    elif a[:1] == ["to_lien"]:
        to_lien()
        prompt_lien()
    elif a[:1] == ["cat_lien"]:
        cat_lien()
    elif a[:1] == ["cat_cong"]:
        cat_cong()
    elif a[:1] == ["so_part"]:
        so_part()
    elif a[:1] == ["bo_cuc"]:
        for k in (a[1:] or (["mat", "khong_mat"] if K == 1 else list(PALS))):
            bo_cuc(k)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
