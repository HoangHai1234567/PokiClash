# -*- coding: utf-8 -*-
"""Quái đảo Mộc (sóc dẻ gai, thay Bọ Sừng): sinh lệnh AtomSpine cho clip + hiệu ứng -> quai_moc/atom/anim.ops.

    py -3 -I ArtGen/Spine/quai_moc_anim.py      # rồi: atom do -f atom/anim.ops -p ArtGen/Spine/quai_moc/atom

Nhịp theo skill animation-petclash: idle 2 s lặp (nhún kiểu sóc, đuôi lá uốn sóng lệch pha, mũ trễ, tai giật, điểm phá nhịp đấm
gió 1,25–1,5), walk 2 s (4 cú nhảy cóc), attack 0,9 s (ngả sau lấy đà 0,28, húc mũ gai trúng 0,45, khựng, quá đà, về), cast 1,0 s
(vung đuôi ra sau, quật qua đầu, lá phóng 0,5), skill 1,8 s (đấm gần 0,62, móc tay xa 0,8, quật đuôi nện đất 1,15), hit 0,6 s,
die 1,4 s (giật, lả, ngã ngửa, mũ tuột, mờ), appear 0,8 s (khung đầu trống, rơi xuống nén, vòng lá). Góc cộng vào dáng gốc
(độ, CCW: thân + là ngả ra sau, đuôi + là vung ra sau, đuôi - là quật ra trước); dời cộng (px, y lên).
"""
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "quai_moc", "atom", "anim.ops")
SLOTS = ["duoi3", "duoi2", "duoi1", "tay_xa", "nam_xa", "chan_xa", "than", "chan_gan", "dau", "tay_gan", "mu", "tai_trai",
         "tai_phai"]
TAIL = "duoi1,duoi2,duoi3"
L = []


def ops(*lines):
    L.extend(lines)


def key(anim, target, *pairs):
    """pairs: (t, v) hoặc (t, v, curve); v số hoặc (x, y)"""
    parts = []
    for p in pairs:
        t, v = p[0], p[1]
        vs = f"{v[0]:.3f},{v[1]:.3f}" if isinstance(v, tuple) else f"{v:.2f}"
        parts.append(f"{t:.3f}:{vs}" + (f":{p[2]}" if len(p) > 2 else ""))
    ops(f"key {anim} {target} " + " ".join(parts))


def dense(anim, target, f, dur, fps=30, zero=False):
    """khoá dày từ f(t); zero=True: trừ (scale: chia) giá trị tại t=0 để khung đầu = dáng gốc (clip khác nối vào không giật)"""
    n = max(1, round(dur * fps))
    g = f
    if zero:
        v0 = f(0.0)
        if target.endswith(".scale"):
            g = lambda t: (f(t)[0] / v0[0], f(t)[1] / v0[1])
        elif isinstance(v0, tuple):
            g = lambda t: (f(t)[0] - v0[0], f(t)[1] - v0[1])
        else:
            g = lambda t: f(t) - v0
    key(anim, target, *[(dur * i / n, g(dur * i / n)) for i in range(n + 1)])


def tail_wave(anim, dur, waves):
    """sóng đuôi lá (gốc dẫn, ngọn trễ, lớn dần ra ngọn), khung đầu = dáng gốc. waves: [(biên độ gốc, chu kỳ, trễ mỗi đốt, tăng)]"""
    for i, b in enumerate(("duoi1", "duoi2", "duoi3")):
        def f(t, i=i):
            return sum(amp * gr ** i * math.sin(2 * math.pi * (t / per - lag * i / per)) for amp, per, lag, gr in waves)
        dense(anim, f"{b}.rotate", f, dur, zero=True)


def bump(t, t0, up, hold, down, amp):
    if t < t0 or t > t0 + up + hold + down:
        return 0.0
    if t < t0 + up:
        return amp * math.sin(0.5 * math.pi * (t - t0) / up)
    if t < t0 + up + hold:
        return amp
    return amp * math.cos(0.5 * math.pi * (t - t0 - up - hold) / down)


def tw(t, period, phase=0.0):
    return math.sin(2 * math.pi * (t / period - phase))


def vfx_art():
    ops("vfx.art la kind=leaf palette=wood size=64 seed=3",
        "vfx.art gai kind=shard palette=wood size=52 seed=5",
        "vfx.art vong kind=shockwave palette=wood size=192 seed=2",
        "vfx.art cham kind=impact palette=wood size=160 seed=4")


