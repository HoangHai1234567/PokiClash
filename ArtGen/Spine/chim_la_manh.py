# -*- coding: utf-8 -*-
"""Chim bảo hộ rừng cánh lá (chim_la), hướng C đã duyệt 2026-11-12 (linh điểu trắng): MẢNH theo khung từng part của rig monster_3630
(skill pokiclash-spine-rig mục 00). Mỗi part một ô ĐÚNG KHUNG ảnh vùng của nó × z; trong ô là hình bóng kín của part tô phẳng theo thiết
kế của mình. Codex vẽ lại sạch, giữ nguyên hình bóng; mã cắt đúng ô, dọn, đo IoU.

- Tờ theo nhóm (tự xếp, nhóm lớn tách nhiều tờ): la_gan, la_xa, la_lat (bộ chibangR3: mặt kia của cánh gần), tan, tan_lat, canh, duoi,
  da, dau (đầu, mỏ, vòng cổ lá, bùa đá, đùi, túm lông gáy), chan.
- Tờ X (ô THÊM, rig gốc không có): năm lá mào, vòng gỗ ở trán, bông hoa, mầm hai lá.
- Tờ L (THÂN LIỀN): cổ – ngực + bụng + túm lông che gốc đùi là một bề mặt nối nhau → gen liền một ảnh rồi nướng vào khung từng part.

    chim_la_manh.py to                 dựng mọi tờ hướng dẫn → inbox/chim_la_1/mau/part_<tờ>.png + .json, lien.png, prompt từng tờ
    chim_la_manh.py cat [tờ ...] [ep]  cắt tờ đã gen (tai_ve/N_<tờ>*.png) → manh/part/<vùng>.png, _iou.json
    chim_la_manh.py lien               nướng tờ thân liền (tai_ve/N_L*.png) vào khung part
    chim_la_manh.py so                 tờ so part đã cắt với hình bóng (đỏ = thiếu, xanh lá = thừa) → mau/so_part.png
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chim_la as CL  # noqa: E402

W, H = 1536, 1024
INK = CL.INK
MAU, TAI = CL.MAU, CL.TAI
MANH = os.path.join(CL.BASE, "manh")
PK = os.path.join(HERE, "gui_gpt", "chim_la_1")
PAL = dict(CL.PALS["bach"], gan_tan=(31, 86, 52), long_net=(206, 198, 170), sage_net=(96, 128, 96), go_net=(92, 62, 40),
           da_net=(104, 100, 92), trang=(255, 255, 255))
el = CL.el
_T = {}


def by():
    """{tên vùng ảnh: hình đầu tiên dùng vùng đó} (dáng gốc, mọi hình kể cả bộ mặc định tắt)."""
    if not _T:
        CL.ATT = "att_goc.json"
        CL._C.clear()
        CL.nap()
        for a in CL._C["het"]:
            _T.setdefault(a["region"], a)
    return _T


def ngan(ten):
    return ten.replace("P_", "")


def a_tl():
    """pixel ảnh vùng của họ cho mỗi đơn vị rig."""
    a = by()["P_xiashen"]
    _, imgs, _ = CL.nap()
    im = imgs[a["region"]]
    uv = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    xy = np.array(a["xy"], float).reshape(-1, 2)
    return float(np.hypot(*(uv.max(0) - uv.min(0))) / np.hypot(*(xy.max(0) - xy.min(0))))


def co_o(ten, z):
    _, imgs, _ = CL.nap()
    im = imgs[by()[ten]["region"]]
    return int(round(im.width * z)), int(round(im.height * z))


def canh_moi(m0, z, dem=0):
    """CÀNH CÂY thay cho dải đá hoa văn chữ triện của con gốc (mảnh dễ nhận ra của họ; người dùng: "làm khác con gốc đi"): từ hình
    bóng một khúc dải, dựng một CÀNH cong mềm chạy theo trục chính của khúc (đa thức bậc hai trong hệ trục PCA), thuôn hai đầu, cộng
    tối đa hai NHÁNH CUỘN (tua cuốn) mọc về phía khúc cũ có móc. Vẫn nằm trong khung ảnh vùng; rig gắn ô cả khung, cứng theo xương."""
    ys, xs = np.nonzero(m0)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    u = np.linalg.svd(P - c, full_matrices=False)[2][0]
    v = np.array([-u[1], u[0]])
    S, T = (P - c) @ u, (P - c) @ v
    dt = cv2.distanceTransform(m0.astype(np.uint8), cv2.DIST_L2, 5)
    day = 2.0 * float(np.percentile(dt[m0], 92))                     # bề dày dải
    s0, s1 = np.percentile(S, 1.5), np.percentile(S, 98.5)
    # thân cành: bậc hai theo các điểm gần trục (bỏ phần móc chìa xa)
    gan = np.abs(T - np.median(T)) < 1.2 * day
    co = np.polyfit(S[gan], T[gan], 2) if gan.sum() > 50 else np.polyfit(S, T, 2)
    out = np.zeros(m0.shape, np.uint8)
    le = dem + int(round(1.6 * z))                                   # giữ cành nằm gọn TRONG khung ảnh vùng (dem = viền đệm của bong)
    Hh, Ww = m0.shape

    def kep(p, w):                                                   # tâm nét lùi vào để cả bề dày nét không chạm mép khung
        r_ = w / 2.0 + le
        return (int(min(max(p[0], r_), Ww - 1 - r_)), int(min(max(p[1], r_), Hh - 1 - r_)))

    ss = np.linspace(s0 + 0.3 * day, s1 - 0.3 * day, 60)
    tt = np.polyval(co, ss)
    Q = c + ss[:, None] * u + tt[:, None] * v
    for k in range(len(Q) - 1):
        f = k / (len(Q) - 1)
        w = day * (1.05 + 0.50 * math.sin(math.pi * min(1.0, max(0.0, f))) ** 0.6)     # cành mập như trên concept
        cv2.line(out, kep(Q[k], w), kep(Q[k + 1], w), 1, max(2, int(w)), cv2.LINE_AA)
    # nhánh con: mẩu cành ngắn, tù đầu, chĩa xiên ra phía khúc cũ có móc (ở 30% và 70% chiều dài; khúc ngắn thì một nhánh ở giữa).
    # (Đã thử nhánh cuộn tròn kiểu tua cuốn: cuộn khép thành vòng khuyên hoặc chìa khỏi khung ảnh vùng; mẩu cành thẳng thì gọn.)
    for j, f in enumerate((0.30, 0.70) if (s1 - s0) > 6.0 * day else (0.5,)):
        sf = s0 + (s1 - s0) * f
        gan_s = np.abs(S - sf) < 0.16 * (s1 - s0)
        r = T[gan_s] - np.polyval(co, S[gan_s])
        if not len(r):
            continue
        xa = max(np.percentile(r, 97), -np.percentile(r, 3))
        if xa < 1.45 * day:                                          # khúc này trơn: không có nhánh
            continue
        sg = 1.0 if np.percentile(r, 97) > -np.percentile(r, 3) else -1.0
        dai = min(max(0.9 * xa, 1.8 * day), 2.7 * day)
        goc_p = c + sf * u + np.polyval(co, sf) * v
        ng = (1.0 if j == 0 else -1.0) * math.radians(38.0)          # hai nhánh xiên về hai phía
        huong = sg * v * math.cos(ng) + u * math.sin(ng)
        pts = np.array([goc_p + huong * dai * q + sg * v * 0.10 * dai * math.sin(math.pi * q) for q in np.linspace(0, 1, 9)])
        for k in range(len(pts) - 1):
            w = day * (0.92 - 0.30 * k / (len(pts) - 1))
            cv2.line(out, kep(pts[k], w), kep(pts[k + 1], w), 1, max(2, int(w)), cv2.LINE_AA)
    out = cv2.GaussianBlur(out * 255, (0, 0), 0.9 * z) > 120
    return out


def bong(ten, z):
    """hình bóng KÍN của part trong khung ảnh vùng × z (làm trơn nhẹ trên ảnh đã đệm viền; giữ mọi khối rời đủ lớn: vùng đá có 2–3 viên)."""
    src = CL.part_goc(by()[ten])
    w, h = co_o(ten, z)
    al = np.asarray(src.resize((w, h), Image.LANCZOS))[..., 3]
    d = int(round(3 * z))
    m = np.pad((al > 100).astype(np.uint8), d)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(1.0 * z))
    if CL.loai(ten) == "canh":
        m = canh_moi(m.astype(bool), z, d).astype(np.uint8)
    else:
        m = cv2.GaussianBlur(m * 255, (0, 0), 0.8 * z) > 127
    m = m[d:-d, d:-d]
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 2:
        lon = st[1:, cv2.CC_STAT_AREA].max()
        giu = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 0.05 * lon]
        m = np.isin(lab, giu)
    return m.astype(bool)


def the_gioi_o(a, w, h, tol=6.0):
    """toạ độ thế giới (dáng gốc) của từng pixel trong khung ảnh vùng (w × h) của một part, qua lưới của nó; NaN ngoài lưới."""
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    ys, xs = np.mgrid[0:h, 0:w]
    P = np.c_[xs.ravel() + 0.5, ys.ravel() + 0.5]
    Wd = np.full((len(P), 2), np.nan)
    tot = np.full(len(P), -9.0)
    for t in np.array(a["tris"]).reshape(-1, 3):
        A_, B_, C_ = U[t[0]], U[t[1]], U[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, P - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        den = den if abs(den) > 1e-9 else 1e-9
        b1 = (v2[:, 0] * v1[1] - v2[:, 1] * v1[0]) / den
        b2 = (v0[0] * v2[:, 1] - v0[1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        tl = tol / max(1.0, float(np.sqrt(abs(den))))
        nho = np.minimum(np.minimum(b0, b1), b2)
        hon = (nho >= -tl) & (nho > tot)
        Wd[hon] = b0[hon, None] * V[t[0]] + b1[hon, None] * V[t[1]] + b2[hon, None] * V[t[2]]
        tot[hon] = nho[hon]
    return Wd.reshape(h, w, 2)


def uv_cua(a, p):
    """toạ độ uv (0..1) trong khung ảnh vùng của điểm thế giới p, qua lưới của part (tam giác chứa điểm, không thì tam giác gần nhất)."""
    U = np.array(a["uv"], float).reshape(-1, 2)
    V = np.array(a["xy"], float).reshape(-1, 2)
    best, kq = -9e9, None
    for t in np.array(a["tris"]).reshape(-1, 3):
        A_, B_, C_ = V[t[0]], V[t[1]], V[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, np.asarray(p, float) - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        if abs(den) < 1e-9:
            continue
        b1 = (v2[0] * v1[1] - v2[1] * v1[0]) / den
        b2 = (v0[0] * v2[1] - v0[1] * v2[0]) / den
        b0 = 1 - b1 - b2
        nho = min(b0, b1, b2)
        if nho > best:
            best, kq = nho, b0 * U[t[0]] + b1 * U[t[1]] + b2 * U[t[2]]
    return kq


def truc(m):
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    u = np.linalg.svd(P - c, full_matrices=False)[2][0]
    t = (P - c) @ u
    return c + u * np.percentile(t, 3), c + u * np.percentile(t, 97), u


def _net_long(im, m, z, mau, n=3, rng=None):
    """vài nét lông / thớ chạy dọc trục dài của mảnh (nét chì mảnh, không phải mực)."""
    p0, p1, u = truc(m)
    nn = np.array([-u[1], u[0]])
    ys, xs = np.nonzero(m)
    rong = np.percentile(np.abs((np.stack([xs, ys], 1) - (p0 + p1) / 2) @ nn), 90)
    tr = cv2.erode(m.astype(np.uint8), el(3.2 * z)).astype(bool)
    tmp = im.copy()
    for k in range(n):
        o = (k - (n - 1) / 2) / max(1, n) * 1.3 * rong
        a_, b_ = p0 + (p1 - p0) * 0.22 + nn * o, p0 + (p1 - p0) * (0.80 - 0.07 * (k % 2)) + nn * o * 0.6
        cv2.line(tmp, (int(a_[0]), int(a_[1])), (int(b_[0]), int(b_[1])), mau, max(2, int(round(0.9 * z))), cv2.LINE_AA)
    im[tr] = tmp[tr]


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    s = ngan(ten)
    nh = CL.loai(ten)
    m = bong(ten, z)
    h, w = m.shape
    im = np.full((h, w, 3), 255, np.uint8)
    at = a_tl()
    nho = nh in ("vuot", "chan", "da", "bua", "mo", "choi") or (nh == "la" and max(w, h) / z < 75)
    vien = (5.7 if nho else 8.0) * at * z                           # 4 px / 6 px trên concept (0,706 px mỗi đơn vị)
    Y, X = np.mgrid[0:h, 0:w]
    a = by()[ten]
    if nh == "la":
        dai = max(w, h) / z
        im[m] = PAL["la"] if dai > 66 else PAL["la_nhat"]
        p0, p1, _ = truc(cv2.erode(m.astype(np.uint8), el(vien)).astype(bool) if dai > 40 else m)
        q0, q1 = p0 + (p1 - p0) * 0.06, p0 + (p1 - p0) * 0.94
        cv2.line(im, (int(q0[0]), int(q0[1])), (int(q1[0]), int(q1[1])), PAL["gan"], max(2, int(round(1.1 * z))), cv2.LINE_AA)
    elif nh == "tan":                                                # tán lá: mảng lục sẫm, vài hàng vảy lá tròn
        im[m] = PAL["tan"]
        tr = cv2.erode(m.astype(np.uint8), el(vien + 1.5 * z)).astype(bool)
        tmp = im.copy()
        r = 15.0 * z
        for j, yy in enumerate(np.arange(r * 0.9, h + r, r * 1.25)):
            for xx in np.arange(-r + (r if j % 2 else 0), w + r, 2 * r):
                cv2.ellipse(tmp, (int(xx), int(yy)), (int(r), int(r * 0.9)), 0, 0, 180, PAL["gan_tan"], max(2, int(round(1.0 * z))), cv2.LINE_AA)
        im[tr] = tmp[tr]
    elif nh == "canh":
        im[m] = PAL["canh"]
    elif nh == "choi":
        im[m] = PAL["la_nhat"]
    elif nh == "duoi":
        dam = s in ("weiba5_01", "weiba5_04", "weiba5_06")
        im[m] = PAL["long_dam"] if dam else PAL["long"]
        _net_long(im, m, z, PAL["sage_net"] if dam else PAL["long_net"], 3)
    elif nh in ("da_to", "da_ngon"):                                 # đá + chỏm rêu ở phía TRÊN (theo thế giới dáng gốc)
        im[m] = PAL["da"]
        Wd = the_gioi_o(a, w, h)
        wy = Wd[..., 1]
        ok = m & ~np.isnan(wy)
        if ok.any():
            lo, hi = np.nanpercentile(wy[ok], 2), np.nanpercentile(wy[ok], 98)
            reu = ok & (wy > lo + (hi - lo) * (0.56 if nh == "da_ngon" else 0.62))
            reu = cv2.morphologyEx(reu.astype(np.uint8), cv2.MORPH_OPEN, el(1.5 * z)).astype(bool)
            im[reu] = PAL["reu"]
            im[cv2.morphologyEx(reu.astype(np.uint8), cv2.MORPH_GRADIENT, el(0.6 * z)).astype(bool) & m] = INK
    elif nh == "da":
        im[m] = PAL["da_dam"]
    elif nh == "bua":
        im[m] = PAL["da"]
        if s == "xiongjia_02":
            cx, cy, r = w // 2, int(h * 0.52), int(w * 0.20)
            P = np.array([(cx, cy - int(r * 1.5)), (cx + r, cy), (cx, cy + int(r * 1.5)), (cx - r, cy)], np.int32)
            cv2.fillPoly(im, [P], PAL["ngoc"], cv2.LINE_AA)
            cv2.polylines(im, [P], True, INK, max(2, int(round(1.6 * z * at))), cv2.LINE_AA)
    elif nh == "dui":
        im[m] = PAL["long_dam"]
        _net_long(im, m, z, PAL["sage_net"], 2)
    elif nh == "la_co":
        im[m] = PAL["la_co"]
    elif nh == "dau":                                                # mũ lục xám (đỉnh + gáy), mặt kem (trước + má + họng), mắt xếch dữ
        im[m] = PAL["dau"]
        MA_UV = [(0.67, 0.44), (0.79, 0.31), (0.92, 0.27), (1.0, 0.40), (1.0, 0.82), (0.80, 0.84), (0.72, 1.0), (0.40, 1.0), (0.44, 0.76),
                 (0.58, 0.64)]
        mk = np.zeros((h, w), np.uint8)
        cv2.fillPoly(mk, [np.int32([(u * w, v * h) for u, v in MA_UV])], 1)
        im[m & mk.astype(bool)] = PAL["ma"]
        e = by()["P_yanjing_01"]
        pe = uv_cua(a, np.array(e["xy"], float).reshape(-1, 2).mean(0)) * np.array([w, h])
        cx, cy = int(pe[0]), int(pe[1])
        rx, ry = int(7.5 * z), int(4.2 * z)
        cv2.ellipse(im, (cx, cy), (rx, ry), 14, 0, 360, PAL["mat"], -1, cv2.LINE_AA)
        cv2.ellipse(im, (cx, cy), (rx, ry), 14, 0, 360, INK, max(2, int(1.3 * z)), cv2.LINE_AA)
        cv2.circle(im, (cx + int(1.0 * z), cy), int(2.6 * z), INK, -1, cv2.LINE_AA)
        cv2.circle(im, (cx + int(0.1 * z), cy - int(1.2 * z)), max(1, int(0.8 * z)), PAL["trang"], -1, cv2.LINE_AA)
        cv2.line(im, (cx - int(11 * z), cy - int(9.5 * z)), (cx + int(9.5 * z), cy - int(2.4 * z)), INK, max(3, int(2.6 * z)), cv2.LINE_AA)
    elif nh == "mo":
        im[m] = PAL["mo"]
    elif nh == "chan":
        im[m] = PAL["chan"]
    elif nh == "vuot":
        im[m] = PAL["vuot"]
    else:                                                            # long: mao_01 (túm lông gáy) và các mảnh thân (thân lấy từ tờ liền)
        im[m] = PAL["long"]
        if s == "mao_01":
            _net_long(im, m, z, PAL["long_net"], 2)
    im[m & ~cv2.erode(m.astype(np.uint8), el(vien)).astype(bool)] = INK
    im[~m] = 255
    return im, m


# ---------------------------------------------------------------- ô THÊM (rig gốc không có): tờ X
LA_MAO = [(228, 37), (276, 42), (322, 48), (254, 40), (140, 26)]     # (dài, nửa rộng) đơn vị rig của năm lá mào (theo sơ đồ đã duyệt)
X_PX = 2.0                                                           # px trên tờ X cho mỗi đơn vị rig
THEM = {}
for _i, (_d, _r) in enumerate(LA_MAO):
    THEM[f"mao_{_i + 1}"] = (int(_r * 2 * X_PX) + 24, int(_d * X_PX) + 24)
THEM.update(vong=(380, 92), hoa=(170, 170), mam=(210, 190))


def o_them(ten):
    w, h = THEM[ten]
    im = np.full((h, w, 3), 255, np.uint8)
    if ten.startswith("mao_"):                                       # lá mào dựng đứng: gốc ở đáy, ngọn ở đỉnh, gân giữa
        i = int(ten[4:]) - 1
        P, c = CL.la_hinh((w / 2, h - 12), (w / 2, 12), LA_MAO[i][1] * X_PX, 0.0)
        cv2.fillPoly(im, [np.int32(P)], PAL["la"] if i % 2 == 0 else PAL["la_nhat"], cv2.LINE_AA)
        cv2.polylines(im, [np.int32(P)], True, INK, 11, cv2.LINE_AA)
        cv2.polylines(im, [np.int32(c[3:-3])], False, PAL["gan"], 5, cv2.LINE_AA)
    elif ten == "vong":                                              # vòng gỗ ở trán: dải cong nhẹ, hai đầu tròn
        t = np.linspace(0, 1, 40)
        tren = np.stack([16 + (w - 32) * t, 34 - 20 * np.sin(np.pi * t)], 1)
        duoi = np.stack([16 + (w - 32) * t, 76 - 20 * np.sin(np.pi * t)], 1)[::-1]
        P = np.int32(np.concatenate([tren, duoi]))
        cv2.fillPoly(im, [P], PAL["canh"], cv2.LINE_AA)
        cv2.polylines(im, [P], True, INK, 10, cv2.LINE_AA)
    elif ten == "hoa":                                               # bông hoa năm cánh hồng nhuỵ cam
        cx, cy = w // 2, h // 2
        for q in range(5):
            g = q * 2 * np.pi / 5 - np.pi / 2
            p = (int(cx + 42 * np.cos(g)), int(cy + 42 * np.sin(g)))
            cv2.circle(im, p, 34, INK, -1, cv2.LINE_AA)
        for q in range(5):
            g = q * 2 * np.pi / 5 - np.pi / 2
            p = (int(cx + 42 * np.cos(g)), int(cy + 42 * np.sin(g)))
            cv2.circle(im, p, 26, PAL["hoa"], -1, cv2.LINE_AA)
        cv2.circle(im, (cx, cy), 20, INK, -1, cv2.LINE_AA)
        cv2.circle(im, (cx, cy), 13, PAL["mo"], -1, cv2.LINE_AA)
    elif ten == "mam":                                               # mầm hai lá trên cuống ngắn
        cx = w // 2
        cv2.line(im, (cx, h - 14), (cx, h - 86), INK, 22, cv2.LINE_AA)
        cv2.line(im, (cx, h - 14), (cx, h - 86), PAL["reu"], 10, cv2.LINE_AA)
        for sg in (-1, 1):
            P, c = CL.la_hinh((cx, h - 84), (cx + sg * 84, 34), 30, 0.22 * sg)
            cv2.fillPoly(im, [np.int32(P)], PAL["la_nhat"], cv2.LINE_AA)
            cv2.polylines(im, [np.int32(P)], True, INK, 9, cv2.LINE_AA)
            cv2.polylines(im, [np.int32(c[4:-4])], False, PAL["gan"], 4, cv2.LINE_AA)
    return im, im.min(axis=2) < 236


# ---------------------------------------------------------------- nhóm tờ
def _ds(dk):
    return [t for t in by() if dk(ngan(t), CL.loai(t))]


def nhom_to():
    """{nhóm: [(tên vùng, z)]}."""
    G = {
        "la_gan": [(t, 3.2) for t in _ds(lambda s, nh: nh == "la" and s.startswith(("chibangR1", "chibangR2")))],
        "la_xa": [(t, 3.2) for t in _ds(lambda s, nh: nh == "la" and s.startswith("chiabangL"))],
        "la_lat": [(t, 2.6) for t in _ds(lambda s, nh: nh == "la" and s.startswith("chibangR3"))],
        "tan": [(t, 2.4) for t in _ds(lambda s, nh: nh == "tan" and not s.startswith("chibangR3"))],
        "tan_lat": [(t, 2.6) for t in _ds(lambda s, nh: s.startswith("chibangR3") and nh in ("tan", "canh"))],
        "canh": [(t, 3.0) for t in _ds(lambda s, nh: nh in ("canh", "choi") and not s.startswith("chibangR3"))],
        "duoi": [(t, 2.2) for t in _ds(lambda s, nh: nh == "duoi")],
        "da": [(t, 3.4) for t in _ds(lambda s, nh: nh in ("da", "da_to", "da_ngon"))],
        "dau": ([("P_tou_01", 5.0), ("P_zui_01", 8.0), ("P_zui_02", 8.0), ("P_mao_01", 3.4)]
                + [(t, 3.2) for t in _ds(lambda s, nh: nh in ("la_co", "dui"))] + [(t, 5.0) for t in _ds(lambda s, nh: nh == "bua")]),
        "chan": [(t, 5.0) for t in _ds(lambda s, nh: nh in ("chan", "vuot"))],
        "X": [(t, 1.0) for t in THEM],
    }
    return G


LIEN = ["P_xiashen", "P_xiong", "P_mao_02"]         # một bề mặt nối nhau: gen liền (tờ L) rồi nướng vào khung part
Z_LIEN = 4.0
BO = ("P_yanjing_01", "P_yanjing_02", "P_shetou_01") + tuple("P_toushi_%02d" % i for i in range(1, 10))   # mắt vẽ trong ảnh đầu; lưỡi, mào của họ bỏ


def xep(items, le=26):
    """xếp ô theo kệ (ô cao trước); trả [tờ] mỗi tờ = {tên: (x, y, w, h, z)}; tự tách tờ khi đầy."""
    cells = []
    for ten, z in items:
        w, h = THEM[ten] if ten in THEM else co_o(ten, z)
        cells.append((ten, z, w, h))
    cells.sort(key=lambda c: -c[3])
    tos, cur, x, y, hh = [], {}, le, le, 0
    for ten, z, w, h in cells:
        if w + 2 * le > W or h + 2 * le > H:
            raise SystemExit(f"ô {ten} quá to ({w} x {h}), giảm z")
        if x + w + le > W:
            x, y, hh = le, y + hh + le, 0
        if y + h + le > H:
            tos.append(cur)
            cur, x, y, hh = {}, le, le, 0
        cur[ten] = (x, y, w, h, z)
        x += w + le
        hh = max(hh, h)
    if cur:
        tos.append(cur)
    return tos


def ds_to():
    """[(mã tờ, nhóm, {tên: (x, y, w, h, z)})]."""
    out = []
    for g, items in nhom_to().items():
        tos = xep(items)
        for i, kh in enumerate(tos):
            out.append((g if len(tos) == 1 else f"{g}{i + 1}", g, kh))
    return out


def dung_to(chi=None):
    os.makedirs(MAU, exist_ok=True)
    muc = {}
    for ma, g, kh in ds_to():
        muc[ma] = g
        if chi and g not in chi:
            continue
        im = np.full((H, W, 3), 255, np.uint8)
        for ten, (x, y, w, h, z) in kh.items():
            cell, m = o_them(ten) if ten in THEM else thiet_ke(ten, z)
            im[y:y + h, x:x + w] = cell
        Image.fromarray(im).save(os.path.join(MAU, f"part_{ma}.png"))
        json.dump({t: {"x": v[0], "y": v[1], "w": v[2], "h": v[3], "z": v[4]} for t, v in kh.items()},
                  open(os.path.join(MAU, f"part_{ma}.json"), "w", encoding="utf-8"), indent=1)
        muc[ma] = g
        print(f"{ma}: {len(kh)} ô ·", ", ".join(f"{ngan(t)} {v[2]}x{v[3]}" for t, v in list(kh.items())[:6]), "…" if len(kh) > 6 else "")
    json.dump(muc, open(os.path.join(MAU, "part_muc.json"), "w"), indent=1)
    if not chi:
        to_lien()
    return muc


# ---------------------------------------------------------------- THÂN LIỀN
def to_lien():
    B = by()
    P = np.concatenate([np.array(B[t]["xy"], float).reshape(-1, 2) for t in LIEN])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    ti = min((H - 90) / (y1 - y0), (W - 90) / (x1 - x0))
    ox = W / 2 - (x0 + x1) / 2 * ti
    oy = H / 2 + (y0 + y1) / 2 * ti
    S2 = 2
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    T2 = lambda p_: np.stack([ox + np.asarray(p_, float)[..., 0] * ti, oy - np.asarray(p_, float)[..., 1] * ti], -1)
    m = np.zeros((H * S2, W * S2), bool)
    for t in LIEN:
        m |= CL.bong_khung(B[t], T2, 3.0)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(6))
    m = cv2.GaussianBlur(m * 255, (0, 0), 9.0) > 127                  # ảnh vùng nhỏ phóng ~11 lần: làm trơn mép bậc thang
    can[m] = PAL["long"]
    # mảng rêu trên bụng: chỗ con gốc có mảng vảy (giữa – phải khung P_xiashen)
    a = B["P_xiashen"]
    U = np.array(a["uv"], float).reshape(-1, 2)
    V = np.array(a["xy"], float).reshape(-1, 2)
    A_ = np.c_[U, np.ones(len(U))]
    M_ = np.linalg.lstsq(A_, V, rcond=None)[0]                        # uv → thế giới (xấp xỉ affine)
    c = np.array([0.70, 0.47, 1.0]) @ M_
    cp = T2(c) * S2
    reu = np.zeros(m.shape, np.uint8)
    cv2.ellipse(reu, (int(cp[0]), int(cp[1])), (int(58 * ti * S2), int(42 * ti * S2)), 20, 0, 360, 1, -1)
    reu = reu.astype(bool) & cv2.erode(m.astype(np.uint8), el(14)).astype(bool)
    can[reu] = PAL["reu"]
    can[cv2.morphologyEx(reu.astype(np.uint8), cv2.MORPH_GRADIENT, el(3)).astype(bool)] = INK
    can[CL.vien(m, int(round(8.0 * ti * S2)))] = INK
    Image.fromarray(can).resize((W, H), Image.LANCZOS).save(os.path.join(MAU, "lien.png"))
    json.dump({"ti": ti, "ox": ox, "oy": oy, "nhom": LIEN}, open(os.path.join(MAU, "lien.json"), "w"), indent=1)
    print(os.path.join(MAU, "lien.png"), f"{ti:.3f} px mỗi đơn vị rig")


def cat_lien():
    from quai import anh
    import glob
    import re
    # tên phải đúng N_L.png hoặc N_L_<số>.png (glob "N_L*" trên Windows không phân biệt hoa thường, ăn nhầm N_la_*.png: đã gặp)
    fs = [f for f in glob.glob(os.path.join(TAI, "N_L*.png")) if re.fullmatch(r"N_L(_\d+)?\.png", os.path.basename(f))]
    if not fs:
        raise SystemExit("chưa có N_L.png")
    path = max(fs, key=os.path.getmtime)
    L = json.load(open(os.path.join(MAU, "lien.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(MAU, "_N_L_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=600, gop_px=10)
    rgba = tt.rgba.astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:4] / 255.0
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    ti, ox, oy = L["ti"], L["ox"], L["oy"]
    print(os.path.basename(path))
    for ten in L["nhom"]:
        a = by()[ten]
        w, h = co_o(ten, Z_LIEN)
        Wd = the_gioi_o(a, w, h)
        ok = ~np.isnan(Wd[..., 0])
        mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
        my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
        cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        al = cell[..., 3:4]
        cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
        # mép của mảnh nằm TRONG khối thân (đè lên mảnh kề cùng màu) để ĐẶC, gần như không mờ: dải nửa trong suốt kem-đè-kem hiện
        # thành một vệt chấm sáng mảnh ở trang xem Spine (đã thấy ở ranh ngực – bụng). Mép ngoài của khối thì do alpha của chính tờ
        # thân liền quyết định (hình bóng nới rộng hơn nét viền).
        sil = cv2.dilate(bong(ten, Z_LIEN).astype(np.uint8), el(1.3 * Z_LIEN)).astype(np.float32)
        sil = np.clip(cv2.GaussianBlur(sil, (0, 0), 0.12 * Z_LIEN) * 2.0 - 0.5, 0.0, 1.0)
        cell[..., 3] = np.where(sil > 0.5, np.where(cell[..., 3] > 200, 255.0, cell[..., 3]), cell[..., 3] * sil)
        out = np.clip(cell, 0, 255).astype(np.uint8)
        Image.fromarray(out, "RGBA").save(os.path.join(ra, ten + ".png"))
        phu = float((out[..., 3] > 127).sum()) / max(1, int(bong(ten, Z_LIEN).sum()))
        print(f"  {ngan(ten)}: {w} x {h}, phủ {phu:.2f} hình bóng của part")
    zs = json.load(open(os.path.join(ra, "_z.json"))) if os.path.exists(os.path.join(ra, "_z.json")) else {}
    zs.update({t: Z_LIEN for t in L["nhom"]})
    json.dump(zs, open(os.path.join(ra, "_z.json"), "w"), indent=0)


# ---------------------------------------------------------------- cắt tờ đã gen
def cat_to(ma, ep=False):
    from quai import anh
    path = anh.to_moi_nhat(TAI, f"N_{ma}")
    if not path or os.path.basename(path)[2:].split(".")[0].split("_")[0] != ma.split("_")[0] and False:
        print(ma, "chưa có ảnh")
        return
    # tránh nhầm N_la_gan1 với N_la_gan10...: tên phải là N_<mã>.png hoặc N_<mã>_<số>.png
    import glob
    import re
    fs = [f for f in glob.glob(os.path.join(TAI, f"N_{ma}*.png")) if re.fullmatch(rf"N_{re.escape(ma)}(_\d+)?\.png", os.path.basename(f))]
    if not fs:
        print(ma, "chưa có ảnh")
        return
    path = max(fs, key=os.path.getmtime)
    khung = json.load(open(os.path.join(MAU, f"part_{ma}.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path2 = os.path.join(MAU, f"_N_{ma}_doi_co.png")
        im.save(path2)
    else:
        path2 = path
    tt = anh.doc_to(path2, dien_tich_min=120, gop_px=10)
    gd = np.asarray(Image.open(os.path.join(MAU, f"part_{ma}.png")).convert("RGB"))
    ra = os.path.join(MANH, "part")
    os.makedirs(ra, exist_ok=True)
    pso, pz = os.path.join(ra, "_iou.json"), os.path.join(ra, "_z.json")
    SO = json.load(open(pso, encoding="utf-8")) if os.path.exists(pso) else {}
    ZS = json.load(open(pz)) if os.path.exists(pz) else {}
    ids = set(i for m_ in tt.manh for i in m_["ids"])
    print(os.path.basename(path))
    kem = []
    for ten, kv in khung.items():
        x, y, w, h, z = kv["x"], kv["y"], kv["w"], kv["h"], kv["z"]
        g = gd[y:y + h, x:x + w].min(axis=2) < 236
        them = ten in THEM
        d = 16 if them else 0
        x0, y0, x1, y1 = max(0, x - d), max(0, y - d), min(W, x + w + d), min(H, y + h + d)
        cell = tt.rgba[y0:y1, x0:x1].copy()
        lab = tt.lab[y0:y1, x0:x1]
        gg = np.zeros(lab.shape, bool)
        gg[y - y0:y - y0 + h, x - x0:x - x0 + w] = g
        giu = np.zeros(lab.shape, bool)
        for i in set(lab[gg].ravel().tolist()) - {0}:
            if i in ids or True:
                giu |= lab == i
        cell[..., 3] = (cell[..., 3] * anh.gian(giu, 2)).astype(np.uint8)
        a = cell[..., 3] > 127
        iou = (a & gg).sum() / max(1, (a | gg).sum())
        cu = SO.get(ten, [0, ""])
        if not ep and cu[1] and cu[0] >= iou:
            print(f"  {ngan(ten)}: IoU {iou:.2f}, giữ bản cũ (IoU {cu[0]:.2f})")
            continue
        bu = 0
        if not them:
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
                    # chỗ vẽ hụt nằm ở VÀNH MÉP hình bóng (GPT vẽ nhỏ hơn hình bóng một chút): tô mực, không tô màu, kẻo thành một dải
                    # màu sáng nằm NGOÀI nét viền của GPT (đã gặp ở mép phải đầu chim)
                    vanh = g & ~cv2.erode(g.astype(np.uint8), el(3.0 * z)).astype(bool)
                    cell[ho & vanh, :3] = INK
            if CL.loai(ten) != "canh":                                    # (cành: rig gắn ô cả khung, không cắt theo lưới của họ)
                at = by()[ten]                                            # nét mực dọc phía trong mép lưới của họ
                hull = np.array(at["uv"], float).reshape(-1, 2)[:at["hull"]] * np.array([w, h])
                hm = np.zeros(a.shape, np.uint8)
                cv2.fillPoly(hm, [np.round(hull).astype(np.int32)], 1)
                dai = hm.astype(bool) & ~cv2.erode(hm, el(1.0 * z), borderValue=0).astype(bool)
                cell[dai & (cell[..., 3] > 127), :3] = INK
        SO[ten] = [round(float(iou), 3), os.path.basename(path)]
        ZS[ten] = z
        Image.fromarray(cell, "RGBA").save(os.path.join(ra, ten + ".png"))
        if iou < 0.9 and not them:
            kem.append(f"{ngan(ten)} {iou:.2f}")
    json.dump(SO, open(pso, "w", encoding="utf-8"), indent=1)
    json.dump(ZS, open(pz, "w"), indent=0)
    v = [SO[t][0] for t in khung if t in SO and t not in THEM]
    if v:
        print(f"  {len(khung)} ô; IoU nhỏ nhất {min(v):.2f}, trung vị {float(np.median(v)):.2f}" + (f"; DƯỚI 0,9: {', '.join(kem)}" if kem else ""))


def so_part():
    cells = []
    for ma, g, kh in ds_to():
        pj = os.path.join(MAU, f"part_{ma}.png")
        if not os.path.exists(pj):
            continue
        gd = np.asarray(Image.open(pj).convert("RGB"))
        for ten, (x, y, w, h, z) in kh.items():
            pm = os.path.join(MANH, "part", ten + ".png")
            if not os.path.exists(pm) or ten in THEM:
                continue
            g_ = gd[y:y + h, x:x + w].min(axis=2) < 236
            c = np.asarray(Image.open(pm).convert("RGBA").resize((w, h)))
            a = c[..., 3] > 127
            im = np.full((h, w, 3), 255, np.uint8)
            im[a] = c[..., :3][a]
            im[g_ & ~a] = (255, 0, 0)
            im[a & ~g_] = (im[a & ~g_] * 0.5 + np.array([0, 255, 0]) * 0.5).astype(np.uint8)
            k = 0.5
            im = cv2.resize(im, (max(8, int(w * k)), max(8, int(h * k))), interpolation=cv2.INTER_AREA)
            cv2.putText(im, ngan(ten)[-9:], (2, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 0, 0), 1)
            cells.append(im)
    Wd, x, y, hh, pos = 1900, 0, 0, 0, []
    for im in cells:
        h, w = im.shape[:2]
        if x + w > Wd:
            x, y, hh = 0, y + hh + 8, 0
        pos.append((x, y))
        x += w + 8
        hh = max(hh, h)
    S = np.full((y + hh, Wd, 3), 230, np.uint8)
    for im, (x, y) in zip(cells, pos):
        S[y:y + im.shape[0], x:x + min(im.shape[1], Wd - x)] = im[:, :Wd - x]
    Image.fromarray(S).save(os.path.join(MAU, "so_part.png"))
    print(os.path.join(MAU, "so_part.png"), len(cells), "ô")


def main(a):
    if a[:1] == ["to"]:
        dung_to(a[1:] or None)
    elif a[:1] == ["cat"]:
        ds = [x for x in a[1:] if x != "ep"] or [m for m, _, _ in ds_to()]
        for ma in ds:
            cat_to(ma, ep="ep" in a)
    elif a[:1] == ["lien"]:
        cat_lien()
    elif a[:1] == ["so"]:
        so_part()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
