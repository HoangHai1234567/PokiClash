"""Bộ hiệu ứng hệ Hỏa (bản thử 2026-11-10), dựng bằng fxlib theo chuẩn mốc phun lửa (hạt chồng lớp phẳng, khói than -> xám
có tro tán). Mỗi hiệu ứng xuất GIF + tờ 12 khung vào thư mục ra.

  kieu_lua    bốn kiểu lửa cạnh nhau (tròn, nhọn móc câu, xoắn trang trí, dung nham), lặp 2 s
  phun_lua    phun lửa (chuẩn mốc, khói mới) ; phun_lua_xoan: cùng chiêu, lửa kiểu xoắn
  vong_lua    vòng lửa liền quanh chân, lặp 2 s
  cau_lua, cau_nham, loc_xoay, kim_lua   cầu lửa, cầu dung nham, lốc xoáy lửa, kim lửa
  len_cap     lên cấp: tụ than, vòng lửa, cột lửa, sao xoắn bay lên, bung sao
  dung_nham   dung nham phun dưới chân đối thủ: nứt đất, phun, giọt rơi toé, đá văng, vũng nguội
  thien_thach thiên thạch: bóng báo trước, đá cháy lao xuống, nổ lớn sau lưng đối thủ, vòng sóng, đá văng, nấm khói
  no_lua      nổ lửa gọn trên thân đối thủ (nhỏ hơn thân)

Chạy: py -3 -I bo_hoa.py <thư mục ra> [tên ...]
"""
import math
import os
import sys

import numpy as np

import fxlib as fx
from fxlib import BACK, FLOOR, FRONT, FOE, H, ME, P, item, unit

SMK = fx.SMOKE_DARK


def stage_geo(stage):
    im, _ = stage.heroes["me"]
    w, h = im.width / fx.K, im.height / fx.K
    mouth = ME + np.array([-0.40 * w, -0.70 * h])
    return mouth, w, h


# ---------------- 1. bốn kiểu lửa ----------------
def kieu_lua(sim):
    cols = [(80, "tron"), (205, "nhon"), (335, "xoan"), (462, "nham")]
    gy = 392.0
    for cx, st in cols:
        base = np.array([cx, gy])
        if st == "nham":
            def spurt(s, rng, j, base=base):
                ang = math.radians(-90 + rng.uniform(-22, 22))
                v = np.array([math.cos(ang), math.sin(ang)]) * rng.uniform(300, 520)
                r = rng.uniform(8, 15)
                p = fx.flame(s, base + np.array([rng.uniform(-30, 30), 0]), v, rng.uniform(0.75, 0.95), r, r, "nham", "nham",
                             drag=0.4, acc=(0, 900), smoke_p=0.15, rng=rng, heat=1.6)
                p.draw = fx.mat_flame("nham", "nham", heat=1.6, size_fn=lambda q, k: q.r1 * (1 - max(0, (k - 0.8) / 0.2)))
            sim.periodic(2.0, 40, spurt)
            pool = P(base, (0, 0), 1e9, group=FLOOR)
            pool.draw = lambda q, k: [item(FLOOR, 1, "ell", 0, fx.INK, q.pos, 34, 3.4),
                                      item(FLOOR, 2, "ell", 0, (186, 46, 30), q.pos, 30, 3.6),
                                      item(FLOOR, 3, "ell", 0, (236, 104, 34), q.pos, 21, 4.0),
                                      item(FLOOR, 4, "ell", 0, (250, 170, 50), q.pos, 11, 4.6)]
            sim.add(pool)
            continue

        def fl(s, rng, j, base=base, st=st):
            x = rng.uniform(-24, 24)
            v = np.array([-x * rng.uniform(0.8, 1.6), -rng.uniform(170, 240)])
            fx.flame(s, base + np.array([x, -4]), v, rng.uniform(0.55, 0.8), rng.uniform(7, 9), rng.uniform(20, 30),
                     st, "xoan" if st == "xoan" else "lua", drag=1.3, acc=(0, -120), smoke_p=0.22,
                     heat=1.8 if st == "nhon" else 1.0, rng=rng)
        sim.periodic(2.0, 44, fl)

        def em(s, rng, j, base=base):
            fx.ember(s, base + np.array([rng.uniform(-20, 20), -40]), rng=rng)
        sim.periodic(2.0, 6, em)


# ---------------- 2. phun lửa ----------------
def make_phun(style="tron", pal="lua"):
    def build(sim):
        mouth = sim.geo[0]
        target = FOE + np.array([0.0, -0.45 * H])
        d = target - mouth
        dist = float(np.hypot(*d))
        u = d / dist
        nrm = np.array([-u[1], u[0]])
        up = nrm if nrm[1] < 0 else -nrm
        T0, T1 = 0.28, 1.18
        HIT = 34.0

        def upd(p, dt, s):
            k = p.age / p.life
            p.vel += nrm * math.sin(p.age * 17 + p.spin) * 260 * k * dt
            if not p.hit and float(np.dot(p.pos - mouth, u)) > dist - HIT:
                p.hit = True
                vu = float(np.dot(p.vel, u))
                side = 1 if float(np.dot(p.pos - mouth, nrm)) >= 0 else -1
                p.vel += -u * vu * 0.92 + nrm * side * abs(vu) * p.rng.uniform(0.15, 0.32)
                kk = p.age / p.life
                r_now = p.r0 + (p.r1 - p.r0) * fx.ease_out(kk / 0.75) ** 0.8
                p.life = min(p.life, p.age + p.rng.uniform(0.1, 0.16))
                p.r1 = min(p.r1, r_now * 1.05)
                p.r0 = min(p.r0, p.r1)
                p.acc = np.zeros(2)

        def shoot(s, x):
            rng = s.rng
            a = rng.uniform(-1, 1) * math.radians(12)
            dv = u * math.cos(a) + nrm * math.sin(a)
            ramp = min(1.0, x * (T1 - T0) / 0.08)
            lu = style == "luoi"  # lưỡi lửa: đầu luồng to hơn, dày hơn cho liền (lưỡi nhỏ thưa thì đứt quãng)
            p = fx.flame(s, mouth + dv * rng.uniform(0, 8), dv * rng.uniform(1200, 1400), rng.uniform(0.40, 0.52),
                         rng.uniform(13, 16) if lu else rng.uniform(7, 10), rng.uniform(28, 36) * (0.8 + 0.2 * ramp), style, pal,
                         drag=1.8, acc=(0, -320), smoke_p=0.3)
            p.smoke_group = BACK
            p.hit = False
            p.upd = upd
            if style == "tron" and rng.uniform() < 0.35:
                p.style = "tron"
        sim.every(T0, T1, lambda s, x: (95 if style == "luoi" else 72) * (1.5 if x < 0.11 else 1.0) * min(1.0, (1 - x) * (T1 - T0) / 0.16),
                  shoot)

        def side_smoke(s, x):
            if x < 0.12:
                return
            f = s.rng.uniform(0.45, 0.95)
            fx.smoke(s, mouth + u * dist * f + up * s.rng.uniform(14, 26) * (0.6 + f), r0=6 * (0.8 + 0.5 * f),
                     r1=18 * (0.8 + 0.5 * f), vel=np.array([s.rng.uniform(-30, 30), s.rng.uniform(-70, -40)]) - u * 20, group=BACK)
        sim.every(T0, T1, 14, side_smoke)

        def side_spark(s, x):
            f = s.rng.uniform(0.25, 0.8)
            sd = s.rng.choice([-1, 1])
            pos = mouth + u * dist * f + nrm * sd * s.rng.uniform(18, 30) * (0.5 + f)
            dv = u * s.rng.uniform(0.5, 1.0) + nrm * sd * s.rng.uniform(0.4, 0.9) + np.array([0, -0.3])
            fx.spark(s, pos, dv, s.rng.uniform(260, 420))
        sim.every(T0, T1, 14, side_spark)

        def charge(s, x):  # than bay vào miệng
            a = s.rng.uniform(0, 2 * math.pi)
            pos = mouth + np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(55, 80)
            p = fx.ember(s, pos, vel=(mouth - pos) * 2.2, life=0.24, size=8)
            p.upd = lambda q, dt, ss: q.vel.__imul__(1 + 3 * dt)
        sim.every(0.0, 0.2, 40, charge)

        def ball(s, x):
            fx.flame(s, mouth + s.rng.uniform(-4, 4, 2), u * 25, 0.22, 4, 10 + 26 * x, style, pal, smoke_p=0)
        sim.every(0.06, T0, 30, ball)

        t_hit = T0 + 0.24
        for i, tb in enumerate((t_hit, t_hit + 0.1, t_hit + 0.4)):
            def burst(s, i=i):
                for _ in range(5 if i < 2 else 3):
                    a = math.atan2(-u[1], -u[0]) + s.rng.uniform(-1.4, 1.4)
                    fx.spark(s, target + s.rng.uniform(-10, 10, 2), np.array([math.cos(a), math.sin(a) - 0.5]),
                             s.rng.uniform(250, 460))
                if i == 0:
                    s.hero_fx["foe"] = {"tint": (255, 150, 80), "amt": 0.5, "decay": 0.5}
            sim.at(tb, burst)

        def tail_smoke(s):
            for _ in range(4):
                fx.smoke(s, mouth + u * dist * s.rng.uniform(0.45, 0.8) + s.rng.uniform(-18, 18, 2), r0=8, r1=22, group=BACK)
            for _ in range(8):
                fx.ash(s, target + s.rng.uniform(-30, 30, 2))
        sim.at(T1 - 0.05, tail_smoke)
    return build


