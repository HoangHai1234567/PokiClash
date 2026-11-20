# -*- coding: utf-8 -*-
"""Quái đảo Thủy (tôm tít đấm bốc): sinh lệnh AtomSpine cho clip + hiệu ứng -> quai_thuy/atom/anim.ops.

    py -3 -I ArtGen/Spine/quai_thuy_anim.py      # rồi: atom do -f anim.ops -p ArtGen/Spine/quai_thuy/atom

Nhịp theo skill animation-petclash: idle 2 s lặp (thở, lệch pha, điểm phá nhịp đấm nhử ở 62–72%), attack 0,9 s (lấy đà
ngược chiều 0,24 s, ra đòn 3 khung, trúng 0,41, khựng, quá đà, về), cast 1,0 s (nhả 0,5), skill 1,8 s (tụ lực run 0,35–0,6,
nện chùy xa 0,68, đấm thẳng 0,98), hit 0,6 s (bật 0,07), die 1,4 s (giật, choáng, ngã ngửa, mờ), appear 0,8 s (rơi xuống,
nén khi chạm đất, khung đầu trống), walk 2 s (2 chu kỳ bước). Góc xoay cộng vào dáng gốc (độ, CCW); dời cộng (px, y lên).
Càng gần: vai (cg_vai) chĩa xuống, xoay + là khuỷu đưa ra trước; cẳng (cg_co) xoay - để chùy chĩa thẳng ra trước.
"""
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "quai_thuy", "atom", "anim.ops")
SLOTS = ["rau_sau", "rau_truoc", "vay_trai", "vay_phai", "cang_xa_bap", "cang_xa_cang", "cang_xa_chuy", "quat",
         "duoi2", "duoi1", "chan3", "chan4", "chan1", "chan2", "than", "dau", "mat_sau", "mat_truoc", "cang_gan_vai",
         "cang_gan_co", "cang_gan_chuy"]
L = []


def ops(*lines):
    L.extend(lines)


def key(anim, target, *pairs):
    """pairs: (t, v) hoặc (t, v, curve); v số hoặc (x, y)"""
    parts = []
    for p in pairs:
        t, v = p[0], p[1]
        vs = f"{v[0]:.2f},{v[1]:.2f}" if isinstance(v, tuple) else f"{v:.2f}"
        parts.append(f"{t:.3f}:{vs}" + (f":{p[2]}" if len(p) > 2 else ""))
    ops(f"key {anim} {target} " + " ".join(parts))


def dense(anim, target, f, dur, fps=30):
    """khoá dày từ hàm f(t) (vòng lặp, rung, nhịp phá)"""
    n = max(1, round(dur * fps))
    key(anim, target, *[(dur * i / n, f(dur * i / n)) for i in range(n + 1)])


def bump(t, t0, up, hold, down, amp):
    """nhịp nhô: lên trong `up` giây, giữ, xuống trong `down` giây"""
    if t < t0 or t > t0 + up + hold + down:
        return 0.0
    if t < t0 + up:
        return amp * math.sin(0.5 * math.pi * (t - t0) / up)
    if t < t0 + up + hold:
        return amp
    return amp * math.cos(0.5 * math.pi * (t - t0 - up - hold) / down)


def tw(t, period, phase=0.0):
    return math.sin(2 * math.pi * (t / period - phase))


