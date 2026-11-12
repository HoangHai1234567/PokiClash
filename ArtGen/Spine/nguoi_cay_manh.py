# -*- coding: utf-8 -*-
"""Người cây (nguoi_cay): cắt MẢNH CỨNG từ bốn tờ "đúng chỗ, đúng cỡ" (M_A..M_D: Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài mảnh không
chồng nhau, vẽ đủ phần khuất) và hai tờ mảnh rời (M_S1: lá, râu, cành khô, rêu rủ; M_S2: quả cầu dây leo, dây gai), rồi ĐẶT mọi mảnh
lên khung concept (mảnh rời đặt theo cuống → mũi đọc trên concept).

    nguoi_cay_manh.py lam    → inbox/nguoi_cay_1/manh/<ảnh>.png (RGBA cắt sát) + dat.json + _so_ghep.png (ghép lại cạnh concept)
                                + _to.png (từng ảnh trên nền xám)

dat.json: {"_thu_tu": [mảnh sau → trước], mảnh: {anh, A: [[a, b, tx], [c, d, ty]] (px ảnh → px concept), co: [w, h], nhom}}.
Con nhìn sang phải; "g" = gần (bên trái người xem, vẽ trước thân), "x" = xa."""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nguoi_cay as NC  # noqa: E402

MANH = os.path.join(NC.BASE, "manh")
DUYET = os.path.join(NC.TAI, "L1_duyet.png")
PAD = 4
INK = (43, 33, 24)
# tờ "đúng chỗ" → {mảnh: tâm ước chừng trên khung concept}
TO = {"A": {"dau": (825, 295), "cang_g": (333, 575), "cang_x": (1160, 505), "ong_g": (522, 857), "ong_x": (965, 847), "dai": (755, 657)},
      "B": {"than": (765, 540), "nam_g": (342, 770), "nam_x": (1208, 298), "ban_g": (497, 940), "ban_x": (1000, 940)},
      "C": {"vai_g": (478, 361), "vai_x": (1023, 365), "dui_g": (585, 755), "dui_x": (907, 750)},
      "D": {"bap_g": (484, 509), "bap_x": (1016, 513)}}
# tờ S1: ba hàng (theo y tâm), mỗi hàng xếp trái → phải
S1 = [(180, ["la_s1", "la_s2", "la_s3", "la_s4", "la_s5", "rau"]), (510, ["la_n1", "la_n2", "la_n3", "la_n4"]),
      (855, ["canh_to", "canh_nho", "canh_vua", "ru1", "ru2", "ru3"])]