# ---------------- 3. vòng lửa ----------------
def fire_ring(sim, centre, rx, ry, period=2.0, n=84, r=11.0, tongues=80):
    """vòng lửa LIỀN (người dùng 2026-11-10): n cụm lửa đứng yên rải dày trên elip, chồng lên nhau thành một dải lửa (một viền
    mực), lõi vàng kem, phập phồng lệch pha; lưỡi lửa nhọn liếm lên từ dải. Nửa xa vẽ sau tướng, nửa gần trước."""
    cols = [fx.INK] + fx.PAL["lua"]
    fr = [1.0, 1.0, 0.86, 0.68, 0.44]  # lõi to để lõi các cụm gộp thành một đường vàng liền (lõi nhỏ thì thành chuỗi hạt cườm)

    def nodes(s, rng, j):
        for i in range(n):
            th = 2 * math.pi * i / n
            p = P(centre + np.array([rx * math.cos(th), ry * math.sin(th)]), (0, 0), period, th=th, ph=rng.uniform(0, 1),
                  seed=i % 4, group=BACK if math.sin(th) < 0 else FRONT, base=centre + np.array([rx * math.cos(th), ry * math.sin(th)]))

            def draw(q, k):
                pulse = math.sin(2 * math.pi * (2 * q.age / period + q.ph))
                rr = r * (1 + 0.18 * pulse) * (0.85 if q.group == FRONT else 1.0)
                pos = q.base + np.array([0, -2.5 * pulse])
                tang = -math.degrees(math.atan2(ry * math.cos(q.th), -rx * math.sin(q.th)))
                return [item(q.group, 20 + li, "solid" if li == 0 else "blob", q.seed, c, pos, 2 * rr * f + (4.5 if li == 0 else 0),
                             1.6, tang) for li, (c, f) in enumerate(zip(cols, fr))]
            p.draw = draw
            s.add(p)
    sim.periodic(period, 1, nodes)

    def lick(s, rng, j):
        th = 2 * math.pi * (j * 0.618 % 1.0)
        pos = centre + np.array([rx * math.cos(th), ry * math.sin(th) - 4])
        g = BACK if math.sin(th) < 0 else FRONT
        fx.flame(s, pos, np.array([math.cos(th) * 20, -rng.uniform(90, 150)]), rng.uniform(0.32, 0.48), 7,
                 rng.uniform(15, 21) * (0.85 if g == FRONT else 1.0), "nhon", "lua", group=g, drag=1.4, acc=(0, -160),
                 smoke_p=0, ember_p=0.05, heat=1.8, rng=rng)
    sim.periodic(period, tongues, lick)


def vong_lua(sim):
    _, w, h = sim.geo
    fire_ring(sim, ME + np.array([0, -2]), 0.46 * w, 16.0)
    sim.periodic(2.0, 10, lambda s, rng, j: fx.heat(s, ME + np.array([rng.uniform(-0.4, 0.4) * w, -30]), h=0.3 * h, rng=rng,
                                                    group=BACK if j % 2 else FRONT))
    sim.periodic(2.0, 10, lambda s, rng, j: fx.ember(s, ME + np.array([rng.uniform(-0.45, 0.45) * w, -10]), rng=rng, size=7))


# ---------------- 5. lên cấp ----------------
def len_cap(sim):
    _, w, h = sim.geo
    cen = ME + np.array([0, -0.45 * h])
    rx, ry = 0.42 * w, 15.0

    def gather(s, x):
        a = s.rng.uniform(0, 2 * math.pi)
        pos = cen + np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(0.7, 0.9) * h
        p = fx.ember(s, pos, vel=(cen - pos) * 2.0 + np.array([-math.sin(a), math.cos(a)]) * 120, life=0.32, size=9)
        p.upd = lambda q, dt, ss: q.vel.__imul__(1 + 2.5 * dt)
    sim.every(0.0, 0.25, 70, gather)

    def boom(s):
        s.hero_fx["me"] = {"tint": (255, 240, 200), "amt": 0.7, "decay": 2.2}
        s.flash = 0.3
        s.shake(0.3)
        fx.ring(s, ME + np.array([0, -2]), 0.45, 0.15 * h, 1.0 * h, col=(244, 150, 52), squash=0.3, band=(8.0, 1.5))
        s.at(s.t + 0.12, lambda ss: fx.ring(ss, ME + np.array([0, -2]), 0.4, 0.1 * h, 0.75 * h, col=(250, 214, 96), squash=0.3,
                                            band=(6.0, 1.0)))
    sim.at(0.3, boom)

    def pillar(s, x):
        th = s.rng.uniform(0, 2 * math.pi)
        g = BACK if math.sin(th) < 0 else FRONT
        pos = ME + np.array([rx * math.cos(th), ry * math.sin(th) - 4])
        v = np.array([math.cos(th) * 40, -s.rng.uniform(520, 700)])
        sc = 1.0 if g == BACK else 0.7
        fx.flame(s, pos, v, s.rng.uniform(0.35, 0.55), 8, s.rng.uniform(18, 26) * sc, "nhon", "lua", group=g, drag=2.2,
                 acc=(0, -200), smoke_p=0, ember_p=0.2, heat=1.7)
    sim.every(0.3, 0.95, lambda s, x: 110 * (1 - 0.6 * x), pillar)

    def spiral(s, x):
        p = P(ME, (0, 0), s.rng.uniform(0.7, 0.9), seed=0, ph=s.rng.uniform(0, 2 * math.pi), R=s.rng.uniform(0.35, 0.5) * w,
              vy=s.rng.uniform(260, 340), tw=s.rng.uniform(0, 6))

        def upd(q, dt, ss):
            a = q.ph + 7.0 * q.age
            q.pos = ME + np.array([q.R * (1 - 0.5 * q.age) * math.cos(a), 14 * math.sin(a) - q.vy * q.age])
            q.vel = np.zeros(2)
            q.group = BACK if math.sin(a) < 0 else FRONT
        p.upd = upd
        p.draw = fx.mat_sprite("star", 42, (255, 255, 255),
                               size_fn=lambda q, k: 13 * min(1, k / 0.15) * (1 - k ** 2) * (0.75 + 0.25 * math.sin(q.age * 30 + q.tw)))
        s.add(p)
    sim.every(0.35, 1.3, 40, spiral)

    def top(s):
        c = ME + np.array([0, -1.15 * h])
        for _ in range(14):
            a = s.rng.uniform(0, 2 * math.pi)
            p = P(c, np.array([math.cos(a), math.sin(a) - 0.3]) * s.rng.uniform(150, 320), s.rng.uniform(0.7, 1.0), drag=2.0,
                  acc=np.array([0, 260.0]), spin=s.rng.uniform(-8, 8), spin_drag=1.0, seed=0)
            p.draw = fx.mat_sprite("star", 42, (255, 255, 255), size_fn=lambda q, k: 14 * min(1, k / 0.1) * (1 - k ** 3))
            s.add(p)
        for _ in range(10):
            fx.ember(s, c + s.rng.uniform(-20, 20, 2), vel=s.rng.uniform(-120, 120, 2))
        for _ in range(6):
            fx.ash(s, c + s.rng.uniform(-30, 30, 2), dark=False)
    sim.at(0.98, top)


