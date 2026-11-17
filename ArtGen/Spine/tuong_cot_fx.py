# -*- coding: utf-8 -*-
"""Bản xem trước chiêu của Cổ Vương (tuong_cot, dạng 2) và Cổ Vương Nhi (tuong_cot_non, dạng 1) trên sân có ĐỐI THỦ + VFX hạt phẳng
tạm (khung rig THẬT, khung sân và hạt của tho5_fx / fxlib), để người dùng hiểu chiêu đánh thế nào trước khi làm VFX trong Unity
(người dùng 2026-11-17: "animation này là sao tôi chưa hiểu").

VFX hệ Mộc + đá: rễ nâu viền mực trồi khỏi đất có lá xanh, bụi đất, dăm đá xám lục, lá xanh bị hút. Không glow, không gradient.

    tuong_cot_fx.py [tuong_cot|tuong_cot_non] [attack|cast|skill|all]   → inbox/tuong_cot_fx/<mã>_<clip>.gif, trang xem.html
"""
import math
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fxlib as fx  # noqa: E402
import tho5_fx as T5  # noqa: E402

T5.RA = os.path.join(HERE, "inbox", "tuong_cot_fx")
RE = [(122, 85, 52), (150, 108, 66)]                # rễ: nâu, nâu nhạt (mặt trên)
LA = [(109, 190, 69), (150, 214, 96)]               # lá
DA = [(120, 128, 110), (157, 165, 147), (98, 104, 92)]
FOE_C = T5.FOE_C


