# -*- coding: utf-8 -*-
"""Dạng 2 Sóng Thần dựng theo CÁCH LAI (DAC_TA mục 5, chuẩn 2026-11-11 04:00): mảnh thân chính cắt thẳng từ concept đã duyệt.

- Tách vùng trên concept (như thuy_long_lien.py): hạt giống kẻ tay theo toạ độ concept, loang đều từng px trong vùng màu, nét mực là
  tường, nét mực và ô kín chưa loang lấy nhãn gần nhất, lọc đa số 7x7, bỏ mẩu < 400 px.
- Hai lớp cắt từ concept: lớp THÂN (thân, cổ, bụng, đai, hai chân, hai bàn chân, đuôi) và lớp ĐẦU (đầu trên, băng đô, nút, vây má,
  hai mào). Lớp thân mọc thêm dưới đầu (vẽ bù TELEA) để đầu ngửa không hở gáy.
- Phần tách hoặc vung xa giữ mảnh GPT đã dò khớp (tm01_rig.bo_tri2): hai tay + găng + nắm tay / bàn tay xoè, giáp vai, hàm dưới +
  lòng miệng, mí, hai dải băng đô, dải đai. Chỗ chúng che trên lớp thân vẽ bù bằng chính mảnh GPT thân / đuôi / chân đã khớp (dán
  hình), phần còn thiếu vẽ bù TELEA.
Cần cv2: chạy bằng D:/spine-venv/Scripts/python -I (tm01.py tự gọi khi LAI2 bật)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from quai import anh, luoi, trongso  # noqa: E402
from quai.khung import Dat  # noqa: E402

# nhãn: (tên, lớp) — lớp "than", "dau", hoặc None (tách ra, dùng mảnh GPT)
NHAN = [("than", "than"), ("duoi", "than"), ("chan_g", "than"), ("bc_g", "than"), ("chan_x", "than"), ("bc_x", "than"),
        ("dau", "dau"), ("mao_a", "dau"), ("mao_b", "dau"),
        ("tay_g", None), ("tay_x", None), ("ham", "dau"), ("dai", None), ("dd", None)]
TEN = [n for n, _ in NHAN]
# hạt giống trên concept (px concept): ("line", [điểm], dày) | ("poly", [điểm])
HAT = {
    "than": [("poly", [(720, 450), (860, 430), (880, 600), (720, 650)]), ("line", [(735, 560), (880, 620)], 10),
             ("line", [(560, 420), (600, 405)], 6), ("line", [(880, 480), (910, 560)], 10),
             ("line", [(912, 402), (920, 440), (902, 520)], 8)],                  # họng, ngực nhạt dưới cằm
    "duoi": [("line", [(590, 662), (480, 690), (380, 660), (335, 590), (340, 510), (380, 470)], 14)],
    "chan_g": [("line", [(880, 682), (945, 720), (962, 795)], 16)],
    "bc_g": [("line", [(965, 862), (1050, 872), (1100, 878)], 12)],
    "chan_x": [("line", [(650, 702), (580, 742), (520, 772)], 16)],
    "bc_x": [("line", [(470, 842), (420, 862)], 12), ("line", [(500, 830), (530, 860)], 8)],
    "dau": [("poly", [(880, 320), (990, 315), (1070, 345), (1000, 362), (900, 370)]), ("line", [(780, 292), (990, 278)], 8),
            ("line", [(1080, 340), (1115, 348)], 6), ("line", [(890, 320), (930, 360)], 8),
            ("poly", [(682, 296), (700, 296), (700, 316), (682, 316)])],            # nút băng đô
    "mao_a": [("line", [(800, 245), (880, 182), (960, 152), (1020, 172)], 9)],
    "mao_b": [("line", [(705, 272), (740, 228), (782, 214)], 8)],
    "tay_g": [("poly", [(690, 360), (770, 350), (780, 440), (700, 452)]), ("line", [(640, 478), (600, 500), (525, 522)], 14),
              ("line", [(470, 575), (495, 590)], 14)],
    "tay_x": [("line", [(972, 452), (1050, 452), (1120, 478), (1222, 440)], 14)],
    "ham": [("line", [(1002, 392), (1080, 380)], 5), ("line", [(1050, 366), (1068, 366)], 4)],
    "dai": [("line", [(676, 300), (600, 268), (520, 255), (492, 246)], 10), ("line", [(676, 312), (600, 326), (520, 322), (440, 336)], 10)],
    "dd": [("line", [(790, 640), (775, 770)], 12)],
}
# miệng trên concept (px concept): hàm dưới (bám xương hàm), lòng miệng (giãn giữa hai hàm), răng nanh trên (bám đầu), bản lề, mũi hàm
HAM_C = [(975, 400), (1088, 396), (1094, 410), (1062, 432), (990, 434), (968, 418)]
MIENG_C = [(986, 371), (1084, 373), (1092, 399), (986, 405)]
NANH_C = [[(1023, 366), (1045, 366), (1041, 397), (1029, 397)], [(1073, 374), (1095, 374), (1091, 403), (1079, 403)]]
BANLE_C, MUI_C = (976, 396), (1092, 404)
KHOP_CHAN = {"g": [(865, 685), (960, 728), (975, 835)], "x": [(665, 700), (565, 745), (478, 808)]}   # hông, gối, cổ chân (concept)


def concept_path():
    return os.path.join(HERE, "inbox", "tm01_2", "tai_ve", "L1_duyet.png")


def tach(ra_soi=None):
    """trả rgb, alpha mềm (0..1), nhãn (-1 nền) ở cỡ concept."""
    rgb = np.array(Image.open(concept_path()).convert("RGB"))
    fg = ~anh.nen_tu_mep(rgb.min(axis=2) > 236)
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    lite = ((mn > 240) & (mx - mn < 14) & fg).astype(np.uint8)        # chỉ giấy trắng thật (bọt lam nhạt không tính)
    n, cl, st, _ = cv2.connectedComponentsWithStats(lite, connectivity=4)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 3000:
            fg[cv2.dilate((cl == i).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = False
    alpha = cv2.GaussianBlur(cv2.erode(fg.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.1)
    alpha = np.clip(alpha * 1.25, 0, 1)
    fgm = fg.astype(np.uint8)
    inner = cv2.erode(fgm, np.ones((5, 5), np.uint8))
    lab = -np.ones(fg.shape, np.int32)
    for i, nm in enumerate(TEN):
        for kind, pts, *r in HAT[nm]:
            m = np.zeros(fg.shape, np.uint8)
            if kind == "line":
                cv2.polylines(m, [np.array(pts, np.int32)], False, 1, r[0] if r else 9)
            else:
                cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
            lab[(m > 0) & (inner > 0)] = i
    ink = (rgb.mean(2) < 72) & fg
    dom = fg & ~ink
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(900):
        miss = dom & (lab < 0)
        g = cv2.dilate(lab.astype(np.float32) + 1, k3).astype(np.int32) - 1
        upd = miss & (g >= 0)
        if not upd.any():
            break
        lab[upd] = g[upd]
    lab = gan_nhat(lab, fg & (lab < 0))
    cnt = np.stack([cv2.boxFilter((lab == i).astype(np.float32), -1, (7, 7), normalize=False) for i in range(len(TEN))], 0)
    lab = np.where(fg, cnt.argmax(0), -1).astype(np.int32)
    for i in range(len(TEN)):
        nc, cc, st, _ = cv2.connectedComponentsWithStats((lab == i).astype(np.uint8), connectivity=8)
        for c in range(1, nc):
            if st[c, cv2.CC_STAT_AREA] < 400:
                lab[cc == c] = -1
    lab = gan_nhat(lab, fg & (lab < 0))
    if ra_soi:
        col = np.array([[230, 60, 60], [60, 160, 230], [240, 190, 40], [120, 200, 80], [200, 90, 220], [40, 200, 190], [250, 130, 30],
                        [130, 90, 250], [250, 90, 150], [90, 250, 140], [180, 180, 60], [60, 90, 120], [255, 255, 255], [120, 40, 40]])
        o = (rgb * 0.45).astype(np.float32)
        for i in range(len(TEN)):
            o[lab == i] = o[lab == i] * 0.45 + col[i % len(col)] * 0.55
        o[lab < 0] = 255
        im = Image.fromarray(o.clip(0, 255).astype(np.uint8))
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        f = anh.font(16)
        for i, nm in enumerate(TEN):
            ys, xs = np.nonzero(lab == i)
            if len(xs):
                d.text((int(xs.mean()) - 12, int(ys.mean())), nm, fill=(0, 0, 0), font=f)
        im.save(ra_soi)
    return rgb, alpha, lab


def gan_nhat(lab, need):
    src = (lab >= 0) & ~need
    if not need.any() or not src.any():
        return lab
    _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(src)
    out = lab.copy()
    out[need] = lab[ys, xs][li[need] - 1]
    return out


def ve_mau(bo, W, H, ox, oy):
    """vẽ các mảnh GPT đã khớp (ảnh, Dat, mặt nạ cắt, tên) lên lưới điểm rig (cột = x + ox, hàng = oy − y), trả RGBA float."""
    out = np.zeros((H, W, 4), np.float32)
    for im, dat, cat, _ in bo:
        w, h = im.size
        P = np.array([[0, 0], [w, 0], [0, h]], float)
        V = dat.ra(P, w, h)
        R = np.stack([V[:, 0] + ox, oy - V[:, 1]], 1)
        A = np.array([[(R[1, 0] - R[0, 0]) / w, (R[2, 0] - R[0, 0]) / h, R[0, 0]],
                      [(R[1, 1] - R[0, 1]) / w, (R[2, 1] - R[0, 1]) / h, R[0, 1]], [0, 0, 1.0]])
        inv = np.linalg.inv(A)
        src = np.asarray(im.convert("RGBA")).astype(np.float32)
        if cat is not None:
            src[..., 3] *= cat
        r = Image.fromarray(src.clip(0, 255).astype(np.uint8), "RGBA").transform(
            (W, H), Image.AFFINE, (inv[0, 0], inv[0, 1], inv[0, 2], inv[1, 0], inv[1, 1], inv[1, 2]), resample=Image.BILINEAR)
        a = np.asarray(r).astype(np.float32)
        al = a[..., 3:4] / 255.0
        out[..., :3] = out[..., :3] * (1 - al) + a[..., :3] * al
        out[..., 3:4] = out[..., 3:4] * (1 - al) + al * 255.0
    return out


def lop(S, x0, y0, bo_than, ra_soi=None):
    """hai lớp cắt từ concept ở cỡ rig. Trả {lớp: (ảnh RGBA PIL, Dat, nhãn cỡ ảnh)} và nhãn cỡ rig."""
    rgb, alpha, lab = tach(ra_soi)
    H0, W0 = lab.shape
    W, H = int(round(W0 * S)), int(round(H0 * S))
    rgb_s = np.asarray(Image.fromarray(rgb).resize((W, H), Image.LANCZOS)).astype(np.float32)
    a_s = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0
    lab_s = np.asarray(Image.fromarray((lab + 1).astype(np.uint8)).resize((W, H), Image.NEAREST)).astype(np.int32) - 1
    ox, oy = x0 * S, y0 * S
    gpt = ve_mau(bo_than, W, H, ox, oy)                       # thân, đuôi, chân GPT đã khớp: nguồn vẽ bù
    lop_of = {i: l for i, (_, l) in enumerate(NHAN)}
    in_than = np.isin(lab_s, [i for i, l in lop_of.items() if l == "than"])
    in_dau = np.isin(lab_s, [i for i, l in lop_of.items() if l == "dau"])
    tach_ra = np.isin(lab_s, [i for i, l in lop_of.items() if l is None]) & (a_s > 0.02)
    out = {}
    # lớp thân: điểm concept của nhãn thân; chỗ tay / dải đai / hàm che: dán mảnh GPT đã khớp (chỉ trong bóng mảnh GPT); mọc thêm dưới đầu
    A = np.zeros((H, W, 4), np.float32)
    A[..., :3] = rgb_s
    A[..., 3] = np.where(in_than, a_s, 0.0) * 255
    # vùng vẽ bù = phần bị tay / dải đai / hàm che nằm trong bóng thân (đóng hình thái học thân + mảnh GPT), không lấn sang đầu
    giu = (A[..., 3] > 128).astype(np.uint8)
    dong = cv2.morphologyEx(np.maximum(giu, (gpt[..., 3] > 120).astype(np.uint8)), cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.07 * H) | 1, int(0.07 * H) | 1)))
    bu = tach_ra & ~in_dau & ((dong > 0) | (gpt[..., 3] > 120)) & (lab_s != TEN.index("ham"))
    co_gpt = bu & (gpt[..., 3] > 120)
    A[co_gpt, :3] = gpt[co_gpt, :3]
    A[bu, 3] = 255
    con = bu & ~co_gpt
    if con.any():
        fill = cv2.inpaint(A[..., :3].clip(0, 255).astype(np.uint8), con.astype(np.uint8), 6, cv2.INPAINT_TELEA)
        A[con, :3] = fill[con]
    vien_bu = bu.copy()
    # bên trong bóng con thì đặc hẳn (chỉ viền ngoài giáp nền thật mới mềm); dải mảnh sát lớp đầu (da đầu lọt vào thân) bỏ đi để lấp lại
    nen0 = (a_s < 0.05).astype(np.uint8)
    trong = cv2.dilate(nen0, np.ones((5, 5), np.uint8)) == 0
    A[..., 3] = np.where(in_than & trong, 255.0, A[..., 3])
    dai_sat = in_than & (cv2.dilate(in_dau.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0) & trong
    A[dai_sat, 3] = 0
    gan = cv2.dilate(((A[..., 3] > 128)).astype(np.uint8), np.ones((3, 3), np.uint8))
    dist = cv2.distanceTransform((1 - gan).astype(np.uint8), cv2.DIST_L2, 5)
    moc = ((in_dau & (dist < 0.12 * H)) | dai_sat) & (A[..., 3] < 128)
    if moc.any():
        # màu loang từ chính lớp thân (không lấy nền trắng): dải mọc thêm dưới đầu, đầu ngửa lên thì lộ ra như cổ họng
        lo = np.asarray(anh.loang_mau(Image.fromarray(A.clip(0, 255).astype(np.uint8), "RGBA"), lan=40)).astype(np.float32)
        mm = moc & (A[..., 3] < 128)
        A[mm, :3] = lo[mm, :3]
        A[mm, 3] = 255
    # nét viền cũ giữa thân và phần đã cắt (tay, dải đai) nằm trong bóng con: xoá (vẽ bù), kẻo còn lại như vết nứt khi tay rời đi
    nen = (a_s < 0.05).astype(np.uint8)                               # nền thật của concept (không tính chỗ lớp khác)
    sat_cat = cv2.dilate(tach_ra.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    xa_nen = cv2.dilate(nen, np.ones((7, 7), np.uint8)) == 0
    sat_dau = cv2.dilate(in_dau.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    vet = (sat_cat | sat_dau) & xa_nen & (rgb_s.mean(2) < 95) & (A[..., 3] >= 128) & ~tach_ra & ~in_dau
    if vet.any():
        fill = cv2.inpaint(A[..., :3].clip(0, 255).astype(np.uint8), cv2.dilate(vet.astype(np.uint8), np.ones((3, 3), np.uint8)), 4,
                           cv2.INPAINT_TELEA)
        vv = cv2.dilate(vet.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        A[vv & (A[..., 3] >= 128), :3] = fill[vv & (A[..., 3] >= 128)]
    # nét mực dọc mép phần vẽ bù giáp nền (mép cắt răng cưa không viền)
    gan_nen = cv2.dilate(nen, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
    ke = vien_bu & gan_nen & (A[..., 3] >= 128)
    A[ke, :3] = (43, 33, 24)
    out["than"] = A
    # lớp đầu: nhãn đầu, mào; chỗ dải băng đô che: vẽ bù TELEA trong bao của vùng đầu
    B = np.zeros((H, W, 4), np.float32)
    B[..., :3] = rgb_s
    B[..., 3] = np.where(in_dau, a_s, 0.0) * 255
    dai_che = (lab_s == TEN.index("dai")) & (a_s > 0.02)
    near = cv2.dilate(in_dau.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    hole = (dai_che & near).astype(np.uint8)
    if hole.any():
        fill = cv2.inpaint(B[..., :3].clip(0, 255).astype(np.uint8), hole, 5, cv2.INPAINT_TELEA)
        B[hole > 0, :3] = fill[hole > 0]
        B[hole > 0, 3] = 255
    out["dau"] = B
    res = {}
    for nm, arr in out.items():
        m = arr[..., 3] > 8
        ys, xs = np.nonzero(m)
        c0, c1, r0, r1 = xs.min() - 2, xs.max() + 3, ys.min() - 2, ys.max() + 3
        crop = arr[r0:r1, c0:c1].clip(0, 255).astype(np.uint8)
        im = anh.loang_mau(Image.fromarray(crop, "RGBA"))
        # điểm ảnh (0, 0) của mảnh ở rig: x = c0 − ox, y = oy − r0
        dat = Dat(c0 - ox, oy - r0, neo=(0, 0), neo_px=True)
        lb = gan_nhat(lab_s[r0:r1, c0:c1].copy(), np.zeros((r1 - r0, c1 - c0), bool))
        keep = [i for i, l in lop_of.items() if l == nm]
        lbk = np.where(np.isin(lb, keep), lb, -1)
        lbk = gan_nhat(lbk, (lbk < 0))
        res[nm] = (im, dat, lbk)
    return res


def trong_so_lop(L, lbk, pick, chains, V):
    """trọng số lưới lớp: mỗi đỉnh thuộc một nhãn (đọc nhãn ở vị trí đỉnh); hoà giữa các nhãn theo khoảng cách đi trong lưới
    (trongso.vung), mỗi nhãn một bộ trọng số riêng (chains[tên](V) -> list dict). pick: {tên nhãn: chỉ số nhãn}."""
    P = np.clip(np.round(L.pts).astype(int), 0, [lbk.shape[1] - 1, lbk.shape[0] - 1])
    vl = lbk[P[:, 1], P[:, 0]]
    vung = [(nm, np.flatnonzero(vl == idx)) for nm, idx in pick.items() if (vl == idx).any()]
    mem = trongso.vung(L, vung, dai_hoa=7.0)
    Ws = {nm: chains[nm](V) for nm, _ in vung}
    out = [dict() for _ in range(L.n)]
    for i in range(L.n):
        for nm, m in mem[i].items():
            for b, w in Ws[nm][i].items():
                out[i][b] = out[i].get(b, 0.0) + m * w
    return trongso.lam_tron(L, trongso.chuan(out), 1)


def dung2_lai(ra_soi=None):
    """rig dạng 2 theo cách lai: hai lớp cắt từ concept + mảnh GPT đã khớp cho phần tách / vung xa. Cùng tên xương, slot của bản cũ
    nên clip (tm01_rig.clips2) chạy nguyên."""
    import tm01_rig as R
    from quai import khung, mieng
    import tm01_chung as C
    pc = R.manh2()
    o = R.bo_tri2(pc, R.ts2_dau(pc))
    S, D2 = R.S2, R.D2
    BV2, BT2 = R.BV2, R.BT2
    imc = pc[R.CHAN2["anh"]]
    chan_bo = [b for b in o["bo"] if b[0] is imc]
    ten_bo = {b[3]: b for b in o["bo"] if b[3]}
    bo_than = chan_bo[2:4] + [ten_bo["duoi"], ten_bo["than"], ten_bo["bc_x"], ten_bo["bc_g"]] + chan_bo[0:2]
    lp = lop(S, D2.x0, D2.y0, bo_than, ra_soi)
    sk = khung.Sk("tm01_2")
    for n in ("tay", "nam", "xoe", "giap_vai", "mi", "dai_a", "dai_b", "dai_dai"):
        sk.anh(n, pc[n])
    sk.anh("lop_than", lp["than"][0])
    sk.anh("lop_dau", lp["dau"][0])
    sz = lambda n: pc[n].size  # noqa: E731
    sk.xuong("root")
    sk.xuong("move", "root")
    Jl, gay = o["lung"], o["gay"]
    banle, mui = D2(*BANLE_C), D2(*MUI_C)        # hàm của chính concept
    sk.xuong("hong", "move", *Jl[0], dai=40)
    lung = sk.chuoi("lung", "hong", Jl)
    sk.xuong("co", lung[-1], *Jl[-1], goc=C.goc(Jl[-1], gay), dai=float(np.hypot(*(gay - Jl[-1]))), the_gioi=True)
    sk.xuong("dau", "co", *gay, goc=o["dau"].goc, dai=60, the_gioi=True)
    gj = C.goc(banle, mui)
    sk.xuong("ham", "dau", *banle, goc=gj, dai=float(np.hypot(*(mui - banle))), the_gioi=True)
    sk.xuong("mieng_dau", "dau", *(mui + np.array([4, -6])), goc=-4, dai=30, the_gioi=True)
    mao = {}
    for n in ("mao_a", "mao_b"):
        Jw = o[n].ra(o[n + "_J"], *sz(n))
        mao[n] = (Jw, sk.chuoi(n, "dau", Jw))
    dai = {}
    for n in ("dai_a", "dai_b"):
        im = pc[n]
        L = luoi.luoi_dai(im, 4, truc=[(im.width - 2, im.height / 2), (2, im.height / 2)], ten=n, buoc=12, in_tk=False)
        dai[n] = (o[n], sk.chuoi(n, "dau", o[n].ra(L.khop(4), *im.size)))
    tay = {}
    for s in ("g", "x"):
        a = o["tay_" + s]
        J = a["dat"].ra(np.array(a["J"]), *pc["tay"].size)
        tay[s] = (a["dat"], sk.chuoi("tay_" + s, lung[-1], J), a["gf"] - a["gu"])
    for s in ("g", "x"):
        nm = tay[s][1]
        W0 = sk.W0[nm[1]]
        tip = (W0 @ np.array([0.88 * sk.bones[sk.bi[nm[1]]]["length"], 0, 1.0]))[:2]
        sk.xuong("nam_" + s, nm[1], *tip, goc=sk.goc_tg(nm[1])[2], dai=30, the_gioi=True)
    sk.xuong("mieng", "nam_x", *(sk.W0["nam_x"] @ np.array([60, 0, 1.0]))[:2], goc=sk.goc_tg("nam_x")[2], dai=30, the_gioi=True)
    chan, ngon, ank = {}, {}, {}
    for s in ("g", "x"):
        J = D2.nhieu(KHOP_CHAN[s])
        names = sk.chuoi("chan_" + s, "hong", J)
        sk.xuong("bc_" + s, names[1], *J[2], goc=0, dai=30, the_gioi=True)
        lp_ = np.linalg.solve(sk.W0[names[1]], np.array([J[2][0], J[2][1], 1.0]))
        ngon[s] = (float(lp_[0]), float(lp_[1]))
        chan[s], ank[s] = (J, names), J[2]
    Jd = o["duoi"].ra(o["duoi_J"], *sz(R.DUOI2))
    duoi = sk.chuoi("duoi", "hong", Jd)
    im = pc["dai_dai"]
    Ldd = luoi.luoi_dai(im, 3, truc=[(im.width / 2, 2), (im.width / 2, im.height - 2)], ten="dai_dai", buoc=11, in_tk=False)
    dd = sk.chuoi("dd", lung[0], o["dai_dai"].ra(Ldd.khop(3), *im.size))
    sk.xuong("shadow", "root")

    # ---------------- slot (sau → trước)
    sk.slot("tay_x", tay["x"][1][0], "tay")
    sk.slot("nam_x", "nam_x", "nam")
    sk.slot("than", lung[0], "lop_than")
    sk.slot("dai_dai", dd[0], "dai_dai")
    for n in ("dai_b", "dai_a"):
        sk.slot(n, dai[n][1][0], n)
    sk.slot("dau", "dau", "lop_dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("tay_g", tay["g"][1][0], "tay")
    sk.slot("giap_vai", tay["g"][1][0], "giap_vai")
    sk.slot("nam_g", "nam_g", "nam")

    # ---------------- lớp thân (cắt từ concept): thân bám chuỗi lưng, đuôi chuỗi đuôi, chân chuỗi đùi → ống, bàn chân hoà cổ chân
    im, dat, lbk = lp["than"]
    Lt = C.bo_tg_det(luoi.luoi_vung(im, BV2, BT2, ten="lop_than"), im)
    Vt = dat.ra(Lt.pts, *im.size)
    Jt = np.vstack([Jl, [gay]])
    ch = {"than": lambda V: trongso.chuoi_chieu(V, Jt, lung + ["co"], cha="hong", cha_hoa=0.8),
          "duoi": lambda V: trongso.chuoi_chieu(V, Jd, duoi, cha="hong", cha_hoa=0.7)}
    for s in ("g", "x"):
        J, names = chan[s]
        ch["chan_" + s] = (lambda V, J=J, names=names: trongso.chuoi_chieu(V, J, names, cha="hong", cha_hoa=0.6))
        ch["bc_" + s] = (lambda V, s=s, names=names: trongso.theo_truc(V, ank[s] + np.array([0, 6.0]), ank[s] - np.array([0, 34.0]),
                                                                       names[1], "bc_" + s, 0.0, 0.6))
    pick = {n: TEN.index(n) for n in ("than", "duoi", "chan_g", "bc_g", "chan_x", "bc_x")}
    Wt = trong_so_lop(Lt, lbk, pick, ch, Vt)
    trongso.kiem(Wt, "lop_than")
    sk.luoi_gan("than", "lop_than", Lt, Wt, the_gioi=Vt)
    # ---------------- lớp đầu (cắt từ concept): đầu cứng theo xương đầu, góc dưới-sau hoà vào cổ; hai mào bám chuỗi mào
    im, dat_h, lbh = lp["dau"]
    Lh = C.bo_tg_det(luoi.luoi_vung(im, BV2, BT2, ten="lop_dau"), im)
    Vh = dat_h.ra(Lh.pts, *im.size)

    pg = lambda P: np.array(P, np.float32).reshape(-1, 1, 2)  # noqa: E731
    PH, PM, PN = pg(HAM_C), pg(MIENG_C), [pg(q) for q in NANH_C]
    ss = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1.0, max(0.0, u)))  # noqa: E731

    def w_dau(V):
        """đầu cứng; gáy hoà vào cổ; hàm dưới của concept bám xương hàm (bản lề hoà dần), lòng miệng giãn theo độ cao giữa môi trên
        và môi dưới, răng nanh trên bám đầu."""
        out = []
        for x, y in V:
            cx, cy = D2.nguoc(x, y)
            t = ss((y - (gay[1] - 26)) / 40.0)
            wc = (1 - t) * ss((gay[0] + 55 - x) / 40.0)
            wh = 0.0
            if cv2.pointPolygonTest(PH, (float(cx), float(cy)), True) >= -2:
                wh = ss((cx - 970) / 22.0)
            elif cv2.pointPolygonTest(PM, (float(cx), float(cy)), False) >= 0 and                     all(cv2.pointPolygonTest(q, (float(cx), float(cy)), True) < -1 for q in PN):
                wh = ss((cy - 377) / 24.0) * ss((cx - 970) / 22.0)
            d = {}
            if wc > 1e-3:
                d["co"] = wc
            if wh > 1e-3:
                d["ham"] = wh * (1 - wc)
            d["dau"] = max(0.0, 1 - sum(d.values()))
            out.append(d)
        return out
    chh = {"dau": w_dau}
    for n in ("mao_a", "mao_b"):
        J, names = mao[n]
        chh[n] = (lambda V, J=J, names=names: trongso.chuoi_chieu(V, J, names, cha="dau", cha_hoa=0.85))
    chh["ham"] = w_dau
    Wh = trong_so_lop(Lh, lbh, {n: TEN.index(n) for n in ("dau", "ham", "mao_a", "mao_b")}, chh, Vh)
    trongso.kiem(Wh, "lop_dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "lop_dau", Lh, Wh, the_gioi=Vh)
    # lòng miệng: là lòng miệng vẽ trong concept, giãn giữa hàm trên và hàm dưới (thịt trong miệng theo hàm dưới), không cần mảnh rời   # rộng hơn bản GPT: mép cắt hàm trên concept không đều, khép miệng vẫn nấp sau đầu
    # ---------------- mí: dò trên lớp đầu cắt từ concept
    imh = lp["dau"][0]
    p_tr = D2(985, 328)
    hat = (p_tr[0] - dat_h.x, dat_h.y - p_tr[1])
    eye = mieng.vung_mat(imh, hat, nguong=40, noi=4)
    kq = mieng.fit_lid(imh, pc["mi"], mat=eye, ten="dạng 2 (lớp đầu concept)", ti=(0.8, 2.2, 0.06), goc=(-30, 30, 3))
    R.luoi_day(sk, "mi", "mi", pc["mi"], mieng.dat_mi(dat_h, imh, kq), lambda V: trongso.cung(len(V), "dau"))
    sk.info["mi_ho"] = kq[4]
    # ---------------- dải băng đô, tay, nắm tay, bàn tay xoè, giáp vai, dải đai (GPT)
    for n, (dat, names) in dai.items():
        R.vung_chuoi(sk, n, n, pc[n], dat, names, "dau", 0.6, buoc=(BV2, BT2))
    for s, (dat, names, _) in tay.items():
        R.vung_chuoi(sk, "tay_" + s, "tay", pc["tay"], dat, names, lung[-1], 0.55, ten="tay")
        g = sk.goc_tg("nam_" + s)
        x0, y0 = g[0], g[1]
        c = np.array([x0, y0])
        u = np.array([math.cos(math.radians(g[2])), math.sin(math.radians(g[2]))])
        wf = lambda V, names=names, s=s, c=c, u=u: trongso.theo_truc(V, c - 6 * u, c + 40 * u, names[1], "nam_" + s, 0.0, 0.45)  # noqa: E731
        R.luoi_day(sk, "nam_" + s, "nam", pc["nam"], Dat(x0, y0, goc=g[2], neo=R._p(pc, "nam", R.P2["nam_co"]), neo_px=True), wf)
        R.luoi_day(sk, "nam_" + s, "xoe", pc["xoe"], Dat(x0, y0, goc=g[2] - 8, neo=R._p(pc, "xoe", R.P2["xoe_co"]), neo_px=True), wf)
    R.luoi_day(sk, "giap_vai", "giap_vai", pc["giap_vai"], o["giap_vai"], lambda V: trongso.cung(len(V), tay["g"][1][0]))
    R.vung_chuoi(sk, "dai_dai", "dai_dai", pc["dai_dai"], o["dai_dai"], dd, lung[0], 0.7, buoc=(BV2, BT2))
    for e, m in (("trung", "đòn thường trúng (nắm đấm nước bay từ găng tay trước)"), ("phun", "bắt đầu cột nước (xương mieng)"),
                 ("het_phun", "hết cột nước"), ("gam", "ngửa gầm, bờm xoè"), ("dap_dat", "đấm xuống đất: sóng lớn dâng sau đối thủ"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    info = {"lung": lung, "tay": {s: v[1] for s, v in tay.items()}, "chan": {s: v[1] for s, v in chan.items()},
            "duoi": duoi, "mao": {n: v[1] for n, v in mao.items()}, "dai": {n: v[1] for n, v in dai.items()}, "dd": dd,
            "khuyu": {s: v[2] for s, v in tay.items()}, "pc": pc, "co_chan": ank, "ngon": ngon,
            "bc0": {s: sk.goc_tg("bc_" + s)[2] for s in ("g", "x")}}
    return sk, info