# ---------------- 6. dung nham ----------------
def dung_nham(sim):
    """đất nứt sủi bọt -> dung nham phun: cột sau lưng đối thủ, giọt giọt lệ bắn lên rơi toé vương miện, đá văng -> miệng hố
    có viền đá, vảy nổi, bong bóng vỡ, khói mảnh."""
    gy = FOE[1]

    def pre(s):
        p = P(FOE + np.array([0, 2]), (0, 0), 0.45, group=FLOOR)
        p.draw = lambda q, k: [item(FLOOR, 1, "crack", 0, None, q.pos, 1.5 * H * 0.42 * (0.3 + 0.7 * fx.ease_out(q.age / 0.3)),
                                    1 / 0.42)]
        s.add(p)
        s.shake(0.15)
    sim.at(0.0, pre)
    sim.every(0.05, 0.42, 22, lambda s, x: lava_drop(s, FOE + np.array([s.rng.uniform(-0.45, 0.45) * H, s.rng.uniform(-6, 6)]),
                                                     np.array([s.rng.uniform(-30, 30), -s.rng.uniform(100, 180)]),
                                                     s.rng.uniform(3, 5), gy + s.rng.uniform(-6, 8)))

    def erupt(s):
        s.shake(0.6)
        s.flash = 0.18
        s.hero_fx["foe"] = {"tint": (255, 120, 60), "amt": 0.4, "decay": 0.8}
        crater(s, FOE + np.array([0, 6]), 30, 1.65)
        for n_, t_ in ((14, 0.0), (8, 0.1)):
            s.at(s.t + t_, lambda ss, n_=n_: [lava_drop(ss, FOE + np.array([ss.rng.uniform(-0.2, 0.2) * H, -4]),
                                                        np.array([math.cos(a), math.sin(a)]) * ss.rng.uniform(320, 560),
                                                        ss.rng.uniform(8, 12), gy + ss.rng.uniform(-10, 18),
                                                        group=FRONT if ss.rng.uniform() < 0.5 else BACK)
                                              for a in [math.radians(-90 + ss.rng.uniform(-32, 32)) for _ in range(n_)]])
        for _ in range(6):
            a = math.radians(-90 + s.rng.uniform(-55, 55))
            rock(s, FOE + np.array([0, -6]), np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(380, 680), gy + s.rng.uniform(-14, 22))
    sim.at(0.42, erupt)

    def geyser(s, x):  # cột dung nham sau lưng đối thủ
        v = np.array([s.rng.uniform(-60, 60), -s.rng.uniform(640, 880) * (1 - 0.4 * x)])
        r = s.rng.uniform(20, 28) * (1 - 0.3 * x)
        q = fx.flame(s, FOE + np.array([s.rng.uniform(-0.14, 0.14) * H, -2]), v, s.rng.uniform(0.7, 0.85), r * 0.6, r,
                     "nham", "nham", group=BACK, drag=0.6, acc=(0, 1500), smoke_p=0.15, heat=1.5)
        q.draw = fx.mat_flame("nham", "nham", heat=1.5, stretch_k=700,
                              size_fn=lambda z, k: (z.r0 + (z.r1 - z.r0) * min(1, k / 0.3)) * (1 - max(0, (k - 0.75) / 0.25)))
    sim.every(0.42, 0.82, 90, geyser)

    def smk(s, x):
        fx.smoke(s, FOE + np.array([s.rng.uniform(-0.3, 0.3) * H, -s.rng.uniform(0.3, 1.0) * H]), r0=10, r1=26,
                 group=BACK, vel=np.array([s.rng.uniform(-40, 40), -s.rng.uniform(60, 110)]))
    sim.every(0.5, 1.3, 7, smk)


# ---------------- 7. thiên thạch ----------------
def thien_thach(sim):
    imp = FOE + np.array([0.0, -6.0])
    s0 = FOE + np.array([310.0, -480.0])
    TI = 0.75
    path = lambda t: s0 + (imp - s0) * (min(1.0, t / TI) ** 1.6)
    dvec = unit(imp - s0)

    shadow = P(FOE, (0, 0), TI, group=FLOOR)
    shadow.draw = lambda q, k: [item(FLOOR, 1, "ell", 0, (40, 24, 20), q.pos, 0.3 * H * (0.25 + 0.75 * k), 3.0, 0,
                                     0.2 + 0.3 * k)]
    sim.add(shadow)

    met = P(s0, (0, 0), TI, ang=0.0, spin=-7.0, seed=1)
    met.upd = lambda q, dt, s: setattr(q, "pos", path(s.t))
    met.draw = lambda q, k: [item(FRONT, 45, "rock", 1, None, q.pos, 58, 1.0, math.degrees(q.ang))]
    sim.add(met)

    def mantle(s, x):  # áo lửa quanh đá, đuôi lửa kéo ngược hướng bay
        pos = path(s.t) + s.rng.uniform(-9, 9, 2)
        v = -dvec * s.rng.uniform(140, 280) + np.array([-dvec[1], dvec[0]]) * s.rng.uniform(-70, 70)
        fx.flame(s, pos, v, s.rng.uniform(0.18, 0.3), 16, s.rng.uniform(20, 26), "tron", "lua", drag=3.0, acc=(0, -120),
                 smoke_p=0.3, heat=1.3)
    sim.every(0.02, TI, 100, mantle)

    def head(s, x):  # lửa trùm phía trước đá
        fx.flame(s, path(s.t) - dvec * 6 + s.rng.uniform(-8, 8, 2), dvec * 40, 0.12, 18, 26, "tron", "lua", heat=1.5, smoke_p=0,
                 group=BACK)
    sim.every(0.02, TI, 40, head)

    def trail(s, x):  # khói đuôi dày, cụm nhỏ chồng nhau thành dải liền (thưa thì thành chuỗi bóng đen)
        fx.smoke(s, path(s.t) - dvec * 30 + s.rng.uniform(-6, 6, 2), vel=-dvec * 30 + s.rng.uniform(-15, 15, 2), r0=6, r1=17,
                 life=s.rng.uniform(0.8, 1.2))
    sim.every(0.05, TI, 70, trail)

    def shed(s, x):
        fx.spark(s, path(s.t), -dvec + s.rng.uniform(-0.6, 0.6, 2), s.rng.uniform(150, 300))
    sim.every(0.05, TI, 18, shed)

    def impact(s):
        s.shake(0.9)
        s.flash = 0.45
        s.hero_fx["foe"] = {"tint": (255, 130, 70), "amt": 0.45, "decay": 0.8}
        for _ in range(24):  # lõi nổ: sau lưng đối thủ, ôm viền thân
            a = math.radians(s.rng.uniform(-180, 0))
            v = np.array([math.cos(a), math.sin(a) * 1.1]) * s.rng.uniform(250, 650)
            fx.flame(s, imp + s.rng.uniform(-10, 10, 2), v, s.rng.uniform(0.45, 0.7), 16, s.rng.uniform(30, 42), "tron", "lua",
                     group=BACK, drag=4.0, acc=(0, -200), heat=1.4, smoke_p=0.35)
        for _ in range(12):
            a = math.radians(s.rng.uniform(-170, -10))
            v = np.array([math.cos(a), math.sin(a)]) * 520
            fx.flame(s, imp, v, 0.32, 8, 20, "nhon", "lua", group=BACK, drag=5.0, acc=(0, -150), smoke_p=0)
        for sd in (-1, 1):  # lửa tạt sát đất phía trước (nhỏ)
            for _ in range(3):
                fx.flame(s, FOE + np.array([sd * s.rng.uniform(10, 30), 6]), np.array([sd * s.rng.uniform(250, 420), -30]),
                         0.35, 8, s.rng.uniform(14, 20), "tron", "lua", group=FRONT, drag=4.0, acc=(0, -200), smoke_p=0)
        fx.ring(s, FOE + np.array([0, 2]), 0.4, 0.2 * H, 1.6 * H, col=(244, 150, 52), squash=0.3, band=(9.0, 1.5))
        s.at(s.t + 0.1, lambda ss: fx.ring(ss, FOE + np.array([0, 2]), 0.35, 0.1 * H, 1.2 * H, col=(252, 236, 180), squash=0.3,
                                           band=(5.0, 1.0)))
        for _ in range(8):
            a = math.radians(-90 + s.rng.uniform(-70, 70))
            p = P(imp, np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(350, 650), 1.5, acc=np.array([0, 1300.0]),
                  spin=s.rng.uniform(-10, 10), seed=s.rng.randint(4), bounce=0.3, ground=FOE[1] + s.rng.uniform(-15, 25),
                  sz=s.rng.uniform(16, 24), group=FRONT if s.rng.uniform() < 0.5 else BACK)
            p.draw = fx.mat_sprite("rock", 45, None, size_fn=lambda q, k: q.sz * (1 - fx.smoothstep(0.6, 1.0, k)))
            s.add(p)
        for n_, t_ in ((14, 0.0), (10, 0.1)):
            s.at(s.t + t_, lambda ss, n_=n_: [fx.spark(ss, imp + ss.rng.uniform(-12, 12, 2),
                                                       np.array([ss.rng.uniform(-1, 1), -ss.rng.uniform(0.3, 1)]),
                                                       ss.rng.uniform(300, 560)) for _ in range(n_)])
        for _ in range(16):  # vành khói sát đất: nhiều cụm, tốc khác nhau -> chồng thành vành liền
            sd = s.rng.choice([-1, 1])
            fx.smoke(s, FOE + np.array([sd * s.rng.uniform(15, 45), s.rng.uniform(-6, 4)]),
                     vel=np.array([sd * s.rng.uniform(90, 260), -s.rng.uniform(10, 50)]),
                     r0=9, r1=s.rng.uniform(16, 22), life=s.rng.uniform(1.0, 1.4), group=BACK)
        for _ in range(6):  # nấm khói bay lên sau lưng
            fx.smoke(s, imp + np.array([s.rng.uniform(-30, 30), -s.rng.uniform(40, 80)]),
                     vel=np.array([s.rng.uniform(-40, 40), -s.rng.uniform(140, 220)]), r0=14, r1=30, life=s.rng.uniform(1.2, 1.5),
                     group=BACK)
        for _ in range(14):
            fx.ash(s, imp + s.rng.uniform(-40, 40, 2), vel=np.array([s.rng.uniform(-80, 80), -s.rng.uniform(80, 160)]))
        cr = P(FOE + np.array([0, 2]), (0, 0), 1.5, group=FLOOR)
        cr.draw = lambda q, k: [item(FLOOR, 1, "crack", 1, None, q.pos, 1.6 * H * 0.42, 1 / 0.42, 0, min(1.0, (1 - k) / 0.3))]
        s.add(cr)
    sim.at(TI, impact)


