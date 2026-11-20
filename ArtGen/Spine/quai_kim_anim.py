# -*- coding: utf-8 -*-
"""Quái đảo Kim (nhím thép): sinh lệnh AtomSpine cho clip + hiệu ứng -> quai_kim/atom/anim.ops.

    py -3 -I ArtGen/Spine/quai_kim_anim.py      # rồi: atom do -f anim.ops -p ArtGen/Spine/quai_kim/atom

Nhịp theo skill animation-petclash: idle 2 s lặp (thở, bờm gợn lệch pha, vuốt co duỗi, điểm phá nhịp 1,3 s: xù bờm),
walk 2 s (4 bước lạch bạch, bờm nảy), attack 0,9 s (giơ vuốt lấy đà ngược chiều, cào chéo xuống snap, trúng 0,45, khựng,
về), cast 1,0 s (ngả sau xoè bờm, chồm tới phóng loạt lông 0,5), skill 1,8 s (cuộn tròn lăn một vòng, toả lông 0,85, bung
ra cào kết liễu 1,15), hit 0,6 s (bật 0,07), die 1,4 s (giật, lảo đảo, gục tới, bờm rũ, mờ), appear 0,8 s (cuộn tròn lăn
vào, bung ra, khung đầu trống). Góc xoay cộng vào dáng gốc (độ, CCW); dời cộng (px, y lên).
Hướng xương: than chĩa lên (+ = ngả sau), dau chĩa lên chếch phải (+ = ngửa), tg (tay gần) chĩa phải (+ = giơ lên),
tx (tay xa) chĩa lên trái (+ = vung ra sau / xuống trái), bom_* chĩa sang trái (− = dựng lên, + = rũ xuống).
"""
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "quai_kim", "atom", "anim.ops")
SLOTS = ["bom_duoi", "bom_giua", "bom_tren", "chan_xa", "tay_xa", "tai_xa", "tay_gan", "vuot_gan", "chan_gan", "than", "mat"]
BOM = (("bom_d", 0.0, 1.0), ("bom_g", 0.12, 1.15), ("bom_t", 0.24, 1.3))   # (xương, trễ pha, biên độ)
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


def dense(anim, target, f, dur, fps=30, z=False):
    """khoá dày từ hàm f(t); z=True: trừ giá trị tại t=0 (khung đầu idle / walk đúng dáng gốc -> clip khác nối vào không giật;
    trừ một hằng nên vòng lặp vẫn liền)"""
    n = max(1, round(dur * fps))
    if z:
        f0 = f(0.0)
        if isinstance(f0, tuple):
            g = lambda t: tuple(v - v0 + (1.0 if target.endswith(".scale") else 0.0) for v, v0 in zip(f(t), f0))  # noqa: E731
        else:
            g = lambda t: f(t) - f0  # noqa: E731
    else:
        g = f
    key(anim, target, *[(dur * i / n, g(dur * i / n)) for i in range(n + 1)])


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