def tail_front(anim, t_on, t_off):
    """đuôi ra trước thân trong [t_on, t_off): tắt lá gốc (sau thân), bật bản sao (trước thân); khoá bậc"""
    for n in ("duoi1", "duoi2", "duoi3"):
        ops(f"key {anim} {n}.attachment 0:{n} {t_on:.3f}:- {t_off:.3f}:{n}",
            f"key {anim} {n}_tr.attachment 0:- {t_on:.3f}:{n}_tr {t_off:.3f}:-")


def ring(anim, img, bone, t, dur, a, b, fade, tag):
    ops(f"vfx.ring {anim} image={img} slot={anim}_{tag} bone={bone} t={t:.3f} dur={dur:.3f} from={a} to={b} fade={fade}")


def ear_lag(anim, t_wind, t_hit, t_end, amp=1.0):
    """tai trễ theo đầu (ngả theo lúc lấy đà, giật ngược lúc đánh, quá đà rồi về); tai phải lệch 0,03 s"""
    for b, k, dt in (("tai_l", 1.0, 0.0), ("tai_r", 1.2, 0.03)):
        key(anim, f"{b}.rotate", (0, 0), (t_wind + dt, 8 * k * amp, "easeOut"), (t_hit + dt, -14 * k * amp),
            (t_hit + 0.1 + dt, 8 * k * amp, "easeOut"), (t_hit + 0.24 + dt, -3 * k * amp), (t_end, 0, "easeInOut"))


def helmet_lag(anim, t_wind, t_hit, t_end, amp=1.0):
    """mũ gai trễ một nhịp theo đầu: đầu ngả sau thì mũ còn chúi, đầu húc tới thì mũ còn ngả, rồi nảy về"""
    key(anim, "mu.rotate", (0, 0), (t_wind + 0.04, -4 * amp, "easeOut"), (t_hit, 5 * amp), (t_hit + 0.08, -6 * amp, "easeOut"),
        (t_hit + 0.2, 2.5 * amp), (t_hit + 0.32, -1 * amp), (t_end, 0, "easeInOut"))


def idle():
    a, d = "idle", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    # nhún nảy kiểu sóc: 4 nhịp nhỏ, thân thở, đầu lệch pha
    dense(a, "hip.translate", lambda t: (0, 4 * abs(math.sin(2 * math.pi * t)) - 1.5 * bump(t, 1.25, 0.05, 0.1, 0.12, 1)), d, zero=True)
    dense(a, "than.scale", lambda t: (1 + 0.018 * math.cos(4 * math.pi * t), 1 - 0.018 * math.cos(4 * math.pi * t)), d, zero=True)
    dense(a, "than.rotate", lambda t: 1.5 * tw(t, 2) - bump(t, 1.25, 0.05, 0.12, 0.15, 4), d, zero=True)
    dense(a, "dau.rotate", lambda t: 2 * tw(t, 2, 0.12) + 1.2 * tw(t, 0.5, 0.2) - bump(t, 1.27, 0.05, 0.1, 0.15, 3), d, zero=True)
    dense(a, "mu.rotate", lambda t: 1.6 * tw(t, 0.5, 0.35) + 1.2 * tw(t, 2, 0.3) + bump(t, 1.33, 0.05, 0.05, 0.2, 3), d, zero=True)
    # tai giật: tai phải ở 0,35 s, tai trái ở 1,7 s
    dense(a, "tai_r.rotate", lambda t: 1.5 * tw(t, 1, 0.4) + bump(t, 0.35, 0.04, 0.04, 0.12, 14) - bump(t, 0.5, 0.04, 0.0, 0.1, 5), d, zero=True)
    dense(a, "tai_l.rotate", lambda t: 1.5 * tw(t, 1, 0.1) + bump(t, 1.7, 0.04, 0.04, 0.12, 12) - bump(t, 1.85, 0.04, 0.0, 0.1, 4), d, zero=True)
    # thủ thế: hai nắm đấm nhún lệch pha; điểm phá nhịp 1,25–1,5: tay gần đấm gió một cú
    dense(a, "tay_gan.rotate", lambda t: 3 * tw(t, 1, 0.2) + bump(t, 1.22, 0.05, 0.02, 0.06, -6) + bump(t, 1.29, 0.04, 0.08, 0.14, 8), d, zero=True)
    dense(a, "tay_gan.scale", lambda t: (1 + bump(t, 1.29, 0.04, 0.08, 0.14, 0.24), 1 - bump(t, 1.29, 0.04, 0.08, 0.14, 0.06)), d, zero=True)
    dense(a, "tay_xa.rotate", lambda t: 3 * tw(t, 1, 0.6) + bump(t, 1.3, 0.06, 0.08, 0.15, 5), d, zero=True)
    dense(a, "nam_xa.rotate", lambda t: 2.5 * tw(t, 1, 0.75), d, zero=True)
    # đuôi lá uốn sóng: gốc dẫn, ngọn trễ và lớn dần
    tail_wave(a, d, [(3.5, 2.0, 0.14, 1.4), (1.2, 0.5, 0.06, 1.3)])
    ops(f"anim.reduce {a} tol=0.25", f"anim.loopfix {a}")