# ---------------- 8. nổ lửa ----------------
def no_lua(sim):
    c = FOE + np.array([0.0, -0.45 * H])

    def boom(s):
        f = P(c, (0, 0), 0.07)
        f.draw = lambda q, k: [item(FRONT, 30, "solid", 1, fx.INK, q.pos, 0.5 * H * (0.85 + 0.3 * k) + 5),
                               item(FRONT, 31, "blob", 1, (254, 244, 214), q.pos, 0.5 * H * (0.85 + 0.3 * k))]
        s.add(f)
        s.shake(0.45)
        s.hero_fx["foe"] = {"tint": (255, 236, 200), "amt": 0.45, "decay": 3.5}
        for _ in range(14):
            a = s.rng.uniform(0, 2 * math.pi)
            v = np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(150, 300)
            q = fx.flame(s, c + s.rng.uniform(-6, 6, 2), v, s.rng.uniform(0.38, 0.52), 12, s.rng.uniform(20, 26), "tron", "lua",
                         drag=4.5, acc=(0, -160), heat=1.6, smoke_p=0.3)
            q.smoke_group = BACK
        for _ in range(10):
            a = s.rng.uniform(0, 2 * math.pi)
            fx.flame(s, c, np.array([math.cos(a), math.sin(a)]) * 380, 0.26, 6, 14, "nhon", "lua", drag=5.5, acc=(0, -100),
                     smoke_p=0)
        p = P(c, (0, 0), 0.26)
        p.draw = fx.mat_ring((252, 241, 200), 1.0, thick_seq=(1, 2), size_fn=lambda q, k: 0.15 * H + 0.27 * H * fx.ease_out(k), layer=35)
        s.add(p)
        fx.ring(s, FOE + np.array([0, 2]), 0.35, 0.15 * H, 0.7 * H, col=(240, 140, 50), squash=0.3)
        for n_, t_ in ((12, 0.0), (8, 0.1)):
            s.at(s.t + t_, lambda ss, n_=n_: [fx.spark(ss, c + ss.rng.uniform(-8, 8, 2), ss.rng.uniform(-1, 1, 2),
                                                       ss.rng.uniform(300, 520)) for _ in range(n_)])
        s.at(s.t + 0.15, lambda ss: [fx.smoke(ss, c + ss.rng.uniform(-20, 20, 2) - np.array([0, 20]), r0=8, r1=20, group=BACK)
                                     for _ in range(4)])
        for _ in range(10):
            fx.ash(s, c + s.rng.uniform(-25, 25, 2), vel=np.array([s.rng.uniform(-90, 90), -s.rng.uniform(60, 140)]))
    sim.at(0.05, boom)


# ---------------- dùng chung cho các chiêu bắn ----------------
def explode(s, c, sc=1.0, group=FRONT):
    """nổ lửa gọn (như no_lua) tại c, cỡ sc: chớp kem 2 khung, lõi lửa nóng, lưỡi nhọn, vòng kem, tia văng 2 đợt, khói sau lưng."""
    f = P(c, (0, 0), 0.07, group=group)
    f.draw = lambda q, k: [item(q.group, 30, "solid", 1, fx.INK, q.pos, 0.42 * H * sc * (0.85 + 0.3 * k) + 5),
                           item(q.group, 31, "blob", 1, (254, 244, 214), q.pos, 0.42 * H * sc * (0.85 + 0.3 * k))]
    s.add(f)
    for _ in range(int(12 * sc + 2)):
        a = s.rng.uniform(0, 2 * math.pi)
        q = fx.flame(s, c + s.rng.uniform(-5, 5, 2), np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(140, 280) * sc,
                     s.rng.uniform(0.34, 0.48), 10 * sc, s.rng.uniform(18, 24) * sc, "tron", "lua", group=group, drag=4.5,
                     acc=(0, -160), heat=1.6, smoke_p=0.3)
        q.smoke_group = BACK
    for _ in range(int(8 * sc + 1)):
        a = s.rng.uniform(0, 2 * math.pi)
        fx.flame(s, c, np.array([math.cos(a), math.sin(a)]) * 360 * sc, 0.24, 5 * sc, 12 * sc, "nhon", "lua", group=group,
                 drag=5.5, acc=(0, -100), smoke_p=0, heat=1.6)
    p = P(c, (0, 0), 0.24, group=group)
    p.draw = fx.mat_ring((252, 236, 180), 1.0, band=(5.0, 1.0), size_fn=lambda q, k: (0.12 + 0.22 * fx.ease_out(k)) * H * sc,
                         layer=35)
    s.add(p)
    for n_, t_ in ((int(10 * sc), 0.0), (int(6 * sc), 0.1)):
        s.at(s.t + t_, lambda ss, n_=n_: [fx.spark(ss, c + ss.rng.uniform(-6, 6, 2), ss.rng.uniform(-1, 1, 2),
                                                   ss.rng.uniform(280, 480) * sc) for _ in range(n_)])
    s.at(s.t + 0.14, lambda ss: [fx.smoke(ss, c + ss.rng.uniform(-16, 16, 2) - np.array([0, 18]), r0=7 * sc, r1=18 * sc,
                                          group=BACK) for _ in range(int(3 * sc + 1))])
    for _ in range(int(6 * sc)):
        fx.ash(s, c + s.rng.uniform(-20, 20, 2), vel=np.array([s.rng.uniform(-80, 80), -s.rng.uniform(60, 130)]))


LAVA = [fx.INK, (204, 52, 28), (242, 112, 34), (252, 182, 56), (255, 234, 150)]
LAVA_F = [1.0, 1.0, 0.8, 0.6, 0.34]