def soft_parts(anim, dur, amp=1.0, period=None):
    """phụ kiện lệch pha: râu, vảy, mắt, đuôi (sóng lặp liền)"""
    p = period or dur
    ops(f"anim.wave {anim} bones=rt1,rt2,rt3 prop=rotate amp={4 * amp:.1f} period={p:.3f} lag=0.12 growth=1.35",
        f"anim.wave {anim} bones=rs1,rs2,rs3 prop=rotate amp={4 * amp:.1f} period={p:.3f} lag=0.12 phase=0.3 growth=1.35",
        f"anim.wave {anim} bones=vay_l prop=rotate amp={6 * amp:.1f} period={p / 2:.3f} phase=0.1",
        f"anim.wave {anim} bones=vay_r prop=rotate amp={6 * amp:.1f} period={p / 2:.3f} phase=0.45",
        f"anim.wave {anim} bones=mat_s prop=rotate amp={4 * amp:.1f} period={p / 2:.3f} phase=0.15",
        f"anim.wave {anim} bones=mat_t prop=rotate amp={4 * amp:.1f} period={p / 2:.3f} phase=0.4",
        f"anim.wave {anim} bones=duoi1,duoi2,quat prop=rotate amp={2.5 * amp:.1f} period={p:.3f} lag=0.15 growth=1.4")


def vfx_art():
    ops("vfx.art giot kind=droplet palette=water size=64 seed=3",
        "vfx.art bot kind=splash palette=water size=96 seed=5",
        "vfx.art vong kind=shockwave palette=water size=192 seed=2",
        "vfx.art cham kind=impact palette=water size=160 seed=4")


def punch_fx(anim, t, bone, ring, big=False, tag=""):
    """hiệu ứng trúng đòn ở mũi chùy: chớp va chạm + vòng sóng + giọt bắn (3 pha: nổ sớm, loang, tan dần)"""
    s = 1.35 if big else 1.0
    ops(f"vfx.ring {anim} image=cham slot={anim}_cham{tag} bone={ring} t={t:.3f} dur={0.22 * s:.3f} from=0.3 to={0.9 * s:.2f} fade=0.15",
        f"vfx.ring {anim} image=vong slot={anim}_vong{tag} bone={ring} t={t + 0.02:.3f} dur={0.42 * s:.3f} from=0.15 to={1.4 * s:.2f} fade=0.3",
        f"vfx.burst {anim} image=giot prefix={anim}_g{tag} bone={bone} count=8 t={t:.3f} dur={0.5 * s:.3f} "
        f"speed={300 * s:.0f} spread=150 gravity=500 fade=0.45 scale=0.9 scaleEnd=0.4 seed={7 + len(tag)}")
    if big:
        ops(f"vfx.burst {anim} image=bot prefix={anim}_b{tag} bone={bone} count=3 t={t + 0.01:.3f} dur=0.55 speed=180 "
            f"spread=200 gravity=200 fade=0.4 scale=0.8 scaleEnd=0.3 seed=11")


def eye_lag(anim, t_wind, t_hit, t_end, amp=1.0):
    """cuống mắt trễ theo đầu: ngả theo lúc lấy đà, giật ngược lúc đấm, quá đà rồi về (khoá tay, không lò xo)"""
    for b, k in (("mat_s", 1.0), ("mat_t", 1.25)):
        key(anim, f"{b}.rotate", (0, 0), (t_wind, 7 * k * amp, "easeOut"), (t_hit, -12 * k * amp), (t_hit + 0.1, 7 * k * amp, "easeOut"),
            (t_hit + 0.24, -3 * k * amp), (t_end, 0, "easeInOut"))


def jab_keys(anim, t_wind, t_hold0, t_hit, t_hold1, t_end, reach=1.0):
    """đấm thẳng càng gần: lấy đà kéo lùi, bật ra 3 khung, khựng, về"""
    key(anim, "cg_vai.rotate", (0, 0), (t_wind, -16, "easeOut"), (t_hold0, -18, "snap"), (t_hit, 80 * reach), (t_hold1, 76 * reach),
        (t_end, 0, "easeInOut"))
    key(anim, "cg_co.rotate", (0, 0), (t_wind, 14, "easeOut"), (t_hold0, 16, "snap"), (t_hit, -66 * reach), (t_hold1, -62 * reach),
        (t_end, 0, "easeInOut"))
    key(anim, "cg_co.scale", (0, (1, 1)), (t_hold0, (1, 1)), (t_hit, (1.16, 0.93)), (t_hit + 0.07, (1, 1), "easeOut"),
        (t_end, (1, 1)))


