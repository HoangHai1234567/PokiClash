# -*- coding: utf-8 -*-
"""Dòng tm08 Uyên Xà (rắn vực sâu), lô 10 tướng mới đảo Thủy: cắt tờ mảnh, dò khớp mảnh vào concept, rig bằng thư viện quai,
clip, xuất .atomik. Thiết kế và phân tích: inbox/tm08_ghichu.md; gói GPT: build_tm08.py.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm08.py cat 2        cắt tờ M01, M02 -> inbox/tm08_2/manh/
    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm08.py place 2      dò khớp mảnh vào concept (cv2) -> rig/place.json, so_ghep.png
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- D:/spine-venv/Scripts/python -I ArtGen/Spine/tm08.py rig 2
    ... all                                                         dạng 2 rồi dạng 1 (gộp tiến hóa)

Thân: ống duỗi thẳng GPT vẽ được nắn theo đường giữa đọc từ concept (bề dày từng đoạn và chiều dài khớp concept), rồi uốn
thành chữ S của concept bằng toạ độ thế giới từng đỉnh (lưới dải, trọng số B-spline trên chuỗi xương hai phía từ xương `than`
đặt ở chỗ thân chạm đất). Đầu phóng 1,35 lần quanh gáy (người dùng chốt), hàm dưới hai xương, lòng miệng theo hàm, mí dò phủ
kín, râu đèn dây mềm, vây ngực lò xo, vây đuôi hai đốt, mặt nạ cắt ở mặt đất cho appear (trồi) và die (chìm).
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, DayMem, LoXo, an_hien, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat, Pose  # noqa: E402

CODE = "tm08"
TI = 0.8            # pixel rig = pixel concept × TI; ảnh mảnh (vẽ ở cỡ concept) co TI lúc nạp (đặt lại theo dạng trong dung())
TI_K = {2: 0.8, 1: 0.58}   # dạng 1 gộp cả dạng 2 nên atlas nhỏ hơn cho .atomik ≤ 0,5 MB
B_VIEN, B_TRONG = 11.0, 15.0


def inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


# đọc trên concept (pixel ảnh, y xuống): đường giữa ống thân từ gáy tới chóp đuôi (nắn lại tự động theo mặt nạ thân), mặt đất,
# gốc x (chỗ thân chạm đất), vị trí ước của từng mảnh để dò khớp, số đốt
CFG = {
    2: dict(ten="Uyên Xà", path=[(1245, 232, 140), (1215, 300, 150), (1195, 390, 165), (1205, 500, 175), (1225, 600, 180), (1175, 700, 185), (1090, 790, 180),
                                 (990, 830, 170), (880, 740, 180), (780, 660, 190), (700, 632, 190), (600, 655, 185), (500, 705, 165),
                                 (400, 780, 150), (300, 830, 135), (220, 877, 95), (155, 888, 60)],
            ground=905, dinh=50, ox=1000, N=14, c_s=0.42, hk=1.3, c_s_ground=True, ham_px=(0.60, 0.78), ham_s=0.66, ham_r=8.0,
            duoi_vay=(88.0, 0.72),
            fit={"dau": ((1330, 190), 170, (0.55, 1.3), (-25, 25)), "ham": ((1400, 265), 110, (0.5, 1.1), (-25, 25)),
                 "duoi_vay": ((150, 720), 160, (0.5, 1.3), (-60, 60))},
            grid1=[["dau", "ham", ("mieng", "luoi")], [("mi", "vay_nguc"), "rau", "duoi_vay"]],
            rau_n=5, rau_goc=-118, rau_dai=0.5, vay_s=0.08, vay_ti=0.42, vay_u=0.30, bk_amp=[1.0, 1.3, 1.6, 2.0, 2.3, 2.6, 2.8, 3.0], T_idle=4.0),
    1: dict(ten="Uyên Nhi", path=[(1010, 470, 260), (1000, 560, 300), (975, 680, 340), (940, 790, 340), (870, 890, 270), (750, 950, 150), (620, 950, 85),
                                  (495, 900, 70), (415, 835, 55)], do_day=False,
            ground=985, dinh=55, ox=800, N=8, c_s=0.55, hk=1.0, c_s_ground=True, ham_px=(0.57, 0.70), ham_s=0.5, ham_r=-4.0,
            duoi_vay=(150.0, 0.72), mao=(1015, 435, 12.0, 1.2), than_cong_chinh=(0, 0, 1.0),
            fit={"dau": ((1100, 410), 200, (0.6, 1.2), (-25, 25)), "ham": ((1190, 535), 110, (0.5, 1.2), (-25, 25)),
                 "duoi_vay": ((330, 790), 130, (0.6, 1.4), (-60, 60)), "mao": ((900, 250), 220, (0.5, 1.3), (-35, 35)),
                 "than_cong": ((840, 760), 220, (0.8, 1.25), (-12, 12))},
            grid1=[["dau", "ham", ("mieng", "luoi")], [("mi", "vay_nguc"), "mao", ("rau", "duoi_vay")]],
            rau_n=3, rau_goc=-100, rau_dai=0.6, vay_s=0.42, vay_ti=0.55, vay_u=0.05, vay_goc=-35.0, bk_amp=[1.5, 2.2, 3.0, 3.8], T_idle=4.0),
}

GIU_CHO = {"dau": ("bo", 430, 300, (46, 47, 110)), "ham": ("ham", 300, 110, (216, 243, 234)), "mieng": ("mieng", 220, 150, (90, 42, 94)),
           "luoi": ("luoi", 230, 48, (197, 106, 154)), "mi": ("mi", 120, 76, (46, 47, 110)), "vay_nguc": ("giot", 250, 130, (143, 227, 208)),
           "rau": ("luoi", 430, 30, (46, 47, 110)), "duoi_vay": ("tron", 330, 330, (143, 227, 208)), "than_w": ("dai", 1500, 260, (46, 47, 110)),
           "mao": ("giot", 400, 330, (143, 227, 208)), "vay_lung": ("dai", 1450, 170, (143, 227, 208)),
           "than_cong": ("tron", 1000, 850, (80, 88, 168))}


# ---------------------------------------------------------------- cắt tờ
def gan_o2(to, grid):
    """gán theo ô 3×2; ô có hai mảnh (tuple) gán theo thứ tự trên → dưới."""
    R = len(grid)
    o = {}
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        r = min(R - 1, int(cy / (to.h / R)))
        c = min(len(grid[r]) - 1, int(cx / (to.w / len(grid[r]))))
        o.setdefault((r, c), []).append(m)
    out = {}
    for (r, c), ms in o.items():
        nm = grid[r][c]
        ms = sorted(ms, key=lambda m: -m["dt"])
        if isinstance(nm, tuple):
            big = sorted(ms[:len(nm)], key=lambda m: (m["y0"] + m["y1"]) / 2)
            for n, m in zip(nm, big):
                out[n] = m
            if len(ms) > len(nm):
                print(f"  ô {r},{c} thừa {len(ms) - len(nm)} mảnh")
        elif nm:
            out[nm] = ms[0]
            if len(ms) > 1:
                print(f"  ô {r},{c} ({nm}) thừa {len(ms) - 1} mảnh: " + ", ".join(f"{m['x1'] - m['x0']}x{m['y1'] - m['y0']}" for m in ms[1:]))
    return out


def cat(k):
    cfg = CFG[k]
    tv, md = os.path.join(inbox(k), "tai_ve"), os.path.join(inbox(k), "manh")
    os.makedirs(md, exist_ok=True)
    p1, p2 = anh.to_moi_nhat(tv, "M01"), anh.to_moi_nhat(tv, "M02")
    names = []
    if p1:
        to = anh.doc_to(p1)
        g = gan_o2(to, cfg["grid1"])
        thieu = [n for row in cfg["grid1"] for nn in row for n in (nn if isinstance(nn, tuple) else (nn,)) if n not in g]
        if thieu:
            print("  M01 THIẾU mảnh:", thieu)
        anh.luu_manh(to, g, md)
        names += list(g)
    if p2:
        to = anh.doc_to(p2, dien_tich_min=20000)
        m = max(to.manh, key=lambda q: q["dt"])
        anh.luu_manh(to, {"than": m}, md)
        names.append("than")
        if len(to.manh) > 1:
            print(f"  M02 có {len(to.manh)} mảnh, lấy mảnh lớn nhất {m['x1'] - m['x0']}x{m['y1'] - m['y0']}")
    p3 = anh.to_moi_nhat(tv, "M03")
    if p3:   # lượt 3: dạng 2 vây lưng gợn rời, dạng 1 thân cong đúng dáng
        to = anh.doc_to(p3, dien_tich_min=20000)
        m = max(to.manh, key=lambda q: q["dt"])
        nm3 = "vay_lung" if k == 2 else "than_cong"
        anh.luu_manh(to, {nm3: m}, md)
        names.append(nm3)
    anh.to_soi(md, names)
    print("  ->", md)


# ---------------------------------------------------------------- đường giữa thân trên concept
def mat_na_than(rgb):
    """mặt nạ ống thân trên concept / tờ: chàm (xanh tím sẫm) + bụng bạc hà nhạt + mực; KHÔNG lấy vây bạc hà bão hoà."""
    r, g, b = [rgb[..., i].astype(int) for i in range(3)]
    lum = (r + g + b) / 3
    white = (np.minimum(np.minimum(r, g), b) > 236)
    indigo = (b > r + 18) & (lum < 170) & (b >= g - 6)      # chàm: b > g; nét sáp bạc hà sẫm có g > b nên không lẫn
    ink = lum < 95
    belly = (lum > 190) & ~white & (np.abs(g - b) < 40) & (g >= r) & ((g - r) < 60)
    fin = (g > r + 45) & (g > b + 8) & (lum < 215) & ~indigo
    return (indigo | ink | belly) & ~fin, indigo, fin


def duong_giua(concept_rgb, path, n_mau=200, do_day=True):
    """đường giữa ống thân: điểm đọc tay (x, y, dày ước) nối mượt (lấy mẫu đều, làm mượt); bề dày tại mỗi mẫu = đoạn mặt nạ thân
    (không kể vây) cắt bởi pháp tuyến trong tầm ±0,8 dày ước, chặn về [0,75; 1,3] dày ước rồi lọc trung vị (tự dò hoàn toàn thì
    đường dò lạc sang vây ngực, đầu, bụng mập: đã thử, bỏ). Trả (đường (M, 2), dày (M,)) pixel concept."""
    _, _, fin = mat_na_than(concept_rgb)
    white = concept_rgb.min(axis=2) > 236
    m = ~white & ~anh.gian(fin, 1)     # cả con trừ vây (bạc hà bão hoà); chấm đèn thành lỗ -> lấp
    m = anh.lap_lo(anh.mo_mo(m, 2), 6000)
    H, W = m.shape
    P = np.asarray([(p[0], p[1]) for p in path], float)
    D0 = np.asarray([p[2] for p in path], float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    s = np.linspace(0, d[-1], n_mau)
    Q = np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1)
    for _ in range(7):
        Q[1:-1] = 0.25 * Q[:-2] + 0.5 * Q[1:-1] + 0.25 * Q[2:]
    prior = np.interp(s, d, D0)
    # bán kính cong phải ≥ 1,2 × nửa bề dày ở mọi chỗ (dải lưới không tự gập đè ở đáy chữ U): làm mượt thêm tới khi đạt
    for lan in range(400):
        dd = np.gradient(Q, axis=0)
        ds = np.hypot(*dd.T)
        d2 = np.gradient(dd, axis=0)
        kap = np.abs(dd[:, 0] * d2[:, 1] - dd[:, 1] * d2[:, 0]) / np.maximum(ds ** 3, 1e-9)
        R = 1.0 / np.maximum(kap, 1e-9)
        ti_so = R / np.maximum(1.0, prior / 2)
        if ti_so.min() >= 1.5:
            break
        xau = ti_so < 1.5
        xau = np.convolve(xau.astype(float), np.ones(9), mode="same") > 0
        Qs = Q.copy()
        Qs[1:-1] = 0.25 * Q[:-2] + 0.5 * Q[1:-1] + 0.25 * Q[2:]
        Q[xau] = Qs[xau]
    print(f"  đường giữa: làm mượt thêm {lan} lần, R / nửa dày nhỏ nhất {ti_so.min():.2f}")
    tg = np.gradient(Q, axis=0)
    tg /= np.maximum(1e-9, np.hypot(*tg.T))[:, None]
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    thick = prior.copy()
    for i in (range(len(Q)) if do_day else ()):
        R = 0.8 * prior[i]
        rr = np.arange(-R, R + 1, 1.0)
        pts = Q[i] + rr[:, None] * nr[i]
        x, y = np.clip(pts[:, 0].astype(int), 0, W - 1), np.clip(pts[:, 1].astype(int), 0, H - 1)
        ins = m[y, x]
        k0 = len(rr) // 2
        if not ins[k0]:
            continue
        a = k0
        while a > 0 and ins[a - 1]:
            a -= 1
        b = k0
        while b < len(rr) - 1 and ins[b + 1]:
            b += 1
        thick[i] = min(1.3 * prior[i], max(0.75 * prior[i], rr[b] - rr[a]))
    thick = np.array([np.median(thick[max(0, i - 6):i + 7]) for i in range(len(thick))])
    thick = np.convolve(np.pad(thick, 3, mode="edge"), np.ones(7) / 7, mode="valid")
    return Q, thick


def lay_mau_duong(Q, thick, s):
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(Q, axis=0).T))]
    s = np.clip(s, 0, d[-1])
    p = np.stack([np.interp(s, d, Q[:, 0]), np.interp(s, d, Q[:, 1])], -1)
    t = np.interp(s, d, thick)
    return p, t, d[-1]


# ---------------------------------------------------------------- nắn ống thân theo bề dày concept
def nan_ong(im, thick_fn, dai_moi, pad=6, bo_vay=False, cat_chom=(0.0, 0.0)):
    """ống GPT (thẳng, nằm ngang, gốc trái) -> ảnh mới dài dai_moi px, bề dày ống (phần không kể vây lưng) tại mỗi cột bằng
    thick_fn(s) (s px từ mép trái). Vây lưng giữ nguyên chiều cao, dồn lên trên. Trả (ảnh, hàng trục YC, x trái)."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    H, W = a.shape[:2]
    al = a[..., 3] > 40
    cols = np.flatnonzero(al.any(axis=0))
    x0, x1 = int(cols[0]), int(cols[-1]) + 1
    _, indigo, _ = mat_na_than(a[..., :3].astype(np.uint8))
    indigo &= al
    top_al = np.array([np.flatnonzero(al[:, x])[0] if al[:, x].any() else 0 for x in range(W)], float)
    bot_al = np.array([np.flatnonzero(al[:, x])[-1] + 1 if al[:, x].any() else 0 for x in range(W)], float)
    top_in = np.array([np.flatnonzero(indigo[:, x])[0] if indigo[:, x].any() else 1e9 for x in range(W)], float)
    # mép trên ống: chấm đèn bạc hà tạo nhát cao xuống -> lọc cực tiểu cửa sổ rồi trung vị; hai mép ngoài lọc trung vị
    def med(v, r=9):
        return np.array([np.median(v[max(0, i - r):i + r + 1]) for i in range(len(v))])
    def mn(v, r=30):
        return np.array([v[max(0, i - r):i + r + 1].min() for i in range(len(v))])
    # mép trên ống và mép dưới trên tờ gần thẳng: khớp đa thức bậc 2 bền (loại điểm lạc: chấm đèn, nét tia, chỏm tròn hai đầu)
    def fit_ben(v, ok, deg=2, lan=4):
        xa = np.arange(W, dtype=float)
        x, y = xa[ok], v[ok]
        m = np.ones(len(x), bool)
        c = None
        for _ in range(lan):
            c = np.polyfit(x[m], y[m], deg)
            r = y - np.polyval(c, x)
            sd = 1.4826 * np.median(np.abs(r[m])) + 1e-6
            m = np.abs(r) < max(3.0, 2.5 * sd)
        return np.polyval(c, xa)
    ok_in = top_in < 1e8
    inner = np.zeros(W, bool)
    inner[x0 + int(0.06 * (x1 - x0)):x1 - int(0.06 * (x1 - x0))] = True
    top_in = fit_ben(top_in, ok_in & inner)
    bot_al = fit_ben(bot_al, al.any(axis=0) & inner)
    top_al = med(top_al, 3)
    top_in = np.maximum(top_in, top_al + 2)
    bot_al = np.maximum(bot_al, top_in + 8)
    # cắt phẳng hai chỏm tròn (dải lưới của thư viện chưa có mũ tròn -> hở): hai đầu đều khuất sau đầu / gốc vây đuôi
    xa0, xa1 = x0 + cat_chom[0] * (x1 - x0), x1 - cat_chom[1] * (x1 - x0)
    Wn = int(round(dai_moi)) + 2 * pad
    xs = xa0 + (np.arange(Wn) - pad) / max(1.0, dai_moi) * (xa1 - xa0)
    xs = np.clip(xs, xa0, xa1 - 1)
    T = np.array([max(8.0, float(thick_fn(X - pad))) for X in range(Wn)])
    tube_src = np.interp(xs, np.arange(W), bot_al - top_in)
    hs = np.interp(xs, np.arange(W), top_in - top_al)         # cao vây tờ
    tin, tal, bal = np.interp(xs, np.arange(W), top_in), np.interp(xs, np.arange(W), top_al), np.interp(xs, np.arange(W), bot_al)
    hs = hs * T / np.maximum(8.0, tube_src)                   # vây cao theo cùng tỉ lệ ống (concept vây ~0,6 ống)
    if bo_vay:
        hs = np.zeros_like(hs)                                 # vây lưng là mảnh riêng (M03)
    Hs_max, T_max = float(hs.max()), float(T.max())
    YC = int(Hs_max + T_max / 2 + pad)
    Hn = int(YC + T_max / 2 + pad)
    out = np.zeros((Hn, Wn, 4), np.float32)
    rows = np.arange(Hn, dtype=np.float32)
    for X in range(Wn):
        xsrc = xs[X]
        xi = int(np.floor(xsrc))
        fx = xsrc - xi
        colA = a[:, min(W - 1, xi)]
        colB = a[:, min(W - 1, xi + 1)]
        col = colA * (1 - fx) + colB * fx
        t_top, t_bot = YC - T[X] / 2, YC + T[X] / 2
        s_top = t_top - hs[X]
        ysrc = np.full(Hn, -1.0, np.float32)
        r1 = (rows >= s_top) & (rows < t_top)
        ysrc[r1] = tal[X] + (rows[r1] - s_top) / max(1e-6, hs[X]) * (tin[X] - tal[X])
        r2 = (rows >= t_top) & (rows <= t_bot)
        ysrc[r2] = tin[X] + (rows[r2] - t_top) / max(1e-6, T[X]) * (bal[X] - tin[X])
        ok = ysrc >= 0
        yi = np.clip(np.floor(ysrc[ok]).astype(int), 0, H - 2)
        fy = (ysrc[ok] - yi)[:, None]
        out[ok, X] = col[yi] * (1 - fy) + col[yi + 1] * fy
        # ngoài hình: alpha 0
        edge = ok & ((rows < s_top + 1.5) | (rows > t_bot - 1.5))
        out[edge, X, 3] *= 0.6
    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA"), YC, pad


