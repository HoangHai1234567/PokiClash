# -*- coding: utf-8 -*-
"""Dựng rig dòng tm01: dạng 2 Sóng Thần (thú rồng kỳ giông võ sĩ) và dạng 1 Tí Tách (giọt nước chibi) + tiến hóa.
Gọi qua tm01.py (rig | ghep). Toạ độ đặt mảnh đọc trên concept đã duyệt (px concept, y xuống) rồi đổi sang rig bằng Doi."""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, DayMem, LoXo, an_hien, cv, ease, lui, rung, song, bao  # noqa: E402
from quai.khung import Dat, Pose  # noqa: E402
import tm01_chung as C  # noqa: E402

INBOX = os.path.join(HERE, "inbox")


def d_(k, sub):
    return os.path.join(INBOX, f"tm01_{k}", sub)


# =====================================================================================================================
# DẠNG 2: SÓNG THẦN
# =====================================================================================================================
S2 = 0.49                      # px rig / px concept
D2 = C.Doi(S2, 750, 905)       # gốc rig: giữa hai bàn chân trên mặt đất của concept
K2 = {  # px concept / px tờ mảnh của từng mảnh (GPT vẽ mỗi mảnh một cỡ)
    "dau": 0.62, "ham": 0.47, "mieng_long": 0.40, "mi": 0.62, "mao_a": 0.72, "mao_b": 0.66, "dai_a": 0.80, "dai_b": 0.80,
    "than": 1.12, "tay": 0.66, "nam": 0.46, "xoe": 0.46, "ban_chan": 0.80, "giap_vai": 0.58,
    "dai_dai": 0.60, "chan2": 0.50, "duoi": 0.62,
}
# chân (lượt 3, M03): vẽ liền cả chi, đùi to; khớp trên ảnh mảnh: hông (trong đỉnh đùi), gối, đầu cổ chân; chỗ gắn bàn chân theo
# tỉ lệ dọc ống chân
CHAN2 = {"anh": "chan2", "hong": (255, 160), "goi": (245, 470), "cuoi": (245, 905), "bc": 0.76}   # bàn chân ngay dưới cổ giáp
GIAP2_RONG = 250.0      # bề rộng giáp vỏ sò trên ảnh chân M03 (px tờ)
# khớp trên ảnh mảnh (px tờ)
P2 = {
    "dau_mat": (335, 122), "dau_banle": (318, 214), "dau_mui": (515, 206), "dau_nut": (42, 116), "dau_co": (190, 250),
    "dau_trong_mat": (300, 112),
    "ham_banle": (45, 55), "ham_mui": (306, 64),
    "than_co": (215, 44), "than_ngoc": (235, 270), "than_vai_g": (62, 92), "than_vai_x": (262, 70), "than_hong": (150, 340),
    "duoi_J": [(25, 236), (130, 228), (250, 245), (370, 252), (480, 214), (538, 128), (470, 26)],
    "duoi2_J": [(40, 410), (200, 380), (380, 400), (560, 400), (720, 340), (820, 240), (840, 110)],
    "mao_a_J": [(60, 214), (175, 135), (290, 72), (372, 118)],
    "mao_b_J": [(48, 160), (138, 102), (225, 58), (288, 92)],
    "nam_co": (28, 96), "xoe_co": (40, 262), "ban_chan_co": (80, 26), "dai_dai_tren": (84, 8),
}
# chỗ trên concept (px concept)
Q2 = {
    "mat": (1012, 330), "hong": (745, 705), "lung": [(745, 705), (770, 612), (805, 518), (858, 440)], "dau": (905, 392),
    "vai_g": (712, 402), "khuyu_g": (592, 488), "co_tay_g": (512, 556),
    "vai_x": (878, 468), "khuyu_x": (1005, 478), "co_tay_x": (1172, 470),
    "hong_g": (845, 700), "co_chan_g": (995, 845), "hong_x": (692, 690), "co_chan_x": (480, 812),
    "duoi_goc": (612, 655), "mao_a": (800, 302), "mao_b": (712, 318), "giap": (712, 396), "dai_dai": (796, 608), "co": (905, 420),
}
H2 = 380.0                          # chiều cao dáng đứng dạng 2 (px rig): bước lưới theo luật DAC_TA mục 5
BV2, BT2 = 0.015 * H2, 0.02 * H2    # bước viền ≈ 1,5%, bước trong ≈ 2% chiều cao con
DUOI2 = "duoi"          # ảnh đuôi dùng: "duoi" (M01) hoặc "duoi2" (M03, chóp mào sóng to như concept)
GOC2 = {"duoi": -8.0, "mao_a": 0.0, "mao_b": 10.0, "dai_a": 152.0, "dai_b": 184.0, "than": -20.0}


LECH = {}   # (k, mảnh) -> (dx, dy): nap_manh cắt sát theo alpha, toạ độ đọc trên ảnh mảnh đã lưu phải trừ phần cắt


def lech_cat(k, names):
    from PIL import Image
    for n in names:
        p = os.path.join(d_(k, "manh"), n + ".png")
        if os.path.exists(p):
            bb = Image.open(p).getbbox()
            LECH[(k, n)] = (bb[0], bb[1]) if bb else (0, 0)


# phần mảnh luôn bị che mà GPT vẽ thành miệng ống (nắp ống cổ trên thân, cổ chân dưới chân): xén đi để không lộ khi động
XEN2 = {"than": [(150, 0), (300, 0), (300, 30), (150, 30)],
        "chan2": [(0, 802), (400, 802), (400, 900), (0, 900)]}      # cổ chân thừa dưới cổ giáp (bàn chân che chỗ này)


def xen(im, n, k, poly):
    from PIL import ImageDraw, Image
    a = np.asarray(im).copy()
    mk = Image.new("L", im.size, 0)
    ImageDraw.Draw(mk).polygon([_p(None, n, q) for q in poly], fill=255)
    a[..., 3][np.asarray(mk) > 0] = 0
    return Image.fromarray(a, "RGBA")


def manh2():
    giu = {n: ("tron", 200, 150, (44, 62, 158)) for n in K2}
    lech_cat(2, K2)
    pc = anh.nap_manh(d_(2, "manh"), giu, ti_le=1.0, ti_le_rieng={n: k * S2 for n, k in K2.items()})
    for n, poly in XEN2.items():
        pc[n] = anh.loang_mau(xen(pc[n], n, 2, poly))
    return pc


def _p(pc, n, key, k=None):
    """điểm ảnh (px ảnh mảnh đã lưu) -> px ảnh đã cắt sát và co của mảnh n."""
    kk = K2[n] * S2 if k is None else k
    dx, dy = LECH.get((2, n), (0, 0))
    x, y = key
    return ((x - dx) * kk, (y - dy) * kk)