def ss(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def pw(pts, t, smooth=()):
    """nội suy theo đoạn (t, v); đoạn bắt đầu ở mốc trong `smooth` thì êm (smoothstep)"""
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            if t0 in smooth:
                u = ss(u)
            return v0 + (v1 - v0) * u
    return pts[-1][1] if t > pts[-1][0] else pts[0][1]


def vfx_art():
    ops("vfx.art manh kind=shard palette=metal size=112 seed=3",
        "vfx.art tia kind=spark palette=metal size=84 seed=5",
        "image.add chem_k path=images/chem_k.png",               # vệt cào ba vuốt tự vẽ (quai_kim_fx.py)
        "vfx.art vong kind=shockwave palette=metal size=300 seed=4",
        "vfx.art cham kind=impact palette=metal size=240 seed=6")


def slash_fx(anim, t, big=False, tag=""):
    """cào trúng: vệt chém quét (vòng co giãn ảnh slash ở vuốt) + chớp va chạm + tia lửa kim loại văng lên rơi xuống"""
    s = 1.3 if big else 1.0
    ops(f"vfx.ring {anim} image=chem_k slot={anim}_chem{tag} bone=tg_vong t={t - 0.03:.3f} dur={0.24 * s:.3f} from=0.55 to={1.35 * s:.2f} fade=0.35",
        f"vfx.ring {anim} image=cham slot={anim}_cham{tag} bone=tg_vong t={t:.3f} dur={0.2 * s:.3f} from=0.35 to={1.0 * s:.2f} fade=0.15",
        f"vfx.burst {anim} image=tia prefix={anim}_t{tag} bone=tg_mui count={9 if big else 7} t={t:.3f} dur={0.42 * s:.3f} "
        f"speed={520 * s:.0f} spread=150 gravity=1100 spin=240 fade=0.5 scale=1.4 scaleEnd=0.45 seed={7 + len(tag)}")


def bom_idle(a, d, extra=None, amp=2.2, period=None):
    """bờm gợn lệch pha (nhóm trên trễ hơn, biên độ lớn dần) + nhịp riêng extra(t, k) cộng thêm"""
    p = period or d
    for b, ph, k in BOM:
        dense(a, f"{b}.rotate", lambda t, ph=ph, k=k: amp * k * tw(t, p, ph) + (extra(t, k) if extra else 0.0), d, z=True)


def idle():
    a, d = "idle", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=4 period=1.0")
    key(a, "than.scale", (0, (1, 1)), (1.0, (1.025, 0.985), "easeInOut"), (2.0, (1, 1), "easeInOut"))
    dense(a, "than.rotate", lambda t: 1.5 * tw(t, 2) - bump(t, 1.3, 0.06, 0.1, 0.3, 2.5), d, z=True)
    dense(a, "dau.rotate", lambda t: 2 * tw(t, 2, 0.12) - bump(t, 1.28, 0.06, 0.12, 0.3, 4), d, z=True)
    # điểm phá nhịp 1,3 s: xù bờm (dựng lên, xoè, dài ra) rồi hạ, nhóm trên trễ 0,03 s
    bom_idle(a, d, extra=lambda t, k: -bump(t, 1.3 + 0.03 * (k - 1) * 3, 0.06, 0.12, 0.32, 5 * k) + (9 if k == 1.0 else 0) *
             bump(t, 1.3, 0.06, 0.12, 0.32, 1))
    for b, ph, k in BOM:
        dense(a, f"{b}.scale", lambda t, k=k, ph=ph: (1 + bump(t, 1.3 + 0.03 * (k - 1) * 3, 0.06, 0.12, 0.32, 0.11), 1.0), d, z=True)
    dense(a, "tg.rotate", lambda t: 3 * tw(t, 1, 0.2), d, z=True)
    dense(a, "tg_vuot.rotate", lambda t: 4 * tw(t, 1, 0.35) + bump(t, 0.55, 0.08, 0.1, 0.15, 10), d, z=True)   # vuốt co duỗi
    dense(a, "tx.rotate", lambda t: 3 * tw(t, 1, 0.6) - bump(t, 1.32, 0.07, 0.1, 0.3, 6), d, z=True)
    dense(a, "tai_x.rotate", lambda t: 3 * tw(t, 2, 0.3) + bump(t, 0.9, 0.05, 0.04, 0.12, 14), d, z=True)        # giật tai
    ops(f"anim.reduce {a} tol=0.25", f"anim.loopfix {a}")


def walk():
    a, d = "walk", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=6 period=0.5")
    ops(f"anim.wave {a} bones=chan_x prop=rotate amp=16 period=1 phase=0",
        f"anim.wave {a} bones=chan_g prop=rotate amp=16 period=1 phase=0.5")
    dense(a, "chan_x.translate", lambda t: (0, max(0.0, 10 * tw(t, 1, 0.75))), d, z=True)
    dense(a, "chan_g.translate", lambda t: (0, max(0.0, 10 * tw(t, 1, 0.25))), d, z=True)
    dense(a, "than.rotate", lambda t: 3 * tw(t, 1, 0.0), d, z=True)                     # lạch bạch nghiêng theo bước
    dense(a, "dau.rotate", lambda t: 2.5 * tw(t, 1, 0.1), d, z=True)
    dense(a, "tg.rotate", lambda t: 7 * tw(t, 1, 0.5), d, z=True)
    dense(a, "tx.rotate", lambda t: 7 * tw(t, 1, 0.0), d, z=True)
    for b, ph, k in BOM:                                                        # bờm nảy theo từng bước, trễ dần
        dense(a, f"{b}.rotate", lambda t, ph=ph, k=k: 3 * k * tw(t, 0.5, 0.15 + ph), d, z=True)
    dense(a, "tai_x.rotate", lambda t: 4 * tw(t, 0.5, 0.3), d, z=True)
    ops(f"anim.reduce {a} tol=0.25", f"anim.loopfix {a}")


def bom_react(a, d, pts, k_scale=None):
    """bờm theo nhịp thân: pts [(t, góc nhóm trên)], nhóm dưới / giữa theo tỉ lệ, trễ 0,03 s mỗi nhóm"""
    for b, ph, k in BOM:
        lag = 0.03 * (k - 1.0) / 0.15
        sh = [(t + (lag if 0 < t < d else 0), v * k / 1.3) for t, v in pts]
        key(a, f"{b}.rotate", *[(t, v) for t, v in sh])
    if k_scale:
        for b, ph, k in BOM:
            key(a, f"{b}.scale", *[(t, (v, 1.0)) for t, v in k_scale])


def attack():
    a, d = "attack", 0.9
    ops(f"anim.add {a} dur={d}")
    # lấy đà 0–0,3 (ngả sau, hạ vuốt gần xuống thấp sau hông), giữ 0,3–0,38, cào hất chéo lên 0,38–0,45 (snap), khựng, về
    key(a, "hip.translate", (0, (0, 0)), (0.3, (-14, -6), "easeOut"), (0.38, (-14, -6), "snap"), (0.45, (22, -4)), (0.58, (20, -4)),
        (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.3, 10, "easeOut"), (0.38, 11, "snap"), (0.45, -13), (0.58, -11), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.3, (0.95, 1.04), "easeOut"), (0.38, (0.95, 1.04), "snap"), (0.45, (1.06, 0.96)),
        (0.58, (1.02, 0.99), "easeOut"), (d, (1, 1), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.3, 6, "easeOut"), (0.4, 7, "snap"), (0.47, -9), (0.6, -7), (d, 0, "easeInOut"))
    key(a, "tg.rotate", (0, 0), (0.3, -42, "easeOut"), (0.38, -46, "snap"), (0.45, 16), (0.58, 12), (d, 0, "easeInOut"))
    key(a, "tg.scale", (0, (1, 1)), (0.38, (1, 1)), (0.43, (1.18, 0.92)), (0.5, (1, 1), "easeOut"), (d, (1, 1)))
    key(a, "tg_vuot.rotate", (0, 0), (0.3, -18, "easeOut"), (0.38, -20, "snap"), (0.45, 18), (0.58, 14), (d, 0, "easeInOut"))
    key(a, "tx.rotate", (0, 0), (0.3, 12, "easeOut"), (0.45, -14), (0.6, -10), (d, 0, "easeInOut"))
    key(a, "tai_x.rotate", (0, 0), (0.3, 8, "easeOut"), (0.45, -10), (0.55, 6), (0.7, -2), (d, 0, "easeInOut"))
    bom_react(a, d, [(0, 0), (0.3, -6), (0.38, -7), (0.45, 9), (0.55, -4), (0.7, 2), (d, 0)])
    ops(f"event {a} 0.45 hit")
    slash_fx(a, 0.45)


