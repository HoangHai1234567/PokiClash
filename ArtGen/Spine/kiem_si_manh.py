# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng (kiem_si): cắt MẢNH CỨNG từ sáu tờ "đúng chỗ, đúng cỡ" (M_A..M_F: Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài mảnh
không chồng nhau, vẽ đủ phần khuất) và hai tờ mảnh rời (M_S1: hai thanh kiếm tháo rời; M_S2: tua, lá mào, bắp tay, đùi), rồi ĐẶT mảnh lên
khung concept (lá mào, tua đặt theo gốc → ngọn đọc trên concept; bắp tay, đùi, kiếm đặt ở bước rig theo xương).

    kiem_si_manh.py lam    → inbox/kiem_si_1/manh/<ảnh>.png (RGBA cắt sát) + dat.json + _so_ghep.png (ghép lại cạnh concept) + _to.png

dat.json: {"_thu_tu": [mảnh sau → trước], mảnh: {anh, A: [[a, b, tx], [c, d, ty]] (px ảnh → px concept) | None, co: [w, h], nhom}}.
Con nhìn sang phải; "g" = gần (bên trái người xem, vẽ trước thân), "x" = xa; chân: "s" = chân sau (bên trái), "t" = chân trước."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kiem_si as KS  # noqa: E402

MANH = os.path.join(KS.BASE, "manh")
DUYET = os.path.join(KS.TAI, "L1_duyet.png")
PAD = 4
# tờ "đúng chỗ" → {mảnh: tâm ước chừng trên khung concept}
TO = {"A": {"vai_g": (557, 435), "vai_x": (1160, 437), "cang_x": (1095, 755), "ong_s": (488, 903), "ong_t": (914, 920)},
      "B": {"mu": (830, 245), "cang_g": (730, 810), "ban_s": (482, 968), "ban_t": (953, 978)},
      "C": {"dau": (922, 462), "ao": (472, 772), "nam_g": (840, 845), "nam_x": (1045, 862)},
      "D": {"than": (865, 687), "duoi": (495, 252)},
      "E": {"giap": (860, 635), "vay": (720, 870)},
      "F": {"dai": (852, 677)}}
# tờ mảnh rời: các hàng (y tâm), mỗi hàng xếp trái → phải
ROI_TO = {"S1": [(120, ["vo_a"]), (300, ["luoi_a"]), (480, ["chuoi_a"]), (660, ["vo_b"]), (860, ["luoi_b", "chuoi_b"])],
          "S2": [(265, ["tua1", "tua2", "la_to", "la_nho"]), (775, ["bap_g", "bap_x", "dui1", "dui2"])]}
# MẢNH RỜI đặt lên concept: (tên mảnh, ảnh, gốc (x, y), ngọn (x, y), bề rộng px concept hoặc None = giữ tỉ lệ ảnh, lật ngang, kiểu đầu)
# kiểu "len": gốc = giữa mép DƯỚI ảnh, ngọn = giữa mép trên (lá mào vẽ dựng đứng); "xuong": gốc = giữa mép TRÊN, ngọn = mép dưới (tua, chi)
ROI = [
    ("la_nho", "la_nho", (1012, 262), (1150, 20), None, False, "len"), ("la_to", "la_to", (1004, 300), (1362, 80), None, False, "len"),
    ("tua_g1", "tua1", (407, 546), (409, 662), None, False, "xuong"), ("tua_g2", "tua2", (492, 568), (493, 688), None, False, "xuong"),
    ("tua_g3", "tua1", (602, 596), (603, 722), None, True, "xuong"), ("tua_x", "tua2", (1200, 578), (1201, 692), None, True, "xuong"),
    # bắp tay, đùi: gần như khuất hết trên concept; đặt tạm theo trục vai → khuỷu, hông → gối ước chừng (bước rig nắn theo xương)
    ("bap_g", "bap_g", (650, 470), (628, 790), None, False, "xuong"), ("bap_x", "bap_x", (1075, 500), (1100, 700), None, False, "xuong"),
    ("dui_s", "dui1", (585, 770), (500, 880), 130, False, "xuong"), ("dui_t", "dui2", (875, 790), (912, 905), 125, False, "xuong"),
]
KIEM = ["vo_a", "luoi_a", "chuoi_a", "vo_b", "luoi_b", "chuoi_b"]          # đặt ở bước rig theo chỗ kiếm của rig gốc
# thứ tự vẽ sau → trước (theo thứ tự slot của rig gốc)
THU_TU = ["duoi", "ao", "ban_t", "dui_t", "ong_t", "ban_s", "dui_s", "ong_s", "tua_x", "bap_x", "than", "vay", "giap", "cang_x", "vai_x",
          "dai", "dau", "la_nho", "la_to", "mu", "nam_x", "nam_g", "bap_g", "cang_g", "tua_g1", "tua_g2", "tua_g3", "vai_g"]


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def moi_nhat(ma):
    """ảnh mới nhất của một tờ (M_A.png, M_A_2.png ...)."""
    ds = [f for f in os.listdir(KS.TAI) if f == f"M_{ma}.png" or (f.startswith(f"M_{ma}_") and f.endswith(".png"))]
    if not ds:
        raise SystemExit(f"chưa có tờ M_{ma}")
    ds.sort(key=lambda f: (int(f[len(f"M_{ma}_"):-4]) if f != f"M_{ma}.png" else 1))
    return os.path.join(KS.TAI, ds[-1])


def doc(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int32)


def nen(A, lo_min=2500):
    """mặt nạ NỀN: trắng thông ra mép ảnh + lỗ trắng kín lớn. Trắng kín nhỏ (răng, chấm mắt, ria) là của mảnh."""
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


