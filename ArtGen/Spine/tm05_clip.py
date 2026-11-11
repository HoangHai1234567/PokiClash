# -*- coding: utf-8 -*-
"""Clip của dòng tm05 (Sò Ngọc) và lệnh xuất. Gọi từ tm05.py rig <k>.

Nhịp học từ con gốc monster_3237 (inbox/tm05_ghichu.md): idle 4 s, thân nghiêng chu kỳ 1,33 s, vỏ trên khép mở nhẹ có điểm phá
nhịp "lập cập" giữa vòng, đòn sập vỏ trong 1 khung. Thêm: gai mỗi cái lò xo, môi lượn sóng, xúc tu / chân lệch pha, mắt chớp.
Dạng 2 lấy đà dài hơn, chiêu dữ hơn, đòn đứng tại chỗ (attack trong dung_yen).
"""
import math
import os
import time

import numpy as np

import tm05
from quai import hoat, khung, soi, tienhoa, xuat
from quai.hoat import Clip, LoXo, an_hien, bao, chuoi_song, cv, ease, lui, rung, song

TEN = {1: "Sò Gai", 2: "Bạng Vương"}


def goc(v):
    return math.degrees(math.atan2(v[1], v[0]))


def goc_khep(info):
    c = tm05.CFG[info["k"]]
    R, H = info["R"], info["H"]
    return goc(R(*c["U"][-1]) - H) - goc(R(*c["D"][-1]) - H)


def ba(names, prof):
    """biên độ theo số đốt: nội suy hồ sơ prof (gốc → ngọn) cho đúng số đốt của chuỗi."""
    prof = np.asarray(prof, float)
    return np.interp(np.linspace(0, 1, len(names)), np.linspace(0, 1, len(prof)), prof)


def bam_dat(sk, P, names, dich, lan=4, he=0.55, gioi=28.0):
    """CCD: xoay các đốt chuỗi (gốc → ngọn) cho ngọn đốt cuối chạm đích (thế giới rig). Gọi cuối hàm đặt dáng."""
    tip_b = names[-1]
    ln = sk.bones[sk.bi[tip_b]]["length"]
    T = np.asarray(dich, float)
    W = sk.the_gioi(P)
    for _ in range(lan):
        for j in range(len(names) - 1, -1, -1):
            b = names[j]
            J = W[b][:2, 2]
            tip = (W[tip_b] @ np.array([ln, 0, 1.0]))[:2]
            a1, a2 = goc(tip - J), goc(T - J)
            d = ((a2 - a1 + 180) % 360 - 180) * he
            d = max(-gioi, min(gioi, d))
            par = sk.bones[sk.bi[b]]["parent"]
            sg = 1.0 if par is None or np.linalg.det(W[par][:2, :2]) > 0 else -1.0
            P.rot(b, d * sg)
            sk.cap_nhat(W, names[j:], P)
    return W


