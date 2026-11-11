# -*- coding: utf-8 -*-
"""Dựng rig Liên Kình theo CÁCH LAI (Claude điều phối 2026-11-11): thân chính (thân + đầu + cuống + vây đuôi + vây lưng + ngà)
là MỘT lưới liền cắt thẳng từ concept (tm07_lien.py); hàm dưới, vây chèo, các lớp sen / nụ cũng cắt từ concept; GPT chỉ cho lòng
miệng, mí, cánh rời, tia lỗ thở. Trọng số lưới thân = trọng số vùng mềm (đầu, ngà, vây đuôi, cuống, vây lưng, thân) nhân với trọng
số chuỗi B-spline chiếu lên sống lưng / cuống / vây (chuoi_chieu) -> thân uốn như cá bơi, không gập ở khớp.
Dùng từ tm07.py (rig2 / rig1 / soi); tên xương, slot, sự kiện giữ nguyên để clips2 / clips1 chạy không đổi.
"""
import json
import math
import os

import numpy as np
from PIL import Image

from quai import anh, luoi, mieng, trongso
from quai.khung import Dat, Sk

import tm07 as T

NUOC_HE = {2: 0.88, 1: 0.68}   # thu nước về cỡ đệm sóng / vũng trong concept
GPT_TI = {2: {"mi": 0.70, "mieng": 0.5, "canh_a": 0.6, "canh_b": 0.6, "canh_c": 0.6, "phun_lo": 0.5},
          1: {"mi": 0.62, "mieng": 0.5, "canh_a": 0.6, "canh_b": 0.6, "canh_c": 0.6, "nu_truoc": 0.56}}


def nap_lien(k, sc=None):
    """mảnh cắt từ concept (lien/, tỉ lệ đúng concept) + mảnh GPT còn dùng (manh/) + nước Hải Long. Trả (pc, nuoc, lien_bbox)."""
    sc = sc or T.SC[k]
    d = os.path.join(T.d_inbox(k), "lien")
    lien = json.load(open(os.path.join(d, "lien.json"), encoding="utf-8"))
    pc = {}
    for nm in lien:
        im = Image.open(os.path.join(d, nm + ".png")).convert("RGBA")
        if abs(sc - 1) > 1e-6:
            im = im.resize((max(2, round(im.width * sc)), max(2, round(im.height * sc))), Image.LANCZOS)
        pc[nm] = anh.loang_mau(im)
    gpt = {nm: T.GIU_CHO[k][nm] for nm in GPT_TI[k] if nm != "mieng"}
    pc.update(anh.nap_manh(os.path.join(T.d_inbox(k), "manh"), gpt, ti_le=sc, ti_le_rieng=GPT_TI[k]))
    # lòng miệng: mảng đỏ rượu đặc (hình chữ nhật kín góc, đốm họng sẫm) để lấp kín lỗ miệng / lỗ hàm của mảnh thân khi há
    from PIL import ImageDraw
    mi_ = Image.new("RGBA", (240, 160), (139, 47, 69, 255))
    ImageDraw.Draw(mi_).ellipse((70, 40, 190, 130), fill=(106, 31, 51, 255))
    pc["mieng"] = mi_
    nuoc = anh.nap_manh(T.HL_MANH, {n: ("tron", 200, 200, (58, 150, 226)) for n in T.NUOC_TI}, ti_le=T.SC[1], ti_le_rieng=T.NUOC_TI)
    return pc, nuoc, lien


def tron_vung(L, vung_tron, dai_hoa, ham_chuoi):
    """trọng số cuối = Σ_vùng w_vùng(đỉnh) · f_vùng(đỉnh). vung_tron: [(tên vùng, đa giác px ảnh)] theo ưu tiên; ham_chuoi: {tên vùng:
    list dict trọng số từng đỉnh (chuỗi) hoặc tên xương (cứng)}."""
    Wv = trongso.vung(L, vung_tron, dai_hoa=dai_hoa)
    out = []
    for i, wv in enumerate(Wv):
        d = {}
        for r, w in wv.items():
            f = ham_chuoi[r]
            src = {f: 1.0} if isinstance(f, str) else f[i]
            for b, wb in src.items():
                d[b] = d.get(b, 0.0) + w * wb
        out.append(d)
    return trongso.chuan(out, toi_da=4)


