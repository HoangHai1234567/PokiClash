"""Bộ hiệu ứng hệ Thủy (bản thử 2026-11-10), dựng trên fxlib theo sổ công thức (skill pokiclash-fx-congthuc mục 5): giữ cách
chồng lớp phẳng và biên đạo theo pha của bộ Hỏa, đổi hình hạt và màu theo nét nước của game (lưỡi sóng mào cuộn, bọt trắng ở
mào, sọc xanh đậm / xanh trời / xanh nhạt, giọt lệ). Xoay quanh ba việc người dùng nêu: TỤ NƯỚC, BẮN TIA NƯỚC, CẦU NƯỚC.

  tu_nuoc     tụ nước: giọt và lưỡi sóng xoáy vào, cầu nước lớn dần, vòng nước co lại; rồi thấm vào tướng (buff)
  tia_nuoc    tụ nhanh ở miệng rồi bắn tia: dòng lưỡi sóng liền, lượn nhẹ; chỗ trúng toé bọt, giọt văng, vòng sóng dưới chân
  cau_nuoc    tụ cầu nước lớn, ném vòng cung (cầu rung, nhỏ giọt); trúng thì toé lớn, cột nước, mưa giọt, vũng nước
  bong_bong   thổi chùm bong bóng trôi lượn tới đối thủ, vỡ lần lượt; bong bóng lớn cuối cùng vỡ toé
  voi_rong    vòi rồng nước: thân phễu liền uốn lượn (hơi trong), sọc bọt trượt quanh, hai dòng sóng xoắn, bọt ở miệng
  luoi_nuoc   hai lưỡi nước trăng khuyết chém liên tiếp      thuong_nuoc  sáu mũi thương nước tụ vòng cung rồi phóng lần lượt
  song_than   tường sóng lăn tới, chồm qua đầu đổ ập xuống   mua_rao      mây nước tụ trên đầu đối thủ trút mưa
  xoay_nuoc   xoáy nước sát đất siết vào tâm rồi mạch phun   khien_nuoc   bong bóng nước bọc tướng (lặp 2 s)
  suoi_hoi    suối trào quanh chân, bọt và lấp lánh (hồi phục)

Hình hạt: water.py (tạm) hoặc ảnh GPT trong hat_gpt/ (build_hat.py gói hat_nuoc) khi có.
Chạy: py -3 -I bo_thuy.py <thư mục ra> [tên ...]
"""
import math
import os
import sys

import numpy as np
from PIL import Image

import fire
import fxlib as fx
import water
from fxlib import BACK, FLOOR, FRONT, FOE, H, ME, P, item, unit

INK = fx.INK
W = [INK, (30, 104, 190), (58, 150, 226), (140, 208, 246), (244, 252, 255)]  # mực, xanh đậm, xanh trời, xanh nhạt, bọt trắng
WF = [1.0, 1.0, 0.8, 0.58, 0.36]
FOAM = (244, 252, 255)
TINT = (120, 190, 255)
FXART = os.path.join(fx.ROOT, "Assets", "03 Art", "Fx")

fx.Art.EXTRA.update({
    "wave": lambda s: water.wave(s)[0], "wave_s": lambda s: water.wave(s, solid=True)[0],
    "drop": lambda s: water.drop(s)[0], "drop_s": lambda s: water.drop(s, solid=True)[0],
    "foam": lambda s: fire.cloud(s)[0], "foam_s": lambda s: fire.cloud(s, solid=True)[0],
    "no_nuoc": lambda s: Image.open(os.path.join(FXART, "no_nuoc.png")).convert("RGBA"),  # vụ nước toé GPT đã duyệt
})
fx.Art.GPT.update({"wave": ("wave", False), "wave_s": ("wave", True), "drop": ("drop", False), "drop_s": ("drop", True),
                   "foam": ("foam", False), "foam_s": ("foam", True), "crown": ("crown", False), "crown_s": ("crown", True)})
HAS_CROWN = os.path.exists(os.path.join(fx.HERE, "hat_gpt", "crown_0.png"))
CROWN = []  # phần hình chiếm trong khung vuông của từng ảnh nước toé GPT: (rộng, cao) theo tỉ lệ cạnh khung
if HAS_CROWN:
    for _i in range(4):
        _im = Image.open(os.path.join(fx.HERE, "hat_gpt", f"crown_{_i}.png"))
        _b = _im.getbbox()
        CROWN.append(((_b[2] - _b[0]) / _im.width, (_b[3] - _b[1]) / _im.height))


def crown(sim, feet, wd, life=0.42, group=FRONT):
    """vương miện nước mọc lên từ mặt đất rồi lún xuống (ảnh GPT nhìn ngang, chồng lớp như lưỡi sóng; đáy bám đất)."""
    if not HAS_CROWN:
        return
    p = P(feet, (0, 0), life, group=group, seed=sim.rng.randint(2), wd=wd)

    def draw(q, k):
        g = fx.ease_out(k / 0.28) if k < 0.28 else 1 - fx.smoothstep(0.5, 1.0, k)
        fw, fh = CROWN[q.seed]
        out = []
        for i, (c, f) in enumerate(zip(W, WF)):
            side = q.wd / fw * (0.6 + 0.4 * f)  # cạnh khung để hình rộng wd; lớp trong hẹp dần
            hgt = side * g * f ** 0.5
            if hgt < 2:
                continue
            ext = 5 if i == 0 else 0
            out.append(item(q.group, 34 + i * 0.1, "crown_s" if i == 0 else "crown", q.seed, c, q.pos - np.array([0.0, fh * hgt / 2]),
                            hgt + ext, (side + ext) / (hgt + ext)))
        return out
    p.draw = draw
    sim.add(p)


def burst_flash(sim, c, size, group=FRONT, life=0.14):
    """chớp nước toé nhìn thẳng: ảnh GPT xám chồng lớp (mực, xanh đậm, xanh trời, xanh nhạt, bọt); chưa có thì dùng ảnh no_nuoc."""
    f = P(c, (0, 0), life, group=group, ang=sim.rng.uniform(0, 360), seed=2 + sim.rng.randint(2), sz=size)
    if HAS_CROWN:
        f.draw = lambda q, k: [item(q.group, 33 + i * 0.1, "crown_s" if i == 0 else "crown", q.seed, c_,
                                    q.pos, q.sz * (0.6 + 0.5 * fx.ease_out(k / 0.6)) * f_ + (5 if i == 0 else 0), 1.0, q.ang)
                               for i, (c_, f_) in enumerate(zip(W, [1.0, 1.0, 0.8, 0.6, 0.4]))]
    else:
        f.draw = lambda q, k: [item(q.group, 33, "no_nuoc", 0, None, q.pos, q.sz * 0.85 * (0.6 + 0.5 * fx.ease_out(k / 0.6)), 1.0, q.ang)]
    sim.add(f)


def stage_geo(stage):
    im, _ = stage.heroes["me"]
    w, h = im.width / fx.K, im.height / fx.K
    return ME + np.array([-0.44 * w, -0.6 * h]), w, h


# ---------------- hạt nước ----------------
def draw_wave(p, k):
    """lưỡi sóng chồng lớp: lớp sáng dồn về NGỌN (bọt trắng ở mào sóng), ngược với lửa (lõi ở chân)."""
    r = p.r0 + (p.r1 - p.r0) * fx.ease_out(k / 0.3)
    r *= 1 - fx.smoothstep(p.fade, 1.0, k)
    if r < 1:
        return []
    sp = float(np.hypot(*p.vel))
    d = unit(unit(p.vel) * 0.6 * p.tip + np.array([0.0, -p.up])) if sp > 30 else np.array([0.0, -1.0])
    ang = fx.tip_angle(d)
    out = []
    for i, (c, f) in enumerate(zip(W, WF)):
        rad = r * f
        if rad < 1:
            continue
        out.append(item(p.group, 20 + i, "wave_s" if i == 0 else "wave", p.seed % 4, c, p.pos + d * (r - rad) * 0.55,
                        2.7 * rad + (5 if i == 0 else 0), 1.0, ang))
    return out


def wave_p(sim, pos, vel, life, r0, r1, group=FRONT, tip=1.0, up=0.25, drag=1.0, acc=(0, 0), fade=0.72, foam_p=0.0):
    rng = sim.rng
    p = P(pos, vel, life, drag=drag, acc=np.array(acc, float), seed=rng.randint(4), r0=r0, r1=r1, group=group, tip=tip, up=up,
          fade=fade, ph=rng.uniform(0, 6.28))
    p.draw = draw_wave
    if foam_p:
        p.on_death = lambda q, s: foam(s, q.pos, group=q.group) if s.rng.uniform() < foam_p else None
    return sim.add(p)


def draw_drop(p, k):
    s = 2.6 * p.r * (1 - fx.smoothstep(0.8, 1.0, k))
    if s < 1:
        return []
    sp = float(np.hypot(*p.vel))
    d = p.vel / sp if sp > 5 else np.array([0.0, 1.0])
    ang = fx.tip_angle(-d)  # đuôi nhọn ở phía sau hướng bay
    return [item(p.group, 40, "drop_s", p.seed, INK, p.pos, s + 4, 1.0, ang),
            item(p.group, 40.3, "drop", p.seed, W[2], p.pos, s, 1.0, ang),
            item(p.group, 40.6, "drop", p.seed, W[3], p.pos + d * s * 0.1, s * 0.56, 1.0, ang)]


def plop(sim, pos):
    """giọt chạm đất: vòng sóng nhỏ loang rồi tan."""
    fx.ring(sim, pos, 0.3, 2, 11, col=FOAM, squash=0.36, group=FLOOR, band=(2.5, 1.0), ink=False)


def drop(sim, pos, vel, life=None, r=5.0, grav=900.0, group=FRONT, ground=None, drag=0.6):
    rng = sim.rng
    p = P(pos, vel, life or rng.uniform(0.5, 0.9), drag=drag, acc=np.array([0, grav]), seed=rng.randint(4), r=r, group=group)
    if ground is not None:
        p.ground = ground
        p.life = 2.0
        p.on_ground = lambda q, s: (plop(s, q.pos), setattr(q, "dead", True))
    p.draw = draw_drop
    return sim.add(p)