def walk():
    a, d = "walk", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    hop = lambda t: abs(math.sin(2 * math.pi * t))          # 4 cú nhảy, mỗi cú 0,5 s
    dense(a, "hip.translate", lambda t: (0, 16 * hop(t)), d, zero=True)
    dense(a, "than.scale", lambda t: (1 + 0.035 * (1 - 2 * hop(t)), 1 - 0.035 * (1 - 2 * hop(t))), d, zero=True)
    dense(a, "than.rotate", lambda t: -3 * math.sin(2 * math.pi * t * 2 - 0.6), d, zero=True)
    dense(a, "chan_gan.translate", lambda t: (0, 9 * max(0, hop(t) - 0.2)), d, zero=True)
    dense(a, "chan_xa.translate", lambda t: (0, 9 * max(0, hop(t - 0.03) - 0.2)), d, zero=True)
    dense(a, "chan_gan.rotate", lambda t: 10 * math.sin(4 * math.pi * t), d, zero=True)
    dense(a, "chan_xa.rotate", lambda t: 10 * math.sin(4 * math.pi * t - 0.5), d, zero=True)
    dense(a, "dau.rotate", lambda t: 2.5 * math.sin(4 * math.pi * t - 1.0), d, zero=True)
    dense(a, "mu.rotate", lambda t: 3 * math.sin(4 * math.pi * t - 1.8), d, zero=True)
    dense(a, "tay_gan.rotate", lambda t: 5 * math.sin(4 * math.pi * t - 0.4), d, zero=True)
    dense(a, "tay_xa.rotate", lambda t: 5 * math.sin(4 * math.pi * t - 1.2), d, zero=True)
    dense(a, "tai_l.rotate", lambda t: 6 * math.sin(4 * math.pi * t - 1.6), d, zero=True)
    dense(a, "tai_r.rotate", lambda t: 6 * math.sin(4 * math.pi * t - 1.9), d, zero=True)
    tail_wave(a, d, [(5.0, 0.5, 0.07, 1.35), (2.5, 2.0, 0.12, 1.3)])
    ops(f"anim.reduce {a} tol=0.6", f"anim.loopfix {a}")


