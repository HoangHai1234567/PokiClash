# -*- coding: utf-8 -*-
"""Thổ Tinh (thach_de): khớp các mảnh tờ D (đầu trên, hàm dưới, hai nanh) vào chỗ mảnh đầu cũ `manh/dau.png` (người dùng 2026-11-18:
"tạo thêm hàm dưới cho tướng"). GPT vẽ đầu trên to hơn đầu cũ nên dò tỉ lệ + dời cho mặt nạ (vùng trên miệng) trùng mặt nạ đầu cũ;
nanh đặt theo vùng màu kem của đầu cũ; hàm dưới đặt theo phần cằm còn lại (đầu cũ trừ đầu trên trừ nanh).

    thach_de_dau.py [non]  → manh/_dau_khop.json (mỗi mảnh: tỉ lệ, tâm theo px ảnh dau.png) + manh/_dau_so.png (ngậm, há 14°, há 28°)

Rig (thach_de_rig.py) đọc _dau_khop.json để đặt mảnh theo chỗ mảnh đầu cũ."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NON = "non" in sys.argv[1:]                                      # dạng 1 Tiểu Thổ Tinh: mảnh non_* ở inbox/thach_de_non/manh
MANH = os.path.join(HERE, "inbox", "thach_de_non" if NON else "thach_de_1", "manh")
P = "non_" if NON else ""


def mo(n):
    return Image.open(os.path.join(MANH, P + n + ".png")).convert("RGBA")


def mask(im, nguong=40):
    return np.asarray(im)[:, :, 3] > nguong


def kem(im):
    a = np.asarray(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    return (al > 100) & (r > 215) & (g > 200) & (b > 160) & (r - b > 18)


def dat(dst_shape, im, s, cx, cy):
    """mặt nạ của im co s lần, tâm ảnh đặt ở (cx, cy) trên khung dst."""
    w, h = max(1, round(im.width * s)), max(1, round(im.height * s))
    m = np.asarray(im.resize((w, h), Image.LANCZOS))[:, :, 3] > 40
    out = np.zeros(dst_shape, bool)
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xs0, ys0 = max(0, -x0), max(0, -y0)
    xd0, yd0 = max(0, x0), max(0, y0)
    xd1, yd1 = min(dst_shape[1], x0 + w), min(dst_shape[0], y0 + h)
    if xd1 > xd0 and yd1 > yd0:
        out[yd0:yd1, xd0:xd1] = m[ys0:ys0 + yd1 - yd0, xs0:xs0 + xd1 - xd0]
    return out


def iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else 0.0


def khop():
    D = mo("dau")
    MD = mask(D)
    H, W = MD.shape
    KD = kem(D)
    # vùng trên miệng của đầu cũ: phần trên đỉnh nanh cao nhất
    ys = np.where(KD.any(1))[0]
    y_mieng = int(ys.min())
    tren = MD.copy()
    tren[y_mieng + 10:, :] = False
    T = mo("dau_tren")
    best = (0, None)
    cu = os.path.join(MANH, "_dau_khop.json")
    if os.path.exists(cu) and "lai" not in sys.argv:          # dò lại (chậm ~50 s) chỉ khi gọi `thach_de_dau.py lai`
        k = json.load(open(cu))["dau_tren"]
        best = (k["iou"], (k["s"], int(k["cx"]), int(k["cy"])))
    s_uoc = (np.ptp(np.where(MD.any(0))[0]) + 1) / (np.ptp(np.where(mask(T).any(0))[0]) + 1)         # ước theo bề ngang
    for s in (np.arange(s_uoc - 0.12, s_uoc + 0.12, 0.01) if best[1] is None else []):
        for cx in range(W // 2 - 30, W // 2 + 31, 3):
            for cy in range(int(H * 0.40), int(H * 0.56), 3):
                m = dat(MD.shape, T, s, cx, cy)
                m2 = m.copy()
                m2[y_mieng + 10:, :] = False
                v = iou(m2, tren)
                if v > best[0]:
                    best = (v, (s, cx, cy))
    s0, cx0, cy0 = best[1]
    # tinh chỉnh bước 1 px
    for s in np.arange(s0 - 0.01, s0 + 0.0101, 0.0025):
        for cx in range(cx0 - 3, cx0 + 4):
            for cy in range(cy0 - 3, cy0 + 4):
                m = dat(MD.shape, T, s, cx, cy)
                m[y_mieng + 10:, :] = False
                v = iou(m, tren)
                if v > best[0]:
                    best = (v, (s, cx, cy))
    s, cx, cy = best[1]
    print(f"đầu trên: tỉ lệ {s:.4f}, tâm ({cx}, {cy}), IoU vùng trên miệng {best[0]:.3f}")
    out = {"dau_tren": dict(s=float(s), cx=float(cx), cy=float(cy), iou=float(best[0]))}
    MT = dat(MD.shape, T, s, cx, cy)
    # nanh: hai vùng kem lớn nhất của đầu cũ (trái = gần, to)
    from scipy import ndimage
    lab, n = ndimage.label(KD)
    vung = sorted([(int((lab == i).sum()), i) for i in range(1, n + 1)], reverse=True)[:2]
    hop = []
    for _, i in vung:
        yy, xx = np.where(lab == i)
        hop.append((xx.min(), yy.min(), xx.max(), yy.max()))
    hop.sort(key=lambda b: b[0])
    for k, b in zip(("nanh_1", "nanh_2"), hop):
        N = mo(k)
        mN = mask(N)
        yy, xx = np.where(mN)
        hN = yy.max() - yy.min() + 1
        sk_ = (b[3] - b[1] + 1) / hN * 1.04
        out[k] = dict(s=float(sk_), cx=float((b[0] + b[2]) / 2), cy=float((b[1] + b[3]) / 2))
        print(f"{k}: hộp đầu cũ {b}, tỉ lệ {sk_:.3f}")
    # hàm: phần cằm còn lại (đầu cũ trừ đầu trên trừ nanh), khớp mép dưới và bề ngang phần đá (không tính lòng miệng)
    # cằm đầu cũ: phần đá (không kem) dưới miệng; đáy = điểm thấp nhất, giữa ngang = trung bình 60 hàng đáy
    cam = MD & ~ndimage.binary_dilation(KD, iterations=4)
    cam[:y_mieng + 30, :] = False
    yy, xx = np.where(cam)
    day = int(yy.max())
    sel = yy > day - 60
    bc = (int(xx[sel].min()), int(yy.min()), int(xx[sel].max()), day)
    cx_cam = float(xx[sel].mean())
    Hm = mo("ham")
    a = np.asarray(Hm).astype(int)
    da = (a[..., 3] > 100) & (a[..., 0] > 120) & (abs(a[..., 0] - a[..., 2]) < 50) & ~kem(Hm)   # đá tím xám (không lòng miệng, không răng)
    yy2, xx2 = np.where(da)
    bh = (int(xx2.min()), int(yy2.min()), int(xx2.max()), int(yy2.max()))
    sel2 = yy2 > bh[3] - 60 / s
    # ngậm miệng: đỉnh răng dưới ngang chân nanh trên (răng cài vào khe nanh), đáy cằm trùng đáy cằm đầu cũ → ra tỉ lệ hàm
    kt = kem(T)
    kt[: int(T.height * 0.8), :] = False                       # nanh chỉ ở 20 % dưới của đầu trên (trên đó là mắt)
    yk = np.where(kt.sum(1) > 3)[0]
    chan_nanh = cy + (int(yk.min()) - T.height / 2) * s       # chân hàng nanh trên (px dau.png)
    kh = kem(Hm)
    yr = np.where(kh.any(1))[0]
    dinh_rang = int(yr.min())                                  # đỉnh răng dưới (px ảnh hàm)
    day_ham = int(np.where(np.asarray(Hm)[:, :, 3].max(1) > 40)[0].max())
    # hàm ngắn hơn cằm cũ: phóng tới 1,15 lần tỉ lệ đầu (rộng hơn thì lòng miệng lòi ra hai bên), phần còn thiếu thì cằm cao lên
    # và nanh (gắn hàm) dời lên theo
    sh = float(np.clip((bc[3] - chan_nanh - 6) / (day_ham - dinh_rang), s, 1.15 * s))
    cam_moi = chan_nanh + 6 + (day_ham - dinh_rang) * sh
    cxh = cx_cam - (float(xx2[sel2].mean()) - Hm.width / 2) * sh
    cyh = cam_moi - (day_ham - Hm.height / 2) * sh
    for k in ("nanh_1", "nanh_2"):
        out[k]["cy"] += cam_moi - bc[3]
    print(f"chân nanh trên y {chan_nanh:.0f}, đáy cằm cũ {bc[3]} → mới {cam_moi:.0f}, răng dưới ảnh hàm y {dinh_rang}..đáy {day_ham}")
    out["ham"] = dict(s=sh, cx=float(cxh), cy=float(cyh))
    print(f"hàm: cằm đầu cũ {bc}, phần đá ảnh hàm {bh}, tỉ lệ {sh:.3f}, tâm ({cxh:.0f}, {cyh:.0f})")
    # khớp hàm (bản lề): đầu sau (trái) của hàng răng dưới
    xr = np.where(kh.any(0))[0]
    out["ban_le"] = dict(x=float(cxh + (int(xr.min()) - 8 - Hm.width / 2) * sh), y=float(cyh + (dinh_rang - Hm.height / 2) * sh))
    out["y_mieng"] = y_mieng
    out["dinh_rang"] = dinh_rang
    json.dump(out, open(os.path.join(MANH, "_dau_khop.json"), "w"), indent=1)
    cat_ham(out)
    return out


def cat_ham(K, vien=6):
    """lòng miệng của hàm rộng hơn đầu trên: ở dáng ngậm, phần trên hàng răng dưới mà nằm ngoài hình bóng đầu trên (nới 3 px) bị bỏ,
    rồi kẻ lại viền mực dọc mép cắt → manh/ham_cat.png (rig dùng ảnh này)."""
    from scipy import ndimage
    D = mo("dau")
    T, Hm = mo("dau_tren"), mo("ham")
    kt, kh = K["dau_tren"], K["ham"]
    sh = kh["s"]
    # hình bóng đầu trên chiếu về khung ảnh hàm: điểm (u, v) của ảnh hàm ↔ dau (cx + (u − W/2)·sh, ...) ↔ ảnh đầu trên
    Hh, Wh = Hm.height, Hm.width
    v, u = np.mgrid[0:Hh, 0:Wh]
    xd = kh["cx"] + (u - Wh / 2) * sh
    yd = kh["cy"] + (v - Hh / 2) * sh
    ut = np.round((xd - kt["cx"]) / kt["s"] + T.width / 2).astype(int)
    vt = np.round((yd - kt["cy"]) / kt["s"] + T.height / 2).astype(int)
    MTi = ndimage.binary_erosion(ndimage.binary_fill_holes(mask(T)), iterations=4 if NON else 14)
    ok = (ut >= 0) & (ut < T.width) & (vt >= 0) & (vt < T.height)
    trong = np.zeros((Hh, Wh), bool)
    trong[ok] = MTi[vt[ok], ut[ok]]
    a = np.asarray(Hm).copy()
    al = a[:, :, 3] > 40
    # mọi thứ phía trên hàng răng dưới mà ra ngoài đầu trên (co vào 14 px) đều bỏ: lòng miệng chỉ còn phần khuất sau đầu trên
    bo = al & ~trong & (v < K["dinh_rang"] + 2)
    if NON:                                                   # đầu non: lòng miệng không lòi ra ngoài má, cắt chỉ đục lỗ bên trong
        bo[:] = False
    con = ndimage.binary_opening(al & ~bo, iterations=3)
    lab, n = ndimage.label(con)
    if n > 1:                                                 # giữ mảng lớn nhất (vụn viền mực rời ra thì bỏ)
        lon = max(range(1, n + 1), key=lambda i: (lab == i).sum())
        con = lab == lon
    mep = con & ~ndimage.binary_erosion(con, iterations=vien) & ndimage.binary_dilation(bo, iterations=vien + 1)
    lo = ndimage.binary_fill_holes(con) & ~con               # lỗ trong lòng miệng (khe giấy trắng giữa răng bị cắt thành nền): tô màu lòng miệng
    a[:, :, 3] = np.where(con, a[:, :, 3], 0)
    a[mep, 0], a[mep, 1], a[mep, 2], a[mep, 3] = 43, 33, 24, 255
    a[lo, 0], a[lo, 1], a[lo, 2], a[lo, 3] = 74, 34, 40, 255
    if lo.any():
        print(f"ham_cat: lấp {int(lo.sum())} px lỗ trong lòng miệng")
    Image.fromarray(a).save(os.path.join(MANH, P + "ham_cat.png"))
    print(f"ham_cat: bỏ {int(bo.sum())} px lòng miệng ngoài đầu trên")


def ghep(K, goc_ham=0.0, nen=None):
    """ghép đầu trên + hàm + nanh lên khung dau.png (phóng 1), hàm và nanh xoay goc_ham độ (mở xuống) quanh bản lề."""
    D = mo("dau")
    Wc, Hc = D.width + 200, D.height + 200
    can = Image.new("RGBA", (Wc, Hc), nen or (0, 0, 0, 0))
    ox, oy = 100, 100
    bl = (K["ban_le"]["x"] + ox, K["ban_le"]["y"] + oy)

    def dan(n, xoay):
        im = mo("ham_cat" if n == "ham" and os.path.exists(os.path.join(MANH, P + "ham_cat.png")) else n)
        k = K[n]
        w, h = round(im.width * k["s"]), round(im.height * k["s"])
        im = im.resize((w, h), Image.LANCZOS)
        lop = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
        lop.alpha_composite(im, (int(round(k["cx"] + ox - w / 2)), int(round(k["cy"] + oy - h / 2))))
        if xoay:
            lop = lop.rotate(xoay, center=bl, resample=Image.BICUBIC)     # PIL: dương = ngược kim; mở hàm = quay theo kim (hướng mặt phải)
        can.alpha_composite(lop)
    dan("ham", -goc_ham)
    dan("dau_tren", 0)
    dan("nanh_1", -goc_ham)
    dan("nanh_2", -goc_ham)
    return can, (ox, oy)


def main():
    K = khop()
    D = mo("dau")
    nen = (200, 200, 205, 255)
    o = Image.new("RGBA", ((D.width + 200) * 4, D.height + 200), nen)
    g0 = Image.new("RGBA", (D.width + 200, D.height + 200), nen)
    g0.alpha_composite(D, (100, 100))
    o.alpha_composite(g0, (0, 0))
    for i, a in enumerate((0, 14, 28)):
        g, _ = ghep(K, a, nen)
        ImageDraw.Draw(g).text((8, 8), f"ghep ham {a} do", fill=(0, 0, 0))
        o.alpha_composite(g, ((i + 1) * (D.width + 200), 0))
    ImageDraw.Draw(o).text((8, 8), "dau cu", fill=(0, 0, 0))
    p = os.path.join(MANH, "_dau_so.png")
    o.convert("RGB").save(p)
    print(p)


if __name__ == "__main__":
    main()