TJ2 = [(150, 330), (168, 245), (192, 150), (215, 44)]          # khớp lưng trên ảnh thân (hông → gáy), px ảnh mảnh
VAI2 = {"g": (62, 92), "x": (250, 95)}                         # hốc vai trên ảnh thân
HONG2 = {"g": (275, 365), "x": (45, 345)}                       # hốc hông trên ảnh thân
RIGID2 = {"than": "than_co", "dau": "dau_mat", "mao_a": None, "mao_b": None, "duoi": None, "dai_dai": None, "giap_vai": None,
          "bc_g": "ban_chan_co", "bc_x": "ban_chan_co"}


def ts2_dau(pc):
    """tham số bố trí ban đầu: từ khop.json (dò theo màu từng mảnh) rồi đè bằng sil.json (dò theo bóng dáng)."""
    import tm01_khop as KH
    import tm01_sil as SL
    kq = KH.Khop(d_(2, "khop.json"), "doc").kq
    Q = {k: (D2(*v) if isinstance(v, tuple) else D2.nhieu(v)) for k, v in Q2.items()}
    ts = {}

    def put(n, r, x, y, g):
        ts.update({n + "_x": r["x"] if r else x, n + "_y": r["y"] if r else y, n + "_g": r["goc"] if r else g,
                   n + "_sx": r["sx"] if r else 1.0, n + "_sy": r["sy"] if r else 1.0})
    put("than", kq.get("than"), *Q["co"], GOC2["than"])
    put("dau", kq.get("dau"), *Q["mat"], 0.0)
    for n in ("mao_a", "mao_b"):
        put(n, kq.get(n), *Q[n], GOC2[n])
    put("duoi", kq.get("duoi"), *Q["duoi_goc"], GOC2["duoi"])
    put("dai_dai", kq.get("dai_dai"), *Q["dai_dai"], -96.0)
    put("giap_vai", kq.get("giap_vai"), *Q["giap"], -10.0)
    for s in ("g", "x"):
        put("bc_" + s, kq.get("bc_" + s), *Q["co_chan_" + s], 0.0)
        r = kq.get("cang_" + s)
        ts.update({"cang_%s_x" % s: r["x"] if r else Q["khuyu_" + s][0], "cang_%s_y" % s: r["y"] if r else Q["khuyu_" + s][1],
                   "cang_%s_g" % s: r["goc"] if r else C.goc(Q["khuyu_" + s], Q["co_tay_" + s]), "cang_%s_k" % s: r["sx"] if r else 1.0,
                   "cang_%s_t" % s: 1.0, "chan_%s_t" % s: 1.0, "chan_%s_hx" % s: 0.0, "chan_%s_hy" % s: 30.0})
    for n in ("dai_a", "dai_b"):
        r = kq.get(n)
        ts.update({n + "_g": (r["goc"] + 180.0) if r else GOC2[n], n + "_s": r["sx"] if r else 1.0})
    ts.update(SL.doc(d_(2, "sil.json")))
    return ts


def bo_tri2(pc, ts):
    """mọi chỗ đặt mảnh từ tham số ts: trả dict (Dat từng mảnh, khớp xương) và 'bo' = các mảnh / đoạn chi ở dáng đứng."""
    sz = lambda n: pc[n].size  # noqa: E731

    def D(n, neo, lat=False):
        sy = ts[n + "_sx"] if n in DEU2 else ts[n + "_sy"]
        return Dat(ts[n + "_x"], ts[n + "_y"], goc=ts[n + "_g"], ti=(ts[n + "_sx"], sy), neo=neo, neo_px=True, lat=lat)
    o = {"bo": []}
    o["than"] = D("than", _p(pc, "than", P2["than_co"]))
    o["dau"] = D("dau", _p(pc, "dau", P2["dau_mat"]))
    for n in ("mao_a", "mao_b"):
        o[n + "_J"] = np.array([_p(pc, n, q) for q in P2[n + "_J"]], float)
        o[n] = D(n, tuple(o[n + "_J"][0]))
    o["duoi_J"] = np.array([_p(pc, DUOI2, q) for q in P2[DUOI2 + "_J"]], float)
    o["duoi"] = D("duoi", tuple(o["duoi_J"][0]), lat=True)
    im = pc["dai_dai"]
    o["dai_dai"] = D("dai_dai", (im.width / 2, 2.0))
    o["giap_vai"] = D("giap_vai", (pc["giap_vai"].width / 2, pc["giap_vai"].height / 2))
    for s in ("g", "x"):
        o["bc_" + s] = D("bc_" + s, _p(pc, "ban_chan", P2["ban_chan_co"]))
    T = o["than"]
    o["lung"] = T.ra([_p(pc, "than", q) for q in TJ2], *sz("than"))
    hd = o["dau"]
    for key in ("co", "banle", "mui", "nut"):
        o[key] = hd.mot(_p(pc, "dau", P2["dau_" + key if key != "co" else "dau_co"]), *sz("dau"))
    o["gay"] = o["co"]
    for n in ("dai_a", "dai_b"):
        imr = pc[n]
        ga = 180.0     # trục ảnh: từ mép phải (gốc) sang trái
        k = ts[n + "_s"]
        o[n] = Dat(*o["nut"], goc=ts[n + "_g"] - ga, ti=k, neo=(imr.width - 2, imr.height / 2), neo_px=True)
    # tay
    imt = pc["tay"]
    p0, p1 = _p(pc, "tay", (3, 105)), _p(pc, "tay", (393, 105))
    seg_t = np.array([0.47, 0.53]) * (p1[0] - p0[0])
    Jt = [np.array(p0), np.array([p0[0] + seg_t[0], p0[1]]), np.array(p1)]
    for s in ("g", "x"):
        A = T.mot(_p(pc, "than", VAI2[s]), *sz("than"))
        E = np.array([ts["cang_%s_x" % s], ts["cang_%s_y" % s]])
        gf, k, th = ts["cang_%s_g" % s], ts["cang_%s_k" % s], ts["cang_%s_t" % s]
        u = (E - A) / max(1e-6, float(np.hypot(*(E - A))))
        A2 = E - u * seg_t[0] * k
        gu = C.goc(A2, E)
        du = Dat(*A2, goc=gu, ti=(k, k * th), neo=tuple(Jt[0]), neo_px=True)
        df = Dat(*E, goc=gf, ti=(k, k * th), neo=tuple(Jt[1]), neo_px=True)
        Wr = E + seg_t[1] * k * np.array([math.cos(math.radians(gf)), math.sin(math.radians(gf))])
        Fm = E + 0.88 * seg_t[1] * k * np.array([math.cos(math.radians(gf)), math.sin(math.radians(gf))])
        o["tay_" + s] = {"A": A2, "E": E, "W": Wr, "F": Fm, "gu": gu, "gf": gf, "k": k, "t": th, "dat": du, "J": Jt, "seg": seg_t}
        cu = np.zeros((imt.height, imt.width), np.float32)
        cu[:, :int(Jt[1][0]) + 4] = 1
        cf = (np.arange(imt.width)[None, :] >= int(Jt[1][0]) - 4).astype(np.float32).repeat(imt.height, 0)
        o["bo"] += [(imt, du, cu, None), (imt, df, cf, "cang_" + s)]
        o["bo"].append((pc["nam"], Dat(*Fm, goc=gf, neo=_p(pc, "nam", P2["nam_co"]), neo_px=True), None, None))
    # chân: hông ở hốc hông của thân, ngọn (chỗ bàn chân) ở cổ chân đã dò, gối gập bằng IK hai đoạn (gập ngược kim từ đường hông → cổ chân)
    nc = CHAN2["anh"]
    imc = pc[nc]
    Jc = [np.array(_p(pc, nc, CHAN2[k])) for k in ("hong", "goi", "cuoi")]
    seg_c = np.array([float(np.hypot(*(Jc[1] - Jc[0]))), float(np.hypot(*(Jc[2] - Jc[1])))])
    fb = CHAN2["bc"]
    for s in ("g", "x"):
        H = T.mot(_p(pc, "than", HONG2[s]), *sz("than")) + np.array([ts.get("chan_%s_hx" % s, 0.0), ts.get("chan_%s_hy" % s, 0.0)])
        Ak = np.array([ts["bc_%s_x" % s], ts["bc_%s_y" % s]])
        reach = float(seg_c[0] + fb * seg_c[1])
        d = float(np.hypot(*(Ak - H)))
        k = ts.get("chan_%s_du" % s, 1.05) * d / reach
        th = ts["chan_%s_t" % s]
        L1, L2 = seg_c[0] * k, fb * seg_c[1] * k
        a = math.atan2(*(Ak - H)[::-1])
        al = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
        Kn = H + L1 * np.array([math.cos(a + al), math.sin(a + al)])
        dth = Dat(*H, goc=C.goc(H, Kn) + 90, ti=(k * th, k), neo=tuple(Jc[0]), neo_px=True)
        dsh = Dat(*Kn, goc=C.goc(Kn, Ak) + 90, ti=(k * th, k), neo=tuple(Jc[1]), neo_px=True)
        o["chan_" + s] = {"H": H, "Ak": Ak, "K": Kn, "k": k, "t": th, "J": Jc, "seg": seg_c}
        rows = np.arange(imc.height)[:, None].repeat(imc.width, 1)
        o["bo"] += [(imc, dth, (rows < Jc[1][1] + 4).astype(np.float32), None),
                    (imc, dsh, (rows >= Jc[1][1] - 4).astype(np.float32), None)]
    for n in ("than", "dau", "mao_a", "mao_b", "duoi", "dai_dai", "giap_vai", "dai_a", "dai_b"):
        o["bo"].append((pc[DUOI2 if n == "duoi" else n], o[n], None, n))
    for s in ("g", "x"):
        o["bo"].append((pc["ban_chan"], o["bc_" + s], None, "bc_" + s))
    return o