def attack():
    a, d, th = "attack", 0.9, 0.45
    ops(f"anim.add {a} dur={d}")
    # lấy đà ngả ra sau 0–0,28, giữ cuộn 0,28–0,38, húc tới snap (0,38 -> 0,45) bước chân theo, khựng tới 0,58, quá đà, về
    key(a, "hip.translate", (0, (0, 0)), (0.28, (-12, -6), "easeOut"), (0.38, (-13, -7), "snap"), (th, (30, -4)), (0.58, (28, -4)),
        (0.7, (8, 0), "easeOut"), (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.28, 10, "easeOut"), (0.38, 11, "snap"), (th, -13), (0.58, -12), (0.7, 2, "easeOut"), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.28, (1.04, 0.95), "easeOut"), (0.38, (1.05, 0.94), "snap"), (th, (0.94, 1.07)), (0.52, (1, 1), "easeOut"),
        (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.3, 8, "easeOut"), (0.39, 9, "snap"), (th, -14), (0.58, -12), (0.72, 3, "easeOut"), (d, 0, "easeInOut"))
    key(a, "tay_gan.rotate", (0, 0), (0.28, 12, "easeOut"), (th, -6), (0.58, -5), (d, 0, "easeInOut"))
    key(a, "tay_xa.rotate", (0, 0), (0.28, 12, "easeOut"), (th, -12), (0.58, -10), (d, 0, "easeInOut"))
    key(a, "nam_xa.rotate", (0, 0), (0.3, 10, "easeOut"), (0.48, -12), (0.6, -10), (d, 0, "easeInOut"))
    # chân bước theo cú lao (bàn gần nhấc lên rồi đặt xuống trước, bàn xa trượt theo), về chỗ cũ khi lùi
    key(a, "chan_gan.translate", (0, (0, 0)), (0.28, (-6, 0), "easeOut"), (0.38, (-6, 0), "snap"), (0.42, (12, 10)), (th, (22, 0)),
        (0.58, (21, 0)), (0.7, (6, 6), "easeOut"), (0.8, (0, 0)), (d, (0, 0)))
    key(a, "chan_xa.translate", (0, (0, 0)), (0.28, (-6, 0), "easeOut"), (0.4, (-6, 0)), (0.47, (20, 4)), (0.52, (24, 0)),
        (0.62, (23, 0)), (0.74, (6, 5), "easeOut"), (0.84, (0, 0)), (d, (0, 0)))
    key(a, "chan_gan.rotate", (0, 0), (0.28, 6, "easeOut"), (0.42, -10), (th, -4), (0.58, -3), (d, 0, "easeInOut"))
    key(a, "chan_xa.rotate", (0, 0), (0.28, 4, "easeOut"), (0.47, -8), (0.52, -3), (d, 0, "easeInOut"))
    # đuôi: vung tới khi lấy đà (ngược thân), quất ra sau khi húc, trễ theo đốt
    key(a, "duoi1.rotate", (0, 0), (0.3, -10, "easeOut"), (th + 0.02, 12), (0.62, 9), (d, 0, "easeInOut"))
    key(a, "duoi2.rotate", (0, 0), (0.33, -8, "easeOut"), (th + 0.05, 10), (0.66, 6), (d, 0, "easeInOut"))
    key(a, "duoi3.rotate", (0, 0), (0.36, -8, "easeOut"), (th + 0.08, 12), (0.7, 5), (d, 0, "easeInOut"))
    ops(f"event {a} {th} hit")
    ear_lag(a, 0.28, th, d)
    helmet_lag(a, 0.28, th, d)
    # trúng: chớp + vòng sóng ở mũi mũ, mảnh gai + lá văng
    ring(a, "cham", "mu_vong", th, 0.22, 0.3, 0.95, 0.15, "cham")
    ring(a, "vong", "mu_vong2", th + 0.02, 0.4, 0.15, 1.3, 0.3, "vong")
    ops(f"vfx.burst {a} image=gai prefix={a}_g bone=mu_mui count=6 t={th:.3f} dur=0.45 speed=320 spread=160 gravity=520 spin=300 "
        f"fade=0.4 scale=0.9 scaleEnd=0.4 seed=7",
        f"vfx.burst {a} image=la prefix={a}_l bone=mu_mui count=4 t={th + 0.01:.3f} dur=0.44 speed=220 spread=200 gravity=260 spin=420 "
        f"fade=0.45 scale=0.8 scaleEnd=0.5 seed=9")


def cast():
    a, d, tr = "cast", 1.0, 0.5
    ops(f"anim.add {a} dur={d}")
    # lấy đà: đuôi vung ra sau, thân ngả, nhún; quật: đuôi qua đầu (gốc dẫn, ngọn búng sau), lá phóng; theo đà rồi về
    key(a, "hip.translate", (0, (0, 0)), (0.36, (-12, -8), "easeOut"), (0.42, (-12, -8), "snap"), (tr, (14, -2)), (0.72, (10, 0)),
        (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.36, 10, "easeOut"), (0.42, 11, "snap"), (tr, -14), (0.72, -11), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.36, (1.04, 0.95), "easeOut"), (0.42, (1.04, 0.95), "snap"), (tr, (0.95, 1.06)), (0.6, (1, 1), "easeOut"),
        (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.38, 8, "easeOut"), (tr + 0.02, -10), (0.74, -7), (d, 0, "easeInOut"))
    # đuôi quét ra trước ngang ngực (bản sao trước thân bật từ 0,46 tới 0,95): gốc dẫn, ngọn búng sau
    key(a, "duoi1.rotate", (0, 0), (0.36, 16, "easeOut"), (0.42, 17, "snap"), (tr - 0.02, -70), (tr + 0.1, -78), (0.76, -66), (d, 0, "easeInOut"))
    key(a, "duoi2.rotate", (0, 0), (0.38, 12, "easeOut"), (0.44, 13, "snap"), (tr + 0.02, -32), (tr + 0.16, -39), (0.8, -28), (d, 0, "easeInOut"))
    key(a, "duoi3.rotate", (0, 0), (0.4, 12, "easeOut"), (0.46, 14, "snap"), (tr + 0.06, -22), (tr + 0.22, -31), (0.84, -18), (d, 0, "easeInOut"))
    tail_front(a, 0.46, 0.95)
    # tay gần chỉ thẳng về đối thủ lúc phóng, tay xa kéo về sau
    key(a, "tay_gan.rotate", (0, 0), (0.38, 16, "easeOut"), (tr, 4), (0.74, 3), (d, 0, "easeInOut"))
    key(a, "tay_gan.scale", (0, (1, 1)), (0.42, (0.92, 1)), (tr, (1.22, 0.96)), (0.6, (1.15, 1), "easeOut"), (d, (1, 1), "easeInOut"))
    key(a, "tay_xa.rotate", (0, 0), (0.38, -6, "easeOut"), (tr, 16), (0.74, 12), (d, 0, "easeInOut"))
    ops(f"event {a} {tr} phun")
    ear_lag(a, 0.38, tr, d, amp=0.9)
    helmet_lag(a, 0.38, tr, d, amp=0.8)
    # lá phóng về phía đối thủ từ trước mặt (xương phong xoay -90: nón hạt chĩa +x); tia mana nhuộm màu do game bắn thêm
    ops(f"vfx.burst {a} image=la prefix={a}_l bone=phong count=10 t={tr:.3f} dur=0.5 speed=760 spread=34 gravity=0 spin=540 "
        f"fade=0.35 scale=0.95 scaleEnd=0.55 seed=13")
    ring(a, "vong", "phong_vong", tr, 0.38, 0.2, 1.2, 0.28, "vong")
    ring(a, "cham", "phong_vong2", tr, 0.18, 0.3, 0.75, 0.14, "cham")