# MẢNH RỜI đặt lên concept: (tên mảnh, ảnh, cuống (x, y), mũi (x, y), bề rộng px concept hoặc None = giữ tỉ lệ ảnh, lật ngang)
# cuống = đầu trên của ảnh (lá, rêu) / đầu dưới (cành khô: gốc cành); toạ độ đọc trên concept kẻ lưới
ROI = [
    # mào lá sau đầu (sau → trước): ba chiếc, đo trên concept
    ("mao1", "la_s1", (744, 218), (595, 192), 88, False), ("mao2", "la_s3", (792, 198), (645, 99), 104, False),
    ("mao3", "la_s2", (838, 194), (752, 72), 90, True),
    # cổ áo lá: lá sẫm trái, lá sẫm phải, lá nhạt trái, lá sẫm giữa
    ("co1", "la_s5", (640, 392), (604, 534), 84, False), ("co4", "la_s2", (906, 392), (962, 542), 84, True),
    ("co2", "la_n1", (703, 360), (689, 532), 90, False), ("co3", "la_s3", (768, 398), (774, 582), 100, False),
    # váy lá: hàng sau rồi hàng trước (cuống nấp sau đai)
    ("vay_s1", "la_s4", (612, 656), (572, 800), 86, False), ("vay_s4", "la_s2", (672, 660), (660, 846), 92, False),
    ("vay_s2", "la_s1", (748, 660), (742, 858), 96, True), ("vay_s5", "la_s5", (836, 660), (842, 850), 92, True),
    ("vay_s3", "la_s3", (898, 656), (936, 800), 86, True),
    ("vay1", "la_s2", (586, 656), (504, 802), 92, False), ("vay7", "la_s4", (922, 654), (974, 802), 92, True),
    ("vay2", "la_n2", (636, 660), (610, 878), 96, False), ("vay6", "la_n4", (868, 660), (882, 874), 96, True),
    ("vay3", "la_s5", (704, 664), (696, 880), 104, False), ("vay4", "la_s1", (790, 664), (786, 924), 116, False),
    # lá nằm trên u vai
    ("la_vai_g", "la_s4", (474, 326), (338, 268), 70, False), ("la_vai_x", "la_s2", (990, 338), (1090, 284), 58, True),
    # rêu rủ dưới bắp tay
    ("ru_g1", "ru1", (488, 556), (486, 682), 42, False), ("ru_g2", "ru2", (526, 556), (530, 664), 42, True),
    ("ru_g3", "ru3", (558, 552), (560, 640), 40, False),
    ("ru_x3", "ru3", (984, 545), (984, 640), 38, True), ("ru_x1", "ru2", (956, 540), (954, 668), 42, False),
    ("ru_x2", "ru1", (1014, 556), (1016, 696), 44, True),
    # râu
    ("rau", "rau", (857, 394), (866, 576), None, False),
]
CUONG = 0.10            # lá của tờ S1 có cuống ngắn: kéo dài mảnh thêm chừng này về phía cuống cho phiến lá phủ đúng chỗ trên concept
CANH = [("canh_g1", "canh_to", (424, 272), (398, 142), None, False), ("canh_g2", "canh_nho", (548, 258), (552, 180), None, False),
        ("canh_x", "canh_vua", (1004, 288), (992, 164), None, False)]
# thứ tự vẽ sau → trước. U rêu vai luôn vẽ SAU (đè lên) cả cánh tay của bên đó, kể cả cẳng tay và nắm tay (người dùng 2026-11-12: "phần
# cánh tay layer phải ở dưới vai": tay xa giơ lên mà cẳng tay đè lên u rêu thì như tay mọc ra trước vai)
THU_TU = ["bap_x", "ru_x3", "ru_x1", "ru_x2", "cang_x", "nam_x", "canh_x", "vai_x", "la_vai_x",
          "ban_x", "dui_x", "ong_x", "ban_g", "dui_g", "ong_g", "than",
          "vay_s1", "vay_s4", "vay_s2", "vay_s5", "vay_s3", "vay1", "vay7", "vay2", "vay6", "vay3", "vay4", "dai",
          "ru_g1", "ru_g2", "ru_g3", "canh_g1", "canh_g2", "bap_g", "cang_g", "nam_g", "vai_g", "la_vai_g",
          "co1", "co4", "co2", "co3",
          "mao1", "mao2", "mao3", "dau", "rau"]

