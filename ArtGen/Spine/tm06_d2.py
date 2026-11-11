# -*- coding: utf-8 -*-
"""tm06 dạng 2 "Giông Bão": kỳ giông núi khổng lồ bò bốn chân cõng bình đồng (rig, clip, xuất). Gọi từ tm06.py (rig 2 / rig 1).

Xương: root → move → than (giữa thân) → hong (nửa sau, chĩa ra sau) / nguc (nửa trước) → co → dau → ham; đuôi 6 đốt con của hong;
bốn chân 3 đốt (đùi, cẳng, bàn: IK giữ cổ chân, bàn phẳng); lá mang 6 chuỗi 3 đốt con của dau; binh (bình đồng, cứng) con của
than, nap (nắp) và mieng (miệng bình: chỗ nhả tia của chiêu bắn) con của binh.
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

from quai import hoat, khung, luoi, mieng, soi, trongso, xuat  # noqa: E402
from quai.hoat import Clip, an_hien, chuoi_song, cv, ease, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

import tm06 as T  # noqa: E402

G2 = 0.45
BO_CAO = ()
GC2 = {"dau": ("bo", 470, 280, (90, 88, 120)), "ham": ("ham", 420, 110, (232, 120, 46)), "mieng": ("mieng", 260, 150, (184, 64, 90)),
       "mi_n": ("mi", 130, 95, (90, 88, 120)), "mi_x": ("mi", 60, 80, (90, 88, 120)), "mang1": ("luoi", 380, 100, (200, 56, 58)),
       "mang2": ("luoi", 320, 90, (200, 56, 58)), "mang3": ("luoi", 260, 80, (200, 56, 58)),
       "than": ("tron", 1050, 330, (90, 88, 120)), "duoi": ("dai", 620, 400, (90, 88, 120)), "binh": ("tron", 520, 420, (78, 158, 138)),
       "nap": ("giot", 300, 260, (78, 158, 138)), "chan1": ("chan", 300, 300, (90, 88, 120)), "chan2": ("chan", 240, 220, (70, 68, 96)),
       "chan3": ("chan", 300, 290, (90, 88, 120)), "chan4": ("chan", 320, 300, (90, 88, 120))}
# điểm đọc trên concept dạng 2 (px concept; inbox/tm06_2/rig/z_*.png): đầu gốc chuỗi, khớp thân, mắt
A2 = dict(than_trai=(310, 600), than_phai=(1095, 560), co=(1105, 525), goc_duoi=(455, 565), binh=(720, 560), mieng_binh=(775, 318),
          hong1=(400, 600), hong2=(630, 650), hong3=(885, 600), hong4=(1200, 620), mat_n=(1243, 526), mat_x=(1385, 532))
LEGS = (("chan1", "hong1", "hong"), ("chan2", "hong2", "hong"), ("chan3", "hong3", "nguc"), ("chan4", "hong4", "nguc"))
MO = (("than", "trai", 0.06, 0.075), ("dau", "trai", 0.06, 0.03), ("chan1", "tren", 0.12, 0.06), ("chan3", "tren", 0.12, 0.06),
      ("chan4", "tren", 0.12, 0.09), ("chan2", "tren", 0.12, 0.05), ("duoi", "phai", 0.1, 0.05))
GILLS = ("mang_x1", "mang_x2", "mang_x3", "mang_n1", "mang_n2", "mang_n3")


def dung2_manh(mat_do=1.0, ti_anh=1.0):
    """bản cũ dựng toàn bằng mảnh GPT (điều phối chê: đầu nhỏ, cổ như rùa thò đầu); giữ để so."""
    D = T.Dung(2, G2, GC2, ti_anh=ti_anh)
    D.bv, D.bt = D.bv * mat_do, D.bt * mat_do
    pc = D.pc
    # chỗ nối chui dưới mảnh khác: mờ dần mép ống (thân trái dưới đuôi... đầu trái trên vòng cổ, đỉnh chân trên thân)
    for n, ben, fr, bo in MO:
        if n in pc:
            pc[n] = T.mo_mep(pc[n], ben, fr, bo=bo)
    sk = khung.Sk(f"{T.CODE}_2")
    for n, im in pc.items():
        sk.anh(n, im)
    W = D.w
    sk.xuong("root")
    sk.xuong("move", "root")
    # thân: trục ngang qua giữa ảnh thân, trái (hông) → phải (cổ); 5 khớp
    dt = D.dat("than")
    im = pc["than"]
    w, h = im.size
    m = T.mat_na(im)
    xs_ = np.linspace(0.02, 0.98, 5) * w
    J_img = []
    for x in xs_:
        col = np.nonzero(m[:, int(min(w - 1, x))])[0]
        J_img.append((x, 0.5 * (col.min() + col.max()) if len(col) else 0.5 * h))
    J_img = np.array(J_img)
    Jt = dt.ra(J_img, w, h)
    ang = lambda a, b: math.degrees(math.atan2(*(b - a)[::-1]))  # noqa: E731
    sk.xuong("than", "move", *Jt[2], goc=ang(Jt[2], Jt[3]), dai=float(np.hypot(*(Jt[3] - Jt[2]))), the_gioi=True)
    sk.xuong("hong", "than", *Jt[1], goc=ang(Jt[1], Jt[0]), dai=float(np.hypot(*(Jt[0] - Jt[1]))), the_gioi=True)
    sk.xuong("nguc", "than", *Jt[3], goc=ang(Jt[3], Jt[4]), dai=float(np.hypot(*(Jt[4] - Jt[3]))), the_gioi=True)
    neck = W(*A2["co"])
    sk.xuong("co", "nguc", *Jt[4], goc=ang(Jt[4], neck), dai=float(np.hypot(*(neck - Jt[4]))), the_gioi=True)
    # đầu, hàm
    dd = D.dat("dau")
    dau = pc["dau"]
    hw, hh = dau.size
    snout_up = dd.mot(T.dau_mut(dau, "phai"), hw, hh)
    sk.xuong("dau", "co", *neck, goc=ang(neck, snout_up), dai=float(np.hypot(*(snout_up - neck))), the_gioi=True)
    dj = D.dat("ham")
    ham = pc["ham"]
    hinge = dj.mot(T.dau_mut(ham, "trai") + np.array([0.05 * ham.width, -0.1 * ham.height]), *ham.size)
    snout = dj.mot(T.dau_mut(ham, "phai"), *ham.size)
    gj = ang(hinge, snout)
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    # lá mang
    gills = {}
    for g in GILLS:
        if g not in D.pl:
            continue
        gi = D.img(g)
        Lg = luoi.luoi_dai(gi, 3, ten=g, buoc=D.bv)
        dg = D.dat(g)
        Jg = dg.ra(Lg.khop(3), *gi.size)
        gills[g] = (Lg, dg, sk.chuoi(g, "dau", Jg))
    # đuôi
    im = pc["duoi"]
    dq = D.dat("duoi")
    g0 = T.nguoc(dq, W(*A2["goc_duoi"]), *im.size)[0]
    Jq_img = T.geo_truc(im, g0, 6)
    Jq = dq.ra(Jq_img, *im.size)
    duoi = sk.chuoi("duoi", "hong", Jq)
    # chân
    legs = {}
    for c, anc, par in LEGS:
        im = pc[c]
        dc = D.dat(c)
        g0 = T.nguoc(dc, W(*A2[anc]), *im.size)[0]
        g0[1] = min(g0[1], 0.12 * im.height)
        Ji = T.geo_truc(im, g0, 3)
        Jc = dc.ra(Ji, *im.size)
        legs[c] = (im, dc, Jc, sk.chuoi(c, par, Jc), par)
    # bình, nắp, miệng bình
    db = D.dat("binh")
    pb = W(*A2["binh"])
    sk.xuong("binh", "than", *pb, the_gioi=True, dai=60)
    dn = D.dat("nap")
    sk.xuong("nap", "binh", dn.x, dn.y, the_gioi=True, dai=30)
    pm = W(*A2["mieng_binh"])
    sk.xuong("mieng", "binh", *pm, goc=ang(pb, pm), dai=40, the_gioi=True)   # trục x chĩa theo cổ bình
    # ---- slot (sau → trước)
    sk.slot("chan2", legs["chan2"][3][0], "chan2")
    sk.slot("chan1", legs["chan1"][3][0], "chan1")       # chân gần sau thân: mép bụng che đỉnh chân (không lộ "miệng ống")
    sk.slot("chan3", legs["chan3"][3][0], "chan3")
    sk.slot("duoi", duoi[0], "duoi")
    for g in ("mang_x1", "mang_x2", "mang_x3"):
        if g in gills:
            sk.slot(g, gills[g][2][0], D.pl[g].get("img", g))
    sk.slot("than", "than", "than")
    sk.slot("chan4", legs["chan4"][3][0], "chan4")
    sk.slot("binh", "binh", "binh")
    sk.slot("nap", "nap", "nap")
    for g in ("mang_n1", "mang_n2", "mang_n3"):
        if g in gills:
            sk.slot(g, gills[g][2][0], D.pl[g].get("img", g))
    sk.slot("mieng_long", "ham", "mieng")
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    eyes = T.tim_mat(dau)
    lids = ("mi_x", "mi_n") if len(eyes) > 1 else ("mi_n",)     # ảnh đầu không vẽ mắt xa thì không cần mí xa
    for lid in lids:
        sk.slot(lid, "dau", lid, an=True)
    # ---- lưới, trọng số
    Lt = luoi.luoi_vung(pc["than"], 1.07 * D.bv, 1.15 * D.bt, ten="than")   # mảng lớn: thưa hơn chút cho vừa dung lượng
    Wt = trongso.chuoi_chieu(dt.ra(Lt.pts, w, h), np.array([Jt[0], Jt[1], Jt[3], Jt[4]]), ["hong", "than", "nguc"], cha=None)
    # cổ: phần đầu phải của thân (vòng cổ) hoà vào xương co
    Qt = dt.ra(Lt.pts, w, h)
    Wc = trongso.theo_truc(Qt, Jt[3], Jt[4] + (Jt[4] - Jt[3]) * 0.15, "nguc", "co", u0=0.7, u1=1.05)
    Wt = [_tron2(a, b, float(np.clip((np.dot(q - Jt[3], Jt[4] - Jt[3]) / np.dot(Jt[4] - Jt[3], Jt[4] - Jt[3]) - 0.55) / 0.3, 0, 1)))
          for a, b, q in zip(Wt, Wc, Qt)]
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=dt)
    Lh = luoi.luoi_vung(dau, D.bv, D.bt, ten="dau")
    Qh = dd.ra(Lh.pts, hw, hh)
    Wh = trongso.theo_truc(Qh, neck, snout_up, "co", "dau", u0=-0.05, u1=0.18)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dd)
    Lj = luoi.luoi_vung(ham, D.bv, D.bt, ten="ham")
    Wj = mieng.ham_hai_xuong(dj.ra(Lj.pts, *ham.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dj)
    mieng.long_mieng(sk, "mieng_long", "mieng", "dau", "ham", hinge, snout, duoi=-0.14, tren=(0.04, 0.07, 0.1, 0.12, 0.12),
                     q_tren=(0.0, 0.0, 0.0, 0.0, 0.0), doc=(0.05, 0.96))
    for g, (Lg, dg, names) in gills.items():
        Wg = trongso.chuoi(Lg.s, Lg.truc[1][-1] / 3, names, cha="dau", cha_hoa=0.5)
        sk.luoi_gan(g, D.pl[g].get("img", g), Lg, Wg, dat=dg)
    Lq = luoi.luoi_vung(pc["duoi"], 1.07 * D.bv, 1.15 * D.bt, ten="duoi")
    Wq = trongso.chuoi_geo(Lq, Jq_img, duoi, cha="hong", cha_hoa=0.7)
    Wq = trongso.lam_tron(Lq, Wq, 1)
    trongso.kiem(Wq, "duoi")
    sk.luoi_gan("duoi", "duoi", Lq, Wq, dat=dq)
    for c, (im, dc, Jc, names, par) in legs.items():
        Lc = luoi.luoi_vung(im, D.bv, D.bt, ten=c)
        Wl = trongso.chuoi_chieu(dc.ra(Lc.pts, *im.size), Jc, names, cha=par, cha_hoa=0.8)
        Wl = trongso.lam_tron(Lc, Wl, 1)
        sk.luoi_gan(c, c, Lc, Wl, dat=dc)
    sk.manh("binh", "binh", db)
    sk.manh("nap", "nap", dn)
    for lid, key in (("mi_n", "mat_n"), ("mi_x", "mat_x")):
        if lid not in lids:
            continue
        s0 = T.nguoc(dd, W(*A2[key]), hw, hh)[0]
        if eyes:
            e = min(eyes, key=lambda q: (q[0] - s0[0]) ** 2 + (q[1] - s0[1]) ** 2)
            if (e[0] - s0[0]) ** 2 + (e[1] - s0[1]) ** 2 < (0.12 * hw) ** 2:
                s0 = np.array(e[:2])
        kq = mieng.fit_lid(dau, pc[lid], mat=T.mat_mat(dau, s0), ten=f"dạng 2 {lid}")
        sk.manh(lid, lid, mieng.dat_mi(dd, dau, kq))
    for e, mo in (("trung", "đuôi đập đất (VFX cột nước trồi dưới chân đối thủ)"), ("phun", "bình đồng bắt đầu nhả luồng nước (VFX bám "
                  "xương mieng ở miệng bình)"), ("het_phun", "hết nhả"), ("bat_nap", "nắp bình bật lên"),
                  ("gam", "ngửa cổ gầm, bình phun cột nước lên trời (VFX mây giông, mưa xối, vòi rồng quanh đối thủ)"),
                  ("het_gam", "hết chiêu cuối"), ("nen", "hai chân trước nện đất")):
        sk.su_kien(e, mo)
    foot = {c: (np.array(v[2][2]), np.array(v[2][3])) for c, v in legs.items()}
    info = dict(D=D, duoi=duoi, gills={g: v[2] for g, v in gills.items()}, legs={c: v[3] for c, v in legs.items()}, foot=foot, k=2,
                Jt=Jt)
    print(f"  dạng 2: {sk.tom_tat()}")
    return sk, info



# ---------------------------------------------------------------- cách lai (điều phối 2026-11-11): thân, đầu trên, vòng cổ, vây, đuôi,
# chân, bình, nắp cắt thẳng từ concept (tm06_lai.py); mảnh GPT chỉ cho hàm dưới + lòng miệng, mí, lá mang
# điểm concept dạng 2 (px): trục thân (hông → cổ), gáy (khớp đầu), tâm đầu, gốc đuôi, đáy bình, miệng bình, bản lề nắp
LAI = dict(truc=[(310, 595), (470, 600), (690, 610), (900, 600), (1040, 560)], gay=(1105, 528), tam_dau=(1250, 520),
           goc_duoi=(445, 565), binh=(720, 560), mieng_binh=(775, 318), ban_le_nap=(668, 318))
LAI_LEGS = (("chan1", "hong"), ("chan2", "hong"), ("chan3", "nguc"), ("chan4", "nguc"))


def _anh_lop(path, T_):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    return im.resize((max(2, round(im.width * T_)), max(2, round(im.height * T_))), Image.LANCZOS)


def dung2(mat_do=1.0, ti_anh=1.0):
    import json
    from PIL import Image
    from quai import anh
    D = T.Dung(2, G2, GC2, ti_anh=ti_anh)
    D.bv, D.bt = D.bv * mat_do, D.bt * mat_do
    meta = json.load(open(T.inbox(2, "lai", "meta.json"), encoding="utf-8"))
    D.xg, D.yg = meta["ground"]
    Tl = G2 * ti_anh                       # pixel atlas / pixel concept cho lớp cắt từ concept
    W = D.w
    sk = khung.Sk(f"{T.CODE}_2")
    lop, dat = {}, {}
    for n, (x0, y0, x1, y1) in meta["layers"].items():
        im = anh.loang_mau(_anh_lop(T.inbox(2, "lai", n + ".png"), Tl))
        lop[n] = im
        c = W((x0 + x1) / 2, (y0 + y1) / 2)
        dat[n] = Dat(c[0], c[1], ti=(G2 * (x1 - x0) / im.width, G2 * (y1 - y0) / im.height))
        sk.anh(n, im)
    pc = D.pc
    pc["ham"] = T.mo_mep(pc["ham"], "trai", 0.12, bo=0.04)     # núm bản lề hàm GPT: chìm vào má, không lòi cục tròn
    for n in ("ham", "mieng", "mi_n", "mi_x", "mang1", "mang2", "mang3"):
        sk.anh(n, pc[n])
    sk.xuong("root")
    sk.xuong("move", "root")
    ang = lambda a, b: math.degrees(math.atan2(*(b - a)[::-1]))  # noqa: E731
    Jt = np.array([W(*p) for p in LAI["truc"]])
    gay, tam = W(*LAI["gay"]), W(*LAI["tam_dau"])
    sk.xuong("than", "move", *Jt[2], goc=ang(Jt[2], Jt[3]), dai=float(np.hypot(*(Jt[3] - Jt[2]))), the_gioi=True)
    sk.xuong("hong", "than", *Jt[1], goc=ang(Jt[1], Jt[0]), dai=float(np.hypot(*(Jt[0] - Jt[1]))), the_gioi=True)
    sk.xuong("nguc", "than", *Jt[3], goc=ang(Jt[3], Jt[4]), dai=float(np.hypot(*(Jt[4] - Jt[3]))), the_gioi=True)
    sk.xuong("co", "nguc", *Jt[4], goc=ang(Jt[4], gay), dai=float(np.hypot(*(gay - Jt[4]))), the_gioi=True)
    sk.xuong("dau", "co", *gay, goc=ang(gay, tam), dai=float(np.hypot(*(tam - gay))), the_gioi=True)
    # hàm dưới GPT (đã đặt khớp concept), bản lề và mõm theo đầu mút ảnh hàm
    dj = D.dat("ham")
    ham = pc["ham"]
    hinge = dj.mot(T.dau_mut(ham, "trai") + np.array([0.05 * ham.width, -0.1 * ham.height]), *ham.size)
    snout = dj.mot(T.dau_mut(ham, "phai"), *ham.size)
    sk.xuong("ham", "dau", *hinge, goc=ang(hinge, snout), dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    # lá mang GPT (đặt theo hai đầu khớp đọc trên concept)
    gills = {}
    for g in GILLS:
        if g not in D.pl:
            continue
        gi = D.img(g)
        Lg = luoi.luoi_dai(gi, 3, ten=g, buoc=D.bv)
        dg = D.dat(g)
        gills[g] = (Lg, dg, sk.chuoi(g, "dau", dg.ra(Lg.khop(3), *gi.size)))
    # lớp thân liền: nhãn vùng (đuôi, thân, vòng cổ, đầu) để chia trọng số
    im_t = lop["than"]
    dt = dat["than"]
    nh = np.asarray(Image.open(T.inbox(2, "lai", "nhan_than.png")).resize(im_t.size, Image.NEAREST)).astype(int) - 1
    names = meta["names"]
    m_duoi, m_dau = nh == names.index("duoi"), nh == names.index("dau")
    # đuôi: 6 đốt theo khoảng cách đi trong vùng đuôi từ gốc
    a = np.zeros(nh.shape + (4,), np.uint8)
    a[..., 3] = (m_duoi * 255).astype(np.uint8)
    im_duoi = Image.fromarray(a, "RGBA")
    g0 = T.nguoc(dt, W(*LAI["goc_duoi"]), *im_t.size)[0]
    Jq_img = T.geo_truc(im_duoi, g0, 6)
    Jq = dt.ra(Jq_img, *im_t.size)
    duoi = sk.chuoi("duoi", "hong", Jq)
    # chân (cắt từ concept): 3 đốt từ đỉnh chân
    legs = {}
    for c, par in LAI_LEGS:
        im = lop[c]
        dc = dat[c]
        m = T.mat_na(im)
        ys, xs = np.nonzero(m)
        top = ys.min()
        g0 = np.array([xs[ys < top + 0.12 * im.height].mean(), top + 2])
        Ji = T.geo_truc(im, g0, 3)
        Jc = dc.ra(Ji, *im.size)
        legs[c] = (im, dc, Jc, sk.chuoi(c, par, Jc), par)
    # bình, nắp (bản lề phía sau), miệng bình (chỗ nhả tia của chiêu bắn)
    pb, pm, pn = W(*LAI["binh"]), W(*LAI["mieng_binh"]), W(*LAI["ban_le_nap"])
    sk.xuong("binh", "than", *pb, the_gioi=True, dai=60)
    sk.xuong("nap", "binh", *pn, the_gioi=True, dai=30)
    sk.xuong("mieng", "binh", *pm, goc=ang(pb, pm), dai=40, the_gioi=True)
    # ---- slot (sau → trước)
    sk.slot("chan2", legs["chan2"][3][0], "chan2")
    for g in ("mang_x1", "mang_x2", "mang_x3"):
        if g in gills:
            sk.slot(g, gills[g][2][0], D.pl[g].get("img", g))
    sk.slot("mieng_long", "ham", "mieng")          # khoang miệng sau lớp thân: chỉ lộ qua chỗ hàm (đã khoét khỏi lớp thân)
    sk.slot("than", "than", "than")
    for c in ("chan1", "chan3", "chan4"):
        sk.slot(c, legs[c][3][0], c)
    sk.slot("binh", "binh", "binh")
    sk.slot("nap", "nap", "nap")
    for g in ("mang_n1", "mang_n2", "mang_n3"):
        if g in gills:
            sk.slot(g, gills[g][2][0], D.pl[g].get("img", g))
    sk.slot("ham", "ham", "ham")
    sk.slot("mi_x", "dau", "mi_x", an=True)
    sk.slot("mi_n", "dau", "mi_n", an=True)
    # ---- lưới thân: trọng số = thân (chuỗi hông → cổ), đầu (đầu hoà vào cổ), đuôi (chuỗi theo đường đi trong vùng)
    Lt = luoi.luoi_vung(im_t, D.bv, D.bt, ten="than")
    Qt = dt.ra(Lt.pts, *im_t.size)
    Wb = trongso.chuoi_chieu(Qt, Jt, ["hong", "than", "nguc", "co"])
    Wh = trongso.theo_truc(Qt, gay, tam, "co", "dau", u0=-0.15, u1=0.25)
    Wd = trongso.chuoi_geo(Lt, Jq_img, duoi, cha="hong", cha_hoa=0.6)
    Mv = trongso.vung(Lt, [("_dau", m_dau), ("_duoi", m_duoi), ("_than", np.ones(nh.shape, bool))], dai_hoa=0.05 * D.cao)
    Wt = []
    for i in range(len(Qt)):
        e = {}
        for key, Wx in (("_dau", Wh), ("_duoi", Wd), ("_than", Wb)):
            f = Mv[i].get(key, 0.0)
            if f <= 0:
                continue
            for b, v in Wx[i].items():
                e[b] = e.get(b, 0.0) + f * v
        Wt.append(e)
    Wt = trongso.chuan(Wt, 4)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than (lai)")
    sk.luoi_gan("than", "than", Lt, Wt, dat=dt)
    # hàm dưới hai xương, khoang miệng màng giãn giữa môi trên và hàm
    Lj = luoi.luoi_vung(ham, D.bv, D.bt, ten="ham")
    sk.luoi_gan("ham", "ham", Lj, mieng.ham_hai_xuong(dj.ra(Lj.pts, *ham.size), hinge, snout, "dau", "ham"), dat=dj)
    mieng.long_mieng(sk, "mieng_long", "mieng", "dau", "ham", hinge, snout, duoi=-0.14, tren=(0.04, 0.07, 0.1, 0.12, 0.12),
                     q_tren=(0.0, 0.0, 0.0, 0.0, 0.0), doc=(0.05, 0.96))
    for g, (Lg, dg, nm) in gills.items():
        sk.luoi_gan(g, D.pl[g].get("img", g), Lg, trongso.chuoi(Lg.s, Lg.truc[1][-1] / 3, nm, cha="dau", cha_hoa=0.5), dat=dg)
    for c, (im, dc, Jc, nm, par) in legs.items():
        Lc = luoi.luoi_vung(im, D.bv, D.bt, vien=3, ten=c)
        Wl = trongso.lam_tron(Lc, trongso.chuoi_chieu(dc.ra(Lc.pts, *im.size), Jc, nm, cha=par, cha_hoa=0.8), 1)
        sk.luoi_gan(c, c, Lc, Wl, dat=dc)
    sk.manh("binh", "binh", dat["binh"])
    sk.manh("nap", "nap", dat["nap"])
    # mí hai mắt: dò trên lớp thân (mắt concept), mí bám xương đầu
    for lid, p in (("mi_n", (1243, 526)), ("mi_x", (1385, 532))):
        s0 = T.nguoc(dt, W(*p), *im_t.size)[0]
        kq = mieng.fit_lid(im_t, pc[lid], mat=T.mat_mat(im_t, s0, noi=4), goc=(-64, 20, 4), ti=(1.0, 3.6, 0.1),
                           ten=f"dạng 2 {lid}")
        sk.manh(lid, lid, mieng.dat_mi(dt, im_t, kq))
    for e, mo in (("trung", "đuôi đập đất (VFX cột nước trồi dưới chân đối thủ)"), ("phun", "bình đồng nhả luồng nước (VFX bám xương "
                  "mieng ở miệng bình)"), ("het_phun", "hết nhả"), ("bat_nap", "nắp bình lật mở quanh bản lề"),
                  ("gam", "ngửa cổ gầm, bình phun cột nước lên trời (VFX mây giông, mưa xối, vòi rồng quanh đối thủ)"),
                  ("het_gam", "hết chiêu cuối"), ("nen", "hai chân trước nện đất")):
        sk.su_kien(e, mo)
    foot = {c: (np.array(v[2][2]), np.array(v[2][3])) for c, v in legs.items()}
    D.iou_ghep = "lai (thân cắt từ concept)"
    info = dict(D=D, duoi=duoi, gills={g: v[2] for g, v in gills.items()}, legs={c: v[3] for c, v in legs.items()}, foot=foot, k=2,
                Jt=Jt)
    print(f"  dạng 2 (lai): {sk.tom_tat()}")
    return sk, info

def _gop_trung(W):
    out = []
    for d in W:
        e = {}
        for b, v in d.items():
            e[b] = e.get(b, 0.0) + v
        out.append(e)
    return out


def _tron2(a, b, f):
    if f <= 0:
        return a
    if f >= 1:
        return b
    e = {}
    for k, v in a.items():
        e[k] = e.get(k, 0.0) + v * (1 - f)
    for k, v in b.items():
        e[k] = e.get(k, 0.0) + v * f
    return trongso.chuan([e])[0]


def gam_evolve(P, fl, tt="n_"):
    """dạng 2 gầm khi vừa hiện ra trong clip evolve (xương có tiền tố tt)."""
    P.rot(tt + "co", 8 * fl)
    P.rot(tt + "dau", 10 * fl)
    P.rot(tt + "ham", -30 * fl)
    P.rot(tt + "nap", 38 * fl + 4 * fl * math.sin(fl * 9))     # nắp lật mở quanh bản lề phía sau


def clips2(sk, info):
    duoi, gills, legs, foot = info["duoi"], info["gills"], info["legs"], info["foot"]
    nd = len(duoi)
    DI = 3.0
    g_ph = {g: 0.55 * i for i, g in enumerate(GILLS)}
    tail_amp = np.linspace(1.2, 5.5, nd)
    front = ("chan3", "chan4")

    def nen(P, t, a=1.0):
        """nền idle: thở nặng, thân uốn sóng từ đầu xuống đuôi (đầu dẫn), đầu bù góc giữ nhìn thẳng, mang và đuôi trễ, bình lắc."""
        P.move("than", 0, a * 2.5 * (1 - math.cos(2 * math.pi * t / DI)) * 0.5)
        P.rot("nguc", 1.2 * a * T.songz(t, DI))
        P.rot("than", 0.8 * a * T.songz(t, DI, -0.5))
        P.rot("hong", 1.0 * a * T.songz(t, DI, -1.0))
        P.rot("co", -1.0 * a * T.songz(t, DI, 0.3))
        P.rot("dau", -0.9 * a * T.songz(t, DI, 0.5))
        for g, names in gills.items():
            T.chuoi_songz(P, names, t, DI / 2, np.array([2.5, 4.0, 5.5]) * a, tre=0.12, pha=g_ph[g])
        T.chuoi_songz(P, duoi, t, DI, tail_amp * a, tre=0.12, pha=0.8)
        P.rot("binh", 1.2 * a * T.songz(t, DI, -1.3))

    def feet(P, chi=None):
        T.chan_bam(sk, P, {c: v for c, v in legs.items() if chi is None or c in chi}, foot)

    def blink(P, t, khoang):
        for lid in ("mi_n", "mi_x"):
            if lid in sk.si:
                an_hien(P, lid, t, khoang)

    def idle_fn(t, P):
        nen(P, t)
        blink(P, t, [(2.0, 2.13)])
        P.rot("ham", -cv(t, [(0, 0), (0.9, 0), (1.0, 7, "out"), (1.1, 2), (1.2, 5, "out"), (1.38, 0, "io"), (DI, 0)]))
        # điểm phá nhịp: nắp bình lạch cạch
        P.rot("nap", 4.0 * cv(t, [(0, 0), (1.6, 0), (1.66, 1, "out"), (1.72, 0.1), (1.78, 0.6, "out"), (1.86, 0, "in"), (DI, 0)]))
        feet(P)

    def appear_fn(t, P, D=1.5):
        g = cv(t, [(0, 0.02), (0.5, 1.08, "out"), (0.7, 0.97, "io"), (0.9, 1.0, "io"), (D, 1.0)])
        P.scale("move", g, g)
        T.fade_all(sk, P, cv(t, [(0, 0), (0.14, 1)]))
        T.xfade(nen, P, t, D, ease((t - 0.6) / 0.6), 0.0, 0.01)
        fl = cv(t, [(0, 0), (0.75, 0), (0.95, 1, "out"), (1.25, 0, "io"), (D, 0)])
        gam_evolve(P, fl, "")
        feet(P)

    def attack_fn(t, P, D=1.3, Tt=0.62):
        """Đuôi Thủy Triều: dồn trọng tâm, đuôi nhấc cao dần (0,12–0,5), quật xuống đập đất đúng 0,62 (trung; ngọn trễ 1–2 khung),
        giữ trôi, về."""
        T.xfade(nen, P, t, D, 1 - 0.8 * hoat.bao(t, 0.05, 1.15, 0.15, 0.2), 0.4, 1.0)
        wt = cv(t, [(0, 0), (0.45, 1, "io"), (Tt, -0.6, "in"), (0.85, -0.45), (D, 0, "io")])
        P.rot("hong", -1.5 * wt)
        P.rot("than", -1.0 * wt)
        P.rot("nguc", 2 * wt)
        P.move("than", -3 * wt, -2 * max(0.0, -wt))
        P.rot("dau", 3 * wt)
        for i, b in enumerate(duoi):
            lag = 0.02 * i
            li = cv(t - lag, [(0, 0), (0.12, 0.1, "io"), (0.48, 1.0, "io"), (0.52, 1.04), (Tt, -0.5, "in"), (0.7, -0.58),
                              (0.88, -0.42, "io"), (D, 0, "io")]) if t - lag > 0 else 0.0
            P.rot(b, -(7, 8, 7, 5, 4, 3)[min(i, 5)] * li - (0 if i < 3 else 3.0 * min(0.0, li)))
        P.rot("ham", -cv(t, [(0, 0), (0.45, 4), (Tt, 14, "out"), (0.82, 8), (D, 0, "io")]))
        P.rot("binh", -4 * wt)
        feet(P)

    def cast_fn(t, P, D=1.6, Tt=0.72, E=1.3):
        """Pháo Bình Đồng: hạ thấp gồng chân (0–0,55), nắp bật 0,6, bình chúc tới, nhả luồng nước đúng 0,72 (phun), giật lùi, giữ
        rung tới 1,3, nắp rơi về chỗ, về."""
        T.xfade(nen, P, t, D, 1 - 0.85 * hoat.bao(t, 0.05, 1.5, 0.2, 0.25), 0.4, 1.4)
        lo = cv(t, [(0, 0), (0.55, 1, "io"), (Tt, 1.1, "out"), (E, 1.0), (D, 0, "io")])
        P.move("than", 0, -5 * lo)
        P.rot("nguc", -3 * lo)
        tilt = cv(t, [(0, 0), (0.45, 0.15, "io"), (Tt - 0.05, 1.0, "out"), (E, 1.0), (D, 0, "io")])
        P.rot("binh", -34 * tilt + 1.4 * rung(t, Tt + 0.03, E))
        P.move("binh", 10 * tilt, 4 * tilt)
        pop = cv(t, [(0, 0), (0.56, 0), (0.66, 1.12, "out"), (0.74, 0.96, "io"), (1.3, 1.0), (1.4, 0.0, "in"), (1.45, 0.08, "out"),
                     (1.5, 0, "in")])
        P.rot("nap", 72 * pop + 5 * rung(t, 0.75, 1.3))       # nắp bật quanh bản lề, rung trong lúc phun, sập lại
        P.move("move", cv(t, [(0, 0), (Tt, 0), (Tt + 0.08, -9, "out"), (E, -5), (D, 0, "io")]), 0)
        P.rot("ham", -(cv(t, [(0, 0), (0.55, 4), (Tt, 26, "out"), (E, 22), (D, 0, "io")]) + 2.5 * rung(t, Tt + 0.03, E)))
        P.rot("dau", 5 * cv(t, [(0, 0), (0.55, -0.4), (Tt, 1, "out"), (E, 0.8), (D, 0, "io")]))
        for g, names in gills.items():
            fl = cv(t, [(0, 0), (0.55, -5), (Tt + 0.05, 12, "out"), (E, 9), (D, 0, "io")])
            for i, b in enumerate(names):
                P.rot(b, fl * (0.5 + 0.35 * i) + 1.5 * rung(t, Tt + 0.03, E) * (i == 2))
        feet(P)

    def skill_fn(t, P, D=2.2, Tt=1.1, E=1.75):
        """Giông Bão: tụ lực (khom, đuôi cuộn 0–0,8), chồm nửa trước lên (0,8–1,1), ngửa cổ gầm há to đúng 1,1 (gam), bình dựng
        phụt cột nước, nắp bật cao; giữ rung hai dáng tới 1,75 (het_gam), hai chân trước nện đất 1,9 (nen), về."""
        T.xfade(nen, P, t, D, 1 - 0.9 * hoat.bao(t, 0.05, 2.05, 0.2, 0.3), 0.7, 2.0)
        cr = cv(t, [(0, 0), (0.75, 1, "io"), (0.85, 1.05), (Tt, -1.0, "out"), (E, -0.95), (1.9, 0.15, "in"), (2.0, -0.05, "out"),
                    (D, 0, "io")])
        rear = max(0.0, -cr)
        P.move("than", 0, -8 * max(cr, 0) + 6 * rear)
        P.rot("than", 9 * rear + 1.0 * rung(t, Tt + 0.03, E))
        P.rot("nguc", 6 * rear - 2 * max(cr, 0))
        P.rot("hong", -6 * rear)
        P.rot("co", 10 * rear + 1.2 * rung(t, Tt + 0.03, E))
        P.rot("dau", 8 * rear - 4 * max(cr, 0))
        P.rot("ham", -(cv(t, [(0, 0), (0.85, 3), (Tt, 34, "out"), (E, 30), (1.95, 0, "io"), (D, 0)]) + 4 * rung(t, Tt + 0.03, E)))
        P.rot("binh", 8 * rear + 1.5 * rung(t, Tt + 0.03, E))
        pop = cv(t, [(0, 0), (1.0, 0), (1.12, 1.08, "out"), (1.2, 0.95, "io"), (1.75, 1.0), (1.86, 0, "in"), (1.91, 0.06, "out"),
                     (1.96, 0, "in")])
        P.rot("nap", 88 * pop + 7 * rung(t, Tt + 0.05, E))
        for i, b in enumerate(duoi):
            P.rot(b, (4 + 2 * i) * max(cr, 0) * (-1 if i % 2 == 0 else 1) * 0.5 + (2 + i) * rear * 0.8)
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, (-6 + 4 * i) * rear + 2.0 * rung(t, Tt + 0.03, E))
        feet(P, chi=("chan1", "chan2"))
        # chân trước: bám đất trừ lúc chồm (nhấc theo thân), nện lại 1,9
        lift = cv(t, [(0, 0), (0.85, 0), (Tt, 1, "out"), (E, 1), (1.9, 0, "in"), (D, 0)])
        for c in front:
            names = legs[c]
            Wc = sk.the_gioi(P)
            ank = foot[c][0]
            base = (Wc["move"] @ np.array([ank[0], ank[1], 1.0]))[:2]
            fk = Wc[names[2]][:2, 2] + np.array([8.0, 6.0]) * lift
            hoat.ik_hai_doan(sk, P, names[0], names[1], base * (1 - lift) + fk * lift)
            Wc = sk.the_gioi(P)
            b = names[2]
            a_now = math.degrees(math.atan2(Wc[b][1, 0], Wc[b][0, 0]))
            a0 = math.degrees(math.atan2(sk.W0[b][1, 0], sk.W0[b][0, 0])) + math.degrees(math.atan2(Wc["move"][1, 0], Wc["move"][0, 0]))
            P.rot(b, (((a0 - a_now + 180) % 360) - 180) * (1 - lift) - 12 * lift)

    def hit_fn(t, P, D=0.7):
        T.xfade(nen, P, t, D, 1 - 0.75 * hoat.bao(t, 0.0, 0.6, 0.05, 0.15), 0.25, 0.6)
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.22, 0.5, "io"), (0.48, -0.1, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.22, 1, "io"), (0.5, -0.05, "io"), (D, 0, "io")])
        P.rot("dau", 9 * hd)
        P.rot("co", 5 * hd)
        P.rot("nguc", 3 * bd)
        P.move("move", -7 * bd, 0)
        P.rot("ham", -9 * hd)
        blink(P, t, [(0.03, 0.36)])
        P.rot("binh", -5 * bd)
        P.rot("nap", 6 * cv(t, [(0, 0), (0.1, 1), (0.16, -0.6), (0.22, 0.4), (0.3, 0), (D, 0)]))
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, (4 + 3 * (2 - i)) * cv(t, [(0, 0), (0.07 + 0.03 * (2 - i), 1, "out"), (0.36, -0.3, "io"), (D, 0, "io")]))
        for i, b in enumerate(duoi):
            P.rot(b, (3 + 1.2 * i) * cv(t, [(0, 0), (0.07 + 0.025 * (nd - 1 - i), 1, "out"), (0.4 + 0.02 * i, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    def die_fn(t, P, D=2.0):
        nen(P, t, max(0.0, 1 - t / 0.35))
        P.rot("dau", cv(t, [(0, 0), (0.07, 10, "out"), (0.3, 4), (0.9, -10, "io"), (D, -12)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 14, "out"), (0.35, 6), (0.9, 16, "io"), (D, 16)]))
        P.rot("co", cv(t, [(0, 0), (0.07, 5, "out"), (0.9, -8, "io"), (D, -8)]))
        drop = cv(t, [(0, 0), (0.35, 0), (0.75, 1, "in"), (0.82, 0.92, "out"), (D, 0.95)])
        P.move("than", 0, -30 * drop)
        P.rot("binh", cv(t, [(0, 0), (0.6, 0), (1.05, 24, "in"), (1.15, 20, "out"), (D, 21)]))
        P.move("binh", cv(t, [(0, 0), (0.6, 0), (1.05, -14, "in"), (D, -15)]), cv(t, [(0, 0), (0.6, 0), (1.05, -10, "in"), (D, -10)]))
        P.rot("nap", cv(t, [(0, 0), (0.75, 0), (0.95, 30, "out"), (1.08, 12, "in"), (1.15, 18, "out"), (D, 16)]))
        blink(P, t, [(0.04, D + 1)])
        for g, names in gills.items():
            for i, b in enumerate(names):
                P.rot(b, cv(t, [(0, 0), (0.9, -10 - 4 * i, "io"), (D, -10 - 4 * i)]))
        for i, b in enumerate(duoi):
            P.rot(b, cv(t, [(0, 0), (0.9, 2 + i, "io"), (D, 2 + i)]))
        feet(P)
        a = cv(t, [(0, 1), (1.5, 1), (1.95, 0, "io"), (D, 0)])
        T.fade_all(sk, P, a, an=("mi_n", "mi_x"))

    return [Clip("appear", 1.5, appear_fn),
            Clip("idle", DI, idle_fn, loop=True),
            Clip("attack", 1.3, attack_fn, ev=[(0.62, "trung", "")]),
            Clip("cast", 1.6, cast_fn, ev=[(0.6, "bat_nap", ""), (0.72, "phun", ""), (1.3, "het_phun", "")], trung=0.72),
            Clip("skill", 2.2, skill_fn, ev=[(1.1, "gam", ""), (1.75, "het_gam", ""), (1.9, "nen", "")], trung=1.1),
            Clip("hit", 0.7, hit_fn),
            Clip("die", 2.0, die_fn)]


def cao_game(sk, frames):
    """chiều cao khai cho game: con dài dẹt (rộng/cao > 1,42) khai cao = rộng / 1,42 để game vẽ nhỏ lại vừa sân."""
    ve = soi.Ve(sk)
    x0, y0, x1, y1 = ve.bao(frames["idle"][0])
    h = soi.chieu_cao(ve, frames["idle"][0], BO_CAO)
    return max(h, (x1 - x0) / 1.42)


def rig2():
    t0 = time.time()
    sk, info = dung2()
    cl = clips2(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    ra = T.inbox(2, "rig")
    os.makedirs(ra, exist_ok=True)
    iou = T.so_concept(sk, fr["idle"][0], 2, info["D"], os.path.join(ra, "so_concept.png"))
    ld = T.lech_dau(sk, fr, cl)
    noi = {}
    for n, (d, w) in ld.items():
        print(f"  khung 0 {n} lệch khung 0 idle {d:.2f} px ({w})")
        noi[n + " (khung 0)"] = f"khung 0 lệch khung 0 idle {d:.2f} px" + (f" ({w})" if w else "")
    noi["so_concept"] = f"IoU khung 0 idle / concept {iou:.3f}; IoU ghép mảnh (place) {info['D'].iou_ghep}"
    tk = sk.tom_tat()
    noi["mat_do"] = f"{tk['dinh']} đỉnh / cao {info['D'].cao:.0f} px rig (bước viền {info['D'].bv:.1f}, trong {info['D'].bt:.1f})"
    cao = cao_game(sk, fr)
    tong = xuat.xuat_het(sk, cl, ra, f"{T.CODE}_2", f"{T.TEN[2]} (dạng 2)", frames=fr, dang=2, so_dang=2,
                         dung_yen=("attack", "cast", "skill"), cao=cao, ma_goc=3241, noi_them=noi,
                         can=[("can_mieng_skill", "skill", 1.2, "ham", 90), ("can_binh_cast", "cast", 0.9, "binh", 130),
                              ("can_duoi_attack", "attack", 0.62, "duoi3", 130), ("can_mi_hit", "hit", 0.1, "dau", 90),
                              ("can_chan_skill", "skill", 1.3, "chan41", 90)])
    T.uon_thu(sk, [info["duoi"]] + list(info["gills"].values()), os.path.join(ra, "uon_thu.png"))
    print(f"xong dạng 2 {time.time() - t0:.1f} s; .atomik {tong['atomik_kb']:.0f} KB; game.height {cao:.0f}")
    return sk, info, cl, fr, tong