def skill():
    a, d = "skill", 1.8
    ops(f"anim.add {a} dur={d}")
    t1, t2, t3 = 0.62, 0.8, 1.15        # đấm gần, móc tay xa (hit), quật đuôi nện đất (hit)

    def tremble(t):
        return (2.5 if int(t * 30) % 2 else -2.5) if 0.3 <= t <= 0.5 else 0.0

    def lin(pts, t, ease_ends=()):
        for (a0, v0), (a1, v1) in zip(pts, pts[1:]):
            if a0 <= t <= a1:
                u = (t - a0) / (a1 - a0) if a1 > a0 else 1
                if a0 in ease_ends:
                    u = u * u * (3 - 2 * u)
                return v0 + (v1 - v0) * u
        return pts[-1][1]
    hx = [(0, 0), (0.3, -16), (0.5, -18), (0.56, 10), (t1, 18), (0.72, 14), (t2, 26), (0.95, 22), (1.08, 20), (t3, 32), (1.45, 30), (d, 0)]
    hy = [(0, 0), (0.3, -8), (0.5, -9), (t1, -2), (t2, -2), (1.08, 2), (t3, -10), (1.2, -6), (1.45, -6), (d, 0)]
    dense(a, "hip.translate", lambda t: (lin(hx, t, (0, 1.45)), lin(hy, t, (0, 1.45))), d)
    th_pts = [(0, 0), (0.3, 12), (0.5, 12), (t1, -12), (0.7, -6), (t2, -16), (0.95, -12), (1.08, -4), (t3, -24), (1.45, -21), (d, 0)]
    dense(a, "than.rotate", lambda t: lin(th_pts, t, (0, 1.45)) + tremble(t), d)
    key(a, "dau.rotate", (0, 0), (0.32, 8, "easeOut"), (t1, -8), (0.7, -4), (t2, -12), (1.05, 2), (t3, -16), (1.45, -13), (d, 0, "easeInOut"))
    # đấm gần (tay gần duỗi + giãn) 0,62; móc tay xa 0,8
    key(a, "tay_gan.rotate", (0, 0), (0.3, 18, "easeOut"), (0.56, 20, "snap"), (t1, 2), (0.7, 4), (0.9, 14, "easeOut"), (t3, -6), (1.45, -4),
        (d, 0, "easeInOut"))
    key(a, "tay_gan.scale", (0, (1, 1)), (0.56, (0.9, 1)), (t1, (1.36, 0.93)), (0.68, (1.3, 0.95)), (0.78, (1, 1), "easeOut"), (d, (1, 1)))
    # móc tay xa: kéo về sau rồi bật thẳng ra trước ngang đầu (dời trong hệ thân: -y cục bộ = +x thế giới), nắm xoay chĩa tới
    key(a, "tay_xa.rotate", (0, 0), (0.3, 14, "easeOut"), (0.72, 18, "snap"), (t2, -8), (0.92, -6), (1.05, 6, "easeOut"), (t3, -8), (1.45, -6),
        (d, 0, "easeInOut"))
    key(a, "tay_xa.translate", (0, (0, 0)), (0.72, (-6, 10), "snap"), (t2, (6, -40)), (0.92, (5, -36)), (1.05, (0, 0), "easeOut"), (d, (0, 0)))
    key(a, "nam_xa.rotate", (0, 0), (0.72, 14, "snap"), (t2, -28), (0.92, -24), (1.05, 0, "easeOut"), (d, 0))
    # đuôi: theo nhịp đấm nhẹ, rồi vung ra sau (0,85–1,05) và quật qua đầu nện đất 1,15 (gốc dẫn, ngọn trễ)
    key(a, "duoi1.rotate", (0, 0), (0.3, 8, "easeOut"), (t1, -6), (t2, -10), (0.98, 22, "easeOut"), (1.01, 24, "snap"), (t3 - 0.06, -86),
        (t3 + 0.05, -92), (1.45, -82), (d, 0, "easeInOut"))
    key(a, "duoi2.rotate", (0, 0), (0.33, 6, "easeOut"), (t1 + 0.03, -5), (t2 + 0.03, -8), (1.0, 16, "easeOut"), (1.04, 18, "snap"),
        (t3 - 0.03, -40), (t3 + 0.1, -45), (1.48, -34), (d, 0, "easeInOut"))
    key(a, "duoi3.rotate", (0, 0), (0.36, 6, "easeOut"), (t1 + 0.06, -4), (t2 + 0.06, -8), (1.02, 14, "easeOut"), (1.07, 16, "snap"),
        (t3, -36), (t3 + 0.16, -41), (1.5, -30), (d, 0, "easeInOut"))
    tail_front(a, 1.07, 1.72)
    key(a, "chan_gan.rotate", (0, 0), (0.3, 6, "easeOut"), (t1, -6), (t3, -10), (1.45, -8), (d, 0, "easeInOut"))
    key(a, "chan_xa.rotate", (0, 0), (0.3, 4, "easeOut"), (t2, -6), (t3, -8), (1.45, -6), (d, 0, "easeInOut"))
    ops(f"event {a} {t2} hit", f"event {a} {t3} hit")
    key(a, "mu.rotate", (0, 0), (0.34, -4, "easeOut"), (t1, 4), (t1 + 0.08, -3), (t2, 5), (t2 + 0.08, -4, "easeOut"), (t3, 7),
        (t3 + 0.08, -6, "easeOut"), (t3 + 0.22, 2), (1.6, 0, "easeInOut"), (d, 0))
    for b, k in (("tai_l", 1.0), ("tai_r", 1.2)):
        key(a, f"{b}.rotate", (0, 0), (0.32, 8 * k, "easeOut"), (t1, -8 * k), (t2, -12 * k), (1.06, 8 * k), (t3, -16 * k),
            (t3 + 0.12, 6 * k), (1.5, -2 * k), (d, 0, "easeInOut"))
    # hiệu ứng: chớp nhỏ ở nắm gần, chớp + mảnh gai ở nắm xa, nện đuôi: vòng đất + chớp + bão lá + rung
    ring(a, "cham", "tg_vong", t1, 0.18, 0.25, 0.7, 0.12, "chg")
    ring(a, "cham", "tx_vong", t2, 0.22, 0.3, 0.95, 0.15, "chx")
    ops(f"vfx.burst {a} image=gai prefix={a}_g bone=tx_mui count=5 t={t2:.3f} dur=0.45 speed=300 spread=160 gravity=520 spin=300 "
        f"fade=0.4 scale=0.85 scaleEnd=0.4 seed=17")
    ring(a, "vong", "dat_truoc", t3, 0.5, 0.2, 1.9, 0.35, "vong")
    ring(a, "cham", "dat_truoc2", t3, 0.24, 0.35, 1.2, 0.16, "chd")
    ops(f"vfx.burst {a} image=la prefix={a}_l bone=dat_truoc_mui count=12 t={t3:.3f} dur=0.64 speed=420 spread=200 gravity=380 spin=600 "
        f"fade=0.45 scale=1.0 scaleEnd=0.5 seed=19")
    ops(f"vfx.shake {a} bone=move t={t2:.3f} dur=0.14 amp=4", f"vfx.shake {a} bone=move t={t3:.3f} dur=0.24 amp=8 seed=2")