def cast():
    a, d = "cast", 1.0
    ops(f"anim.add {a} dur={d}")
    # ngả sau + xoè dựng bờm 0–0,36, giữ, chồm tới hất bờm phóng lông 0,5 (snap), giữ tới 0,7, về
    key(a, "hip.translate", (0, (0, 0)), (0.36, (-12, -10), "easeOut"), (0.44, (-12, -10), "snap"), (0.5, (14, -6)), (0.7, (12, -6)),
        (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.36, 12, "easeOut"), (0.44, 13, "snap"), (0.5, -16), (0.7, -14), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.36, (0.94, 1.05), "easeOut"), (0.44, (0.94, 1.05), "snap"), (0.5, (1.06, 0.96)),
        (0.62, (1, 1), "easeOut"), (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.36, 8, "easeOut"), (0.46, 9, "snap"), (0.52, -10), (0.72, -8), (d, 0, "easeInOut"))
    key(a, "tx.rotate", (0, 0), (0.36, -18, "easeOut"), (0.5, 10), (0.7, 8), (d, 0, "easeInOut"))
    key(a, "tg.rotate", (0, 0), (0.36, 14, "easeOut"), (0.5, -16), (0.7, -12), (d, 0, "easeInOut"))
    key(a, "tg_vuot.rotate", (0, 0), (0.36, 16, "easeOut"), (0.5, -10), (d, 0, "easeInOut"))
    key(a, "tai_x.rotate", (0, 0), (0.36, -10, "easeOut"), (0.5, 12), (0.62, -4), (d, 0, "easeInOut"))
    # bờm: xoè (trên dựng −, dưới rũ +) và dài ra lúc tụ, hất tới phóng ở 0,5, run nhẹ lúc giữ
    for b, ph, k in BOM:
        fan = {"bom_d": 5, "bom_g": -4, "bom_t": -8}[b]
        flick = {"bom_d": -3, "bom_g": -7, "bom_t": -12}[b]
        key(a, f"{b}.rotate", (0, 0), (0.36, fan, "easeOut"), (0.44 + 0.01 * ph * 10, fan * 1.1, "snap"), (0.5 + 0.01 * ph * 10, flick),
            (0.58, flick * 0.7), (0.7, flick * 0.8), (d, 0, "easeInOut"))
        key(a, f"{b}.scale", (0, (1, 1)), (0.36, (1.07, 1.0), "easeOut"), (0.46, (1.08, 1.0), "snap"), (0.52, (0.97, 1.0)),
            (0.66, (1.02, 1.0), "easeOut"), (d, (1, 1), "easeInOut"))
    ops(f"event {a} 0.5 phun")
    # loạt lông thép bay về phía trước (+x) từ đỉnh bờm, vòng nhả ở chỗ phóng
    ops(f"vfx.burst {a} image=manh prefix={a}_m bone=ban count=10 t=0.5 dur=0.4 speed=1700 spread=36 gravity=0 "
        f"fade=0.7 scale=1.5 scaleEnd=1.1 seed=4",
        f"vfx.ring {a} image=cham slot={a}_cham bone=ban_vong t=0.49 dur=0.22 from=0.3 to=0.9 fade=0.2")


