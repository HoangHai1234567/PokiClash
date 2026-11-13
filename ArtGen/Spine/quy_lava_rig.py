# -*- coding: utf-8 -*-
"""Tiểu quỷ lava (quy_lava): rig trên bộ xương của con gốc monster_3336. Mảnh của mình cắt từ năm tờ "đúng chỗ" (quy_lava_manh.py), đặt
theo concept đã duyệt; mỗi đỉnh lưới của mình lấy trọng số từ lưới part của họ nằm đúng chỗ đó (toạ độ trọng tâm trong tam giác của họ,
ngoài lưới thì nội suy theo khoảng cách), nên mảnh của mình chuyển động như part của họ. Chuyển động nền lấy mẫu từ clip của họ
(<scan>/sample_goc.json: runtime Spine thật đã giải IK hai chân và transform constraint); phần riêng ở quy_lava_clip.py.

- DÁNG GỐC của rig mình = khung 0 idle_01 của họ (concept vẽ theo dáng đó).
- Khớp khung: concept (px) → sơ đồ bố cục (khop_concept.json, dò hình bóng) → thế giới rig gốc (phép dựng sơ đồ, quy_lava_bo_cuc.khung_T).

    quy_lava_rig.py                    dựng, xuất inbox/quy_lava_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    quy_lava_rig.py tinh               dáng gốc cạnh concept → rig/soi_tinh.png
    quy_lava_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [xuong]   khung lớn nền xám → rig/soi_<clip>.png
Chạy qua quai/khoa.py nang. Xương và chuyển động nền là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi  # noqa: E402
from quai import luoi as LU  # noqa: E402
from quai.hoat import LoXo  # noqa: E402
import quy_lava as G  # noqa: E402
import quy_lava_bo_cuc as BC  # noqa: E402
import quy_lava_manh as QM  # noqa: E402

TEN = "quy_lava_1"
RA = os.path.join(QM.BASE, "rig")
SCAN = G.scan()
KG = 1.25                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 1.9                    # pixel ảnh atlas cho mỗi đơn vị rig con gốc (concept ≈ 2,2 px / đơn vị con gốc)
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
IB = I["bones"]
TENX = [b["name"] for b in IB]
KE_THUA = [i for i, b in enumerate(IB) if b.get("inherit", 0) not in (0, None)]   # xương "không nhận góc xoay của cha" (inherit 2)


def rieng(F):
    """biến đổi riêng (x, y, góc, sx, sy) của mọi xương ở một khung mẫu, đổi sang kiểu ghép THƯỜNG (runtime .atomik chỉ có noScale):
    với xương inherit 2 (đầu xem_11, hai vai xem_36, xem_37), phần xoay + tỉ lệ = nghịch đảo(2×2 thế giới cha) × 2×2 thế giới con
    (từ trường `m` của mẫu), vị trí giữ như của họ (Spine vẫn cho vị trí theo đủ biến đổi của cha)."""
    L = np.array([f[:5] for f in F["l"]], float)
    for i in KE_THUA:
        pi = IB[i]["parent"]
        Mc = np.array(F["m"][i], float).reshape(2, 2)
        Mp = np.array(F["m"][pi], float).reshape(2, 2)
        Ml = np.linalg.solve(Mp, Mc)
        sx = math.hypot(Ml[0, 0], Ml[1, 0])
        L[i, 2] = math.degrees(math.atan2(Ml[1, 0], Ml[0, 0]))
        L[i, 3], L[i, 4] = sx, float(np.linalg.det(Ml)) / sx
    return L


B0 = rieng(S["idle_01"]["frames"][0])                                     # dáng gốc của mình = khung 0 idle của họ
TIEU_DE = "Tiểu quỷ lava (quy_lava_1): tướng đầu tiên đảo Hỏa"
BO = {"root", "shadow"}
# mảnh → (slot của họ lấy trọng số theo thứ tự ưu tiên, số cột × hàng lưới); None = mảnh cứng trên xương ở XUONG
TRONG_SO = {"than": (["xem_11", "xem_16"], 9), "lua": (["xem_17"], 10), "giot1": (["xem_17"], 2), "giot2": (["xem_17"], 2),
            "tay_x": (["xem_23", "xem_25"], 6), "dot_g": (["xem_6", "xem_8", "xem_9"], 5),
            "chan_g": (["xem_15", "xem_12", "xem_13"], 4), "dui_g": (["xem_15"], 4), "chan_x": (["xem_18", "xem_14"], 4),
            "sung_g": (["xem_1"], 3), "sung_x": (["xem_0"], 3)}
XUONG = {"khien": "xem_20", "mat_g": "xem_3", "mat_x": "xem_3", "mat_g_nham": "xem_3", "mat_x_nham": "xem_3", "mieng": "xem_2",
         "nam_x": "xem_23", "giao": "xem_12", "giao_mui": "xem_12", "gang": "xem_8"}   # găng CỨNG theo cẳng tay: tay duỗi dài không kéo méo găng
MUI_GIAO = (1000.0, 913.0)        # mũi giáo trên concept (px): xương `mieng` (chỗ bắn tia lửa của chiêu mana)
SINH_DOI = {"nam_x2": ("nam_x", "giao_mui"), "tay_x2": ("tay_x", "giao_mui")}   # chiêu cuối: tay xa + nắm tay xa vẽ TRƯỚC thân và giáo, dưới găng tay  # slot sinh đôi: (mảnh gốc, vẽ ngay SAU slot này); nắm tay xa vẽ trước cán giáo lúc cầm giáo hai tay
AN = set(QM.AN) | set(SINH_DOI)
BAP_G = ("bap_g", "tay_x", "gang")   # bắp tay gần (mảnh mới, dùng lại ảnh tay xa): vai xem_7 → khuỷu xem_8, vẽ ngay TRƯỚC slot "gang"
DINH_DAU = 380.0                   # đỉnh đầu trên concept (px y): chiều cao game không tính ngọn lửa
DOI2 = None                        # dạng 2: (s, tx, ty) đưa px concept dạng 2 về px concept dạng 1 (khớp theo hai mắt + miệng)
if QM.DANG == 2:
    TEN = "quy_lava_2"
    TIEU_DE = "Hiệp sĩ dung nham (quy_lava_2): dạng 2 của tiểu quỷ lava"
    XUONG = dict(XUONG, vai_g="xem_7")       # giáp vai gai bám bắp tay gần
    XUONG["cam"] = "xem_18"                 # khối hai tay + giáo dựng (chiêu cuối) cứng theo thân trên
    MUI_GIAO = (998.0, 935.0)
    DINH_DAU = 365.0
    _M1 = np.array([(797.0, 530.0), (945.0, 523.0), (880.0, 598.0)])   # mắt gần, mắt xa, miệng trên concept dạng 1
    _M2 = np.array([(816.0, 480.0), (960.0, 480.0), (880.0, 551.0)])   # cùng mốc trên concept dạng 2
    _A = np.zeros((6, 3))
    _b = _M1.reshape(-1)
    _A[0::2, 0], _A[0::2, 1] = _M2[:, 0], 1.0
    _A[1::2, 0], _A[1::2, 2] = _M2[:, 1], 1.0
    DOI2 = tuple(float(v) for v in np.linalg.lstsq(_A, _b, rcond=None)[0])


def mat_ho(b):
    return np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]])


def khop():
    """concept px → thế giới rig gốc (khung 0 idle, đơn vị con gốc)."""
    K = json.load(open(os.path.join(HERE, "inbox", "quy_lava_1", "mau", "khop_concept.json"), encoding="utf-8"))
    if DOI2 is not None:                                                  # dạng 2: px concept dạng 2 → px concept dạng 1 → như dạng 1
        s2, a2, b2 = DOI2
        K = dict(s=K["s"] * s2, tx=K["s"] * a2 + K["tx"], ty=K["s"] * b2 + K["ty"])
    _, _, atts = G.nap(BC.ATT)
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["slot"] in BC.VAI])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = min((BC.W - 260) / (x1 - x0), (BC.H - 300) / (y1 - y0))
    ox = BC.W / 2 - (x0 + x1) / 2 * SC
    oy = BC.H - 70 + y0 * SC

    def tg(p):
        p = np.asarray(p, float)
        lx, ly = K["s"] * p[..., 0] + K["tx"], K["s"] * p[..., 1] + K["ty"]
        return np.stack([(lx - ox) / SC, (oy - ly) / SC], -1)
    return tg, SC / K["s"]


def luoi_ho():
    """{slot của họ: (đỉnh thế giới khung 0 idle (n, 2), tam giác (m, 3), trọng số [{xương: w}] mỗi đỉnh)}."""
    out = {}
    for a in A0["atts"]:
        if not a["cur"] or a.get("region") is None:
            continue
        V = np.array(a["xy"], float).reshape(-1, 2)
        _, tr = G.luoi(a)
        if a.get("w"):
            W = [{TENX[b]: w for b, w in v} for v in a["w"]]
        else:
            W = [{TENX[a["bone"]] if isinstance(a["bone"], int) else a["bone"]: 1.0}] * len(V)
        out[a["slot"]] = (V, np.asarray(tr), W)
    return out


def trong_so_tai(L, slots, p):
    """trọng số tại điểm p (thế giới con gốc) theo lưới các slot của họ: trong tam giác → toạ độ trọng tâm; ngoài → nghịch đảo d⁴."""
    for s in slots:
        V, tr, W = L[s]
        for t in tr:
            a, b, c = V[t[0]], V[t[1]], V[t[2]]
            M = np.array([b - a, c - a]).T
            if abs(np.linalg.det(M)) < 1e-9:
                continue
            l1, l2 = np.linalg.solve(M, p - a)
            l0 = 1 - l1 - l2
            if min(l0, l1, l2) >= -1e-6:
                acc = {}
                for k, lk in zip(t, (l0, l1, l2)):
                    for bn, w in W[k].items():
                        acc[bn] = acc.get(bn, 0.0) + w * lk
                return _gon(acc)
    acc = {}
    for s in slots:
        V, tr, W = L[s]
        d2 = ((V - p) ** 2).sum(1) + 4.0
        for v, k in zip(W, 1.0 / d2 ** 2):
            for bn, w in v.items():
                acc[bn] = acc.get(bn, 0.0) + w * k
    return _gon(acc)


def _gon(acc):
    tong = sum(acc.values())
    acc = {b: v / tong for b, v in acc.items() if v / tong > 0.02}
    acc = dict(sorted(acc.items(), key=lambda q: -q[1])[:4])
    tong = sum(acc.values())
    return {b: v / tong for b, v in acc.items()}


def dung(nang=None):
    dat = json.load(open(os.path.join(QM.MANH, "dat.json"), encoding="utf-8"))
    thu_tu = dat.pop("_thu_tu")
    tg, px_don_vi = khop()
    Lh = luoi_ho()
    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này (lao, nhảy)
    for i, b in enumerate(IB):
        if b["name"] in BO:
            continue
        cha = TENX[b["parent"]]
        x, y, r, sx, sy = B0[i]
        sk.xuong(b["name"], "move" if cha in BO else cha, x * KG, y * KG + ((nang or 0.0) if cha in BO else 0.0), goc=r,
                 dai=b["len"] * KG, sx=sx, sy=sy)
    nang_ = nang or 0.0

    def the_gioi(t, pts_anh):
        """điểm ảnh (px ảnh gốc của mảnh) → (thế giới rig mình, thế giới con gốc)."""
        Aff = np.array(dat[t]["A"], float)
        P = np.asarray(pts_anh, float).reshape(-1, 2)
        c = (Aff[:, :2] @ P.T).T + Aff[:, 2]
        w = tg(c)
        return w * KG + np.array([0.0, nang_]), w

    def px_tg(p):
        return tg(np.array(p, float)) * KG + np.array([0.0, nang_])

    ti_anh = PXU / px_don_vi                     # ảnh atlas = ảnh mảnh × ti_anh

    def nap(a):
        if a not in sk.images:
            g = Image.open(os.path.join(QM.MANH, a + ".png"))
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti_anh)), max(2, round(g.height * ti_anh))),
                                                        Image.LANCZOS).convert("RGBA"))
            sk.anh(a, im)
        return sk.images[a]

    def gan(t, n, ts, an=False):
        im = nap(dat[t]["anh"])
        w0, h0 = dat[t]["co"]
        L = LU.luoi_o(im.width, im.height, n, n)
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        V, Vh = the_gioi(t, uv * np.array([w0, h0], float))
        W = [ts(Vh[i]) for i in range(len(uv))]
        b0 = max(W[len(W) // 2], key=W[len(W) // 2].get)
        sk.slot(t, b0, t, an=an)
        sk.luoi_gan(t, dat[t]["anh"], L, W, the_gioi=V, ten=t)
        return W

    for t2, (goc, sau) in SINH_DOI.items():
        dat[t2] = dict(dat[goc])
        thu_tu.insert(thu_tu.index(sau) + 1, t2)
    def gan_bap(t, a):
        """bắp tay hình xúc xích dọc vai (gốc xem_7) → khuỷu (gốc xem_8), thò mỗi đầu 0,35 bề dày để hai đầu tròn chui dưới vai / găng;
        trọng số chuyển dần xem_7 → xem_8 dọc trục, nên dời xem_8 ra xa (tay dài thêm) thì bắp giãn theo."""
        im = nap(a)
        al = np.asarray(im)[..., 3] > 120
        ys, xs = np.nonzero(al)
        P_ = np.stack([xs, ys], 1).astype(float)
        c = P_.mean(0)
        _, _, Vt = np.linalg.svd(P_ - c, full_matrices=False)
        ax = Vt[0]
        tt = (P_ - c) @ ax
        nn = (P_ - c) @ np.array([-ax[1], ax[0]])
        e0, e1 = c + ax * tt.min(), c + ax * tt.max()
        day_anh = float(np.percentile(np.abs(nn), 95) * 2)
        A, Bq = sk.W0["xem_7"][:2, 2], sk.W0["xem_8"][:2, 2]
        u = (Bq - A) / np.hypot(*(Bq - A))
        rong = 0.95 * float(np.hypot(*(Bq - A)))                               # bề dày bắp tay (đơn vị rig)
        k = rong / day_anh
        q0, q1 = A - u * 0.35 * rong, Bq + u * 0.35 * rong
        L = LU.luoi_o(im.width, im.height, 7, 3)
        uv = np.asarray(L.pts, float)
        tl = (uv - e0) @ ax / max(1e-6, (e1 - e0) @ ax)
        nl = (uv - c) @ np.array([-ax[1], ax[0]])
        V = q0[None] + (q1 - q0)[None] * tl[:, None] + np.array([-u[1], u[0]])[None] * (nl * k)[:, None]
        W = []
        for q in tl:
            w8 = float(np.clip((q - 0.25) / 0.5, 0, 1))
            w8 = w8 * w8 * (3 - 2 * w8)
            W.append({b: v for b, v in (("xem_7", 1 - w8), ("xem_8", w8)) if v > 1e-3})
        sk.slot(t, "xem_7", t)
        sk.luoi_gan(t, a, L, W, the_gioi=V, ten=t)

    thu_tu.insert(thu_tu.index(BAP_G[2]), BAP_G[0])
    ds_slot = []
    for t in thu_tu:
        an = t in AN
        tk = SINH_DOI[t][0] if t in SINH_DOI else t
        if t == BAP_G[0]:
            gan_bap(t, BAP_G[1])
            ds_slot.append(t)
            continue
        if tk in TRONG_SO:
            slots, n = TRONG_SO[tk]
            W = gan(t, n, lambda p, s=slots: trong_so_tai(Lh, s, p), an)
            if nang is not None:
                xs = sorted({b for w in W for b in w})
                print(f"  {t:11s} lưới {n}×{n}  xương {xs}")
        else:
            gan(t, 2, lambda p, b=XUONG[tk]: {b: 1.0}, an)
        ds_slot.append(t)

    if nang is None:                             # lượt đo: đáy bàn chân của mình ở đâu thì nâng cả con lên chừng ấy
        day = min(float(a_["V"][:, 1].min()) for sl_ in ("chan_g", "chan_x") for a_ in sk.atts[sl_].values())
        print(f"đáy bàn chân ở y = {day:.1f}: nâng cả con {-day:.1f}")
        return dung(nang=-day)
    cao = float(px_tg((800.0, DINH_DAU))[1])
    # mũi giáo: xương `mieng` con của xương giáo, trục x chĩa theo lưỡi giáo (từ cán về mũi)
    mui = px_tg(MUI_GIAO)
    cuoi = px_tg((700.0, 690.0))
    huong = math.degrees(math.atan2(mui[1] - cuoi[1], mui[0] - cuoi[0]))
    sk.xuong("mieng", "xem_12", float(mui[0]), float(mui[1]), huong, the_gioi=True)
    sk.xuong("far", "root", 0.9 * cao + 60.0, 0.45 * cao)                    # chỗ đối thủ (game dời tới tâm thân đối thủ)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(dat=dat, thu_tu=ds_slot, cao=cao, nang=nang, px_tg=px_tg, the_gioi=the_gioi, mem=[])


def ve_tinh(sk, info):
    ve = soi.Ve(sk)
    P = khung.Pose()
    for sl in AN:
        P.alpha[sl] = 0.0
    Bx = soi._union([ve.bao(P)], 0.04)
    C = Image.open(QM.DUYET).convert("RGB")
    sc = C.height / (Bx[3] - Bx[1]) * 0.86
    im = ve.ve(P, Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
    out = Image.new("RGB", (C.width + im.width + 10, max(C.height, im.height)), (255, 255, 255))
    out.paste(C, (0, 0))
    out.paste(im, (C.width + 10, 0))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, "soi_tinh.png")
    out.save(pth)
    print(pth, out.size)


def ve_khung(sk, clips, ten, ts, sc=1.0, xuong=False):
    c = [x for x in clips if x.ten == ten][0]
    fr = hoat.nuong(sk, c)
    ve = soi.Ve(sk)
    Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
    Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
    ims = []
    for P in Ps:
        im = ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
        if xuong:
            W = sk.the_gioi(P)
            d = ImageDraw.Draw(im)
            x0, y0, x1, y1 = Bx
            for b in sk.bones:
                px_ = (W[b["name"]][0, 2] - x0) * sc
                py_ = (y1 - W[b["name"]][1, 2]) * sc
                d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], outline=(255, 0, 0), width=2)
                d.text((px_ + 4, py_ - 6), b["name"].replace("xem_", ""), fill=(255, 255, 0))
        ims.append(im)
    cot = min(len(ims), 6)
    hang = (len(ims) + cot - 1) // cot
    out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, f"soi_{ten}.png")
    out.save(pth)
    print(pth, out.size)


def main(a):
    sk, info = dung()
    if a and a[0] == "tinh":
        ve_tinh(sk, info)
        return
    import quy_lava_clip as QC
    clips, them = QC.lam_clip(sk, info)
    if a and a[0] == "soi":
        ve_khung(sk, clips, a[1], [float(x) for x in a[2].split(",")], float(a[3]) if len(a) > 3 else 1.0, "xuong" in a)
        return
    xuat.xuat_het(sk, clips, RA, TEN, TIEU_DE, dang=1, so_dang=1, dung_yen=("cast",), lao=("attack", "skill"), far=(), cao=info["cao"],
                  ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=them)


if __name__ == "__main__":
    main(sys.argv[1:])