def lava_drop_draw(z, k):
    """giọt dung nham hình giọt lệ: cầu chính + hai cục đuôi nhỏ dần phía sau hướng bay (gộp một khối, một viền mực), lõi sáng to;
    một số giọt có vảy đá nguội."""
    r = z.r1
    sp = float(np.hypot(*z.vel))
    d = z.vel / sp if sp > 1 else np.array([0.0, 1.0])
    tail = min(1.0, sp / 400)
    parts = [(z.pos, 1.0), (z.pos - d * r * 1.0 * tail, 0.66), (z.pos - d * r * 1.8 * tail, 0.38)]
    out = []
    for li, (c, f) in enumerate(zip(LAVA, LAVA_F)):
        for pos, ps in parts:
            rr = r * f * ps
            if rr < 0.8:
                continue
            out.append(item(z.group, 20 + li, "solid" if li == 0 else "blob", z.seed, c, pos, 2 * rr + (4.5 if li == 0 else 0)))
    if getattr(z, "crust", False):
        out.append(item(z.group, 25, "rock", z.seed, None, z.pos + np.array([r * 0.25, -r * 0.2]), r * 0.9, 1.0, math.degrees(z.ang)))
    return out


def lava_splat(q, s):
    """giọt chạm đất: vệt toé dẹt (vũng + vương miện 3-4 giọt nhỏ bắn lên), nguội dần về nâu đá rồi co lại."""
    p = P(q.pos.copy(), (0, 0), s.rng.uniform(0.45, 0.65), group=FLOOR, r=q.r1 * 1.4)
    p.draw = lambda z, k: [] if z.r * (1 - k ** 2) < 1 else [
        item(FLOOR, 5, "ell", 0, fx.INK, z.pos, (z.r * 0.75 + 2.5) * (1 - k ** 2), 2.6),
        item(FLOOR, 6, "ell", 0, fx.lerp((226, 92, 32), (104, 46, 40), min(1, k * 1.4)), z.pos, z.r * 0.75 * (1 - k ** 2), 2.6),
        item(FLOOR, 6.5, "ell", 0, (252, 182, 56), z.pos, z.r * 0.4 * max(0, 1 - k / 0.45), 2.8)]
    s.add(p)
    if q.r1 > 4.5:
        for _ in range(s.rng.randint(2, 4)):  # vương miện
            a = math.radians(-90 + s.rng.uniform(-55, 55))
            c = P(q.pos.copy(), np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(70, 150), 0.6, acc=np.array([0, 900.0]),
                  r1=s.rng.uniform(2.2, 3.2), seed=s.rng.randint(4), group=q.group, ground=q.pos[1] + 1)
            c.draw = lava_drop_draw
            c.on_ground = lambda z, ss: setattr(z, "dead", True)
            s.add(c)


def lava_drop(s, pos, vel, r, ground, group=FRONT):
    q = P(pos, vel, 2.0, drag=0.3, acc=np.array([0, 1400.0]), r1=r, seed=s.rng.randint(4), group=group,
          ang=s.rng.uniform(0, 6.28), spin=s.rng.uniform(-4, 4), crust=s.rng.uniform() < 0.3)
    q.draw = lava_drop_draw
    q.ground = ground
    q.on_ground = lambda z, ss: (lava_splat(z, ss), setattr(z, "dead", True))
    return s.add(q)


def lava_pool(s, pos, life=1.4, R=20.0):
    pool = P(pos, (0, 0), life, group=FLOOR)
    pool.draw = lambda q, k: [] if k > 0.98 else [
        item(FLOOR, 2, "ell", 0, fx.INK, q.pos, (R + 5) * (1 - k ** 3) * min(1, k / 0.1), 3.2),
        item(FLOOR, 3, "ell", 0, fx.lerp((186, 46, 30), (96, 44, 40), k), q.pos, R * (1 - k ** 3) * min(1, k / 0.1), 3.3),
        item(FLOOR, 4, "ell", 0, (236, 104, 34), q.pos, R * 0.65 * max(0, 1 - k / 0.75) * min(1, k / 0.1), 3.8),
        item(FLOOR, 4.5, "ell", 0, (250, 170, 50), q.pos, R * 0.35 * max(0, 1 - k / 0.5) * min(1, k / 0.1), 4.4)]
    s.add(pool)


def crater(s, pos, R=22.0, life=1.6, bubbles=True):
    """miệng hố dung nham: khe nứt toả, vũng dung nham, viền đá dung nham quanh mép, vảy đá nguội trôi trên mặt, bong bóng phồng
    lên rồi vỡ bắn giọt, khói mảnh bốc lên."""
    cr = P(pos, (0, 0), life, group=FLOOR)
    cr.draw = lambda q, k: [item(FLOOR, 1, "crack", 3, None, q.pos, 1.7 * H * 0.42 * min(1, q.age / 0.2), 1 / 0.42, 0,
                                 min(1.0, (1 - k) / 0.25))]
    s.add(cr)
    lava_pool(s, pos, life, R)
    ax, ay = 1.55 * R, 0.5 * R
    n = 13
    for j in range(n):  # viền đá
        th = 2 * math.pi * j / n + s.rng.uniform(-0.15, 0.15)
        rp = P(pos + np.array([ax * math.cos(th), ay * math.sin(th)]), (0, 0), life, group=FLOOR, seed=s.rng.randint(4),
               ang=s.rng.uniform(0, 6.28), sz=s.rng.uniform(9, 15) * (1.15 if math.sin(th) > 0 else 0.9), th=th)
        rp.draw = lambda q, k: [item(FLOOR, 9 if math.sin(q.th) > 0 else 1.5, "rock", q.seed, None, q.pos,
                                     q.sz * min(1, fx.ease_out(q.age / 0.15)) * (1 - fx.smoothstep(0.8, 1.0, k)), 1.0,
                                     math.degrees(q.ang))]
        s.add(rp)
    for j in range(4):  # vảy nổi
        cp = P(pos + np.array([s.rng.uniform(-0.9, 0.9) * ax * 0.6, s.rng.uniform(-0.5, 0.5) * ay * 0.6]),
               (s.rng.uniform(-6, 6), s.rng.uniform(-2, 2)), life, group=FLOOR, seed=s.rng.randint(4), ang=s.rng.uniform(0, 6.28),
               spin=s.rng.uniform(-0.6, 0.6), sz=s.rng.uniform(8, 12))
        cp.draw = lambda q, k: [item(FLOOR, 7, "rock", q.seed, None, q.pos, q.sz * min(1, k / 0.15) * (1 - fx.smoothstep(0.75, 1.0, k)),
                                     1.6, math.degrees(q.ang))]
        s.add(cp)
    if bubbles:
        t0 = s.t

        def bubble(ss, x):
            bp = P(pos + np.array([ss.rng.uniform(-0.8, 0.8) * ax * 0.7, ss.rng.uniform(-0.6, 0.6) * ay * 0.7]), (0, 0),
                   ss.rng.uniform(0.25, 0.4), group=FLOOR, mx=ss.rng.uniform(4, 7))
            bp.draw = lambda q, k: [item(FLOOR, 8, "ell", 0, fx.INK, q.pos, q.mx * fx.ease_out(k) * 2 + 3, 1.2),
                                    item(FLOOR, 8.5, "ell", 0, (252, 182, 56), q.pos, q.mx * fx.ease_out(k) * 2, 1.2)]

            def pop(q, sss):
                for _ in range(2):
                    a = math.radians(-90 + sss.rng.uniform(-40, 40))
                    c = P(q.pos.copy(), np.array([math.cos(a), math.sin(a)]) * sss.rng.uniform(80, 140), 0.5,
                          acc=np.array([0, 900.0]), r1=2.6, seed=sss.rng.randint(4), group=FRONT, ground=q.pos[1] + 1)
                    c.draw = lava_drop_draw
                    c.on_ground = lambda z, s4: setattr(z, "dead", True)
                    sss.add(c)
            bp.on_death = pop
            ss.add(bp)
        s.every(t0 + 0.1, t0 + life * 0.75, 7, bubble)
        s.every(t0 + 0.1, t0 + life * 0.8, 6, lambda ss, x: fx.smoke(ss, pos + np.array([ss.rng.uniform(-ax, ax) * 0.6, -4]),
                                                                    r0=4, r1=11, pal=fx.SMOKE_DARK, group=BACK, with_ash=0.2))