DEU2 = ("dau", "mao_a", "mao_b", "giap_vai", "bc_g", "bc_x", "dai_dai")      # mảnh giữ tỉ lệ đều (không kéo méo hình vẽ)


def gioi_sil(ts, deu):
    """giới hạn dò bóng dáng: dời ±40 px rig, góc ±25°; tỉ lệ đều 0,8–1,25; tỉ lệ dọc/ngang riêng và độ dày 0,85–1,3."""
    g = {}
    for k, v in ts.items():
        if k.endswith("_hx") or k.endswith("_hy"):
            g[k] = (v - 60, v + 60, 8.0)
        elif k.endswith("_x") or k.endswith("_y"):
            g[k] = (v - 40, v + 40, 6.0)
        elif k.endswith("_g"):
            g[k] = (v - 25, v + 25, 4.0)
        elif k.endswith("_sy") and k[:-3] in deu:
            continue
        elif k.endswith("_t") or k.endswith("_sx") or k.endswith("_sy"):
            lo, hi = (0.8, 1.25) if k[:-3] in deu else (0.85, 1.3)
            if k.startswith("chan_") or k == "duoi_sy":
                hi = 1.45
            g[k] = (v * lo, v * hi, 0.05 * v)
        else:
            g[k] = (v * 0.8, v * 1.25, 0.05 * v)
    return g


def sil2():
    """dò bóng dáng dạng 2, ghi sil.json."""
    import tm01_khop as KH
    import tm01_sil as SL
    pc = manh2()
    ts = ts2_dau(pc)
    conc = KH.Concept(d_(2, os.path.join("tai_ve", "L1_duyet.png")), D2)
    if not SL.doc(d_(2, "sil.json")):          # bàn chân, dải đai: bước dò màu bóp nhỏ sai (bị che) -> bắt đầu lại từ cỡ 1
        for n in ("bc_g", "bc_x", "dai_dai"):
            ts[n + "_sx"] = ts[n + "_sy"] = 1.0
    # chân: cỡ theo số đo giáp ống chân trên concept (rộng ~120 px concept gần, ~110 px xa), độ dày 1: tìm độ cao hông cho ra cỡ đó
    # (hông giữ gần hốc hông; chân dài hơn khoảng hông – cổ chân bao nhiêu thì gối gập bấy nhiêu, như concept)
    rong_giap = {"g": 120.0 * S2, "x": 110.0 * S2}
    goi_dich = {"g": D2(962, 722), "x": D2(566, 742)}            # gối đọc trên concept
    for sd in ("g", "x"):
        best = None
        for th in (1.0, 1.1, 1.2, 1.25):
            ts["chan_%s_t" % sd] = th
            for hx in np.arange(-30, 31, 10):
                for hy in np.arange(-10, 131, 8):
                    for du in np.arange(1.02, 1.61, 0.04):
                        ts["chan_%s_hx" % sd], ts["chan_%s_hy" % sd], ts["chan_%s_du" % sd] = float(hx), float(hy), float(du)
                        c = bo_tri2(pc, ts)["chan_" + sd]
                        w = GIAP2_RONG * K2[CHAN2["anh"]] * S2 * c["k"] * th
                        e = ((w - rong_giap[sd]) / 3.0) ** 2 + (float(np.hypot(*(c["K"] - goi_dich[sd]))) / 8.0) ** 2 + 30 * (th - 1)
                        if best is None or e < best[0]:
                            best = (e, hx, hy, du, w, c["K"], th)
        _, hx, hy, du, w, Kn, th = best
        ts["chan_%s_hx" % sd], ts["chan_%s_hy" % sd], ts["chan_%s_du" % sd], ts["chan_%s_t" % sd] = float(hx), float(hy), float(du), th
        print(f"  chân {sd}: hông dời ({hx:.0f}, {hy:.0f}) px rig, dài hơn {du:.2f} lần, bè {th:.2f}, giáp rộng {w / S2:.0f} px "
              f"concept, gối lệch đích {np.hypot(*(Kn - goi_dich[sd])) / S2:.0f} px concept")
    gioi = {k: v for k, v in gioi_sil(ts, DEU2).items() if not k.startswith("chan_")}
    i0, i1 = SL.toi_uu(ts, lambda t: bo_tri2(pc, t)["bo"], conc, gioi, vong=24)
    i1b = SL.toi_uu(ts, lambda t: bo_tri2(pc, t)["bo"], conc, {k: (v[0], v[1], v[2] * 0.5) for k, v in gioi.items()}, mau_he=0.0006,
                    vong=16)[1]
    print(f"  vòng tinh (trọng số màu 0,0006): IoU {i1:.3f} → {i1b:.3f}")
    i1 = i1b
    SL.luu(ts, d_(2, "sil.json"))
    print(f"  IoU bóng dáng (ước nhanh) {i0:.3f} → {i1:.3f}; ghi {d_(2, 'sil.json')}")