def hit():
    a, d = "hit", 0.6
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-18, 3), "easeOut"), (0.25, (-10, 0)), (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.07, 14, "easeOut"), (0.3, 7), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.07, (0.95, 1.05)), (0.2, (1.02, 0.98), "easeOut"), (d, (1, 1), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.1, 14, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    key(a, "mu.rotate", (0, 0), (0.07, -6), (0.16, 7, "easeOut"), (0.3, -3), (0.45, 1), (d, 0, "easeInOut"))
    key(a, "tay_gan.rotate", (0, 0), (0.07, 22, "easeOut"), (0.3, 8), (d, 0, "easeInOut"))
    key(a, "tay_xa.rotate", (0, 0), (0.07, 18, "easeOut"), (0.3, 6), (d, 0, "easeInOut"))
    key(a, "nam_xa.rotate", (0, 0), (0.1, 12, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    key(a, "tai_l.rotate", (0, 0), (0.07, -10), (0.16, 14, "easeOut"), (0.3, -4), (d, 0, "easeInOut"))
    key(a, "tai_r.rotate", (0, 0), (0.08, -12), (0.18, 16, "easeOut"), (0.32, -5), (d, 0, "easeInOut"))
    # đuôi: sóng ngược từ ngọn (ngọn đỉnh 0,07, giữa 0,15, gốc 0,22)
    key(a, "duoi3.rotate", (0, 0), (0.07, -16, "easeOut"), (0.2, 8), (0.36, -3), (d, 0, "easeInOut"))
    key(a, "duoi2.rotate", (0, 0), (0.15, -10, "easeOut"), (0.3, 5), (d, 0, "easeInOut"))
    key(a, "duoi1.rotate", (0, 0), (0.22, -6, "easeOut"), (0.38, 2), (d, 0, "easeInOut"))
    ops(f"vfx.shake {a} bone=than t=0.0 dur=0.18 amp=4 freq=30", f"anim.reduce {a} tol=0.4")


def die():
    a, d = "die", 1.4
    ops(f"anim.add {a} dur={d}")
    # giật lùi 0,07 -> lả, chao đảo 0,1–0,5 -> ngồi phịch xuống, ngả ngửa lên đuôi 0,5–0,88 -> nảy nhẹ -> mũ lệch -> mờ 1,05–1,4
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-14, 2), "easeOut"), (0.3, (-8, 0)), (0.5, (-6, -2)), (0.86, (-12, -16), "easeIn"),
        (0.93, (-12, -19)), (1.03, (-12, -15), "easeOut"), (d, (-12, -16)))
    dense(a, "than_duoi.rotate", lambda t: 0 if t < 0.5 else 6 * min(1, ((t - 0.5) / 0.38) ** 2), d)
    dense(a, "than.rotate", lambda t: (14 * math.sin(math.pi * min(t, 0.14) / 0.14) if t < 0.14 else
                                        5 * math.sin(2 * math.pi * (t - 0.14) / 0.36) if t < 0.5 else
                                        20 * ((t - 0.5) / 0.38) ** 2 if t < 0.88 else 20 - 3 * math.exp(-(t - 0.88) * 8) * math.sin((t - 0.88) * 30)), d)
    key(a, "than.scale", (0, (1, 1)), (0.86, (1, 1)), (0.92, (1.08, 0.88), "easeOut"), (1.1, (1.03, 0.95), "easeInOut"), (d, (1.03, 0.95)))
    key(a, "dau.rotate", (0, 0), (0.1, 12), (0.3, -8), (0.45, 6), (0.88, 20, "easeIn"), (0.95, 15), (d, 17))
    key(a, "mu.rotate", (0, 0), (0.1, -6), (0.3, 8), (0.5, -4), (0.88, 4, "easeIn"), (0.98, -12, "easeOut"), (1.15, -8), (d, -9))
    key(a, "tay_gan.rotate", (0, 0), (0.07, 24), (0.4, -16, "easeOut"), (0.88, -30, "easeIn"), (0.95, -24), (d, -26))
    key(a, "tay_xa.rotate", (0, 0), (0.07, 20), (0.4, -14, "easeOut"), (0.88, -40, "easeIn"), (0.95, -34), (d, -36))
    key(a, "nam_xa.rotate", (0, 0), (0.4, -20), (0.88, -30), (d, -28))
    # chân duỗi ra trước khi ngồi phịch (theo hông, bàn chân hếch lên)
    key(a, "chan_gan.translate", (0, (0, 0)), (0.5, (0, 0)), (0.88, (12, -4), "easeIn"), (0.95, (12, -1)), (d, (12, -2)))
    key(a, "chan_xa.translate", (0, (0, 0)), (0.5, (0, 0)), (0.88, (4, -12), "easeIn"), (0.95, (4, -9)), (d, (4, -10)))
    key(a, "chan_gan.rotate", (0, 0), (0.5, 0), (0.88, -12, "easeIn"), (0.98, -8), (d, -10))
    key(a, "chan_xa.rotate", (0, 0), (0.5, 0), (0.88, -10, "easeIn"), (0.98, -7), (d, -8))
    for b, k in (("tai_l", 1.0), ("tai_r", 1.2)):
        key(a, f"{b}.rotate", (0, 0), (0.12, 14 * k), (0.35, -20 * k), (0.6, -16 * k), (0.9, -30 * k), (d, -28 * k))
    key(a, "duoi1.rotate", (0, 0), (0.1, -8), (0.5, 4), (0.88, 22, "easeIn"), (0.98, 17), (d, 19))
    key(a, "duoi2.rotate", (0, 0), (0.14, -10), (0.55, 6), (0.92, 14, "easeIn"), (1.02, 9), (d, 11))
    key(a, "duoi3.rotate", (0, 0), (0.18, -12), (0.6, 8), (0.96, 12, "easeIn"), (1.06, 6), (d, 8))
    for sl in SLOTS:
        key(a, f"{sl}.alpha", (0, 1), (1.05, 1), (d, 0))


