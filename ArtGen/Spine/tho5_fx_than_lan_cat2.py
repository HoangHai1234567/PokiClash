# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của Sa Tích DẠNG 2 (than_lan_cat_2, rig monster_3530): dùng lại khung sân + hạt của tho5_fx.py (không sửa file đó),
chạy rig thật (than_lan_cat_2_rig.dung_het, far đặt ở giữa thân địch). Giống ý dạng 1 nhưng mạnh hơn: năm phiến găm (phiến cuối nặng hơn),
hai cú đập đất rồi lốc cát cao hơn, vết cắn + cát văng to hơn.

    py -3 -I ArtGen/Spine/tho5_fx_than_lan_cat2.py [cast|skill|attack|all]   → inbox/tho5_fx/than_lan_cat2_<clip>.gif + _soi.png
"""
import math
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5_fx as F  # noqa: E402
from tho5_fx import fx, bui, vong_dat, cham_no, vet_can, loc_cat, GOM, CAT, FOE_C  # noqa: E402


def cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]

    def xoe(s, x):                                               # cát bốc quanh mũ trùm lúc gồng
        p = T.diem(tt(s.t), "all7") + s.rng.uniform(-50, 50, 2)
        bui(s, p, vel=np.array([s.rng.uniform(-40, 40), s.rng.uniform(-70, -20)]), r0=5, r1=13, life=0.5)
    sim.every(0.05, 0.45, 30, xoe)
    ks = sorted(R.PHIEN)
    for j, k in enumerate(ks):
        cuoi = j == len(ks) - 1
        sim.at(R.T_PHONG[k] + R.BAY, lambda s, cuoi=cuoi: cham_no(s, FOE_C + s.rng.uniform(-16, 16, 2), 1.3 if cuoi else 0.9,
                                                                   mau_dam=lambda r: GOM[r.randint(3)]))


def skill(sim, T, fr):
    R = T.R

    def xoay_chan(s, x):                                         # cát xoáy quanh chân đối thủ
        a = s.rng.uniform(0, 6.28)
        bui(s, fx.FOE + np.array([55 * math.cos(a), -4 + 9 * math.sin(a)]), vel=np.array([-70 * math.sin(a), -20.0]), r0=5, r1=13,
            life=0.5, group=fx.BACK)
    sim.every(0.08, R.T_TRUNG_SKILL, 22, xoay_chan)

    def dam(s, to):
        vong_dat(s, fx.ME + np.array([-20.0, 2.0]), 95 if to else 80)
        for d in (-1, 1):
            bui(s, fx.ME + np.array([-20.0 + d * 40.0, -4.0]), vel=np.array([d * 100.0, -24.0]), r0=10, r1=26 if to else 22)
        s.shake(0.32 if to else 0.22)
    sim.at(R.T_DAM, lambda s: dam(s, False))
    sim.at(R.T_DAM2, lambda s: dam(s, True))
    loc_cat(sim, fx.FOE + np.array([0.0, 4.0]), R.T_TRUNG_SKILL - 0.06, R.T_HET + 0.2, cao=fx.H * 1.45)
    sim.at(R.T_TRUNG_SKILL, lambda s: (s.shake(0.35), s.hero_fx.update(foe={"tint": CAT[2], "amt": 0.7, "decay": 1.2, "off": (0, 0),
                                                                             "sq": (1.0, 1.0)})))


def attack(sim, T, fr):
    R = T.R
    c = FOE_C + np.array([12.0, 6.0])
    sim.at(R.T_DOP, lambda s: (vet_can(s, c), cham_no(s, c, 1.0, mau_dam=lambda r: CAT[r.randint(3)])))


CONG_THUC = {"cast": (cast, "Chiêu mana: năm phiến mũ trùm đất nung bay găm rồi về"),
             "skill": (skill, "Chiêu cuối: giơ tay, đập đất hai lần, lốc cát cao trùm đối thủ"),
             "attack": (attack, "Đánh thường: lao tới đớp + cào")}

if __name__ == "__main__":
    chon = sys.argv[1] if len(sys.argv) > 1 else "all"
    T = F.Tuong("than_lan_cat_2")
    for clip, (fn, nhan) in CONG_THUC.items():
        if chon in ("all", clip):
            F.chay(T, clip, fn, f"than_lan_cat2_{clip}", nhan=nhan)