def rock(s, pos, vel, ground, sz=None, group=None):
    p = P(pos, vel, 1.6, acc=np.array([0, 1300.0]), spin=s.rng.uniform(-10, 10), seed=s.rng.randint(4), bounce=0.32,
          ground=ground, sz=sz or s.rng.uniform(16, 24), group=group or (FRONT if s.rng.uniform() < 0.5 else BACK))
    p.draw = fx.mat_sprite("rock", 45, None, size_fn=lambda q, k: q.sz * (1 - fx.smoothstep(0.6, 1.0, k)))
    return s.add(p)


# ---------------- 9. cầu lửa (đuôi khói) ----------------
def cau_lua(sim):
    """tụ cầu lửa ở miệng 0,3 s -> bay 0,45 s (vòng cung nhẹ) kéo đuôi lửa, đuôi khói cam -> nâu -> xám và tia văng -> nổ gọn."""
    mouth = sim.geo[0]
    tgt = FOE + np.array([0.0, -0.42 * H])
    T0, TT = 0.3, 0.45
    d = unit(tgt - mouth)

    def path(t):
        x = min(1.0, max(0.0, (t - T0) / TT))
        return mouth + (tgt - mouth) * x + np.array([0.0, -40.0]) * math.sin(math.pi * x)

    def charge(s, x):
        a = s.rng.uniform(0, 2 * math.pi)
        pos = mouth + np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(45, 70)
        q = fx.ember(s, pos, vel=(mouth - pos) * 2.4, life=0.22, size=8)
        q.upd = lambda z, dt, ss: z.vel.__imul__(1 + 3 * dt)
    sim.every(0.0, T0 - 0.05, 45, charge)
    sim.every(0.04, T0, 50, lambda s, x: fx.flame(s, mouth + s.rng.uniform(-3, 3, 2), d * 20, 0.14, 6, 8 + 14 * x, "tron", "lua",
                                                    heat=1.8, smoke_p=0))

    def core(s, x):  # lõi cầu: hạt đời ngắn sinh liên tục, BÁM theo quả cầu (lệch nhỏ quanh tâm), nên cầu tròn chứ không thành que
        q = fx.flame(s, path(s.t), (0, 0), s.rng.uniform(0.12, 0.18), 16, s.rng.uniform(24, 29), "tron", "lua", drag=0,
                     acc=(0, 0), heat=1.9, smoke_p=0, ember_p=0)
        q.off = s.rng.uniform(-6, 6, 2)
        q.drift = s.rng.uniform(-40, 40, 2)

        def follow(z, dt, ss):
            z.off = z.off + z.drift * dt
            z.pos = path(ss.t) + z.off - z.vel * dt
            z.vel = (path(ss.t + 0.01) - path(ss.t)) / 0.01 * 0.15
        q.upd = follow
    sim.every(T0, T0 + TT, 150, core)

    def tail(s, x):
        q = fx.flame(s, path(s.t) - d * 14 + s.rng.uniform(-5, 5, 2), -d * s.rng.uniform(40, 100) + np.array([0, -20]),
                     s.rng.uniform(0.14, 0.22), 12, 12, "tron", "lua", drag=3.0, acc=(0, -140), heat=1.0, smoke_p=0, ember_p=0.04)
        q.draw = fx.mat_flame("tron", "lua", heat=1.0, size_fn=lambda z, k: z.r1 * (1 - k) ** 1.2)  # đuôi ngắn, co nhanh
    sim.every(T0, T0 + TT, 60, tail)

    def smoke_tail(s, x):  # khói đứng lại sau quả cầu, màu khói cháy
        fx.smoke(s, path(s.t) - d * 18 + s.rng.uniform(-4, 4, 2), vel=np.array([s.rng.uniform(-12, 12), -s.rng.uniform(10, 30)]),
                 r0=9, r1=s.rng.uniform(15, 19), life=s.rng.uniform(0.7, 1.0), pal=fx.SMOKE_FIRE, with_ash=0.1)
    sim.every(T0 + 0.03, T0 + TT, 110, smoke_tail)
    sim.every(T0, T0 + TT, 25, lambda s, x: fx.spark(s, path(s.t), -d + s.rng.uniform(-0.6, 0.6, 2), s.rng.uniform(140, 260)))

    def hit(s):
        s.shake(0.45)
        s.hero_fx["foe"] = {"tint": (255, 236, 200), "amt": 0.45, "decay": 3.0}
        explode(s, tgt, 0.85)
    sim.at(T0 + TT, hit)


# ---------------- 10. cầu dung nham ----------------
def cau_nham(sim):
    """ném cầu dung nham vòng cung cao 0,6 s, quả cầu nhỏ giọt dọc đường (rơi toé xuống đất), rơi trúng thì toé ra vũng."""
    mouth = sim.geo[0]
    land = FOE + np.array([0.0, -0.3 * H])
    T0, TT, ARC = 0.3, 0.6, 115.0

    def path(t):
        x = min(1.0, max(0.0, (t - T0) / TT))
        return mouth + (land - mouth) * x + np.array([0.0, -4 * ARC * x * (1 - x)])

    def vel_at(t):
        return (path(t + 0.01) - path(t - 0.01)) / 0.02

    sim.every(0.0, T0, 60, lambda s, x: fx.flame(s, mouth + s.rng.uniform(-4, 4, 2), (s.rng.uniform(-30, 30), -s.rng.uniform(40, 90)),
                                                   0.2, 5, 6 + 10 * x, "nham", "nham", heat=1.8, smoke_p=0))
    ball = P(path(T0), (0, 0), TT, spin=-6.0)

    def bupd(q, dt, s):
        q.pos = path(s.t)
        q.vel = vel_at(s.t)
    ball.upd = bupd

    def bdraw(q, k):
        r = 22.0
        sp = float(np.hypot(*q.vel))
        st = 1.0 + min(0.25, sp / 3000)
        ang = -math.degrees(math.atan2(q.vel[1], q.vel[0]))
        out = [item(FRONT, 20, "solid", 2, fx.INK, q.pos, 2 * r + 5, st, ang),
               item(FRONT, 21, "blob", 2, (186, 46, 30), q.pos, 2 * r, st, ang),
               item(FRONT, 22, "blob", 3, (236, 104, 34), q.pos, 1.64 * r, st, ang),
               item(FRONT, 23, "blob", 0, (250, 170, 50), q.pos, 1.15 * r, st, ang),
               item(FRONT, 24, "blob", 1, (254, 230, 132), q.pos, 0.6 * r, st, ang)]
        for i in range(3):  # vảy đá nguội trôi trên mặt quả cầu
            a = q.ang + i * 2.1
            out.append(item(FRONT, 25, "rock", i, None, q.pos + np.array([math.cos(a), math.sin(a) * 0.8]) * r * 0.62,
                            r * 0.55, 1.0, math.degrees(a)))
        return out
    ball.draw = bdraw
    sim.at(T0, lambda s: s.add(ball))
    sim.every(T0, T0 + TT, 50, lambda s, x: fx.flame(s, path(s.t) + s.rng.uniform(-12, 12, 2), (s.rng.uniform(-20, 20), -60), 0.22,
                                                       5, 9, "nham", "nham", heat=1.8, smoke_p=0))
    sim.every(T0 + 0.05, T0 + TT, 16, lambda s, x: lava_drop(s, path(s.t) + s.rng.uniform(-8, 8, 2),
                                                             vel_at(s.t) * 0.25 + np.array([s.rng.uniform(-40, 40), 0]),
                                                             s.rng.uniform(4, 7), FOE[1] + s.rng.uniform(-10, 30) + (ME[1] - FOE[1]) * (1 - x) * 0.9))
    sim.every(T0 + 0.05, T0 + TT, 100, lambda s, x: fx.smoke(s, path(s.t) - unit(vel_at(s.t)) * 22 + s.rng.uniform(-4, 4, 2),
                                                            r0=9, r1=s.rng.uniform(15, 19), vel=np.array([0, -20]),
                                                            life=s.rng.uniform(0.7, 0.95), pal=fx.SMOKE_FIRE, with_ash=0.08))

    def hit(s):
        s.shake(0.6)
        s.flash = 0.15
        s.hero_fx["foe"] = {"tint": (255, 120, 60), "amt": 0.45, "decay": 0.9}
        for _ in range(22):
            a = math.radians(-90 + s.rng.uniform(-60, 60))
            v = np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(180, 380)
            lava_drop(s, land + s.rng.uniform(-10, 10, 2), v, s.rng.uniform(4, 8), FOE[1] + s.rng.uniform(-12, 18),
                      group=FRONT if s.rng.uniform() < 0.45 else BACK)
        for _ in range(16):
            a = s.rng.uniform(0, 2 * math.pi)
            q = fx.flame(s, land + s.rng.uniform(-6, 6, 2), np.array([math.cos(a), math.sin(a) * 0.7]) * s.rng.uniform(100, 220),
                         0.4, 12, s.rng.uniform(18, 26), "nham", "nham", group=BACK, drag=4.0, acc=(0, 200), heat=1.6, smoke_p=0.3)
        for _ in range(5):
            a = math.radians(-90 + s.rng.uniform(-60, 60))
            rock(s, land, np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(300, 560), FOE[1] + s.rng.uniform(-14, 22))
        crater(s, FOE + np.array([0, 2]), 20, 1.4)
        for _ in range(6):
            fx.smoke(s, land + s.rng.uniform(-20, 20, 2) - np.array([0, 20]), r0=10, r1=24, group=BACK)
        for n_, t_ in ((10, 0.0), (6, 0.1)):
            s.at(s.t + t_, lambda ss, n_=n_: [fx.spark(ss, land, np.array([ss.rng.uniform(-1, 1), -ss.rng.uniform(0.3, 1)]),
                                                       ss.rng.uniform(260, 460)) for _ in range(n_)])
    sim.at(T0 + TT, hit)