def appear():
    a, d = "appear", 0.8
    ops(f"anim.add {a} dur={d}")
    for s in SLOTS:
        key(a, f"{s}.alpha", (0, 0), (0.04, 1))
    key(a, "move.translate", (0, (0, 240)), (0.32, (0, 0), "easeIn"), (d, (0, 0)))
    key(a, "than.scale", (0, (0.95, 1.06)), (0.32, (0.95, 1.06)), (0.36, (1.12, 0.86)), (0.47, (0.97, 1.04), "easeOut"),
        (0.6, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "hip.translate", (0, (0, 0)), (0.32, (0, 0)), (0.36, (0, -12)), (0.5, (0, 3), "easeOut"), (0.62, (0, 0)), (d, (0, 0)))
    # rơi: hai tay giơ, đuôi dựng; chạm đất: thủ thế, nắm đấm xa giơ "chào" một cái
    key(a, "tay_gan.rotate", (0, 24), (0.32, 24), (0.38, -8), (0.52, 6, "easeOut"), (d, 0, "easeInOut"))
    key(a, "tay_xa.rotate", (0, 22), (0.32, 22), (0.38, -10), (0.5, 18, "easeOut"), (0.6, 4), (d, 0, "easeInOut"))
    key(a, "nam_xa.rotate", (0, 10), (0.32, 10), (0.4, -10), (0.52, 14, "easeOut"), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 6), (0.32, 6), (0.38, -8), (0.52, 3), (d, 0, "easeInOut"))
    key(a, "mu.rotate", (0, 6), (0.32, 6), (0.36, -2), (0.42, 9, "easeOut"), (0.54, -4), (0.66, 1.5), (d, 0, "easeInOut"))
    key(a, "mu.translate", (0, (0, 10)), (0.32, (0, 10)), (0.37, (0, -6)), (0.48, (0, 3), "easeOut"), (d, (0, 0), "easeInOut"))
    key(a, "duoi1.rotate", (0, -14), (0.32, -14), (0.38, 12), (0.5, -6, "easeOut"), (0.64, 3), (d, 0, "easeInOut"))
    key(a, "duoi2.rotate", (0, -10), (0.34, -10), (0.41, 12), (0.54, -6, "easeOut"), (0.68, 2), (d, 0, "easeInOut"))
    key(a, "duoi3.rotate", (0, -8), (0.36, -8), (0.44, 14), (0.58, -6, "easeOut"), (0.72, 2), (d, 0, "easeInOut"))
    key(a, "tai_l.rotate", (0, 12), (0.32, 12), (0.38, -12), (0.5, 5), (d, 0, "easeInOut"))
    key(a, "tai_r.rotate", (0, 14), (0.33, 14), (0.4, -14), (0.52, 6), (d, 0, "easeInOut"))
    for leg, v in (("chan_gan", -10), ("chan_xa", 10)):
        key(a, f"{leg}.rotate", (0, v), (0.32, v), (0.38, -v * 0.5), (0.52, 0, "easeOut"), (d, 0))
    ops(f"vfx.burst {a} image=la prefix={a}_l bone=move count=6 t=0.32 dur=0.48 speed=260 spread=170 gravity=300 spin=480 fade=0.45 "
        f"scale=0.85 scaleEnd=0.5 seed=5")
    ring(a, "vong", "dat_vong", 0.32, 0.42, 0.2, 1.6, 0.3, "vong")


def main():
    ops("# clip + hiệu ứng sóc dẻ gai (quái đảo Mộc) — sinh bởi ArtGen/Spine/quai_moc_anim.py")
    vfx_art()
    for f in (idle, walk, attack, cast, skill, hit, die, appear):
        f()
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{len(L)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