def foam(sim, pos, vel=None, life=None, r0=4.0, r1=11.0, group=FRONT):
    rng = sim.rng
    v = vel if vel is not None else np.array([rng.uniform(-20, 20), rng.uniform(-40, -10)])
    p = P(pos, v, life or rng.uniform(0.45, 0.75), drag=2.5, seed=rng.randint(4), r0=r0, r1=r1, group=group,
          ang=rng.uniform(0, 6.28), spin=rng.uniform(-1, 1))

    def draw(q, k):
        r = q.r0 + (q.r1 - q.r0) * fx.ease_out(k / 0.25) if k < 0.25 else q.r1 * (1 - 0.9 * fx.smoothstep(0.25, 1.0, k))
        a = 1 - fx.smoothstep(0.7, 1.0, k)
        if r < 1 or a < 0.03:
            return []
        g = math.degrees(q.ang)
        return [item(q.group, 30, "foam_s", q.seed, INK, q.pos, 2 * r + 3.5, 1.0, g, a),
                item(q.group, 31, "foam", q.seed, FOAM, q.pos, 2 * r, 1.0, g, a)]
    p.draw = draw
    return sim.add(p)


def ripple(sim, pos, R0, R1, life=0.5, col=None, band=(9.0, 3.0)):
    """vòng sóng dưới đất: dải xanh dày có viền mực + một vòng bọt trắng mảnh bên trong (không viền)."""
    fx.ring(sim, pos, life, R0 * 0.82, R1 * 0.82, col=FOAM, squash=0.3, group=FLOOR, layer=30.8, band=(3.0, 1.0), ink=False)
    return fx.ring(sim, pos, life, R0, R1, col=col or W[2], squash=0.3, group=FLOOR, band=band)


def splash(sim, c, sc=1.0, ground=None, group=FRONT):
    """nước toé lúc trúng: một khung hình toé (ảnh vẽ tay đã duyệt) 0,14 s, vành lưỡi sóng toả đều, giọt văng vòng cung, bọt,
    vòng sóng dưới đất."""
    rng = sim.rng
    burst_flash(sim, c, 0.72 * H * sc, group)
    n = int(8 * sc + 1)
    for i in range(n):
        a = 2 * math.pi * (i + rng.uniform(-0.3, 0.3)) / n
        wave_p(sim, c + rng.uniform(-4, 4, 2), np.array([math.cos(a), math.sin(a)]) * rng.uniform(200, 330) * sc, rng.uniform(0.3, 0.42),
               8 * sc, rng.uniform(14, 19) * sc, group, tip=1.0, up=0.15, drag=4.5, acc=(0, 300))
    gy = ground if ground is not None else c[1] + 0.45 * H
    for _ in range(int(14 * sc)):
        a = math.radians(-90 + rng.uniform(-85, 85))
        drop(sim, c + rng.uniform(-6, 6, 2), np.array([math.cos(a), math.sin(a)]) * rng.uniform(240, 460) * sc, r=rng.uniform(3, 6),
             ground=gy + rng.uniform(-10, 18), group=group if rng.uniform() < 0.6 else BACK)
    for _ in range(int(5 * sc)):
        foam(sim, c + rng.uniform(-18, 18, 2) * sc, r1=rng.uniform(9, 14) * sc, group=group)
    feet = np.array([c[0], gy])
    crown(sim, feet + np.array([0.0, 4.0]), 0.78 * H * sc, group=FRONT)
    ripple(sim, feet, 0.12 * H, 0.75 * H * sc)
    sim.at(sim.t + 0.12, lambda s: ripple(s, feet, 0.08 * H, 0.5 * H * sc, col=W[3]))


def orb(sim, c_fn, t_grow, t_end, r_end, r_fn=None, group=FRONT):
    """cầu nước: bốn lớp tròn chồng nhau, rung nhẹ (co giãn lệch pha), hai vòng xoắn quay bên trong, cụm bọt nhỏ bám mép dưới."""
    t0 = sim.t
    p = P(c_fn(0), (0, 0), t_end, group=group, seed=sim.rng.randint(4))

    def upd(q, dt, s):
        new = c_fn(s.t - t0)
        q.vel = (new - q.pos) / max(dt, 1e-5) * 0.0
        q.dpos = new - q.pos
        q.pos = new
    p.dpos = np.zeros(2)
    p.upd = upd

    def draw(q, k):
        age = q.age
        r = r_fn(age) if r_fn else r_end * fx.ease_out(age / t_grow)
        r *= 1 - fx.smoothstep(0.93, 1.0, k) if r_fn is None else 1.0
        if r < 1.5:
            return []
        wob = 1 + 0.07 * math.sin(age * 15)
        mv = float(np.hypot(*q.dpos))
        ang = -math.degrees(math.atan2(q.dpos[1], q.dpos[0])) if mv > 0.3 else 0
        st = wob * (1 + min(0.25, mv / 14))
        out = [item(q.group, 20, "solid", q.seed, INK, q.pos, 2 * r / wob + 5, st, ang),
               item(q.group, 21, "blob", q.seed, W[1], q.pos, 2 * r / wob, st, ang),
               item(q.group, 22, "blob", (q.seed + 1) % 4, W[2], q.pos + np.array([0, -r * 0.08]), 1.66 * r / wob, st, ang),
               item(q.group, 23, "blob", (q.seed + 2) % 4, W[3], q.pos + np.array([-r * 0.12, -r * 0.2]), 1.1 * r, 1.0, ang)]
        for j in range(2):  # dòng nước xoáy bên trong
            a = age * 7 + j * math.pi
            out.append(item(q.group, 24, "curl", j, W[4] if j == 0 else W[3], q.pos + np.array([math.cos(a), math.sin(a) * 0.7]) * r * 0.3,
                            r * 0.7, 1.0, math.degrees(-a)))
        fp = q.pos + np.array([r * 0.42, r * 0.62])
        out += [item(q.group, 25, "foam_s", 1, INK, fp, r * 0.62 + 3, 1.0, 0), item(q.group, 25.5, "foam", 1, FOAM, fp, r * 0.62, 1.0, 0)]
        return out
    p.draw = draw
    return sim.add(p)


def gather(sim, c_fn, t0, t1, reach=85.0, rate=60.0, group=FRONT):
    """tụ nước về điểm c_fn(t): giọt và lưỡi sóng nhỏ bay xoáy trôn ốc vào tâm, vòng nước co lại dần."""
    def inflow(s, x):
        rng = s.rng
        a0 = rng.uniform(0, 2 * math.pi)
        R = rng.uniform(0.7, 1.0) * reach
        life = rng.uniform(0.3, 0.42)
        big = rng.uniform() < 0.3
        c0 = c_fn(s.t)
        q = P(c0 + np.array([math.cos(a0), math.sin(a0) * 0.8]) * R, (0, 0), life, seed=rng.randint(4), group=group,
              r=rng.uniform(3, 5.5), r0=5, r1=rng.uniform(7, 10), tip=1.0, up=0.0, fade=0.75, a0=a0, R=R)

        def upd(z, dt, ss):
            k = min(1.0, z.age / z.life)
            a = z.a0 + 4.5 * k * k
            rr = z.R * (1 - k) ** 1.3
            new = c_fn(ss.t) + np.array([math.cos(a), math.sin(a) * 0.8]) * rr
            z.vel = (new - z.pos) / max(dt, 1e-5)
            z.pos = new - z.vel * dt
        q.upd = upd
        q.draw = draw_wave if big else draw_drop
        s.add(q)
    sim.every(t0, t1, rate, inflow)
    n = max(1, int((t1 - t0) / 0.22))
    for i in range(n):
        sim.at(t0 + i * 0.22, lambda s: fx.ring(s, c_fn(s.t), 0.34, reach * 0.9, reach * 0.16, col=W[3], squash=1.0, group=group,
                                                 layer=18, band=(2.0, 4.0), ink=False))


def bubble(sim, pos, vel, life, r, group=FRONT, on_pop=None):
    rng = sim.rng
    p = P(pos, vel, life, group=group, seed=rng.randint(4), r=r, ph=rng.uniform(0, 6.28))

    def draw(q, k):
        rr = q.r * min(1.0, q.age / 0.12) * (1 + 0.05 * math.sin(q.age * 11 + q.ph))
        st = 1 + 0.06 * math.sin(q.age * 9 + q.ph)
        return [item(q.group, 26, "solid", q.seed, INK, q.pos, 2 * rr + 4, st),
                item(q.group, 27, "blob", q.seed, W[2], q.pos, 2 * rr, st),
                item(q.group, 28, "blob", (q.seed + 1) % 4, W[3], q.pos + np.array([-rr * 0.06, -rr * 0.08]), 1.68 * rr, st),
                item(q.group, 29, "blob", (q.seed + 2) % 4, (214, 240, 252), q.pos + np.array([-rr * 0.14, -rr * 0.18]), 1.1 * rr),
                item(q.group, 29.5, "foam", 2, FOAM, q.pos + np.array([rr * 0.4, rr * 0.5]), rr * 0.5)]
    p.draw = draw

    def pop(q, s):
        burst_flash(s, q.pos, q.r * 4.2, q.group, life=0.1)
        for _ in range(5):
            a = s.rng.uniform(0, 2 * math.pi)
            drop(s, q.pos, np.array([math.cos(a), math.sin(a) - 0.4]) * s.rng.uniform(120, 240), life=0.4, r=q.r * 0.3, group=q.group)
        foam(s, q.pos, r1=q.r * 0.8, group=q.group)
        if on_pop:
            on_pop(q, s)
    p.on_death = pop
    return sim.add(p)


def hit_tint(s, amt=0.4, decay=1.2):
    s.hero_fx["foe"] = {"tint": TINT, "amt": amt, "decay": decay}