# ---------------- 11. lốc xoáy lửa ----------------
def loc_xoay(sim):
    """lốc lửa cuốn đối thủ: hút than vào chân 0,3 s -> phễu lửa quay (càng cao càng loe, quay 9 rad/s, nửa sau thân vẽ sau,
    nửa trước vẽ trước và nhỏ hơn), vệt quay, đá và than bay vòng, khói thoát ra ở đỉnh -> tắt dần."""
    C = FOE + np.array([0.0, 2.0])
    HT = 1.22 * H
    R0, R1 = 16.0, 74.0
    OM = 9.0
    T1 = 1.9

    def vac(s, x):  # hút vào chân lốc
        a = s.rng.uniform(0, 2 * math.pi)
        pos = C + np.array([math.cos(a) * 1.1 * H, math.sin(a) * 0.3 * H])
        tang = np.array([-math.sin(a), math.cos(a) * 0.3])
        q = fx.ember(s, pos, vel=(C - pos) * 2.2 + tang * 160, life=0.42, size=7,
                     group=FRONT if math.sin(a) > 0 else BACK)
        q.upd = lambda z, dt, ss: z.vel.__imul__(1 + 1.5 * dt)
    sim.every(0.0, T1, 40, vac)
    sim.at(0.15, lambda s: s.shake(0.15))
    cr = P(C, (0, 0), 2.4, group=FLOOR)
    cr.draw = lambda q, k: [item(FLOOR, 1, "crack", 2, None, q.pos, 1.2 * H * 0.42 * min(1, q.age / 0.4), 1 / 0.42, 0,
                                 min(1.0, (1 - k) / 0.25))]
    sim.add(cr)
    band = P(C, (0, 0), 2.3, group=FLOOR)
    band.draw = fx.mat_ring((248, 170, 60), 0.3, band=(6.0, 2.0), size_fn=lambda q, k: R0 * 2.2 * min(1, q.age / 0.3) * (1 - 0.3 * k))
    sim.add(band)

    def orbit(q, dt, s):
        a = q.ph + OM * q.age
        y = q.vy * q.age
        h = min(1.0, y / HT)
        R = q.R0 + (q.R1 - q.R0) * h ** 0.9
        q.pos = C + np.array([R * math.cos(a), 0.3 * R * math.sin(a) - y])
        q.vel = np.array([-R * math.sin(a) * OM, 0.3 * R * math.cos(a) * OM - q.vy])
        q.group = BACK if math.sin(a) < 0 else FRONT
        q.h = h

    def funnel(s, x):
        q = fx.flame(s, C, (0, 0), s.rng.uniform(0.6, 0.8), 8, 22, "tron", "lua", drag=0, acc=(0, 0), heat=1.5, smoke_p=0.12,
                     ember_p=0.08)
        q.ph, q.vy, q.R0, q.R1, q.h = s.rng.uniform(0, 2 * math.pi), s.rng.uniform(230, 300), R0, R1 * s.rng.uniform(0.85, 1.05), 0.0
        q.upd = orbit
        q.smoke_group = BACK
        q.draw = fx.mat_flame("tron", "lua", heat=1.5, stretch_k=700,
                              size_fn=lambda z, k: (8 + 18 * z.h) * (0.75 if z.group == FRONT else 1.0) * (1 - fx.smoothstep(0.7, 1.0, k)))
    sim.every(0.25, T1, lambda s, x: 120 * min(1.0, x * 6) * (1 - 0.5 * max(0.0, (x - 0.85) / 0.15)), funnel)

    def streak(s, x):  # vệt quay cho thấy chiều xoáy
        p = P(C, (0, 0), s.rng.uniform(0.35, 0.5), seed=s.rng.randint(2), ph=s.rng.uniform(0, 2 * math.pi),
              vy=s.rng.uniform(200, 320), R0=R0 * 1.2, R1=R1 * 1.1, h=0.0)
        p.upd = orbit
        p.draw = fx.mat_sprite("streak", 40, (255, 255, 255), align=True, size_fn=lambda z, k: 9 * (1 - k ** 2),
                               stretch_fn=lambda z, k: 3.0)
        s.add(p)
    sim.every(0.3, T1, 45, streak)

    def swirl(s, x):  # dải cung lửa nằm ngang bay lên, càng cao càng loe, quay theo chiều xoáy (như vòng xoáy Epic Toon FX)
        p = P(C, (0, 0), s.rng.uniform(0.55, 0.7), ph=s.rng.uniform(0, 360), vy=s.rng.uniform(220, 280),
              span=int(s.rng.uniform(110, 190)), col=[(248, 150, 48), (252, 210, 78), (234, 80, 42)][s.rng.randint(3)])

        def draw(q, k):
            y = q.vy * q.age
            hh = min(1.0, y / HT)
            R = (R0 + (R1 - R0) * hh ** 0.9) * 1.05
            c = C + np.array([0.0, -y])
            a0 = (q.ph + math.degrees(OM) * q.age) % 360
            alpha = min(1.0, k / 0.15, (1 - k) / 0.25)
            bw = 3 + 6 * (1 - abs(2 * k - 1))
            out = []
            for lo, hi_, grp in ((180, 360, BACK), (0, 180, FRONT)):  # nửa trên elip là phía xa: vẽ sau tướng
                segs = []
                st, en = a0, a0 + q.span
                for off in (0, 360):
                    s0, e0 = max(st, lo + off), min(en, hi_ + off)
                    if e0 - s0 > 4:
                        segs.append((s0 % 360, e0 - s0))
                for s0, ln in segs:
                    out.append(item(grp, 26, "arcpx", int(s0) * 1000 + int(ln), tuple(q.col) + (bw * fx.K,), c, 2 * R * 0.3,
                                    1 / 0.3, 0, alpha))
            return out
        p.draw = draw
        s.add(p)
    sim.every(0.3, T1, 26, swirl)

    def debris(s, x):
        p = P(C, (0, 0), s.rng.uniform(0.7, 1.0), seed=s.rng.randint(4), ph=s.rng.uniform(0, 2 * math.pi),
              vy=s.rng.uniform(120, 200), R0=R0 * 2, R1=R1 * 1.25, h=0.0, sz=s.rng.uniform(9, 14), spin=s.rng.uniform(-9, 9))
        p.upd = orbit
        p.draw = fx.mat_sprite("rock", 45, None, size_fn=lambda z, k: z.sz * (1 - fx.smoothstep(0.75, 1.0, k)))
        s.add(p)
    sim.every(0.35, T1, 7, debris)

    def top_smoke(s, x):
        fx.smoke(s, C + np.array([s.rng.uniform(-0.8, 0.8) * R1, -HT + s.rng.uniform(0, 20)]),
                 vel=np.array([s.rng.uniform(-50, 50), -s.rng.uniform(40, 80)]), r0=11, r1=s.rng.uniform(19, 25), group=BACK, pal=fx.SMOKE_FIRE)
    sim.every(0.45, T1 + 0.2, 20, top_smoke)

    def tint(s):
        t = P(C, (0, 0), T1 - 0.3)
        t.upd = lambda q, dt, ss: ss.hero_fx.__setitem__("foe", {"tint": (255, 130, 70),
                                                                  "amt": 0.25 + 0.12 * math.sin(q.age * 18)})
        s.add(t)
        s.shake(0.35)
    sim.at(0.3, tint)
    sim.at(T1 - 0.05, lambda s: s.hero_fx.__setitem__("foe", {"tint": (255, 130, 70), "amt": 0.3, "decay": 0.8}))