def skill():
    a, d = "skill", 1.8
    ops(f"anim.add {a} dur={d}")
    # 0–0,3 thu mình (đầu chúi, tay chân co, thân tròn lại); 0,32–0,8 lăn một vòng (xoay −360 quanh tâm thân, nảy lên);
    # 0,85 bung bờm toả lông tròn; 0,85–1,08 bung ra, giơ vuốt; 1,15 cào kết liễu (snap); giữ; về
    T_SPIN0, T_SPIN1, T_ZERO = 0.32, 0.76, 0.8

    def spin(t):
        if t < T_SPIN0 or t >= T_ZERO - 1e-6:
            return 0.0                                   # trước / sau cú lăn: 0 (−360 ≡ 0, không để giá trị −360 lúc hoà clip)
        return -360 * ss((t - T_SPIN0) / (T_SPIN1 - T_SPIN0))
    n = round(d * 30)
    i_step = round(T_ZERO * 30) - 1                      # khoá cuối trước 0,8 (= −360) giữ nguyên rồi nhảy về 0 (cùng dáng)
    key(a, "xoay.rotate", *[(i / 30, spin(i / 30), "stepped") if i == i_step else (i / 30, spin(i / 30)) for i in range(n + 1)])
    curl = lambda t: pw([(0, 0), (0.3, 1), (0.82, 1), (1.0, 0)], t, smooth=(0, 0.82))  # noqa: E731

    def hip_p(t):
        return (pw([(0, 0), (0.3, -10), (0.8, 40), (0.9, 34), (1.08, 26), (1.15, 46), (1.4, 44), (d, 0)], t, smooth=(0, 0.3, 1.4)),
                pw([(0, 0), (0.3, -24), (0.56, 70), (0.8, -6), (0.9, 0), (d, 0)], t, smooth=(0.3, 0.56, 0.8)))
    dense(a, "hip.translate", hip_p, d)
    dense(a, "than.scale", lambda t: (1 - 0.1 * curl(t), 1 + 0.06 * curl(t)), d)
    dense(a, "dau.rotate", lambda t: -20 * curl(t) + pw([(0, 0), (0.85, 0), (1.05, 8), (1.15, -10), (1.4, -8), (d, 0)], t,
                                                       smooth=(1.4,)), d)
    dense(a, "than.rotate", lambda t: pw([(0, 0), (0.85, 0), (1.05, 10), (1.15, -14), (1.4, -12), (d, 0)], t, smooth=(0.85, 1.4)), d)
    dense(a, "tx.rotate", lambda t: -58 * curl(t) + pw([(0, 0), (1.0, 0), (1.15, -12), (1.4, -8), (d, 0)], t, smooth=(1.4,)), d)
    # tay gần: co sát thân lúc cuộn, bung ra hạ thấp lấy đà (1,05–1,1), cào hất chéo lên 1,15 (snap), giữ, về
    dense(a, "tg.rotate", lambda t: pw([(0, 0), (0.3, -48), (0.82, -48), (1.05, -46), (1.1, -48), (1.15, 36), (1.4, 31), (d, 0)], t,
                                       smooth=(0, 0.82, 1.4)), d)
    dense(a, "tg_vuot.rotate", lambda t: pw([(0, 0), (0.3, -30), (0.82, -30), (1.05, -18), (1.1, -20), (1.15, 26), (1.4, 21), (d, 0)], t,
                                            smooth=(0, 0.82, 1.4)), d)
    key(a, "tg.scale", (0, (1, 1)), (1.1, (1, 1)), (1.14, (1.2, 0.92)), (1.22, (1, 1), "easeOut"), (d, (1, 1)))
    for leg, s in (("chan_x", 1), ("chan_g", -1)):        # chân co vào trong khối cầu, theo hông lúc nảy (chân gắn move)
        dense(a, f"{leg}.translate", lambda t, s=s: (s * 14 * curl(t) + hip_p(t)[0] * (0.6 + 0.4 * curl(t)),
                                                     80 * curl(t) + max(0.0, hip_p(t)[1]) * curl(t)), d)
        dense(a, f"{leg}.rotate", lambda t, s=s: -s * 30 * curl(t), d)
    # bờm: xoè hết cỡ lúc lăn (quả cầu gai), giật toả ở 0,85, về
    for b, ph, k in BOM:
        fan = {"bom_d": 6, "bom_g": -4, "bom_t": -15}[b]   # bờm trên theo đầu chúi
        dense(a, f"{b}.rotate", lambda t, fan=fan, k=k: fan * curl(t) + pw([(0, 0), (0.83, 0), (0.88, -6 * k), (1.0, 2 * k), (1.2, 0),
                                                                             (d, 0)], t, smooth=(1.0,)), d)
        dense(a, f"{b}.scale", lambda t: (1 + 0.08 * curl(t) + bump(t, 0.83, 0.04, 0.03, 0.2, 0.06), 1.0), d)
    key(a, "tai_x.rotate", (0, 0), (0.3, -16, "easeOut"), (0.85, -16), (1.0, 10), (1.15, -8), (1.3, 3), (d, 0, "easeInOut"))
    ops(f"event {a} 0.85 hit", f"event {a} 1.15 hit")
    # 0,85: lông thép toả tròn từ tâm thân + vòng sóng kim loại; 1,15: cào kết liễu
    ops(f"vfx.burst {a} image=manh prefix={a}_m bone=than_tam count=12 t=0.85 dur=0.42 speed=1300 spread=360 gravity=0 "
        f"fade=0.65 scale=1.5 scaleEnd=1.1 seed=9",
        f"vfx.ring {a} image=cham slot={a}_cham bone=than_vong t=0.85 dur=0.26 from=0.5 to=1.9 fade=0.2",
        f"vfx.ring {a} image=vong slot={a}_vong bone=dat_vong t=0.86 dur=0.42 from=0.3 to=2.4 fade=0.3",
        f"slot.order {a}_vong to=back")
    slash_fx(a, 1.15, big=True, tag="b")
    ops(f"vfx.shake {a} bone=move t=0.85 dur=0.2 amp=6", f"vfx.shake {a} bone=move t=1.15 dur=0.22 amp=7 seed=2")


