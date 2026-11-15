# -*- coding: utf-8 -*-
"""Chiến binh đất nung (dat_nung): cắt MẢNH CỨNG từ sáu tờ "đúng chỗ, đúng cỡ" (M_A..M_F: Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài
mảnh không chồng nhau, vẽ đủ phần khuất).

    dat_nung_manh.py lam      → inbox/dat_nung_1/manh/<tên>.png (RGBA, cắt sát) + dat.json ({ảnh vùng của rig gốc: {"anh": tên mảnh, "M": afin
                                2×3 px ảnh mảnh → thế giới rig ở khung 0 idle}}, "_px", "_tat") + _so_ghep.png (ghép lại cạnh concept) +
                                _to.png (từng mảnh trên nền xám)

Khung concept ↔ thế giới rig gốc (khung 0 idle): px = OX + SC·X, py = OY − SC·Y (đúng phép dựng sơ đồ bố cục: GPT bám sơ đồ nên một phép
cho cả con là đủ). Mỗi mảnh của mình thay MỘT ảnh vùng của họ (bảng VUNG) và bám xương của ảnh vùng đó; vùng không có mảnh thì bỏ."""
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
import dat_nung as G  # noqa: E402

MANH = os.path.join(G.BASE, "manh")
DUYET = os.path.join(G.TAI, "L1_duyet.png")
KH = json.load(open(os.path.join(G.MAU, "bo_cuc_hop_tuong_binh.json"), encoding="utf-8"))["_khung"]
SC, OX, OY = KH["sc"], KH["ox"], KH["oy"]
PAD = 4
PX = 0.62                                         # px atlas / đơn vị rig
# tờ → {mảnh: tâm ước chừng trên khung concept}
TO = {"A": {"dau": (810, 390), "vai_x": (590, 430), "nam": (630, 822), "tam_dung": (1075, 735), "da_dai": (1100, 360)},
      "B": {"kiem": (470, 500), "vai_g": (1030, 510), "da_dung": (825, 265), "loi": (700, 580)},
      "C": {"lava": (750, 530), "ban_x": (397, 725), "da_thoi": (1175, 570), "cang": (835, 807), "da_trai": (525, 290)},
      "D": {"co_x": (668, 450), "co_g": (890, 560), "phien_tren": (390, 470), "duoi_cang": (832, 880)},
      "E": {"rang_1": (646, 650), "rang_2": (745, 690), "rang_3": (821, 684), "rang_4": (861, 664), "da_phai": (950, 300),
            "phien_duoi": (365, 592), "khoi_a": (945, 707)},
      "F": {"khop": (940, 623), "khoi_b": (965, 832), "cang_x": (428, 662), "da_nho": (1085, 475), "bap_x": (155, 155)}}
NGON_TO, NGON_HOP = "C", (235, 640, 400, 865)     # mười đốt ngón tay xa: mọi cụm nhỏ còn lại của tờ C trong hộp này
# mảnh → ảnh vùng của rig gốc mà nó thay (bám xương của vùng đó)
VUNG = {"dau": "P_tou", "vai_x": "P_jianjiaR3", "nam": "P_shouL4_1", "tam_dung": "P_shouL2_1", "da_dai": "P_dun10", "kiem": "P_wuqi",
        "vai_g": "P_jianjiaL1", "da_dung": "P_dun08", "loi": "P_huoyan17", "lava": "P_huoyan20", "ban_x": "P_shouR4", "da_thoi": "P_dun05",
        "cang": "P_shouL3_1", "da_trai": "P_dun07", "co_x": "P_jianjiaR2", "co_g": "P_jianjiaL2", "phien_tren": "P_dun03",
        "duoi_cang": "P_shouL3_3", "rang_1": "P_shenti1_2", "rang_2": "P_shenti1_1", "rang_3": "P_shenti1_3", "rang_4": "P_dun11",
        "da_phai": "P_dun09", "phien_duoi": "P_dun02", "khoi_a": "P_shouL2_2", "khop": "P_shouL1", "khoi_b": "P_dun01",
        "cang_x": "P_shouR3", "da_nho": "P_dun06", "bap_x": "P_shouR2"}
NGON_VUNG = ["P_shouR4_09", "P_shouR4_11", "P_shouR4_10", "P_shouR4_08", "P_shouR4_07", "P_shouR4_06", "P_shouR4_04", "P_shouR4_03",
             "P_shouR4_02", "P_shouR4_01", "P_shouR4_05"]