def _bez(p0, p1, p2, n=10):
    return [(1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2 for t in np.linspace(0, 1, n)]


def re_troi(sim, goc, cao, nghieng=0.0, day=9.0, t_len=0.12, giu=0.35, t_lun=0.25, la=True, group=fx.FRONT):
    """một rễ trồi khỏi đất: dải cong thuôn nhọn (nâu, viền mực), mọc lên trong t_len, giữ, lún; đầu rễ có một lá."""
    goc = np.array(goc, float)
    rng = sim.rng
    uon = rng.uniform(-0.5, 0.5) * cao * 0.35 + nghieng * cao
    dur = t_len + giu + t_lun

    def ve(q, k):
        a = q.age
        h = cao * (min(1.0, a / t_len) ** 0.6 if a < t_len else (1.0 if a < t_len + giu else max(0.0, 1 - (a - t_len - giu) / t_lun)))
        if h < 2:
            return []
        p0, p2 = np.array([0.0, 0.0]), np.array([uon * h / cao, -h])
        p1 = np.array([uon * 0.15, -h * 0.55])
        C = _bez(p0, p1, p2)
        L, R = [], []
        for i, c in enumerate(C):
            j = min(i + 1, len(C) - 1)
            d = C[j] - C[max(0, j - 1)]
            nn = np.array([-d[1], d[0]])
            nn = nn / (np.hypot(*nn) or 1.0)
            w = day * (1 - i / (len(C) - 1)) ** 0.8 + 0.6
            L.append(tuple(q.pos + c + nn * w))
            R.append(tuple(q.pos + c - nn * w))
        out = [fx.poly(group, 40, L + R[::-1], T5.INK, 1.0, 2.4), fx.poly(group, 40.1, L + R[::-1], RE[0], 1.0)]
        out.append(fx.poly(group, 40.2, L[:-2] + [tuple(q.pos + c) for c in C[::-1][2:]], RE[1], 1.0))
        if la and h > cao * 0.7:
            tip = q.pos + C[-1]
            s = 7.0 * min(1.0, (h - cao * 0.7) / (cao * 0.3))
            leaf = [(tip[0], tip[1]), (tip[0] + s * 0.9, tip[1] - s * 0.6), (tip[0] + s * 1.6, tip[1] - s * 0.1), (tip[0] + s * 0.8, tip[1] + s * 0.3)]
            out += [fx.poly(group, 40.3, leaf, T5.INK, 1.0, 1.8), fx.poly(group, 40.4, leaf, LA[0], 1.0)]
        return out
    p = fx.P(goc.copy(), (0, 0), dur, group=group)
    p.draw = ve
    return sim.add(p)


def bui(sim, pos, **kw):
    return T5.bui(sim, np.array(pos, float), **kw)


def dam(sim, pos, n=6, muc=1.0, ground=None):
    rng = sim.rng
    for i in range(n):
        a = -math.pi / 2 + (i / n - 0.5) * 2.6 + rng.uniform(-0.2, 0.2)
        v = np.array([math.cos(a), math.sin(a)]) * rng.uniform(150, 260) * muc
        T5.dam_da(sim, np.array(pos, float), v, size=rng.uniform(3.5, 6.5) * muc, col=DA[rng.randint(3)],
                  ground=(ground if ground is not None else fx.FOE[1]) + rng.uniform(-4, 6))


def la_hut(sim, dich_fn, t0, t1, rate=30):
    """lá xanh từ xung quanh bị hút xoáy vào điểm dich_fn(t)."""
    rng = sim.rng

    def mot(s, x=None):
        a = rng.uniform(0, 6.28)
        c = dich_fn(s.t)
        p0 = c + np.array([math.cos(a), math.sin(a) * 0.7]) * rng.uniform(70, 120)
        q = fx.P(p0, (0, 0), 0.45, group=fx.FRONT, p0=p0, a0=a)
        sz = rng.uniform(4.0, 6.5)
        col = LA[rng.randint(2)]

        def upd(q, dt, s2):
            k = (q.age / q.life) ** 1.6
            cc = dich_fn(s2.t)
            r = (1 - k)
            aa = q.a0 + 2.2 * k
            q.pos = cc + (q.p0 - cc) * r @ np.array([[math.cos(2.2 * k), math.sin(2.2 * k)], [-math.sin(2.2 * k), math.cos(2.2 * k)]]) - q.vel * dt
            q.ang = aa
        q.upd = upd

        def ve(q, k):
            pts = [(sz * math.cos(q.ang), sz * math.sin(q.ang)), (sz * 0.35 * math.cos(q.ang + 1.6), sz * 0.35 * math.sin(q.ang + 1.6)),
                   (-sz * math.cos(q.ang), -sz * math.sin(q.ang)), (sz * 0.35 * math.cos(q.ang - 1.6), sz * 0.35 * math.sin(q.ang - 1.6))]
            return T5.ve_khoi(fx.FRONT, 46, q.pos, pts, col, 1.6)
        q.draw = ve
        s.add(q)
    sim.every(t0, t1, rate, mot)


def bong_bao(sim, pos, t0, t1, R=46.0):
    """bóng tối tròn dẹt dưới chân đối thủ lớn dần (báo cột sắp giáng)."""
    p = fx.P(np.array(pos, float), (0, 0), t1 - t0, group=fx.FLOOR)

    def ve(q, k):
        r = R * (0.3 + 0.7 * k)
        pts = [(q.pos[0] + r * math.cos(a), q.pos[1] + 0.32 * r * math.sin(a)) for a in np.linspace(0, 6.28, 24)]
        return [fx.poly(fx.FLOOR, 4, pts, (40, 32, 26), 0.25 + 0.35 * k)]
    p.draw = ve
    sim.at(t0, lambda s: s.add(p))


def trung_foe(s, muc=1.0, nay=-6.0, giu=0.1):
    s.hero_fx["foe"] = {"tint": (255, 246, 214), "amt": 0.9, "decay": 6.0, "off": (-5.0 * muc, nay * muc), "sq": (1.0, 1.0)}
    s.at(s.t + giu, lambda s2: s2.hero_fx.get("foe", {}).update(off=(0.0, 0.0)))


# ---------------------------------------------------------------- dạng 2
def d2_attack(sim, T, fr):
    R = T.R

    def dap(s):
        T5.cham_no(s, FOE_C + np.array([4.0, -6.0]), 1.4, mau_dam=lambda r: DA[r.randint(3)])
        T5.vong_dat(s, fx.FOE + np.array([0.0, 2.0]), 70, 0.4)
        s.shake(0.25)
        trung_foe(s, 1.4, -2.0)
    sim.at(R.T_ATK, dap)


def d2_cast(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]       # noqa: E731

    def cam(s):
        m = T.diem(tt(R.T_CAM), "mieng")
        g = np.array([m[0], fx.ME[1] + 2.0])
        T5.vong_dat(s, g, 90, 0.5)
        for d in (-1, 1):
            bui(s, g + np.array([d * 26.0, -4.0]), vel=np.array([d * 90.0, -30.0]), r0=10, r1=24)
        dam(s, g + np.array([0, -6.0]), 5, 0.8, ground=fx.ME[1])
        s.shake(0.3)
        # rễ trồi nối nhau dọc mặt đất tới đối thủ
        a, b = g, fx.FOE + np.array([14.0, 2.0])
        n = 8
        for i in range(n):
            f = (i + 1) / n
            def troi(s2, f=f):
                c = a + (b - a) * f + np.array([0.0, s2.rng.uniform(-4, 4)])
                for j in range(2):
                    re_troi(s2, c + np.array([s2.rng.uniform(-10, 10), 0]), s2.rng.uniform(18, 30) * (0.7 + 0.5 * f), day=5.0,
                            giu=0.18, t_lun=0.2, la=j == 0)
                bui(s2, c, vel=np.array([s2.rng.uniform(-40, 40), -30.0]), r0=6, r1=16, life=0.45)
            s.at(R.T_CAM + (R.T_RE - R.T_CAM) * f, troi)

    def re_quan(s):                                           # rễ lớn trồi quanh đối thủ, quấn
        for dx, h, ng in ((-26, 78, 0.25), (24, 86, -0.3), (-8, 96, 0.1), (12, 70, -0.1)):
            re_troi(s, fx.FOE + np.array([dx, 4.0]), h, nghieng=ng, day=8.0, t_len=0.10, giu=0.4, t_lun=0.25)
        T5.cham_no(s, FOE_C + np.array([0.0, 16.0]), 1.0, mau_dam=lambda r: DA[r.randint(3)])
        trung_foe(s, 1.0, -12.0, 0.3)
        s.shake(0.2)
    sim.at(R.T_CAM, cam)
    sim.at(R.T_RE, re_quan)


def d2_skill(sim, T, fr):
    R = T.R
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]       # noqa: E731
    sim.at(R.T_NEM, lambda s: bui(s, T.diem(tt(R.T_NEM), "m_nam_xa"), vel=np.array([0.0, -40.0]), r0=8, r1=20))
    la_hut(sim, lambda t: T.diem(tt(t), "m_loi"), R.T_TU, R.T_GIANG - 0.05, 34)
    bong_bao(sim, fx.FOE + np.array([0.0, 2.0]), R.T_GIANG, R.T_SKILL, 70)
    T5.vet_nut(sim, fx.FOE + np.array([-60.0, 2.0]), fx.FOE + np.array([60.0, 4.0]), R.T_SKILL, 0.15)

    def giang(s):
        g = fx.FOE + np.array([0.0, 2.0])
        T5.vong_dat(s, g, 170, 0.6)
        T5.vong_dat(s, g, 110, 0.45)
        for d in range(-3, 4):
            bui(s, g + np.array([d * 18.0, -4.0]), vel=np.array([d * 40.0, -40.0]), r0=12, r1=30, life=0.8)
        dam(s, g + np.array([0, -10.0]), 12, 1.3)
        s.shake(0.7)
        s.flash = 0.35
        trung_foe(s, 2.0, -26.0, 0.35)

    def re(s):
        for dx, h, ng in ((-58, 64, 0.35), (-34, 80, 0.2), (36, 84, -0.25), (60, 66, -0.35)):
            re_troi(s, fx.FOE + np.array([dx, 4.0]), h, nghieng=ng, day=8.0, t_len=0.10, giu=0.35, t_lun=0.25)
    sim.at(R.T_SKILL, giang)
    sim.at(R.T_RE2, re)
    sim.at(R.T_BAT, lambda s: s.shake(0.15))