def cum(A, dt_min=300, lo_min=2500):
    fg = ~nen(A, lo_min)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1))
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
    return [(lab == i, st[i], cen[i]) for i in range(1, n) if st[i, 4] >= dt_min]


def cat_to(ma):
    A = doc(moi_nhat(ma))
    ds = cum(A, lo_min=10 ** 9 if ma in ("C", "D") else 2500)          # đầu (ria trắng), thân: không đục lỗ trắng kín
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
        x, y, w, h, _ = ds[bi][1]
        print(f"    {ten:8s} x {x}-{x + w}  y {y}-{y + h}")
    thua = [tuple(int(v) for v in st[:5]) for i, (m, st, c) in enumerate(ds) if i not in da and st[4] >= 500]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra


def cat_roi(ma):
    A = doc(moi_nhat(ma))
    ds = cum(A, 600)
    hg = ROI_TO[ma]
    ra = {}
    hang = {i: [] for i in range(len(hg))}
    for m, st, cen in ds:
        k = min(range(len(hg)), key=lambda i: abs(hg[i][0] - cen[1]))
        hang[k].append((cen[0], m, st))
    for k, (_, ten) in enumerate(hg):
        hs = sorted(hang[k], key=lambda t: t[0])
        if len(hs) != len(ten):
            raise SystemExit(f"tờ {ma} hàng {k + 1}: đếm được {len(hs)} mảnh, cần {len(ten)} ({ten}): " +
                             str([tuple(int(v) for v in h_[2][:4]) for h_ in hs]))
        for t, (_, m, st) in zip(ten, hs):
            ra[t] = (A, m)
            print(f"    {t:8s} {st[2]} × {st[3]}")
    print(f"  tờ {ma}: {len(ra)} mảnh")
    return ra


def hai_dau(im, kieu):
    """(gốc, ngọn) trên ảnh mảnh rời. "xuong": gốc = giữa mép trên, ngọn = giữa mép dưới; "len": gốc = giữa mép dưới, ngọn = giữa mép trên."""
    a = np.asarray(im)[..., 3] > 120
    ys, xs = np.nonzero(a)
    y0, y1 = ys.min(), ys.max()
    tren = (float(xs[ys <= y0 + 6].mean()), float(y0))
    duoi = (float(xs[ys >= y1 - 6].mean()), float(y1))
    return (duoi, tren) if kieu == "len" else (tren, duoi)


def aff_hai_diem(p0, p1, q0, q1, w_anh=None, rong=None, lat=False):
    """affine ảnh → concept đưa p0 → q0, p1 → q1; tỉ lệ dọc trục = |q| / |p|; tỉ lệ ngang = rong / w_anh (None: bằng tỉ lệ dọc)."""
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
    src = np.asarray(im.convert("RGBa"))
    out = cv2.warpAffine(src, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    canvas.alpha_composite(Image.frombytes("RGBa", (w, h), out.tobytes()).convert("RGBA"))


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
    for ma in ROI_TO:
        for ten, (A, m) in cat_roi(ma).items():
            luu_anh(ten, A, m)
    for ten in KIEM:
        dat[ten] = dict(anh=ten, A=None, co=[anh_[ten].width, anh_[ten].height], nhom="kiem")
    for ten, anh_ten, q0, q1, rong, lat, kieu in ROI:
        im = anh_[anh_ten]
        p0, p1 = hai_dau(im, kieu)
        Aff = aff_hai_diem(p0, p1, q0, q1, im.width - 2 * PAD, rong, lat)
        dat[ten] = dict(anh=anh_ten, A=Aff, co=[im.width, im.height], nhom="roi", goc=list(q0), ngon=list(q1))
    thieu = [t for t in THU_TU if t not in dat]
    if thieu:
        raise SystemExit("thiếu mảnh: " + ", ".join(thieu))
    dat["_thu_tu"] = THU_TU
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    # ghép lại cạnh concept (không có kiếm: kiếm đặt ở bước rig)
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in THU_TU:
        dan(ghep, anh_[dat[t]["anh"]], dat[t]["A"])
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    ghep.convert("RGB").save(os.path.join(MANH, "_ghep.png"))
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
    print(os.path.join(MANH, "_to.png"), len(anh_), "ảnh,", len(THU_TU), "mảnh + 6 mảnh kiếm")


def cat_tay():
    """tờ M_T (bàn tay hai mảnh): bốn cụm xếp trái → phải: bốn ngón A, bốn ngón B, lòng bàn tay A, lòng bàn tay B."""
    A = doc(moi_nhat("T"))
    ds = sorted(cum(A, 3000, lo_min=10 ** 9), key=lambda t: -t[1][4])[:4]
    if len(ds) != 4:
        raise SystemExit(f"tờ T: đếm được {len(ds)} mảnh, cần 4")
    ds.sort(key=lambda t: t[2][0])
    for ten, (m, st, cen) in zip(["tay_ngon_a", "tay_ngon_b", "tay_long_a", "tay_long_b"], ds):
        # mảnh vẽ to rồi thu ~0,3 lần lúc lắp: nét mực 8 px chỉ còn ~2,5 px, mảnh hơn nét của cả con (~6 px) → làm ĐẬM nét trước
        # (nở vùng mực 5 px về mỗi phía, kể cả ra ngoài viền)
        muc = (A.max(2) < 120) & m
        muc = cv2.dilate(muc.astype(np.uint8), el(5)).astype(bool)
        A2 = A.copy()
        A2[muc] = (43, 33, 24)
        im, _ = manh_rgba(A2, m | muc)
        im.save(os.path.join(MANH, ten + ".png"))
        print(f"    {ten:12s} {im.width} × {im.height}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["tay"]:
        cat_tay()
    elif sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