THEO_RIG = {"bap_x"}                              # mảnh khuất trên concept (Codex vẽ ở góc trống): đặt theo tâm ảnh vùng của rig
XOAY_DUNG = {"kiem"}                              # mảnh dài nằm chéo: xoay ảnh cho dựng đứng (đỡ tốn atlas), M mang phép xoay
TAT = {"loi": ("loi_tat", (128, 112, 104)), "lava": ("lava_nguoi", (92, 78, 74))}       # hình TẮT / NGUỘI (die): tên, màu đá nguội


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def doc(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int32)


def nen(A, lo_min=2500):
    """mặt nạ NỀN: trắng thông ra mép ảnh + lỗ trắng kín lớn. Trắng kín nhỏ là của mảnh."""
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    H, W = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H or a >= lo_min:
            bg |= lab == i
    return bg


def manh_rgba(A, m):
    """ảnh RGBA cắt sát của mặt nạ m (mép mềm 1 px theo độ sáng: điểm mép ngả trắng thì trong dần)."""
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


def cum(ma):
    A = doc(os.path.join(G.TAI, f"M_{ma}.png"))
    fg = ~nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    return A, n, lab, st, cen


def cat_to(ma):
    A, n, lab, st, cen = cum(ma)
    ra, da_dung = {}, set()
    for ten, (cx, cy) in TO[ma].items():
        best, bi = 1e18, -1
        for i in range(1, n):
            if st[i, 4] < 250 or i in da_dung:
                continue
            x, y, w, h, _ = st[i]
            dx = max(x - cx, 0, cx - (x + w))
            dy = max(y - cy, 0, cy - (y + h))
            d = dx * dx + dy * dy + 0.02 * ((cen[i][0] - cx) ** 2 + (cen[i][1] - cy) ** 2)
            if d < best:
                best, bi = d, i
        if bi < 0:
            raise SystemExit(f"tờ {ma}: không thấy mảnh {ten}")
        da_dung.add(bi)
        ra[ten] = (A, lab == bi)
    ngon = []
    if ma == NGON_TO:
        x0, y0, x1, y1 = NGON_HOP
        for i in range(1, n):
            if i in da_dung or st[i, 4] < 250:
                continue
            if x0 <= cen[i][0] <= x1 and y0 <= cen[i][1] <= y1:
                da_dung.add(i)
                # các đốt vẽ sát nhau dính thành một cụm: bóp cụm lấy lõi từng đốt, mỗi điểm thuộc lõi gần nhất
                m = (lab == i)
                loi = cv2.erode(m.astype(np.uint8), el(9))
                k, lb, sk_, ck = cv2.connectedComponentsWithStats(loi, 8)
                if k <= 2:
                    ngon.append((A, m, tuple(cen[i])))
                    continue
                _, nhan = cv2.distanceTransformWithLabels((lb == 0).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
                # nhãn của distanceTransformWithLabels là chỉ số điểm 0 gần nhất: đổi về nhãn lõi
                ys0, xs0 = np.nonzero(lb > 0)
                bang = np.zeros(nhan.max() + 1, np.int32)
                bang[nhan[ys0, xs0]] = lb[ys0, xs0]
                gan_ = bang[nhan]
                for j in range(1, k):
                    mj = m & (gan_ == j)
                    mj = cv2.morphologyEx(mj.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
                    if mj.sum() > 200:
                        ys, xs = np.nonzero(mj)
                        ngon.append((A, mj, (float(xs.mean()), float(ys.mean()))))
    thua = [tuple(int(v) for v in st[i, :5]) for i in range(1, n) if i not in da_dung and st[i, 4] >= 400]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f" + {len(ngon)} đốt ngón" if ngon else "") + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra, ngon


def nguoi(im, mau):
    """bản TẮT / NGUỘI: mọi vùng màu (không phải nét mực) đổi sang màu đá nguội, giữ độ đậm nhạt tương đối và vân sáp."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    sang = rgb.mean(2, keepdims=True)
    muc = (rgb.max(2, keepdims=True) < 105)
    co = (al > 40) & ~muc
    med = float(np.median(sang[co])) if co.any() else 160.0
    k = np.clip(0.80 + 0.35 * (sang - med) / 90.0, 0.55, 1.2)
    out = np.where(muc, rgb, np.array(mau, np.float32)[None, None, :] * k)
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), "RGBA")


KHOP_R = 70                                        # dò lại chỗ mảnh quanh chỗ Codex vẽ, tối đa chừng này px
CHINH = {}                                         # mảnh: (dx, dy) ép tay (px concept), thay cho dò tự động
KHONG_KHOP = {"khop", "cang_x", "rang_4", "duoi_cang", "khoi_a", "khoi_b", "co_x", "co_g"}   # mảnh khuất nhiều / lẫn màu mảnh kề: dò không tin được                                 # mảnh giữ nguyên chỗ Codex vẽ


def khop(C_lab, ten, im, goc):
    """Codex vẽ mảnh lệch chỗ concept vài chục px: dò lại (dx, dy) cho mảnh khớp concept nhất (SQDIFF có mặt nạ trên Lab, phạt nhẹ theo quãng
    dời). Phần khuất của mảnh (concept bị thứ khác che) cộng sai số gần như đều nên phần lộ quyết định."""
    if ten in CHINH:
        return (goc[0] + CHINH[ten][0], goc[1] + CHINH[ten][1]), CHINH[ten], 0.0
    if ten in KHONG_KHOP or ten in THEO_RIG:
        return goc, (0, 0), 0.0
    a = np.asarray(im)
    m = (a[..., 3] > 128)
    tpl = cv2.cvtColor(np.ascontiguousarray(a[..., :3]), cv2.COLOR_RGB2LAB).astype(np.float32)
    h, w = m.shape
    H, W = C_lab.shape[:2]
    xa, ya = max(0, goc[0] - KHOP_R), max(0, goc[1] - KHOP_R)
    xb, yb = min(W, goc[0] + w + KHOP_R), min(H, goc[1] + h + KHOP_R)
    res = cv2.matchTemplate(C_lab[ya:yb, xa:xb], tpl, cv2.TM_SQDIFF, mask=np.dstack([m] * 3).astype(np.float32))
    res = res / max(1.0, float(m.sum()))
    yy, xx = np.mgrid[0:res.shape[0], 0:res.shape[1]]
    dx, dy = xx + xa - goc[0], yy + ya - goc[1]
    diem = res + 0.25 * (dx * dx + dy * dy)
    j = np.unravel_index(np.argmin(diem), diem.shape)
    d = (int(dx[j]), int(dy[j]))
    return (goc[0] + d[0], goc[1] + d[1]), d, float(res[j])


def M_khung(goc):
    """afin px ảnh mảnh (góc trên trái ở `goc` trên khung concept) → thế giới rig."""
    return np.array([[1 / SC, 0.0, (goc[0] - OX) / SC], [0.0, -1 / SC, (OY - goc[1]) / SC]])


def xoay_dung(im, M):
    """xoay ảnh mảnh dài cho trục chính dựng đứng; trả ảnh mới và afin mới (px ảnh xoay → thế giới)."""
    al = np.asarray(im)[..., 3] > 60
    ys, xs = np.nonzero(al)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    u = vt[0]
    th = math.degrees(math.atan2(u[0], -u[1]))                 # góc (thuận kim trên màn hình) của trục chính so với phương đứng
    th = (th + 90) % 180 - 90
    q = im.convert("RGBa").rotate(th, resample=Image.BICUBIC, expand=True).convert("RGBA")       # PIL: xoay NGƯỢC kim trên màn hình
    bb = q.getbbox()
    q2 = q.crop((max(0, bb[0] - PAD), max(0, bb[1] - PAD), min(q.width, bb[2] + PAD), min(q.height, bb[3] + PAD)))
    ox, oy = max(0, bb[0] - PAD), max(0, bb[1] - PAD)
    r = math.radians(th)
    Rv = np.array([[math.cos(r), math.sin(r)], [-math.sin(r), math.cos(r)]])      # p' − c' = Rv (p − c) (toạ độ ảnh, y xuống)
    co, cn = np.array([im.width / 2, im.height / 2]), np.array([q.width / 2, q.height / 2])
    # p = co + Rvᵀ (p2 + (ox, oy) − cn)
    A2 = Rv.T
    b2 = co + Rv.T @ (np.array([ox, oy]) - cn)
    M2 = np.zeros((2, 3))
    M2[:, :2] = M[:, :2] @ A2
    M2[:, 2] = M[:, :2] @ b2 + M[:, 2]
    return q2, M2


def lam():
    os.makedirs(MANH, exist_ok=True)
    C = doc(DUYET)
    P, ngon = {}, []
    for ma in TO:
        if not os.path.exists(os.path.join(G.TAI, f"M_{ma}.png")):
            print(f"  chưa có tờ {ma}")
            continue
        r, ng = cat_to(ma)
        P.update(r)
        ngon += ng
    G.Q._C.pop("att", None)
    _, _, atts = G.nap("att_idle0.json")
    by = {a["region"]: a for a in atts}

    def tam_vung(r):
        V = np.array(by[r]["xy"], float).reshape(-1, 2)
        return (V.min(0) + V.max(0)) / 2

    dat, anh_ = {"_px": PX, "_tat": {}}, {}

    def luu(ten, im, M, vung):
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = (im, M)
        dat[vung] = dict(anh=ten, M=[[float(v) for v in row] for row in M])

    C_lab = cv2.cvtColor(C.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    doi = []
    for ten, (A, m) in P.items():
        im, goc = manh_rgba(A, m)
        goc, d, sai = khop(C_lab, ten, im, goc)
        doi.append(f"{ten} {d[0]:+d},{d[1]:+d}")
        M = M_khung(goc)
        if ten in THEO_RIG:                                      # đặt tâm mảnh vào tâm ảnh vùng của rig
            c = tam_vung(VUNG[ten])
            M = np.array([[1 / SC, 0.0, c[0] - im.width / 2 / SC], [0.0, -1 / SC, c[1] + im.height / 2 / SC]])
        if ten in XOAY_DUNG:
            im, M = xoay_dung(im, M)
        luu(ten, im, M, VUNG[ten])
        if ten in TAT:
            t2, mau = TAT[ten]
            im2 = nguoi(im, mau)
            im2.save(os.path.join(MANH, t2 + ".png"))
            anh_[t2] = (im2, M)
            dat["_tat"][VUNG[ten]] = t2
    # đốt ngón: khớp với ảnh vùng ngón của rig theo vị trí tương đối (tịnh tiến cho trùng trọng tâm rồi ghép gần nhất)
    if ngon:
        cs = np.array([((c[0] - OX) / SC, (OY - c[1]) / SC) for _, _, c in ngon])
        vs = [v for v in NGON_VUNG if v in by]
        rc = np.array([tam_vung(v) for v in vs])
        rc2 = rc - rc.mean(0) + cs.mean(0)
        D = np.hypot(*(cs[:, None, :] - rc2[None, :, :]).transpose(2, 0, 1))
        con_m, con_v = set(range(len(ngon))), set(range(len(vs)))
        while con_m and con_v:
            i, j = min(((i, j) for i in con_m for j in con_v), key=lambda q: D[q[0], q[1]])
            A, m, _ = ngon[i]
            im, goc = manh_rgba(A, m)
            goc, d, _s = khop(C_lab, "ngon", im, goc)
            luu(f"ngon_{vs[j][-2:]}", im, M_khung(goc), vs[j])
            con_m.discard(i)
            con_v.discard(j)
        print(f"  đốt ngón: {len(ngon)} cụm, gán {len(ngon) - len(con_m)}; vùng ngón không có mảnh: {[vs[j] for j in con_v]}")
    print("  dời về chỗ concept (px): " + "; ".join(doi))
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)

    # ghép lại cạnh concept (theo thứ tự vẽ của rig)
    Wc, Hc = C.shape[1], C.shape[0]
    thu_tu = []
    for a in sorted(atts, key=lambda a: a["order"]):
        if a["region"] in dat and a["region"] not in thu_tu:
            thu_tu.append(a["region"])
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for r in thu_tu:
        im, M = anh_[dat[r]["anh"]]
        # px ảnh → px concept: X, Y = M · (x, y, 1); cx = OX + SC·X, cy = OY − SC·Y
        Mc = np.array([[SC * M[0, 0], SC * M[0, 1], OX + SC * M[0, 2]], [-SC * M[1, 0], -SC * M[1, 1], OY - SC * M[1, 2]], [0, 0, 1.0]])
        inv = np.linalg.inv(Mc)
        lay = im.convert("RGBa").transform((Wc, Hc), Image.AFFINE, tuple(inv[:2].reshape(-1)), resample=Image.BICUBIC).convert("RGBA")
        ghep.alpha_composite(lay)
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - C).max(2)
    print(f"  ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ; {len(thu_tu)} vùng có mảnh")
    # tờ từng mảnh trên nền xám
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    x = y = 12
    hh = 0
    cho = []
    ten_ds = [dat[r]["anh"] for r in thu_tu] + list(dat["_tat"].values())
    for t in ten_ds:
        im = anh_[t][0]
        if x + im.width + 12 > 2400:
            x, y, hh = 12, y + hh + 34, 0
        cho.append((t, x, y))
        x += max(im.width, 90) + 16
        hh = max(hh, im.height)
    to = Image.new("RGB", (2400, y + hh + 40), (150, 150, 150))
    dr = ImageDraw.Draw(to)
    for t, x, y in cho:
        to.paste(anh_[t][0], (x, y + 20), anh_[t][0])
        dr.text((x, y), t, fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(ten_ds), "mảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