# ---------------- 1. tụ nước ----------------
def tu_nuoc(sim):
    mouth, w, h = sim.geo
    c = ME + np.array([0.0, -1.12 * h])  # tụ trên đầu tướng
    c_fn = lambda t: c + np.array([0.0, 3.0 * math.sin(t * 5)])
    gather(sim, c_fn, 0.0, 1.05, reach=95, rate=70)
    orb(sim, c_fn, 1.0, 1.55, 30)

    def absorb(s):  # cầu nước vỡ, thấm xuống tướng: lưỡi sóng đổ xuống quanh thân, vòng nước loang dưới chân, tướng ửng xanh
        s.hero_fx["me"] = {"tint": TINT, "amt": 0.55, "decay": 0.9}
        burst_flash(s, c, 0.6 * H)
        for i in range(16):
            sd = -1 if i % 2 else 1
            g = BACK if i % 3 else FRONT
            wave_p(s, c + np.array([sd * s.rng.uniform(4, 16), 0]), np.array([sd * s.rng.uniform(80, 220), s.rng.uniform(-120, 40)]),
                   s.rng.uniform(0.45, 0.65), 7, s.rng.uniform(12, 17) * (0.75 if g == FRONT else 1), g, tip=1.0, up=-0.1, drag=1.5,
                   acc=(0, 900))
        for _ in range(14):
            a = math.radians(-90 + s.rng.uniform(-80, 80))
            drop(s, c, np.array([math.cos(a), math.sin(a)]) * s.rng.uniform(160, 320), r=s.rng.uniform(3, 5), ground=ME[1] + s.rng.uniform(-10, 14))
        ripple(s, ME + np.array([0, -2]), 0.2 * w, 0.75 * w, life=0.6)
        s.at(s.t + 0.18, lambda ss: ripple(ss, ME + np.array([0, -2]), 0.15 * w, 0.55 * w, life=0.5, col=W[3]))
    sim.at(1.55, absorb)
    sim.every(1.6, 2.2, 10, lambda s, x: foam(s, ME + np.array([s.rng.uniform(-0.3, 0.3) * w, -s.rng.uniform(0.1, 0.8) * h]),
                                              vel=np.array([0, -40.0]), r1=8, group=FRONT if s.rng.uniform() < 0.5 else BACK))


# ---------------- 2. tia nước ----------------
def tia_nuoc(sim):
    mouth, w, h = sim.geo
    tgt = FOE + np.array([0.0, -0.45 * H])
    dd = tgt - mouth
    dist = float(np.hypot(*dd))
    u = dd / dist
    nrm = np.array([-u[1], u[0]])
    src = mouth + u * 14
    T0, T1, SP = 0.42, 1.3, 1150.0
    travel = (dist - 30) / SP
    gather(sim, lambda t: src, 0.0, T0 - 0.04, reach=60, rate=55)
    # cầu nguồn ở miệng: lớn lên lúc tụ, nhỏ dần khi tia xả hết
    orb(sim, lambda t: src, T0, T1 + 0.05, 17,
        r_fn=lambda a: 17 * fx.ease_out(a / T0) if a < T0 else 17 * (1 - 0.6 * (a - T0) / (T1 - T0)) * (1 - fx.smoothstep(T1 - 0.1, T1 + 0.05, a)))
    sim.at(T0, lambda s: (s.shake(0.2), [foam(s, src + s.rng.uniform(-8, 8, 2), r1=10) for _ in range(4)]))

    # lõi tia LIỀN (mảng tô phẳng) nối miệng tới chỗ trúng, lượn nhẹ; các lưỡi sóng chạy đè lên làm mép cuộn
    core = P(src, (0, 0), T1 + travel + 0.1 - T0, group=FRONT)

    def core_draw(q, k):
        a = q.age
        head, tail = min(dist - 18, SP * a), max(0.0, SP * (a - (T1 - T0)))
        if head - tail < 30:
            return []
        ss_ = np.arange(tail, head + 0.1, 12.0)

        def side(wf, off):
            L, R = [], []
            for x in ss_:
                hw = (7.5 + 1.6 * math.sin(x * 0.07 - a * 30)) * min(1.0, (x - tail) / 26 + 0.25, (head - x) / 16 + 0.45)
                c = src + u * x + nrm * (3.0 * math.sin(x * 0.045 - a * 22) + off * hw)
                L.append(c + nrm * hw * wf)
                R.append(c - nrm * hw * wf)
            return L + R[::-1]
        return [fx.poly(FRONT, 9.0, side(1.0, 0), INK, 1.0, grow=2.4), fx.poly(FRONT, 9.1, side(1.0, 0), W[1]),
                fx.poly(FRONT, 9.2, side(0.66, -0.12), W[2]), fx.poly(FRONT, 9.3, side(0.28, -0.3), W[3])]
    core.draw = core_draw
    sim.at(T0, lambda s: s.add(core))

    def jet(s, x):
        rng = s.rng
        a = rng.uniform(-1, 1) * math.radians(2.5)
        dv = u * math.cos(a) + nrm * math.sin(a)
        q = wave_p(s, src + dv * rng.uniform(0, 10) + nrm * rng.uniform(-3, 3), dv * SP * rng.uniform(0.95, 1.05), travel * rng.uniform(0.95, 1.08),
                   14, rng.uniform(17, 22), FRONT, tip=1.0, up=0.12, drag=0.0, fade=0.9, foam_p=0.35)
        q.upd = lambda z, dt, ss: z.vel.__iadd__(nrm * math.sin(z.age * 24 + z.ph) * 700 * dt)  # dòng nước lượn
    sim.every(T0, T1, lambda s, x: 90 * (1.4 if x < 0.1 else 1.0) * min(1.0, (1 - x) * (T1 - T0) / 0.14), jet)
    # giọt văng hai bên dọc tia
    sim.every(T0 + 0.05, T1, 26, lambda s, x: drop(
        s, src + u * dist * s.rng.uniform(0.15, 0.85) + nrm * s.rng.choice([-1, 1]) * 10,
        u * s.rng.uniform(120, 260) + nrm * s.rng.choice([-1, 1]) * s.rng.uniform(90, 200) + np.array([0, -60.0]), r=s.rng.uniform(2.5, 4.5),
        ground=ME[1] + (FOE[1] - ME[1]) * s.rng.uniform(0.2, 0.9) + s.rng.uniform(0, 30)))
    # chỗ trúng: bọt cuộn, giọt bắn ngược, vòng sóng dưới chân đối thủ
    t_hit = T0 + travel

    def spray(s, x):
        a = math.atan2(-u[1], -u[0]) + s.rng.uniform(-1.3, 1.3)
        drop(s, tgt + s.rng.uniform(-10, 10, 2), np.array([math.cos(a), math.sin(a) - 0.5]) * s.rng.uniform(200, 420), r=s.rng.uniform(3, 5.5),
             ground=FOE[1] + s.rng.uniform(-10, 18), group=FRONT if s.rng.uniform() < 0.6 else BACK)
    sim.every(t_hit, T1 + travel, 38, spray)
    sim.every(t_hit, T1 + travel, 22, lambda s, x: foam(s, tgt + s.rng.uniform(-16, 16, 2), vel=s.rng.uniform(-60, 60, 2), r1=s.rng.uniform(9, 14)))
    sim.every(t_hit, T1 + travel, 9, lambda s, x: wave_p(s, tgt + s.rng.uniform(-8, 8, 2),
                                                         np.array([s.rng.choice([-1, 1]) * s.rng.uniform(120, 240), -s.rng.uniform(60, 200)]),
                                                         0.34, 7, s.rng.uniform(12, 16), FRONT, tip=1.0, up=0.3, drag=4.0, acc=(0, 500)))
    for i in range(4):
        sim.at(t_hit + i * 0.24, lambda s: (ripple(s, FOE + np.array([0, 2]), 0.15 * H, 0.7 * H),
                                            crown(s, FOE + np.array([s.rng.uniform(-10, 10), 6.0]), 0.7 * H, life=0.36)))

    def first(s):
        s.shake(0.3)
        hit_tint(s, 0.4, 0.5)
    sim.at(t_hit, first)
    sim.at(T1 + travel, lambda s: (splash(s, tgt, 0.8, ground=FOE[1]), hit_tint(s, 0.4, 1.2)))


# ---------------- 3. cầu nước ----------------
def cau_nuoc(sim):
    mouth, w, h = sim.geo
    src = mouth + np.array([-16.0, -10.0])
    tgt = FOE + np.array([0.0, -0.45 * H])
    T0, TT, ARC = 0.6, 0.55, 70.0

    def path(t):
        if t < T0:
            return src + np.array([0.0, 2.5 * math.sin(t * 9)])
        x = min(1.0, (t - T0) / TT)
        return src + (tgt - src) * x + np.array([0.0, -4 * ARC * x * (1 - x)])
    gather(sim, path, 0.0, T0 - 0.05, reach=90, rate=75)
    orb(sim, path, T0 - 0.05, T0 + TT, 30)
    sim.at(T0, lambda s: (s.shake(0.15), [foam(s, src + s.rng.uniform(-10, 10, 2), r1=11) for _ in range(4)]))
    sim.every(T0, T0 + TT, 34, lambda s, x: drop(s, path(s.t) + s.rng.uniform(-14, 14, 2), np.array([s.rng.uniform(-50, 50), s.rng.uniform(-40, 60)]),
                                                 r=s.rng.uniform(3, 5), ground=ME[1] + (FOE[1] - ME[1]) * x + s.rng.uniform(-5, 30)))
    sim.every(T0, T0 + TT, 24, lambda s, x: foam(s, path(s.t) + s.rng.uniform(-10, 10, 2), vel=np.array([0, -15.0]), r0=4, r1=s.rng.uniform(8, 12)))
    sim.every(T0, T0 + TT, 30, lambda s, x: wave_p(s, path(s.t), -unit(path(s.t + 0.02) - path(s.t)) * s.rng.uniform(40, 120) + s.rng.uniform(-40, 40, 2),
                                                   0.22, 9, 13, FRONT, tip=1.0, up=0.1, drag=3.0))

    def hit(s):
        s.shake(0.6)
        s.flash = 0.12
        hit_tint(s, 0.5, 0.9)
        splash(s, tgt, 1.25, ground=FOE[1])
        # cột nước dựng lên sau lưng đối thủ
        s.every(s.t, s.t + 0.28, 80, lambda ss, x: wave_p(ss, FOE + np.array([ss.rng.uniform(-0.3, 0.3) * H, -4]),
                                                          np.array([ss.rng.uniform(-50, 50), -ss.rng.uniform(380, 620) * (1 - 0.4 * x)]),
                                                          ss.rng.uniform(0.4, 0.55), 8, ss.rng.uniform(16, 24), BACK, tip=1.0, up=0.5, drag=1.6,
                                                          acc=(0, 900), foam_p=0.5))
        # mưa giọt rơi lại
        s.every(s.t + 0.3, s.t + 0.75, 40, lambda ss, x: drop(ss, FOE + np.array([ss.rng.uniform(-0.8, 0.8) * H, -ss.rng.uniform(0.9, 1.4) * H]),
                                                               np.array([ss.rng.uniform(-20, 20), 120.0]), r=ss.rng.uniform(3, 5),
                                                               ground=FOE[1] + ss.rng.uniform(-10, 20),
                                                               group=FRONT if ss.rng.uniform() < 0.5 else BACK))
        pud = P(FOE + np.array([0, 3]), (0, 0), 1.3, group=FLOOR)
        pud.draw = lambda q, k: [item(FLOOR, 2, "ell", 0, INK, q.pos, (22 + 4) * min(1, k / 0.12) * (1 - k ** 3), 3.3, 0, 0.9),
                                 item(FLOOR, 3, "ell", 0, W[2], q.pos, 22 * min(1, k / 0.12) * (1 - k ** 3), 3.4),
                                 item(FLOOR, 4, "ell", 0, W[3], q.pos + np.array([-6, -1]), 12 * min(1, k / 0.12) * (1 - k ** 2), 3.8)]
        s.add(pud)
    sim.at(T0 + TT, hit)