def clips(sk, info):
    k = info["k"]
    gai, mt, md, lu, ch = info["gai"], info["mt"], info["md"], info["luoi"], info["chains"]
    kh = goc_khep(info)
    S = tm05.CFG[k]["S"] / 0.45            # quy đổi biên độ dời theo cỡ rig
    legs = {n: v for n, v in ch.items() if n.startswith("c")}
    xts = {n: v for n, v in ch.items() if n.startswith("x")}
    foot = info["foot"]
    print(f"  dạng {k}: góc khép {kh:.1f}°, {len(gai)} gai, {len(legs)} chân, {len(xts)} xúc tu")

    mem = [LoXo([g], k=[230 if k == 2 else 300], damp=0.45, maxang=11) for g in gai]
    for n, v in xts.items():
        mem.append(LoXo(v, k=list(ba(v, [280, 200, 140])), damp=0.5, maxang=18))
    if k == 2:
        mem.append(LoXo(["mien"], k=[260], damp=0.45, maxang=10))

    def cham(P, lift=None):
        """giữ ngọn chân / xúc tu chân bám đất (theo xương move); lift {chân: (dx, dy)} nhấc chân."""
        if not legs:
            return
        W = sk.the_gioi(P)
        for n, names in legs.items():
            f = foot[n]
            d = (lift or {}).get(n, (0.0, 0.0))
            tg = (W["move"] @ np.array([f[0] + d[0], f[1] + d[1], 1.0]))[:2]
            bam_dat(sk, P, names, tg, lan=3)

    def nen(P, tt, amp=1.0):
        """chuyển động nền của idle ở giờ tt (vòng 4 s)."""
        if k == 2:
            P.move("than", 0, 3.2 * S * song(tt, 2.0) * amp)
            P.rot("than", 1.1 * song(tt, 4.0, 0.6) * amp)
            P.rot("vo_tren", (1.4 + 1.4 * song(tt, 2.0, -0.9)) * amp)
            P.rot("vo_duoi", -0.5 * (1 + song(tt, 2.0, -0.9)) * amp)
            P.scale("mat", 1.0, 1 + 0.02 * song(tt, 2.0, -0.5) * amp)
            for i, (n, names) in enumerate(legs.items()):
                chuoi_song(P, names, tt, 4.0, ba(names, [2.0, 2.6, 3.0, 2.6, 2.0]) * amp, tre=0.15, ngon_dan=False, pha=1.3 * i)
            if lu:
                chuoi_song(P, lu, tt, 2.0, np.array([1.2, 2.0, 3.0]) * amp, tre=0.12, ngon_dan=False)
            P.move("ngoc", 2.6 * S * song(tt, 4.0, 1.0) * amp, 0)
            P.rot("ngoc", -9 * song(tt, 4.0, 1.0) * amp)
        else:
            P.rot("than", 4.0 * song(tt, 4 / 3.0) * amp)
            P.move("than", 0, 2.2 * S * song(tt, 2 / 3.0, 0.5) * amp)
            P.scale("than", 1 + 0.012 * song(tt, 2 / 3.0, 2.0) * amp, 1 - 0.018 * song(tt, 2 / 3.0, 2.0) * amp)
            P.rot("vo_tren", (1.0 + 1.0 * song(tt, 2.0, -0.7)) * amp)
            P.rot("vo_duoi", -0.4 * (1 + song(tt, 2.0, -0.7)) * amp)
            for n, names in legs.items():
                chuoi_song(P, names, tt, 4 / 3.0, ba(names, [2.0, 3.0, 4.0, 4.0]) * amp, tre=0.1, ngon_dan=False)
            P.move("ngoc", 1.5 * S * song(tt, 2.0, 0.3) * amp, 0)
            P.rot("ngoc", -6 * song(tt, 2.0, 0.3) * amp)
        chuoi_song(P, mt, tt, 4 / 3.0, ba(mt, [1.2, 2.2, 2.8, 2.8]) * amp, tre=0.12)
        chuoi_song(P, md, tt, 4 / 3.0, ba(md, [1.0, 1.8, 2.4, 2.4]) * amp, tre=0.12, pha=1.7)
        for i, (n, names) in enumerate(xts.items()):
            chuoi_song(P, names, tt, 2.0, ba(names, [4.0, 7.0, 10.0]) * amp, tre=0.14, pha=0.9 * i)
        for i, g in enumerate(gai):
            P.rot(g, 1.4 * song(tt, 2.0, 0.8 * i) * amp)

    def nb(P, t, D, amp=1.0):
        """nền idle cho clip không lặp: hoà từ giờ t (khung 0 trùng idle khung 0) sang giờ t - D (khung cuối trùng idle khung 0)."""
        w = ease(t / D, "io")
        nen(P, t, amp * (1 - w))
        nen(P, t - D, amp * w)

    def khep(P, f):
        """khép vỏ: f = 1 khép kín (tính theo góc mở dáng gốc)."""
        P.rot("vo_tren", -0.8 * kh * f)
        P.rot("vo_duoi", 0.2 * kh * f)

    def mo(P, deg):
        P.rot("vo_tren", deg)
        P.rot("vo_duoi", -0.3 * deg)

    def mi(P, t, khoang):
        an_hien(P, "mi_a", t, khoang)
        an_hien(P, "mi_b", t, khoang)

    def ae(P, a):
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a

    # ---------------------------------------------------------------- idle
    D_IDLE = 4.0

    def idle_fn(t, P):
        nen(P, t)
        if k == 2:   # lập cập vỏ giữa vòng, chớp mắt một lần, chớp đôi
            khep(P, cv(t, [(0, 0), (2.45, 0), (2.53, 0.28), (2.61, 0.03), (2.69, 0.24), (2.77, 0.03), (2.85, 0.16), (2.97, 0, "io"), (4, 0)]))
            mi(P, t, [(1.20, 1.32), (3.30, 3.39), (3.49, 3.58)])
        else:
            khep(P, cv(t, [(0, 0), (1.70, 0), (1.78, 0.32), (1.86, 0.02), (1.94, 0.36), (2.02, 0.04), (2.10, 0.28), (2.23, 0, "io"), (4, 0)]))
            mi(P, t, [(2.90, 3.02), (0.62, 0.72)])
        cham(P)

    # ---------------------------------------------------------------- appear
    def appear_fn(t, P):
        if k == 2:
            D = 1.8
            ae(P, cv(t, [(0, 0), (0.16, 1)]))
            nb(P, t, D, ease((t - 1.1) / 0.6))
            rise = cv(t, [(0, 1), (0.15, 1), (0.95, 0, "out"), (D, 0)])
            P.move("than", 0, -95 * S * rise)
            P.scale("than", 1 - 0.18 * rise, 1 - 0.18 * rise)
            khep(P, cv(t, [(0, 1), (0.85, 1), (1.05, -0.2, "out"), (1.45, 0, "io"), (D, 0)]))
            mo(P, 14 * cv(t, [(0, 0), (0.95, 0), (1.1, 1, "out"), (1.4, 0.4, "io"), (D, 0, "io")]))
            for i, g in enumerate(gai):
                P.scale(g, 1 + 0.18 * bao(t, 1.0, 1.5, 0.08, 0.3), 1)
            lift = {}
            for i, n in enumerate(legs):
                u = ease((t - (0.15 + 0.14 * i)) / 0.35, "out")
                f = foot[n]
                lift[n] = ((0 - f[0]) * 0.55 * (1 - u), (60 * S - f[1]) * (1 - u) * 0.9)
            mi(P, t, [(0, 0.95), (1.5, 1.6)])
            P.alpha["mi_a"] *= cv(t, [(0, 0), (0.16, 1)])
            P.alpha["mi_b"] *= cv(t, [(0, 0), (0.16, 1)])
            cham(P, lift)
        else:
            D = 1.3
            ae(P, cv(t, [(0, 0), (0.1, 1)]))
            nb(P, t, D, ease((t - 0.8) / 0.5))
            P.move("move", 0, cv(t, [(0, 190 * S), (0.32, 0, "in"), (D, 0)]))
            sq = cv(t, [(0, 0), (0.32, 0), (0.4, 1, "out"), (0.55, -0.45, "io"), (0.72, 0.15, "io"), (0.9, 0, "io"), (D, 0)])
            P.scale("move", 1 + 0.16 * sq, 1 - 0.2 * sq)
            khep(P, cv(t, [(0, 1), (0.55, 1), (0.66, -0.25, "out"), (0.85, 0, "io"), (D, 0)]))
            mi(P, t, [(0.92, 1.02)])
            cham(P)

    # ---------------------------------------------------------------- attack
    def attack_fn(t, P):
        if k == 2:
            D, Hh = 1.3, 0.5
            nb(P, t, D, 1 - 0.75 * bao(t, 0.05, 1.2, 0.2, 0.3))
            lean = cv(t, [(0, 0), (0.32, 1, "io"), (0.44, 1.07), (Hh, -1.0, "in"), (0.56, -1.12), (0.86, -0.92, "io"), (D, 0, "io")])
            P.rot("than", 7 * lean)
            P.move("than", cv(t, [(0, 0), (0.32, -10 * S, "io"), (Hh, 14 * S, "in"), (0.86, 11 * S), (D, 0, "io")]), -2 * S * abs(lean))
            mo(P, cv(t, [(0, 0), (0.32, 12, "io"), (0.45, 14), (Hh, 0, "in"), (D, 0)]))
            khep(P, cv(t, [(0, 0), (0.45, 0), (Hh, 1.0, "in"), (0.56, 0.96), (0.86, 0.85, "io"), (D, 0, "io")]))
            P.scale("vo_tren", cv(t, [(0, 1), (0.47, 1), (Hh, 1.07), (0.56, 0.98), (0.7, 1), (D, 1)]),
                    cv(t, [(0, 1), (0.47, 1), (Hh, 0.95), (0.56, 1.02), (0.7, 1), (D, 1)]))
            if lu:
                P.move(lu[0], -16 * S * cv(t, [(0, 0), (0.4, 0), (Hh, 1, "in"), (0.86, 1), (D, 0, "io")]), 0)
            P.move("ngoc", -10 * S * cv(t, [(0, 0), (0.4, 0), (Hh, 1, "in"), (0.86, 1), (D, 0, "io")]),
                   -6 * S * cv(t, [(0, 0), (0.4, 0), (Hh, 1, "in"), (0.86, 1), (D, 0, "io")]))
            P.rot("mat", -4 * bao(t, 0.3, 0.9, 0.1, 0.2))
            cham(P)
        else:
            D, Hh = 1.0, 0.45
            nb(P, t, D, 1 - 0.8 * bao(t, 0.05, 0.95, 0.15, 0.25))
            sq = cv(t, [(0, 0), (0.24, 1, "io"), (0.3, -0.5, "out"), (0.4, -0.2), (Hh, 0.9, "in"), (0.55, -0.15, "io"), (0.7, 0, "io"), (D, 0)])
            P.scale("move", 1 + 0.08 * sq, 1 - 0.1 * sq)
            P.move("move", cv(t, [(0, 0), (0.24, -8 * S, "io"), (0.42, 22 * S, "out"), (0.6, 18 * S), (D, 0, "io")]),
                   cv(t, [(0, 0), (0.28, 0), (0.36, 24 * S, "out"), (Hh, 0, "in"), (D, 0)]))
            P.rot("than", cv(t, [(0, 0), (0.24, 6, "io"), (Hh, -7, "in"), (0.6, -5), (D, 0, "io")]))
            mo(P, cv(t, [(0, 0), (0.24, 10, "io"), (0.4, 14), (Hh, 0, "in"), (D, 0)]))
            khep(P, cv(t, [(0, 0), (0.4, 0), (Hh, 1.0, "in"), (0.52, 0.95), (0.75, 0.82, "io"), (D, 0, "io")]))
            cham(P)

    # ---------------------------------------------------------------- cast
    def cast_fn(t, P):
        if k == 2:
            D, Hh, E = 1.7, 0.62, 1.3
            nb(P, t, D, 1 - 0.8 * bao(t, 0.05, 1.6, 0.2, 0.3))
            rear = cv(t, [(0, 0), (0.45, 1, "io"), (0.56, 1.05), (Hh, -0.5, "in"), (0.7, -0.6), (E, -0.5), (D, 0, "io")])
            P.rot("than", 5 * rear + 1.0 * rung(t, Hh + 0.04, E))
            P.move("than", cv(t, [(0, 0), (Hh, 0), (0.7, -8 * S, "out"), (E, -6 * S), (D, 0, "io")]), 0)
            mo(P, cv(t, [(0, 0), (0.45, 10, "io"), (Hh, 17, "out"), (E, 15), (D, 0, "io")]) + 1.4 * rung(t, Hh + 0.04, E))
            push = cv(t, [(0, 0), (0.4, 0), (Hh, 1, "out"), (E, 0.9), (D, 0, "io")])
            if lu:
                P.move(lu[0], 14 * S * push, 2 * S * push)
                P.rot(lu[1], -6 * push)
                P.rot(lu[2], 8 * push)
            P.move("ngoc", 12 * S * push, 6 * S * push)
            P.rot("ngoc", -20 * push)
            P.scale("mat", 1 + 0.03 * push, 1 - 0.04 * push)
            cham(P)
        else:
            D, Hh, E = 1.2, 0.55, 0.95
            nb(P, t, D, 1 - 0.8 * bao(t, 0.05, 1.1, 0.15, 0.25))
            rear = cv(t, [(0, 0), (0.4, 1, "io"), (0.5, 1.05), (Hh, -0.6, "in"), (0.62, -0.7), (E, -0.6), (D, 0, "io")])
            P.rot("than", 6 * rear + 1.0 * rung(t, Hh + 0.04, E))
            P.move("move", cv(t, [(0, 0), (Hh, 0), (0.62, -7 * S, "out"), (E, -5 * S), (D, 0, "io")]), 0)
            mo(P, cv(t, [(0, 0), (0.4, 9, "io"), (Hh, 16, "out"), (E, 14), (D, 0, "io")]) + 1.2 * rung(t, Hh + 0.04, E))
            push = cv(t, [(0, 0), (0.4, 0), (Hh, 1, "out"), (E, 0.9), (D, 0, "io")])
            P.move("ngoc", 9 * S * push, 4 * S * push)
            P.scale("move", 1 - 0.04 * max(rear, 0), 1 + 0.05 * max(rear, 0))
            cham(P)

    # ---------------------------------------------------------------- skill
    def skill_fn(t, P):
        if k == 2:
            D, Hh, E = 2.6, 1.15, 2.0
            nb(P, t, D, 1 - 0.85 * bao(t, 0.05, 2.5, 0.2, 0.4))
            khep(P, cv(t, [(0, 0), (0.3, 1, "io"), (1.02, 1), (1.12, -0.1, "out"), (D, 0)]))
            mo(P, cv(t, [(0, 0), (1.02, 0), (1.12, 24, "out"), (E, 21), (D, 0, "io")]) + 2.0 * rung(t, Hh, E))
            cr = cv(t, [(0, 0), (0.45, 1, "io"), (0.95, 1), (1.1, -0.6, "out"), (1.3, -0.3, "io"), (E, -0.3), (D, 0, "io")])
            P.move("than", 2.0 * S * rung(t, 0.35, 0.95), -14 * S * max(cr, 0) + 10 * S * max(-cr, 0))
            P.scale("than", 1 + 0.05 * max(cr, 0) - 0.03 * max(-cr, 0), 1 - 0.07 * max(cr, 0) + 0.06 * max(-cr, 0))
            P.rot("than", 1.6 * rung(t, 0.35, 0.95) + 1.2 * rung(t, Hh, E) - 4 * max(-cr, 0))
            fl = bao(t, 1.04, E + 0.2, 0.08, 0.35)
            for i, g in enumerate(gai):
                P.rot(g, (10 if i < 5 else 8) * fl * (1 if i % 2 else -1) * 0.6 + 6 * fl)
                P.scale(g, 1 + 0.16 * fl, 1)
            up = cv(t, [(0, 0), (0.68, 0), (0.86, 1, "out"), (1.0, 0, "in"), (D, 0)])
            lift = {n: (0.0, 48 * S * up) for n in legs if n in ("cft", "cfs")}
            mi(P, t, [(0.3, 0.98)])
            P.rot("mat", -5 * bao(t, 1.05, E, 0.08, 0.3))
            cham(P, lift)
        else:
            D, Hh, E = 1.9, 0.85, 1.4
            nb(P, t, D, 1 - 0.85 * bao(t, 0.05, 1.8, 0.15, 0.35))
            khep(P, cv(t, [(0, 0), (0.25, 1, "io"), (0.8, 1), (Hh, -0.1, "out"), (D, 0)]))
            mo(P, cv(t, [(0, 0), (0.8, 0), (Hh, 15, "out"), (E, 12), (D, 0, "io")]) + 1.4 * rung(t, Hh, E))
            br = bao(t, 0.15, 1.5, 0.3, 0.3)
            fl = bao(t, 0.82, 1.5, 0.06, 0.3)
            for i, g in enumerate(gai):
                P.scale(g, 1 + 0.2 * br, 1 + 0.06 * br)
                P.rot(g, 2.0 * rung(t, 0.2, 0.62) + 12 * fl * (1 if i % 2 else -1) * 0.5)
            sq = cv(t, [(0, 0), (0.55, 1, "io"), (0.62, 1.05), (0.72, -0.9, "out"), (0.85, -0.6), (1.08, 0, "in"), (1.14, 0.9, "out"),
                        (1.3, -0.2, "io"), (1.5, 0, "io"), (D, 0)])
            P.scale("move", 1 + 0.1 * sq, 1 - 0.13 * sq)
            P.move("move", 1.8 * S * rung(t, 0.2, 0.6), cv(t, [(0, 0), (0.62, 0), (0.85, 72 * S, "out"), (1.08, 0, "in"), (D, 0)]))
            P.rot("than", 1.4 * rung(t, 0.2, 0.6) + 1.2 * rung(t, Hh + 0.3, E))
            mi(P, t, [(0.25, 0.8)])
            cham(P)

    # ---------------------------------------------------------------- hit
    def hit_fn(t, P):
        D = 0.7 if k == 2 else 0.6
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        nb(P, t, D, 1 - 0.7 * bao(t, 0.0, D, 0.04, 0.3))
        P.rot("than", (6 if k == 2 else 9) * hd)
        P.move("than" if k == 2 else "move", -12 * S * bd, 0)
        khep(P, 0.45 * hd)
        P.scale("mat", 1 - 0.05 * hd, 1 - 0.08 * hd)
        mi(P, t, [(0.03, 0.36)])
        for i, g in enumerate(gai):
            P.rot(g, 7 * cv(t, [(0, 0), (0.07 + 0.01 * i, 1, "out"), (0.3, -0.4, "io"), (D, 0, "io")]))
        for j, (n, names) in enumerate(legs.items()):
            for i, b in enumerate(names):   # sóng chạy từ ngọn về gốc
                P.rot(b, (2 + i) * cv(t, [(0, 0), (0.07 + 0.03 * (len(names) - 1 - i), 1, "out"), (0.35 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))
        cham(P)

    # ---------------------------------------------------------------- die
    def die_fn(t, P):
        nen(P, t, 1 - ease(t / 0.45))
        if k == 2:
            D = 2.6
            P.rot("than", cv(t, [(0, 0), (0.07, 8, "out"), (0.3, 3), (0.9, -4, "io"), (1.5, -3), (1.9, 14, "in"), (2.05, 11, "out"), (D, 12)])
                  + 2.5 * math.sin(2 * math.pi * (t - 0.9) / 0.6) * bao(t, 0.9, 1.5, 0.1, 0.15))
            mo(P, cv(t, [(0, 0), (0.07, -6, "out"), (0.3, 0), (0.9, 18, "io"), (D, 20)]))
            P.move("than", cv(t, [(0, 0), (0.5, 0), (1.2, -10 * S, "io"), (1.9, -40 * S, "in"), (2.05, -34 * S, "out"), (D, -36 * S)]),
                   cv(t, [(0, 0), (0.5, 0), (1.2, -42 * S, "in"), (1.35, -36 * S, "out"), (1.9, -60 * S, "in"), (D, -60 * S)]))
            for i, b in enumerate(lu):
                P.rot(b, -cv(t, [(0, 0), (0.4, 0), (1.0, 10 + 6 * i, "io"), (D, 12 + 6 * i)]))
            P.move("ngoc", cv(t, [(0, 0), (0.8, 0), (1.5, 34 * S, "in"), (D, 40 * S)]), cv(t, [(0, 0), (0.8, 0), (1.5, -26 * S, "in"), (D, -30 * S)]))
            for n, names in xts.items():
                for i, b in enumerate(names):
                    P.rot(b, -cv(t, [(0, 0), (0.4, 0), (1.0, 14 + 8 * i, "io"), (D, 16 + 8 * i)]))
            mi(P, t, [(0.04, D + 1)])
            a = cv(t, [(0, 1), (1.95, 1), (2.45, 0, "io"), (D, 0)])
            ae(P, a)
            P.alpha["mi_a"] = P.alpha["mi_b"] = a if t >= 0.04 else 0.0
            cham(P)
        else:
            D = 2.0
            mo(P, cv(t, [(0, 0), (0.07, -5, "out"), (0.3, 0), (0.85, 18, "io"), (D, 20)]))
            P.rot("than", cv(t, [(0, 0), (0.07, 9, "out"), (0.3, 4)]) + 3 * math.sin(2 * math.pi * (t - 0.85) / 0.55) * bao(t, 0.85, 1.35, 0.1, 0.1))
            P.rot("move", cv(t, [(0, 0), (1.3, 0), (1.62, 62, "in"), (1.72, 56, "out"), (D, 58)]))
            P.move("move", cv(t, [(0, 0), (1.3, 0), (1.62, -30 * S, "in"), (D, -30 * S)]), 0)
            P.move("ngoc", cv(t, [(0, 0), (0.7, 0), (1.3, 22 * S, "in"), (D, 26 * S)]), cv(t, [(0, 0), (0.7, 0), (1.3, -16 * S, "in"), (D, -18 * S)]))
            for n, names in xts.items():
                for i, b in enumerate(names):
                    P.rot(b, -cv(t, [(0, 0), (0.4, 0), (1.0, 14 + 9 * i, "io"), (D, 16 + 9 * i)]))
            mi(P, t, [(0.04, D + 1)])
            a = cv(t, [(0, 1), (1.5, 1), (1.92, 0, "io"), (D, 0)])
            ae(P, a)
            P.alpha["mi_a"] = P.alpha["mi_b"] = a if t >= 0.04 else 0.0
            cham(P)

    out = [Clip("appear", 1.8 if k == 2 else 1.3, appear_fn, mem=mem),
           Clip("idle", D_IDLE, idle_fn, loop=True, mem=mem),
           Clip("attack", 1.3 if k == 2 else 1.0, attack_fn, ev=[(0.5 if k == 2 else 0.45, "trung", "")], mem=mem),
           Clip("cast", 1.7 if k == 2 else 1.2, cast_fn,
                ev=[(0.62, "phun", ""), (1.3, "het_phun", "")] if k == 2 else [(0.55, "phun", ""), (0.95, "het_phun", "")], mem=mem),
           Clip("skill", 2.6 if k == 2 else 1.9, skill_fn,
                ev=[(1.0, "dap", ""), (1.15, "gam", ""), (1.17, "song", ""), (2.0, "het_gam", "")] if k == 2
                else [(0.85, "gam", ""), (0.86, "gai", ""), (1.4, "het_gam", "")], mem=mem),
           Clip("hit", 0.7 if k == 2 else 0.6, hit_fn, mem=mem),
           Clip("die", 2.6 if k == 2 else 2.0, die_fn, mem=mem)]
    return out, {"khep": khep, "mo": mo, "nen": nen, "cham": cham, "mem": mem}


def xuong_mem(mem, tien_to=""):
    out = []
    for m in mem:
        out += [tien_to + b for b in m.bones]
    return out


def khop_dau(frames, dich, bones, giay=0.3, fps=30):
    """đầu clip không lặp: lò xo bắt đầu từ 0 còn idle khung 0 đã có độ lệch lò xo; cộng phần chênh (idle0 - khung 0) của các
    xương lò xo, tắt dần trong `giay` đầu: khung 0 trùng idle khung 0 mà động tác đầu clip (trúng đòn đỉnh 0,07 s) không bị nhoà."""
    m = max(1, int(round(giay * fps)))
    f0 = frames[0]
    for b in bones:
        a, c = f0.t.get(b, list(khung.ZERO)), dich.t.get(b, list(khung.ZERO))
        diff = [c[q] - a[q] for q in range(3)] + [c[3] / max(1e-9, a[3]), c[4] / max(1e-9, a[4])]
        if max(abs(diff[0]), abs(diff[1]), abs(diff[2]), abs(diff[3] - 1), abs(diff[4] - 1)) < 1e-6:
            continue
        for j in range(min(m + 1, len(frames))):
            w = 1 - ease(j / m)
            g = frames[j]._g(b)
            for q in range(3):
                g[q] += diff[q] * w
            g[3] *= 1 + (diff[3] - 1) * w
            g[4] *= 1 + (diff[4] - 1) * w


def noi_atomik(path, clips, idle_khac=None):
    """đo nối clip trên ĐỈNH LƯỚI tính từ dữ liệu .atomik (như runtime Unity, gồm lò xo đã nướng): khung 0 và khung cuối mỗi
    clip so với khung 0 idle. Trả dòng chữ cho báo cáo."""
    _, js, _ = xuat.doc_atomik(path)
    dur = {a["name"]: a["dur"] for a in js["anims"]}
    I0 = xuat.atomik_dinh(js, "idle", 0.0)

    def d(A, B):
        best, where = 0.0, ""
        for kname in set(A) | set(B):
            if kname not in A or kname not in B:
                return float("inf"), f"{kname} chỉ hiện ở một bên"
            if A[kname].shape != B[kname].shape:
                continue
            dd = float(np.hypot(*(A[kname] - B[kname]).T).max())
            if dd > best:
                best, where = dd, kname
        return best, where

    out = []
    for c in clips:
        if c not in dur or c in ("idle", "aura"):
            continue
        s = []
        if c != "appear":
            v, w = d(xuat.atomik_dinh(js, c, 0.0), I0)
            s.append(f"khung 0 lệch idle {v:.2f} px" + (f" ({w})" if v > 0.5 else ""))
        else:
            s.append("khung 0 trống" if not xuat.atomik_dinh(js, c, 0.0) else "khung 0 CÒN HIỆN")
        if c == "die":
            s.append("khung cuối trống" if not xuat.atomik_dinh(js, c, dur[c]) else "khung cuối CÒN HIỆN")
        elif c != "evolve":
            v, w = d(xuat.atomik_dinh(js, c, dur[c]), I0)
            s.append(f"khung cuối lệch idle {v:.2f} px" + (f" ({w})" if v > 0.5 else ""))
        out.append(f"{c}: " + "; ".join(s))
    A = xuat.atomik_dinh(js, "idle", 0.0)
    B = xuat.atomik_dinh(js, "idle", dur["idle"])
    v, w = d(A, B)
    out.append(f"idle: khung cuối lệch khung 0 {v:.2f} px")
    print("  NỐI CLIP (đỉnh lưới từ .atomik):\n    " + "\n    ".join(out))
    return out


def ghi_mat_do(sk, k, ra, ten, them=()):
    """mật độ lưới theo chiều cao con + hở từng mảnh, nối vào so_sanh.md."""
    bv, bt, cao = tm05.buoc(k)
    tt = sk.tom_tat()
    dong = [f"", f"## Mật độ lưới (đặc tả mục 5: tối thiểu viền 1,5%, trong 2% chiều cao; dòng này dùng 1,3% / 1,75%, dày hơn)", "",
            f"- Chiều cao con (concept × S): {cao:.0f} đơn vị rig; bước viền {bv:.1f}, bước trong {bt:.1f}.",
            f"- Tổng {tt['dinh']} đỉnh, {tt['tam_giac']} tam giác; {tt['dinh'] / cao:.1f} đỉnh trên mỗi đơn vị chiều cao.", "",
            "| Mảnh | Đỉnh | Tam giác | Hở (px) | Góc nhỏ TB |", "|---|---|---|---|---|"]
    ho_max = 0
    for (slot, nm), L in sk.luoi.items():
        tk = L.thong_ke() if hasattr(L, "thong_ke") else {}
        ho = getattr(L, "ho", 0) or 0
        ho_max = max(ho_max, ho)
        dong.append(f"| {slot} | {L.n} | {len(L.tris)} | {ho} | {round(tk.get('goc_tb', 0), 1)} |")
    dong.append("")
    dong.append(f"- Hở lớn nhất: {ho_max} px." + (" Mảnh cứng (gai, ngọc, mũ miện, mí) là region 4 đỉnh." if True else ""))
    dong += list(them)
    p = os.path.join(ra, "so_sanh.md")
    with open(p, "a", encoding="utf-8") as f:
        f.write("\n".join(dong) + "\n")
    print(f"  mật độ: {tt['dinh']} đỉnh / cao {cao:.0f}; hở lớn nhất {ho_max} px")


def uon_thu(sk, info, ra):
    """uốn thử: vỏ há thêm 20°, chân / xúc tu mỗi đốt 18°, môi 8°: soi lưới cong trơn, không gập ở khớp, màng lòng miệng phủ kín."""
    P = khung.Pose()
    P.rot("vo_tren", 20)
    P.rot("vo_duoi", -6)
    for n, names in info["chains"].items():
        for b in names:
            P.rot(b, 18 if n.startswith("x") else 10)
    for b in info["mt"] + info["md"]:
        P.rot(b, 8)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


def khep_thu(sk, info, ra):
    """khép thử: vỏ khép kín (lòng miệng, ngọc, lưỡi phải khuất hết)."""
    P = khung.Pose()
    kh = goc_khep(info)
    P.rot("vo_tren", -0.8 * kh)
    P.rot("vo_duoi", 0.2 * kh)
    if info["luoi"]:
        P.move(info["luoi"][0], -16 * tm05.CFG[info["k"]]["S"] / 0.45, 0)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2)
    a.convert("RGB").save(ra)
    return ra


def chay(k):
    t0 = time.time()
    if k == 2:
        sk, info = tm05.dung(2)
        cl, _ = clips(sk, info)
        fr = {c.ten: hoat.nuong(sk, c) for c in cl}
        mb = xuong_mem(next(c for c in cl if c.ten == "idle").mem)
        for c in cl:
            if not c.loop:
                khop_dau(fr[c.ten], fr["idle"][0], mb)
        print(f"dạng 2: nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
        ra = tm05.thu_muc(2, "rig")
        tong = xuat.xuat_het(sk, cl, ra, "tm05_2", "Sò Ngọc dạng 2: Bạng Vương", frames=fr, dang=2, so_dang=2,
                             dung_yen=("attack", "cast", "skill"), ma_goc=3237,
                             can=[("can_mieng_cast", "cast", 0.75, "ngoc", 95), ("can_mieng_skill", "skill", 1.3, "vo_tren", 130),
                                  ("can_khep_attack", "attack", 0.52, "vo_tren", 130), ("can_mi_hit", "hit", 0.12, "mat", 60),
                                  ("can_chan_skill", "skill", 0.86, "cft2", 90), ("can_gai_skill", "skill", 1.2, "gt2", 110)])
        uon_thu(sk, info, os.path.join(ra, "uon_thu.png"))
        khep_thu(sk, info, os.path.join(ra, "khep_thu.png"))
        tong["noi_atomik"] = noi_atomik(os.path.join(ra, "tm05_2.atomik"), [c.ten for c in cl])
        tong["iou"] = tm05.so_concept(2, sk, fr["idle"][0], ra)
        ghi_mat_do(sk, 2, ra, "tm05_2", ["", "## Nối clip trên đỉnh lưới (.atomik)", ""] + [f"- {x}" for x in tong["noi_atomik"]]
                   + ["", f"IoU mặt nạ khung 0 idle với concept: {tong['iou']:.3f} (so_concept.png)."])
        print(f"xong dạng 2 {time.time() - t0:.1f} s; {tong.get('atomik_kb', 0):.0f} KB")
        return tong
    # dạng 1 + gộp dạng 2 (tiến hóa)
    sk2, info2 = tm05.dung(2)
    cl2, h2 = clips(sk2, info2)
    idle2 = next(c for c in cl2 if c.ten == "idle")
    idle2_0 = hoat.nuong(sk2, idle2)[0]
    sk1, info1 = tm05.dung(1)
    cl1, h1 = clips(sk1, info1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    mb1 = xuong_mem(h1["mem"])
    for c in cl1:
        if not c.loop:
            khop_dau(fr1[c.ten], fr1["idle"][0], mb1)
    print(f"dạng 1: nướng {len(cl1)} clip ({time.time() - t0:.1f} s)")
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0]), soi.chieu_cao(ve2, idle2_0)
    M = tienhoa.gop(sk1, sk2)
    kh1 = goc_khep(info1)

    def gong(t, P):   # dạng 1 khép chặt vỏ, xù gai, run lên (khung 0 = idle khung 0 dạng 1)
        h1["nen"](P, t, 1 - ease(t / 0.6))
        f = cv(t, [(0, 0), (0.3, 1, "io"), (1.3, 1)])
        P.rot("vo_tren", -0.8 * kh1 * f)
        P.rot("vo_duoi", 0.2 * kh1 * f)
        sq = cv(t, [(0, 0), (0.3, 0.6, "io"), (0.6, 1.0), (1.3, 1.0)])
        P.scale("move", 1 + 0.08 * sq, 1 - 0.1 * sq)
        P.rot("than", 2.0 * rung(t, 0.35, 1.3))
        for g in info1["gai"]:
            P.scale(g, 1 + 0.25 * sq, 1)
        an_hien(P, "mi_a", t, [(0.3, 1.4)])
        an_hien(P, "mi_b", t, [(0.3, 1.4)])
        h1["cham"](P)

    def gam(t, P, fl):  # dạng 2 há hàm gầm
        P.rot("n_vo_tren", 16 * fl)
        P.rot("n_vo_duoi", -5 * fl)
        P.scale("n_than", 1 + 0.04 * fl, 1 + 0.04 * fl)
        for g in info2["gai"]:
            P.rot("n_" + g, 7 * fl)

    memM = h1["mem"] + tienhoa.doi_ten_mem(h2["mem"])
    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, idle2_0, tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    clM = cl1 + [ev]
    frM = dict(fr1)
    frM["evolve"] = hoat.nuong(M, ev)
    khop_dau(frM["evolve"], fr1["idle"][0], mb1)
    _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, idle2_0, hA / hB)
    ra = tm05.thu_muc(1, "rig")
    tong = xuat.xuat_het(M, clM, ra, "tm05_1", "Sò Ngọc dạng 1: Sò Gai (gộp tiến hóa)", frames=frM, dang=1, so_dang=2, ma_goc=3237,
                         noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                         can=[("can_mieng_cast", "cast", 0.65, "ngoc", 80), ("can_khep_attack", "attack", 0.47, "vo_tren", 110),
                              ("can_mi_hit", "hit", 0.12, "mat", 60), ("can_gai_skill", "skill", 0.9, "gt2", 90),
                              ("can_rau_hit", "hit", 0.1, "xt_b1", 70)])
    uon_thu(sk1, info1, os.path.join(ra, "uon_thu.png"))
    khep_thu(sk1, info1, os.path.join(ra, "khep_thu.png"))
    tong["noi_atomik"] = noi_atomik(os.path.join(ra, "tm05_1.atomik"), [c.ten for c in clM])
    tong["iou"] = tm05.so_concept(1, sk1, fr1["idle"][0], ra)
    ghi_mat_do(sk1, 1, ra, "tm05_1", ["", "## Nối clip trên đỉnh lưới (.atomik)", ""] + [f"- {x}" for x in tong["noi_atomik"]]
               + ["", f"IoU mặt nạ khung 0 idle với concept: {tong['iou']:.3f} (so_concept.png).",
                  "Rig dạng 1 là rig gộp tiến hóa (gồm cả dạng 2 ẩn): số đỉnh tổng gồm cả dạng 2."])
    print(f"xong dạng 1 {time.time() - t0:.1f} s; {tong.get('atomik_kb', 0):.0f} KB")
    return tong