# ---------------------------------------------------------------- dạng 1
def d1_attack(sim, T, fr):
    def huc(s):
        T5.cham_no(s, FOE_C + np.array([6.0, 4.0]), 0.9, mau_dam=lambda r: DA[r.randint(3)])
        trung_foe(s, 1.0)
    sim.at(0.46, huc)


def d1_cast(sim, T, fr):
    def cam(s):
        g = fx.ME + np.array([-20.0, 2.0])
        T5.vong_dat(s, g, 60, 0.4)
        bui(s, g, vel=np.array([0.0, -30.0]), r0=8, r1=18)
        s.shake(0.15)
        a, b = g, fx.FOE + np.array([12.0, 2.0])
        n = 6
        for i in range(n):
            f = (i + 1) / n
            s.at(0.62 + 0.33 * f, lambda s2, f=f: re_troi(s2, a + (b - a) * f, s2.rng.uniform(14, 22), day=4.0, giu=0.15, t_lun=0.2))

    def toi(s):
        for dx, h, ng in ((-16, 52, 0.2), (14, 58, -0.2)):
            re_troi(s, fx.FOE + np.array([dx, 4.0]), h, nghieng=ng, day=6.0, t_len=0.10, giu=0.3, t_lun=0.2)
        T5.cham_no(s, FOE_C + np.array([0.0, 18.0]), 0.7, mau_dam=lambda r: DA[r.randint(3)])
        trung_foe(s, 0.8, -8.0, 0.25)
    sim.at(0.62, cam)
    sim.at(0.95, toi)


