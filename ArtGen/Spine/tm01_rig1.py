# -*- coding: utf-8 -*-
"""Dạng 1 Tí Tách (giọt nước chibi) của dòng tm01 + clip tiến hóa gộp dạng 2. Gọi qua tm01.py (rig 1 | ghep 1).

Thân là MỘT lưới dày (mào cuộn nằm trong lưới thân, bám chuỗi 3 đốt), nén giãn là diễn xuất chính (học con gốc: xương gốc nén
giãn ở đáy, tâm thân, đỉnh, chóp 2 đốt). Mắt vẽ trên thân; mí, mắt `> <`, bốn miệng là hình dán lên thân với trọng số nội suy từ
lưới thân (nén giãn cùng thân, không trượt). Toạ độ đặt mảnh đọc trên ảnh thân của tờ mảnh (đơn vị B = px ảnh thân đã lưu)."""
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
import tm01_rig as R2  # noqa: E402

S1 = 0.46                         # px rig / đơn vị B (px ảnh thân)
D1 = C.Doi(S1, 213, 600)          # gốc: giữa hai bàn chân trên mặt đất (toạ độ B)
K1 = {"than": 1.0, "m_het": 0.77, "m_tron": 0.77, "m_mim": 0.77, "m_nghien": 0.77, "nham_gan": 1.0, "nham_xa": 1.0,
      "ep_gan": 1.0, "ep_xa": 1.0, "tay": 0.9, "ban_chan": 0.74, "duoi": 0.72, "dai_a": 0.8, "dai_b": 0.8}
# toạ độ trên ảnh mảnh (px ảnh đã lưu)
P1 = {"tay_vai": (3, 55), "tay_nam": (226, 52), "duoi_J": [(25, 98), (100, 100), (175, 90), (225, 55), (272, 24)],
      "ban_chan_day": (85, 96)}
# chỗ trên thân (đơn vị B)
Q1 = {"day": (215, 578), "than": (215, 420), "dinh": (238, 262), "tren": (250, 165),
      "mao": [(240, 165), (292, 42), (380, 44), (408, 128)],
      "mat_gan": (196, 306), "mat_xa": (339, 300), "mieng": (300, 374),
      "nam_g": (466, 322), "goc_tay_g": 50.0, "nam_x": (-28, 372), "goc_tay_x": 162.0,
      "bc_g": (322, 600), "bc_x": (104, 600), "duoi_goc": (112, 482), "goc_duoi": -12.0,
      "nut": (62, 206), "goc_dai_a": 158.0, "goc_dai_b": 196.0}
H1 = 280.0                          # chiều cao dáng đứng dạng 1 (px rig)
BV1, BT1 = 0.015 * H1, 0.02 * H1    # bước viền ≈ 1,5%, bước trong ≈ 2% chiều cao con
MAO_VUNG = [(195, 0), (440, 0), (440, 215), (330, 190), (250, 172), (195, 152)]


def d_(sub):
    return os.path.join(HERE, "inbox", "tm01_1", sub)


def manh1():
    R2.LECH.clear()
    from PIL import Image
    for n in K1:
        p = os.path.join(d_("manh"), n + ".png")
        bb = Image.open(p).getbbox()
        R2.LECH[(1, n)] = (bb[0], bb[1])
    giu = {n: ("tron", 120, 120, (53, 191, 230)) for n in K1}
    return anh.nap_manh(d_("manh"), giu, ti_le=1.0, ti_le_rieng={n: k * S1 for n, k in K1.items()})


def _p(n, q):
    dx, dy = R2.LECH.get((1, n), (0, 0))
    kk = K1[n] * S1
    return ((q[0] - dx) * kk, (q[1] - dy) * kk)


D1C = C.Doi(S1 / 1.11, 752, 860)   # concept → rig dạng 1 (so bóng dáng, dò bố trí)