LAI2 = True    # dạng 2 dựng theo cách lai (tm01_lai.py: thân, chân, đuôi, đầu, mào cắt thẳng từ concept; cần cv2 → spine-venv)


def dung2(che_do="doc"):
    if LAI2:
        import tm01_lai
        return tm01_lai.dung2_lai(d_(2, "nhan_lai.png"))
    pc = manh2()
    sk = khung.Sk("tm01_2")
    for n, im in pc.items():
        sk.anh(n, im)
    o = bo_tri2(pc, ts2_dau(pc))
    sz = lambda n: pc[n].size  # noqa: E731
    sk.xuong("root")
    sk.xuong("move", "root")
    dat_than, dat_dau = o["than"], o["dau"]
    Jl, gay, banle, mui, nut = o["lung"], o["gay"], o["banle"], o["mui"], o["nut"]
    sk.xuong("hong", "move", *Jl[0], dai=40)
    lung = sk.chuoi("lung", "hong", Jl)
    sk.xuong("co", lung[-1], *Jl[-1], goc=C.goc(Jl[-1], gay), dai=float(np.hypot(*(gay - Jl[-1]))), the_gioi=True)
    sk.xuong("dau", "co", *gay, goc=dat_dau.goc, dai=60, the_gioi=True)
    gj = C.goc(banle, mui)
    sk.xuong("ham", "dau", *banle, goc=gj, dai=float(np.hypot(*(mui - banle))), the_gioi=True)
    sk.xuong("mieng_dau", "dau", *(mui + np.array([4, -6])), goc=-4, dai=30, the_gioi=True)
    mao = {}
    for n in ("mao_a", "mao_b"):
        J, dat = o[n + "_J"], o[n]
        mao[n] = (dat, J, sk.chuoi(n, "dau", dat.ra(J, *sz(n))))
    dai = {}
    for n in ("dai_a", "dai_b"):
        im = pc[n]
        L = luoi.luoi_dai(im, 4, truc=[(im.width - 2, im.height / 2), (2, im.height / 2)], ten=n, buoc=12, in_tk=False)
        dai[n] = (L, o[n], sk.chuoi(n, "dau", o[n].ra(L.khop(4), *im.size)))
    tay = {}
    for s in ("g", "x"):
        a = o["tay_" + s]
        im = pc["tay"]
        L = luoi.luoi_dai(im, 2, truc=[tuple(a["J"][0]), tuple(a["J"][2])], ten="tay_" + s, buoc=12, in_tk=False)
        J = a["dat"].ra(np.array(a["J"]), *im.size)
        names = sk.chuoi("tay_" + s, lung[-1], J)
        tay[s] = (L, a["dat"], names, a["seg"], a["gf"] - a["gu"])
    for s in ("g", "x"):
        nm = tay[s][2]
        W0 = sk.W0[nm[1]]
        tip = (W0 @ np.array([0.88 * sk.bones[sk.bi[nm[1]]]["length"], 0, 1.0]))[:2]
        sk.xuong("nam_" + s, nm[1], *tip, goc=sk.goc_tg(nm[1])[2], dai=30, the_gioi=True)
    sk.xuong("mieng", "nam_x", *(sk.W0["nam_x"] @ np.array([60, 0, 1.0]))[:2], goc=sk.goc_tg("nam_x")[2], dai=30, the_gioi=True)
    chan, bc_dat, ngon = {}, {}, {}
    for s in ("g", "x"):
        c = o["chan_" + s]
        im = pc[CHAN2["anh"]]
        L = luoi.luoi_dai(im, 2, truc=[tuple(c["J"][0]), tuple(c["J"][2])], ten="chan_" + s, buoc=12, in_tk=False)
        H, Ak, k, th = c["H"], c["Ak"], c["k"], c["t"]
        dat = Dat(*H, goc=C.goc(H, Ak) + 90, ti=(k * th, k), neo=tuple(c["J"][0]), neo_px=True)
        names = sk.chuoi("chan_" + s, "hong", dat.ra(np.array(c["J"]), *im.size))
        sk.xuong("bc_" + s, names[1], *Ak, goc=0, dai=30, the_gioi=True)
        lp = np.linalg.solve(sk.W0[names[1]], np.array([Ak[0], Ak[1], 1.0]))
        ngon[s] = (float(lp[0]), float(lp[1]))
        chan[s] = (L, dat, names, c["seg"])
        bc_dat[s] = o["bc_" + s]
    Jd, dat_duoi = o["duoi_J"], o["duoi"]
    duoi = sk.chuoi("duoi", "hong", dat_duoi.ra(Jd, *sz(DUOI2)))
    im = pc["dai_dai"]
    Ldd = luoi.luoi_dai(im, 3, truc=[(im.width / 2, 2), (im.width / 2, im.height - 2)], ten="dai_dai", buoc=11, in_tk=False)
    dat_dd = o["dai_dai"]
    dd = sk.chuoi("dd", lung[0], dat_dd.ra(Ldd.khop(3), *im.size))
    dat_gv = o["giap_vai"]
    sk.xuong("shadow", "root")

    # ---------------- slot (sau → trước)
    for n in ("dai_b", "dai_a"):
        sk.slot(n, dai[n][2][0], n)
    sk.slot("tay_x", tay["x"][2][0], "tay")
    sk.slot("nam_x", "nam_x", "nam")
    sk.slot("duoi", duoi[0], DUOI2)
    sk.slot("bc_x", "bc_x", "ban_chan")
    sk.slot("chan_x", chan["x"][2][0], CHAN2["anh"])
    sk.slot("mao_b", mao["mao_b"][2][0], "mao_b")
    sk.slot("mao_a", mao["mao_a"][2][0], "mao_a")
    sk.slot("than", lung[0], "than")
    sk.slot("bc_g", "bc_g", "ban_chan")
    sk.slot("chan_g", chan["g"][2][0], CHAN2["anh"])       # chân gần trước bụng (đùi ló dưới đai như concept), sau dải đai
    sk.slot("dai_dai", dd[0], "dai_dai")
    sk.slot("mieng_long", "ham", "mieng_long")
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("tay_g", tay["g"][2][0], "tay")
    sk.slot("giap_vai", tay["g"][2][0], "giap_vai")
    sk.slot("nam_g", "nam_g", "nam")

    # ---------------- lưới + trọng số
    # thân: lưới vùng, trọng số chuỗi chiếu lên đường lưng (hông → gáy), gốc hoà vào hông
    im = pc["than"]
    Lt = luoi.luoi_vung(im, BV2, BT2, ten="than")
    Vt = dat_than.ra(Lt.pts, *im.size)
    Jt = np.vstack([Jl, [gay]])
    Wt = trongso.chuoi_chieu(Vt, Jt, lung + ["co"], cha="hong", cha_hoa=0.8)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, the_gioi=Vt)
    # đầu: lưới vùng; góc dưới-sau (gáy) hoà vào cổ
    im = pc["dau"]
    Lh = luoi.luoi_vung(im, BV2, BT2, ten="dau")
    w, h = im.size
    gx, gy = _p(pc, "dau", P2["dau_co"])
    Wh = trongso.vung(Lh, [("co", [(0, gy - 0.12 * h), (gx, gy - 0.05 * h), (gx + 0.1 * w, h), (0, h)]),
                           ("dau", [(0, 0), (w, 0), (w, h), (0, h)])], dai_hoa=0.10 * w)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    # hàm dưới: hai xương (sau bản lề bám đầu, trước bám hàm)
    im = pc["ham"]
    hb = _p(pc, "ham", P2["ham_banle"])
    hm = _p(pc, "ham", P2["ham_mui"])
    dat_ham = Dat(*banle, goc=gj - math.degrees(math.atan2(-(hm[1] - hb[1]), hm[0] - hb[0])),
                  ti=float(np.hypot(*(mui - banle))) / float(np.hypot(hm[0] - hb[0], hm[1] - hb[1])), neo=hb, neo_px=True)
    Lj = luoi.luoi_vung(im, 0.85 * BV2, 0.85 * BT2, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *im.size), banle, mui, "dau", "ham", u0=-0.05, u1=0.18)
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    # lòng miệng: thuộc hàm dưới
    mieng.long_mieng(sk, "mieng_long", "mieng_long", "dau", "ham", banle, mui, tren=(-0.02, -0.04, -0.07, -0.10, -0.12),
                     duoi=-0.22, doc=(-0.02, 0.92))
    # mí mắt: dò cho phủ kín mắt
    hat = _p(pc, "dau", P2["dau_trong_mat"])
    eye = mieng.vung_mat(pc["dau"], hat, nguong=40, noi=4)
    kq = mieng.fit_lid(pc["dau"], pc["mi"], mat=eye, ten="dạng 2", ti=(0.8, 2.0, 0.08), goc=(-30, 30, 4))
    luoi_day(sk, "mi", "mi", pc["mi"], mieng.dat_mi(dat_dau, pc["dau"], kq), lambda V: trongso.cung(len(V), "dau"))
    sk.info["mi_ho"] = kq[4]
    # mào: lưới vùng + chuỗi chiếu lên khớp
    for n, (dat, J, names) in mao.items():
        im = pc[n]
        L = luoi.luoi_vung(im, BV2, BT2, ten=n)
        V = dat.ra(L.pts, *im.size)
        W = trongso.chuoi_chieu(V, dat.ra(J, *im.size), names, cha="dau", cha_hoa=0.85)
        sk.luoi_gan(n, n, L, trongso.lam_tron(L, W, 1), the_gioi=V)
    # dải băng đô
    for n, (L, dat, names) in dai.items():
        vung_chuoi(sk, n, n, pc[n], dat, names, "dau", 0.6, buoc=(BV2, BT2))
    # tay, nắm tay, bàn tay xoè
    for s, (L, dat, names, seg, _) in tay.items():
        vung_chuoi(sk, "tay_" + s, "tay", pc["tay"], dat, names, lung[-1], 0.55, ten="tay")
        g = sk.goc_tg("nam_" + s)
        x0, y0 = g[0], g[1]
        co_tay = np.array([x0, y0])
        u = np.array([math.cos(math.radians(g[2])), math.sin(math.radians(g[2]))])
        wf = lambda V, s=s, c=co_tay, u=u: trongso.theo_truc(V, c - 6 * u, c + 40 * u, tay[s][2][1], "nam_" + s, 0.0, 0.45)  # noqa: E731
        luoi_day(sk, "nam_" + s, "nam", pc["nam"], Dat(x0, y0, goc=g[2], neo=_p(pc, "nam", P2["nam_co"]), neo_px=True), wf)
        luoi_day(sk, "nam_" + s, "xoe", pc["xoe"], Dat(x0, y0, goc=g[2] - 8, neo=_p(pc, "xoe", P2["xoe_co"]), neo_px=True), wf)
    # giáp vai: đồ cứng trên cánh tay trên của tay gần
    luoi_day(sk, "giap_vai", "giap_vai", pc["giap_vai"], dat_gv, lambda V: trongso.cung(len(V), tay["g"][2][0]))   # vỏ ốc: đồ cứng thật
    # chân, bàn chân
    for s, (L, dat, names, seg) in chan.items():
        vung_chuoi(sk, "chan_" + s, CHAN2["anh"], pc[CHAN2["anh"]], dat, names, "hong", 0.6, ten=CHAN2["anh"])
        ak = np.array([bc_dat[s].x, bc_dat[s].y])
        luoi_day(sk, "bc_" + s, "ban_chan", pc["ban_chan"], bc_dat[s],
                 lambda V, s=s, ak=ak: trongso.theo_truc(V, ak + np.array([0, 4.0]), ak - np.array([0, 40.0]), chan[s][2][1], "bc_" + s, 0.0, 0.5))
    # đuôi: lưới vùng, chuỗi chiếu lên khớp (đuôi vẽ cong sẵn)
    im = pc[DUOI2]
    L = luoi.luoi_vung(im, BV2, BT2, ten="duoi")
    W = trongso.chuoi_geo(L, Jd, duoi, cha="hong", cha_hoa=0.7)
    W = trongso.lam_tron(L, W, 1)
    trongso.kiem(W, "duoi")
    sk.luoi_gan("duoi", DUOI2, L, W, dat=dat_duoi)
    # dải đai
    vung_chuoi(sk, "dai_dai", "dai_dai", pc["dai_dai"], dat_dd, dd, lung[0], 0.7, buoc=(BV2, BT2))

    for e, m in (("trung", "đòn thường trúng (nắm đấm nước bay từ găng tay trước)"), ("phun", "bắt đầu cột nước (xương mieng)"),
                 ("het_phun", "hết cột nước"), ("gam", "ngửa gầm, bờm xoè"), ("dap_dat", "đấm xuống đất: sóng lớn dâng sau đối thủ"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    info = {"lung": lung, "tay": {s: v[2] for s, v in tay.items()}, "chan": {s: v[2] for s, v in chan.items()},
            "duoi": duoi, "mao": {n: v[2] for n, v in mao.items()}, "dai": {n: v[2] for n, v in dai.items()}, "dd": dd,
            "khuyu": {s: v[4] for s, v in tay.items()}, "pc": pc,
            "co_chan": {s: np.array([bc_dat[s].x, bc_dat[s].y]) for s in ("g", "x")}, "ngon": ngon,
            "bc0": {s: sk.goc_tg("bc_" + s)[2] for s in ("g", "x")}}
    return sk, info


def vung_chuoi(sk, slot, ten_anh, im, dat, names, cha, cha_hoa, buoc=None, ten=None):
    """lưới vùng đều cho mảnh duỗi thẳng, trọng số B-spline chiếu lên đường khớp của chuỗi (thế giới dáng gốc)."""
    buoc = buoc or (BV2, BT2)
    L = luoi.luoi_vung(im, buoc[0], buoc[1], ten=slot)
    V = dat.ra(L.pts, *im.size)
    J = [sk.W0[names[0]][:2, 2]] + [sk.W0[b] @ np.array([sk.bones[sk.bi[b]]["length"], 0, 1.0]) for b in names]
    J = np.array([np.asarray(j)[:2] for j in J])
    W = trongso.lam_tron(L, trongso.chuoi_chieu(V, J, names, cha=cha, cha_hoa=cha_hoa), 1)
    trongso.kiem(W, slot)
    sk.luoi_gan(slot, ten_anh, L, W, the_gioi=V, ten=ten)
    return L


def luoi_day(sk, slot, ten_anh, im, dat, wfn, buoc=None):
    """mảnh nhỏ (nắm tay, bàn chân, giáp, mí) cũng là lưới dày đều (không còn mảnh 4 đỉnh); wfn(V thế giới) -> trọng số."""
    b = buoc or (BV2, BT2)
    L = luoi.luoi_vung(im, b[0], b[1], ten=f"{slot}/{ten_anh}")
    V = dat.ra(L.pts, *im.size)
    sk.luoi_gan(slot, ten_anh, L, trongso.chuan(wfn(V)), the_gioi=V, ten=ten_anh)
    return L


def chan_bam(sk, P, info, cao=0.0, uon={"g": 1.0, "x": 1.0}):
    """IK chân: cổ chân về chỗ dáng gốc (theo move), bàn chân giữ góc thế giới dáng gốc (bám phẳng đất)."""
    W = sk.the_gioi(P)
    for s, names in info["chan"].items():
        tgt = (W["move"] @ np.array([*info["co_chan"][s], 1.0]))[:2]
        hoat.ik_hai_doan(sk, P, names[0], names[1], tgt, ngon=info["ngon"][s], uon=uon.get(s))
    W = sk.the_gioi(P)
    for s in ("g", "x"):
        a = khung.goc_mat(W["bc_" + s])
        mv = khung.goc_mat(W["move"])
        P.rot("bc_" + s, ((info["bc0"][s] + mv - a) + 180) % 360 - 180)


def the_dung2(P, info):
    """dáng đứng theo concept: khuỷu gập, hàm hé."""
    for s in ("g", "x"):
        P.rot(info["tay"][s][1], info["khuyu"][s])
    P.rot("ham", -6)


# ---------------------------------------------------------------- clip dạng 2
def mem2(info):
    """phần mềm dạng 2: mào (lò xo cứng), dải băng đô (dây mềm có gió), dải đai (lò xo), đuôi (lò xo nhẹ trên sóng)."""
    def gio(t, i):
        return np.array([-600.0 - 400.0 * math.sin(2 * math.pi * t / 1.2 + 0.8 * i), 300.0 * math.cos(2 * math.pi * t / 0.8 + i)])
    return [LoXo(info["mao"]["mao_a"], k=[420, 330, 260], damp=0.6, maxang=10),
            LoXo(info["mao"]["mao_b"], k=[440, 350, 270], damp=0.6, maxang=10),
            DayMem(info["dai"]["dai_a"], k0=0.24, k1=0.07, zeta=0.45, luc=gio, lim=(16, 26)),
            DayMem(info["dai"]["dai_b"], k0=0.26, k1=0.08, zeta=0.45, luc=lambda t, i: gio(t + 0.37, i + 2), lim=(16, 26)),
            LoXo(info["dd"], k=[380, 300, 230], damp=0.55, maxang=14),
            LoXo(info["duoi"], k=[700, 600, 500, 420, 360, 320], damp=0.65, maxang=8)]


def clips2(sk, info):
    T = 2.4                                   # chu kỳ idle (dạng cuối: vòng dài hơn)
    tg, tx = info["tay"]["g"], info["tay"]["x"]
    lung, duoi = info["lung"], info["duoi"]
    tail_amp = [1.5, 2.2, 3.0, 4.0, 5.0, 6.0]

    def nen(P, tt, a=1.0):
        """dao động nền idle, trừ giá trị ở giây 0 (khung 0 idle = dáng concept)."""
        Q1, Q0 = Pose(), Pose()
        nen_tho(Q1, tt, a)
        nen_tho(Q0, 0.0, a)
        for bn, v in Q1.t.items():
            v0 = Q0.t.get(bn, [0, 0, 0, 1, 1])
            P.move(bn, v[0] - v0[0], v[1] - v0[1])
            P.rot(bn, v[2] - v0[2])

    def nen_tho(P, tt, a=1.0):
        s1, s2 = song(tt, T), song(tt, T, -0.9)
        P.move("hong", 0, -2.2 * s1 * a)
        P.rot(lung[0], 0.6 * s1 * a)
        P.rot(lung[1], 1.0 * s2 * a)
        P.rot(lung[2], 1.2 * song(tt, T, -1.6) * a)
        P.rot("dau", -1.8 * song(tt, T, -1.6) * a + 0.8 * song(tt, T / 2, 0.4) * a)
        P.rot(tg[0], 2.5 * song(tt, T, -2.0) * a)
        P.rot(tg[1], 3.5 * song(tt, T, -2.6) * a)
        P.rot(tx[0], 1.8 * song(tt, T, -2.2) * a)
        P.rot(tx[1], -3.0 * song(tt, T, -2.8) * a)
        hoat.chuoi_song(P, duoi, tt, T, np.array(tail_amp) * a, tre=0.12, ngon_dan=False)

    def ket(P):
        chan_bam(sk, P, info)

    def idle(t, P):
        the_dung2(P, info)
        nen(P, t)
        P.rot("ham", -cv(t, [(0, 0), (1.62, 0), (1.70, 13, "out"), (1.80, 4), (1.88, 10, "out"), (2.05, 0, "io"), (T, 0)]))
        an_hien(P, "mi", t, [(1.38, 1.50)])
        ket(P)

    def appear(t, P, D=1.4):
        the_dung2(P, info)
        sx = cv(t, [(0, 1.5), (0.32, 0.82, "out"), (0.52, 1.08, "io"), (0.7, 0.97, "io"), (0.85, 1.0, "io"), (D, 1.0)])
        sy = cv(t, [(0, 0.04), (0.32, 1.22, "out"), (0.52, 0.92, "io"), (0.7, 1.03, "io"), (0.85, 1.0, "io"), (D, 1.0)])
        P.scale("move", sx, sy)
        a = cv(t, [(0, 0), (0.14, 1, "io")])
        for sl in sk.slots:
            if sl["alpha"] > 0:
                P.alpha[sl["name"]] = a
        nen(P, lui(t, D), ease((t - 0.7) / 0.5))
        pump = cv(t, [(0, 0), (0.78, 0), (0.92, 1, "out"), (1.12, 1), (D, 0, "io")])
        P.rot(tx[0], 55 * pump)
        P.rot(tx[1], 35 * pump)
        P.rot("co", 5 * pump)
        P.rot("dau", 7 * pump)
        P.rot("ham", -24 * pump)
        ket(P)

    def attack(t, P, D=1.0, H=0.46):
        the_dung2(P, info)
        nen(P, lui(t, D), 1 - 0.8 * bao(t, 0.05, 0.9, 0.15, 0.2))
        ch = cv(t, [(0, 0), (0.28, 1, "io"), (0.36, 1.05), (H - 0.03, 0.35, "in"), (H, -0.1, "out"), (0.72, -0.05), (D, 0, "io")])
        ex = cv(t, [(0, 0), (0.36, 0), (H, 1, "in"), (0.5, 1.06), (0.74, 0.95), (D, 0, "io")])
        P.rot(tx[0], -55 * ch + 6 * ex)
        P.rot(tx[1], 105 * ch - info["khuyu"]["x"] * ex)
        P.rot(tg[0], 6 * ch + 14 * ex)
        P.rot(tg[1], 10 * ex)
        P.move("hong", -8 * ch + 12 * ex, -3 * ch)
        P.rot(lung[1], 4 * ch - 5 * ex)
        P.rot(lung[2], 5 * ch - 6 * ex)
        P.rot("dau", 3 * ch - 4 * ex)
        P.rot("ham", -cv(t, [(0, 0), (0.3, 0), (H, 22, "out"), (0.7, 16), (D, 0, "io")]))
        sm = cv(t, [(0, 1), (H - 0.034, 1), (H, 1.16), (H + 0.034, 0.97), (0.6, 1), (D, 1)])
        P.scale("nam_x", sm, 2 - sm)
        ket(P)

    def cast(t, P, D=1.6, H=0.72, E=1.3):
        the_dung2(P, info)
        nen(P, lui(t, D), 1 - 0.85 * bao(t, 0.05, 1.5, 0.2, 0.25))
        g = cv(t, [(0, 0), (0.5, 1, "io"), (0.6, 1.04), (H, 0, "in"), (E, 0), (D, 0)])
        th = cv(t, [(0, 0), (0.58, 0), (H, 1, "out"), (E, 1), (D, 0, "io")])
        r = rung(t, H + 0.03, E)
        P.rot(tx[0], -62 * g - 9 * th + 1.2 * r)
        P.rot(tx[1], 80 * g - info["khuyu"]["x"] * th)
        P.rot(tg[0], -18 * g + 116 * th + 1.5 * r)
        P.rot(tg[1], 40 * g - info["khuyu"]["g"] * th)
        P.move("hong", -6 * g + 8 * th, -7 * g - 4 * th)
        P.rot(lung[1], 6 * g - 5 * th + 0.8 * r)
        P.rot(lung[2], 7 * g - 6 * th)
        P.rot("dau", 4 * g - 2 * th + 1.0 * r)
        P.rot("ham", -(cv(t, [(0, 0), (0.5, 4), (H, 24, "out"), (E, 20), (D, 0, "io")]) + 2.5 * r))
        open_ = 0.66 <= t < 1.36
        for sd in ("g", "x"):
            P.att["nam_" + sd] = "xoe" if open_ else "nam"
        ket(P)

    def skill(t, P, D=2.2, R=0.75, H=1.2, E=1.7):
        the_dung2(P, info)
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.05, 2.1, 0.2, 0.35))
        co = cv(t, [(0, 0), (0.5, 1, "io"), (R, 0, "out"), (D, 0)])
        up = cv(t, [(0, 0), (0.5, 0), (R, 1, "out"), (1.02, 1), (H, 0, "in"), (D, 0)])
        sl = cv(t, [(0, 0), (1.02, 0), (H, 1, "in"), (H + 0.05, 1.05), (E, 0.92), (D, 0, "io")])
        r = rung(t, R + 0.03, 1.02) + 0.5 * rung(t, H + 0.04, 1.5)
        P.move("hong", -4 * co, -11 * co + 6 * up - 15 * sl)
        P.rot(lung[0], -3 * co + 3 * up - 8 * sl)
        P.rot(lung[1], -4 * co + 6 * up - 9 * sl + 0.8 * r)
        P.rot(lung[2], -3 * co + 7 * up - 8 * sl)
        P.rot("co", 1 * co + 13 * up - 5 * sl)
        P.rot("dau", 1 * co + 4 * up - 2 * sl + 1.4 * r)
        P.rot("ham", -(26 * up + 10 * sl + 2.5 * abs(r)))
        P.rot(tx[0], -50 * co + 95 * up - 62 * sl + 1.5 * r)
        P.rot(tx[1], 30 * co + 10 * up - 25 * sl)
        P.rot(tg[0], 25 * co - 120 * up + 105 * sl + 1.5 * r)
        P.rot(tg[1], 20 * co - 20 * up - 30 * sl)
        ket(P)

    def hit(t, P, D=0.6):
        the_dung2(P, info)
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.5, "io"), (0.42, -0.1, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.06, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        P.rot("co", 6 * hd)
        P.rot("dau", 10 * hd)
        P.rot(lung[2], 8 * bd)
        P.rot(lung[1], 4 * bd)
        P.move("hong", -12 * bd, 0)
        P.rot("ham", -14 * hd)
        P.rot(tx[0], 14 * hd)
        P.rot(tx[1], 12 * bd)
        P.rot(tg[0], -10 * bd)
        an_hien(P, "mi", t, [(0.03, 0.34)])
        n = len(duoi)
        for i, b in enumerate(duoi):
            P.rot(b, (3 + 1.5 * i) * cv(t, [(0, 0), (0.07 + 0.025 * (n - 1 - i), 1, "out"), (0.32 + 0.025 * i, -0.3, "io"), (D, 0, "io")]))
        ket(P)

    def die(t, P, D=2.2):
        the_dung2(P, info)
        j = cv(t, [(0, 0), (0.07, 1, "out"), (0.3, 0.4, "io"), (D, 0.4)])
        sag = cv(t, [(0, 0), (0.25, 0), (0.85, 1, "io"), (D, 1)])
        sway = math.sin(2 * math.pi * (t - 0.85) / 0.7) * bao(t, 0.85, 1.35, 0.1, 0.15)
        melt = cv(t, [(0, 0), (1.3, 0), (1.95, 1, "in"), (D, 1)])
        P.rot("co", 6 * j - 12 * sag)
        P.rot("dau", 8 * j - 14 * sag + 4 * sway)
        P.rot("ham", -(10 * j + 22 * sag))
        P.rot(lung[2], 6 * j - 9 * sag + 2 * sway)
        P.rot(lung[1], -6 * sag)
        P.rot(tx[0], 10 * j - 70 * sag)
        P.rot(tx[1], -info["khuyu"]["x"] * sag * 0.6)
        P.rot(tg[0], -10 * j + 25 * sag)
        P.move("hong", -8 * j, -22 * sag)
        P.scale("move", 1 + 0.35 * melt, 1 - 0.85 * melt)
        a = cv(t, [(0, 1), (1.6, 1), (2.12, 0, "io"), (D, 0)])
        for sl in sk.slots:
            if sl["alpha"] > 0:
                P.alpha[sl["name"]] = a
        P.alpha["mi"] = a if t >= 0.04 else 0.0
        ket(P)

    def m():
        return mem2(info)
    return [Clip("appear", 1.4, appear, mem=m()),
            Clip("idle", T, idle, loop=True, mem=m()),
            Clip("attack", 1.0, attack, ev=[(0.46, "trung", "")], mem=m()),
            Clip("cast", 1.6, cast, ev=[(0.72, "phun", ""), (1.3, "het_phun", "")], mem=m()),
            Clip("skill", 2.2, skill, ev=[(0.75, "gam", ""), (1.2, "dap_dat", ""), (1.8, "het_gam", "")], trung=1.2, mem=m()),
            Clip("hit", 0.6, hit, mem=m()),
            Clip("die", 2.2, die, mem=m())]


def so_concept(sk, frames_idle, concept, doi, ra):
    """ảnh khung 0 idle cạnh concept cùng tỉ lệ + ảnh khác biệt mặt nạ; in IoU lên ảnh."""
    from PIL import Image, ImageDraw
    ve = soi.Ve(sk)
    C.ghep_concept(ve, frames_idle[0], concept, doi, ra)
    v, chi_c, chi_r = C.iou_concept(ve, frames_idle[0], concept, doi, ra[:-4] + "_iou.png")
    im = Image.open(ra).convert("RGB")
    d = ImageDraw.Draw(im)
    d.text((10, 10), f"IoU mặt nạ khung 0 idle / concept: {v:.3f} (chỉ concept {chi_c} px, chỉ rig {chi_r} px)", fill=(180, 0, 0),
           font=anh.font(22))
    im.save(ra)
    print(f"  so_concept: IoU {v:.3f}")
    return v


def uon_thu2(sk, info, ra):
    P = Pose()
    the_dung2(P, info)
    for b in info["duoi"]:
        P.rot(b, 18)
    P.rot(info["tay"]["x"][1], 60)
    P.rot(info["tay"]["g"][1], -50)
    P.rot("ham", -30)
    for n in info["mao"].values():
        for b in n:
            P.rot(b, 12)
    for n in info["dai"].values():
        for b in n:
            P.rot(b, -14)
    chan_bam(sk, P, info)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110)).convert("RGB").save(ra)


