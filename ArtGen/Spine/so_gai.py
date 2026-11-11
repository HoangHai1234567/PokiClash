# -*- coding: utf-8 -*-
"""Dòng sò đột biến (mã làm việc so_gai, tướng thứ 4 đảo Thủy, 2026-11-11): cắt concept, cắt tờ mảnh GPT, dựng rig.

    py -3 -I ArtGen/Spine/so_gai.py to                 cắt tờ mảnh M01 (lưỡi dài, lòng miệng, môi chu, hai mí, ngọc trai) -> inbox/so_gai_1/to/
    py -3 -I ArtGen/Spine/so_gai.py cat 1|2            cắt concept dạng k -> inbox/so_gai_<k>/manh/ (+ manh.json, _soi.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/so_gai.py rig 1|2    rig một dạng (không evolve) -> inbox/so_gai_<k>/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/so_gai.py all        dạng 2 rồi dạng 1 gộp dạng 2 (evolve)

Cách cắt (khớp concept 100 %): phân lớp theo màu rồi loang từ hạt giống: MAI TRÊN (lam lục / chàm, kèm mắt, nanh trên, gai, u hà,
vành cam trên), MAI DƯỚI (xà cừ, kèm vành cam dưới, nanh dưới, gai), TRONG MIỆNG (tím than + lưỡi hồng). Hai mai là mảnh cứng xoay
quanh bản lề phía sau như con gốc; quanh bản lề hai mảnh chồng nhau một đĩa nhỏ nên xoay không hở. Lòng miệng = mảng tím của
concept + vòm tím GPT nối ra phía sau mai trên (lộ ra khi há). Lưỡi lúc nghỉ cắt từ concept (vá chỗ nanh che); lưỡi dài để quật,
môi chu, mí mắt lấy từ tờ GPT. Ghi chú: inbox/so_gai_ghichu.md.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ti_tach as T  # noqa: E402  (nen_trang, cum, lap_lo, gian, co, luu, hop, moi_nhat, ln, spl, _quai)

sys.stdout.reconfigure(encoding="utf-8")
CODE = "so_gai"
GRAY = (150, 150, 150)
FONT = "C:/Windows/Fonts/arial.ttf"


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def concept(k):
    return os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")


# ================================================================ tờ mảnh GPT
def cat_to():
    thu = os.path.join(d_inbox(1), "tai_ve")
    src = T.moi_nhat(thu, "M01")
    if not src:
        raise SystemExit("chưa có tờ M01 trong " + thu)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    H = a.shape[0]
    bg = T.nen_trang(a, 240)
    cs = T.cum(~bg, 1500)
    tren = [c for c in cs if (c["y0"] + c["y1"]) / 2 < H * 0.48]
    duoi = sorted([c for c in cs if (c["y0"] + c["y1"]) / 2 >= H * 0.48], key=lambda c: c["x0"])
    if len(tren) != 1 or len(duoi) != 5:
        raise SystemExit(f"tờ mảnh: cần 1 mảnh trên + 5 mảnh dưới, thấy {len(tren)} + {len(duoi)}")
    ra = os.path.join(d_inbox(1), "to")
    os.makedirs(ra, exist_ok=True)
    info = {}
    for ten, c in zip(["luoi_dai", "long", "moi", "mi_g", "mi_x", "ngoc"], tren + duoi):
        m = T.lap_lo(c["m"])
        al = np.where(T.co(m, 2), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7))
        box = T.hop(m)
        T.luu(a, al, box, os.path.join(ra, ten + ".png"))
        info[ten] = box
    src2 = T.moi_nhat(thu, "M02")
    if src2:                                                                           # lưỡi gen lại riêng (tờ M01 ra như cây xúc xích)
        a2 = np.array(Image.open(src2).convert("RGB")).astype(np.float32)
        c2 = max(T.cum(~T.nen_trang(a2, 240), 1500), key=lambda c: c["dt"])
        m2 = T.lap_lo(c2["m"])
        al2 = np.where(T.co(m2, 2), 1.0, cv2.GaussianBlur(m2.astype(np.float32), (0, 0), 0.7))
        info["luoi_dai"] = T.hop(m2)
        T.luu(a2, al2, info["luoi_dai"], os.path.join(ra, "luoi_dai.png"))
        info["luoi_tu"] = os.path.basename(src2)
    src3 = T.moi_nhat(thu, "M03")
    if src3:                                                                           # môi chu: hai vành ép vào nhau, phồng ở giữa
        a3 = np.array(Image.open(src3).convert("RGB")).astype(np.float32)
        c3 = max(T.cum(~T.nen_trang(a3, 240), 1500), key=lambda c: c["dt"])
        m3 = T.lap_lo(c3["m"])
        al3 = np.where(T.co(m3, 2), 1.0, cv2.GaussianBlur(m3.astype(np.float32), (0, 0), 0.7))
        b3 = T.hop(m3)
        w3 = b3[2] - b3[0]
        cot = m3[:, b3[0] + int(0.06 * w3):b3[0] + int(0.16 * w3)].sum(0)               # bề cao dải kép ở đầu trái (chưa phồng)
        info["moi_chu"] = [b3[0] + int(0.15 * w3), b3[1], b3[2] - int(0.15 * w3), b3[3]]   # bỏ bớt hai đầu dải, giữ chỗ phồng + chút dải
        info["moi_chu_dai"] = float(np.median(cot))
        x0m, x1m = info["moi_chu"][0], info["moi_chu"][2]
        doc = np.clip(np.minimum(np.arange(a3.shape[1]) - x0m, x1m - 1 - np.arange(a3.shape[1])) / (0.14 * (x1m - x0m)), 0, 1)
        al3 = al3 * (doc * doc * (3 - 2 * doc))[None, :]
        T.luu(a3, al3, info["moi_chu"], os.path.join(ra, "moi_chu.png"))
    json.dump(info, open(os.path.join(ra, "to.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("tờ mảnh:", {k: (v[2] - v[0], v[3] - v[1]) for k, v in info.items() if isinstance(v, list)}, info.get("luoi_tu", "lưỡi từ M01"))


# ================================================================ cắt concept
def phan_lop(a, bg):
    """nhãn từng pixel: 0 nền, 1 mai trên, 2 mai dưới, 3 trong miệng. Trả (nhãn, mực, hồng, tím)."""
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    fg = ~bg
    tim = (R > G + 8) & (B > G + 18) & (mx < 125) & fg                                   # tím than trong miệng
    hong = (R > 165) & (G < 140) & (B > 75) & (B < 200) & (R - G > 65) & (B > G - 12) & fg   # lưỡi (cả đường giữa đậm)
    trong0 = tim | hong
    muc = (mx < 100) & (B < R + 25) & fg & ~tim                                          # nét mực nâu, con ngươi
    lam = (B > R + 45) & (mx > 60) & fg                                                  # lam lục, chàm: mai trên
    xacu = (mn > 165) & (np.abs(R - B) < 22) & (G < R + 6) & fg                          # xà cừ, tím nhạt: mai dưới
    lab = np.zeros(a.shape[:2], np.uint8)
    for v, m in ((1, lam), (2, xacu)):
        for c in T.cum(m, 3000):
            lab[c["m"]] = v
    di = fg & ~trong0                                                                    # vùng được loang (cả nét mực)
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(4000):
        moi = False
        for v in (1, 2):
            g = (cv2.dilate((lab == v).astype(np.uint8), k3) > 0) & di & (lab == 0)
            if g.any():
                lab[g] = v
                moi = True
        if not moi:
            break
    # nét mực nằm xa phần màu của mai (viền lưỡi, viền lòng miệng) thuộc về trong miệng
    nhu_muc = (mx < 150) & (mx - mn < 75) & (B < R + 25) & fg & ~tim                  # mực và rìa mực (xám nâu, không phải chàm)
    for v in (1, 2):
        vo = (lab == v) & ~nhu_muc
        xa = cv2.distanceTransform((~vo).astype(np.uint8), cv2.DIST_L2, 5)
        lab[(lab == v) & nhu_muc & (xa > 9)] = 3
    lab[trong0] = 3
    lab[fg & (lab == 0)] = 3
    # mảng "trong miệng" lẻ, toàn mực, nằm lọt trong một mai (lõi nét mày dày, lõi con ngươi): trả về mai đó
    n, cl, st, _ = cv2.connectedComponentsWithStats((lab == 3).astype(np.uint8), connectivity=8)
    if n > 2:
        chinh = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        for i in range(1, n):
            if i == chinh:
                continue
            m = cl == i
            if trong0[m].mean() > 0.2:
                continue
            v = np.bincount(lab[T.gian(m, 2) & ~m], minlength=4)
            if v[1] + v[2] > 0:
                lab[m] = 1 if v[1] >= v[2] else 2
    ke = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    for v in (1, 2):
        m = (lab == v).astype(np.uint8)
        day = cv2.dilate(cv2.morphologyEx(m, cv2.MORPH_OPEN, ke), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
        lab[(m > 0) & ~day] = 3
    # mẩu "trong miệng" lẻ không dính với khoang miệng chính (chóp gai mảnh, mép sẹo vừa bị bỏ ở bước trên): trả về mai kề nó
    n, cl, st, _ = cv2.connectedComponentsWithStats((lab == 3).astype(np.uint8), connectivity=8)
    if n > 2:
        chinh = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        for i in range(1, n):
            if i == chinh:
                continue
            m = cl == i
            v = np.bincount(lab[T.gian(m, 2) & ~m], minlength=4)
            if v[1] + v[2] > 0:
                lab[m] = 1 if v[1] >= v[2] else 2
    for v in (1, 2):                                                                   # mẩu vụn rời của một mai (nét mực lẻ): bỏ hẳn
        n, cl, st, _ = cv2.connectedComponentsWithStats((lab == v).astype(np.uint8), connectivity=8)
        if n > 2:
            chinh = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            for i in range(1, n):
                if i != chinh and st[i, cv2.CC_STAT_AREA] < 0.02 * st[chinh, cv2.CC_STAT_AREA]:
                    lab[cl == i] = 0
    return lab, muc, hong, tim


def ghep_ham(k, a, bg, U, L, I, de, info, ra):
    """HÀM DƯỚI theo đúng cách con gốc tách (người dùng 2026-11-11: "xem hàm dưới con gốc làm như nào làm y hệt"): con gốc có MẢNH
    TRƯỚC (mặt ngoài cái bát, vành gần ở mép trên) và MẢNH SAU (nửa đĩa tối, đường vành xa ở mép trên) kẹp cái lưỡi ở giữa.
    Ảnh H01 (GPT vẽ lại concept chỉ còn mai dưới, thấy lòng bát + vành xa) được căn trùng mặt bát của concept rồi tách:
      - mảnh sau `long` = lòng bát tím + vành xa của H01 (nanh dưới đứng trước lòng bát thì tô tím; nối xuống 28 px sau mặt trước);
      - mảnh trước giữ pixel concept; chỗ chóp lưỡi che vành (dạng 2) lấy vành liền của H01, chóp lưỡi thành mảnh rời `luoi_mep`.
    Không có H01 thì giữ lòng bát vẽ bằng mã. Trả True nếu đã ghép."""
    src = T.moi_nhat(os.path.join(d_inbox(k), "tai_ve"), "H01")
    if not src:
        return False
    Hh, Ww = a.shape[:2]
    g = np.array(Image.open(src).convert("RGB").resize((Ww, Hh), Image.LANCZOS)).astype(np.float32)

    def xa_cu(x):
        return (x.min(2) > 165) & (np.abs(x[..., 0] - x[..., 2]) < 22) & (x[..., 1] < x[..., 0] + 6)

    def hopm(m):
        ys, xs = np.nonzero(m)
        return float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max())

    bgG = T.nen_trang(g)
    pc = L & xa_cu(a)
    than_g = max(T.cum(~bgG, 3000), key=lambda c: c["dt"])["m"]                       # cả cái mai dưới trong H01
    pg = cv2.morphologyEx((than_g & xa_cu(g)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    pc = cv2.morphologyEx(pc.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    if pg.sum() < 5000 or pc.sum() < 5000:
        print("  hàm dưới H01: không thấy mặt bát để căn, bỏ qua")
        return False
    c_, q_ = hopm(pc), hopm(pg)
    s0 = (c_[1] - c_[0]) / (q_[1] - q_[0])
    pcs = cv2.resize(pc.astype(np.uint8), (Ww // 2, Hh // 2), interpolation=cv2.INTER_NEAREST) > 0
    pgs = cv2.resize(pg.astype(np.uint8), (Ww // 2, Hh // 2), interpolation=cv2.INTER_NEAREST)

    def iou(sc, tx, ty):
        w = cv2.warpAffine(pgs, np.float32([[sc, 0, tx / 2], [0, sc, ty / 2]]), (Ww // 2, Hh // 2), flags=cv2.INTER_NEAREST) > 0
        return float((w & pcs).sum()) / max(1.0, float((w | pcs).sum()))

    tot = (iou(1.0, 0.0, 0.0), 1.0, 0.0, 0.0)                                           # GPT thường giữ nguyên chỗ: thử trước dáng không đổi
    for sc in s0 * np.arange(0.95, 1.055, 0.01):
        tx0 = (c_[0] + c_[1]) / 2 - sc * (q_[0] + q_[1]) / 2
        ty0 = (c_[2] + c_[3]) / 2 - sc * (q_[2] + q_[3]) / 2
        for dx in range(-16, 17, 4):
            for dy in range(-16, 17, 4):
                v = iou(sc, tx0 + dx, ty0 + dy)
                if v > tot[0]:
                    tot = (v, sc, tx0 + dx, ty0 + dy)
    _, sc, tx, ty = tot
    for dx in range(-4, 5, 2):
        for dy in range(-4, 5, 2):
            v = iou(sc, tx + dx, ty + dy)
            if v > tot[0]:
                tot = (v, sc, tx + dx, ty + dy)
    v, sc, tx, ty = tot
    G = cv2.warpAffine(g, np.float32([[sc, 0, tx], [0, sc, ty]]), (Ww, Hh), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    fg = ~T.nen_trang(G)
    Rg, Gg, Bg = G[..., 0], G[..., 1], G[..., 2]
    tim_g = (Rg > Gg + 8) & (Bg > Gg + 18) & (G.max(2) < 125) & fg
    cs = T.cum(cv2.morphologyEx(tim_g.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)) > 0, 2000)
    if not cs:
        print("  hàm dưới H01: không thấy lòng bát tím, bỏ qua")
        return False
    Pm = max(cs, key=lambda c: c["dt"])["m"]
    tim_mau = np.median(G[Pm & tim_g], 0)
    rng = np.random.default_rng(11)
    cols = np.nonzero(Pm.any(0))[0]
    sau = np.zeros((Hh, Ww), bool)
    long_ = np.zeros((Hh, Ww), bool)                                                   # phần lòng bát (dưới vành xa): chỗ không tím thì tô tím
    yt = {}
    for x in cols:
        pm = np.nonzero(Pm[:, x])[0]
        ypt, ypb = int(pm.min()), int(pm.max())
        cf = np.nonzero(fg[:ypt + 1, x])[0]
        t0 = int(cf.min()) if len(cf) else ypt
        if ypt - t0 > 90:                                                              # trên lòng bát mà cao bất thường: không phải vành xa (gai, nút bản lề)
            run = np.nonzero(~fg[:ypt, x])[0]
            t0 = int(run.max()) + 1 if len(run) else ypt
        yt[int(x)] = t0
        sau[t0:min(Hh, ypb + 29), x] = True
        long_[ypt:min(Hh, ypb + 29), x] = True
    for x in list(range(max(0, int(cols.min()) - 50), int(cols.min()))) + list(range(int(cols.max()) + 1, min(Ww, int(cols.max()) + 51))):
        xn = int(cols.min()) if x < cols.min() else int(cols.max())                    # hai đầu, ngoài lòng bát: lấy đúng phần hình của H01
        day = min(Hh, int(np.nonzero(Pm[:, xn])[0].max()) + 29)
        cf = np.nonzero(fg[:day, x])[0]
        if len(cf):
            sau[int(cf.min()):day, x] = fg[int(cf.min()):day, x]
    img = G.copy()
    doi = long_ & ~tim_g
    img[doi] = np.clip(tim_mau + rng.normal(0, 3.5, (int(doi.sum()), 1)), 0, 255)
    # vành xa phải khuất sau mai trên lúc nghỉ: nếu thấp hơn mép trên vùng miệng thì kéo giãn lớp sau theo chiều dọc (neo ở đáy)
    can = []
    for x in cols:
        ii = np.nonzero(I[:, x])[0]
        if len(ii):
            day = float(np.nonzero(sau[:, x])[0].max())
            can.append((day - (ii.min() - 16)) / max(1.0, day - yt[int(x)]))
    sy = float(min(1.6, max(1.0, np.percentile(can, 92)))) if can else 1.0
    ys, xs = np.nonzero(sau)
    X0, X1, Y0, Y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    lop = np.dstack([img[Y0:Y1, X0:X1], 255.0 * sau[Y0:Y1, X0:X1]]).astype(np.float32)
    if sy > 1.02:
        lop = cv2.resize(lop, (X1 - X0, int(round((Y1 - Y0) * sy))), interpolation=cv2.INTER_LINEAR)
        Y0 = Y1 - lop.shape[0]
    cav = np.zeros((Hh, Ww, 4), np.float32)
    y_a, y_b = max(0, Y0), Y1
    cav[y_a:y_b, X0:X1] = lop[y_a - Y0:]
    than_ = T.co(T.lap_lo(U | L | I | de), 2)
    # chỗ lớp sau cao quá bóng thân lúc nghỉ (đầu miệng phía trước, nơi mai trên chỉ còn cái vành): ÉP từng cột xuống cho vừa (hệ số
    # làm trơn dọc chiều ngang) để vành xa lượn theo mép trong của mai trên, thay vì bị cắt khuyết
    kin0 = cav[..., 3] > 128
    cs_x = np.nonzero(kin0.any(0))[0]
    hs = np.ones(Ww)
    tops, days = {}, {}
    for x in cs_x:
        rr = np.nonzero(kin0[:, x])[0]
        t_, d_ = int(rr.min()), int(rr.max())
        tops[int(x)], days[int(x)] = t_, d_
        ngoai_ = np.nonzero(~than_[t_:d_ + 1, x])[0]                                    # đi từ đáy lên: hàng thấp nhất nằm ngoài bóng thân
        ya = t_ + int(ngoai_.max()) + 4 if len(ngoai_) else t_
        if t_ < ya and d_ > t_:
            hs[x] = max(0.05, (d_ - ya) / float(d_ - t_))
    if (hs < 0.999).any():
        hm = np.array([hs[max(0, q - 14):q + 15].min() for q in range(Ww)])
        gk = np.exp(-0.5 * (np.arange(-30, 31) / 10.0) ** 2)
        hsm = np.minimum(hm, np.convolve(np.pad(hm, 30, mode="edge"), gk / gk.sum(), mode="valid"))
        moi_ = np.zeros_like(cav)
        for x in cs_x:
            t_, d_ = tops[int(x)], days[int(x)]
            f_ = float(hsm[x])
            if f_ > 0.999:
                moi_[t_:d_ + 1, x] = cav[t_:d_ + 1, x]
                continue
            t2 = int(round(d_ - f_ * (d_ - t_)))
            if d_ - t2 < 2:
                continue
            src_r = t_ + (np.arange(t2, d_ + 1) - t2) / float(d_ - t2) * (d_ - t_)
            lo_, fr_ = np.floor(src_r).astype(int), src_r - np.floor(src_r)
            hi_ = np.minimum(lo_ + 1, d_)
            moi_[t2:d_ + 1, x] = cav[lo_, x] * (1 - fr_)[:, None] + cav[hi_, x] * fr_[:, None]
        cav = moi_
    kin = cav[..., 3] > 128
    loi = int((kin & ~than_).sum())
    cav[..., 3] *= than_                                                               # lúc nghỉ không lòi ra ngoài thân
    co_ = cav[..., 3] > 128
    dinh_ = np.where(co_.any(0), np.argmax(co_, 0), Hh + 1)                            # mép trên của lớp sau theo cột
    thieu = I & ~co_ & (np.arange(Hh)[:, None] >= dinh_[None, :])                      # lỗ nằm DƯỚI vành xa: tô tím (phần trên vành xa ở khoé miệng để cho mai trên)
    cav[thieu, :3] = np.clip(tim_mau + rng.normal(0, 3.5, (int(thieu.sum()), 1)), 0, 255)
    cav[thieu, 3] = 255
    m = cav[..., 3] > 10
    day_ = cv2.dilate(cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))),
                      cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
    cs_ = T.cum(m & day_, 200)
    m = max(cs_, key=lambda c: c["dt"])["m"] if cs_ else m                               # bỏ sợi mảnh, mẩu rời (kẻo bay lơ lửng khi há)
    cav[..., 3] *= m
    # vùng miệng lúc nghỉ mà lớp sau không phủ (mẩu vách ở khoé miệng, ngay dưới đầu vành trên): cho vào MAI TRÊN (mặt trong của mép
    # mai trên) để dáng nghỉ kín mà lúc há không thành mẩu tím bay theo mai dưới
    sot = np.zeros_like(m)
    for c in T.cum(I & ~m, 100):
        if (T.gian(c["m"], 5) & U).any():
            sot |= c["m"]
    info["manh"].pop("khoe", None)
    if sot.any():
        kh = np.zeros((Hh, Ww, 4), np.float32)
        kh[sot, :3] = np.clip(tim_mau + rng.normal(0, 3.5, (int(sot.sum()), 1)), 0, 255)
        kh[..., 3] = 255.0 * T.gian(sot, 1)
        kh[T.gian(sot, 1) & ~sot, :3] = tim_mau
        bk = T.hop(T.gian(sot, 1))
        Image.fromarray(np.clip(kh[bk[1]:bk[3], bk[0]:bk[2]], 0, 255).astype(np.uint8), "RGBA").save(os.path.join(ra, "khoe.png"))
        info["manh"]["khoe"] = bk
        print(f"  khoé miệng: {int(sot.sum())} px vách thành mảnh riêng (theo mai trên, ẩn khi há)")
    box = T.hop(m)
    Image.fromarray(np.clip(cav[box[1]:box[3], box[0]:box[2]], 0, 255).astype(np.uint8), "RGBA").save(os.path.join(ra, "long.png"))
    info["manh"]["long"] = box
    info["ham_gpt"] = os.path.basename(src)
    # mặt trước: chỗ chóp lưỡi che vành lấy vành liền của H01; chóp lưỡi thành mảnh rời đặt trước mai dưới
    if de.any():
        bd = info["manh"]["mai_duoi"]
        tr = np.array(Image.open(os.path.join(ra, "mai_duoi.png")).convert("RGBA")).astype(np.float32)
        vung = T.gian(de, 4)[bd[1]:bd[3], bd[0]:bd[2]]
        Gc = G[bd[1]:bd[3], bd[0]:bd[2]]
        dung_ = vung & fg[bd[1]:bd[3], bd[0]:bd[2]] & ~tim_g[bd[1]:bd[3], bd[0]:bd[2]]
        tr[dung_, :3] = Gc[dung_]
        tr[dung_, 3] = 255
        Image.fromarray(np.clip(tr, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(ra, "mai_duoi.png"))
        al = cv2.GaussianBlur(de.astype(np.float32), (0, 0), 0.8)
        al = np.where(T.co(de, 2), 1.0, al)
        bm = T.hop(de, 3)
        T.luu(a, al, bm, os.path.join(ra, "luoi_mep.png"))
        info["manh"]["luoi_mep"] = bm
        info["manh"].pop("mai_duoi_k", None)
    print(f"  hàm dưới {os.path.basename(src)}: căn IoU mặt bát {v:.3f} (co {sc:.3f}, dời {tx:.0f}, {ty:.0f}); kéo giãn dọc {sy:.2f}; cắt lòi "
          f"{loi} px; tô bù vùng miệng {int(thieu.sum())} px")
    return True


def cat(k):
    src = concept(k)
    if not os.path.exists(src):
        raise SystemExit("chưa có " + src)
    to_dir = os.path.join(d_inbox(1), "to")
    if not os.path.exists(os.path.join(to_dir, "to.json")):
        cat_to()
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    Hh, Ww = a.shape[:2]
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    bg = T.nen_trang(a)
    lab, muc, hong, tim = phan_lop(a, bg)
    U, L, I = lab == 1, lab == 2, lab == 3
    # chóp lưỡi thè qua mép dưới (dạng 2): phần lưỡi nằm ĐÈ LÊN mai dưới giữ luôn trên mai dưới (vẽ sẵn như đang liếm mép), kẻo
    # mai dưới thủng một lỗ. Mép trên của vành dưới theo từng cột, cột bị lưỡi che thì nội suy từ hai bên.
    cam = L & (R > 200) & (G > 95) & (G < 180) & (B < 125)                            # vành cam của mai dưới
    xacu = L & (a.min(2) > 165) & (np.abs(R - B) < 22)                                # mặt bát xà cừ
    hong_c = T.cum(cv2.morphologyEx(hong.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)) > 0, 200)
    hong = max(hong_c, key=lambda c: c["dt"])["m"] if hong_c else hong
    T00 = hong | (I & muc & T.gian(hong, 12))
    xs_all = np.arange(Ww)
    yb = np.full(Ww, np.nan)                                                           # mép trên của mặt bát theo cột
    yc = np.full(Ww, np.nan)                                                           # mép trên của vành cam theo cột
    for x in np.nonzero(xacu.any(0))[0]:
        yb[x] = np.argmax(xacu[:, x])
    for x in np.nonzero(cam.any(0))[0]:
        yc[x] = np.argmax(cam[:, x])
    co2 = ~np.isnan(yb) & ~np.isnan(yc) & (yb > yc)
    de = np.zeros_like(L)
    if co2.sum() > 40:
        day_vanh = float(np.median((yb - yc)[co2])) + 7                                # bề dày vành (kể cả viền mực trên)
        rows = np.arange(Hh)[:, None]
        sau = T00 & (rows > np.nan_to_num(yb, nan=1e9)[None, :] - day_vanh + 14)       # lưỡi lấn sâu vào vành ít nhất 14 px
        A = np.convolve(sau.any(0).astype(float), np.ones(17), mode="same") > 0        # các cột có chóp lưỡi đè mép (nới 8 cột)
        if sau.sum() > 300 and (~A & ~np.isnan(yb)).sum() > 20:
            tot = ~A & ~np.isnan(yb)
            yb2 = np.interp(xs_all, xs_all[tot], yb[tot])                              # mặt bát ở cột bị che: nội suy từ hai bên
            de = T00 & (rows > yb2[None, :] - day_vanh) & A[None, :]
            de = cv2.morphologyEx(de.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    if de.any():
        L = L | de
        I = I & ~de
        print(f"  chóp lưỡi đè mép dưới: {int(de.sum())} px giữ trên mai dưới")
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)
    info = {"concept": os.path.basename(src), "manh": {}, "luoi_de_mep": int(de.sum())}

    # bản lề: tâm đường giáp giữa hai mai (bên trái); hai mai cùng giữ một đĩa quanh đó để xoay không hở
    giap = T.gian(U, 2) & L
    if giap.sum() > 20:
        ys, xs = np.nonzero(giap)
        cut = xs < np.percentile(xs, 60)
        hx, hy = float(xs[cut].mean()), float(ys[cut].mean())
    else:
        ys, xs = np.nonzero(I)
        i0 = xs.argmin()
        hx, hy = float(xs[i0]), float(ys[i0])
    yy, xx = np.mgrid[0:Hh, 0:Ww]
    dia = ((xx - hx) ** 2 + (yy - hy) ** 2 <= 26 ** 2) & (U | L)
    info["ban_le"] = [hx, hy]

    # LÒNG MAI DƯỚI (như con gốc; người dùng 2026-11-11: "nhìn kĩ cách họ tách 2 mảnh ở con gốc đi, hàm dưới khi há thấy cả viền
    # trong của hàm đựng lưỡi", "không cần làm thịt ở trong miệng"): bên trong miệng chỉ là MẶT TRONG CỦA MAI DƯỚI = một hình thấu
    # kính trơn màu tím (dây cung từ bản lề tới đầu vành dưới, vồng lên trên), có VÀNH CAM phía xa dọc mép trên; gắn theo mai dưới,
    # nằm sau lưỡi. Mai trên mở ra như cái nắp, giữa nắp và mai dưới là khoảng trống. Lúc nghỉ vành xa khuất sau mai trên.
    Ic = I | de
    wr = U.sum(1)
    u_top = int(np.argmax(wr >= 0.45 * wr.max()))                                      # đỉnh vòm mai trên (bỏ gai)
    th_day = int(np.nonzero(L.any(1))[0].max())
    ccam = np.nonzero(cam.any(0))[0]
    xE = int(ccam.max()) - 6
    yE = float(np.argmax(cam[:, xE]))
    Lc = math.hypot(xE - hx, yE - hy)
    ux, uy = (xE - hx) / Lc, (yE - hy) / Lc                                            # dọc dây cung (bản lề -> đầu vành dưới)
    uu = ((xx - hx) * ux + (yy - hy) * uy) / Lc
    vv = (xx - hx) * uy - (yy - hy) * ux                                               # dương = phía trên dây cung (ảnh y xuống)
    u_max = float(np.percentile(uu[Ic], 99.9)) if Ic.any() else 1.0
    if u_max > 1.0:                                                                    # vùng miệng dài quá đầu vành dưới (khoé miệng dưới đầu vành trên): kéo dài dây cung cho phủ hết
        uu = uu / (u_max * 1.01)
        Lc = Lc * u_max * 1.01
    tq = np.clip((uu - 0.4) / 0.5, 0, 1)
    mu = 0.35 + (0.12 - 0.35) * tq * tq * (3 - 2 * tq)                                 # đầu phía trước (phải) dựng đứng hơn: phủ cả khoé miệng
    dang = np.clip(1 - (2 * uu - 1) ** 2, 0, 1) ** mu                                  # dáng vồng: 0 ở hai đầu, 1 ở giữa
    vung = Ic & (uu > 0.08) & (uu < 0.80)
    can = float(np.percentile(vv[vung] / np.maximum(dang[vung], 0.3), 99.5)) if vung.any() else 60.0   # vồng tối thiểu để phủ vùng miệng lúc nghỉ
    noi = 0.13 * (th_day - u_top)
    ke81 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81))
    Us = cv2.morphologyEx(U.astype(np.uint8), cv2.MORPH_CLOSE, ke81)                   # bóng mai trên đã lấp kẽ nanh
    Mr = cv2.getRotationMatrix2D((hx, hy), -26.0, 1.0)
    Us_ngam = cv2.warpAffine(Us, Mr, (Ww, Hh), flags=cv2.INTER_NEAREST) > 0            # lúc ngậm (~26°)
    Us = Us > 0
    khuat = T.co(Us | L | Ic, 6)                                                       # chỗ vành xa được phép nằm lúc nghỉ (khuất sau mai trên)
    h_l = can + noi
    lens = (uu >= -0.01) & (uu <= 1.01) & (vv <= h_l * dang) & (vv >= -46)
    # chỗ nào vồng cao quá bóng mai trên (đầu miệng phía trước, nơi mai trên chỉ còn cái vành) thì đi theo mép trong của bóng đó
    lens &= khuat & T.co(Us | L | Ic, 3)
    lens = cv2.morphologyEx(lens.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))) > 0
    lens = max(T.cum(lens, 200), key=lambda c: c["dt"])["m"]
    day_v = int(np.clip(0.75 * (float(np.median((yb - yc)[co2])) if co2.sum() > 40 else 26), 14, 34))   # vành xa mỏng hơn vành gần

    def xuong_(m, n):
        o = np.zeros_like(m)
        o[n:] = m[:-n]
        return o

    vanh = lens & ~xuong_(lens, day_v) & (vv > 4)                                      # dải sát mép trên: vành phía xa
    net = lens & (vv > 2) & (~xuong_(lens, 6) | (~xuong_(lens, day_v + 6) & ~vanh))    # nét mực mép trên và dưới vành
    # phần vùng miệng thấu kính không phủ (vách trong ở khoé miệng bên phải): chuyển sang mai trên (mặt trong mép mai trên); mẩu vụn thì gộp vào thấu kính
    du = Ic & ~lens & ~de
    sang_tren = np.zeros_like(U)
    co_h01 = T.moi_nhat(os.path.join(d_inbox(k), "tai_ve"), "H01") is not None
    for c in ([] if co_h01 else T.cum(du, 1)):
        if c["dt"] > 150 and (T.gian(c["m"], 4) & U).any():
            sang_tren |= c["m"]
        elif (T.gian(c["m"], 3) & lens).any():
            lens |= c["m"]
    U = U | sang_tren
    I = I & ~sang_tren
    info["day_cung"] = [ux, uy]
    print(f"  lòng mai dưới: vồng {h_l:.0f} px (cần {can:.0f}), vành dày {day_v} px; vách khoé miệng chuyển sang mai trên {int(sang_tren.sum())} px; "
          f"vùng miệng chưa phủ {int((I & ~lens).sum())} px")

    def mem(m):
        return np.where(T.co(m, 2), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7)) * m

    # hai mai
    for ten, m in (("mai_tren", U | dia), ("mai_duoi", L | dia)):
        al = np.where(bg, 0.0, 1.0) * m
        edge = T.gian(bg, 2) & m                                                      # chỉ mép giáp nền mới làm mềm
        al = np.where(edge, mem(m), al)
        box = T.hop(m)
        T.luu(a, al, box, os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box

    if de.any():
        mk = (L | dia)
        box = T.hop(mk)
        a8 = np.clip(a, 0, 255).astype(np.uint8)
        va = cv2.inpaint(a8, T.gian(de, 3).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA).astype(np.float32)
        al = np.where(bg, 0.0, 1.0) * mk
        al = np.where(T.gian(bg, 2) & mk, mem(mk), al)
        T.luu(va, al, box, os.path.join(ra, "mai_duoi_k.png"))
        info["manh"]["mai_duoi_k"] = box

    # mắt (vàng) trên mai trên -> mí = mảng màu mai phủ kín con mắt và viền dưới của nó, chừa nét mày phía trên: nhắm mắt chỉ còn
    # nét mày xếch. Màu lấy từ pixel mai (không mực) gần nhất rồi làm nhoè nhẹ, thêm vân.
    vang = (R > 215) & (G > 160) & (B < 130) & U
    mat_c = sorted(T.cum(cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0, 300), key=lambda c: -c["dt"])[:2]
    mat_c.sort(key=lambda c: c["x0"])                                                 # trái = mắt gần
    info["mat"] = []
    rngm = np.random.default_rng(3)
    for ten, c in zip(("mi_g", "mi_x"), mat_c):
        hull = cv2.convexHull(np.argwhere(c["m"])[:, ::-1].astype(np.int32))           # bao lồi phần vàng: gồm cả con ngươi, chấm sáng
        em = np.zeros((Hh, Ww), np.uint8)
        cv2.fillConvexPoly(em, hull, 1)
        em = T.gian(em > 0, 2)                                                        # lòng mắt (vàng, con ngươi, chấm sáng)
        phu = T.gian(em, 14) & U
        cols = np.nonzero(em.any(0))[0]
        top = {int(x): int(np.argmax(em[:, x])) for x in cols}                        # mép trên của lòng mắt theo cột
        for x in range(max(0, cols.min() - 12), min(Ww, cols.max() + 13)):
            xn = int(min(max(x, cols.min()), cols.max()))
            phu[:top[xn] - 1, x] = False                                              # phía trên mép đó là nét mày: không che
        nguon = U & ~muc & ~T.gian(em, 12) & (B > R + 45)                             # pixel màu mai sạch
        _, idx = cv2.distanceTransformWithLabels((~nguon).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys0, xs0 = np.nonzero(nguon)
        lut = np.zeros((idx.max() + 1, 3), np.float32)
        lut[idx[ys0, xs0]] = a[ys0, xs0]
        to_mau = lut[idx]
        to_mau = cv2.GaussianBlur(to_mau, (0, 0), 3.0)
        x0, y0, x1, y1 = T.hop(phu, 2)
        ma = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
        ma[..., :3] = np.clip(to_mau[y0:y1, x0:x1] + rngm.normal(0, 4, (y1 - y0, x1 - x0, 1)), 0, 255)
        al = cv2.GaussianBlur(phu.astype(np.float32), (0, 0), 0.8)
        al = np.where(T.co(phu, 2), 1.0, al)
        ma[..., 3] = 255.0 * al[y0:y1, x0:x1]
        ho = int((em[y0:y1, x0:x1] & (ma[..., 3] < 128)).sum())
        Image.fromarray(ma.astype(np.uint8), "RGBA").save(os.path.join(ra, ten + ".png"))
        info["manh"][ten] = [x0, y0, x1, y1]
        info["mat"].append({"x0": c["x0"], "y0": c["y0"], "x1": c["x1"], "y1": c["y1"], "ho": ho})
        print(f"  mí {ten}: phủ mắt, còn hở {ho} px")

    # lưỡi lúc nghỉ: phần hồng của concept + viền mực của nó; vá chỗ nanh dưới che và nối xuống sau vành mai dưới
    T0 = T00
    Tm = cv2.morphologyEx(T0.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45))) > 0
    xuong = Tm.copy()
    for dy in range(1, 30):
        xuong[dy:] |= Tm[:-dy]
    Tm = (xuong & T.co(U | L | I | de, 8)) | T0
    hong_mau = np.median(a[hong & (R > 200)], 0)
    rng = np.random.default_rng(7)
    luoi = a.copy()
    them = Tm & ~T0
    luoi[them] = np.clip(hong_mau + rng.normal(0, 5, (int(them.sum()), 1)), 0, 255)
    box = T.hop(Tm)
    T.luu(luoi, Tm.astype(np.float32), box, os.path.join(ra, "luoi_nghi.png"))
    info["manh"]["luoi_nghi"] = box
    info["luoi_lo"] = [int(v) for v in T.hop(hong, 0)]                                 # phần lưỡi thấy được trong concept

    iy, ix = np.nonzero(I)
    ix0, ix1, iy0, iy1 = int(ix.min()), int(ix.max()), int(iy.min()), int(iy.max())
    tim_mau = np.median(a[tim], 0)
    cam_mau = np.median(a[cam], 0) if cam.sum() > 50 else np.array([240, 138, 75], np.float32)
    cav = np.zeros((Hh, Ww, 4), np.float32)
    van = 3.0 * np.sin((xx + yy) * 0.85) + rng.normal(0, 3.5, (Hh, Ww))                # vân sáp chéo
    cav[..., :3] = np.clip(tim_mau[None, None, :] + van[..., None], 0, 255)
    cav[vanh, :3] = np.clip(cam_mau[None, :] + van[vanh][:, None], 0, 255)
    cav[net, :3] = (43, 33, 24)
    lens = lens | (T.gian(Tm, 4) & T.co(U | L | I | de, 2))                            # sau lưỡi nghỉ luôn có lòng mai (viền lưỡi không hở)
    al = cv2.GaussianBlur(lens.astype(np.float32), (0, 0), 0.8)
    cav[..., 3] = 255.0 * np.where(T.co(lens, 2), 1.0, al)
    box = T.hop(lens)
    Image.fromarray(cav[box[1]:box[3], box[0]:box[2]].astype(np.uint8), "RGBA").save(os.path.join(ra, "long.png"))
    info["manh"]["long"] = box

    # hình học cho rig: đầu mép miệng bên phải, độ hé, chỗ môi chu
    cot = np.arange(ix0, ix1 + 1)
    day = np.array([I[:, x].sum() for x in cot])
    xe = int(cot[np.argmax(day * (cot > hx + 0.6 * (ix1 - hx)))])                      # cột hé rộng nhất ở nửa phải
    ysx = np.nonzero(I[:, xe])[0]
    info["mep"] = {"x": xe, "y0": int(ysx.min()), "y1": int(ysx.max()), "ix": [ix0, ix1], "iy": [iy0, iy1]}
    cc = np.nonzero(~np.isnan(yc))[0]
    xm = int(cc.max()) - 10                                                            # đầu vành dưới phía trước (bên phải)
    info["moi"] = [xm, float(yc[xm])]
    xg = int(cc[np.argmin(np.abs(cc - int(hx + 0.68 * (ix1 - hx))))])
    info["giua_mep"] = [xg, float(yc[xg])]
    xq = int(cc[np.argmin(np.abs(cc - int(hx + 0.55 * (ix1 - hx))))])
    info["moi_giua"] = [xq, float(yc[xq])]
    info["day_vanh"] = float(np.median((yb - yc)[co2])) + 7 if co2.sum() > 40 else 34.0                                             # điểm trên mép dưới ở 68 % (đặt gốc lưỡi dài)
    info["goc_khep"] = math.degrees(math.atan2(float(ysx.max() - ysx.min()), xe - hx))
    wl = L.sum(1)
    info["than"] = {"x0": int(np.nonzero((U | L).any(0))[0].min()), "x1": int(np.nonzero((U | L).any(0))[0].max()), "y_top": u_top,
                    "y_day": int(np.nonzero(wl >= 0.25 * wl.max())[0].max()), "y_dinh": int(np.nonzero(U.any(1))[0].min())}
    ghep_ham(k, a, bg, U, L, I, de, info, ra)
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # tờ soi: nhãn, các mảnh tách rời, ghép lại, khác concept
    mau = np.zeros((Hh, Ww, 3), np.uint8) + 150
    mau[U], mau[L], mau[I] = (40, 150, 160), (240, 225, 235), (90, 40, 110)
    cv2.circle(mau, (int(hx), int(hy)), 9, (255, 60, 60), -1)
    t1 = Image.fromarray(mau).convert("RGBA")

    def nen():
        return Image.new("RGBA", (Ww, Hh), GRAY + (255,))

    def dan(im, ten, dx=0, dy=0):
        p = Image.open(os.path.join(ra, ten + ".png"))
        x0, y0 = info["manh"][ten][:2]
        im.alpha_composite(p, (max(0, x0 + dx), max(0, y0 + dy)))

    t2 = nen()                                                                         # tách rời: mai trên nhấc lên, mai dưới hạ xuống
    dan(t2, "long")
    dan(t2, "luoi_nghi")
    dan(t2, "mai_duoi", 0, 110)
    dan(t2, "mai_tren", 0, -150)
    t3 = nen()
    for ten in ("long", "luoi_nghi", "mai_duoi", "mai_tren"):
        dan(t3, ten)
    t4 = nen()
    t4.alpha_composite(Image.fromarray(np.dstack([a.astype(np.uint8), np.where(bg, 0, 255).astype(np.uint8)]), "RGBA"))
    d = np.abs(np.array(t3.convert("RGB")).astype(int) - np.array(t4.convert("RGB")).astype(int)).max(2)
    t5 = Image.fromarray(np.dstack([np.clip(d * 4, 0, 255)] * 3).astype(np.uint8)).convert("RGBA")
    t6 = nen()
    for ten in ("long", "luoi_nghi", "mai_duoi", "mai_tren", "mi_g", "mi_x"):
        dan(t6, ten)
    o = [(t1, "1. nhãn: mai trên / mai dưới / trong miệng, chấm đỏ = bản lề"), (t2, "2. tách rời (lòng miệng + lưỡi nghỉ ở giữa)"),
         (t3, "3. ghép lại"), (t4, "4. concept"), (t5, "5. khác nhau 3 và 4 (x4)"), (t6, "6. nhắm mắt (hai mí)")]
    to = Image.new("RGBA", (Ww // 2 * 3, Hh // 2 * 2), (60, 60, 60, 255))
    f = ImageFont.truetype(FONT, 22)
    for i, (im, chu) in enumerate(o):
        s = im.resize((Ww // 2, Hh // 2), Image.LANCZOS)
        ImageDraw.Draw(s).text((12, 8), chu, fill=(255, 255, 255, 255), font=f)
        to.alpha_composite(s, ((i % 3) * (Ww // 2), (i // 3) * (Hh // 2)))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    print(f"dạng {k}: bản lề ({hx:.0f}, {hy:.0f}), góc khép {info['goc_khep']:.1f}°, mép phải x={xe}; ghép lại khác concept tối đa "
          f"{int(d.max())}, {int((d > 24).sum())} px lệch > 24 -> {os.path.join(ra, '_soi.png')}")


# ================================================================ RIG (thư viện quai) ================================================================
# Cấu trúc học từ con gốc monster_3237 (ghi chú inbox/so_gai_ghichu.md mục 2):
#   root -> move (game dời: lao) -> lac (trục con lắc ở cao: thân lắc lư như lật đật = bone2 của gốc)
#        -> than (tâm thân: nghiêng, nhảy, nén giãn = bone4)
#             -> mai_duoi (bản lề phía sau = bone6): lòng miệng, lưỡi nghỉ (ln0, ln1), mai dưới, lưỡi dài (lu0..7), môi chu (moi -> mieng)
#             -> mai_tren (bản lề phía sau = bone5): mai trên, hai mí
# Hai mai, lòng miệng, mí, môi là MẢNH CỨNG (vỏ sò là đồ cứng thật); chỉ lưỡi là lưới mềm nhiều đốt.
SC = 0.5
CHAM = {1: 1.0, 2: 1.1}
N_LUOI = 8
REF_W = 300.0                  # bề ngang vỏ con gốc (đơn vị rig của nó): đổi độ dời của khoá gốc


def khep(k):
    """góc phải xoay mai trên (độ, quanh bản lề) để hai vành vừa chạm và để miệng khép khít: đo trên mặt nạ concept."""
    src = concept(k)
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    bg = T.nen_trang(a)
    lab, _, _, _ = phan_lop(a, bg)
    mj = json.load(open(os.path.join(d_inbox(k), "manh", "manh.json"), encoding="utf-8"))
    hx, hy = mj["ban_le"]
    U, L, I = (lab == 1).astype(np.uint8), lab == 2, lab == 3
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    xa = (xx - hx) ** 2 + (yy - hy) ** 2 > 60 ** 2
    x1 = mj["mep"]["ix"][1]
    giua = np.zeros_like(L)
    giua[:, int(hx + 0.2 * (x1 - hx)):int(hx + 0.85 * (x1 - hx))] = True
    goc_khe = float((I & giua).sum())
    cham = khit = None
    for g in np.arange(1, 70, 1.0):
        M = cv2.getRotationMatrix2D((hx, hy), -g, 1.0)                                 # ảnh y xuống: góc âm của cv2 = xoay thuận kim = khép
        Ur = cv2.warpAffine(U, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_NEAREST) > 0
        de = int((Ur & L & xa).sum())
        ho = float((I & giua & ~Ur).sum())
        if cham is None and de > 200:
            cham = g
        if khit is None and ho < 0.15 * goc_khe:
            khit = g
        if cham is not None and khit is not None:
            break
    return float(cham or 12), float(khit or (cham or 12) + 8)


def dung(k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    Dat = khung.Dat
    dm = os.path.join(d_inbox(k), "manh")
    dto = os.path.join(d_inbox(1), "to")
    mj = json.load(open(os.path.join(dm, "manh.json"), encoding="utf-8"))
    th = mj["than"]
    ox, oy = (th["x0"] + th["x1"]) / 2.0, float(th["y_day"])

    def R(x, y):
        return ((x - ox) * SC, (oy - y) * SC)

    def tam(box):
        return R((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)

    def nap(path, ti=SC):
        im = Image.open(path).convert("RGBA")
        im = im.resize((max(2, round(im.width * ti)), max(2, round(im.height * ti))), Image.LANCZOS)
        return anh.loang_mau(im)

    Wb, Hb = (th["x1"] - th["x0"]) * SC, (th["y_day"] - th["y_top"]) * SC
    H = (th["y_day"] - th["y_dinh"]) * SC                                              # cả gai
    Hg = R(*mj["ban_le"])
    mep = mj["mep"]
    g_cham, g_khit = khep(k)

    sk = khung.Sk(f"{CODE}_{k}")
    for n in ("mai_tren", "mai_duoi", "long", "luoi_nghi", "mi_g", "mi_x"):
        sk.anh(n, nap(os.path.join(dm, n + ".png")))
    co_k = "mai_duoi_k" in mj["manh"]
    if co_k:
        sk.anh("mai_duoi_k", nap(os.path.join(dm, "mai_duoi_k.png")))
    co_khoe = "khoe" in mj["manh"]
    if co_khoe:
        sk.anh("khoe", nap(os.path.join(dm, "khoe.png")))
    co_mep = "luoi_mep" in mj["manh"]
    if co_mep:
        sk.anh("luoi_mep", nap(os.path.join(dm, "luoi_mep.png")))
    L_luoi = 1.12 * Wb                                                                 # lưỡi dài hơn bề ngang thân một chút
    im_l = Image.open(os.path.join(dto, "luoi_dai.png"))
    sk.anh("luoi_dai", nap(os.path.join(dto, "luoi_dai.png"), L_luoi / im_l.width))
    tj = json.load(open(os.path.join(dto, "to.json"), encoding="utf-8"))
    co_moi = "moi_chu" in tj
    if co_moi:                                                                         # dải kép của mảnh cao bằng hai vành của con này
        ti_m = SC * 1.9 * mj["day_vanh"] / max(20.0, tj["moi_chu_dai"])
        sk.anh("moi", nap(os.path.join(dto, "moi_chu.png"), ti_m))

    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("lac", "move", 0, 2.6 * Hb)
    sk.xuong("than", "lac", 0, 0.48 * Hb, the_gioi=True)
    sk.xuong("mai_duoi", "than", *Hg, the_gioi=True)
    sk.xuong("mai_tren", "than", *Hg, the_gioi=True)
    dc = mj.get("day_cung", [1.0, 0.0])
    sk.xuong("long", "mai_duoi", *Hg, goc=math.degrees(math.atan2(-dc[1], dc[0])), the_gioi=True)   # lòng mai dưới: ép dẹt về dây cung khi ngậm
    # lưỡi nghỉ: hai xương dọc phần lưỡi thấy được
    lo = mj["luoi_lo"]
    yl = (lo[1] + lo[3]) / 2.0
    sk.xuong("ln0", "mai_duoi", *R(lo[0], yl), the_gioi=True)
    sk.xuong("ln1", "ln0", *R(lo[0] + 0.55 * (lo[2] - lo[0]), yl), the_gioi=True)
    # lưỡi dài: gốc nằm sâu trong miệng, phía sau, ngang mép trên của vành dưới
    goc_l = R(mj["ban_le"][0] + 0.30 * (mep["ix"][1] - mj["ban_le"][0]), mj["giua_mep"][1] - 16)
    im = sk.images["luoi_dai"]
    Ll = luoi.luoi_dai(im, N_LUOI, mu=True, buoc=max(7.0, im.height / 5.0), ten=f"lưỡi dài {k}")
    dat_l = Dat(goc_l[0], goc_l[1], neo=(0.02, 0.5))
    lu = sk.chuoi("lu", "mai_duoi", dat_l.ra(Ll.khop(N_LUOI), im.width, im.height))
    # môi chu: ở giữa đường miệng, nằm trên chỗ hai vành ép vào nhau lúc ngậm; xoay theo dây cung. Xương mieng ở lỗ môi, trục x
    # chĩa hướng nhổ (sang phải). Chưa có mảnh môi thì xương mieng vẫn đặt ở đó (VFX bám vào).
    goc_dc = math.degrees(math.atan2(-dc[1], dc[0]))
    pm = R(mj["moi_giua"][0], mj["moi_giua"][1] - 0.35 * mj["day_vanh"])
    sk.xuong("moi", "mai_duoi", *pm, goc=goc_dc, the_gioi=True)
    sk.xuong("mieng", "moi", pm[0] + 6, pm[1], goc=0, dai=40, the_gioi=True)

    sk.slot("long", "long", "long")
    sk.slot("luoi", "ln0", "luoi_nghi")
    sk.slot("mai_duoi", "mai_duoi", "mai_duoi")
    sk.slot("luoi_d", lu[0], None, truoc="mai_duoi")                                   # lưỡi dài: GIỮA hai lớp hàm dưới (như con gốc)
    if co_mep:
        sk.slot("luoi_mep", "mai_duoi", "luoi_mep")                                    # chóp lưỡi thè qua mép (dạng 2): trước mai dưới
    sk.slot("luoi_t", lu[0], None)                                                     # cùng cái lưỡi dài, lớp TRƯỚC mai dưới: dùng lúc lưỡi vắt xuống qua mép
    if co_khoe:
        sk.slot("khoe", "mai_tren", "khoe")                                            # vách khoé miệng: che khe ở khoé lúc gần ngậm, ẩn khi há
    sk.slot("mai_tren", "mai_tren", "mai_tren")
    sk.slot("mi_g", "mai_tren", "mi_g", an=True)
    sk.slot("mi_x", "mai_tren", "mi_x", an=True)
    if co_moi:
        sk.slot("moi", "moi", "moi", an=True)

    for n in ("long", "mai_duoi", "mai_tren", "mi_g", "mi_x"):
        sk.manh(n, n, Dat(*tam(mj["manh"][n])))
    if co_moi:
        sk.manh("moi", "moi", Dat(*pm, goc=goc_dc))
    if co_k:
        sk.manh("mai_duoi", "mai_duoi_k", Dat(*tam(mj["manh"]["mai_duoi_k"])), ten="mai_duoi_k")
    if co_mep:
        sk.manh("luoi_mep", "luoi_mep", Dat(*tam(mj["manh"]["luoi_mep"])))
    if co_khoe:
        sk.manh("khoe", "khoe", Dat(*tam(mj["manh"]["khoe"])))
    # lưỡi nghỉ: lưới nhỏ, gốc bám ln0, nửa ngoài bám ln1
    im = sk.images["luoi_nghi"]
    Ln = luoi.luoi_vung(im, buoc_vien=0.02 * H, buoc_trong=0.03 * H, ten=f"lưỡi nghỉ {k}")
    dat_n = Dat(*tam(mj["manh"]["luoi_nghi"]))
    V = dat_n.ra(Ln.pts, im.width, im.height)
    x0n, x1n = R(lo[0], 0)[0], R(lo[2], 0)[0]
    Wn = []
    for x, y in V:
        u = min(1.0, max(0.0, (x - x0n) / max(1.0, x1n - x0n)))
        w1 = min(1.0, max(0.0, (u - 0.2) / 0.6))
        w1 = w1 * w1 * (3 - 2 * w1)
        Wn.append({"ln0": 1.0} if w1 < 0.004 else ({"ln1": 1.0} if w1 > 0.996 else {"ln0": 1 - w1, "ln1": w1}))
    sk.luoi_gan("luoi", "luoi_nghi", Ln, Wn, dat=dat_n)
    Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / N_LUOI, lu, cha="mai_duoi", cha_hoa=0.0)
    sk.luoi_gan("luoi_d", "luoi_dai", Ll, Wl, dat=dat_l)
    sk.luoi_gan("luoi_t", "luoi_dai", Ll, Wl, dat=dat_l)
    for ev, mo in (("trung", "đòn đớp / nhát quật đầu chạm đối thủ"), ("quat", "nhát quật lưỡi kế tiếp"), ("phun", "nhổ ngọc trai (VFX bám xương mieng)")):
        sk.su_kien(ev, mo)
    info = {"k": k, "Wb": Wb, "Hb": Hb, "H": H, "lu": lu, "g_cham": g_cham, "g_khit": g_khit, "de_mep": mj.get("luoi_de_mep", 0) > 0, "co_k": co_k, "co_mep": co_mep, "co_khoe": co_khoe, "co_moi": co_moi,
            "dinh": Ln.n + Ll.n}
    return sk, info


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    Clip, rung = hoat.Clip, hoat.rung
    ln, spl = T.ln, T.spl
    Wb, Hb, H, lu = info["Wb"], info["Hb"], info["H"], info["lu"]
    K = Wb / REF_W
    ch = CHAM[k]
    F = 30.0 / ch
    CU, CD = -0.75 * info["g_khit"], 0.25 * info["g_khit"]                             # dáng khép khít: mai trên sập xuống, mai dưới nhích lên
    nhe = 0.4 if info["de_mep"] else 1.0                                               # dạng có chóp lưỡi vẽ sẵn trên mai dưới: lưỡi nghỉ nhúc nhích ít
    hien = [s["name"] for s in sk.slots if s["alpha"] > 0]

    def mai(P, tren, duoi):
        P.rot("mai_tren", tren)
        P.rot("mai_duoi", duoi)
        rel = tren - duoi
        if info["co_khoe"] and rel > 4:
            P.alpha["khoe"] = 0.0                                                      # há: khoé miệng mở, bỏ mẩu vách
        if rel < 0:                                                                    # ngậm: vành trong xẹp về phía mép (kẻo lòi ra trên lưng mai trên)
            P.scale("long", 1, max(0.7, 1 + 0.3 * rel / info["g_khit"]))
        if tren < 0:                                                                   # miệng khép: lưỡi nghỉ thụt xuống sau vành dưới, kẻo lòi giữa hai vành
            g = min(1.0, tren / CU)
            P.move("ln0", 0, -0.10 * Hb * g)
            P.scale("ln0", 1, 1 - 0.5 * g)

    def nham(P, a=1.0):
        P.alpha["mi_g"] = a
        P.alpha["mi_x"] = a

    def luoi_nghi(P, a, b, dai=1.0):
        P.rot("ln0", a * nhe)
        P.rot("ln1", b * nhe)
        if dai != 1.0:
            P.scale("ln0", 1 + (dai - 1) * nhe, 1)

    def luoi_dai(P, t, A, C, co, tre=0.012):
        """lưỡi dài: A(giây) góc gốc, C(giây) độ cuộn mỗi đốt (độ); đốt xa hơn đi trễ hơn (quất như roi). co: tỉ lệ cả lưỡi."""
        P.att["luoi_t" if A(t) < -6 else "luoi_d"] = "luoi_dai"                       # chĩa xuống dưới mép thì vắt ra trước mai dưới
        P.att["luoi"] = None
        if info["co_k"]:
            P.att["mai_duoi"] = "mai_duoi_k"
        if info["co_mep"]:
            P.alpha["luoi_mep"] = 0.0                                                  # lưỡi dài thè ra: ẩn chóp lưỡi nghỉ
        truoc = 0.0
        for i, b in enumerate(lu):
            ti = t - i * tre
            w = A(ti) + i * C(ti)
            P.rot(b, w - truoc)
            truoc = w
        P.scale(lu[0], co, co)

    def an_het(P, a):
        for s in hien:
            if s == "khoe" and P.alpha.get("khoe", 1.0) == 0.0:
                continue
            P.alpha[s] = a
        for s in ("mi_g", "mi_x"):
            if P.alpha.get(s, 0) > 0:
                P.alpha[s] = a

    # ---------------- idle: lắc lư như lật đật (bone2 + bone4 của gốc), vòng giữa nhai nhai, có chớp mắt
    def idle_fn(t, P):
        f = (t * F) % 120
        th = 2 * math.pi * f / 40.0
        P.rot("lac", 3.4 * (math.cos(th) - 1))
        P.rot("than", 7.5 * math.sin(th))
        mai(P, ln(f, [(0, 0), (16, 1.7), (38, 0), (51, 2.6), (55, 0), (59, 4.2), (63, -0.3), (67, 5.6), (71, 0.5), (80, 0), (96, 1.7), (118, 0), (120, 0)]),
            ln(f, [(0, 0), (40, 0), (51, -6.5), (55, -2.8), (59, -6.2), (63, -2.8), (67, -5), (80, 0), (120, 0)]))
        luoi_nghi(P, 3 * math.sin(th + 0.5) - 3 * math.sin(0.5), 6 * math.sin(th - 0.6) + 6 * math.sin(0.6))
        if 100 <= f < 104:
            nham(P)

    # ---------------- appear: rơi xuống như quả bóng (miệng ngậm), bẹp, nảy, há ra đớp hai cái
    def appear_fn(t, P):
        f = t * F
        an_het(P, ln(f, [(0, 0), (2, 1)]))
        P.move("than", 0, 2.6 * Hb * (1 - min(1.0, f / 7.0) ** 2) + K * ln(f, [(0, 0), (8, 0), (11, 34), (14, 0), (16, 8), (18, 0)]))
        P.rot("than", ln(f, [(0, -40), (7, 0), (9, 5), (12, -3), (16, 0)]))
        P.scale("than", ln(f, [(0, .95), (7, .95), (8.5, 1.14), (11, .97), (14, 1.05), (17, 1), (24, 1)]),
                ln(f, [(0, 1.05), (7, 1.05), (8.5, .86), (11, 1.04), (14, .96), (17, 1), (24, 1)]))
        mai(P, ln(f, [(0, CU), (10, CU), (13, 14), (15, CU * .6), (17.5, 12), (19.5, CU * .5), (22, 0), (24, 0)]),
            ln(f, [(0, CD), (10, CD), (13, -6), (15, CD * .6), (17.5, -5), (19.5, CD * .5), (22, 0), (24, 0)]))
        if f < 10:
            nham(P, ln(f, [(0, 0), (2, 1)]))

    # ---------------- attack: há hai mai thật to rồi đớp mạnh (skill_01 của gốc); cú lao nằm trên move để sân kéo tới đối thủ
    def attack_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (3, 4.8), (13, 5.5), (15, -1.4), (16, -20), (17, -26), (19, -22), (21, 7.8), (25, 8), (30, 0)]))
        P.move("than", K * ln(f, [(0, 0), (3, -14), (13, -18), (16, 10), (17, 16), (21, -20), (25, -12), (30, 0)]),
               K * ln(f, [(0, 0), (3, 80), (13, 88), (15, 67), (16, 12), (17, 0), (21, 0), (25, 34), (29, 0)]))
        P.move("move", 0.45 * H * ln(f, [(0, 0), (13, 0), (15, .5), (16, 1), (20, 1), (23, .45), (27, 0)]), 0)
        P.scale("than", ln(f, [(0, 1), (3, .96), (13, .95), (16, .98), (17, 1.14), (19, 1.1), (21, .96), (25, 1.02), (30, 1)]),
                ln(f, [(0, 1), (3, 1.04), (13, 1.05), (16, 1.02), (17, .86), (19, .9), (21, 1.04), (25, .98), (30, 1)]))
        mai(P, ln(f, [(0, 0), (3, 43), (13, 56), (15, 44), (16, 60), (17, CU - 4), (19, CU - 1), (21, CU), (25, -3), (28, 3), (32, 0)]),
            ln(f, [(0, 0), (3, -25), (13, -35), (15, -33), (16, -48), (17, CD + 2), (21, CD), (25, -5), (32, 0)]))
        luoi_nghi(P, ln(f, [(0, 0), (3, 4), (13, 6), (16, 8), (17, 0), (32, 0)]), ln(f, [(0, 0), (3, -8), (8, 4), (13, -6), (16, 8), (17, 0), (32, 0)]),
                  ln(f, [(0, 1), (3, 1.08), (15, 1.08), (17, 1), (32, 1)]))
        if 16.5 <= f < 23:
            nham(P)

    # ---------------- cast: lấy hơi, NGẬM miệng, nín hơi (phồng, run, ngả ra sau), rồi BẬT MIỆNG NHỔ viên ngọc ra, giật lùi, về dáng
    # (người dùng 2026-11-11: "tưởng tượng ngậm mồm rồi nhổ ra ngọc"). Môi chu nằm ở đầu miệng phía trước, dẩu ra lúc nhổ.
    def cast_fn(t, P):
        f = t * F
        r = rung(t, 11 / F, 18 / F)
        mai(P, ln(f, [(0, 0), (5, 11), (8, CU - 2), (9.5, CU), (18.6, CU), (19.6, 15), (21, 21), (25, 9), (30, -2), (34, 1), (40, 0)]),
            ln(f, [(0, 0), (5, -6), (8, CD + 1), (9.5, CD), (18.6, CD), (19.6, -7), (21, -9), (25, -4), (30, 1), (40, 0)]))
        P.rot("than", ln(f, [(0, 0), (5, 4), (9.5, 6), (17, 11), (18.3, 12), (19.6, -10), (21.5, 9), (25, 5), (31, 0)]))
        P.scale("than", ln(f, [(0, 1), (5, .98), (9.5, 1.02), (17.5, 1.10), (19.6, .93), (21.5, 1.03), (26, 1), (40, 1)]),
                ln(f, [(0, 1), (5, 1.03), (9.5, 1.01), (17.5, 1.07), (19.6, 1.02), (21.5, .98), (26, 1), (40, 1)]))
        P.move("than", K * (ln(f, [(0, 0), (9.5, -5), (17.5, -14), (19.6, 12), (21.5, -26), (26, -9), (33, 0)]) + 1.3 * r),
               K * ln(f, [(0, 0), (19.6, 0), (21.5, 10), (24, 0), (40, 0)]))
        if info["co_moi"] and 9 <= f < 20.4:
            P.alpha["moi"] = ln(f, [(9, 0), (10, 1), (19.6, 1), (20.4, 0)])
            sx = ln(f, [(9, .7), (11.5, 1.05), (13, 1), (17.5, 1.1), (19.2, 1.3), (20.4, 1.1)])
            sy = ln(f, [(9, .45), (11.5, 1.05), (13, 1), (17.5, 1.12), (19.2, .82), (20.4, .6)])
            P.scale("moi", sx * (1 + 0.03 * r), sy * (1 - 0.03 * r))
        if 8.5 <= f < 19.8:
            nham(P)

    # ---------------- skill: há miệng, thè lưỡi dài, lao tới, quật ba phát (skill_02 của gốc), thu lưỡi, lùi về
    def kf(keys):
        return lambda tt: spl(tt * F, keys)

    A_ = kf([(3, 20), (7, 60), (9, 96), (11, -30), (13, -18), (15, 82), (18, -22), (20, -10), (23, 108), (26, -40), (29, -26), (33, 10), (36, 0)])
    C_ = kf([(3, 6), (7, 10), (9, 14), (11, -7), (13, -2), (15, 12), (18, -6), (20, -1), (23, 16), (26, -9), (29, -3), (36, 0)])

    def skill_fn(t, P):
        f = t * F
        P.move("move", 0.5 * H * ln(f, [(0, 0), (4, 0), (9, 1), (31, 1), (38, 0)]), 0)
        P.move("than", 0, K * ln(f, [(0, 0), (4, 0), (6.5, 42), (9, 0), (23, 0), (25, 20), (26, 0), (31, 0), (34.5, 30), (38, 0)]))
        P.rot("than", ln(f, [(0, 0), (4, 8), (9, 14), (11, -12), (13, -4), (15, 10), (18, -10), (20, -3), (23, 16), (26, -22), (29, -8), (35, 0)]))
        P.scale("than", ln(f, [(0, 1), (25, 1), (26, 1.1), (28, 1.06), (31, 1), (44, 1)]), ln(f, [(0, 1), (25, 1), (26, .9), (28, .95), (31, 1), (44, 1)]))
        mai(P, ln(f, [(0, 0), (4, 38), (9, 30), (11, 24), (15, 32), (18, 24), (23, 40), (26, 20), (30, 26), (35, 6), (38, 0)]),
            ln(f, [(0, 0), (4, -8), (11, -14), (15, -6), (18, -14), (23, -5), (26, -18), (30, -8), (36, 0)]))
        if 3 <= f < 36:
            luoi_dai(P, t, A_, C_, ln(f, [(3, .22), (7, 1), (31, 1), (36, .22)]))
        if 25.5 <= f < 29:
            nham(P)

    # ---------------- hit: bị đánh lăn ngửa ra sau, mắt nhắm, miệng bật ra rồi về (hit_01 của gốc, lùi 1 khung)
    def hit_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (1, 34), (4, 46), (6, 36), (9, 10), (12, -3), (16, 0)]))
        P.move("than", K * ln(f, [(0, 0), (1, -58), (3, -22), (5, -44), (7, -50), (10, -28), (13, -10), (16, 0)]),
               K * ln(f, [(0, 0), (4, 20), (8, 0), (11, 9), (14, 0), (16, 0)]))
        P.scale("than", ln(f, [(0, 1), (1, .9), (4, 1.04), (8, 1), (16, 1)]), ln(f, [(0, 1), (1, 1.1), (4, .96), (8, 1), (16, 1)]))
        mai(P, ln(f, [(0, 0), (1, CU), (5, CU * .8), (7, 10), (10, 34), (13, 8), (16, 0)]), ln(f, [(0, 0), (1, CD), (5, CD), (10, -10), (16, 0)]))
        luoi_nghi(P, ln(f, [(0, 0), (7, 10), (10, 16), (13, -6), (16, 0)]), ln(f, [(0, 0), (7, -10), (10, 20), (13, -8), (16, 0)]))
        if 0.5 <= f < 10.5:
            nham(P)

    # ---------------- die: bị hất tung ra sau, rơi xuống mai bật mở, lưỡi thè dài nằm vật, rồi tan (die_01 của gốc)
    A_d = kf([(13, 30), (16, -22), (19, -8), (23, -20), (46, -18)])
    C_d = kf([(13, 8), (16, -9), (19, -4), (23, -7), (46, -6)])

    def die_fn(t, P):
        f = t * F
        P.rot("than", ln(f, [(0, 0), (2, 17), (6, 44), (9, 56), (11, 40), (13, 6), (15, -24), (17, -20), (25, -19), (46, -19)]))
        P.move("than", K * ln(f, [(0, 0), (2, -20), (6, -70), (9, -120), (13, -104), (17, -100), (46, -100)]),
               K * ln(f, [(0, 0), (2, 110), (6, 140), (9, 70), (12, 0), (14, 18), (17, 0), (46, 0)]))
        P.scale("than", ln(f, [(0, 1), (11, 1), (12.5, 1.12), (15, .97), (18, 1), (46, 1)]), ln(f, [(0, 1), (11, 1), (12.5, .88), (15, 1.03), (18, 1), (46, 1)]))
        mai(P, ln(f, [(0, 0), (2, CU), (9, CU), (11, 20), (13, 84), (15, 44), (18, 58), (22, 34), (26, 40), (46, 38)]),
            ln(f, [(0, 0), (2, CD), (9, CD), (13, -14), (17, -6), (46, -6)]))
        if f >= 13:
            luoi_dai(P, t, A_d, C_d, ln(f, [(13, .25), (17, .78), (46, .78)]))
        nham(P)
        if f > 33:
            an_het(P, ln(f, [(33, 1), (45, 0), (46, 0)]))
            P.alpha["luoi_d"] = ln(f, [(33, 1), (45, 0), (46, 0)])
            P.alpha["luoi_t"] = P.alpha["luoi_d"]

    return [Clip("appear", 24 / F, appear_fn),
            Clip("idle", 120 / F, idle_fn, loop=True),
            Clip("attack", 32 / F, attack_fn, ev=[(17 / F, "trung", "")]),
            Clip("cast", 40 / F, cast_fn, ev=[(19.6 / F, "phun", "")]),
            Clip("skill", 44 / F, skill_fn, ev=[(11 / F, "trung", ""), (18 / F, "quat", ""), (26 / F, "quat", "")], trung=11 / F),
            Clip("hit", 16 / F, hit_fn),
            Clip("die", 46 / F, die_fn)]


def lo_kin(sk, frames, s=0.5):
    """lỗ thủng nhìn xuyên qua thân (vùng trong suốt bị hình bao kín): số px rig vuông lớn nhất trong clip, và khung nào."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    ve = soi.Ve(sk)
    worst, at = 0.0, -1
    for i, P in enumerate(frames):
        b = ve.bao(P)
        if b[2] - b[0] < 4:
            continue
        box = (b[0] - 6, b[1] - 6, b[2] + 6, b[3] + 6)
        al = np.asarray(ve.ve(P, box, s, ss=1))[..., 3] > 110
        lo = T.lap_lo(al) & ~al
        lo = cv2.morphologyEx(lo.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)) > 0
        n = float(lo.sum()) / (s * s)
        if n > worst:
            worst, at = n, i
    return worst, at