def hit():
    a, d = "hit", 0.6
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-18, 3), "easeOut"), (0.25, (-10, 0)), (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.07, 14, "easeOut"), (0.3, 7), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.07, (0.94, 1.05), "easeOut"), (0.25, (1.01, 0.99)), (d, (1, 1), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.1, 13, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    key(a, "tg.rotate", (0, 0), (0.07, 24, "easeOut"), (0.3, 8), (d, 0, "easeInOut"))
    key(a, "tg_vuot.rotate", (0, 0), (0.1, 20, "easeOut"), (0.3, 6), (d, 0, "easeInOut"))
    key(a, "tx.rotate", (0, 0), (0.07, 18, "easeOut"), (0.3, 6), (d, 0, "easeInOut"))
    key(a, "tai_x.rotate", (0, 0), (0.08, 16, "easeOut"), (0.22, -6), (0.38, 2), (d, 0, "easeInOut"))
    # bờm dựng ngược theo cú bật (ngọn trễ hơn), lắc tắt dần
    for b, ph, k in BOM:
        key(a, f"{b}.rotate", (0, 0), (0.07 + ph * 0.25, -8 * k, "easeOut"), (0.22 + ph * 0.25, 4 * k), (0.38, -1.5 * k), (d, 0, "easeInOut"))
    ops(f"vfx.shake {a} bone=than t=0.0 dur=0.18 amp=4 freq=30", f"anim.reduce {a} tol=0.4")


def die():
    a, d = "die", 1.4
    ops(f"anim.add {a} dur={d}")
    # giật lùi 0,07 -> lảo đảo 0,1–0,5 -> gục về trước 0,5–0,88 -> nén khi chạm -> bờm rũ -> mờ 1,05–1,4
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-14, 2), "easeOut"), (0.3, (-6, 0)), (0.5, (-4, 0)), (0.88, (10, -40), "easeIn"),
        (0.95, (10, -44)), (1.05, (10, -40), "easeOut"), (d, (10, -41)))
    dense(a, "than.rotate", lambda t: (12 * math.sin(math.pi * min(t, 0.14) / 0.14) if t < 0.14 else
                                        4 * math.sin(2 * math.pi * (t - 0.14) / 0.36) if t < 0.5 else
                                        -30 * ((t - 0.5) / 0.38) ** 2 if t < 0.88 else -30 + 3 * math.exp(-(t - 0.88) * 8) * math.sin((t - 0.88) * 30)), d)
    key(a, "than.scale", (0, (1, 1)), (0.88, (1, 1)), (0.93, (0.9, 1.08), "easeOut"), (1.1, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.1, 12), (0.3, -6), (0.45, 4), (0.88, -18, "easeIn"), (0.95, -13), (d, -15))
    key(a, "tg.rotate", (0, 0), (0.07, 22), (0.4, 6, "easeOut"), (0.88, -40, "easeIn"), (0.95, -34), (d, -36))
    key(a, "tg_vuot.rotate", (0, 0), (0.1, 16), (0.5, 4), (0.88, -24), (d, -22))
    key(a, "tx.rotate", (0, 0), (0.07, 16), (0.4, -6, "easeOut"), (0.88, 40, "easeIn"), (0.95, 34), (d, 36))
    key(a, "tai_x.rotate", (0, 0), (0.1, 14), (0.3, -8), (0.6, 4), (0.9, 18), (d, 16))
    for leg, v in (("chan_x", -14), ("chan_g", 12)):
        key(a, f"{leg}.rotate", (0, 0), (0.5, 0), (0.9, v, "easeIn"), (1.0, v * 0.85), (d, v * 0.9))
    for b, ph, k in BOM:                                  # bờm dựng lúc giật; khi gục: nhóm dưới rũ xuống, nhóm trên theo đầu chúi
        g = {"bom_d": 6, "bom_g": 3, "bom_t": -10}[b]
        key(a, f"{b}.rotate", (0, 0), (0.07 + ph * 0.2, -8 * k, "easeOut"), (0.35, 2 * k), (0.88, g, "easeIn"),
            (0.96 + ph * 0.15, g * 0.7), (1.1, g * 0.9, "easeOut"), (d, g * 0.9))
    for sl in SLOTS:
        key(a, f"{sl}.alpha", (0, 1), (1.05, 1), (d, 0))