def idle():
    a, d = "idle", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=4 period=1.0")
    key(a, "than.scale", (0, (1, 1)), (1.0, (1.025, 0.985), "easeInOut"), (2.0, (1, 1), "easeInOut"))
    ops(f"anim.wave {a} bones=than prop=rotate amp=1.5 period=2",
        f"anim.wave {a} bones=dau prop=rotate amp=2 period=2 phase=0.12")
    # thủ thế: hai càng nhún lệch pha; điểm phá nhịp 1,25–1,5 s: càng gần đấm nhử hai cái
    dense(a, "cg_vai.rotate", lambda t: 3 * tw(t, 1, 0.2) + bump(t, 1.25, 0.05, 0.03, 0.07, 22) + bump(t, 1.42, 0.05, 0.02, 0.08, 18), d)
    dense(a, "cg_co.rotate", lambda t: 2 * tw(t, 1, 0.3) - bump(t, 1.25, 0.05, 0.03, 0.07, 18) - bump(t, 1.42, 0.05, 0.02, 0.08, 14), d)
    dense(a, "cx_bap.rotate", lambda t: 3 * tw(t, 1, 0.65) - bump(t, 1.25, 0.06, 0.1, 0.1, 5), d)
    dense(a, "cx_cang.rotate", lambda t: 3 * tw(t, 1, 0.75), d)
    soft_parts(a, d)
    ops(f"anim.loopfix {a}")


def walk():
    a, d = "walk", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=5 period=0.5")
    for leg, ph in (("chan1", 0.0), ("chan3", 0.0), ("chan2", 0.5), ("chan4", 0.5)):
        ops(f"anim.wave {a} bones={leg} prop=rotate amp=14 period=1 phase={ph}")
    ops(f"anim.wave {a} bones=than prop=rotate amp=2 period=1",
        f"anim.wave {a} bones=dau prop=rotate amp=2.5 period=1 phase=0.1",
        f"anim.wave {a} bones=cg_vai prop=rotate amp=5 period=1 phase=0.25",
        f"anim.wave {a} bones=cx_bap prop=rotate amp=5 period=1 phase=0.75")
    soft_parts(a, d, amp=1.3, period=1.0)
    ops(f"anim.loopfix {a}")


def attack():
    a, d = "attack", 0.9
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.24, (-12, -2), "easeOut"), (0.36, (-12, -2)), (0.41, (18, 0)), (0.55, (16, 0)),
        (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.24, 8, "easeOut"), (0.36, 8), (0.41, -12), (0.55, -10), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.28, 6, "easeOut"), (0.40, 6), (0.45, -8), (0.6, -6), (d, 0, "easeInOut"))
    jab_keys(a, 0.24, 0.36, 0.41, 0.55, d)
    key(a, "cx_bap.rotate", (0, 0), (0.24, -8, "easeOut"), (0.41, 14), (0.55, 12), (d, 0, "easeInOut"))
    key(a, "cx_cang.rotate", (0, 0), (0.28, -6, "easeOut"), (0.45, 10), (0.6, 8), (d, 0, "easeInOut"))
    ops(f"event {a} 0.41 hit")
    ops(f"anim.spring {a} bones=rt1,rt2,rt3", f"anim.spring {a} bones=rs1,rs2,rs3", f"anim.spring {a} bones=duoi1,duoi2,quat")
    eye_lag(a, 0.24, 0.41, d)
    punch_fx(a, 0.41, "cg_mui", "cg_vong")