# ---------------- 4. bong bóng ----------------
def bong_bong(sim):
    mouth, w, h = sim.geo
    tgt = FOE + np.array([0.0, -0.45 * H])
    src = mouth + np.array([-10.0, -4.0])
    dd = unit(tgt - src)
    nrm = np.array([-dd[1], dd[0]])

    def blow(s, x, big=False):
        rng = s.rng
        r = 26.0 if big else rng.uniform(8, 15)
        aim = tgt + (np.zeros(2) if big else np.array([rng.uniform(-0.25, 0.25) * H, rng.uniform(-0.25, 0.25) * H]))
        sp = 250.0 if big else rng.uniform(300, 420)
        q = bubble(s, src + rng.uniform(-6, 6, 2), dd * sp * 0.4 + nrm * rng.uniform(-120, 120), 2.2, r)
        q.aim, q.sp, q.big = aim, sp, big

        def upd(z, dt, ss):
            to = z.aim - z.pos
            dist = float(np.hypot(*to))
            want = to / max(dist, 1e-5) * z.sp + nrm * math.sin(z.age * 6 + z.ph) * 90
            z.vel += (want - z.vel) * min(1.0, 4.0 * dt)
            if dist < 16 + z.r * 0.4:
                z.dead = True
        q.upd = upd

        def on_pop(z, ss):
            ss.shake(0.5 if z.big else 0.1)
            hit_tint(ss, 0.5 if z.big else 0.3, 1.0 if z.big else 3.0)
            if z.big:
                splash(ss, z.pos, 0.9, ground=FOE[1])
            else:
                ripple(ss, FOE + np.array([0, 2]), 0.1 * H, 0.4 * H, life=0.35, col=W[3], band=(3.0, 1.0))
        q.on_pop_cb = on_pop
        old = q.on_death
        q.on_death = lambda z, ss: (old(z, ss), on_pop(z, ss))
    sim.every(0.1, 0.95, 12, blow)
    sim.every(0.1, 0.95, 16, lambda s, x: foam(s, src + s.rng.uniform(-6, 6, 2), vel=dd * 60 + s.rng.uniform(-30, 30, 2), r0=3, r1=7))
    sim.at(1.0, lambda s: blow(s, 0, big=True))


def smooth(pts, n=5):
    """đường cong kín Catmull-Rom đi qua các điểm (cho mảng nước liền có mép mềm)."""
    Q = [np.array(q, float) for q in pts]
    m = len(Q)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[(i + 1) % m], Q[(i + 2) % m]
        for j in range(n):
            t = j / n
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    return out


def water_shape(group, layer, pts, mid=None, k2=0.78, k3=0.45, shift=(0, 0), alpha=1.0):
    """một mảng nước LIỀN tô phẳng: mực, xanh đậm, xanh trời (thu về mid theo k2), xanh nhạt (k3). k là số hoặc (kx, ky).
    Chỉ dùng cho hình lồi quanh mid; hình có chỗ lõm (sóng cuộn) thì tự vẽ từng lớp bằng fx.poly."""
    pts = [np.array(q, float) for q in pts]
    c = np.mean(pts, axis=0) if mid is None else np.array(mid, float)
    sh = np.array(shift, float)
    k2, k3 = np.array(k2, float) * np.ones(2), np.array(k3, float) * np.ones(2)
    return [fx.polys(group, layer, [(pts, INK, 2.4), (pts, W[1], 0), ([c + (q - c) * k2 + sh for q in pts], W[2], 0),
                                    ([c + (q - c) * k3 + sh * 2 for q in pts], W[3], 0)], alpha)]


def puddle(s, pos, R=22.0, life=1.3):
    pud = P(pos, (0, 0), life, group=FLOOR)
    pud.draw = lambda q, k: [item(FLOOR, 2, "ell", 0, INK, q.pos, (R + 4) * min(1, k / 0.12) * (1 - k ** 3), 3.3, 0, 0.9),
                             item(FLOOR, 3, "ell", 0, W[2], q.pos, R * min(1, k / 0.12) * (1 - k ** 3), 3.4),
                             item(FLOOR, 4, "ell", 0, W[3], q.pos + np.array([-6, -1]), R * 0.55 * min(1, k / 0.12) * (1 - k ** 2), 3.8)]
    s.add(pud)


def rain_back(s, c, n=16, spread=0.8, t0=0.3, t1=0.75):
    """mưa giọt rơi lại quanh c sau khi nước bắn lên."""
    s.every(s.t + t0, s.t + t1, n / (t1 - t0), lambda ss, x: drop(
        ss, c + np.array([ss.rng.uniform(-spread, spread) * H, -ss.rng.uniform(0.9, 1.35) * H]), np.array([ss.rng.uniform(-20, 20), 120.0]),
        r=ss.rng.uniform(3, 5), ground=c[1] + ss.rng.uniform(-10, 20), group=FRONT if ss.rng.uniform() < 0.5 else BACK))


# ---------------- 5. vòi rồng nước (làm lại 2026-11-10, hai lần) ----------------
# Bản 1: lưỡi sóng bay vòng loạn pha + dải cung: không có thân, người dùng chê xấu. Bản 2: một phễu liền nhẵn: cứng, tối, như cái xô.
# Bản này: phễu = chồng VÒNG NƯỚC dẹt, mỗi vòng có viền mực, lắc ngang lệch pha theo độ cao (lốc hoạt hình vẽ tay).
def voi_rong(sim):
    """phễu là 8 vòng nước dẹt xếp chồng, vòng trên to hơn và đè lên vòng dưới, cả chồng lắc ngang lệch pha (uốn như con rắn)
    và nghiêng qua lại; mỗi vòng ba màu phẳng. Thân nằm SAU đối thủ, phía trước chỉ có lớp nước mỏng trong, sọc bọt trượt và các
    lưỡi sóng xoắn nên vẫn thấy đối thủ. Chân vòi hút nước vào, miệng phễu sủi bọt, giọt văng; cuối cùng sụp xuống toé ra."""
    C = FOE + np.array([0.0, 4.0])
    HT, TA, T_UP, T1, T_END, N = 1.27 * H, 0.25, 0.35, 1.9, 2.3, 8

    def grow(t):
        t -= TA
        return 0.0 if t <= 0 else fx.ease_out(min(1.0, t / T_UP)) * (1 - fx.smoothstep(T1 - TA, T_END - TA, t))

    radius = lambda hh: 16 + 72 * hh ** 1.15
    sway = lambda hh, t: math.sin(t * 7.5 - hh * 5.0)

    def centre(hh, t):
        return C + np.array([(4 + 24 * hh) * sway(hh, t), -hh * HT * grow(t)])

    def ring(i, t, kx=1.0, ky=1.0, dx=0.0, dy=0.0):
        g = grow(t)
        hh = (i + 0.5) / N
        c = centre(hh, t)
        r, hr = radius(hh) * (0.5 + 0.5 * g), HT * g / N * 0.86
        tl = 0.16 * math.sin(t * 7.5 - hh * 5.0 + 1.3)
        ca, sa = math.cos(tl), math.sin(tl)
        out = []
        for a in np.linspace(0, 2 * math.pi, 22, endpoint=False):
            x, y = dx * r + kx * r * math.cos(a), dy * hr + ky * hr * math.sin(a)
            out.append((c[0] + x * ca - y * sa, c[1] + x * sa + y * ca))
        return out

    # nước quanh chân bị hút vào
    def suck(s, x):
        a = s.rng.uniform(0, 6.28)
        pos = C + np.array([math.cos(a) * 1.0 * H, math.sin(a) * 0.3 * H])
        drop(s, pos, (C - pos) * 2.6 + np.array([-math.sin(a), math.cos(a) * 0.3]) * 150, life=0.38, r=s.rng.uniform(3, 4.5), grav=0,
             group=FRONT if math.sin(a) > 0 else BACK, drag=0)
    sim.every(0.0, T1, 26, suck)
    for i in range(7):
        sim.at(0.05 + i * 0.28, lambda s: ripple(s, C, 0.9 * H, 0.2 * H, life=0.4, col=W[3], band=(3.0, 7.0)))
    sim.at(TA, lambda s: (s.shake(0.35), crown(s, C + np.array([0.0, 4.0]), 0.75 * H, life=0.5)))

    body = P(C, (0, 0), T_END, group=FRONT)

    def body_draw(q, k):
        t = q.age
        if grow(t) < 0.05:
            return []
        shapes = []
        for i in range(N):  # vòng trên vẽ sau nên đè lên vòng dưới
            shapes += [(ring(i, t), INK, 2.2), (ring(i, t), W[1], 0), (ring(i, t, 0.92, 0.6, 0.0, 0.12), W[2], 0),
                       (ring(i, t, 0.36, 0.22, -0.42, 0.22), W[3], 0)]
        return [fx.polys(FRONT, 18.0, shapes, 0.78)]
    body.draw = body_draw
    sim.add(body)

    # sọc bọt trượt quanh mặt trước của phễu (nửa dưới elip là phía gần)
    def stripe(s, x):
        q = P(C, (0, 0), s.rng.uniform(0.45, 0.6), tb=s.t, span=int(s.rng.uniform(60, 100)), col=FOAM if s.rng.uniform() < 0.65 else W[3],
              h0=s.rng.uniform(0.05, 0.3))

        def draw(z, k):
            t = z.tb + z.age
            hh = min(1.0, z.h0 + 0.75 * k)
            c = centre(hh, t)
            R = radius(hh) * 0.95
            a0 = int(8 + (164 - z.span) * k)  # trượt từ phải sang trái = phễu đang quay
            alpha = min(1.0, k / 0.15, (1 - k) / 0.25) * 0.95
            bw = (2.5 + 3.0 * (1 - abs(2 * k - 1))) * fx.K
            return [item(FRONT, 19.0, "arcpx0", a0 * 1000 + z.span, tuple(z.col) + (bw,), c, 2 * R * 0.3, 1 / 0.3, 0, alpha)]
        q.draw = draw
        s.add(q)
    sim.every(TA + 0.1, T1, 16, stripe)

    # mào sóng văng ra ở hai mép phễu (thấy rõ nước đang quay)
    def flick(s, x):
        hh = s.rng.uniform(0.15, 1.0)
        sd = s.rng.choice([-1, 1])
        c = centre(hh, s.t)
        wave_p(s, c + np.array([sd * radius(hh) * 0.9, 0.0]), np.array([sd * s.rng.uniform(120, 240), -s.rng.uniform(60, 200)]),
               s.rng.uniform(0.26, 0.38), 6, s.rng.uniform(11, 17) * (0.6 + 0.4 * hh), FRONT, tip=1.0, up=0.35, drag=3.0, acc=(0, 500),
               foam_p=0.25)
    sim.every(TA + 0.12, T1, 30, flick)

    # miệng phễu: bọt cuộn, giọt văng
    def rim(s, x):
        a = s.rng.uniform(0, 6.28)
        c = centre(1.0, s.t)
        R = radius(1.0)
        foam(s, c + np.array([R * math.cos(a), 0.3 * R * math.sin(a) + 4]), vel=np.array([math.cos(a) * 60, -s.rng.uniform(10, 50)]), r0=6,
             r1=s.rng.uniform(10, 15), group=FRONT if math.sin(a) > 0 else BACK)
    sim.every(TA + T_UP, T1 + 0.1, 26, rim)
    sim.every(TA + T_UP, T1, 26, lambda s, x: drop(
        s, centre(s.rng.uniform(0.5, 1.0), s.t) + np.array([s.rng.uniform(-30, 30), 0]),
        np.array([s.rng.choice([-1, 1]) * s.rng.uniform(170, 300), -s.rng.uniform(40, 160)]), r=s.rng.uniform(3, 5),
        ground=FOE[1] + s.rng.uniform(-10, 24), group=FRONT if s.rng.uniform() < 0.5 else BACK))

    def tint(s):
        t = P(C, (0, 0), T1 - TA)
        t.upd = lambda q, dt, ss: ss.hero_fx.__setitem__("foe", {"tint": TINT, "amt": 0.25 + 0.1 * math.sin(q.age * 16)})
        s.add(t)
    sim.at(TA + 0.05, tint)

    def end(s):  # vòi sụp: nước đổ xuống toé ra
        s.shake(0.4)
        hit_tint(s, 0.35, 1.0)
        splash(s, FOE + np.array([0.0, -0.3 * H]), 0.9, ground=FOE[1], group=BACK)
        rain_back(s, FOE, 16, 0.6, 0.0, 0.35)
        puddle(s, FOE + np.array([0, 3]), 20, 1.0)
    sim.at(T1 + 0.15, end)


