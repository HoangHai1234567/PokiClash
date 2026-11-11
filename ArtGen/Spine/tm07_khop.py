# -*- coding: utf-8 -*-
"""Khớp từng mảnh GPT vào concept đã duyệt bằng dò tự động (tỉ lệ, góc, vị trí), thuần numpy + Pillow (py -3 không có cv2).

Cách: phân lớp màu cả concept lẫn mảnh theo bảng màu của dòng (chàm, ngà, đỏ, hồng, vàng, cyan, đỏ rượu, ba lam nước, bọt, mực);
với mỗi (tỉ lệ, góc) trong lưới quanh ước lượng, xoay + co bản đồ lớp của mảnh rồi tương quan FFT với bản đồ lớp của concept theo
từng lớp (điểm = số điểm ảnh trùng lớp − phạt điểm ảnh rơi vào nền trắng), chỉ xét vị trí trong cửa sổ quanh chỗ ước lượng;
tìm thô ở 1/4 rồi tinh ở 1/2. Ra inbox/tm07_<k>/khop.json {tên: s, r, cx, cy, diem} (s = px concept / px mảnh, r độ ngược kim
đồng hồ trên màn hình, cx cy tâm mảnh trên concept) và so_ghep.png (mảnh dán lên concept theo kết quả).

    py -3 -I ArtGen/Spine/tm07_khop.py 2 [tên mảnh ...]
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "inbox")

# bảng màu (tên, RGB, trọng số khớp)
MAU = [("cham", (58, 74, 156), 1.0), ("nga", (244, 236, 216), 1.0), ("do", (217, 68, 58), 1.0), ("hong", (238, 138, 128), 1.0),
       ("vang", (232, 182, 74), 1.0), ("cyan", (69, 207, 224), 1.0), ("ruou", (139, 47, 69), 1.0), ("lam_dam", (30, 104, 190), 0.6),
       ("lam", (58, 150, 226), 0.6), ("lam_nhat", (140, 208, 246), 0.6), ("muc", (43, 33, 24), 0.3), ("peri", (143, 167, 230), 1.0),
       ("kem", (247, 240, 223), 1.0), ("hong_nhat", (243, 181, 174), 1.0), ("vang_nhat", (241, 210, 122), 1.0), ("trang", (255, 255, 255), 0.0)]
NEN = len(MAU) - 1   # lớp nền trắng


def lop(rgb, alpha=None, mo=2):
    """bản đồ lớp màu (nearest trong bảng) sau khi làm mờ hộp bán kính mo (gộp vân chì sáp vào màu tô, chỉ còn viền mực là
    lớp mực); alpha < 128 -> -1."""
    from PIL import ImageFilter
    im = Image.fromarray(np.asarray(rgb, np.uint8))
    if mo:
        im = im.filter(ImageFilter.BoxBlur(mo))
    a = np.asarray(im, np.int32)           # int32: bình phương hiệu màu tới 65025 × 3, int16 tràn (lỗi đã gặp: trắng thành "do")
    anc = np.array([m[1] for m in MAU], np.int32)
    d = ((a[..., None, :] - anc[None, None, :, :]) ** 2).sum(-1)
    L = np.argmin(d, axis=-1).astype(np.int16)
    if alpha is not None:
        L[alpha < 128] = -1
    return L


def _onehot(L, k):
    return (L == k).astype(np.float32)


def _xoay_co(L, s, r):
    """bản đồ lớp (int16, -1 ngoài) co s và xoay r độ (ngược kim trên màn hình), nearest."""
    im = Image.fromarray((L + 1).astype(np.uint8))
    w, h = im.size
    im = im.resize((max(1, int(round(w * s))), max(1, int(round(h * s)))), Image.NEAREST)
    im = im.rotate(r, resample=Image.NEAREST, expand=True, fillcolor=0)
    return np.asarray(im).astype(np.int16) - 1


MUC = [i for i, m in enumerate(MAU) if m[0] == "muc"][0]
MU = 1.0   # trọng số phần nét mực (viền phải trùng viền: chống phóng to lấn sang vùng cùng màu)


def _corr(FCk, P, shape):
    H, W = shape
    pad = np.zeros((H, W), np.float32)
    pad[:P.shape[0], :P.shape[1]] = P
    return np.fft.irfft2(FCk * np.conj(np.fft.rfft2(pad)), s=(H, W))


def _tuong_quan(FC, Lp, shape, lam=1.0):
    """điểm số theo vị trí tâm mảnh = (Σ_k w_k corr(C_k, P_k) − lam·corr(C_nền, P_có hình)) / diện tích tô
    + MU · corr(C_mực giãn, P_mực) / số điểm mực của mảnh. Phần tô là độ chính xác (không thưởng phóng to), phần mực
    bắt viền mảnh trùng viền concept (không thưởng thu nhỏ lọt trong vùng cùng màu)."""
    H, W = shape
    h, w = Lp.shape
    tot = np.zeros((H, W), np.float32)
    n_fill = 0
    for k, (_, _, wk) in enumerate(MAU):
        if k in (NEN, MUC):
            continue
        Pk = _onehot(Lp, k)
        nk = int(Pk.sum())
        if not nk:
            continue
        n_fill += nk
        tot += wk * _corr(FC[k], Pk, shape)
    tot -= lam * _corr(FC[NEN], ((Lp >= 0) & (Lp != MUC)).astype(np.float32), shape)
    tot /= max(1, n_fill)
    Pm = _onehot(Lp, MUC)
    nm = int(Pm.sum())
    if nm:
        tot += MU * _corr(FC["muc_gian"], Pm, shape) / nm
    return tot, (w / 2, h / 2)


def khop(C, Lp_full, s0, r0, c0, ds=(0.72, 1.35, 9), dr=(-28, 28, 15), win=140, lam=1.0, ten=""):
    """dò (s, r, cx, cy) cho mảnh có bản đồ lớp Lp_full (đủ cỡ) trên concept lớp C (đủ cỡ). Thô 1/4 rồi tinh 1/2."""
    best = None
    for f, S_, R_, W_ in ((4, np.linspace(ds[0], ds[1], ds[2]), np.linspace(dr[0], dr[1], dr[2]), win),
                          (2, None, None, 28)):
        Cs = np.asarray(Image.fromarray((C + 1).astype(np.uint8)).resize((C.shape[1] // f, C.shape[0] // f), Image.NEAREST)).astype(np.int16) - 1
        H, W = Cs.shape
        FC = {k: np.fft.rfft2(_onehot(Cs, k)) for k in range(len(MAU))}
        m = _onehot(Cs, MUC)
        g = m.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                g = np.maximum(g, np.roll(np.roll(m, dy, 0), dx, 1))
        FC["muc_gian"] = np.fft.rfft2(g)
        if S_ is None:
            S_ = np.linspace(best[0] * 0.93, best[0] * 1.07, 5)
            R_ = np.linspace(best[1] - 5, best[1] + 5, 5)
            cx0, cy0 = best[2], best[3]
        else:
            S_, R_ = S_ * s0, R_ + r0
            cx0, cy0 = c0
        yy, xx = np.mgrid[0:H, 0:W]
        cand = None
        for s in S_:
            for r in R_:
                Lp = _xoay_co(Lp_full, s / f, r)
                if Lp.shape[0] >= H or Lp.shape[1] >= W:
                    continue
                tot, (hw, hh) = _tuong_quan(FC, Lp, (H, W), lam)
                cx = (xx + hw) * f
                cy = (yy + hh) * f
                ok = (np.abs(cx - cx0) <= W_) & (np.abs(cy - cy0) <= W_)
                # tiên nghiệm yếu: xa ước lượng (tỉ lệ, góc, vị trí) thì trừ nhẹ, chỉ bằng chứng rõ mới kéo đi
                prior = 0.25 * abs(math.log(s / s0)) + 0.004 * abs(r - r0) + 0.12 * np.hypot(cx - c0[0], cy - c0[1]) / max(1, win)
                sc = np.where(ok, tot - prior, -1e9)
                i = int(np.argmax(sc))
                v = float(sc.flat[i])
                if cand is None or v > cand[4]:
                    cand = (float(s), float(r), float(cx.flat[i]), float(cy.flat[i]), v, 1)
        if cand is None:
            raise RuntimeError(f"{ten}: không có ứng viên")
        best = (cand[0], cand[1], cand[2], cand[3], cand[4])
        area = cand[5]
    diem = best[4]   # độ chính xác tô (−1..1) + MU · tỉ lệ nét mực trùng (0..1)
    print(f"  {ten:10s} s={best[0]:.3f} r={best[1]:+.1f} tâm=({best[2]:.0f}, {best[3]:.0f}) điểm={diem:.2f}")
    return dict(s=round(best[0], 4), r=round(best[1], 2), cx=round(best[2], 1), cy=round(best[3], 1), diem=round(diem, 3))


def so_ghep(con, pieces, kq, ra):
    """dán mảnh lên concept (mờ 0,55) theo kết quả."""
    out = con.convert("RGBA").copy()
    lay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    for nm, (im, _) in pieces.items():
        if nm not in kq:
            continue
        q = kq[nm]
        p = im.resize((max(1, int(im.width * q["s"])), max(1, int(im.height * q["s"]))), Image.LANCZOS).rotate(q["r"], expand=True, resample=Image.BICUBIC)
        a = p.getchannel("A").point(lambda v: int(v * 0.6))
        p.putalpha(a)
        lay.alpha_composite(p, (int(q["cx"] - p.width / 2), int(q["cy"] - p.height / 2)))
    out.alpha_composite(lay)
    out.convert("RGB").save(ra)


def chay(k, uoc, chi=None):
    """uoc = {tên: (s0, r0, (cx, cy), tuỳ chọn dict ds/dr/win)}: ước lượng ban đầu (concept px)."""
    base = os.path.join(INBOX, f"tm07_{k}")
    con = Image.open(os.path.join(base, "tai_ve", "L1_duyet.png")).convert("RGB")
    C = lop(np.asarray(con))
    pj = os.path.join(base, "khop.json")
    kq = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else {}
    pieces = {}
    for nm, spec in uoc.items():
        p = os.path.join(base, "manh", nm + ".png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        pieces[nm] = (im, spec)
    for nm, (im, spec) in pieces.items():
        if chi and nm not in chi:
            continue
        a = np.asarray(im)
        Lp = lop(a[..., :3], a[..., 3])
        opt = spec[3] if len(spec) > 3 else {}
        kq[nm] = khop(C, Lp, spec[0], spec[1], spec[2], ten=nm, **opt)
    json.dump(kq, open(pj, "w", encoding="utf-8"), indent=1)
    so_ghep(con, pieces, kq, os.path.join(base, "so_ghep.png"))
    print("  ->", pj, "|", os.path.join(base, "so_ghep.png"))
    return kq


# ước lượng ban đầu (concept px, góc ngược kim trên màn hình, tâm mảnh)
UOC = {
    2: {"dau": (0.66, 10, (1190, 420), dict(ds=(0.82, 1.15, 8), dr=(-12, 12, 7), win=70)),
        "nga": (0.62, 32, (1330, 250), dict(ds=(0.95, 1.05, 3), dr=(-10, 10, 9), win=50)),
        "vay_lung": (0.66, 0, (500, 320), dict(ds=(0.95, 1.05, 3), dr=(-12, 12, 7), win=50)),
        "than": (0.62, -4, (760, 600), dict(ds=(0.7, 1.4, 10), dr=(-14, 14, 8), win=90)),
        "cuong": (0.45, 42, (290, 525), dict(ds=(0.5, 1.6, 9))),
        "vay_duoi": (0.6, 4, (219, 376), dict(ds=(0.85, 1.2, 6), dr=(-12, 12, 7), win=60)),
        "vay_cheo": (0.46, -75, (770, 715), dict(ds=(0.85, 1.25, 6), dr=(-22, 22, 9), win=70)),
        "sen_sau": (0.40, 0, (775, 360), dict(ds=(0.92, 1.08, 5), dr=(-6, 6, 5), win=40)),
        "sen_truoc": (0.46, 0, (770, 405), dict(ds=(0.92, 1.08, 5), dr=(-6, 6, 5), win=40)),
        "dai": (0.37, 0, (770, 325), dict(ds=(0.9, 1.1, 5), dr=(-6, 6, 3), win=30)),
        "ham": (0.5, -10, (1250, 470), dict(ds=(0.8, 1.2, 7), dr=(-25, 15, 9), win=60))},
    1: {"dau": (0.78, 2, (938, 488), dict(ds=(0.97, 1.03, 3), dr=(-6, 6, 5), win=16)),
        "nga": (0.38, 35, (1035, 335), dict(ds=(0.85, 1.2, 6), dr=(-15, 15, 7), win=50)),
        "vay_lung": (0.45, 0, (598, 342), dict(ds=(0.95, 1.05, 3), dr=(-12, 12, 7), win=14)),
        "than": (0.95, 0, (712, 548), dict(ds=(0.97, 1.03, 3), dr=(-5, 5, 3), win=16)),
        "cuong": (0.35, 70, (448, 505), dict(ds=(0.7, 1.4, 8), dr=(-30, 30, 13), win=50)),
        "vay_duoi": (0.4, -8, (455, 425), dict(ds=(0.85, 1.2, 6), dr=(-15, 15, 7), win=50)),
        "vay_cheo": (0.33, -65, (735, 695), dict(ds=(0.85, 1.25, 6), dr=(-22, 22, 9), win=60)),
        "de_nu": (0.6, 0, (732, 356), dict(ds=(0.95, 1.05, 3), dr=(-6, 6, 3), win=12)),
        "nu_sau": (0.62, 0, (738, 262), dict(ds=(0.9, 1.1, 5), dr=(-8, 8, 5), win=40)),
        "nu_truoc": (0.68, 0, (742, 290), dict(ds=(0.9, 1.1, 5), dr=(-8, 8, 5), win=40))},
}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = int(sys.argv[1])
    chay(k, UOC[k], sys.argv[2:] or None)