def ts1_dau(pc):
    """tham số bố trí ban đầu của dạng 1 (chỗ đặt tay ở toạ độ B), rồi đè bằng sil.json nếu đã dò."""
    import tm01_sil as SL
    Q = {k: (D1(*v) if isinstance(v, tuple) else (D1.nhieu(v) if isinstance(v, list) else v)) for k, v in Q1.items()}
    ts = {"than_x": Q["day"][0], "than_y": Q["day"][1], "than_g": 0.0, "than_sx": 1.0, "than_sy": 1.0,
          "duoi_x": Q["duoi_goc"][0], "duoi_y": Q["duoi_goc"][1], "duoi_g": Q1["goc_duoi"], "duoi_sx": 1.0, "duoi_sy": 1.0,
          "mieng_x": Q["mieng"][0], "mieng_y": Q["mieng"][1], "mieng_s": 1.0}
    imt = pc["tay"]
    Lt = float(np.hypot(*(np.array(_p("tay", P1["tay_nam"])) - np.array(_p("tay", P1["tay_vai"])))))
    for s in ("g", "x"):
        g = Q["goc_tay_" + s]
        u = np.array([math.cos(math.radians(g)), math.sin(math.radians(g))])
        vai = Q["nam_" + s] - u * (0.86 * Lt)
        ts.update({f"tay_{s}_x": vai[0], f"tay_{s}_y": vai[1], f"tay_{s}_g": g, f"tay_{s}_k": 1.0, f"tay_{s}_t": 1.0,
                   f"bc_{s}_x": Q["bc_" + s][0], f"bc_{s}_y": Q["bc_" + s][1], f"bc_{s}_s": 1.0})
    for n in ("dai_a", "dai_b"):
        ts.update({n + "_g": Q1["goc_" + n], n + "_s": 1.0})
    ts.update(SL.doc(d_("sil.json")))
    return ts


def bo_tri1(pc, ts):
    o = {"bo": []}
    imb = pc["than"]
    o["than"] = Dat(ts["than_x"], ts["than_y"], goc=ts["than_g"], ti=(ts["than_sx"], ts["than_sy"]), neo=_p("than", Q1["day"]),
                    neo_px=True)
    T = o["than"]
    for key in ("day", "dinh", "tren", "nut", "mat_gan", "mat_xa"):
        o[key] = T.mot(_p("than", Q1[key]), *imb.size)
    o["than_pt"] = T.mot(_p("than", Q1["than"]), *imb.size)
    o["mao"] = T.ra([_p("than", q) for q in Q1["mao"]], *imb.size)
    o["mieng"] = Dat(ts["mieng_x"], ts["mieng_y"], goc=ts["than_g"], ti=(ts["mieng_s"] * ts["than_sx"], ts["mieng_s"] * ts["than_sy"]),
                     neo=(0.5, 0.5))
    imt = pc["tay"]
    p0, p1 = _p("tay", P1["tay_vai"]), _p("tay", P1["tay_nam"])
    ga = math.degrees(math.atan2(-(p1[1] - p0[1]), p1[0] - p0[0]))
    for s in ("g", "x"):
        k, th = ts[f"tay_{s}_k"], ts[f"tay_{s}_t"]
        o["tay_" + s] = Dat(ts[f"tay_{s}_x"], ts[f"tay_{s}_y"], goc=ts[f"tay_{s}_g"] - ga, ti=(k, k * th), neo=p0, neo_px=True)
        o["bc_" + s] = Dat(ts[f"bc_{s}_x"], ts[f"bc_{s}_y"], ti=ts[f"bc_{s}_s"], neo=_p("ban_chan", P1["ban_chan_day"]), neo_px=True)
    o["duoi_J"] = np.array([_p("duoi", q) for q in P1["duoi_J"]])
    o["duoi"] = Dat(ts["duoi_x"], ts["duoi_y"], goc=ts["duoi_g"], ti=(ts["duoi_sx"], ts["duoi_sy"]), neo=tuple(o["duoi_J"][0]),
                    neo_px=True, lat=True)
    for n in ("dai_a", "dai_b"):
        imr = pc[n]
        o[n] = Dat(*o["nut"], goc=ts[n + "_g"] - 180.0, ti=ts[n + "_s"], neo=(imr.width - 2, imr.height / 2), neo_px=True)
    for n, img in (("than", "than"), ("tay_g", "tay"), ("tay_x", "tay"), ("bc_g", "ban_chan"), ("bc_x", "ban_chan"), ("duoi", "duoi"),
                   ("dai_a", "dai_a"), ("dai_b", "dai_b")):
        o["bo"].append((pc[img], o[n], None, n))
    return o


def sil1():
    import tm01_khop as KH
    import tm01_sil as SL
    pc = manh1()
    ts = ts1_dau(pc)
    conc = KH.Concept(d_(os.path.join("tai_ve", "L1_duyet.png")), D1C)
    gioi = R2.gioi_sil(ts, ())
    i0, i1 = SL.toi_uu(ts, lambda t: bo_tri1(pc, t)["bo"], conc, gioi, vong=24)
    SL.luu(ts, d_("sil.json"))
    print(f"  IoU bóng dáng (ước nhanh) {i0:.3f} → {i1:.3f}; ghi {d_('sil.json')}")