# ---------------- 6. sóng thần ----------------
SONG = [(-1.3, 0.0), (-0.95, 0.24), (-0.55, 0.62), (-0.1, 0.94), (0.35, 1.0), (0.72, 0.86), (0.9, 0.6), (0.84, 0.4),  # lưng, đỉnh, mũi mào
        (0.68, 0.52), (0.48, 0.6), (0.3, 0.42), (0.32, 0.18), (0.5, 0.0), (-0.2, -0.04), (-0.8, -0.04)]               # bụng mào, mặt lõm, chân
SONG2 = [(-1.02, 0.05), (-0.8, 0.24), (-0.45, 0.55), (-0.05, 0.8), (0.35, 0.87), (0.64, 0.77), (0.76, 0.64), (0.5, 0.72), (0.18, 0.56),
         (0.12, 0.22), (0.3, 0.04), (-0.4, 0.0)]
SONG3 = [(-0.82, 0.14), (-0.5, 0.42), (-0.1, 0.66), (0.22, 0.74), (0.2, 0.62), (-0.1, 0.52), (-0.45, 0.28), (-0.7, 0.1)]
SONG_MAO = [(-0.1, 0.96), (0.2, 1.03), (0.5, 0.99), (0.76, 0.85), (0.9, 0.63), (0.83, 0.45)]


def song_than(sim):
    """nước tụ dưới chân tướng rồi MỘT CON SÓNG LIỀN có mào cuộn (mảng tô phẳng: lưng xanh đậm, dải xanh trời, vệt xanh nhạt)
    lăn về phía đối thủ, càng đi càng cao, mào phủ bọt trắng, chân sóng bắn lưỡi sóng nhỏ, để lại bọt và vòng sóng; tới nơi con
    sóng sụp xuống: nước chồm qua đầu đối thủ đổ ập, bọt tràn hai bên, mưa giọt, vũng nước."""
    mouth, w, h = sim.geo
    A = ME + np.array([-0.42 * w, -4.0])
    B = FOE + np.array([0.0, 4.0])
    u = unit(B - A)
    sx = 1.0 if u[0] > 0 else -1.0
    side = np.array([-u[1], u[0] * 0.35])
    T0, TT, TC, TR = 0.38, 0.62, 0.2, 0.14

    def front(t):
        x = min(1.0, max(0.0, (t - T0) / TT))
        return A + (B - sx * np.array([0.3 * H, 0.0]) - A) * (x * x * (3 - 2 * x)), x
    gather(sim, lambda t: A + np.array([0.0, -8.0]), 0.0, T0, reach=60, rate=50)
    sim.at(0.05, lambda s: ripple(s, ME + np.array([0, -2]), 0.2 * w, 0.6 * w))
    sim.at(T0 - TR, lambda s: (s.shake(0.25), crown(s, A + np.array([0, 4.0]), 0.6 * H)))

    body = P(A, (0, 0), TR + TT + TC, group=FRONT)

    def body_draw(q, k):
        t = T0 - TR + q.age
        c, pr = front(t)
        fall = 1 - fx.smoothstep(T0 + TT, T0 + TT + TC, t)
        hg = (0.55 + 0.6 * pr) * H * fx.ease_out(min(1.0, q.age / 0.22)) * fall
        wd = (0.5 + 0.25 * pr) * H * (1 + 0.6 * (1 - fall))
        if hg < 4:
            return []

        def shape(ctrl, wob=0.03):
            return smooth([(c[0] + sx * (f + wob * math.sin(t * 13 + i)) * wd,
                            c[1] - (v + (wob * math.sin(t * 11 + i * 1.7) if v > 0.08 else 0.0)) * hg) for i, (f, v) in enumerate(ctrl)])
        out = [fx.poly(FRONT, 22.0, shape(SONG), INK, 1.0, grow=2.6), fx.poly(FRONT, 22.1, shape(SONG), W[1]),
               fx.poly(FRONT, 22.2, shape(SONG2, 0.02), W[2]), fx.poly(FRONT, 22.3, shape(SONG3, 0.02), W[3])]
        for i, (f, v) in enumerate(SONG_MAO):  # bọt trắng phủ mào
            pos = np.array([c[0] + sx * f * wd, c[1] - v * hg])
            r = (0.13 + 0.03 * math.sin(t * 9 + i * 2)) * hg * (0.75 if i in (0, 5) else 1.0)
            out += [item(FRONT, 23.0, "foam_s", i % 4, INK, pos, 2 * r + 4), item(FRONT, 23.1, "foam", i % 4, FOAM, pos, 2 * r)]
        for i, f in enumerate((-1.15, -0.75, -0.35, 0.05, 0.42)):  # bọt sủi dọc chân sóng
            pos = np.array([c[0] + sx * f * wd, c[1] - 0.02 * hg])
            r = (0.07 + 0.02 * math.sin(t * 12 + i * 2.3)) * hg
            out += [item(FRONT, 23.0, "foam_s", (i + 1) % 4, INK, pos, 2 * r + 4), item(FRONT, 23.1, "foam", (i + 1) % 4, FOAM, pos, 2 * r)]
        return out
    body.draw = body_draw
    sim.at(T0 - TR, lambda s: s.add(body))

    def spray(s, x):  # lưỡi sóng nhỏ bắn ở chân và trước mặt sóng
        c, pr = front(s.t)
        sz = 9 + 8 * pr
        wave_p(s, c + np.array([sx * s.rng.uniform(0.1, 0.5) * H * 0.6, -s.rng.uniform(0, 14)]),
               np.array([sx * s.rng.uniform(160, 300), -s.rng.uniform(120, 300)]), s.rng.uniform(0.26, 0.36), sz * 0.6, sz, FRONT, tip=1.0,
               up=0.5, drag=2.0, acc=(0, 900), foam_p=0.3)
    sim.every(T0, T0 + TT, 46, spray)
    sim.every(T0, T0 + TT, 30, lambda s, x: foam(s, front(s.t)[0] - u * 0.75 * H + side * s.rng.uniform(-30, 30), vel=np.array([0.0, -8.0]),
                                                 r0=5, r1=s.rng.uniform(9, 13), group=BACK))
    sim.every(T0, T0 + TT, 7, lambda s, x: ripple(s, front(s.t)[0] - u * 0.8 * H, 8, 44, life=0.4, col=W[3], band=(5.0, 1.5)))
    sim.every(T0, T0 + TT, 26, lambda s, x: drop(s, front(s.t)[0] + np.array([sx * s.rng.uniform(-0.2, 0.5) * H, -s.rng.uniform(0.5, 1.0) * H]),
                                                 np.array([s.rng.uniform(-120, 120), -s.rng.uniform(100, 260)]), r=s.rng.uniform(3, 5),
                                                 ground=front(s.t)[0][1] + s.rng.uniform(-6, 20)))

    def crash(s):
        s.shake(0.75)
        s.flash = 0.12
        hit_tint(s, 0.5, 0.8)
        body_c = FOE + np.array([0.0, -0.4 * H])
        for i in range(18):  # nước chồm qua đầu rồi đổ xuống
            fr = s.rng.uniform() < 0.25
            wave_p(s, B + np.array([s.rng.uniform(-50, 50), -10.0]), np.array([s.rng.uniform(-150, 150) + u[0] * 120, -s.rng.uniform(380, 640)]),
                   s.rng.uniform(0.45, 0.65), 12, s.rng.uniform(20, 30) * (0.6 if fr else 1.0), FRONT if fr else BACK, tip=1.0, up=0.4, drag=1.5,
                   acc=(0, 1100), foam_p=0.6)
        splash(s, body_c, 1.1, ground=FOE[1])
        for _ in range(12):  # bọt tràn hai bên sát đất
            sd = s.rng.choice([-1, 1])
            foam(s, B + np.array([sd * s.rng.uniform(10, 40), s.rng.uniform(-6, 6)]), vel=np.array([sd * s.rng.uniform(120, 260), -s.rng.uniform(0, 30)]),
                 life=s.rng.uniform(0.6, 0.9), r0=6, r1=s.rng.uniform(11, 16), group=FRONT if s.rng.uniform() < 0.5 else BACK)
        rain_back(s, FOE, 18)
        puddle(s, FOE + np.array([0, 3]), 26, 1.4)
    sim.at(T0 + TT + 0.04, crash)