def gif_nho(sk, fr, info, k, ra):
    """GIF xem thử clip cast có viên ngọc bay (viên ngọc là VFX của game: ở đây chỉ ghép vào ảnh xem thử, không vào rig)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    ve = soi.Ve(sk)
    H, Hb = info["H"], info["Hb"]
    ngoc = Image.open(os.path.join(d_inbox(1), "to", "ngoc.png")).convert("RGBA")
    sc = 0.6
    d = max(8, int(0.24 * Hb * sc))
    ngoc = ngoc.resize((d, d), Image.LANCZOS)
    i_ph = int(round(19.6 / 30.0 * CHAM[k] * 30))
    box = (-0.8 * H, -0.12 * H, 2.6 * H, 1.5 * H)
    m0 = sk.the_gioi(fr[i_ph])["mieng"][:2, 2]
    out = []
    for i, P in enumerate(fr):
        im = ve.ve(P, box, sc, bg=(150, 150, 150), ss=2)
        if i >= i_ph:
            x = m0[0] + (i - i_ph) / 30.0 * 6.5 * H
            if x < box[2] + d:
                px, py = (x - box[0]) * sc, (box[3] - m0[1]) * sc
                im.alpha_composite(ngoc, (int(px - d / 2), int(py - d / 2)))
        out.append(im.convert("RGB"))
    out = out + [out[-1]] * 8
    out[0].save(ra, save_all=True, append_images=out[1:], duration=33, loop=0)
    return ra


def rig(k, tien_hoa=None):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = T._quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    for c in cl:
        w, at = lo_kin(sk, fr[c.ten])
        print(f"  lỗ kín {c.ten}: lớn nhất {w:.0f} px2" + (f" (khung {at})" if w > 0 else ""))
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ten = f"{CODE}_{k}"
    noi = {}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        ve1, ve2 = soi.Ve(sk), soi.Ve(sk2)
        ti = soi.chieu_cao(ve1, fr["idle"][0]) / soi.chieu_cao(ve2, fr2["idle"][0])
        M = tienhoa.gop(sk, sk2)
        cu1, cd1 = -0.75 * info["g_khit"], 0.25 * info["g_khit"]

        def gong(t, P):                                                       # dạng cũ ngậm chặt, mắt nhắm, rung, phồng dần
            g = hoat.cv(t, [(0, 0), (0.3, 1, "out"), (1.3, 1)])
            P.rot("mai_duoi", info["g_khit"] * g)                             # ngậm bằng cách nâng mai dưới
            P.scale("long", 1, 1 - 0.3 * g)
            P.move("ln0", 0, -0.10 * info["Hb"] * g)
            P.scale("ln0", 1, 1 - 0.5 * g)
            s = hoat.cv(t, [(0, 1), (0.3, 0.94), (0.6, 1.08, "out"), (1.3, 1.3)])
            r = hoat.rung(t, 0.45, 1.3)
            P.scale("than", s * (1 + 0.02 * r), s * (1 - 0.02 * r))
            if t > 0.2:
                am = 1.0 - hoat.ease((t - 1.05) / 0.3)
                P.alpha["mi_g"] = am
                P.alpha["mi_x"] = am

        def bung(t, P, fl):                                                   # dạng sau hiện ra, há thật to rồi đớp một cái
            o = hoat.cv(t, [(0, 0), (1.5, 0), (1.85, 1, "out"), (2.05, 1), (2.15, -0.35, "in"), (2.35, 0.15, "io"), (2.5, 0, "io"), (2.8, 0)])
            P.rot("n_mai_tren", 46 * o)
            P.rot("n_mai_duoi", -16 * o)

        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=bung)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
    tk = xuat.xuat_het(M, clM, ra, ten, f"Sò đột biến dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("cast",), lao=("skill",),
                       khop_idle=0, noi_them=noi, tol={"rotate": 0.08, "translate": 0.15, "scale": 0.001},
                       can=[("can_dop", "attack", 17 / 30.0 * CHAM[k], "than", 0.7 * info["H"]),
                            ("can_ha", "attack", 13 / 30.0 * CHAM[k], "than", 0.8 * info["H"]),
                            ("can_chu_moi", "cast", 16 / 30.0 * CHAM[k], "moi", 0.6 * info["H"])])
    gif_nho(sk, fr["cast"], info, k, os.path.join(ra, "xem_nho_ngoc.gif"))
    print(f"dạng {k}: góc chạm {info['g_cham']:.0f}°, góc khép khít {info['g_khit']:.0f}°; {info['dinh']} đỉnh lưỡi; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    return sk, info, fr, cl


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg[:1] == ["to"]:
        cat_to()
    elif arg[:1] == ["cat"]:
        for k in ([int(arg[1])] if len(arg) > 1 else [1, 2]):
            cat(k)
    elif arg[:1] == ["rig"]:
        rig(int(arg[1]))
    elif arg[:1] == ["all"]:
        r2 = rig(2)
        rig(1, tien_hoa=r2)
    else:
        print(__doc__)
