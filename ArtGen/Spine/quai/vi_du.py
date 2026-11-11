# -*- coding: utf-8 -*-
"""Con thử của thư viện quai: dựng từ hình giữ chỗ (thân, đầu, hàm + lòng miệng, mắt + mí, đuôi chuỗi 5 đốt, hai chân 2 đốt
bám đất bằng IK, râu dây mềm, bong bóng bay vòng bằng aura), đủ clip (appear, idle, attack, cast, skill, hit, die, aura), dạng 2
giữ chỗ (to hơn, màu đậm, thêm vây cứng) để gộp tiến hóa, xuất .atomik + game.json, nạp lại kiểm, tờ khung, lưới, ảnh cận.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/quai/vi_du.py
Ra: ArtGen/Spine/quai/vi_du_ra/dang_1 (rig gộp tiến hóa), dang_2.
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import numpy as np  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, DayMem, LoXo, an_hien, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

RA = os.path.join(HERE, "vi_du_ra")
B_VIEN, B_TRONG = 11.0, 15.0   # bước lưới đích (pixel atlas)


def manh(dang):
    k = 1.0 if dang == 1 else 1.18
    cb = (86, 160, 214) if dang == 1 else (38, 92, 168)
    ch = (98, 178, 226) if dang == 1 else (52, 110, 190)
    P = {"than": anh.gia("tron", int(300 * k), int(200 * k), cb)}
    dau = anh.gia("bo", int(220 * k), int(170 * k), ch)
    dau.alpha_composite(anh.gia("mat", int(50 * k), int(44 * k)), (int(120 * k), int(40 * k)))
    P["dau"] = dau
    P["ham"] = anh.gia("ham", int(120 * k), int(46 * k), (242, 217, 160))
    P["mieng"] = anh.gia("mieng", int(110 * k), int(60 * k))
    P["mi"] = anh.gia("mi", int(62 * k), int(44 * k), ch)
    P["duoi"] = anh.gia("dai", int(260 * k), int(72 * k), cb)
    P["chan_t"] = anh.gia("chan", int(70 * k), int(120 * k), cb)
    P["chan_s"] = P["chan_t"].copy()          # trùng điểm ảnh: atlas dùng chung một vùng
    P["rau"] = anh.gia("luoi", int(130 * k), 18, (244, 238, 220))
    P["bong"] = anh.gia("tron", 40, 40, (200, 235, 250), vien=3)
    P["tay"] = anh.gia("ong", int(150 * k), int(64 * k), ch)   # ống hai chỏm tròn: thử luoi_dai(mu=True)
    if dang == 2:
        P["vay"] = anh.gia("giot", 80, 100, (233, 184, 74))
    return {n: anh.loang_mau(im) for n, im in P.items()}, k


def dung(dang):
    """dựng rig một dạng: trả (sk, info)."""
    pc, k = manh(dang)
    sk = khung.Sk(f"vi_du_{dang}")
    for n, im in pc.items():
        sk.anh(n, im)
    S = lambda x, y: (x * k, y * k)  # noqa: E731
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *S(0, 150), dai=60)
    sk.xuong("hong", "than", *S(-75, 150), the_gioi=True, dai=40)
    sk.xuong("nguc", "than", *S(75, 160), the_gioi=True, dai=40)
    sk.xuong("dau", "nguc", *S(110, 235), the_gioi=True, dai=100 * k)
    hinge, snout = np.array(S(150, 225)), np.array(S(265, 215))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    sk.xuong("mieng", "dau", *S(274, 222), goc=-4, dai=40, the_gioi=True)   # chỗ nhả cho VFX: trục x chĩa hướng nhả
    # đuôi: dải lưới 5 đốt, ảnh vẽ duỗi ngang gốc bên trái; đặt lật cho ngọn chĩa ra sau (trái), hơi vểnh
    dat_duoi = Dat(*S(-118, 162), goc=-20, neo=(0.0, 0.5), lat=True)
    Ld = luoi.luoi_dai(pc["duoi"], 5, ten="duoi", buoc=13)
    duoi = sk.chuoi("duoi", "hong", dat_duoi.ra(Ld.khop(5), *pc["duoi"].size))
    # chân: dải dọc 2 đốt (trục từ trên xuống), gốc chân hoà vào ngực / hông
    legs = {}
    for side, x0, par in (("t", 85, "nguc"), ("s", -80, "hong")):
        im = pc["chan_" + side]
        Lc = luoi.luoi_dai(im, 2, truc=[(im.width / 2, 0), (im.width / 2, im.height)], ten="chan_" + side, buoc=12)
        dat = Dat(*S(x0, 120), neo=(0.5, 0.0))
        J = dat.ra(Lc.khop(2), *im.size)
        J[-1, 1] = 6 * k
        names = sk.chuoi("ch" + side, par, J)
        legs[side] = (Lc, dat, names, J)
    # râu: dây mềm 4 đốt trên mõm
    # tay mập: ống hai chỏm tròn 2 đốt, gốc chìm vào ngực; luoi_dai(mu=True) phủ kín hai chỏm (so với bản không mũ)
    dat_tay = Dat(*S(70, 150), goc=-62, neo=(0.12, 0.5))
    luoi.luoi_dai(pc["tay"], 2, ten="tay (không mũ, để so)")
    Lt_ = luoi.luoi_dai(pc["tay"], 2, mu=True, ten="tay")
    tay = sk.chuoi("tay", "nguc", dat_tay.ra(Lt_.khop(2), *pc["tay"].size))
    dat_rau = Dat(*S(246, 236), goc=-16, neo=(0.0, 0.5))
    Lr = luoi.luoi_dai(pc["rau"], 4, ten="rau", buoc=11)
    rau = sk.chuoi("rau", "dau", dat_rau.ra(Lr.khop(4), *pc["rau"].size))
    sk.xuong("bong", "root", *S(0, 430))
    # slot: sau → trước
    sk.slot("chan_s", legs["s"][2][0], "chan_s")
    sk.slot("duoi", duoi[0], "duoi")
    sk.slot("than", "than", "than")
    if dang == 2:
        sk.slot("vay", "than", "vay")
    sk.slot("chan_t", legs["t"][2][0], "chan_t")
    sk.slot("tay", tay[0], "tay")
    sk.slot("mieng", "ham", "mieng")
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("rau", rau[0], "rau")
    sk.slot("bong", "bong", "bong")
    # thân: lưới vùng đều, ba vùng hoà theo khoảng cách đi trong lưới
    im = pc["than"]
    Lt = luoi.luoi_vung(im, B_VIEN, B_TRONG, ten="than")
    w, h = im.size
    Wt = trongso.vung(Lt, [("hong", [(0, 0), (0.3 * w, 0), (0.3 * w, h), (0, h)]), ("nguc", [(0.7 * w, 0), (w, 0), (w, h), (0.7 * w, h)]),
                           ("than", [(0, 0), (w, 0), (w, h), (0, h)])], dai_hoa=60 * k)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=Dat(*S(0, 150)))
    if dang == 2:   # vây cứng thật: mảnh cứng bám 100% thân
        sk.manh("vay", "vay", Dat(*S(-20, 238), goc=12, neo=(0.5, 0.92)))
    # đầu: lưới vùng; góc dưới-sau (cổ) hoà vào ngực
    im = pc["dau"]
    dat_dau = Dat(*S(180, 285))
    Lh = luoi.luoi_vung(im, B_VIEN, B_TRONG, ten="dau")
    w, h = im.size
    Wh = trongso.vung(Lh, [("nguc", [(0, 0.72 * h), (0.28 * w, 0.86 * h), (0.3 * w, h), (0, h)]), ("dau", [(0, 0), (w, 0), (w, h), (0, h)])],
                      dai_hoa=26 * k)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    # hàm dưới: lưới hai xương (sau bản lề: đầu / cổ họng, trước: hàm)
    im = pc["ham"]
    dat_ham = Dat(*hinge, goc=gj, neo=(0.06, 0.25))
    Lj = luoi.luoi_vung(im, 9.0, 12.0, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *im.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    # lòng miệng: thuộc hàm dưới, lưới 5×3
    mieng.long_mieng(sk, "mieng", "mieng", "dau", "ham", hinge, snout, duoi=-0.24)
    # mí mắt: dò cho phủ kín
    kq = mieng.fit_lid(pc["dau"], pc["mi"], hat=(int(120 * k + 0.58 * 50 * k), int(40 * k + 0.52 * 44 * k)), ten=f"dạng {dang}")
    sk.manh("mi", "mi", mieng.dat_mi(dat_dau, pc["dau"], kq))
    # đuôi, chân, râu: trọng số B-spline dọc dải
    seg = Ld.truc[1][-1] / 5
    Wd = trongso.chuoi(Ld.s, seg, duoi, cha="hong", cha_hoa=0.7)
    trongso.kiem(Wd, "duoi")
    sk.luoi_gan("duoi", "duoi", Ld, Wd, dat=dat_duoi)
    for side, (Lc, dat, names, J) in legs.items():
        par = "nguc" if side == "t" else "hong"
        Wc = trongso.chuoi(Lc.s, Lc.truc[1][-1] / 2, names, cha=par, cha_hoa=0.8)
        sk.luoi_gan("chan_" + side, "chan_" + side, Lc, Wc, dat=dat)
    Wr = trongso.chuoi(Lr.s, Lr.truc[1][-1] / 4, rau, cha="dau", cha_hoa=0.5)
    Wy = trongso.chuoi(Lt_.s, Lt_.truc[1][-1] / 2, tay, cha="nguc", cha_hoa=0.7)
    trongso.kiem(Wy, "tay")
    sk.luoi_gan("tay", "tay", Lt_, Wy, dat=dat_tay)
    sk.luoi_gan("rau", "rau", Lr, Wr, dat=dat_rau)
    sk.manh("bong", "bong", Dat(*S(0, 430)))
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                 ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    foot = {s: np.array(J[-1]) for s, (_, _, _, J) in legs.items()}
    return sk, {"k": k, "duoi": duoi, "rau": rau, "tay": tay, "legs": {s: v[2] for s, v in legs.items()}, "foot": foot, "pc": pc}


# ---------------------------------------------------------------- clip
def clips(sk, info, dang):
    k, duoi, rau, legs, foot = info["k"], info["duoi"], info["rau"], info["legs"], info["foot"]
    tay = info["tay"]
    tail_amp = np.array([3, 4, 5.5, 7, 8.5]) * (0.8 if dang == 2 else 1.0)
    mem = [LoXo(duoi, k=[420, 340, 270, 210, 170], damp=0.6, maxang=12),
           DayMem(rau, k0=0.22, k1=0.06, zeta=0.5, lim=(16, 26), luc=lambda t, i: np.array([0.0, -900.0 * (1 + i)]))]
    soft = lambda extra=(): mem + list(extra)  # noqa: E731

    def nen(P, tt, amp=1.0):
        """chuyển động nền của idle (giờ tt); amp giảm khi đang ra đòn."""
        s, c = song(tt, 2.0), song(tt, 2.0, 1.2)
        P.move("than", 0, 3.0 * k * s * amp)
        P.rot("nguc", 1.6 * c * amp)
        P.rot("hong", -1.0 * c * amp)
        P.rot("dau", (-2.0 * c + 1.4 * song(tt, 2.0, 2.2)) * amp)
        chuoi_song(P, duoi, tt, 2.0, tail_amp * amp, tre=0.12, ngon_dan=False)
        chuoi_song(P, tay, tt, 2.0, [5 * amp, 8 * amp], tre=0.1, ngon_dan=False, pha=1.0)

    def feet(P):
        W = sk.the_gioi(P)
        for s, names in legs.items():
            tgt = (W["move"] @ np.array([foot[s][0], foot[s][1], 1.0]))[:2]
            hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)

    def idle_fn(t, P):
        nen(P, t)
        P.rot("ham", -cv(t, [(0, 0), (0.62, 0), (0.72, 14, "out"), (0.8, 3), (0.9, 10, "out"), (1.05, 0, "io"), (2.0, 0)]))  # táp miệng
        an_hien(P, "mi", t, [(1.32, 1.44)])                                                                               # chớp mắt
        feet(P)

    def appear_fn(t, P, D=1.2):
        g = cv(t, [(0, 0.02), (0.42, 1.12, "out"), (0.6, 0.95, "io"), (0.8, 1.0, "io"), (D, 1.0)])
        P.scale("move", g, g)
        a = cv(t, [(0, 0), (0.12, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        nen(P, lui(t, D), ease((t - 0.5) / 0.6))
        P.rot("dau", 10 * cv(t, [(0, 0), (0.7, 0), (0.85, 1, "out"), (1.05, 0, "io"), (D, 0)]))
        P.rot("ham", -22 * cv(t, [(0, 0), (0.7, 0), (0.85, 1, "out"), (1.05, 0, "io"), (D, 0)]))
        feet(P)

    def attack_fn(t, P, D=0.9, H=0.42):
        lean = cv(t, [(0, 0), (0.3, 1, "io"), (0.36, 1.08), (H, -1.15, "in"), (0.47, -1.25), (0.64, -1.1, "io"), (D, 0, "io")])
        nen(P, lui(t, D), 1 - 0.7 * hoat.bao(t, 0.1, 0.8, 0.2, 0.25))
        P.move("move", cv(t, [(0, 0), (0.3, -12 * k), (H, 24 * k, "in"), (0.64, 20 * k), (D, 0, "io")]), 0)
        P.rot("nguc", 6 * lean)
        P.rot("hong", -3 * lean)
        P.rot("dau", 9 * lean)
        P.rot("ham", -cv(t, [(0, 0), (0.28, 24, "io"), (H - 0.03, 28), (H, 2, "in"), (0.62, 0), (D, 0)]))
        P.scale("dau", cv(t, [(0, 1), (H - 0.03, 1), (H, 1.12), (H + 0.05, 0.97), (0.62, 1), (D, 1)]),
                cv(t, [(0, 1), (H - 0.03, 1), (H, 0.93), (H + 0.05, 1.03), (0.62, 1), (D, 1)]))
        feet(P)

    def cast_fn(t, P, D=1.0, H=0.52, E=0.85):
        rear = cv(t, [(0, 0), (0.42, 1, "io"), (0.49, 1.06), (H, -0.6, "in"), (0.6, -0.7), (E, -0.6), (D, 0, "io")])
        nen(P, lui(t, D), 1 - 0.8 * hoat.bao(t, 0.1, 0.95, 0.2, 0.2))
        P.rot("nguc", 5 * rear)
        P.rot("dau", 9 * rear + 1.4 * rung(t, H + 0.04, E))
        P.rot("ham", -(cv(t, [(0, 0), (0.42, 6, "io"), (H, 36, "out"), (E, 32), (D, 0, "io")]) + 3 * rung(t, H + 0.04, E)))
        P.move("move", cv(t, [(0, 0), (H, 0), (H + 0.08, -10 * k, "out"), (E, -6 * k), (D, 0, "io")]), 0)
        feet(P)

    def skill_fn(t, P, D=1.8, H=0.66, E=1.3):
        cr = cv(t, [(0, 0), (0.55, 1, "io"), (0.62, 1.06), (H, -1, "out"), (E, -1), (D, 0, "io")])
        nen(P, lui(t, D), 1 - 0.85 * hoat.bao(t, 0.1, 1.7, 0.25, 0.4))
        P.scale("move", 1 + 0.05 * max(cr, 0) - 0.03 * min(cr, 0), 1 - 0.09 * max(cr, 0) + 0.06 * min(cr, 0))
        P.rot("nguc", -4 * cr + 1.5 * rung(t, H + 0.04, E))
        P.rot("dau", -10 * cr + 2.0 * rung(t, H + 0.04, E))
        P.rot("ham", -(cv(t, [(0, 0), (0.55, 4), (H, 40, "out"), (E, 36), (D, 0, "io")]) + 4 * rung(t, H + 0.04, E)))
        for i, b in enumerate(duoi):
            P.rot(b, (4 + 3 * i) * max(-cr, 0) * (1 if i % 2 else -1) * 0.6)
        feet(P)

    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        P.rot("dau", 16 * hd)
        P.rot("nguc", 7 * bd)
        P.move("move", -10 * k * bd, 0)
        P.rot("ham", -12 * hd)
        an_hien(P, "mi", t, [(0.03, 0.32)])
        for i, b in enumerate(duoi):   # trúng đòn: sóng chạy từ ngọn về gốc
            P.rot(b, (6 + 2 * i) * cv(t, [(0, 0), (0.07 + 0.03 * (len(duoi) - 1 - i), 1, "out"), (0.35 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    def die_fn(t, P, D=1.6):
        P.rot("dau", cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 8), (0.8, -32, "io"), (D, -34)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 18, "out"), (0.3, 6), (0.8, 24, "io"), (D, 24)]))
        P.rot("nguc", cv(t, [(0, 0), (0.07, 6, "out"), (0.8, -10, "io"), (D, -10)]))
        P.rot("move", cv(t, [(0, 0), (0.85, 0), (1.22, 78, "in"), (1.32, 72, "out"), (D, 74)]))
        an_hien(P, "mi", t, [(0.04, D + 1)])
        a = cv(t, [(0, 1), (1.22, 1), (1.56, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
            if s["name"] == "mi":
                P.alpha["mi"] = a

    def aura_fn(t, P, D=2.0):
        u = 2 * math.pi * t / D
        P.move("bong", 170 * k * math.cos(u), 26 * k * math.sin(u))
        P.scale("bong", 0.9 + 0.12 * math.sin(u * 2), 0.9 + 0.12 * math.sin(u * 2))
        P.alpha["bong"] = 0.75 + 0.2 * math.sin(u)

    out = [Clip("appear", 1.2, appear_fn, mem=soft()),
           Clip("idle", 2.0, idle_fn, loop=True, mem=soft()),
           Clip("attack", 0.9, attack_fn, ev=[(0.42, "trung", "")], mem=soft()),
           Clip("cast", 1.0, cast_fn, ev=[(0.52, "phun", ""), (0.85, "het_phun", "")], mem=soft()),
           Clip("skill", 1.8, skill_fn, ev=[(0.66, "gam", ""), (1.3, "het_gam", "")], mem=soft()),
           Clip("hit", 0.6, hit_fn, mem=soft()),
           Clip("die", 1.6, die_fn, mem=soft()),
           Clip("aura", 2.0, aura_fn, loop=True)]
    return out


def uon_thu(sk, info, ra):
    """ảnh uốn thử: đuôi mỗi đốt 22°, chân gối 40°, đầu 20°, hàm há 32°: soi lưới cong trơn, không gập ở khớp."""
    P = khung.Pose()
    for b in info["duoi"]:
        P.rot(b, 22)
    for s, names in info["legs"].items():
        P.rot(names[0], 25)
        P.rot(names[1], -45)
    P.rot("dau", 20)
    P.rot("ham", -32)
    for b in info["tay"]:
        P.rot(b, 30)
    for b in info["rau"]:
        P.rot(b, -15)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


def main():
    t0 = time.time()
    # dạng 2 trước (dạng 1 cần idle khung 0 của dạng 2 để làm tiến hóa)
    sk2, info2 = dung(2)
    cl2 = clips(sk2, info2, 2)
    fr2 = {c.ten: hoat.nuong(sk2, c) for c in cl2}
    print(f"dạng 2: nướng {len(cl2)} clip ({time.time() - t0:.1f} s)")
    t2 = xuat.xuat_het(sk2, cl2, os.path.join(RA, "dang_2"), "vi_du_2", "Con thử dạng 2", frames=fr2, dang=2, so_dang=2, ma_goc=3211,
                       can=[("can_mieng_skill", "skill", 0.9, "ham", 70)])
    uon_thu(sk2, info2, os.path.join(RA, "dang_2", "uon_thu.png"))
    # dạng 1 + gộp dạng 2 (tiến hóa)
    sk1, info1 = dung(1)
    cl1 = clips(sk1, info1, 1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0]), soi.chieu_cao(ve2, fr2["idle"][0])
    M = tienhoa.gop(sk1, sk2)

    def gong(t, P):   # dạng cũ gồng, ngửa đầu
        sq = cv(t, [(0, 0), (0.3, -0.07), (0.45, 0.06, "out"), (1.0, 0.04), (1.3, 0.0)])
        P.scale("move", 1 - 0.5 * sq, 1 + sq)
        P.rot("dau", cv(t, [(0, 0), (0.3, -6), (0.6, 14, "out"), (1.3, 16)]) + 1.5 * rung(t, 0.5, 1.3))

    def gam(t, P, fl):  # dạng sau gầm
        P.rot("n_dau", 14 * fl)
        P.rot("n_ham", -34 * fl)
        P.scale("n_move", 1 + 0.05 * fl, 1 + 0.05 * fl)

    memM = cl1[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    aura = tienhoa.gop_aura(cl1[-1], cl2[-1])
    clM = [c for c in cl1 if c.ten != "aura"] + [ev, aura]
    frM = {c.ten: fr1[c.ten] for c in cl1 if c.ten != "aura"}
    frM["evolve"] = hoat.nuong(M, ev)
    frM["aura"] = hoat.nuong(M, aura)
    _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
    t1 = xuat.xuat_het(M, clM, os.path.join(RA, "dang_1"), "vi_du_1", "Con thử dạng 1 (gộp tiến hóa)", frames=frM, dang=1, so_dang=2,
                       ma_goc=3211, noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"}, can=[("can_mieng_cast", "cast", 0.62, "ham", 70), ("can_co_attack", "attack", 0.42, "nguc", 90),
                                         ("can_duoi_hit", "hit", 0.1, "duoi2", 110), ("can_mi_hit", "hit", 0.1, "dau", 70)])
    uon_thu(sk1, info1, os.path.join(RA, "dang_1", "uon_thu.png"))
    print(f"xong {time.time() - t0:.1f} s; dạng 1 {t1['atomik_kb']:.0f} KB, dạng 2 {t2['atomik_kb']:.0f} KB")


if __name__ == "__main__":
    main()