# ---------------- 7. mưa rào ----------------
def mua_rao(sim):
    """mây nước tụ trên đầu đối thủ rồi trút mưa: giọt dài rơi nhanh, giọt trúng người thì toé bọt, giọt chạm đất loang vòng, thỉnh
    thoảng bắn vương miện nhỏ; vũng nước lớn dần; hết mưa mây tan."""
    top = FOE + np.array([0.0, -1.2 * H])
    T0, T1 = 0.5, 1.65
    gather(sim, lambda t: top, 0.0, T0, reach=70, rate=45)
    for i in range(7):
        p = P(top, (0, 0), T1 + 0.5, seed=i % 4, off=np.array([(i - 3) * 27.0 + sim.rng.uniform(-6, 6), sim.rng.uniform(-9, 9) - (8 if i in (2, 3, 4) else 0)]),
              r=sim.rng.uniform(27, 36) * (1.15 if i in (2, 3, 4) else 1.0), ph=sim.rng.uniform(0, 6.28), group=FRONT)

        def draw(q, k):
            g = fx.ease_out(q.age / T0) * (1 - fx.smoothstep(T1, T1 + 0.5, q.age))
            r = q.r * g
            if r < 1.5:
                return []
            pos = top + q.off * g + np.array([0.0, 2.5 * math.sin(q.age * 4 + q.ph)])
            return [item(FRONT, 30, "foam_s", q.seed, INK, pos, 2 * r + 4), item(FRONT, 31, "foam", q.seed, (150, 186, 224), pos, 2 * r),
                    item(FRONT, 31.5, "foam", (q.seed + 1) % 4, (204, 226, 244), pos + np.array([-r * 0.15, -r * 0.22]), 1.3 * r)]
        p.draw = draw
        sim.add(p)

    def rain(s, x):
        x0 = s.rng.uniform(-0.8, 0.8) * H
        on_foe = abs(x0) < 0.38 * H and s.rng.uniform() < 0.6
        q = drop(s, top + np.array([x0, 12.0]), np.array([-50.0, s.rng.uniform(760, 940)]), r=s.rng.uniform(6.5, 9.5), grav=300,
                 ground=(FOE[1] - s.rng.uniform(0.45, 0.85) * H) if on_foe else FOE[1] + s.rng.uniform(-12, 22),
                 group=FRONT if (on_foe or s.rng.uniform() < 0.5) else BACK)
        q.seed = 1  # giọt dài thon
        if on_foe:
            def hitfoe(z, ss):
                foam(ss, z.pos, r1=7)
                for _ in range(2):
                    drop(ss, z.pos, np.array([ss.rng.uniform(-150, 150), -ss.rng.uniform(60, 170)]), life=0.3, r=2.6)
                z.dead = True
            q.on_ground = hitfoe
    sim.every(T0, T1, lambda s, x: 125 * min(1.0, x * 5), rain)
    sim.every(T0 + 0.15, T1 + 0.1, 5, lambda s, x: crown(s, FOE + np.array([s.rng.uniform(-0.6, 0.6) * H, s.rng.uniform(0, 14)]),
                                                         s.rng.uniform(0.25, 0.4) * H, life=0.3))
    for i in range(4):
        sim.at(T0 + 0.15 + i * 0.3, lambda s: ripple(s, FOE + np.array([0, 2]), 0.15 * H, 0.7 * H, col=W[3]))
    sim.at(T0 + 0.12, lambda s: (s.shake(0.2), puddle(s, FOE + np.array([0, 3]), 26, 1.7)))

    def tint(s):
        t = P(top, (0, 0), T1 - T0)
        t.upd = lambda q, dt, ss: ss.hero_fx.__setitem__("foe", {"tint": TINT, "amt": 0.22 + 0.08 * math.sin(q.age * 14)})
        s.add(t)
    sim.at(T0 + 0.1, tint)
    sim.at(T1, lambda s: hit_tint(s, 0.3, 1.0))


# ---------------- 8. thương nước ----------------
def thuong_nuoc(sim):
    """sáu mũi thương nước lần lượt tụ thành vòng cung trên đầu tướng (nở bật, nhỏ giọt), chĩa vào đối thủ rồi phóng lần lượt,
    kéo theo giọt và bọt; mỗi mũi trúng toé một chớp nước nhỏ."""
    mouth, w, h = sim.geo
    A = ME + np.array([-10.0, -1.08 * h])
    N, RA, LEN = 6, 0.42 * w, 62.0
    tgt = FOE + np.array([0.0, -0.42 * H])
    LF = [1.0, 1.0, 0.8, 0.58, 0.34]

    def hit_at(s, pos, d):
        s.shake(0.14)
        hit_tint(s, 0.35, 3.0)
        burst_flash(s, pos, 0.34 * H, life=0.1)
        for _ in range(5):
            a = s.rng.uniform(0, 6.28)
            drop(s, pos, np.array([math.cos(a), math.sin(a) - 0.4]) * s.rng.uniform(140, 300), life=0.4, r=3.2)
        foam(s, pos + s.rng.uniform(-8, 8, 2), r1=9)

    def make(s, i):
        th = math.pi + math.pi * (i + 0.5) / N
        home = A + np.array([RA * math.cos(th), 0.5 * RA * math.sin(th)])
        aim = tgt + np.array([s.rng.uniform(-0.18, 0.18) * H, s.rng.uniform(-0.15, 0.2) * H])
        q = P(home, (0, 0), 3.0, home=home, aim=aim, i=i, fly=False, launch=0.85 + i * 0.1)
        foam(s, home, r1=10)
        for _ in range(3):
            drop(s, home + s.rng.uniform(-10, 10, 2), np.array([s.rng.uniform(-60, 60), -s.rng.uniform(20, 90)]), life=0.35, r=2.8)

        def upd(z, dt, ss):
            if not z.fly:
                z.pos = z.home + np.array([0.0, 3.5 * math.sin(z.age * 7 + z.i)])
                z.vel = (z.aim - z.pos) * 0.001
                if ss.rng.uniform() < 0.08:
                    drop(ss, z.pos + ss.rng.uniform(-6, 6, 2), np.array([0.0, 40.0]), life=0.35, r=2.4)
                if ss.t >= z.launch:
                    z.fly = True
                    z.vel = unit(z.aim - z.pos) * 1500
                    ss.shake(0.05)
            else:
                if ss.rng.uniform() < 0.5:
                    drop(ss, z.pos - unit(z.vel) * 26, -unit(z.vel) * 80 + ss.rng.uniform(-50, 50, 2), life=0.25, r=3, grav=200)
                if ss.rng.uniform() < 0.25:
                    foam(ss, z.pos - unit(z.vel) * 28, vel=np.zeros(2), life=0.3, r0=3, r1=6)
                if float(np.dot(z.aim - z.pos, z.vel)) <= 0:
                    z.dead = True
                    hit_at(ss, z.aim, unit(z.vel))
        q.upd = upd

        def draw(z, k):
            age = z.age
            sc = 1.25 * fx.ease_out(age / 0.1) if age < 0.1 else 1.25 - 0.25 * min(1.0, (age - 0.1) / 0.06)
            d = unit(z.vel) if z.fly else unit(z.aim - z.pos)
            ang = fx.tip_angle(d)
            out = []
            for li, (c, f) in enumerate(zip(W, LF)):
                L = LEN * sc * f * (1.25 if z.fly and li < 2 else 1.0) + (5 if li == 0 else 0)
                out.append(item(FRONT, 20 + li, "drop_s" if li == 0 else "drop", 1, c, z.pos - d * (LEN * sc * (1 - f) * 0.2), L, 0.62, ang))
            return out
        q.draw = draw
        s.add(q)
    for i in range(N):
        sim.at(0.06 + i * 0.08, lambda s, i=i: make(s, i))
    sim.at(0.85 + N * 0.1 + 0.12, lambda s: (crown(s, FOE + np.array([0, 6.0]), 0.7 * H), ripple(s, FOE + np.array([0, 2]), 0.15 * H, 0.7 * H),
                                              rain_back(s, FOE, 8, 0.5, 0.0, 0.3)))