def d1_skill(sim, T, fr):
    tt = lambda t: fr[min(len(fr) - 1, int(round(t * fx.FPS)))]       # noqa: E731
    la_hut(sim, lambda t: T.diem(tt(t), "m_loi"), 0.30, 0.90, 22)
    bong_bao(sim, fx.FOE + np.array([0.0, 2.0]), 0.95, 1.18, 40)

    def giang(s):
        g = fx.FOE + np.array([0.0, 2.0])
        T5.vong_dat(s, g, 90, 0.45)
        for d in (-1, 0, 1):
            bui(s, g + np.array([d * 18.0, -4.0]), vel=np.array([d * 50.0, -35.0]), r0=9, r1=22)
        dam(s, g + np.array([0, -8.0]), 7, 1.0)
        s.shake(0.35)
        trung_foe(s, 1.4, -14.0, 0.25)
    sim.at(1.18, giang)


CONG_THUC = {
    "tuong_cot": {"attack": (d2_attack, "Đánh thường: Đập Trụ", True), "cast": (d2_cast, "Chiêu mana: Rễ Trói Đất"),
                  "skill": (d2_skill, "Chiêu cuối: Thần Trụ Giáng Thế")},
    "tuong_cot_non": {"attack": (d1_attack, "Đánh thường: Húc Vương Miện", True), "cast": (d1_cast, "Chiêu mana: Rễ Con"),
                      "skill": (d1_skill, "Chiêu cuối: Tiểu Trụ Giáng")},
}


def trang():
    gifs = sorted(f for f in os.listdir(T5.RA) if f.endswith(".gif"))
    the = "".join(f'<figure><img src="{g}"><figcaption>{g[:-4]}</figcaption></figure>' for g in gifs)
    open(os.path.join(T5.RA, "xem.html"), "w", encoding="utf-8").write(
        "<!doctype html><meta charset=utf-8><title>Cổ Vương: xem trước chiêu</title><style>body{font:15px sans-serif;margin:16px;"
        "background:#f4f1ea}figure{display:inline-block;margin:8px;background:#fff;padding:6px;border:1px solid #ddd}img{width:540px;"
        "display:block}</style><h1>Cổ Vương / Cổ Vương Nhi: xem trước chiêu (rig thật + hiệu ứng tạm)</h1><p>Tướng mình dưới phải, đối "
        "thủ trên trái (như trong trận). Hiệu ứng chỉ để hình dung, sẽ làm lại trong Unity.</p>" + the)
    print(os.path.join(T5.RA, "xem.html"))


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "tuong_cot"
    chon = sys.argv[2] if len(sys.argv) > 2 else "all"
    T = T5.Tuong(code)
    for clip, ct in CONG_THUC[code].items():
        if chon in ("all", clip):
            T5.chay(T, clip, ct[0], f"{code}_{clip}", nhan=ct[1], lao=len(ct) > 2 and ct[2])
    trang()