if NC.K == 1:               # DẠNG 1 (con non): số đo trên concept dạng 1; ít lớp lá, không cành khô; dây gai và quả cầu dùng lại ảnh dạng lớn
    TO = {"A": {"dau": (798, 292), "cang_g": (346, 598), "cang_x": (1150, 497), "ong_g": (532, 855), "ong_x": (955, 850), "dai": (742, 664)},
          "B": {"than": (752, 552), "nam_g": (340, 762), "nam_x": (1200, 300), "ban_g": (495, 940), "ban_x": (1000, 940)},
          "C": {"vai_g": (550, 395), "vai_x": (1006, 410), "dui_g": (582, 755), "dui_x": (907, 752)},
          "D": {"bap_g": (492, 507), "bap_x": (1016, 516)}}
    S1 = [(180, ["mam_a", "mam_b", "la_c1", "la_c2", "la_c3"]), (510, ["la_v1", "la_v2", "la_v3", "la_v4", "la_v5"]), (820, ["ru1", "ru2"])]
    ROI = [
        # mầm hai lá trên đỉnh đầu (cuống ảnh = chân mầm, nấp sau đỉnh đầu)
        # (thân mầm `mam_than` là một que ngắn vẽ bằng mã, xem lam(); hai lá xoè ngang từ đầu que)
        ("mam1", "mam_a", (803, 116), (627, 78), None, False), ("mam2", "mam_b", (797, 116), (947, 62), None, True),
        # cổ áo ba lá
        ("co1", "la_c1", (737, 420), (696, 540), 86, False), ("co3", "la_c3", (872, 420), (918, 534), 86, True),
        ("co2", "la_c2", (802, 424), (812, 580), 98, False),
        # váy năm lá ngắn
        ("vay1", "la_v1", (606, 672), (543, 792), 94, False), ("vay5", "la_v5", (886, 670), (954, 792), 94, True),
        ("vay3", "la_v3", (745, 676), (742, 836), 102, False), ("vay2", "la_v2", (662, 674), (640, 828), 98, False),
        ("vay4", "la_v4", (824, 676), (844, 828), 98, True),
        # mỗi tay một dải rêu rủ
        ("ru_g1", "ru1", (497, 552), (497, 672), 46, False), ("ru_x1", "ru2", (978, 555), (978, 670), 44, False),
    ]
    CANH = []
    THU_TU = ["bap_x", "ru_x1", "cang_x", "nam_x", "vai_x", "ban_x", "dui_x", "ong_x", "ban_g", "dui_g", "ong_g", "than",
              "vay1", "vay5", "vay3", "vay2", "vay4", "dai", "ru_g1", "bap_g", "cang_g", "nam_g", "vai_g", "co1", "co3", "co2",
              "mam_than", "mam1", "mam2", "dau"]


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def moi_nhat(ma):
    """ảnh mới nhất của một tờ (M_A.png, M_A_2.png ...)."""
    ds = [f for f in os.listdir(NC.TAI) if f == f"M_{ma}.png" or (f.startswith(f"M_{ma}_") and f.endswith(".png"))]
    if not ds:
        raise SystemExit(f"chưa có tờ M_{ma}")
    ds.sort(key=lambda f: (int(f[len(f"M_{ma}_"):-4]) if f != f"M_{ma}.png" else 1))
    return os.path.join(NC.TAI, ds[-1])


def doc(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int32)


def nen(A, lo_min=2500):
    """mặt nạ NỀN: trắng thông ra mép ảnh + lỗ trắng kín lớn. Trắng kín nhỏ (răng, chấm mắt) là của mảnh."""
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    H, W = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H or a >= lo_min:
            bg |= lab == i
    return bg


def manh_rgba(A, m):
    """ảnh RGBA cắt sát của mặt nạ m (mép mềm: điểm mép ngả trắng thì trong dần)."""
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - PAD), max(0, ys.min() - PAD), min(m.shape[1], xs.max() + PAD + 1), min(m.shape[0], ys.max() + PAD + 1)
    sub = A[y0:y1, x0:x1].astype(np.uint8)
    mm = m[y0:y1, x0:x1]
    a = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = sub.min(2).astype(np.float32)
    a = np.where(vien, np.minimum(a, np.clip((250.0 - sang) / 70.0, 0, 1)), a)
    out = np.dstack([sub, (np.clip(a, 0, 1) * 255).astype(np.uint8)])
    out[..., :3][out[..., 3] == 0] = 0
    return Image.fromarray(out, "RGBA"), (int(x0), int(y0))


def cum(A, dt_min=300):
    fg = ~nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1))
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
    return [(lab == i, st[i], cen[i]) for i in range(1, n) if st[i, 4] >= dt_min]


def cat_to(ma):
    A = doc(moi_nhat(ma))
    ds = cum(A)
    ra, da = {}, set()
    for ten, (cx, cy) in TO[ma].items():
        best, bi = 1e18, -1
        for i, (m, st, cen) in enumerate(ds):
            if i in da:
                continue
            x, y, w, h, _ = st
            dx, dy = max(x - cx, 0, cx - (x + w)), max(y - cy, 0, cy - (y + h))
            d = dx * dx + dy * dy + 0.02 * ((cen[0] - cx) ** 2 + (cen[1] - cy) ** 2)
            if d < best:
                best, bi = d, i
        if bi < 0:
            raise SystemExit(f"tờ {ma}: không thấy mảnh {ten}")
        da.add(bi)
        ra[ten] = (A, ds[bi][0])
    thua = [tuple(int(v) for v in st[:5]) for i, (m, st, c) in enumerate(ds) if i not in da and st[4] >= 500]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra


def cat_s1():
    A = doc(moi_nhat("S1"))
    ds = cum(A, 600)
    ra = {}
    hang = {i: [] for i in range(len(S1))}
    for m, st, cen in ds:
        k = min(range(len(S1)), key=lambda i: abs(S1[i][0] - cen[1]))
        hang[k].append((cen[0], m))
    for k, (_, ten) in enumerate(S1):
        hs = sorted(hang[k], key=lambda t: t[0])
        if len(hs) != len(ten):
            raise SystemExit(f"tờ S1 hàng {k + 1}: đếm được {len(hs)} mảnh, cần {len(ten)} ({ten})")
        for t, (_, m) in zip(ten, hs):
            ra[t] = (A, m)
    print(f"  tờ S1: {len(ra)} mảnh")
    return ra


def cat_s2():
    A = doc(moi_nhat("S2"))
    ds = sorted(cum(A, 3000), key=lambda t: -t[1][4])[:2]
    if len(ds) != 2:
        raise SystemExit("tờ S2: không đủ hai vật")
    ds.sort(key=lambda t: t[2][1])                      # cầu ở trên, dây gai ở dưới
    print("  tờ S2: cầu", tuple(int(v) for v in ds[0][1][:4]), "dây gai", tuple(int(v) for v in ds[1][1][:4]))
    return {"cau": (A, ds[0][0]), "gai": (A, ds[1][0])}


def hai_dau(im, kieu):
    """(cuống, mũi) trên ảnh mảnh rời: lá / rêu / râu: cuống = giữa mép trên, mũi = điểm thấp nhất; cành: gốc = giữa mép dưới, ngọn = giữa
    khung trên cùng."""
    a = np.asarray(im)[..., 3] > 120
    ys, xs = np.nonzero(a)
    y0, y1 = ys.min(), ys.max()
    tren = xs[ys <= y0 + 6]
    duoi = xs[ys >= y1 - 6]
    if kieu == "canh":
        return (float(duoi.mean()), float(y1)), (float((xs.min() + xs.max()) / 2), float(y0))
    return (float(tren.mean()), float(y0)), (float(duoi.mean()), float(y1))


def aff_hai_diem(p0, p1, q0, q1, w_anh=None, rong=None, lat=False):
    """affine ảnh → concept đưa p0 → q0, p1 → q1; tỉ lệ dọc trục = |q| / |p|; tỉ lệ ngang = rong / w_anh (None: bằng tỉ lệ dọc);
    lat: lật ngang quanh trục."""
    p0, p1, q0, q1 = (np.array(v, float) for v in (p0, p1, q0, q1))
    dp, dq = p1 - p0, q1 - q0
    lp, lq = np.hypot(*dp), np.hypot(*dq)
    up, uq = dp / lp, dq / lq
    np_, nq = np.array([-up[1], up[0]]), np.array([-uq[1], uq[0]])
    sd = lq / lp
    sn = (rong / w_anh if rong and w_anh else sd) * (-1 if lat else 1)
    M = sd * np.outer(uq, up) + sn * np.outer(nq, np_)
    t = q0 - M @ p0
    return [[float(M[0, 0]), float(M[0, 1]), float(t[0])], [float(M[1, 0]), float(M[1, 1]), float(t[1])]]