# ---------------- 9. khiên nước (lặp 2 s) ----------------
def khien_nuoc(sim):
    """bong bóng nước lớn bọc quanh tướng: vành xanh có viền phập phồng, màng nước mỏng, vệt bọt trượt trên mặt, lưỡi sóng nhỏ
    chạy quanh vành, bọt nổi lên bên trong, vòng sóng dưới chân."""
    _, w, h = sim.geo
    c = ME + np.array([-0.03 * w, -0.5 * h])
    R, SQ = 0.58 * max(h, 0.8 * w), 0.9

    def shell(s, rng, j):
        p = P(c, (0, 0), 2.0, group=FRONT)

        def draw(q, k):
            rr = R * (1 + 0.025 * math.sin(2 * math.pi * 2 * k))
            return [item(FRONT, 17, "blob", 0, W[3], c, 2 * rr * SQ, 1 / SQ, 0, 0.2),
                    item(FRONT, 30, "ringpx", int(5 * fx.K), W[2], c, 2 * rr * SQ, 1 / SQ),
                    item(FRONT, 30.5, "ringpx0", int(2 * fx.K), FOAM, c, 2 * rr * 0.93 * SQ, 1 / SQ, 0, 0.9)]
        p.draw = draw
        s.add(p)
        t = P(c, (0, 0), 2.0)
        t.upd = lambda q, dt, ss: ss.hero_fx.__setitem__("me", {"tint": TINT, "amt": 0.12})
        s.add(t)
    sim.periodic(2.0, 1, shell)

    def swoosh(s, rng, j):
        p = P(c, (0, 0), 0.9, span=int(rng.uniform(40, 70)), a_from=rng.uniform(190, 250), col=FOAM if j % 2 else W[3], rr=R * rng.uniform(0.74, 0.88))

        def draw(q, k):
            a0 = int(q.a_from + 70 * k)
            alpha = min(1.0, k / 0.2, (1 - k) / 0.3) * 0.9
            return [item(FRONT, 31, "arcpx0", a0 * 1000 + q.span, tuple(q.col) + (3.5 * fx.K,), c, 2 * q.rr * SQ, 1 / SQ, 0, alpha)]
        p.draw = draw
        s.add(p)
    sim.periodic(2.0, 7, swoosh)

    def runner(s, rng, j):
        q = wave_p(s, c, (0, 0), 1.0, 6, rng.uniform(9, 12), FRONT, tip=1.0, up=0.0, drag=0, fade=0.75)
        q.ph = rng.uniform(0, 6.28)

        def upd(z, dt, ss):
            a = z.ph + 3.0 * z.age
            new = c + np.array([R * math.cos(a), R * SQ * math.sin(a)])
            z.vel = (new - z.pos) / max(dt, 1e-5)
            z.pos = new - z.vel * dt
        q.upd = upd
    sim.periodic(2.0, 9, runner)
    sim.periodic(2.0, 8, lambda s, rng, j: foam(s, c + np.array([rng.uniform(-0.6, 0.6) * R, rng.uniform(0.1, 0.6) * R]),
                                                vel=np.array([rng.uniform(-10, 10), -rng.uniform(50, 90)]), life=0.8, r0=3, r1=rng.uniform(5, 8)))
    sim.periodic(2.0, 2, lambda s, rng, j: ripple(s, ME + np.array([0, -2]), 0.3 * w, 0.62 * w, life=0.9, col=W[3], band=(5.0, 1.5)))


# ---------------- 10. suối hồi phục ----------------
def suoi_hoi(sim):
    """hồi phục: vòng sóng loang dưới chân, hai dòng giọt nước XANH NGỌC xoắn quanh thân từ chân lên đầu (nửa sau vẽ sau tướng),
    ba vòng xanh ngọc lần lượt dâng từ chân lên đầu và thu nhỏ dần, bong bóng và lấp lánh nổi lên, tướng ửng xanh ngọc hai nhịp.
    Màu sáng, ít hình: không dùng lưỡi sóng xanh đậm (đè lên tướng rất rối)."""
    _, w, h = sim.geo
    HEAL, HEAL2 = (128, 232, 200), (218, 250, 238)
    rx = 0.46 * w
    for i in range(3):
        sim.at(i * 0.3, lambda s: ripple(s, ME + np.array([0, -2]), 0.15 * w, 0.7 * w, life=0.6, col=W[3]))
    sim.at(0.0, lambda s: crown(s, ME + np.array([0, 2.0]), 0.6 * w, life=0.45, group=BACK))

    def helix(s, x, j=[0]):
        j[0] += 1
        q = P(ME, (0, 0), 0.95, ph=(j[0] % 2) * math.pi + 7.0 * s.t, r=s.rng.uniform(8.5, 12.5), seed=s.rng.randint(4))

        def upd(z, dt, ss):
            k = z.age / z.life
            a = z.ph + 6.5 * z.age
            R = rx * (1 - 0.25 * k)
            new = ME + np.array([R * math.cos(a), 0.28 * R * math.sin(a) - k * 1.05 * h])
            z.vel = (new - z.pos) / max(dt, 1e-5)
            z.pos = new - z.vel * dt
            z.group = FRONT if math.sin(a) > 0 else BACK
        q.upd = upd

        def draw(z, k):
            sp = float(np.hypot(*z.vel))
            if z.age < 0.04 or sp < 1 or sp > 3000:
                return []
            L = 2.7 * z.r * min(1.0, k / 0.12) * (1 - k ** 3)
            ang = fx.tip_angle(-z.vel / sp)  # đuôi giọt chĩa ngược chiều bay
            return [item(z.group, 24, "drop_s", z.seed, INK, z.pos, L + 4, 0.7, ang), item(z.group, 25, "drop", z.seed, HEAL, z.pos, L, 0.7, ang),
                    item(z.group, 26, "drop", z.seed, HEAL2, z.pos, L * 0.5, 0.7, ang)]
        q.draw = draw
        s.add(q)
    sim.every(0.1, 1.25, 26, helix)

    def ring_up(s):  # vòng xanh ngọc dâng từ chân lên đầu
        q = P(ME, (0, 0), 0.75)

        def draw(z, k):
            c = ME + np.array([0.0, -k * 0.95 * h])
            R = rx * (1.0 - 0.3 * k) * min(1.0, k / 0.15)
            al = min(1.0, (1 - k) / 0.35)
            hg = 2 * R * 0.28
            return [item(BACK, 27, "arcpx", 180 * 1000 + 180, HEAL + (4 * fx.K,), c, hg, 1 / 0.28, 0, al),
                    item(FRONT, 27, "arcpx", 180, HEAL + (4 * fx.K,), c, hg, 1 / 0.28, 0, al)]
        q.draw = draw
        s.add(q)
    for t0 in (0.2, 0.65, 1.1):
        sim.at(t0, ring_up)

    def sparkle(s, x):
        p = P(ME + np.array([s.rng.uniform(-0.4, 0.4) * w, -s.rng.uniform(0.1, 0.8) * h]), (s.rng.uniform(-10, 10), -s.rng.uniform(50, 100)),
              s.rng.uniform(0.5, 0.9), seed=0, tw=s.rng.uniform(0, 6))
        p.draw = fx.mat_sprite("star", 42, (255, 255, 255),
                               size_fn=lambda q, k: 21 * min(1, k / 0.18) * (1 - k ** 2) * (0.6 + 0.4 * abs(math.sin(q.age * 14 + q.tw))))
        s.add(p)
    sim.every(0.3, 1.7, 15, sparkle)
    sim.every(0.2, 1.6, 9, lambda s, x: bubble(s, ME + np.array([s.rng.uniform(-0.4, 0.4) * w, -s.rng.uniform(0.0, 0.4) * h]),
                                               np.array([s.rng.uniform(-12, 12), -s.rng.uniform(70, 120)]), s.rng.uniform(0.5, 0.85),
                                               s.rng.uniform(5, 9), group=FRONT if s.rng.uniform() < 0.6 else BACK))
    sim.at(0.15, lambda s: s.hero_fx.__setitem__("me", {"tint": HEAL, "amt": 0.5, "decay": 0.7}))
    sim.at(0.85, lambda s: s.hero_fx.__setitem__("me", {"tint": HEAL, "amt": 0.4, "decay": 0.6}))