# ================================================================ dạng 2
def dung2(pc, nuoc, lien, nuoc_thua=False, luoi_thua=1.0, sc=None):
    k = 2
    S = sc or T.SC[k]
    he = S / T.SC[k]
    bv, bt = T.BUOC[k][0] * luoi_thua * he, T.BUOC[k][1] * luoi_thua * he
    print(f"  bước lưới dạng {k}: viền {bv:.1f}, trong {bt:.1f} px (cao {T.CAO[k] * he:.0f}); cách lai (thân cắt từ concept)")
    O = T.O_CONCEPT[k]

    def R(x, y):
        return ((x - O[0]) * S, (O[1] - y) * S)

    def I(nm, pts):   # concept px -> px ảnh mảnh
        x0, y0 = lien[nm][0], lien[nm][1]
        return [((x - x0) * S, (y - y0) * S) for x, y in pts]

    def DL(nm):       # Dat của mảnh cắt: tâm khung bao
        x0, y0, x1, y1 = lien[nm]
        return Dat(*R((x0 + x1) / 2, (y0 + y1) / 2), neo=(0.5, 0.5))
    sk = Sk(f"{T.CODE}_2")
    for n, im in pc.items():
        sk.anh(n, im)
    sk.xuong("root")
    sk.xuong("move", "root")
    info = {"pc": pc}
    # ---- xương
    Jc = [(335, 585), (462, 612), (600, 623), (740, 613), (880, 588), (1010, 552), (1120, 512)]
    J = np.array([R(*p) for p in Jc])
    sk.xuong("than", "move", *J[4], goc=math.degrees(math.atan2(*(J[5] - J[4])[::-1])), dai=60, the_gioi=True)
    bk = sk.chuoi("bk", "than", [J[4], J[3], J[2], J[1], J[0]])
    fw = sk.chuoi("fw", "than", [J[4], J[5], J[6]])
    body_names = ["bk3", "bk2", "bk1", "bk0", "fw0", "fw1"]
    Jd = np.array([R(*p) for p in ((335, 585), (295, 548), (262, 505), (243, 468))])
    du = sk.chuoi("du", "bk3", Jd)
    sk.xuong("vd", "du2", *Jd[3], goc=sk.goc_tg("du2")[2], dai=40, the_gioi=True)
    Jl = np.array([R(*p) for p in ((530, 455), (490, 340), (445, 240))])
    vl = sk.chuoi("vl", "bk2", Jl)
    neck = J[6]
    goc_dau = 14.0
    sk.xuong("dau", "fw1", *neck, goc=goc_dau, dai=200 * S, the_gioi=True)
    hinge, snout = np.array(R(1180, 448)), np.array(R(1348, 405))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    mp = hinge + 0.86 * (snout - hinge) + np.array([0, 6])
    sk.xuong("mieng", "dau", *mp, goc=gj + 4, dai=40, the_gioi=True)
    tr, tip = np.array(R(1252, 336)), np.array(R(1522, 158))
    gn = math.degrees(math.atan2(*(tip - tr)[::-1]))
    sk.xuong("nga", "dau", *tr, goc=gn, dai=float(np.hypot(*(tip - tr))), the_gioi=True)
    sk.xuong("mui_nga", "nga", float(np.hypot(*(tip - tr))) * 0.97, 0, 0, 20)
    bl = R(1150, 292)
    sk.xuong("lo_tho", "dau", *bl, goc=100, dai=20, the_gioi=True)
    Jg = np.array([R(*p) for p in ((905, 592), (850, 690), (780, 790), (700, 870))])
    vg = sk.chuoi("vg", "fw0", Jg)
    Jx = np.array([R(*p) for p in ((1010, 332), (1060, 286), (1118, 238))])
    vx = sk.chuoi("vx", "fw0", Jx)
    sen0 = R(772, 486)
    sk.xuong("sen", "bk0", *sen0, goc=90, dai=30, the_gioi=True)
    ims, imt = pc["sen_sau"], pc["sen_truoc"]
    cs = [sk.xuong(f"cs{i}", "sen", *sen0, goc=90 + a, dai=ims.height * 0.8, the_gioi=True) for i, a in enumerate((42, 21, 0, -21, -42))]
    ct = [sk.xuong(f"ct{i}", "sen", *sen0, goc=90 + a, dai=imt.height * 0.8, the_gioi=True) for i, a in enumerate((40, 14, -14, -40))]
    info.update(bk=bk, fw=fw, du=du, vl=vl, vg=vg, vx=vx, cs=cs, ct=ct)

    # ---- slot (sau -> trước), nước ở giữa
    def sau_than():
        sk.slot("vx", vx[0], "vx")

    def truoc_than():
        sk.slot("than", "than", "than")          # lòng miệng đã tô đỏ rượu vào lỗ hàm / lỗ miệng của chính mảnh thân
        sk.slot("ham", "ham", "ham")
        sk.slot("nga", "nga", "nga")
        sk.slot("mi", "dau", "mi", an=True)
        sk.slot("phun_lo", "lo_tho", "phun_lo", an=True)
        sk.slot("sen_sau", "sen", "sen_sau")
        sk.slot("dai", "sen", "dai")
        sk.slot("sen_truoc", "sen", "sen_truoc")
        sk.slot("vg", vg[0], "vay_cheo")
        for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
            sk.xuong(f"cr{i}", "sen", 0, 0)
            sk.slot(f"cr{i}", f"cr{i}", nmp, an=True)
        return "cr2"
    info["nuoc"] = T.them_nuoc(sk, nuoc, k, truoc_than, sau_than, thua=nuoc_thua, he=he * NUOC_HE[k])

    # ---- lưới thân liền: vùng mềm × chuỗi
    im = pc["than"]
    Lt = luoi.luoi_vung(im, bv, bt, vien=3, ten="than")
    dat_than = DL("than")
    Q = dat_than.ra(Lt.pts, im.width, im.height)
    f_body = trongso.chuoi_chieu(Q, J, body_names)
    f_du = trongso.chuoi_chieu(Q, Jd, du, cha="bk3", cha_hoa=0.6)
    f_vl = trongso.chuoi_chieu(Q, Jl, vl, cha="bk2", cha_hoa=0.6)
    vung2 = [("vd", I("than", [(0, 180), (432, 180), (432, 445), (300, 474), (262, 504), (205, 484), (0, 450)])),   # vây đuôi: cứng theo vd, ưu tiên trước
             ("nga", I("than", [(1243, 348), (1262, 300), (1300, 262), (1500, 142), (1532, 180), (1335, 352)])),
             ("dau", I("than", [(1035, 232), (1130, 212), (1250, 250), (1300, 300), (1352, 400), (1358, 480), (1300, 565), (1150, 600), (1060, 590), (1030, 520), (1035, 420)])),
             ("du", I("than", [(205, 468), (300, 466), (365, 545), (332, 606), (238, 560)])),
             ("vl", I("than", [(420, 232), (568, 222), (604, 380), (560, 475), (470, 465)])),
             ("than", I("than", [(0, 0), (1536, 0), (1536, 1024), (0, 1024)]))]
    Wt = tron_vung(Lt, vung2, 34 * S, {"nga": "nga", "dau": "dau", "vd": "vd", "du": f_du, "vl": f_vl, "than": f_body})
    Wt = trongso.lam_tron(Lt, Wt, 1)
    trongso.kiem(Wt, "than", cho_cung=("nga", "vd"))
    sk.luoi_gan("than", "than", Lt, Wt, dat=dat_than)
    # ---- hàm dưới (cắt concept): lưới hai xương; lòng miệng GPT theo hàm
    imj = pc["ham"]
    dat_ham = DL("ham")
    Lj = luoi.luoi_vung(imj, bv * 0.8, bt * 0.8, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *imj.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    sk.manh("nga", "nga", DL("nga"))
    # ---- mí: dò trên chính mảnh thân (mống cyan)
    kq = mieng.fit_lid(im, pc["mi"], mat=T.mat_cyan(im), ten="dạng 2")
    sk.manh("mi", "mi", mieng.dat_mi(dat_than, im, kq))
    sk.manh("phun_lo", "phun_lo", Dat(*bl, goc=goc_dau, neo=(0.5, 1.0)))
    # ---- vây chèo gần / xa (cắt concept): chuỗi chiếu
    for nm, slot, names, Jf, cha in (("vay_cheo", "vg", vg, Jg, "fw0"), ("vx", "vx", vx, Jx, "fw0")):
        imf = pc[nm]
        if nm == "vx" and he != 1:          # bản co trong rig gộp: vây xa nhỏ (~60 px) làm mảnh cứng, khỏi hở ở viền mỏng
            sk.manh(slot, nm, DL(nm), xuong=names[0])
            continue
        Lf = luoi.luoi_vung(imf, bv, bt, vien=(3 if he == 1 else 5), ten=nm)
        datf = DL(nm)
        Wf = trongso.chuoi_chieu(datf.ra(Lf.pts, *imf.size), Jf, names, cha=cha, cha_hoa=0.6)
        sk.luoi_gan(slot, nm, Lf, Wf, dat=datf)
    # ---- sen: mỗi lớp một lưới, cột = cánh
    for nm_, names in (("sen_sau", cs), ("sen_truoc", ct)):
        im_ = pc[nm_]
        ww, hh_ = im_.size
        Lp = luoi.luoi_vung(im_, bv, bt, vien=(2 if he == 1 else 4), ten=nm_)   # bản co: chóp cánh mảnh, nới viền 4 px
        n = len(names)
        regs = [(b, [(i * ww / n, 0), ((i + 1) * ww / n, 0), ((i + 1) * ww / n, hh_), (i * ww / n, hh_)]) for i, b in enumerate(names)]
        Wp = trongso.vung(Lp, regs, dai_hoa=16 * S)
        for d, (px, py) in zip(Wp, Lp.pts):
            kk = max(0.0, 1 - (hh_ - py) / (0.22 * hh_))
            if kk > 0:
                for b in list(d):
                    d[b] *= 1 - kk
                d["sen"] = d.get("sen", 0.0) + kk
        sk.luoi_gan(nm_, nm_, Lp, trongso.lam_tron(Lp, trongso.chuan(Wp), 1), dat=DL(nm_))
    sk.manh("dai", "dai", DL("dai"))
    for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
        sk.manh(f"cr{i}", nmp, Dat(*sen0, neo=(0.5, 0.5)))
    for e, m in (("trung", "ngà đâm trúng (VFX lưỡi nước liềm từ mui_nga)"), ("phun", "bắt đầu phun Thủy Pháo (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "chiêu cuối: gầm, sen xoè"), ("song", "đuôi quật xuống nước: VFX sóng sen dâng"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    return sk, info


# ================================================================ dạng 1
def dung1(pc, nuoc, lien):
    k = 1
    S = T.SC[k]
    bv, bt = T.BUOC[k]
    print(f"  bước lưới dạng {k}: viền {bv:.1f}, trong {bt:.1f} px (cao {T.CAO[k]:.0f}); cách lai")
    O = T.O_CONCEPT[k]

    def R(x, y):
        return ((x - O[0]) * S, (O[1] - y) * S)

    def I(nm, pts):
        x0, y0 = lien[nm][0], lien[nm][1]
        return [((x - x0) * S, (y - y0) * S) for x, y in pts]

    def DL(nm):
        x0, y0, x1, y1 = lien[nm]
        return Dat(*R((x0 + x1) / 2, (y0 + y1) / 2), neo=(0.5, 0.5))
    sk = Sk(f"{T.CODE}_1")
    for n, im in pc.items():
        sk.anh(n, im)
    sk.xuong("root")
    sk.xuong("move", "root")
    info = {"pc": pc}
    sk.xuong("than", "move", *R(712, 536), dai=40)
    sk.xuong("hong", "than", *R(520, 560), the_gioi=True, dai=30)
    sk.xuong("nguc", "than", *R(880, 520), goc=6, the_gioi=True, dai=30)
    Jd = np.array([R(*p) for p in ((455, 585), (440, 525), (445, 468))])
    du = sk.chuoi("du", "hong", Jd)
    sk.xuong("vd", "du1", *Jd[2], goc=sk.goc_tg("du1")[2], dai=30, the_gioi=True)
    Jl = np.array([R(*p) for p in ((612, 400), (600, 352), (582, 322))])
    vl = sk.chuoi("vl", "than", Jl)
    neck = R(905, 500)
    goc_dau = 4.0
    sk.xuong("dau", "nguc", *neck, goc=goc_dau, dai=150 * S, the_gioi=True)
    hinge, snout = np.array(R(1050, 572)), np.array(R(1120, 580))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    mp = hinge + 0.86 * (snout - hinge) + np.array([0, 5])
    sk.xuong("mieng", "dau", *mp, goc=gj + 4, dai=30, the_gioi=True)
    tr, tip = np.array(R(1000, 362)), np.array(R(1086, 282))
    gn = math.degrees(math.atan2(*(tip - tr)[::-1]))
    sk.xuong("nga", "dau", *tr, goc=gn, dai=float(np.hypot(*(tip - tr))), the_gioi=True)
    sk.xuong("mui_nga", "nga", float(np.hypot(*(tip - tr))) * 0.95, 0, 0, 10)
    Jg = np.array([R(*p) for p in ((705, 612), (742, 690), (762, 760))])
    vg = sk.chuoi("vg", "than", Jg)
    nu0 = np.array(R(730, 360))
    sk.xuong("nu", "than", *nu0, goc=96, dai=30, the_gioi=True)
    sk.xuong("nu_s", "nu", 0, 0)
    sk.xuong("nu_t", "nu", 0, 0)
    info.update(du=du, vg=vg, vl=vl)

    def sau_than():
        pass

    def truoc_than():
        sk.slot("than", "than", "than")
        sk.slot("ham", "ham", "ham")
        sk.slot("nga", "nga", "nga")
        sk.slot("mi", "dau", "mi", an=True)
        sk.slot("de_nu", "nu", "de_nu")
        sk.slot("nu_sau", "nu_s", "nu_sau")
        sk.slot("nu_truoc", "nu_t", "nu_truoc", an=True)   # lớp cánh GPT chỉ hiện lúc nụ bung
        sk.slot("vg", vg[0], "vay_cheo")
        for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
            sk.xuong(f"cr{i}", "nu", 0, 0)
            sk.slot(f"cr{i}", f"cr{i}", nmp, an=True)
        return "cr2"
    info["nuoc"] = T.them_nuoc(sk, nuoc, k, truoc_than, sau_than, he=NUOC_HE[k])
    im = pc["than"]
    Lt = luoi.luoi_vung(im, bv, bt, vien=3, ten="than")
    dat_than = DL("than")
    Q = dat_than.ra(Lt.pts, im.width, im.height)
    f_du = trongso.chuoi_chieu(Q, Jd, du, cha="hong", cha_hoa=0.6)
    f_vl = trongso.chuoi_chieu(Q, Jl, vl, cha="than", cha_hoa=0.6)
    vung1 = [("vd", I("than", [(360, 340), (540, 340), (536, 456), (470, 476), (400, 468), (360, 450)])),
             ("nga", I("than", [(988, 292), (1030, 272), (1082, 282), (1092, 362), (1000, 372)])),
             ("dau", I("than", [(830, 290), (900, 250), (1050, 275), (1125, 400), (1128, 570), (1080, 650), (960, 700), (860, 650), (820, 520)])),
             ("du", I("than", [(418, 452), (470, 452), (482, 560), (432, 592), (400, 520)])),
             ("vl", I("than", [(556, 318), (652, 316), (644, 404), (568, 404)])),
             ("hong", I("than", [(378, 225), (560, 225), (560, 830), (378, 830)])),
             ("nguc", I("than", [(820, 225), (1140, 225), (1140, 830), (820, 830)])),
             ("than", I("than", [(0, 0), (1536, 0), (1536, 1024), (0, 1024)]))]
    Wt = tron_vung(Lt, vung1, 60 * S, {"nga": "nga", "dau": "dau", "vd": "vd", "du": f_du, "vl": f_vl, "hong": "hong", "nguc": "nguc", "than": "than"})
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than", cho_cung=("nga", "vd"))
    sk.luoi_gan("than", "than", Lt, Wt, dat=dat_than)
    imj = pc["ham"]
    dat_ham = DL("ham")
    Lj = luoi.luoi_vung(imj, bv * 0.8, bt * 0.8, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *imj.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    sk.manh("nga", "nga", DL("nga"))
    kq = mieng.fit_lid(im, pc["mi"], mat=T.mat_cyan(im), ten="dạng 1")
    sk.manh("mi", "mi", mieng.dat_mi(dat_than, im, kq))
    imf = pc["vay_cheo"]
    Lf = luoi.luoi_vung(imf, bv, bt, ten="vay_cheo")
    datf = DL("vay_cheo")
    sk.luoi_gan("vg", "vay_cheo", Lf, trongso.chuoi_chieu(datf.ra(Lf.pts, *imf.size), Jg, vg, cha="than", cha_hoa=0.6), dat=datf)
    sk.manh("de_nu", "de_nu", DL("de_nu"))
    sk.manh("nu_sau", "nu_sau", DL("nu_sau"))
    sk.manh("nu_truoc", "nu_truoc", Dat(*(nu0 + np.array([4, -4])), goc=-4, neo=(0.5, 0.97)))
    for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
        sk.manh(f"cr{i}", nmp, Dat(*nu0, neo=(0.5, 0.5)))
    for e, m in (("trung", "viên nước rời miệng (VFX bám mieng)"), ("phun", "bắt đầu nhả bong bóng sen"), ("het_phun", "hết nhả"),
                 ("bung", "nụ bật mở: VFX mưa cánh sen"), ("het_bung", "nụ khép lại")):
        sk.su_kien(e, m)
    return sk, info