def cast():
    a, d = "cast", 1.0
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.4, (-16, 0), "easeOut"), (0.46, (-16, 0)), (0.5, (14, 2)), (0.75, (12, 0)),
        (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.4, 12, "easeOut"), (0.46, 12), (0.5, -10), (0.75, -8), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.42, 8, "easeOut"), (0.52, -6), (0.78, -4), (d, 0, "easeInOut"))
    jab_keys(a, 0.4, 0.46, 0.5, 0.75, d, reach=1.1)
    key(a, "cx_bap.rotate", (0, 0), (0.4, -10, "easeOut"), (0.5, 12), (0.75, 10), (d, 0, "easeInOut"))
    ops(f"event {a} 0.5 phun")
    ops(f"anim.spring {a} bones=rt1,rt2,rt3", f"anim.spring {a} bones=rs1,rs2,rs3", f"anim.spring {a} bones=duoi1,duoi2,quat")
    eye_lag(a, 0.4, 0.5, d)
    # đòn xa: chỉ vòng sóng ở mũi chùy (đạn nước bay tới đối thủ là việc lớp VFX của game, theo sự kiện "phun")
    ops(f"vfx.ring {a} image=vong slot={a}_vong bone=cg_vong t=0.5 dur=0.4 from=0.2 to=1.3 fade=0.3",
        f"vfx.ring {a} image=cham slot={a}_cham bone=cg_vong t=0.5 dur=0.2 from=0.3 to=0.8 fade=0.15")


def skill():
    a, d = "skill", 1.8
    ops(f"anim.add {a} dur={d}")
    # tụ lực 0–0,6: lùi, ngả lưng, giơ chùy xa cao; run 0,35–0,6 (hai dáng lệch 2–3° đổi nhau mỗi khung)
    def tremble(t):
        return (2.5 if int(t * 30) % 2 else -2.5) if 0.35 <= t <= 0.6 else 0.0

    def hip_x(t):
        pts = [(0, 0), (0.3, -18), (0.6, -20), (0.66, 24), (0.9, 22), (0.95, 30), (1.3, 28), (d, 0)]
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                if t0 in (0, 1.3):
                    u = u * u * (3 - 2 * u)
                return v0 + (v1 - v0) * u
        return 0
    dense(a, "hip.translate", lambda t: (hip_x(t), 0), d)
    dense(a, "than.rotate", lambda t: (14 * min(1, t / 0.3) if t < 0.62 else
                                        -12 if t < 0.92 else -10 if t < 1.3 else -10 * (1 - ((t - 1.3) / 0.5) ** 2)) + tremble(t), d)
    key(a, "dau.rotate", (0, 0), (0.32, 8, "easeOut"), (0.62, 8), (0.7, -10), (0.98, -6), (1.02, -10), (1.3, -8), (d, 0, "easeInOut"))
    # chùy xa: giơ cao lấy đà rồi nện xuống trước (0,62 -> 0,68)
    key(a, "cx_bap.rotate", (0, 0), (0.32, 28, "easeOut"), (0.62, 30, "snap"), (0.68, -16), (0.85, -14), (1.3, -12), (d, 0, "easeInOut"))
    key(a, "cx_cang.rotate", (0, 0), (0.32, 30, "easeOut"), (0.62, 32, "snap"), (0.68, -26), (0.85, -24), (1.3, -22), (d, 0, "easeInOut"))
    key(a, "cx_cang.scale", (0, (1, 1)), (0.62, (1, 1)), (0.68, (1.18, 0.92)), (0.75, (1, 1), "easeOut"), (d, (1, 1)))
    # càng gần: thủ chặt khi tụ, đấm thẳng 0,98
    key(a, "cg_vai.rotate", (0, 0, "easeInOut"), (0.3, -14, "easeOut"), (0.9, -16, "snap"), (0.98, 82), (1.3, 78), (d, 0, "easeInOut"))
    key(a, "cg_co.rotate", (0, 0), (0.3, 12, "easeOut"), (0.9, 14, "snap"), (0.98, -58), (1.3, -55), (d, 0, "easeInOut"))
    key(a, "cg_co.scale", (0, (1, 1)), (0.9, (1, 1)), (0.98, (1.18, 0.92)), (1.05, (1, 1), "easeOut"), (d, (1, 1)))
    ops(f"event {a} 0.68 hit", f"event {a} 0.98 hit")
    ops(f"anim.spring {a} bones=rt1,rt2,rt3", f"anim.spring {a} bones=rs1,rs2,rs3", f"anim.spring {a} bones=duoi1,duoi2,quat")
    eye_lag(a, 0.32, 0.68, d, amp=1.3)
    punch_fx(a, 0.68, "cx_mui", "cx_vong", big=True, tag="a")
    punch_fx(a, 0.98, "cg_mui", "cg_vong", big=True, tag="b")
    ops(f"vfx.shake {a} bone=move t=0.68 dur=0.22 amp=7", f"vfx.shake {a} bone=move t=0.98 dur=0.2 amp=6 seed=2")