# ---------------- 11. xoáy nước rồi mạch phun ----------------
def xoay_nuoc(sim):
    """xoáy nước dưới chân đối thủ: các cung nước và lưỡi sóng chạy vòng sát đất, siết dần vào tâm; rồi mạch nước phun thẳng lên
    từ tâm xoáy, vương miện nước, bọt trên đỉnh, mưa giọt, vũng nước."""
    C = FOE + np.array([0.0, 4.0])
    T1 = 0.95

    def arc(s, x):
        p = P(C, (0, 0), 0.5, ph=s.rng.uniform(0, 360), span=int(s.rng.uniform(80, 150)), kind=s.rng.randint(3))

        def draw(q, k):
            R = (0.95 - 0.65 * k) * H
            a0 = int((q.ph + 420 * k) % 360)
            alpha = min(1.0, k / 0.15, (1 - k) / 0.25)
            if q.kind == 0:
                return [item(FLOOR, 31, "arcpx0", a0 * 1000 + q.span, FOAM + (3 * fx.K,), C, 2 * R * 0.3, 1 / 0.3, 0, alpha)]
            return [item(FLOOR, 30, "arcpx", a0 * 1000 + q.span, (W[2] if q.kind == 1 else W[3]) + (5 * fx.K,), C, 2 * R * 0.3, 1 / 0.3, 0, alpha)]
        p.draw = draw
        s.add(p)
    sim.every(0.0, T1 + 0.1, 28, arc)

    def runner(s, x):
        q = wave_p(s, C, (0, 0), 0.55, 6, s.rng.uniform(9, 13), FRONT, tip=1.0, up=0.08, drag=0, fade=0.75)
        q.ph = s.rng.uniform(0, 6.28)

        def upd(z, dt, ss):
            k = z.age / z.life
            a = z.ph + 7.5 * z.age
            R = (0.9 - 0.62 * k) * H
            new = C + np.array([R * math.cos(a), 0.3 * R * math.sin(a) - 3])
            z.vel = (new - z.pos) / max(dt, 1e-5)
            z.pos = new - z.vel * dt
            z.group = BACK if math.sin(a) < 0 else FRONT
        q.upd = upd
    sim.every(0.05, T1, 36, runner)
    sim.every(0.1, T1, 16, lambda s, x: foam(s, C + np.array([s.rng.uniform(-0.25, 0.25) * H, s.rng.uniform(-6, 6)]), vel=np.zeros(2), life=0.4,
                                             r0=3, r1=s.rng.uniform(6, 9), group=BACK))

    def tint(s):
        t = P(C, (0, 0), T1 - 0.1)
        t.upd = lambda q, dt, ss: ss.hero_fx.__setitem__("foe", {"tint": TINT, "amt": 0.18 + 0.06 * math.sin(q.age * 14)})
        s.add(t)
    sim.at(0.1, tint)
    sim.at(0.1, lambda s: s.shake(0.15))

    def geyser(s):
        s.shake(0.65)
        s.flash = 0.1
        hit_tint(s, 0.5, 0.8)
        crown(s, C + np.array([0, 4.0]), 0.85 * H, life=0.5)
        ripple(s, C, 0.15 * H, 0.85 * H)
        burst_flash(s, FOE + np.array([0.0, -0.45 * H]), 0.6 * H)

        pil = P(C, (0, 0), 0.66, group=FRONT)  # cột nước liền vọt lên giữa thân đối thủ, hẹp và trong mờ
        CT = [(-1.7, 0.0), (-0.9, 0.1), (-0.62, 0.45), (-0.78, 0.74), (-1.5, 0.88), (-1.25, 1.02), (-0.6, 0.96), (0.0, 1.1), (0.6, 0.96),
              (1.25, 1.02), (1.5, 0.88), (0.78, 0.74), (0.62, 0.45), (0.9, 0.1), (1.7, 0.0)]  # chân loe, thân thon, đầu xoè ba ngọn

        def pdraw(q, k):
            a = q.age
            g = fx.ease_out(min(1.0, a / 0.12)) * (1 - fx.smoothstep(0.4, 0.66, a))
            if g < 0.05:
                return []
            ht, wd = 1.3 * H * g, 0.17 * H * (0.75 + 0.25 * g)
            pts = smooth([(C[0] + (f + 0.07 * math.sin(a * 22 + i * 1.3)) * wd, C[1] - v * ht) for i, (f, v) in enumerate(CT)])
            out = water_shape(FRONT, 16.0, pts, mid=(C[0], C[1] - 0.52 * ht), k2=(0.55, 0.9), k3=(0.2, 0.78), shift=(-0.12 * wd, 0), alpha=0.82)
            for i, (f, v) in enumerate(((-1.2, 0.98), (0.0, 1.1), (1.2, 0.98), (-0.6, 1.02), (0.6, 1.02))):  # bọt trên đầu cột
                pos = np.array([C[0] + f * wd, C[1] - v * ht])
                r = (0.62 + 0.12 * math.sin(a * 18 + i * 2)) * wd * (1.0 if i < 3 else 0.75)
                out += [item(FRONT, 17.0, "foam_s", i % 4, INK, pos, 2 * r + 4), item(FRONT, 17.1, "foam", i % 4, FOAM, pos, 2 * r)]
            return out
        pil.draw = pdraw
        s.add(pil)

        def col(ss, x):
            fr = ss.rng.uniform() < 0.25
            wave_p(ss, C + np.array([ss.rng.uniform(-0.2, 0.2) * H, -4.0]), np.array([ss.rng.uniform(-50, 50), -ss.rng.uniform(520, 800) * (1 - 0.4 * x)]),
                   ss.rng.uniform(0.4, 0.55), 9, ss.rng.uniform(18, 26) * (0.6 if fr else 1.0), FRONT if fr else BACK, tip=1.0, up=0.6, drag=1.4,
                   acc=(0, 900), foam_p=0.5)
        s.every(s.t, s.t + 0.45, lambda ss, x: 60 * (1 - 0.5 * x), col)
        s.every(s.t + 0.1, s.t + 0.6, 20, lambda ss, x: foam(ss, FOE + np.array([ss.rng.uniform(-0.3, 0.3) * H, -ss.rng.uniform(1.0, 1.3) * H]),
                                                               vel=np.array([ss.rng.uniform(-60, 60), -ss.rng.uniform(0, 40)]), r0=6,
                                                               r1=ss.rng.uniform(11, 16), group=BACK))
        rain_back(s, FOE, 18)
        puddle(s, FOE + np.array([0, 3]), 24, 1.3)
    sim.at(T1, geyser)


# ---------------- 12. lưỡi nước ----------------
def luoi_nuoc(sim):
    """tụ nhanh ở miệng rồi chém hai lưỡi nước trăng khuyết liên tiếp: mỗi lưỡi là MỘT mảng trăng khuyết liền (mực, xanh đậm,
    xanh trời, dải bọt trắng ở mép trước), bật ra nở to, bay nhanh, để lại vệt mờ, giọt và bọt; trúng thì toé nước."""
    mouth, w, h = sim.geo
    tgt = FOE + np.array([0.0, -0.42 * H])
    dd = tgt - mouth
    dist = float(np.hypot(*dd))
    u = dd / dist
    nrm = np.array([-u[1], u[0]])
    src = mouth + u * 12
    T0, SP = 0.32, 900.0
    travel = (dist - 20) / SP
    gather(sim, lambda t: src, 0.0, T0 - 0.04, reach=55, rate=50)
    orb(sim, lambda t: src, T0, T0 + 0.25, 13)

    def crescent(c, d, ax, sc, a, a2, b, n=13):
        th = np.linspace(-math.pi / 2, math.pi / 2, n)
        outer = [c + (d * a * math.cos(x) + ax * b * math.sin(x)) * sc for x in th]
        inner = [c + (d * a2 * math.cos(x) + ax * b * math.sin(x)) * sc for x in th[::-1]]
        return outer + inner[1:-1]

    def blade(s, tilt):
        s.shake(0.15)
        ax = nrm * math.cos(tilt) + u * math.sin(tilt)   # trục dọc lưỡi, mỗi nhát nghiêng một kiểu
        d = u * math.cos(tilt) - nrm * math.sin(tilt)    # mặt lưỡi
        q = P(src, u * SP, travel, group=FRONT)

        def draw(z, k):
            sc = 0.4 + 0.6 * fx.ease_out(min(1.0, z.age / 0.07))
            c = z.pos - d * 8 * sc
            return [fx.poly(FRONT, 26.0, crescent(c, d, ax, sc, 34, 2, 58), INK, 1.0, grow=2.4),
                    fx.poly(FRONT, 26.1, crescent(c, d, ax, sc, 34, 2, 58), W[1]),
                    fx.poly(FRONT, 26.2, crescent(c, d, ax, sc, 30, 9, 51), W[2]),
                    fx.poly(FRONT, 26.3, crescent(c, d, ax, sc, 22, 12, 42), W[3]),
                    fx.poly(FRONT, 26.4, crescent(c, d, ax, sc, 30.5, 23, 46), FOAM)]
        q.draw = draw
        s.add(q)
        t0 = s.t
        pos = lambda ss: src + u * SP * (ss.t - t0)

        def ghost(ss, x):  # vệt mờ phía sau lưỡi
            g = P(pos(ss) - u * 16, u * SP * 0.25, 0.13)
            g.draw = lambda z, k: [fx.poly(FRONT, 25.0, crescent(z.pos, d, ax, 1 - 0.25 * k, 26, 14, 50), W[3], 0.55 * (1 - k))]
            ss.add(g)
        s.every(s.t + 0.03, s.t + travel, 34, ghost)
        s.every(s.t, s.t + travel, 44, lambda ss, x: drop(ss, pos(ss) + ax * ss.rng.uniform(-48, 48) - u * 14,
                                                         -u * ss.rng.uniform(40, 140) + np.array([0.0, -40.0]), life=0.4, r=ss.rng.uniform(2.6, 4.2)))
        s.every(s.t, s.t + travel, 20, lambda ss, x: foam(ss, pos(ss) + ax * ss.rng.choice([-1, 1]) * ss.rng.uniform(34, 52) - u * 10, vel=np.zeros(2),
                                                         life=0.35, r0=3, r1=ss.rng.uniform(6, 9)))

        def hit(ss):
            ss.shake(0.4)
            hit_tint(ss, 0.45, 1.6)
            cut_ = P(tgt, (0, 0), 0.16)  # vết chém trắng loé trên người đối thủ
            cut_.draw = lambda z, k: [fx.poly(FRONT, 36.0, crescent(z.pos - d * 6, d, ax, 1.0 + 0.35 * k, 14 * (1 - k), 4 * (1 - k), 64), INK, 1 - k ** 2, grow=2.0),
                                      fx.poly(FRONT, 36.1, crescent(z.pos - d * 6, d, ax, 1.0 + 0.35 * k, 14 * (1 - k), 4 * (1 - k), 64), FOAM, 1 - k ** 2)]
            ss.add(cut_)
            splash(ss, tgt, 0.75, ground=FOE[1])
        s.at(s.t + travel, hit)
    sim.at(T0, lambda s: blade(s, 0.35))
    sim.at(T0 + 0.22, lambda s: blade(s, -0.35))


EFFECTS = {  # tên: (hàm dựng, dài, nhãn, chu kỳ lặp hoặc None)
    "tu_nuoc": (tu_nuoc, 2.4, "Tụ nước", None),
    "tia_nuoc": (tia_nuoc, 2.1, "Tia nước", None),
    "cau_nuoc": (cau_nuoc, 2.3, "Cầu nước", None),
    "luoi_nuoc": (luoi_nuoc, 1.7, "Lưỡi nước", None),
    "thuong_nuoc": (thuong_nuoc, 2.3, "Thương nước", None),
    "bong_bong": (bong_bong, 2.4, "Bong bóng", None),
    "song_than": (song_than, 2.3, "Sóng thần", None),
    "mua_rao": (mua_rao, 2.5, "Mưa rào", None),
    "xoay_nuoc": (xoay_nuoc, 2.4, "Xoáy nước, mạch phun", None),
    "voi_rong": (voi_rong, 2.9, "Vòi rồng nước", None),
    "khien_nuoc": (khien_nuoc, 2.0, "Khiên nước", 2.0),
    "suoi_hoi": (suoi_hoi, 2.2, "Suối hồi phục", None),
}


def main(out_dir, names):
    stage = fx.Stage(bg="battle_thuy_c01.png", me="inbox/thuong_lam_3/tai_ve/L1_lien.png", foe="inbox/kuba_3/tai_ve/L1_lien.png")
    geo = stage_geo(stage)
    for nm in names:
        build, dur, label, loop = EFFECTS[nm]

        def b(sim, build=build):
            sim.geo = geo
            build(sim)
        fx.run(b, out_dir, nm, dur, loop=loop, stage=stage, label=label)
        print("xong", nm, file=sys.stderr)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(fx.HERE, "_bo_thuy")
    main(out, sys.argv[2:] or list(EFFECTS))