# ---------------- 12. kim lửa ----------------
def kim_lua(sim):
    """bảy kim lửa lần lượt hiện thành vòng cung trên đầu (nở bật), lơ lửng chĩa vào đối thủ, rồi lần lượt phóng (0,09 s một
    kim) kéo vệt lửa, mỗi kim trúng một chớp nhỏ + tia văng, đối thủ giật và ửng lên theo từng nhát."""
    _, w, h = sim.geo
    A = ME + np.array([-10.0, -1.08 * h])
    N, RA = 7, 0.42 * w
    tgt = FOE + np.array([0.0, -0.42 * H])
    LEN = 58.0
    layers = [(fx.INK, 1.0, 4.5), ((234, 80, 42), 1.0, 0), ((248, 150, 48), 0.82, 0), ((252, 210, 78), 0.6, 0),
              ((254, 244, 206), 0.34, 0)]

    def make(s, i):
        th = math.pi + math.pi * (i + 0.5) / N
        home = A + np.array([RA * math.cos(th), 0.5 * RA * math.sin(th)])
        aim = tgt + np.array([s.rng.uniform(-0.18, 0.18) * H, s.rng.uniform(-0.15, 0.2) * H])
        q = P(home, (0, 0), 3.0, seed=i % 2, home=home, aim=aim, i=i, fly=False, launch=0.78 + i * 0.09, born=s.t)
        for _ in range(3):
            fx.flame(s, home + s.rng.uniform(-6, 6, 2), (s.rng.uniform(-30, 30), -s.rng.uniform(30, 70)), 0.22, 5, 11, "tron", "lua",
                     heat=1.6, smoke_p=0)
        fx.ember(s, home, size=7)

        def upd(z, dt, ss):
            if not z.fly:
                z.pos = z.home + np.array([0.0, 3.5 * math.sin(z.age * 7 + z.i)])
                z.vel = (z.aim - z.pos) * 0.001
                if ss.rng.uniform() < 0.12:  # lửa liếm quanh kim lúc lơ lửng
                    fx.flame(ss, z.pos + ss.rng.uniform(-8, 8, 2), (ss.rng.uniform(-15, 15), -ss.rng.uniform(40, 80)), 0.25, 4, 9,
                             "nhon", "lua", heat=1.7, smoke_p=0, ember_p=0.1)
                if ss.t >= z.launch:
                    z.fly = True
                    z.vel = unit(z.aim - z.pos) * 1500
                    ss.shake(0.05)
            else:  # đuôi lửa: hạt to, đời rất ngắn, chồng lên nhau thành đuôi thon liền (thưa thì thành chuỗi hạt cườm)
                if ss.rng.uniform() < 0.35:  # vệt tia kéo dài theo hướng bay
                    fx.spark(ss, z.pos - unit(z.vel) * 22, -unit(z.vel) + ss.rng.uniform(-0.15, 0.15, 2), ss.rng.uniform(250, 380),
                             life=0.14, size=11, grav=0, drag=6)
                if ss.rng.uniform() < 0.12:
                    fx.flame(ss, z.pos - unit(z.vel) * 24, -unit(z.vel) * 40, 0.12, 6, 9, "tron", "lua", heat=1.6, smoke_p=0,
                             ember_p=0)
                if float(np.dot(z.aim - z.pos, z.vel)) <= 0:
                    z.dead = True
                    hit_at(ss, z.aim, unit(z.vel))
        q.upd = upd

        def draw(z, k):
            age = z.age
            sc = 1.25 * fx.ease_out(age / 0.08) if age < 0.08 else 1.25 - 0.25 * min(1.0, (age - 0.08) / 0.06)
            d = unit(z.aim - z.pos) if not z.fly else unit(z.vel)
            ang = fx.tip_angle(d)
            st = 1.0 if not z.fly else 1.3
            out = []
            for li, (c, f, ext) in enumerate(layers):
                L = LEN * sc * f * (st if li < 2 else 1.0) + ext
                out.append(item(FRONT, 20 + li, "needle_s" if li == 0 else "needle", z.seed, c,
                                z.pos - d * (LEN * sc * (1 - f) * 0.25), L, 1.0, ang))
            return out
        q.draw = draw
        s.add(q)

    def hit_at(s, p, d):
        s.shake(0.14)
        s.hero_fx["foe"] = {"tint": (255, 236, 200), "amt": 0.4, "decay": 4.0}
        f = P(p, (0, 0), 0.06)
        f.draw = lambda q, k: [item(FRONT, 30, "solid", 0, fx.INK, q.pos, 26 + 5), item(FRONT, 31, "blob", 0, (254, 244, 214), q.pos, 26)]
        s.add(f)
        for _ in range(3):
            a = s.rng.uniform(0, 2 * math.pi)
            fx.flame(s, p, np.array([math.cos(a), math.sin(a)]) * 120, 0.24, 7, 14, "tron", "lua", heat=1.6, smoke_p=0.25, drag=4)
        for _ in range(5):
            fx.spark(s, p, -d + s.rng.uniform(-0.9, 0.9, 2), s.rng.uniform(200, 380), size=7)

    for i in range(N):
        sim.at(0.06 + i * 0.07, lambda s, i=i: make(s, i))
    sim.at(0.78 + N * 0.09 + 0.2, lambda s: [fx.smoke(s, tgt + s.rng.uniform(-25, 25, 2), r0=7, r1=18, group=BACK)
                                             for _ in range(4)])


EFFECTS = {
    "kieu_lua": (kieu_lua, 2.0, 2.0, "Bốn kiểu lửa", False),
    "phun_lua": (make_phun("tron"), 1.9, None, "Phun lửa", True),
    "phun_lua_xoan": (make_phun("xoan", "xoan"), 1.9, None, "Phun lửa (kiểu xoắn)", True),
    "phun_lua_luoi": (make_phun("luoi", "lua"), 1.9, None, "Phun lửa (lưỡi lửa kiểu tranh tướng)", True),
    "vong_lua": (vong_lua, 2.0, 2.0, "Vòng lửa", True),
    "len_cap": (len_cap, 1.9, None, "Lên cấp", True),
    "dung_nham": (dung_nham, 2.1, None, "Dung nham", True),
    "thien_thach": (thien_thach, 2.3, None, "Thiên thạch", True),
    "no_lua": (no_lua, 1.5, None, "Nổ lửa", True),
    "cau_lua": (cau_lua, 1.7, None, "Cầu lửa", True),
    "cau_nham": (cau_nham, 2.2, None, "Cầu dung nham", True),
    "loc_xoay": (loc_xoay, 2.7, None, "Lốc xoáy lửa", True),
    "kim_lua": (kim_lua, 2.2, None, "Kim lửa", True),
}


def main(out_dir, names):
    stage = fx.Stage()
    plain = fx.Stage(heroes=False)
    geo = stage_geo(stage)
    for nm in names:
        build, dur, loop, label, heroes = EFFECTS[nm]

        def b(sim, build=build):
            sim.geo = geo
            build(sim)
        lab = label
        if nm == "kieu_lua":
            lab = [(80, 430, "tròn"), (205, 430, "nhọn"), (335, 430, "xoắn"), (462, 430, "dung nham")]
        fx.run(b, out_dir, nm, dur, loop=loop, stage=stage if heroes else plain, label=lab)
        print("xong", nm, file=sys.stderr)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(fx.HERE, "_bo_hoa")
    main(out, sys.argv[2:] or list(EFFECTS))