def dan(canvas, im, A):
    """dán ảnh RGBA lên canvas RGBA theo affine A (ảnh → canvas)."""
    M = np.array(A, float)
    w, h = canvas.size
    inv = cv2.invertAffineTransform(M)
    src = np.asarray(im.convert("RGBa"))
    out = cv2.warpAffine(src, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    del inv
    lop = Image.frombytes("RGBa", (w, h), out.tobytes()).convert("RGBA")
    canvas.alpha_composite(lop)


def lam():
    os.makedirs(MANH, exist_ok=True)
    C = doc(DUYET)
    anh_, dat = {}, {}

    def luu_anh(ten, A, m):
        im, goc = manh_rgba(A, m)
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = im
        return im, goc

    for ma in TO:
        for ten, (A, m) in cat_to(ma).items():
            im, goc = luu_anh(ten, A, m)
            dat[ten] = dict(anh=ten, A=[[1.0, 0.0, float(goc[0])], [0.0, 1.0, float(goc[1])]], co=[im.width, im.height], nhom="cho")
    for ten, (A, m) in cat_s1().items():
        luu_anh(ten, A, m)
    if NC.K == 1:                                       # thân mầm: một que ngắn màu cuống lá, viền mực hai bên (đầu trên nấp sau hai lá,
        a_ = np.asarray(anh_["mam_a"])                  # đầu dưới nấp sau đỉnh đầu)
        dac = a_[..., 3] > 200
        sang = a_[..., :3].astype(int).sum(2)
        mau = np.median(a_[..., :3][dac & (sang > np.median(sang[dac]) - 30)], axis=0).astype(np.uint8)
        w_, h_ = 30, 84
        q = np.zeros((h_, w_, 4), np.uint8)
        q[..., :3] = mau
        q[..., 3] = 255
        q[:, :6, :3] = INK
        q[:, -6:, :3] = INK
        im = Image.fromarray(q, "RGBA")
        im.save(os.path.join(MANH, "mam_than.png"))
        anh_["mam_than"] = im
        dat["mam_than"] = dict(anh="mam_than", A=[[1.0, 0.0, 785.0], [0.0, 1.0, 96.0]], co=[w_, h_], nhom="roi", cuong=[800.0, 176.0],
                               mui=[800.0, 100.0])
    if NC.K == 1:                                       # dây gai, quả cầu: chép ảnh đã cắt của dạng lớn
        for ten in ("cau", "gai"):
            im = Image.open(os.path.join(HERE, "inbox", f"{NC.CODE}_2", "manh", ten + ".png")).convert("RGBA")
            im.save(os.path.join(MANH, ten + ".png"))
            anh_[ten] = im
            dat[ten] = dict(anh=ten, A=None, co=[im.width, im.height], nhom="chieu")
    else:
        for ten, (A, m) in cat_s2().items():
            im, _ = luu_anh(ten, A, m)
            dat[ten] = dict(anh=ten, A=None, co=[im.width, im.height], nhom="chieu")
    for ten, anh_ten, q0, q1, rong, lat in ROI + CANH:
        im = anh_[anh_ten]
        kieu = "canh" if anh_ten.startswith("canh") else "la"
        p0, p1 = hai_dau(im, kieu)
        if anh_ten.startswith("la_") and not ten.startswith("vay"):      # lá váy KHÔNG kéo dài: cuống phải nấp sau đai (kéo dài là cuống nhô lên trên mép đai)
            q0 = tuple(np.array(q0, float) - CUONG * (np.array(q1, float) - np.array(q0, float)))
        Aff = aff_hai_diem(p0, p1, q0, q1, im.width - 2 * PAD, rong, lat)
        dat[ten] = dict(anh=anh_ten, A=Aff, co=[im.width, im.height], nhom="roi", cuong=[float(q0[0]), float(q0[1])], mui=list(q1))
    thieu = [t for t in THU_TU if t not in dat]
    if thieu:
        raise SystemExit("thiếu mảnh: " + ", ".join(thieu))
    dat["_thu_tu"] = THU_TU
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    # ghép lại cạnh concept
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in THU_TU:
        dan(ghep, anh_[dat[t]["anh"]], dat[t]["A"])
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    ghep.convert("RGB").save(os.path.join(MANH, "_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - C).max(2)
    print(f"  ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ")
    # tờ từng ảnh trên nền xám
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    x = y = 12
    hh = 0
    cho = []
    for t, im in anh_.items():
        if x + im.width + 12 > 2400:
            x, y, hh = 12, y + hh + 34, 0
        cho.append((t, x, y))
        x += max(im.width, 90) + 16
        hh = max(hh, im.height)
    to = Image.new("RGB", (2400, y + hh + 40), (150, 150, 150))
    dr = ImageDraw.Draw(to)
    for t, x, y in cho:
        to.paste(anh_[t], (x, y + 20), anh_[t])
        dr.text((x, y), t, fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(anh_), "ảnh,", len(THU_TU), "mảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