def hit():
    a, d = "hit", 0.6
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-16, 3), "easeOut"), (0.25, (-10, 0)), (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.07, 14, "easeOut"), (0.3, 8), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.1, 12, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    key(a, "cg_vai.rotate", (0, 0), (0.07, -22, "easeOut"), (0.3, -10), (d, 0, "easeInOut"))
    key(a, "cg_co.rotate", (0, 0), (0.09, 16, "easeOut"), (0.3, 6), (d, 0, "easeInOut"))
    key(a, "cx_bap.rotate", (0, 0), (0.07, 20, "easeOut"), (0.3, 8), (d, 0, "easeInOut"))
    key(a, "cx_cang.rotate", (0, 0), (0.1, 18, "easeOut"), (0.3, 6), (d, 0, "easeInOut"))
    ops(f"anim.spring {a} bones=rt1,rt2,rt3 stiffness=0.2 damping=0.5", f"anim.spring {a} bones=rs1,rs2,rs3 stiffness=0.2 damping=0.5",
        f"anim.spring {a} bones=mat_s stiffness=0.2", f"anim.spring {a} bones=mat_t stiffness=0.2",
        f"anim.spring {a} bones=duoi1,duoi2,quat")
    ops(f"vfx.shake {a} bone=than t=0.0 dur=0.18 amp=4 freq=30", f"anim.reduce {a} tol=0.4")


def die():
    a, d = "die", 1.4
    ops(f"anim.add {a} dur={d}")
    # giật lùi 0,07 -> choáng lảo đảo 0,1–0,5 -> gục sập về trước 0,5–0,9 (đầu chúi đất) -> nén khi chạm -> mờ 1,05–1,4
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-14, 2), "easeOut"), (0.3, (-6, 0)), (0.5, (-4, 0)), (0.88, (6, -30), "easeIn"),
        (0.95, (6, -34)), (1.05, (6, -30), "easeOut"), (d, (6, -31)))
    dense(a, "than.rotate", lambda t: (12 * math.sin(math.pi * min(t, 0.14) / 0.14) if t < 0.14 else
                                        4 * math.sin(2 * math.pi * (t - 0.14) / 0.36) if t < 0.5 else
                                        -26 * ((t - 0.5) / 0.38) ** 2 if t < 0.88 else -26 + 3 * math.exp(-(t - 0.88) * 8) * math.sin((t - 0.88) * 30)), d)
    key(a, "than.scale", (0, (1, 1)), (0.88, (1, 1)), (0.93, (1.06, 0.92), "easeOut"), (1.1, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.1, 12), (0.3, -6), (0.45, 4), (0.88, -16, "easeIn"), (0.95, -12), (d, -14))
    key(a, "mat_s.rotate", (0, 0), (0.12, 20), (0.35, -28), (0.6, -22), (0.9, -40), (d, -38))
    key(a, "mat_t.rotate", (0, 0), (0.12, 18), (0.35, -34), (0.6, -26), (0.9, -46), (d, -44))
    key(a, "cg_vai.rotate", (0, 0), (0.07, -20), (0.4, -10, "easeOut"), (0.88, 26, "easeIn"), (0.95, 20), (d, 22))
    key(a, "cg_co.rotate", (0, 0), (0.1, 20), (0.5, 24), (0.88, 6), (d, 8))
    key(a, "cx_bap.rotate", (0, 0), (0.07, 20), (0.4, -20, "easeOut"), (0.88, -58, "easeIn"), (0.95, -52), (d, -54))
    key(a, "cx_cang.rotate", (0, 0), (0.4, -20), (0.88, -40), (d, -38))
    for leg, v in (("chan1", -22), ("chan2", -10), ("chan3", 10), ("chan4", 22)):
        key(a, f"{leg}.rotate", (0, 0), (0.5, 0), (0.9, v, "easeIn"), (1.0, v * 0.85), (d, v * 0.9))
    ops(f"anim.spring {a} bones=rt1,rt2,rt3 stiffness=0.15 damping=0.5", f"anim.spring {a} bones=rs1,rs2,rs3 stiffness=0.15 damping=0.5",
        f"anim.settle {a} bones=duoi1,duoi2,quat at=0.9 cycles=2")
    for sl in SLOTS:
        key(a, f"{sl}.alpha", (0, 1), (1.05, 1), (d, 0))