# ---------------------------------------------------------------- dò khớp mảnh vào concept (cv2)
def _cv2():
    import cv2
    return cv2


def warp(rgba, s, r):
    cv2 = _cv2()
    h, w = rgba.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), r, s)
    c, si = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * si + w * c) + 2, int(h * c + w * si) + 2
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    return cv2.warpAffine(rgba, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def match(ref_lab, part, scales, rots, f, around, win, ref_dt=None, w_ink=420.0):
    """điểm = SQDIFF màu Lab có mặt nạ / diện tích + w_ink × khoảng cách trung bình từ nét mực của mảnh tới nét mực concept
    (ref_dt: distance transform của nét mực concept; chặn SQDIFF thiên về mẫu nhỏ)."""
    cv2 = _cv2()
    best = None
    R = cv2.resize(ref_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    DT = cv2.resize(ref_dt, None, fx=f, fy=f, interpolation=cv2.INTER_AREA) * f if ref_dt is not None else None
    for s in scales:
        for r in rots:
            wp = warp(part, s * f, r)
            if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                continue
            m = (wp[:, :, 3] > 200).astype(np.float32)
            area = m.sum()
            if area < 20:
                continue
            t = cv2.cvtColor(np.ascontiguousarray(wp[:, :, :3]), cv2.COLOR_RGB2LAB).astype(np.float32)
            res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m])) / area
            if DT is not None:
                ink = ((wp[:, :, :3].astype(int).sum(axis=2) < 300) & (wp[:, :, 3] > 200)).astype(np.float32)
                n_ink = ink.sum()
                if n_ink >= 8:
                    md = cv2.matchTemplate(DT, ink, cv2.TM_CCORR) / n_ink
                    res = res + w_ink * md / f
            th, tw = wp.shape[:2]
            ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
            cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
            bad = (np.abs(cx - around[0]) > win) | (np.abs(cy - around[1]) > win)
            res = np.where(bad, np.inf, res)
            mn, _, loc, _ = cv2.minMaxLoc(res)
            if not np.isfinite(mn):
                continue
            if best is None or mn < best[0]:
                best = (float(mn), float(s), float(r), (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def place(k):
    """dò (tỉ lệ, góc, tâm) của từng mảnh trên concept (tờ mảnh cùng cỡ concept nên tỉ lệ quanh 1): thô f=0,25 rồi tinh f=0,5, 1."""
    cv2 = _cv2()
    cfg = CFG[k]
    ref = np.asarray(Image.open(os.path.join(inbox(k), "tai_ve", "L1_duyet.png")).convert("RGB"))
    ref_lab = cv2.cvtColor(ref, cv2.COLOR_RGB2LAB).astype(np.float32)
    ink = (ref.astype(int).sum(axis=2) < 300).astype(np.uint8)
    ref_dt = cv2.distanceTransform(1 - ink, cv2.DIST_L2, 3).astype(np.float32)
    md, rd = os.path.join(inbox(k), "manh"), os.path.join(inbox(k), "rig")
    os.makedirs(rd, exist_ok=True)
    out = {}
    for nm, (around, win, (s0, s1), (r0, r1)) in cfg["fit"].items():
        p = os.path.join(md, nm + ".png")
        if not os.path.exists(p):
            print(f"  {nm}: chưa có mảnh, bỏ qua")
            continue
        part = np.asarray(Image.open(p).convert("RGBA"))
        if nm == "ham" and "dau" in out:   # hàm nằm dưới nửa trước đầu
            d = out["dau"]
            dw, dh = Image.open(os.path.join(md, "dau.png")).size
            around, win = (d["cx"] + 0.12 * dw * d["s"], d["cy"] + 0.36 * dh * d["s"]), 60
        t0 = time.time()
        c = match(ref_lab, part, np.arange(s0, s1 + 1e-6, 0.05), np.arange(r0, r1 + 1e-6, 5), 0.25, around, win, ref_dt)
        if c is None:
            print(f"  {nm}: không dò được")
            continue
        c = match(ref_lab, part, np.arange(c[1] * 0.94, c[1] * 1.061, c[1] * 0.02), np.arange(c[2] - 5, c[2] + 5.1, 2.5), 0.5, (c[3], c[4]), 40, ref_dt)
        c = match(ref_lab, part, np.arange(c[1] * 0.98, c[1] * 1.021, c[1] * 0.01), np.arange(c[2] - 2, c[2] + 2.1, 1), 1.0, (c[3], c[4]), 12, ref_dt)
        out[nm] = {"s": c[1], "r": c[2], "cx": c[3], "cy": c[4], "err": c[0]}
        print(f"  {nm}: tỉ lệ {c[1]:.3f} góc {c[2]:+.1f} tâm ({c[3]:.0f}, {c[4]:.0f}) sai {c[0]:.0f} ({time.time() - t0:.1f} s)")
    with open(os.path.join(rd, "place.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    # ảnh so: mảnh đặt lên concept mờ
    base = Image.fromarray(ref).convert("RGBA")
    base = Image.blend(base, Image.new("RGBA", base.size, (255, 255, 255, 255)), 0.55)
    for nm, c in out.items():
        part = np.asarray(Image.open(os.path.join(md, nm + ".png")).convert("RGBA"))
        wp = Image.fromarray(warp(part, c["s"], c["r"]))
        base.alpha_composite(wp, (int(c["cx"] - wp.width / 2), int(c["cy"] - wp.height / 2)))
    base.convert("RGB").save(os.path.join(rd, "so_ghep.png"))
    print("  ->", os.path.join(rd, "so_ghep.png"))
    return out


# ---------------------------------------------------------------- dựng rig
def toa_do(cfg):
    ox, gy = cfg["ox"], cfg["ground"]

    def to_rig(p):
        p = np.asarray(p, float)
        return np.stack([(p[..., 0] - ox) * TI, (gy - p[..., 1]) * TI], -1)

    def to_concept(q):
        q = np.asarray(q, float)
        return np.stack([q[..., 0] / TI + ox, gy - q[..., 1] / TI], -1)
    return to_rig, to_concept


def vung_tron(im, tam, r):
    h, w = im.height, im.width
    yy, xx = np.mgrid[0:h, 0:w]
    return (xx - tam[0]) ** 2 + (yy - tam[1]) ** 2 < r * r


def diem_mep(im, phia="trai", ti=0.14, duoi=None):
    """trọng tâm của phần mảnh ở mép (gốc tròn của mảnh): phia trái/phải, ti phần bề rộng; duoi: chỉ lấy nửa dưới (tỉ lệ y từ)."""
    a = np.asarray(im)[..., 3] > 60
    h, w = a.shape
    cols = np.flatnonzero(a.any(axis=0))
    x0, x1 = cols[0], cols[-1] + 1
    sel = np.zeros_like(a)
    if phia == "trai":
        sel[:, x0:int(x0 + ti * (x1 - x0))] = True
    else:
        sel[:, int(x1 - ti * (x1 - x0)):x1] = True
    if duoi is not None:
        sel[:int(duoi * h), :] = False
    yy, xx = np.nonzero(a & sel)
    return float(xx.mean()), float(yy.mean())


def tam_mau(im, dk):
    """tâm các pixel thoả điều kiện màu dk(r, g, b) trên ảnh RGBA."""
    a = np.asarray(im).astype(int)
    m = (a[..., 3] > 60) & dk(a[..., 0], a[..., 1], a[..., 2])
    yy, xx = np.nonzero(m)
    if len(xx) < 10:
        return None
    return float(xx.mean()), float(yy.mean())


def dat_nguoc(dat, Pw, w, h):
    """pixel ảnh ứng với điểm thế giới Pw qua Dat (nghịch đảo Dat.ra)."""
    c, s = math.cos(math.radians(dat.goc)), math.sin(math.radians(dat.goc))
    dx, dy = Pw[0] - dat.x, Pw[1] - dat.y
    lx, ly = c * dx + s * dy, -s * dx + c * dy
    ax, ay = (dat.neo if dat.neo_px else (dat.neo[0] * w, dat.neo[1] * h))
    px = ax + lx / dat.sx * (-1 if dat.lat else 1)
    py = ay - ly / dat.sy
    return float(px), float(py)


def dung(k, ti=None):
    global TI
    TI = ti or TI_K[k]
    cfg = CFG[k]
    md, rd = os.path.join(inbox(k), "manh"), os.path.join(inbox(k), "rig")
    os.makedirs(rd, exist_ok=True)
    to_rig, to_concept = toa_do(cfg)
    hk = cfg["hk"]
    global B_VIEN, B_TRONG
    Hcon = (cfg["ground"] - cfg["dinh"]) * TI
    B_VIEN, B_TRONG = round(0.015 * Hcon, 1), round(0.02 * Hcon, 1)
    print(f"  bước lưới theo chiều cao {Hcon:.0f}: viền {B_VIEN}, trong {B_TRONG}")
    concept = np.asarray(Image.open(os.path.join(inbox(k), "tai_ve", "L1_duyet.png")).convert("RGB"))
    pl = {}
    pj = os.path.join(rd, "place.json")
    if os.path.exists(pj):
        pl = json.load(open(pj, encoding="utf-8"))
    # ---- đường giữa thân (concept px) và ống nắn
    Q, thick = duong_giua(concept, cfg["path"], do_day=cfg.get("do_day", True))
    _, _, Ltot_c = lay_mau_duong(Q, thick, 0.0)
    print(f"  thân: đường giữa {Ltot_c:.0f} px concept, dày gáy {thick[2]:.0f} / giữa {thick[len(thick) // 2]:.0f} / đuôi {thick[-3]:.0f}")
    than_p = os.path.join(md, "than.png")
    co_vl = k == 2 and os.path.exists(os.path.join(md, "vay_lung.png"))          # vây lưng gợn rời (M03)
    co_cong = k == 1 and os.path.exists(os.path.join(md, "than_cong.png")) and "than_cong" in pl   # thân cong đúng dáng (M03)
    if os.path.exists(than_p) and not co_cong:
        im_t = Image.open(than_p)
        imw, YC, padw = nan_ong(im_t, lambda s: lay_mau_duong(Q, thick, s)[1], Ltot_c, bo_vay=co_vl)
        imw.save(os.path.join(md, "than_w.png"))
        print(f"  ống nắn: {im_t.width}x{im_t.height} -> {imw.width}x{imw.height}, trục hàng {YC}" + (" (bỏ vây)" if co_vl else ""))
    else:
        YC, padw = None, 6
    pc = anh.nap_manh(md, GIU_CHO, ti_le=TI)
    sk = khung.Sk(f"{CODE}_{k}")
    bo_anh = {"than_cong"} if not co_cong else {"than_w"}
    if not co_vl:
        bo_anh.add("vay_lung")
    if k == 2:
        bo_anh.add("mao")
    for n, im in pc.items():
        if n not in bo_anh:
            sk.anh(n, im)
    N = cfg["N"]
    Lr = Ltot_c * TI
    seg = Lr / N
    s_j = np.arange(N + 1) * seg
    Jc, Tc, _ = lay_mau_duong(Q, thick, s_j / TI)
    J = to_rig(Jc)
    # chỉ số đốt chạm đất (gốc chuỗi): chỗ y nhỏ nhất quanh c_s
    c = int(round(cfg["c_s"] * N))
    if cfg.get("c_s_ground"):
        lo, hi = max(1, c - 2), min(N - 1, c + 2)
        c = int(lo + np.argmin(J[lo:hi + 1, 1]))
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("shadow", "root")
    sk.xuong("dat", "root")
    sk.xuong("than", "move", J[c, 0], J[c, 1], the_gioi=True, dai=20)
    fw = sk.chuoi("fw", "than", J[c::-1])          # than -> gáy
    bk = sk.chuoi("bk", "than", J[c:])             # than -> đuôi
    names_s = fw[::-1] + bk                        # theo s tăng (gáy -> đuôi)
    # pháp tuyến lưng và bán kính cong tại các khớp (để đặt xương vây lưng và co vây ở chỗ cong gắt)
    def phap_tuyen(s_arr):
        p0, _, _ = lay_mau_duong(Q, thick, np.asarray(s_arr) / TI)
        p1, _, _ = lay_mau_duong(Q, thick, (np.asarray(s_arr) + 4) / TI)
        tg_ = to_rig(p1) - to_rig(p0)
        tg_ /= np.maximum(1e-9, np.hypot(*tg_.T))[:, None]
        return tg_, np.stack([tg_[:, 1], -tg_[:, 0]], 1)
    def do_cong(s_arr):
        """bán kính cong R (px rig) tại s và cờ 'cong về phía lưng' (tâm cong nằm phía vây lưng)."""
        s_arr = np.asarray(s_arr)
        _, ndq = phap_tuyen(s_arr)
        pa, _, _ = lay_mau_duong(Q, thick, np.clip(s_arr - 18, 0, Lr) / TI)
        pb, _, _ = lay_mau_duong(Q, thick, np.clip(s_arr + 18, 0, Lr) / TI)
        p0, _, _ = lay_mau_duong(Q, thick, np.clip(s_arr, 0, Lr) / TI)
        d2 = to_rig(pa) + to_rig(pb) - 2 * to_rig(p0)
        R = 1.0 / np.maximum(np.hypot(*d2.T) / (18.0 ** 2), 1e-6)
        R = np.where((s_arr < 20) | (s_arr > Lr - 20), 1e9, R)      # hai mút: dây cung bị cắt, không tính cong
        return R, (d2 * ndq).sum(axis=1) > 0

    def nen_cong(off_d, s_arr, nua_day):
        """nén độ lệch khỏi trục (off_d > 0 phía lưng) ở chỗ cong gắt: phía trong bụng cong không vượt 0,85 R (tránh dải gập đè)."""
        R, ve_lung = do_cong(s_arr)
        lim = 0.85 * R
        trong = np.where(ve_lung, off_d > 0, off_d < 0)
        he = np.where(trong, np.minimum(1.0, lim / np.maximum(1e-6, nua_day)), 1.0)
        return off_d * he, he
    vl = []
    if co_vl:
        tgJ, ndJ = phap_tuyen(s_j[:-1])
        for i in range(N):
            goc_vl = J[i] + ndJ[i] * (Tc[i] * TI / 2 - 12)
            sk.xuong(f"vl{i}", names_s[i], goc_vl[0], goc_vl[1], goc=math.degrees(math.atan2(tgJ[i][1], tgJ[i][0])), dai=seg, the_gioi=True)
            vl.append(f"vl{i}")
    # ---- đầu
    f = pl.get("dau", {"s": 1.0, "r": 0.0, "cx": cfg["fit"]["dau"][0][0], "cy": cfg["fit"]["dau"][0][1]})
    cxy = to_rig((f["cx"], f["cy"]))
    im_d = pc["dau"]
    dat_fit = Dat(cxy[0], cxy[1], goc=f["r"], ti=f["s"])
    gay_px = dat_nguoc(dat_fit, J[0], im_d.width, im_d.height)
    dat_dau = Dat(J[0, 0], J[0, 1], goc=f["r"], ti=f["s"] * hk, neo=gay_px, neo_px=True)
    sk.xuong("dau", fw[-1], J[0, 0], J[0, 1], goc=f["r"], dai=100, the_gioi=True)
    # chóp mõm (hàm trên): điểm phải nhất của đầu
    a_d = np.asarray(im_d)[..., 3] > 60
    yy, xx = np.nonzero(a_d)
    i_r = np.argmax(xx)
    mui = dat_dau.mot((xx[i_r], yy[i_r]), im_d.width, im_d.height)
    mieng_pt = mui + np.array([-6.0, -4.0])
    sk.xuong("mieng", "dau", mieng_pt[0], mieng_pt[1], goc=f["r"], dai=30, the_gioi=True)
    # ---- hàm: bản lề neo vào điểm bản lề trên ảnh đầu (tỉ lệ ảnh, CFG ham_px), tỉ lệ lấy từ dò (hay ham_s × tỉ lệ đầu)
    fj = pl.get("ham")
    im_j = pc["ham"]
    s_j = (fj["s"] if fj else cfg["ham_s"] * f["s"]) * hk
    r_j = f["r"] + cfg.get("ham_r", 0.0)
    ban_le = dat_dau.mot((cfg["ham_px"][0] * im_d.width, cfg["ham_px"][1] * im_d.height), im_d.width, im_d.height)
    ban_le_px = diem_mep(im_j, "trai", 0.12)
    dat_ham = Dat(ban_le[0], ban_le[1], goc=r_j, ti=s_j, neo=ban_le_px, neo_px=True)
    mui_j_px = diem_mep(im_j, "phai", 0.08)
    mui_j = dat_ham.mot(mui_j_px, im_j.width, im_j.height)
    gj = math.degrees(math.atan2(*(mui_j - ban_le)[::-1]))
    sk.xuong("ham", "dau", ban_le[0], ban_le[1], goc=gj, dai=float(np.hypot(*(mui_j - ban_le))), the_gioi=True)
    # ---- lưỡi: dải 4 đốt, con của hàm, nằm dọc hàm trong miệng
    im_l = pc["luoi"]
    uj = (mui_j - ban_le) / max(1e-9, np.hypot(*(mui_j - ban_le)))
    dat_luoi = Dat(*(ban_le + uj * 0.12 * np.hypot(*(mui_j - ban_le)) + np.array([-uj[1], uj[0]]) * 6), goc=gj, ti=hk * 0.5, neo=(0.0, 0.5))
    Ll = luoi.luoi_dai(im_l, 4, ten="luoi", buoc=12, hang=4)
    luoi_b = sk.chuoi("luoi", "ham", dat_luoi.ra(Ll.khop(4), *im_l.size))
    # ---- râu: hai sợi con của hàm, gốc ở cằm
    im_r = pc["rau"]
    rau = {}
    Lr_ = luoi.luoi_dai(im_r, cfg["rau_n"], ten="rau", buoc=12, hang=3)
    for side, fr in (("s", 0.42), ("t", 0.62)):
        goc_px = (ban_le_px[0] + (mui_j_px[0] - ban_le_px[0]) * fr, im_j.height * 0.86)
        g0 = dat_ham.mot(goc_px, im_j.width, im_j.height)
        d_r = Dat(g0[0], g0[1], goc=cfg["rau_goc"] + (6 if side == "t" else -4), ti=cfg["rau_dai"], neo=(0.0, 0.5))
        rau[side] = (sk.chuoi("rau" + side, "ham", d_r.ra(Lr_.khop(cfg["rau_n"]), *im_r.size)), d_r)
    # ---- vây ngực: hai cái, gốc trên cổ phía bụng, lò xo 2 đốt
    im_v = pc["vay_nguc"]
    Lv = luoi.luoi_dai(im_v, 2, ten="vay_nguc", buoc=16, hang=6)
    s_v = cfg["vay_s"] * Lr
    pv_c, tv_c, _ = lay_mau_duong(Q, thick, s_v / TI)
    pv = to_rig(pv_c)
    p2c, _, _ = lay_mau_duong(Q, thick, (s_v + 20) / TI)
    tg = to_rig(p2c) - pv
    tg /= max(1e-9, np.hypot(*tg))
    n_d = np.array([tg[1], -tg[0]])          # phía lưng (vây lưng)
    n_v = -n_d                               # phía bụng
    goc_v = pv + n_v * (tv_c * TI * cfg["vay_u"])
    dv = tg + 0.35 * n_v                     # vây ngực chĩa về sau (phía đuôi), hơi xuống bụng
    gv = cfg["vay_goc"] if "vay_goc" in cfg else math.degrees(math.atan2(dv[1], dv[0]))
    i_seg = min(len(names_s) - 1, int(s_v // seg))
    xv = names_s[i_seg]
    vay = {}
    vt = cfg["vay_ti"]
    for side, off, ti_ in (("s", (6 * TI, -14 * TI), 0.85 * vt), ("t", (0, 0), vt)):
        d_v = Dat(goc_v[0] + off[0], goc_v[1] + off[1], goc=gv, ti=ti_, neo=(0.0, 0.5))
        vay[side] = (sk.chuoi("vay" + side, xv, d_v.ra(Lv.khop(2), *im_v.size)), d_v)
    # ---- mào (dạng 1): lò xo 3 đốt trên đỉnh đầu
    mao = None
    if "mao" in cfg and "mao" in pc and k == 1:
        mcx, mcy, m_goc, m_s = cfg["mao"]           # tâm đáy mào trên concept (px), góc, tỉ lệ (đặt tay: dò tự động không tin được)
        im_m = pc["mao"]
        a_m = np.asarray(im_m)[..., 3] > 60
        yy, xx = np.nonzero(a_m)
        goc_m_px = (float(xx[yy > yy.max() - 0.1 * im_m.height].mean()), float(yy.max()))
        dinh_px = (float(xx[yy < yy.min() + 0.1 * im_m.height].mean()), float(yy.min()))
        cm = to_rig((mcx, mcy))
        dat_m = Dat(cm[0], cm[1], goc=m_goc, ti=m_s, neo=goc_m_px, neo_px=True)
        Lm = luoi.luoi_vung(im_m, B_VIEN, B_TRONG, ten="mao")
        Jm = np.array([dat_m.mot(goc_m_px, *im_m.size) * (1 - u) + dat_m.mot(dinh_px, *im_m.size) * u for u in (0, 0.35, 0.7, 1.0)])
        mao = sk.chuoi("mao", "dau", Jm)
    # ---- vây đuôi: 2 đốt
    dv_goc, dv_s = cfg["duoi_vay"]                   # hướng (độ, thế giới rig) và tỉ lệ đọc trên concept
    im_dv = pc["duoi_vay"]
    goc_dv_px = diem_mep(im_dv, "trai", 0.12)
    dat_dv = Dat(J[N, 0], J[N, 1], goc=dv_goc, ti=dv_s, neo=goc_dv_px, neo_px=True)
    a_dv = np.asarray(im_dv)[..., 3] > 60
    yy, xx = np.nonzero(a_dv)
    xa = float(xx.max())
    tip_dv = dat_dv.mot((xa, float(yy[xx > xa - 0.1 * im_dv.width].mean())), *im_dv.size)
    Jdv = np.array([J[N], J[N] * 0.5 + tip_dv * 0.5, tip_dv])
    dvb = sk.chuoi("dv", bk[-1], Jdv)
    # ---- slot: sau -> trước
    sk.slot("cat_dat", "dat")
    sk.slot("vay_s", vay["s"][0][0], "vay_nguc")
    sk.slot("rau_s", rau["s"][0][0], "rau")
    sk.slot("duoi_vay", dvb[0], "duoi_vay")
    if co_vl:
        sk.slot("vay_lung", "vl0", "vay_lung")
    sk.slot("than", names_s[0], "than_cong" if co_cong else "than_w")
    sk.slot("vay_t", vay["t"][0][0], "vay_nguc")
    if mao:
        sk.slot("mao", mao[0], "mao")
    sk.slot("mieng", "ham", "mieng")
    sk.slot("ham", "ham", "ham")
    sk.slot("luoi", luoi_b[0], "luoi", an=True)
    sk.slot("dau", "dau", "dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("rau_t", rau["t"][0][0], "rau")
    cuoi = "rau_t"
    # mặt nạ cắt ở mặt đất (trồi / chìm): giữ phần trên y = -14
    sk.cat("cat_dat", cuoi, [(-4000, -30), (4000, -30), (4000, 6000), (-4000, 6000)])
    if co_cong:
        # ---- thân cong vẽ đúng dáng concept: lưới vùng, đặt theo dò khớp, trọng số chiếu lên đường khớp (B-spline)
        fb = pl["than_cong"]
        im_b = pc["than_cong"]
        dx_, dy_, ds_ = cfg.get("than_cong_chinh", (0, 0, 1.0))   # chỉnh tay sau dò (dò SQDIFF thiên nhỏ vì đầu, vây che bụng)
        cb = to_rig((fb["cx"] + dx_, fb["cy"] + dy_))
        dat_b = Dat(cb[0], cb[1], goc=fb["r"], ti=fb["s"] * ds_)
        Lb = luoi.luoi_vung(im_b, B_VIEN, B_TRONG, ten="than")
        Qb = dat_b.ra(Lb.pts, *im_b.size)
        Wt = trongso.chuoi_chieu(Qb, J, names_s)
        Wt = trongso.lam_tron(Lb, Wt, 1)
        trongso.kiem(Wt, "than")
        sk.luoi_gan("than", "than_cong", Lb, Wt, dat=dat_b)
    else:
        # ---- lưới thân: dải trên ống nắn, uốn theo đường giữa
        im_w = pc["than_w"]
        if YC is None:
            YC, padw = im_w.height / 2 / TI, 6
        yc = YC * TI
        xl = padw * TI
        Lt = luoi.luoi_dai(im_w, N, truc=[(xl, yc), (im_w.width - xl, yc)], ten="than", mu=True, buoc_theo_cao=Hcon)
        s_v_all = np.clip(Lt.s, 0, Lr)
        pts_c, _, _ = lay_mau_duong(Q, thick, s_v_all / TI)
        Pr = to_rig(pts_c)
        tg, n_d = phap_tuyen(s_v_all)
        off = (Lt.pts[:, 1] - yc)                      # ảnh y xuống: âm = phía vây lưng
        du = Lt.s - s_v_all
        _, T_v, _ = lay_mau_duong(Q, thick, s_v_all / TI)
        off_d, he_t = nen_cong(-off, s_v_all, T_v * TI / 2)
        V = Pr + n_d * off_d[:, None] + tg * du[:, None]
        print(f"  ống: nén phía trong chỗ cong gắt tối thiểu {he_t.min():.2f}")
        Wt = trongso.chuoi(s_v_all, seg, names_s)
        trongso.kiem(Wt, "than")
        sk.luoi_gan("than", "than_w", Lt, Wt, the_gioi=V)
    if co_vl:
        # ---- vây lưng gợn rời: dải lưới trục ở mép gốc (đáy ảnh), đặt dọc mép lưng ống, chiều cao co ở chỗ cong gắt về phía lưng
        im_f = pc["vay_lung"]
        a_f = np.asarray(im_f)[..., 3] > 60
        rows_f = np.flatnonzero(a_f.any(axis=1))
        cols_f = np.flatnonzero(a_f.any(axis=0))
        yb = float(rows_f[-1]) - 2.0
        xf0, xf1 = float(cols_f[0]) + 2.0, float(cols_f[-1]) - 2.0
        Lf = luoi.luoi_dai(im_f, N, truc=[(xf0, yb), (xf1, yb)], ten="vay_lung", mu=True, buoc_theo_cao=Hcon)
        s_f = np.clip(Lf.s / max(1.0, xf1 - xf0) * Lr, 0, Lr)      # kéo vây theo chiều dài thân
        pts_c, T_f, _ = lay_mau_duong(Q, thick, s_f / TI)
        Pf = to_rig(pts_c)
        tgf, ndf = phap_tuyen(s_f)
        hf = np.maximum(0.0, yb - Lf.pts[:, 1])                    # chiều cao trên mép gốc (px rig)
        # giới hạn tổng lệch khỏi trục theo s: lọc cực tiểu ±40 px rồi trung bình ±30 px để chiều cao vây đổi dần dọc thân
        # (cột kề nhau co khác nhau đột ngột thì tam giác vây chéo nhau, hở nêm ở đáy chữ U)
        s_g = np.arange(0.0, Lr + 1, 4.0)
        R_g, vl_g = do_cong(s_g)
        _, T_g, _ = lay_mau_duong(Q, thick, s_g / TI)
        lim_g = np.where(vl_g, 0.85 * R_g, 1e9)
        k1, k2 = 10, 8
        lim_g = np.array([lim_g[max(0, i - k1):i + k1 + 1].min() for i in range(len(lim_g))])
        lim_g = np.array([lim_g[max(0, i - k2):i + k2 + 1].mean() for i in range(len(lim_g))])
        lim = np.interp(s_f, s_g, lim_g)
        nua = T_f * TI / 2
        base = np.minimum(nua, lim) - 18                                        # gốc vây chồng 18 px vào ống
        h_max = float(hf.max())
        co = np.clip((np.maximum(base + 10, lim) - base) / max(1e-6, h_max), 0.0, 1.0)
        Vf = Pf + ndf * (base + hf * co)[:, None]
        # khâu: dọc mỗi hàng của dải, đỉnh cột sau không được lùi về sau đỉnh cột trước theo tiếp tuyến (bow-tie -> lỗ nêm ở đáy chữ U)
        if hasattr(Lf, "hang"):
            C_, R_, idx_ = Lf.hang
            n_khau = 0
            for r_ in range(R_):
                for c_ in range(1, C_):
                    i0, i1 = idx_[c_ - 1, r_], idx_[c_, r_]
                    if i0 < 0 or i1 < 0:
                        continue
                    t_ = tgf[i1]
                    d_ = float((Vf[i1] - Vf[i0]) @ t_)
                    if d_ < 1.5:
                        Vf[i1] = Vf[i0] + t_ * 1.5
                        n_khau += 1
            print(f"  vây lưng: khâu {n_khau} đỉnh chống gập")
        Wf = trongso.chuoi(s_f, seg, vl)
        sk.luoi_gan("vay_lung", "vay_lung", Lf, Wf, the_gioi=Vf)
        print(f"  vây lưng: {Lf.n} đỉnh, co ở chỗ cong gắt tối thiểu {co.min():.2f}")
    # ---- lưới đầu: vùng gáy hoà vào đốt cổ đầu tiên
    Lh = luoi.luoi_vung(im_d, B_VIEN, B_TRONG, ten="dau")
    rg = 0.26 * im_d.height
    Wh = trongso.vung(Lh, [(fw[-1], vung_tron(im_d, gay_px, rg)), ("dau", [(0, 0), (im_d.width, 0), (im_d.width, im_d.height), (0, im_d.height)])],
                      dai_hoa=0.14 * im_d.height)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    # ---- hàm dưới hai xương, lòng miệng theo hàm
    Lj = luoi.luoi_vung(im_j, B_VIEN * 0.85, B_TRONG * 0.85, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *im_j.size), ban_le, mui_j, "dau", "ham", u0=-0.1, u1=0.16)
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    mieng.long_mieng(sk, "mieng", "mieng", "dau", "ham", ban_le, mui, duoi=-0.26, doc=(-0.06, 0.92))
    # ---- mí mắt
    hat = tam_mau(im_d, lambda r, g, b: (r > 200) & (g > 130) & (g < 215) & (b < 130))
    if hat is None:
        hat = (im_d.width * 0.65, im_d.height * 0.45)
    kq = mieng.fit_lid(im_d, pc["mi"], hat=(int(hat[0]), int(hat[1])), ten=f"dạng {k}")
    sk.manh("mi", "mi", mieng.dat_mi(dat_dau, im_d, kq))
    # ---- dải: lưỡi, râu, vây ngực, mào, vây đuôi
    Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / 4, luoi_b, cha="ham", cha_hoa=0.6)
    sk.luoi_gan("luoi", "luoi", Ll, Wl, dat=dat_luoi)
    for side, (names, d_r) in rau.items():
        Wr = trongso.chuoi(Lr_.s, Lr_.truc[1][-1] / cfg["rau_n"], names, cha="ham", cha_hoa=0.5)
        sk.luoi_gan("rau_" + side, "rau", Lr_, Wr, dat=d_r)
    for side, (names, d_v) in vay.items():
        Wv = trongso.chuoi(Lv.s, Lv.truc[1][-1] / 2, names, cha=xv, cha_hoa=0.7)
        sk.luoi_gan("vay_" + side, "vay_nguc", Lv, Wv, dat=d_v)
    if mao:
        Qm = dat_m.ra(Lm.pts, *im_m.size)
        Wm = trongso.chuoi_chieu(Qm, Jm, mao, cha="dau", cha_hoa=0.6)
        sk.luoi_gan("mao", "mao", Lm, Wm, dat=dat_m)
    Ldv = luoi.luoi_vung(im_dv, B_VIEN, B_TRONG, ten="duoi_vay")
    Qdv = dat_dv.ra(Ldv.pts, *im_dv.size)
    Wdv = trongso.chuoi_chieu(Qdv, Jdv, dvb, cha=bk[-1], cha_hoa=0.6)
    sk.luoi_gan("duoi_vay", "duoi_vay", Ldv, Wdv, dat=dat_dv)
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                 ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("troi", "trồi khỏi đất"), ("chim", "chìm xuống")):
        sk.su_kien(e, m)
    info = dict(fw=fw, bk=bk, vl=vl, c=c, N=N, seg=seg, luoi=luoi_b, rau=rau, vay=vay, mao=mao, dv=dvb, J=J, Lr=Lr, pc=pc, k=k,
                to_rig=to_rig, to_concept=to_concept, concept=concept, dat_dau=dat_dau, hk=hk)
    return sk, info


# ---------------------------------------------------------------- clip
def clips(sk, info, k):
    cfg = CFG[k]
    fw, bk, luoi_b, rau, vay, mao, dv = info["fw"], info["bk"], info["luoi"], info["rau"], info["vay"], info["mao"], info["dv"]
    vl = info["vl"]
    nf, nb = len(fw), len(bk)
    H = float(max(info["J"][:, 1].max(), 300))
    A = 1.0 if k == 2 else 1.15
    amp_f = np.array([2.2 + 1.3 * i for i in range(nf)]) * A          # gốc (than) -> gáy
    amp_b = np.array(cfg["bk_amp"][:nb] if len(cfg["bk_amp"]) >= nb else list(cfg["bk_amp"]) + [cfg["bk_amp"][-1]] * nb)[:nb] * A
    gl = -700.0 * (1.3 if k == 2 else 1.0)
    mem_rau = [DayMem(rau[s][0], k0=0.26, k1=0.07, zeta=0.55, lim=(12, 20), luc=lambda t, i, s=s: np.array([70.0 * math.sin(2 * math.pi * t / 1.7 + (0.9 if s == "t" else 0)), gl])) for s in rau]
    mem_vay = [LoXo(vay[s][0], k=[360, 260], damp=0.6, maxang=10) for s in vay]
    mem_dv = [LoXo(dv, k=[340, 240], damp=0.6, maxang=12)]
    mem_mao = [LoXo(mao, k=[380, 280, 200], damp=0.6, maxang=11)] if mao else []
    mem_luoi_rot = [DayMem(luoi_b, k0=0.2, k1=0.05, zeta=0.5, lim=(18, 30), luc=lambda t, i: np.array([0.0, -26000.0]))]
    mem = mem_rau + mem_vay + mem_dv + mem_mao

    def s0(tt, T, ph):
        """sin lệch pha nhưng bằng 0 ở t = 0 (khung 0 idle = dáng gốc = concept): trừ hằng sin(ph)."""
        return math.sin(2 * math.pi * tt / T + ph) - math.sin(ph)

    def than_song(P, tt, amp=1.0, T=2.0, dau_bu=0.8):
        """sóng thân: nửa trước đầu dẫn (hai đốt kề ngược dấu, lớn nhất giữa cổ), đầu bù; nửa sau gốc dẫn, lớn dần ra đuôi.
        Mọi dao động bằng 0 ở t = 0 để khung 0 idle trùng dáng gốc."""
        tot = 0.0
        for i, b in enumerate(fw):
            kk = nf - 1 - i
            a = amp_f[i] * amp * math.sin(math.pi * (i + 0.5) / nf)
            v = (-1 if i % 2 else 1) * a * s0(tt, T, -2 * math.pi * kk * 0.1 / T)
            P.rot(b, v)
            tot += v
        P.rot("dau", -dau_bu * tot)
        for i, b in enumerate(bk):
            P.rot(b, amp_b[i] * amp * s0(tt, T, 1.1 - 2 * math.pi * i * 0.11 / T))
        for i, b in enumerate(vl):          # gợn sóng chạy dọc vây lưng, lệch pha từng đốt
            P.rot(b, (2.4 + 0.6 * (0.3 + 0.7 * amp)) * s0(tt, 1.3, -0.62 * i))
        P.rot("dau", 1.2 * amp * s0(tt, T, 2.0))
        P.rot("ham", -1.5 * amp * max(0.0, s0(tt, T, 0.4)))

    def rot_fw(P, v, prof=None):
        """xoay cả cổ (gốc -> gáy) tổng v độ, chia theo prof; đầu bù một phần để mắt vẫn nhìn đối thủ."""
        prof = prof if prof is not None else np.linspace(0.6, 1.4, nf)
        prof = np.asarray(prof) / np.sum(prof)
        for i, b in enumerate(fw):
            P.rot(b, v * prof[i])
        P.rot("dau", -0.55 * v)

    def rot_bk(P, v, prof=None):
        prof = prof if prof is not None else np.linspace(0.5, 1.5, nb)
        prof = np.asarray(prof) / np.sum(prof)
        for i, b in enumerate(bk):
            P.rot(b, v * prof[i])

    T = cfg["T_idle"]

    def idle_fn(t, P):
        than_song(P, t, 1.0, T / 2)
        # điểm phá nhịp: ngẩng đầu táp miệng (2,55 s), chớp mắt (1,3 s và 3,6 s)
        P.rot("dau", 5 * cv(t, [(0, 0), (2.4, 0), (2.55, 1, "out"), (2.85, 0.6), (3.05, 0, "io"), (T, 0)]))
        P.rot("ham", -cv(t, [(0, 0), (2.4, 0), (2.5, 12, "out"), (2.58, 2), (2.66, 9, "out"), (2.85, 0, "io"), (T, 0)]))
        an_hien(P, "mi", t, [(1.3, 1.42), (3.6, 3.72)])

    def appear_fn(t, P, D=1.4):
        # trồi từ dưới đất (mặt nạ cắt), đuôi lên trước, đầu lên sau, lắc tắt dần, táp miệng
        up = cv(t, [(0, 0), (0.08, 0), (0.75, 1.06, "out"), (0.95, 0.98, "io"), (1.15, 1.0, "io"), (D, 1.0)])
        P.move("move", 0, -(H + 40) * (1 - up))
        a = cv(t, [(0, 0), (0.06, 0), (0.12, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        than_song(P, lui(t, D), ease((t - 0.3) / 0.7))
        rot_fw(P, -22 * cv(t, [(0, 1), (0.5, 1), (0.8, -0.25, "out"), (1.0, 0.08, "io"), (1.2, 0, "io"), (D, 0)]))
        P.rot("dau", 8 * cv(t, [(0, 0), (0.7, 0), (0.85, 1, "out"), (1.1, 0, "io"), (D, 0)]))
        P.rot("ham", -24 * cv(t, [(0, 0), (0.78, 0), (0.88, 1, "out"), (1.12, 0, "io"), (D, 0)]))

    if k == 2:
        def attack_fn(t, P, D=1.1, Hh=0.46):
            # quật đuôi: đuôi nhấc lên ra sau (lấy đà) rồi đập xuống đất phía trước; cổ ngả sau nhẹ rồi chồm
            lift = cv(t, [(0, 0), (0.3, 1, "io"), (0.38, 1.08), (Hh, -0.16, "in"), (0.52, -0.1), (0.75, -0.06, "io"), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.7 * hoat.bao(t, 0.1, 0.95, 0.2, 0.25))
            rot_bk(P, -34 * lift, np.linspace(0.3, 1.6, nb))
            P.rot(dv[0], -20 * lift)
            rot_fw(P, 9 * cv(t, [(0, 0), (0.3, 1, "io"), (Hh, -0.7, "in"), (0.6, -0.5), (D, 0, "io")]))
            P.rot("dau", -6 * cv(t, [(0, 0), (0.3, 1, "io"), (Hh, -1, "in"), (0.6, -0.6), (D, 0, "io")]))
            P.rot("ham", -cv(t, [(0, 0), (0.3, 4), (Hh, 22, "out"), (0.62, 10), (D, 0, "io")]))
            P.move("move", cv(t, [(0, 0), (0.3, -8), (Hh, 10, "in"), (0.6, 8), (D, 0, "io")]), 0)

        def cast_fn(t, P, D=1.5, Hh=0.6, E=1.15):
            # Thủy Pháo: dựng cổ cao, ngửa tụ, nén, chồm nhả tia dày, giữ rung, thở ra
            rear = cv(t, [(0, 0), (0.45, 1, "io"), (0.53, 1.08), (Hh, -0.55, "in"), (0.68, -0.65), (E, -0.55), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.85 * hoat.bao(t, 0.1, 1.4, 0.2, 0.2))
            rot_fw(P, 16 * rear, np.linspace(1.4, 0.6, nf))
            rot_bk(P, 5 * max(rear, 0), np.linspace(1.2, 0.6, nb))
            P.rot("dau", 10 * rear + 1.3 * rung(t, Hh + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.45, 8, "io"), (Hh, 58, "out"), (E, 52), (D, 0, "io")]) + 3 * rung(t, Hh + 0.04, E)))
            P.move("move", cv(t, [(0, 0), (Hh, 0), (Hh + 0.08, -12, "out"), (E, -7), (D, 0, "io")]), 0)
            P.scale("dau", cv(t, [(0, 1), (Hh - 0.03, 1), (Hh, 1.1), (Hh + 0.06, 0.98), (Hh + 0.14, 1), (D, 1)]),
                    cv(t, [(0, 1), (Hh - 0.03, 1), (Hh, 0.94), (Hh + 0.06, 1.02), (Hh + 0.14, 1), (D, 1)]))

        def skill_fn(t, P, D=2.2, Hh=0.95, E=1.7):
            # Thâm Uyên Xoáy: cuộn chặt (đuôi vểnh, cổ xoắn vòng) tụ lực, bung ngửa gầm, giữ rung hai dáng, về
            cr = cv(t, [(0, 0), (0.7, 1, "io"), (0.85, 1.1), (Hh, -1, "out"), (E, -1), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.9 * hoat.bao(t, 0.1, 2.05, 0.25, 0.35))
            # xoáy đầu vòng tròn lúc tụ
            w = hoat.bao(t, 0.15, 0.9, 0.2, 0.15)
            P.rot("dau", 7 * w * math.sin(2 * math.pi * t / 0.45))
            rot_fw(P, 10 * w * math.cos(2 * math.pi * t / 0.45), np.linspace(0.4, 1.6, nf))
            rot_fw(P, -14 * max(cr, 0) + 20 * max(-cr, 0), np.linspace(1.5, 0.5, nf))
            rot_bk(P, -26 * max(cr, 0) - 10 * max(-cr, 0), np.linspace(0.4, 1.7, nb))
            P.rot(dv[0], -25 * max(cr, 0))
            P.rot("dau", -8 * max(cr, 0) + 16 * max(-cr, 0) + 2.0 * rung(t, Hh + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.7, 6), (Hh, 55, "out"), (E, 50), (D, 0, "io")]) + 4 * rung(t, Hh + 0.04, E)))
            P.scale("move", 1 + 0.04 * max(cr, 0), 1 - 0.06 * max(cr, 0) + 0.04 * max(-cr, 0))
            P.move("move", 0, 14 * max(-cr, 0))
    else:
        def attack_fn(t, P, D=0.95, Hh=0.42):
            # mổ: cuộn cổ ra sau lấy đà, phóng đầu tới trong 1 khung, cắn, giữ có trôi, về
            lean = cv(t, [(0, 0), (0.28, 1, "io"), (0.35, 1.08), (Hh, -1.2, "in"), (0.5, -1.3), (0.68, -1.1, "io"), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.7 * hoat.bao(t, 0.1, 0.85, 0.2, 0.25))
            rot_fw(P, 20 * lean, np.linspace(0.5, 1.6, nf))
            P.rot("dau", 10 * lean)
            P.rot("ham", -cv(t, [(0, 0), (0.26, 26, "io"), (Hh - 0.03, 32), (Hh, 2, "in"), (0.62, 0), (D, 0)]))
            P.move("move", cv(t, [(0, 0), (0.28, -10), (Hh, 22, "in"), (0.62, 18), (D, 0, "io")]), 0)
            P.scale("dau", cv(t, [(0, 1), (Hh - 0.03, 1), (Hh, 1.12), (Hh + 0.05, 0.97), (0.62, 1), (D, 1)]),
                    cv(t, [(0, 1), (Hh - 0.03, 1), (Hh, 0.93), (Hh + 0.05, 1.03), (0.62, 1), (D, 1)]))

        def cast_fn(t, P, D=1.1, Hh=0.52, E=0.9):
            # Thủy Thương: ngửa tụ, há, tia nhỏ, giật nhẹ
            rear = cv(t, [(0, 0), (0.4, 1, "io"), (0.47, 1.06), (Hh, -0.6, "in"), (0.6, -0.7), (E, -0.6), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.8 * hoat.bao(t, 0.1, 1.0, 0.2, 0.2))
            rot_fw(P, 10 * rear, np.linspace(1.3, 0.7, nf))
            P.rot("dau", 9 * rear + 1.4 * rung(t, Hh + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.4, 6, "io"), (Hh, 40, "out"), (E, 36), (D, 0, "io")]) + 3 * rung(t, Hh + 0.04, E)))
            P.move("move", cv(t, [(0, 0), (Hh, 0), (Hh + 0.08, -8, "out"), (E, -5), (D, 0, "io")]), 0)

        def skill_fn(t, P, D=1.8, Hh=0.7, E=1.35):
            # Mưa Bọt: nén thân cúi xuống, bật ngửa phun chùm bong bóng lên trời, giữ rung, về
            cr = cv(t, [(0, 0), (0.55, 1, "io"), (0.63, 1.08), (Hh, -1, "out"), (E, -1), (D, 0, "io")])
            than_song(P, lui(t, D), 1 - 0.85 * hoat.bao(t, 0.1, 1.7, 0.25, 0.3))
            P.scale("move", 1 + 0.06 * max(cr, 0) - 0.03 * min(cr, 0), 1 - 0.1 * max(cr, 0) + 0.07 * max(-cr, 0))
            rot_fw(P, 12 * max(cr, 0) - 26 * max(-cr, 0), np.linspace(1.4, 0.6, nf))
            P.rot("dau", 8 * max(cr, 0) - 18 * max(-cr, 0) + 2.0 * rung(t, Hh + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.55, 4), (Hh, 46, "out"), (E, 42), (D, 0, "io")]) + 4 * rung(t, Hh + 0.04, E)))
            rot_bk(P, -8 * max(-cr, 0))

    def hit_fn(t, P, D=0.6):
        # không lấy đà: đầu bật ra sau ở 0,07 s, sóng chạy từ đầu về gốc, mắt nhắm
        than_song(P, lui(t, D), ease((t - 0.25) / 0.35))
        for i, b in enumerate(fw):
            dl = 0.03 * (nf - 1 - i)
            P.rot(b, (5 + 2.2 * i) * cv(t, [(0, 0), (0.07 + dl, 1, "out"), (0.33 + dl, -0.25, "io"), (D, 0, "io")]))
        P.rot("dau", 14 * cv(t, [(0, 0), (0.07, 1, "out"), (0.22, 0.5, "io"), (0.42, -0.1, "io"), (D, 0, "io")]))
        P.rot("ham", -10 * cv(t, [(0, 0), (0.07, 1, "out"), (0.4, 0, "io"), (D, 0)]))
        P.move("move", -9 * cv(t, [(0, 0), (0.07, 0.4, "out"), (0.2, 1, "io"), (0.45, -0.05, "io"), (D, 0, "io")]), 0)
        for i, b in enumerate(bk):
            P.rot(b, (2 + 1.2 * i) * cv(t, [(0, 0), (0.12 + 0.03 * i, 1, "out"), (0.4 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))
        an_hien(P, "mi", t, [(0.03, 0.3)])

    def die_fn(t, P, D=2.0):
        # giật, nhắm mắt, ngửa đầu lè lưỡi lả đi, cổ đổ dần, chìm xuống đất (mặt nạ), tan
        P.rot("dau", cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.85, 40, "io"), (1.25, 34), (D, 30)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 8), (0.85, 30, "io"), (D, 30)]))
        rot_fw(P, cv(t, [(0, 0), (0.07, 8, "out"), (0.5, 4), (1.1, -34, "io"), (1.4, -40), (D, -40)]), np.linspace(0.5, 1.6, nf))
        rot_bk(P, cv(t, [(0, 0), (0.07, -6, "out"), (0.5, 0), (1.3, 6, "io"), (D, 6)]))
        P.rot("dau", 2.5 * math.sin(2 * math.pi * t / 0.5) * hoat.bao(t, 0.3, 1.2, 0.2, 0.3))
        an_hien(P, "mi", t, [(0.04, D + 1)])
        P.alpha["luoi"] = cv(t, [(0, 0), (0.3, 0), (0.42, 1)])
        sink = cv(t, [(0, 0), (1.3, 0), (1.9, 1, "in"), (D, 1)])
        P.move("move", 0, -(H + 60) * sink)
        a = cv(t, [(0, 1), (1.5, 1), (1.95, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0 or s["name"] in ("mi", "luoi"):
                P.alpha[s["name"]] = P.alpha.get(s["name"], 1.0) * a

    def luoi_die_post(t, P):
        pass

    ev_attack = [(0.46 if k == 2 else 0.42, "trung", "")]
    out = [Clip("appear", 1.4, appear_fn, mem=mem, ev=[(0.3, "troi", "")]),
           Clip("idle", T, idle_fn, loop=True, mem=mem),
           Clip("attack", 1.1 if k == 2 else 0.95, attack_fn, ev=ev_attack, mem=mem),
           Clip("cast", 1.5 if k == 2 else 1.1, cast_fn, ev=[(0.6 if k == 2 else 0.52, "phun", ""), (1.15 if k == 2 else 0.9, "het_phun", "")], mem=mem),
           Clip("skill", 2.2 if k == 2 else 1.8, skill_fn, ev=[(0.95 if k == 2 else 0.7, "gam", ""), (1.7 if k == 2 else 1.35, "het_gam", "")], mem=mem),
           Clip("hit", 0.6, hit_fn, mem=mem),
           Clip("die", 2.0, die_fn, mem=mem + mem_luoi_rot, ev=[(1.3, "chim", "")])]
    return out


# ---------------------------------------------------------------- so với concept
def so_concept(sk, info, frames_idle0, ra):
    """khung 0 idle vẽ ở tỉ lệ concept, chồng lên concept; IoU mặt nạ (cả con, và bỏ vùng đầu đã cố ý phóng to)."""
    ve = soi.Ve(sk)
    cfg = CFG[info["k"]]
    concept = info["concept"]
    Hc, Wc = concept.shape[:2]
    to_rig = info["to_rig"]
    # hộp vẽ = cả ảnh concept đổi sang rig
    tl, br = to_rig((0, 0)), to_rig((Wc, Hc))
    box = (tl[0], br[1], br[0], tl[1])
    img = ve.ve(frames_idle0, box, 1.0 / TI, bg=(255, 255, 255), ss=1)
    img = img.convert("RGBA").resize((Wc, Hc), Image.BILINEAR)
    a = np.asarray(img)
    m_rig = (a[..., :3].min(axis=2) < 236)
    m_con = (concept.min(axis=2) < 236)
    m_con = anh.mo_mo(m_con, 1)
    iou = float((m_rig & m_con).sum() / max(1, (m_rig | m_con).sum()))
    # bỏ vùng đầu (hộp quanh đầu dò được, nới theo hk)
    f = json.load(open(os.path.join(inbox(info["k"]), "rig", "place.json"), encoding="utf-8")).get("dau") if os.path.exists(os.path.join(inbox(info["k"]), "rig", "place.json")) else None
    iou2 = iou
    if info.get("dau_box"):
        f = None
        x0, y0, x1, y1 = [int(v) for v in info["dau_box"]]
        if info["hk"] > 1.0:   # hộp đầu nới theo tỉ lệ phóng quanh gáy (về phía mõm, lên trên)
            x1 = min(Wc, int(x0 + (x1 - x0) * info["hk"] + 20))
            y0 = max(0, int(y1 - (y1 - y0) * info["hk"] - 20))
        keep = np.ones_like(m_rig)
        keep[y0:y1, x0:x1] = False
        iou2 = float((m_rig & m_con & keep).sum() / max(1, ((m_rig | m_con) & keep).sum()))
    if f:
        dw, dh = info["pc"]["dau"].width / TI * f["s"] * info["hk"], info["pc"]["dau"].height / TI * f["s"] * info["hk"]
        x0, x1 = int(max(0, f["cx"] - 0.75 * dw)), int(min(Wc, f["cx"] + 0.75 * dw))
        y0, y1 = int(max(0, f["cy"] - 0.75 * dh)), int(min(Hc, f["cy"] + 0.75 * dh))
        keep = np.ones_like(m_rig)
        keep[y0:y1, x0:x1] = False
        iou2 = float((m_rig & m_con & keep).sum() / max(1, ((m_rig | m_con) & keep).sum()))
    # ảnh: concept | khung 0 | chồng (concept đỏ, rig xanh)
    ov = np.full((Hc, Wc, 3), 255, np.uint8)
    ov[m_con] = (255, 150, 150)
    ov[m_rig] = (120, 170, 255)
    ov[m_con & m_rig] = (90, 90, 90)
    from PIL import ImageDraw
    sheet = Image.new("RGB", (Wc * 3 // 2, Hc // 2 + 30), (255, 255, 255))
    sheet.paste(Image.fromarray(concept).resize((Wc // 2, Hc // 2)), (0, 30))
    sheet.paste(img.convert("RGB").resize((Wc // 2, Hc // 2)), (Wc // 2, 30))
    sheet.paste(Image.fromarray(ov).resize((Wc // 2, Hc // 2)), (Wc, 30))
    d = ImageDraw.Draw(sheet)
    d.text((8, 8), f"concept | khung 0 idle | chồng: IoU {iou:.3f} (bỏ vùng đầu phóng {info['hk']:.2f}x: {iou2:.3f})", fill=(0, 0, 0), font=anh.font(16))
    sheet.save(ra)
    print(f"  so_concept: IoU {iou:.3f}, bỏ vùng đầu {iou2:.3f} -> {ra}")
    return iou, iou2


def uon_thu(sk, info, ra):
    P = Pose()
    for b in info["fw"]:
        P.rot(b, 10)
    for b in info["bk"]:
        P.rot(b, -8)
    P.rot("dau", -12)
    P.rot("ham", -34)
    for s, (names, _) in info["rau"].items():
        for b in names:
            P.rot(b, 8)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.0, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


def dung_any(k, ti=None):
    """cách lai (tm08_lai.dung_lai) khi đã cắt lớp từ concept (manh_lai/lop.json), không thì dựng từ mảnh GPT."""
    if os.path.exists(os.path.join(inbox(k), "manh_lai", "lop.json")):
        import tm08_lai
        return tm08_lai.dung_lai(k, ti)
    return dung(k, ti)


def rig(k, sk2=None, fr2=None):
    global TI
    t0 = time.time()
    cfg = CFG[k]
    rd = os.path.join(inbox(k), "rig")
    sk, info = dung_any(k)
    cl = clips(sk, info, k)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"  dạng {k}: nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
    iou = so_concept(sk, info, fr["idle"][0], os.path.join(rd, "so_concept.png"))
    noi_them = {"so_concept": f"IoU khung 0 idle với concept {iou[0]:.3f} (bỏ vùng đầu phóng {info['hk']:.2f}x: {iou[1]:.3f})"}
    ve = soi.Ve(sk)
    hA = soi.chieu_cao(ve, fr["idle"][0])
    B = ve.bao(fr["idle"][0])
    rong = B[2] - B[0]
    cao = max(hA, rong / 1.42)   # con dài dẹt: khai cao hơn để game co cho vừa sân
    can = [("can_mieng_cast", "cast", 0.62 if k == 2 else 0.54, "ham", 110), ("can_mieng_skill", "skill", 1.0 if k == 2 else 0.75, "ham", 120),
           ("can_rau_hit", "hit", 0.1, "ham", 150), ("can_gay_idle", "idle", 1.0, info["fw"][-1], 120),
           ("can_duoi_attack", "attack", 0.46 if k == 2 else 0.42, info["bk"][-1], 160), ("can_mi_hit", "hit", 0.1, "dau", 120)]
    M = sk
    clM, frM = cl, fr
    tol = None
    if k == 1 and sk2 is not None:
        # rig gộp mang cả atlas dạng 2: dựng lại dạng 2 ở TI dạng 1 (0,65) cho atlas nhỏ; lọc khoá chặt hơn
        sk2, info2 = dung_any(2, ti=TI_K[1])
        fr2 = {"idle": hoat.nuong(sk2, clips(sk2, info2, 2)[1])}
        TI = TI_K[1]
        tol = {"rotate": 0.3, "translate": 0.7, "scale": 0.005}
        hB = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0])
        M = tienhoa.gop(sk, sk2)
        fw, nf = info["fw"], len(info["fw"])

        def gong(t, P):
            sq = cv(t, [(0, 0), (0.3, -0.06), (0.45, 0.06, "out"), (1.0, 0.05), (1.3, 0.0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            P.rot("dau", cv(t, [(0, 0), (0.3, -5), (0.6, 14, "out"), (1.3, 16)]) + 1.5 * rung(t, 0.5, 1.3))
            for i, b in enumerate(fw):
                P.rot(b, cv(t, [(0, 0), (0.3, 3), (0.6, -8, "out"), (1.3, -9)]) * (i + 1) / nf)

        def gam(t, P, fl):
            P.rot("n_dau", 12 * fl)
            P.rot("n_ham", -40 * fl)
            P.scale("n_move", 1 + 0.04 * fl, 1 + 0.04 * fl)

        memM = cl[1].mem + tienhoa.doi_ten_mem([m for m in sk2.info.get("mem_idle", [])])
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
        noi_them["evolve"] = s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"
    tong = xuat.xuat_het(M, clM, rd, f"{CODE}_{k}", f"{cfg['ten']} (dạng {k})", frames=frM, dang=k, so_dang=2, ma_goc=3247,
                         dung_yen=("attack", "cast", "skill"), cao=cao, can=can, noi_them=noi_them, tol=tol)
    uon_thu(sk, info, os.path.join(rd, "uon_thu.png"))
    bv, bt = info.get("buoc", (B_VIEN, B_TRONG))
    lai_txt = "; cách lai: thân, vây lưng, vây đuôi, vây ngực, mào, đầu cắt từ concept" if info.get("lai") else ""
    with open(os.path.join(rd, "so_sanh.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\nMật độ lưới: {tong['dinh']} đỉnh / chiều cao {hA:.0f} px rig = {tong['dinh'] / hA:.2f} đỉnh mỗi px chiều cao; bước viền "
                f"{bv} px, bước trong {bt} px (1,5% / 2% chiều cao); thân {info['N']} đốt{lai_txt}.\n")
    sk.info["mem_idle"] = cl[1].mem
    print(f"  dạng {k} xong {time.time() - t0:.1f} s; .atomik {tong['atomik_kb']:.0f} KB")
    return sk, fr


def main(argv):
    cmd = argv[0] if argv else "all"
    if cmd == "cat":
        cat(int(argv[1]))
    elif cmd == "place":
        place(int(argv[1]))
    elif cmd == "rig":
        k = int(argv[1])
        if k == 1:
            sk2, fr2 = rig(2)
            rig(1, sk2, fr2)
        else:
            rig(2)
    elif cmd == "all":
        sk2, fr2 = rig(2)
        rig(1, sk2, fr2)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
