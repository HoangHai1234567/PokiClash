# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của Sa Long DẠNG 1 (dạng non, rong_cat_non, rig monster_3529): dùng lại khung sân + hạt của tho5_fx.py (không sửa
file đó), chạy rig thật (rong_cat_non_rig.dung_het). Giống ý Sa Long dạng 2 (rong_cat) nhưng NHẸ HƠN: hai lưỡi cát nhỏ thay ba, hai cột sa
thạch (cột cuối vừa) thay ba cột (cột cuối to), vết vuốt + cát văng nhỏ hơn. Mốc giờ đọc từ sự kiện của clip.

    py -3 -I ArtGen/Spine/tho5_fx_rong_cat_non.py [cast|skill|attack|all]   → inbox/tho5_fx/rong_cat_non_<clip>.gif + _soi.png
"""
import math
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5_fx as F  # noqa: E402
from tho5_fx import fx, bui, vong_dat, cham_no, luoi_cat, cot_da, vet_nut, ve_khoi, CAT, FOE_C  # noqa: E402


def _ev(T, clip, ten):
    return [float(e[0]) for e in T.clips[clip].ev if e[1] == ten]


def cast(sim, T, fr):
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    ts = _ev(T, "cast", "chem1") + _ev(T, "cast", "chem2")
    for i, tc in enumerate(ts):
        def chem(s, tc=tc, i=i):
            m = T.diem(tt(tc), "mieng")
            luoi_cat(s, m, FOE_C + np.array([0.0, (i - 0.5) * 18.0]), 0.22, R=28 + 4 * i,
                     on_hit=lambda q, s2: cham_no(s2, q.pos.copy(), 0.75, mau_dam=lambda r: CAT[r.randint(3)]))
        sim.at(tc, chem)


def skill(sim, T, fr):
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]
    rng = sim.rng
    t_gong, t_nen = _ev(T, "skill", "gong")[0], _ev(T, "skill", "nen")[0]
    t_cot = _ev(T, "skill", "cot1") + _ev(T, "skill", "cot2")

    def hut(s, x):                                               # cát, đá vụn hút về vuốt xa đang giơ
        m = T.diem(tt(s.t), "vuot_xa")
        a = rng.uniform(0, 6.28)
        p0 = m + np.array([math.cos(a), math.sin(a) * 0.6]) * rng.uniform(40, 65)
        q = fx.P(p0, (0, 0), 0.28, group=fx.FRONT, p0=p0)

        def upd(q, dt, s2):
            q.pos = q.p0 + (T.diem(tt(s2.t), "vuot_xa") - q.p0) * (q.age / q.life) ** 1.5 - q.vel * dt
        q.upd = upd
        sz = rng.uniform(2.2, 3.8)
        q.draw = lambda q, k: ve_khoi(fx.FRONT, 45, q.pos, [(sz * math.cos(t), sz * math.sin(t)) for t in (0.3, 1.9, 3.5, 5.0)],
                                      CAT[rng.randint(3)], 1.6)
        s.add(q)
    sim.every(t_gong, t_nen - 0.1, 28, hut)

    def nen(s):
        m = T.diem(tt(t_nen), "vuot_xa")
        vong_dat(s, np.array([m[0], fx.ME[1] + 2.0]), 80, 0.5)
        for d in (-1, 1):
            bui(s, np.array([m[0] + d * 26, fx.ME[1] - 4.0]), vel=np.array([d * 80.0, -26.0]), r0=9, r1=20)
        s.shake(0.22)
        vet_nut(s, np.array([m[0], fx.ME[1]]), fx.FOE + np.array([16.0, 2.0]), s.t, 0.18)
    sim.at(t_nen, nen)
    dx = (-44.0, 0.0)
    for i, tc in enumerate(t_cot):
        def cot(s, i=i):
            to = i == len(t_cot) - 1
            cot_da(s, fx.FOE + np.array([dx[i], 3.0]), 44 if to else 28, 110 if to else 62, giu=0.45 if to else 0.32)
            s.shake(0.35 if to else 0.15)
            if to:
                s.flash = 0.25
                cham_no(s, FOE_C + np.array([0.0, 10.0]), 1.6, mau_dam=lambda r: CAT[r.randint(3)])
                s.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 5.0, "off": (0.0, -20.0), "sq": (1.0, 1.0)}
                s.at(s.t + 0.3, lambda s2: s2.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))
        sim.at(tc, cot)


def attack(sim, T, fr):
    t_atk = _ev(T, "attack", "trung")[0]

    def chem(s):
        for i in range(3):
            q = fx.P(FOE_C + np.array([-6.0 + 8 * i, -5.0 + 6 * i]), (0, 0), 0.16, group=fx.FRONT)
            q.draw = lambda q, k: [fx.item(fx.FRONT, 61, "arcpx", 200 * 1000 + 70, (255, 246, 214, 5), q.pos, 24, 1.4, 0, 1 - k * k)]
            s.add(q)
        cham_no(s, FOE_C, 0.8, mau_dam=lambda r: CAT[r.randint(3)])
    sim.at(t_atk, chem)


CONG_THUC = {"cast": (cast, "Chiêu mana: vuốt quét, hai lưỡi cát nhỏ"),
             "skill": (skill, "Chiêu cuối: chồm gồng, nện đất, hai cột sa thạch"),
             "attack": (attack, "Đánh thường: lao vồ chém vuốt")}

if __name__ == "__main__":
    chon = sys.argv[1] if len(sys.argv) > 1 else "all"
    T = F.Tuong("rong_cat_non")
    for clip, (fn, nhan) in CONG_THUC.items():
        if chon in ("all", clip):
            F.chay(T, clip, fn, f"rong_cat_non_{clip}", nhan=nhan)
