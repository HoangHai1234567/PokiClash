# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của Thạch Giáp DẠNG 2 (cong_da2_rig.py, rig monster_3528): rig thật + VFX tạm bằng hạt của tho5_fx.py (KHÔNG sửa
tho5_fx.py). Giống ý dạng 1, mạnh hơn: chiêu mana ba cụm pha lê găm (mỗi cú nổ to hơn sỏi), chiêu cuối mưa pha lê dày hơn + ba mảnh to.

    py -3 -I ArtGen/Spine/tho5_fx_cong_da2.py [cast|skill|attack|all]   → inbox/tho5_fx/cong_da2_<clip>.gif (+ _soi.png)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
import numpy as np  # noqa: E402
import fxlib as fx  # noqa: E402
import tho5_fx as F  # noqa: E402
from tho5_fx import bui, dam_da, vong_dat, manh_pha_le, cham_no, FOE_C, AMBER, DA  # noqa: E402


def mau_phach(r):
    return AMBER[r.randint(2)] if r.uniform() < 0.6 else DA[r.randint(3)]


def cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]

    def rung(s, x):                                              # lắc núi đá: bụi, dăm nhỏ rơi khỏi mai
        p = T.diem(tt(s.t), "tam") + s.rng.uniform(-45, 45, 2) * np.array([1.0, 0.6])
        bui(s, p, vel=np.array([s.rng.uniform(-30, 30), s.rng.uniform(-20, 20)]), r0=5, r1=12, life=0.5)
        if s.rng.uniform() < 0.6:
            dam_da(s, p, np.array([s.rng.uniform(-110, 110), s.rng.uniform(-170, -60)]), size=3.5, ground=fx.ME[1] + 4)
    sim.every(R.T_LAC0, R.T_LAC1 + 0.04, 50, rung)
    for k in R.BAY_MANH:
        t0, t1 = R.T_PHONG[k], R.T_PHONG[k] + R.BAY
        sim.at(t0, lambda s, k=k: bui(s, T.diem(tt(R.T_PHONG[k]), f"fly_{k}"), r0=6, r1=15, life=0.45))
        sim.at(t1, lambda s, k=k: cham_no(s, FOE_C + s.rng.uniform(-14, 14, 2), 1.3 if k != "c" else 0.9, mau_dam=mau_phach))
    sim.at(R.T_DAP_C, lambda s: (vong_dat(s, fx.ME + np.array([0, 2.0]), 90), [bui(s, fx.ME + np.array([d * 50.0, -4.0]),
                                 vel=np.array([d * 80.0, -20.0]), r0=9, r1=24) for d in (-1, 1)], s.shake(0.12)))


def skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]

    def gong(s, x):                                              # gồng: bụi dưới chân, sỏi nảy
        p = fx.ME + np.array([s.rng.uniform(-75, 75), -2.0])
        bui(s, p, vel=np.array([s.rng.uniform(-50, 50), -15.0]), r0=6, r1=14, life=0.5, group=fx.BACK)
    sim.every(R.T_GONG0, R.T_GONG1, 28, gong)
    sim.at(R.T_GONG0, lambda s: s.shake(0.08))

    def ban(s):                                                  # pha lê vọt lên: nhiều vệt mảnh pha lê, bụi bung ở hốc
        goc = T.diem(tt(R.T_BAN_TROI), "pha_le")
        for i in range(9):
            manh_pha_le(s, goc + np.array([s.rng.uniform(-24, 24), 0.0]), np.array([s.rng.uniform(-80, 80), -1100.0 - 110 * i]),
                        L=24, Wd=9, life=0.5)
        for i in range(6):
            bui(s, goc + s.rng.uniform(-26, 26, 2), vel=np.array([s.rng.uniform(-90, 90), s.rng.uniform(-60, -20)]), r0=8, r1=20)
        vong_dat(s, fx.ME + np.array([0, 2.0]), 100)
        s.shake(0.2)
    sim.at(R.T_BAN_TROI, ban)
    xs = [-40, 26, -12, 40, -30, 10, 34, -20, 18, -36, 4]        # mưa: 11 mảnh nhỏ so le
    for i, dx in enumerate(xs):
        def roi(s, dx=dx):
            p0 = FOE_C + np.array([dx + 70.0, -300.0])
            manh_pha_le(s, p0, np.array([-230.0, 1050.0]), L=26, Wd=10, life=0.6, y_cham=FOE_C[1] + s.rng.uniform(-30, 25),
                        on_hit=lambda q, s2: cham_no(s2, q.pos.copy(), 0.8, mau_dam=mau_phach))
        sim.at(R.T_MUA + 0.03 * i, roi)
    for j, (dx, tre) in enumerate(((-38.0, 0.12), (40.0, 0.07))):     # hai mảnh vừa
        sim.at(R.T_SKILL_TRUNG - 0.04 - tre, lambda s, dx=dx: manh_pha_le(
            s, FOE_C + np.array([dx + 80.0, -330.0]), np.array([-250.0, 1100.0]), L=38, Wd=14, life=0.6, y_cham=FOE_C[1] + 6,
            on_hit=lambda q, s2: cham_no(s2, q.pos.copy(), 1.3, mau_dam=mau_phach)))

    def to(s):                                                   # mảnh to nhất cắm xuống đúng khung trúng
        p0 = FOE_C + np.array([90.0, -340.0])

        def trung(q, s2):
            cham_no(s2, q.pos.copy(), 2.4, mau_dam=mau_phach)
            vong_dat(s2, fx.FOE + np.array([0, 2.0]), 110, 0.6)
            s2.flash = 0.4
            s2.shake(0.45)
            cam = fx.P(np.array([q.pos[0] + 12, fx.FOE[1] - 4.0]), (0, 0), 0.5, group=fx.FRONT)
            base = [(0, -54), (14, -24), (14, 9), (-14, 9), (-14, -24)]
            sang = [(0, -54), (14, -24), (14, 9), (0, 9)]
            cam.draw = lambda c, k: F.ve_khoi(fx.FRONT, 47, c.pos + np.array([1.6 * math.sin(c.age * 70), 0]), base, AMBER[0], 2.6, 1.0,
                                              (sang, AMBER[1]))
            cam.on_death = lambda c, s3: cham_no(s3, c.pos + np.array([0, -22.0]), 1.4, mau_dam=lambda r: AMBER[r.randint(2)])
            s2.add(cam)
        manh_pha_le(s, p0, np.array([-260.0, 1150.0]), L=56, Wd=21, life=0.6, y_cham=FOE_C[1] + 10, on_hit=trung)
    sim.at(R.T_SKILL_TRUNG - 0.04, to)


def attack(sim, T, fr):
    R = T.R

    def huc(s):
        p = T.diem(fr[int(R.T_HUC * fx.FPS)], "mieng") + np.array([-10.0, 0.0])
        cham_no(s, p, 1.2)
        vong_dat(s, fx.FOE + np.array([20.0, 2.0]), 70)
    sim.at(R.T_HUC, huc)
    sim.at(max(0.0, R.T_HUC - 0.14), lambda s: [bui(s, fx.ME + np.array([d * 30.0 + 30, -4.0]), vel=np.array([60.0 + d * 30, -20.0]),
                                                    r0=6, r1=16, life=0.5, group=fx.BACK) for d in (-1, 1)])


CONG_THUC = {"cast": (cast, "Dạng 2, chiêu mana: chồm lắc núi đá, ba cụm pha lê bay găm"),
             "skill": (skill, "Dạng 2, chiêu cuối: pha lê vọt lên, mưa pha lê dày + ba mảnh to"),
             "attack": (attack, "Dạng 2, đánh thường: ngửa lấy đà, lao húc")}

if __name__ == "__main__":
    chon = sys.argv[1] if len(sys.argv) > 1 else "all"
    T = F.Tuong("cong_da2")
    for clip, (fn, nhan) in CONG_THUC.items():
        if chon in ("all", clip):
            F.chay(T, clip, fn, f"cong_da2_{clip}", nhan=nhan)