def appear():
    a, d = "appear", 0.8
    ops(f"anim.add {a} dur={d}")
    for s in SLOTS:
        key(a, f"{s}.alpha", (0, 0), (0.04, 1))
    # cuộn tròn lăn vào từ trái (xoay +360 -> 0, tức lăn về phía phải), bung ra ở 0,4, nén, thủ thế
    curl = lambda t: pw([(0, 1), (0.36, 1), (0.52, 0)], t, smooth=(0.36,))  # noqa: E731
    dense(a, "xoay.rotate", lambda t: 360 * (1 - ss(min(1.0, t / 0.4))), d)
    dense(a, "move.translate", lambda t: (-260 * (1 - ss(min(1.0, t / 0.4))), 0), d)
    hip_y = lambda t: pw([(0, 30), (0.2, 50), (0.4, 0), (0.46, -12), (0.6, 2), (0.7, 0), (d, 0)], t,  # noqa: E731
                         smooth=(0, 0.2, 0.46, 0.6))
    dense(a, "hip.translate", lambda t: (0, hip_y(t)), d)
    dense(a, "than.scale", lambda t: (1 - 0.1 * curl(t) - bump(t, 0.4, 0.04, 0.02, 0.15, 0.06), 1 + 0.06 * curl(t) +
                                      bump(t, 0.4, 0.04, 0.02, 0.15, 0.05)), d)
    dense(a, "dau.rotate", lambda t: -20 * curl(t) + bump(t, 0.48, 0.06, 0.04, 0.18, 6), d)
    dense(a, "tx.rotate", lambda t: -58 * curl(t) - bump(t, 0.5, 0.06, 0.03, 0.18, 10), d)
    dense(a, "tg.rotate", lambda t: -48 * curl(t) + bump(t, 0.5, 0.06, 0.03, 0.18, 18), d)
    dense(a, "tg_vuot.rotate", lambda t: -30 * curl(t) + bump(t, 0.52, 0.05, 0.03, 0.17, 14), d)
    for leg, s in (("chan_x", 1), ("chan_g", -1)):
        dense(a, f"{leg}.translate", lambda t, s=s: (s * 14 * curl(t), 80 * curl(t) + max(0.0, hip_y(t)) * curl(t)), d)
        dense(a, f"{leg}.rotate", lambda t, s=s: -s * 30 * curl(t), d)
    for b, ph, k in BOM:
        fan = {"bom_d": 6, "bom_g": -4, "bom_t": -15}[b]   # bờm trên theo đầu chúi
        dense(a, f"{b}.rotate", lambda t, fan=fan, k=k, ph=ph: fan * curl(t) - bump(t, 0.46 + ph * 0.15, 0.05, 0.04, 0.18, 7 * k), d)
        dense(a, f"{b}.scale", lambda t: (1 + 0.08 * curl(t), 1.0), d)
    ops(f"vfx.burst {a} image=tia prefix={a}_t bone=move count=6 t=0.4 dur=0.4 speed=380 spread=150 gravity=900 spin=200 "
        f"fade=0.5 scale=1.4 scaleEnd=0.45 seed=5",
        f"vfx.ring {a} image=vong slot={a}_vong bone=dat_vong t=0.4 dur=0.38 from=0.3 to=2.2 fade=0.3",
        f"slot.order {a}_vong to=back")


def main():
    ops("# clip + hiệu ứng nhím thép (quái đảo Kim) — sinh bởi ArtGen/Spine/quai_kim_anim.py")
    vfx_art()
    for f in (idle, walk, attack, cast, skill, hit, die, appear):
        f()
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{len(L)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
