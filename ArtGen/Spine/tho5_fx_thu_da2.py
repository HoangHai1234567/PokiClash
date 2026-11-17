# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của Tê Thiềm DẠNG 2 (thu_da_2, rig thu_da2_rig.py) trên sân giả, dùng các hạt của tho5_fx.py (không sửa file đó).
Đòn giống ý dạng 1 nhưng mạnh hơn:
    attack = lao tới đâm mũi pha lê: chớp, dăm hổ phách + đá, vòng bụi;
    cast   = há hàm tụ: bụi + sỏi + mảnh pha lê nhỏ xoáy hút vào miệng; PHUN TẢNG ĐÁ to (mạch hổ phách) bay vồng, nổ lớn;
    skill  = giơ khối pha lê gồng (bụi rỉ dưới chân, dăm hổ phách rơi khỏi khối), nhảy tới (bụi bật), BỔ: nổ rất lớn ở đối thủ, vòng cột
             pha lê hổ phách trồi quanh chân đối thủ, vòng bụi lớn; đáp về: vòng bụi; gầm: bụi rung.
    py -3 -I ArtGen/Spine/tho5_fx_thu_da2.py [attack|cast|skill|all]   → inbox/tho5_fx/thu_da2_<clip>.gif (+ _soi.png)
"""
import math
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
import fxlib as fx  # noqa: E402
import tho5_fx as F  # noqa: E402

F.DUNG["thu_da2"] = F.dung_thu_da          # cùng giao diện dung() / lam_clip(sk, info, cao) như dạng 1
FOE_C = F.FOE_C


def cot_pha_le(sim, chan, cao, rong, t_len=0.10, giu=0.40, t_lun=0.22, group=fx.FRONT):
    """cột lăng trụ pha lê hổ phách trồi từ đất (mặt chính + dải mặt sáng), giữ rồi lún; dăm ở chân."""
    chan = np.array(chan, float)
    rng = sim.rng
    ng = rng.uniform(-0.3, 0.3)
    dur = t_len + giu + t_lun
    p = fx.P(chan.copy(), (0, 0), dur, group=group)

    def ve(q, k):
        a = q.age
        hh = cao * (min(1.0, a / t_len) ** 0.5 if a < t_len else (1.0 if a < t_len + giu else max(0.0, 1 - (a - t_len - giu) / t_lun)))
        if hh < 2:
            return []
        w = rong / 2
        than = [(-w, 0), (-w + ng * w, -hh * 0.78), (ng * w * 1.6, -hh), (w + ng * w, -hh * 0.78), (w, 0)]
        sang = [(-w * 0.15, 0), (-w * 0.15 + ng * w, -hh * 0.78), (ng * w * 1.6, -hh), (w * 0.4 + ng * w, -hh * 0.78), (w * 0.4, 0)]
        return F.ve_khoi(group, 42, q.pos, than, F.AMBER[0], 2.6, 1.0, (sang, F.AMBER[1]))
    p.draw = ve
    sim.add(p)
    for i in range(3):
        F.dam_da(sim, chan + np.array([rng.uniform(-rong, rong) * 0.5, -3.0]), np.array([rng.uniform(-150, 150), rng.uniform(-280, -140)]),
                 size=rng.uniform(3, 5), col=F.AMBER[rng.randint(2)] if rng.uniform() < 0.5 else F.DA[rng.randint(3)], ground=chan[1] + 2)


def attack(sim, T, fr):
    R = T.R

    def dam(s):
        F.cham_no(s, FOE_C + np.array([14.0, 6.0]), 1.4, mau_dam=lambda r: F.AMBER[r.randint(2)] if r.uniform() < 0.5 else F.DA[r.randint(3)])
        F.vong_dat(s, fx.FOE + np.array([10.0, 2.0]), 70)
        for i in range(3):
            F.manh_pha_le(s, FOE_C + np.array([14.0, 6.0]), np.array([s.rng.uniform(-260, 60), s.rng.uniform(-420, -200)]), L=14, Wd=6,
                          life=0.35)
    sim.at(R.T_DAM, dam)
    sim.at(0.30, lambda s: [F.bui(s, fx.ME + np.array([d * 26.0, -3.0]), vel=np.array([d * 70.0 + 40, -20.0]), r0=7, r1=17)
                            for d in (-1, 1)])


def cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng

    def hut(s, x):
        m = T.diem(tt(s.t), "mieng")
        a = rng.uniform(0, 6.28)
        p0 = m + np.array([math.cos(a), math.sin(a)]) * rng.uniform(50, 85)
        q = fx.P(p0, (0, 0), 0.32, group=fx.FRONT, p0=p0)

        def upd(q, dt, s2):
            q.pos = q.p0 + (T.diem(tt(s2.t), "mieng") - q.p0) * (q.age / q.life) ** 1.6 - q.vel * dt
        q.upd = upd
        u = rng.uniform()
        if u < 0.35:
            pts = [(4.0 * math.cos(t), 4.0 * math.sin(t)) for t in (0.2, 1.8, 3.3, 4.8)]
            q.draw = lambda q, k: F.ve_khoi(fx.FRONT, 45, q.pos, pts, F.DA[rng.randint(3)], 1.6)
        elif u < 0.55:
            pts = [(5.0, 0), (0, 2.5), (-5.0, 0), (0, -2.5)]
            q.draw = lambda q, k: F.ve_khoi(fx.FRONT, 45, q.pos, pts, F.AMBER[rng.randint(2)], 1.6)
        else:
            q.draw = lambda q, k: [fx.item(fx.FRONT, 44, "ringpx0", 3, F.DUST[2], q.pos, 7 * (1 - k), 1.0, 0, 0.9)]
        s.add(q)
    sim.every(R.T_TU, R.T_PHUN - 0.04, 52, hut)

    def phun(s):
        m = T.diem(tt(R.T_PHUN), "mieng")

        def trung(q, s2):
            F.cham_no(s2, q.pos.copy(), 1.6, mau_dam=lambda r: F.AMBER[r.randint(2)] if r.uniform() < 0.4 else F.DA[r.randint(3)])
            F.vong_dat(s2, fx.FOE + np.array([0, 2.0]), 100, 0.55)
            s2.shake(0.25)
        F.tang_da(s, m, FOE_C + np.array([8.0, 0.0]), 0.40, r=21.0, vong=55.0, on_hit=trung)
        for i in range(4):
            F.bui(s, m + rng.uniform(-8, 8, 2), vel=np.array([rng.uniform(-90, -30), rng.uniform(-40, 10)]), r0=6, r1=15, life=0.4)
    sim.at(R.T_PHUN, phun)


def skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng

    def gong(s, x):                                              # gồng: bụi rỉ dưới chân, dăm hổ phách rơi khỏi khối pha lê
        F.bui(s, T.diem(tt(s.t), "day") + np.array([rng.uniform(-50, 50), -2.0]), vel=np.array([rng.uniform(-40, 40), -14.0]), r0=5,
              r1=12, life=0.5, group=fx.BACK)
        if rng.uniform() < 0.5:
            p = T.diem(tt(s.t), "all19") + rng.uniform(-30, 30, 2)
            F.dam_da(s, p, np.array([rng.uniform(-60, 60), rng.uniform(-80, 0)]), size=3.0, col=F.AMBER[rng.randint(2)],
                     ground=T.diem(tt(s.t), "day")[1] + 3)
    sim.every(R.T_GONG0, R.T_NHAY, 28, gong)
    sim.at(R.T_GONG0, lambda s: s.shake(0.06))
    sim.at(R.T_NHAY, lambda s: [F.bui(s, T.diem(tt(R.T_NHAY), "day") + np.array([d * 30.0, -3.0]), vel=np.array([d * 90.0, -25.0]), r0=8,
                                      r1=20) for d in (-1, 1)])

    def bo(s):
        c = FOE_C + np.array([6.0, 14.0])
        F.cham_no(s, c, 2.0, mau_dam=lambda r: F.AMBER[r.randint(2)] if r.uniform() < 0.55 else F.DA[r.randint(3)])
        F.vong_dat(s, fx.FOE + np.array([0, 2.0]), 140, 0.7)
        s.flash = 0.4
        s.shake(0.6)
        for i in range(7):                                       # vòng cột pha lê trồi quanh chân đối thủ (phần lớn sau lưng nó)
            a = 6.28 * (i + 0.3) / 7
            chan = fx.FOE + np.array([62 * math.cos(a), 2 + 16 * math.sin(a)])
            s.at(s.t + 0.03 * (i % 3), lambda s2, chan=chan, a=a: cot_pha_le(s2, chan, rng.uniform(62, 92), rng.uniform(14, 19),
                                                                            group=fx.BACK if math.sin(a) < 0.2 else fx.FRONT))
        s.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 5.0, "off": (-8.0, -10.0), "sq": (1.0, 1.0)}
        s.at(s.t + 0.2, lambda s2: s2.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))
    sim.at(R.T_BO, bo)
    sim.at(R.T_VE, lambda s: (F.vong_dat(s, fx.ME + np.array([0, 2.0]), 80), s.shake(0.12)))

    def gam(s, x):
        F.bui(s, fx.ME + np.array([rng.uniform(-70, 70), -2.0]), vel=np.array([rng.uniform(-60, 60), -20.0]), r0=5, r1=13, life=0.45,
              group=fx.BACK)
    sim.every(R.T_GAM0, R.T_GAM1, 20, gam)


CONG_THUC = {"attack": (attack, "Đánh thường: lao tới đâm mũi pha lê", True),
             "cast": (cast, "Chiêu mana: há hàm tụ đá, phun tảng đá lớn"),
             "skill": (skill, "Chiêu cuối: giơ khối pha lê gồng, nhảy tới bổ, vòng cột pha lê trồi", True)}

if __name__ == "__main__":
    chon = sys.argv[1] if len(sys.argv) > 1 else "all"
    T = F.Tuong("thu_da2")
    for clip, ct in CONG_THUC.items():
        if chon in ("all", clip):
            F.chay(T, clip, ct[0], f"thu_da2_{clip}", nhan=ct[1], lao=len(ct) > 2 and ct[2])