def dung1():
    pc = manh1()
    sk = khung.Sk("tm01_1")
    for n, im in pc.items():
        sk.anh(n, im)
    o = bo_tri1(pc, ts1_dau(pc))
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("day", "move", *o["day"], dai=30)
    sk.xuong("than", "day", *o["than_pt"], goc=90, dai=60, the_gioi=True)
    sk.xuong("dinh", "than", *o["dinh"], goc=90, dai=40, the_gioi=True)
    mao = sk.chuoi("mao", "dinh", o["mao"])
    mi = o["mieng"]
    sk.xuong("mieng", "dinh", mi.x + 16 * S1, mi.y, goc=-6, dai=24, the_gioi=True)
    im = pc["than"]
    dat_than = o["than"]
    Lb = C.bo_tg_det(luoi.luoi_vung(im, BV1, BT1, ten="than"), im)
    Vb = dat_than.ra(Lb.pts, *im.size)
    Wthan = trongso.chuoi_chieu(Vb, np.array([o["day"], o["than_pt"], o["dinh"], o["tren"]]), ["day", "than", "dinh"])
    Wmao = trongso.chuoi_chieu(Vb, o["mao"], mao, cha="dinh", cha_hoa=1.0)
    poly = [_p("than", q) for q in MAO_VUNG]
    Wv = trongso.vung(Lb, [("M", poly), ("B", [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)])], dai_hoa=14)
    am = np.array([w.get("M", 0.0) for w in Wv])
    Wb = trongso.lam_tron(Lb, trongso.tron((am, Wmao), (1 - am, Wthan)), 2)
    trongso.kiem(Wb, "than")
    tay = {}
    for s in ("g", "x"):
        imt = pc["tay"]
        Ld = luoi.luoi_dai(imt, 2, truc=[_p("tay", P1["tay_vai"]), _p("tay", P1["tay_nam"])], ten="tay_" + s, buoc=10, in_tk=False)
        Jimg, seg = C.khop_theo_ti(Ld, [0, 0.52, 1.0])
        names = sk.chuoi("tay_" + s, "than", o["tay_" + s].ra(Jimg, *imt.size), khong_ti_le=True)
        tay[s] = (o["tay_" + s], names)
    for s in ("g", "x"):
        sk.xuong("bc_" + s, "move", o["bc_" + s].x, o["bc_" + s].y, dai=20)
    Jd, dat_duoi = o["duoi_J"], o["duoi"]
    duoi = sk.chuoi("duoi", "day", dat_duoi.ra(Jd, *pc["duoi"].size), khong_ti_le=True)
    dai = {}
    for n in ("dai_a", "dai_b"):
        imd = pc[n]
        Ld = luoi.luoi_dai(imd, 4, truc=[(imd.width - 2, imd.height / 2), (2, imd.height / 2)], ten=n, buoc=10, in_tk=False)
        dai[n] = (o[n], sk.chuoi(n, "dinh", o[n].ra(Ld.khop(4), *imd.size), khong_ti_le=True))
    sk.xuong("shadow", "root")

    # ---------------- slot (sau → trước)
    sk.slot("tay_x", tay["x"][1][0], "tay")
    sk.slot("duoi", duoi[0], "duoi")
    for n in ("dai_b", "dai_a"):
        sk.slot(n, dai[n][1][0], n)
    sk.slot("bc_x", "bc_x", "ban_chan")
    sk.slot("bc_g", "bc_g", "ban_chan")
    sk.slot("than", "day", "than")
    sk.slot("mieng_hinh", "dinh", "m_het")
    for n in ("nham_gan", "nham_xa", "ep_gan", "ep_xa"):
        sk.slot(n, "dinh", n, an=True)
    sk.slot("tay_g", tay["g"][1][0], "tay")

    # ---------------- lưới gắn
    sk.luoi_gan("than", "than", Lb, Wb, the_gioi=Vb)
    for s, (dat, names) in tay.items():
        R2.vung_chuoi(sk, "tay_" + s, "tay", pc["tay"], dat, names, "than", 0.5, buoc=(BV1, BT1), ten="tay")
    for s in ("g", "x"):
        imf = pc["ban_chan"]
        dat = o["bc_" + s]
        Lf = luoi.luoi_vung(imf, BV1, BT1, ten="bc_" + s)
        w, h = imf.size
        Wf = trongso.vung(Lf, [("bc_" + s, [(0, 0.45 * h), (w, 0.45 * h), (w, h), (0, h)]), ("day", [(0, 0), (w, 0), (w, h), (0, h)])],
                          dai_hoa=0.3 * h)
        sk.luoi_gan("bc_" + s, "ban_chan", Lf, trongso.lam_tron(Lf, Wf, 1), dat=dat, ten="ban_chan")
    imd = pc["duoi"]
    Ldu = luoi.luoi_vung(imd, BV1, BT1, ten="duoi")
    Wd = trongso.lam_tron(Ldu, trongso.chuoi_geo(Ldu, Jd, duoi, cha="day", cha_hoa=0.7), 1)
    trongso.kiem(Wd, "duoi")
    sk.luoi_gan("duoi", "duoi", Ldu, Wd, dat=dat_duoi)
    for n, (dat, names) in dai.items():
        R2.vung_chuoi(sk, n, n, pc[n], dat, names, "dinh", 0.6, buoc=(BV1, BT1))
    # miệng: bốn hình trong một slot, dán lên thân
    for n in ("m_het", "m_tron", "m_mim", "m_nghien"):
        dat = o["mieng"]
        C.dan_len_than(sk, "mieng_hinh", n, Lb, Wb, Vb, dat, buoc=BV1)
    # mí, mắt ép: dò cho phủ kín từng mắt trên ảnh thân
    ho = {}
    for eye, lid, ep in (("mat_gan", "nham_gan", "ep_gan"), ("mat_xa", "nham_xa", "ep_xa")):
        hat = _p("than", Q1[eye])
        mk = mieng.vung_mat(pc["than"], hat, nguong=40, noi=3)
        for nm in (lid, ep):
            kq = mieng.fit_lid(pc["than"], pc[nm], mat=mk, ten=nm, ti=(0.7, 1.8, 0.06), goc=(-20, 20, 4))
            ho[nm] = kq[4]
            C.dan_len_than(sk, nm, nm, Lb, Wb, Vb, mieng.dat_mi(dat_than, pc["than"], kq), buoc=BV1)
    sk.info["mi_ho"] = ho
    for e, m in (("trung", "bong bóng trúng"), ("phun", "bắt đầu phun tia nước (xương mieng)"), ("het_phun", "hết phun"),
                 ("gam", "giơ nắm đấm hét: mây mưa tụ trên đầu đối thủ"), ("het_gam", "hết mưa")):
        sk.su_kien(e, m)
    info = {"mao": mao, "tay": {s: v[1] for s, v in tay.items()}, "duoi": duoi, "dai": {n: v[1] for n, v in dai.items()}}
    return sk, info