def appear():
    a, d = "appear", 0.8
    ops(f"anim.add {a} dur={d}")
    for s in SLOTS:
        key(a, f"{s}.alpha", (0, 0), (0.04, 1))
    key(a, "move.translate", (0, (0, 240)), (0.32, (0, 0), "easeIn"), (d, (0, 0)))
    key(a, "than.scale", (0, (1.06, 0.95)), (0.32, (1.06, 0.95)), (0.36, (0.86, 1.1)), (0.47, (1.05, 0.97), "easeOut"),
        (0.6, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "hip.translate", (0, (0, 0)), (0.32, (0, 0)), (0.36, (0, -10)), (0.5, (0, 2), "easeOut"), (0.62, (0, 0)), (d, (0, 0)))
    # rơi: càng giơ cao; chạm đất: thủ thế, đấm nhẹ một cái "chào"
    key(a, "cg_vai.rotate", (0, 18), (0.32, 18), (0.38, -8), (0.55, 30, "easeOut"), (0.64, 6), (d, 0, "easeInOut"))
    key(a, "cg_co.rotate", (0, -10), (0.32, -10), (0.38, 8), (0.55, -26, "easeOut"), (0.64, -4), (d, 0, "easeInOut"))
    key(a, "cx_bap.rotate", (0, 22), (0.32, 22), (0.38, -12), (0.6, 4, "easeOut"), (d, 0, "easeInOut"))
    key(a, "mat_s.rotate", (0, 10), (0.32, 10), (0.4, -12), (0.55, 4), (d, 0))
    key(a, "mat_t.rotate", (0, 10), (0.32, 10), (0.4, -14), (0.55, 5), (d, 0))
    for leg, v in (("chan1", -12), ("chan2", -6), ("chan3", 6), ("chan4", 12)):
        key(a, f"{leg}.rotate", (0, v), (0.32, v), (0.38, -v * 0.6), (0.55, 0, "easeOut"), (d, 0))
    ops(f"anim.spring {a} bones=rt1,rt2,rt3", f"anim.spring {a} bones=rs1,rs2,rs3", f"anim.spring {a} bones=duoi1,duoi2,quat")
    ops(f"vfx.burst {a} image=bot prefix={a}_b bone=move count=8 t=0.32 dur=0.45 speed=200 spread=160 gravity=420 fade=0.4 scale=0.8 scaleEnd=0.4 seed=5",
        f"vfx.ring {a} image=vong slot={a}_vong bone=dat_vong t=0.32 dur=0.4 from=0.2 to=1.6 fade=0.3")


def main():
    ops("# clip + hiệu ứng tôm tít đấm bốc (quái đảo Thủy) — sinh bởi ArtGen/Spine/quai_thuy_anim.py")
    vfx_art()
    for f in (idle, walk, attack, cast, skill, hit, die, appear):
        f()
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{len(L)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