def rig2(xuat_ra=True):
    t0 = time.time()
    sk, info = dung2()
    cl = clips2(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"dạng 2: nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
    if not xuat_ra:
        return sk, info, cl, fr, None
    ra = d_(2, "rig")
    os.makedirs(ra, exist_ok=True)
    so_concept(sk, fr["idle"], d_(2, os.path.join("tai_ve", "L1_duyet.png")), D2, os.path.join(ra, "so_concept.png"))
    tong = xuat.xuat_het(sk, cl, ra, "tm01_2", "Sóng Thần (tm01 dạng 2)", frames=fr, dang=2, so_dang=2,
                         dung_yen=("attack", "cast", "skill"), ma_goc=3211,
                         can=[("can_mieng_skill", "skill", 0.9, "ham", 55), ("can_mieng_cast", "cast", 0.9, "ham", 55),
                              ("can_tay_attack", "attack", 0.46, "tay_x1", 70), ("can_mi_hit", "hit", 0.1, "dau", 45),
                              ("can_chan_skill", "skill", 1.25, "chan_g1", 70), ("can_co_skill", "skill", 0.85, "co", 70),
                              ("can_chan_attack", "attack", 0.46, "chan_g1", 70), ("can_chan_xa_skill", "skill", 1.25, "chan_x1", 70)])
    uon_thu2(sk, info, os.path.join(ra, "uon_thu.png"))
    print(f"xong dạng 2 {time.time() - t0:.1f} s; mí còn hở {sk.info.get('mi_ho')} px")
    return sk, info, cl, fr, tong


def main(cmd, k):
    if k == 2 and cmd == "sil":
        sil2()
        return
    if k == 2 and cmd == "ghep":
        sk, info = dung2()
        P = Pose()
        the_dung2(P, info)
        chan_bam(sk, P, info)
        ve = soi.Ve(sk)
        print(C.ghep_concept(ve, P, d_(2, os.path.join("tai_ve", "L1_duyet.png")), D2, d_(2, "ghep.png")))
        return
    if k == 2 and cmd == "rig":
        rig2()
        return
    if k == 1:
        import tm01_rig1
        tm01_rig1.main(cmd)
        return
    raise SystemExit("chưa có lệnh này")