def mem1(info):
    def gio(t, i):
        return np.array([-500.0 - 350.0 * math.sin(2 * math.pi * t / 1.0 + 0.8 * i), 260.0 * math.cos(2 * math.pi * t / 0.7 + i)])
    return [LoXo(info["mao"], k=[360, 280, 220], damp=0.5, maxang=12),
            DayMem(info["dai"]["dai_a"], k0=0.24, k1=0.07, zeta=0.45, luc=gio, lim=(16, 26)),
            DayMem(info["dai"]["dai_b"], k0=0.26, k1=0.08, zeta=0.45, luc=lambda t, i: gio(t + 0.31, i + 2), lim=(16, 26)),
            LoXo(info["duoi"], k=[520, 420, 340, 280], damp=0.55, maxang=12)]


def clips1(sk, info):
    T = 2.0
    tg, tx, duoi = info["tay"]["g"], info["tay"]["x"], info["duoi"]
    MAT = ("nham_gan", "nham_xa")
    EP = ("ep_gan", "ep_xa")

    def nen(P, tt, a=1.0):
        """dao động nền idle, trừ giá trị ở giây 0 (khung 0 idle = dáng concept)."""
        Q1, Q0 = Pose(), Pose()
        nen_tho(Q1, tt, a)
        nen_tho(Q0, 0.0, a)
        for bn, v in Q1.t.items():
            v0 = Q0.t.get(bn, [0, 0, 0, 1, 1])
            P.move(bn, v[0] - v0[0], v[1] - v0[1])
            P.rot(bn, v[2] - v0[2])
            P.scale(bn, v[3] / v0[3], v[4] / v0[4])

    def nen_tho(P, tt, a=1.0):
        s = song(tt, T)
        P.scale("day", 1 + 0.025 * s * a, 1 - 0.03 * s * a)
        P.move("day", 0, 2.5 * song(tt, T / 2, -0.5) * a)
        P.rot("than", 2.0 * song(tt, T, -0.6) * a)
        P.rot("dinh", -1.5 * song(tt, T, -1.2) * a)
        P.rot(tg[0], 5 * song(tt, T / 2, -1.1) * a)
        P.rot(tg[1], 4 * song(tt, T / 2, -1.6) * a)
        P.rot(tx[0], -4 * song(tt, T / 2, -1.3) * a)
        hoat.chuoi_song(P, duoi, tt, T, np.array([4, 6, 8, 10]) * a, tre=0.1, ngon_dan=False)

    def mat(P, t, khoang, ep=False):
        for n in (EP if ep else MAT):
            an_hien(P, n, t, khoang)

    def idle(t, P):
        nen(P, t)
        mat(P, t, [(1.30, 1.42)])
        huff = bao(t, 1.5, 1.82, 0.05, 0.12)
        P.scale("day", 1 + 0.04 * huff, 1 - 0.05 * huff)
        P.att["mieng_hinh"] = "m_mim" if 1.5 <= t < 1.8 else "m_het"

    def appear(t, P, D=1.2):
        y = cv(t, [(0, 230), (0.34, 0, "in"), (D, 0)])
        P.move("move", 0, y)
        sx = cv(t, [(0, 0.72), (0.33, 0.8), (0.42, 1.36, "out"), (0.6, 0.9, "io"), (0.78, 1.05, "io"), (0.92, 1.0, "io"), (D, 1.0)])
        sy = cv(t, [(0, 1.32), (0.33, 1.22), (0.42, 0.68, "out"), (0.6, 1.12, "io"), (0.78, 0.97, "io"), (0.92, 1.0, "io"), (D, 1.0)])
        P.scale("day", sx, sy)
        for b in ("bc_g", "bc_x"):
            P.move(b, 0, y)
        a = cv(t, [(0, 0), (0.1, 1, "io")])
        for sl in sk.slots:
            if sl["alpha"] > 0:
                P.alpha[sl["name"]] = a
        nen(P, lui(t, D), ease((t - 0.7) / 0.4))
        P.att["mieng_hinh"] = "m_tron" if 0.36 <= t < 0.62 else "m_het"
        mat(P, t, [(0.38, 0.55)], ep=True)

    def attack(t, P, D=0.9, H=0.45):
        nen(P, lui(t, D), 1 - 0.85 * bao(t, 0.05, 0.8, 0.12, 0.2))
        pu = cv(t, [(0, 0), (0.28, 1, "io"), (0.36, 1.05), (H, 0, "in"), (D, 0)])
        sp = cv(t, [(0, 0), (0.38, 0), (H, 1, "out"), (0.64, 0.85), (D, 0, "io")])
        P.scale("day", 1 + 0.08 * pu - 0.06 * sp, 1 - 0.1 * pu + 0.08 * sp)
        P.rot("than", 8 * pu - 10 * sp)
        P.rot("dinh", 3 * pu - 5 * sp)
        P.move("move", -5 * pu + 7 * sp, 0)
        P.rot(tg[0], 14 * pu - 22 * sp)
        P.rot(tx[0], -10 * pu + 14 * sp)
        P.att["mieng_hinh"] = "m_mim" if 0.12 <= t < 0.4 else ("m_tron" if t < 0.68 else "m_het")

    def cast(t, P, D=1.2, H=0.5, E=1.0):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.05, 1.1, 0.12, 0.2))
        re = cv(t, [(0, 0), (0.4, 1, "io"), (0.45, 1.04), (H, 0, "in"), (D, 0)])
        lu = cv(t, [(0, 0), (0.44, 0), (H, 1, "out"), (E, 1), (D, 0, "io")])
        r = rung(t, H + 0.03, E)
        P.scale("day", 1 - 0.08 * re + 0.1 * lu + 0.012 * r, 1 + 0.12 * re - 0.1 * lu - 0.012 * r)
        P.rot("than", 10 * re - 12 * lu + 1.0 * r)
        P.rot("dinh", 4 * re - 5 * lu)
        P.move("move", -4 * re + 6 * lu, 0)
        P.rot(tg[0], 20 * re - 30 * lu)
        P.rot(tx[0], -12 * re + 18 * lu)
        P.att["mieng_hinh"] = "m_mim" if 0.1 <= t < 0.47 else ("m_tron" if t < E + 0.05 else "m_het")

    def skill(t, P, D=1.8, G=0.8, E=1.4):
        nen(P, lui(t, D), 1 - 0.9 * bao(t, 0.05, 1.7, 0.15, 0.3))
        cr = cv(t, [(0, 0), (0.45, 1, "io"), (G - 0.08, 1.05), (G, 0, "out"), (D, 0)])
        up = cv(t, [(0, 0), (0.6, 0), (G, 1, "out"), (E, 1), (D, 0, "io")])
        r = rung(t, 0.2, G - 0.06) + rung(t, G + 0.03, E)
        P.scale("day", 1 + 0.1 * cr - 0.08 * up + 0.015 * r, 1 - 0.14 * cr + 0.13 * up - 0.015 * r)
        P.rot("dinh", 6 * up + 1.2 * r)
        P.rot(tg[0], -8 * cr - 12 * up)
        P.rot(tg[1], 22 * up)
        P.rot(tx[0], 10 * cr - 40 * up)
        P.att["mieng_hinh"] = "m_nghien" if 0.15 <= t < G - 0.02 else ("m_het" if t < E + 0.1 else "m_het")

    def hit(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.1, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        P.scale("day", 1 - 0.14 * hd, 1 + 0.1 * hd)
        P.rot("than", 12 * hd)
        P.rot("dinh", 6 * hd)
        P.move("move", -8 * hd, 0)
        P.rot(tg[0], 18 * hd)
        P.rot(tx[0], -14 * hd)
        mat(P, t, [(0.03, 0.36)], ep=True)
        P.att["mieng_hinh"] = "m_nghien" if 0.03 <= t < 0.36 else "m_het"
        n = len(duoi)
        for i, b in enumerate(duoi):
            P.rot(b, (5 + 2 * i) * cv(t, [(0, 0), (0.07 + 0.03 * (n - 1 - i), 1, "out"), (0.35 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))

    def die(t, P, D=1.6):
        j = cv(t, [(0, 0), (0.07, 1, "out"), (0.3, 0.3, "io"), (D, 0.3)])
        sag = cv(t, [(0, 0), (0.25, 0), (0.65, 1, "io"), (D, 1)])
        sway = math.sin(2 * math.pi * (t - 0.65) / 0.5) * bao(t, 0.65, 1.0, 0.08, 0.12)
        fl = cv(t, [(0, 0), (0.98, 0), (1.3, 1, "in"), (D, 1)])
        P.scale("day", (1 - 0.1 * j) * (1 + 0.55 * fl), (1 + 0.08 * j - 0.08 * sag) * (1 - 0.82 * fl))
        P.rot("than", 10 * j - 6 * sag + 3 * sway)
        P.rot("dinh", -10 * sag)
        P.rot(tg[0], 10 * j - 40 * sag)
        P.rot(tx[0], 30 * sag)
        a = cv(t, [(0, 1), (1.15, 1), (1.52, 0, "io"), (D, 0)])
        for sl in sk.slots:
            if sl["alpha"] > 0:
                P.alpha[sl["name"]] = a
        for n in EP:
            P.alpha[n] = a if t >= 0.04 else 0.0
        P.att["mieng_hinh"] = "m_tron" if t < 0.3 else "m_mim"

    m = lambda: mem1(info)  # noqa: E731
    return [Clip("appear", 1.2, appear, mem=m()),
            Clip("idle", T, idle, loop=True, mem=m()),
            Clip("attack", 0.9, attack, ev=[(0.45, "trung", "")], mem=m()),
            Clip("cast", 1.2, cast, ev=[(0.5, "phun", ""), (1.0, "het_phun", "")], mem=m()),
            Clip("skill", 1.8, skill, ev=[(0.8, "gam", ""), (1.5, "het_gam", "")], trung=0.95, mem=m()),
            Clip("hit", 0.6, hit, mem=m()),
            Clip("die", 1.6, die, mem=m())]


def dung_va_clip():
    sk, info = dung1()
    return sk, info, clips1(sk, info)


def uon_thu1(sk, info, ra):
    P = Pose()
    P.scale("day", 1.25, 0.75)
    P.rot("dinh", 12)
    for b in info["mao"]:
        P.rot(b, 16)
    for b in info["duoi"]:
        P.rot(b, 20)
    P.rot(info["tay"]["g"][1], 40)
    for n in info["dai"].values():
        for b in n:
            P.rot(b, -15)
    P.alpha["ep_gan"] = P.alpha["ep_xa"] = 1.0
    P.att["mieng_hinh"] = "m_tron"
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110)).convert("RGB").save(ra)


def main(cmd):
    if cmd == "sil":
        sil1()
        return
    if cmd == "ghep":
        sk, info = dung1()
        ve = soi.Ve(sk)
        P = Pose()
        B = ve.bao(P)
        img = ve.ve(P, (B[0] - 20, B[1] - 20, B[2] + 20, B[3] + 20), 1.5, bg=(150, 150, 150), ss=2, xuong=True)
        img.convert("RGB").save(d_("ghep.png"))
        print(d_("ghep.png"), "cao", B[3] - B[1], "rộng", B[2] - B[0], "mí", sk.info["mi_ho"])
        return
    if cmd != "rig":
        raise SystemExit("lệnh: ghep | rig")
    t0 = time.time()
    sk2, info2, cl2, fr2, _ = R2.rig2(xuat_ra=False)
    sk1, info1 = dung1()
    cl1 = clips1(sk1, info1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    print(f"dạng 1: nướng {len(cl1)} clip ({time.time() - t0:.1f} s)")
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0]), soi.chieu_cao(ve2, fr2["idle"][0])
    M = tienhoa.gop(sk1, sk2)
    idleB0 = fr2["idle"][0]
    endB = tienhoa.doi_ten_pose(idleB0)

    def gong(t, P):                     # Tí Tách gồng: nén, rung, mào bật, nghiến răng
        sq = cv(t, [(0, 0), (0.3, -0.06), (0.5, 0.1, "out"), (1.0, 0.08), (1.3, 0.0)])
        P.scale("day", 1 + 0.6 * sq, 1 - sq)
        P.rot("dinh", 2.0 * rung(t, 0.45, 1.3))
        P.rot(info1["tay"]["g"][0], -14 * ease((t - 0.2) / 0.4))
        P.rot(info1["tay"]["x"][0], 14 * ease((t - 0.2) / 0.4))
        P.att["mieng_hinh"] = "m_nghien" if t > 0.25 else "m_het"

    def gam(t, P, fl):                  # Sóng Thần hiện ra trong dáng đứng (khung 0 idle) rồi gầm
        for b, v in endB.t.items():
            g = P._g(b)
            for q in range(5):
                g[q] = g[q] + v[q] if q < 3 else g[q] * v[q]
        P.rot("n_co", 10 * fl)
        P.rot("n_dau", 5 * fl)
        P.rot("n_ham", -26 * fl)
        P.rot("n_" + info2["tay"]["x"][0], 50 * fl)
        P.rot("n_" + info2["tay"]["x"][1], 30 * fl)

    memM = mem1(info1) + tienhoa.doi_ten_mem(R2.mem2(info2))
    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, idleB0, tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    clM = cl1 + [ev]
    frM = dict(fr1)
    frM["evolve"] = hoat.nuong(M, ev)
    _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, idleB0, hA / hB)
    ra = d_("rig")
    os.makedirs(ra, exist_ok=True)
    R2.so_concept(sk1, fr1["idle"], d_(os.path.join("tai_ve", "L1_duyet.png")), D1C,
                  os.path.join(ra, "so_concept.png"))
    tong = xuat.xuat_het(M, clM, ra, "tm01_1", "Tí Tách (tm01 dạng 1, gộp tiến hóa)", frames=frM, dang=1, so_dang=2,
                         dung_yen=("attack", "cast", "skill"), ma_goc=3211,
                         noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                         can=[("can_mieng_cast", "cast", 0.7, "mieng", 40), ("can_mat_hit", "hit", 0.1, "dinh", 55),
                              ("can_mao_skill", "skill", 0.85, "mao1", 55), ("can_tay_attack", "attack", 0.45, "tay_g1", 50),
                              ("can_doi_dang", "evolve", 1.3, "than", 120)])
    uon_thu1(sk1, info1, os.path.join(ra, "uon_thu.png"))
    print(f"xong dạng 1 {time.time() - t0:.1f} s; mí còn hở {sk1.info['mi_ho']}")
