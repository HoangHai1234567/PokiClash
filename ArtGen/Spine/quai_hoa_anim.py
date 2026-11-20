# -*- coding: utf-8 -*-
"""Quái lính đảo Hỏa (gà chọi lửa): sinh lệnh AtomSpine cho clip + hiệu ứng -> quai_hoa/atom/anim.ops.

    py -3 -I ArtGen/Spine/quai_hoa_anim.py      # rồi: atom do -f anim.ops -p ArtGen/Spine/quai_hoa/atom

Nhịp theo skill animation-petclash: idle 2 s lặp (thở, đầu giật kiểu gà, mào + đuôi lửa uốn lệch pha, điểm phá nhịp vỗ cánh
1,25–1,55), walk 2 s (4 bước nghênh ngang, đầu thụt tới lui), attack 0,9 s (nhún ngả sau 0,24 s, giữ, đá cựa chân trước bật 3
khung, trúng 0,45, khựng, về), cast 1,0 s (ưỡn ngực hít, chồm đầu há mỏ phun lửa 0,5, giữ tới 0,78), skill 1,8 s (vỗ cánh bật
lên, đá liên hoàn trên không 0,80 và 1,10, đáp đất rung 1,42), hit 0,6 s (bật 0,07), die 1,4 s (giật, lảo đảo, gục chúi, mờ
1,05–1,4), appear 0,8 s (khung đầu trống, vỗ cánh rơi xuống, đáp nén, gáy). Góc cộng vào dáng gốc (độ, CCW); dời cộng (px, y lên).
Chân gắn move: thân nhún trên hip, bàn chân đứng yên; đá = xoay cẳng (+ là đá ra trước).
"""
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quai_hoa_rig as R  # noqa: E402

OUT = os.path.join(HERE, "quai_hoa", "atom", "anim.ops")
SLOTS = ["canh_xa", "duoi", "chan_trai", "chan_phai", "than", "chan_phai_truoc", "mao", "dau", "mo_duoi", "canh_gan"]
TAIL = [("d1a", "d1b"), ("d2a", "d2b"), ("d3a", "d3b"), ("d4a", "d4b")]
COMB = [("m1a", "m1b"), ("m2a", "m2b"), ("m3a", "m3b")]
THAN_ANG = 67.83          # góc dáng gốc xương thân (độ): dời đầu theo hệ của thân
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
    n = max(1, round(dur * fps))
    key(anim, target, *[(dur * i / n, f(dur * i / n)) for i in range(n + 1)])


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


def fwd(dx, dy):
    """dời (dx, dy) thế giới -> hệ của xương thân (dời đầu)"""
    a = math.radians(-THAN_ANG)
    return dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)


# ---------------------------------------------------------------- FK chân (tính chỗ mũi vuốt ở khung trúng)
def _w(pt):
    return pt[0] - R.OX, R.OY - pt[1]


def _rot(v, deg):
    a = math.radians(deg)
    return v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a)


B = {n: (a, b) for n, _, a, b in R.BONES}
TOE = {"p": (1100, 932), "t": (660, 930)}


def toe(leg, dc, db, mv=(0, 0), tr=(0, 0)):
    """mũi vuốt (thế giới, y lên): cẳng xoay dc, bàn thêm db, cẳng dời tr (hệ move), move dời mv"""
    J, A = _w(B[f"chan_{leg}"][0]), _w(B[f"ban_{leg}"][0])
    J, A = (J[0] + tr[0], J[1] + tr[1]), (A[0] + tr[0], A[1] + tr[1])
    T = _w(TOE[leg])
    T = (T[0] + tr[0], T[1] + tr[1])
    a1 = _rot((A[0] - J[0], A[1] - J[1]), dc)
    A2 = (J[0] + a1[0], J[1] + a1[1])
    t1 = _rot((T[0] - A[0], T[1] - A[1]), dc + db)
    return A2[0] + t1[0] + mv[0], A2[1] + t1[1] + mv[1]


# ---------------------------------------------------------------- phụ kiện lửa
def flames(anim, dur, amp=1.0, period=None, tail=True):
    """mào 3 lưỡi + đuôi 4 lông lửa: sóng lặp liền, mỗi chuỗi một pha, ngọn lắc mạnh hơn gốc. Mọi clip cùng biên độ, pha
    (chỉ khác chu kỳ, chu kỳ khít thời lượng) nên khung đầu / cuối clip trùng khung 0 idle: hết clip về idle không giật."""
    p = period or dur / 2
    for i, (a, b) in enumerate(COMB):
        ops(f"anim.wave {anim} bones={a},{b} prop=rotate amp={4 * amp:.1f} period={p:.3f} lag=0.18 phase={0.27 * i:.2f} growth=1.8")
    if tail:
        for i, (a, b) in enumerate(TAIL):
            ops(f"anim.wave {anim} bones={a},{b} prop=rotate amp={3.5 * amp:.1f} period={p * 2:.3f} lag=0.15 phase={0.21 * i + 0.1:.2f} growth=1.7")


def leg_front(anim, t_on, t_x0, t_off):
    """chân trước ra trước thân: từ t_on tắt chân gốc (sau thân), bật bản sao chan_phai_truoc (trước thân); từ t_x0 chân gốc bật
    lại dưới bản sao, bản sao mờ dần tới t_off rồi tắt (nắp đùi lặn dần sau thân, không chớp đổi lớp). Khoá hình bậc + độ đậm."""
    ops(f"key {anim} chan_phai.attachment 0:chan_phai {t_on:.3f}:- {t_x0:.3f}:chan_phai",
        f"key {anim} chan_phai_truoc.attachment 0:- {t_on:.3f}:chan_phai_truoc {t_off:.3f}:-",
        f"key {anim} chan_phai_truoc.alpha 0:1 {t_x0:.3f}:1 {t_off:.3f}:0")


def follow(anim, pairs, dur, k=0.6, lag=0.08, bone="duoi"):
    """gốc đuôi theo đà: ngược chiều xoay thân, trễ `lag` giây (lông lửa trên nó vẫn sóng riêng)"""
    out = [(0.0, 0.0)]
    for t, v in pairs:
        tt = min(dur, t + lag)
        if tt > out[-1][0] + 1e-3:
            out.append((tt, -k * v, "easeInOut"))
    if out[-1][0] < dur - 1e-3:
        out.append((dur, out[-1][1]))
    key(anim, f"{bone}.rotate", *out)


def vfx_art():
    ops("vfx.art lua kind=flame palette=fire size=96 seed=3",
        "vfx.art tia kind=spark palette=fire size=56 seed=5",
        "vfx.art vong kind=shockwave palette=fire size=192 seed=4",
        "vfx.art cham kind=impact palette=fire size=160 seed=6",
        "vfx.art bui kind=puff palette=earth size=88 seed=7")


def kick_fx(anim, t, emit, ring, big=False, tag=""):
    """trúng cú đá: chớp va chạm + vòng lửa + tia lửa văng (nổ sớm, loang, tan)"""
    s = 1.3 if big else 1.0
    ops(f"vfx.ring {anim} image=cham slot={anim}_cham{tag} bone={ring} t={t:.3f} dur={0.2 * s:.3f} from=0.3 to={0.85 * s:.2f} fade=0.12",
        f"vfx.ring {anim} image=vong slot={anim}_vong{tag} bone={ring} t={t + 0.02:.3f} dur={0.4 * s:.3f} from=0.15 to={1.3 * s:.2f} fade=0.3",
        f"vfx.burst {anim} image=tia prefix={anim}_t{tag} bone={emit} count={6 if big else 8} t={t:.3f} dur={0.45 * s:.3f} "
        f"speed={320 * s:.0f} spread=360 gravity=420 spin=200 fade=0.45 scale=0.9 scaleEnd=0.35 seed={9 + len(tag)}")


# ---------------------------------------------------------------- clip
def idle():
    a, d = "idle", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=3 period=1.0")
    key(a, "than.scale", (0, (1, 1)), (1.0, (1.03, 0.985), "easeInOut"), (2.0, (1, 1), "easeInOut"))
    ops(f"anim.wave {a} bones=than prop=rotate amp=1.2 period=2")
    # đầu kiểu gà: đứng im rồi giật nhanh (2 khung) tới / lui, nghiêng nhẹ; điểm phá nhịp cúi gằm rồi ngẩng
    f0, f1 = fwd(12, 0), fwd(-6, 2)

    def head_t(t):
        if t < 0.32:
            return (0, 0)
        if t < 0.38:
            u = (t - 0.32) / 0.06
            return (f0[0] * u, f0[1] * u)
        if t < 0.86:
            return f0
        if t < 0.92:
            u = (t - 0.86) / 0.06
            return (f0[0] + (f1[0] - f0[0]) * u, f0[1] + (f1[1] - f0[1]) * u)
        if t < 1.6:
            return f1
        if t < 1.68:
            u = (t - 1.6) / 0.08
            return (f1[0] * (1 - u), f1[1] * (1 - u))
        return (0, 0)
    dense(a, "dau.translate", head_t, d)
    dense(a, "dau.rotate", lambda t: (-4 if 0.38 <= t < 0.86 else 0) + bump(t, 1.22, 0.06, 0.12, 0.1, -9) + bump(t, 1.5, 0.05, 0.05, 0.1, 6)
          + 1.2 * tw(t, 2, 0.1), d)
    # điểm phá nhịp 1,25–1,55: vỗ cánh gần hai cái ngắn, cánh xa theo sau
    dense(a, "canh_gan.rotate", lambda t: 2 * tw(t, 1, 0.0) - bump(t, 1.25, 0.06, 0.02, 0.07, 24) - bump(t, 1.41, 0.06, 0.02, 0.08, 20), d)
    dense(a, "canh_gan2.rotate", lambda t: 2 * tw(t, 1, 0.5) - bump(t, 1.27, 0.06, 0.02, 0.07, 14) - bump(t, 1.43, 0.06, 0.02, 0.08, 12), d)
    dense(a, "canh_xa.rotate", lambda t: 2 * tw(t, 1, 0.5) - bump(t, 1.29, 0.06, 0.02, 0.08, 16) - bump(t, 1.45, 0.06, 0.02, 0.08, 12), d)
    dense(a, "mo_duoi.rotate", lambda t: -bump(t, 1.24, 0.04, 0.08, 0.06, 8), d)
    flames(a, d)
    ops(f"anim.loopfix {a}")


def walk():
    a, d = "walk", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    ops(f"anim.bob {a} bone=hip amp=6 period=0.5")
    # bước: chân trước, chân sau lệch nửa chu kỳ; bàn gập khi nhấc
    ops(f"anim.wave {a} bones=chan_p prop=rotate amp=16 period=1 phase=0",
        f"anim.wave {a} bones=chan_t prop=rotate amp=16 period=1 phase=0.5",
        f"anim.wave {a} bones=ban_p prop=rotate amp=10 period=1 phase=0",
        f"anim.wave {a} bones=ban_t prop=rotate amp=10 period=1 phase=0.5",
        f"anim.wave {a} bones=than prop=rotate amp=3 period=1 phase=0",
        f"anim.wave {a} bones=canh_gan prop=rotate amp=6 period=0.5 phase=0",
        f"anim.wave {a} bones=canh_xa prop=rotate amp=5 period=0.5 phase=0.5")
    # đầu thụt tới lui mỗi bước (giữ rồi giật)
    f0 = fwd(14, 0)

    def head_t(t):
        u = (t % 0.5) / 0.5
        k = 1.0 if u < 0.55 else max(0.0, 1 - (u - 0.55) / 0.12)
        k = k if u >= 0.08 else u / 0.08
        return (f0[0] * k, f0[1] * k)
    dense(a, "dau.translate", head_t, d)
    ops(f"anim.wave {a} bones=dau prop=rotate amp=3 period=0.5 phase=0.5")
    flames(a, d, period=0.5)
    ops(f"anim.loopfix {a}")


def attack():
    a, d, th = "attack", 0.9, 0.45
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.24, (-14, -8), "easeOut"), (0.36, (-15, -9), "snap"), (th, (16, 6)), (0.58, (14, 5)),
        (d, (0, 0), "easeInOut"))
    TR = [(0, 0), (0.24, 10), (0.36, 11), (th, -14), (0.58, -12), (d, 0)]
    key(a, "than.rotate", (0, 0), (0.24, 10, "easeOut"), (0.36, 11, "snap"), (th, -14), (0.58, -12), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.24, (0.94, 1.04)), (0.36, (0.93, 1.05), "snap"), (th, (1.06, 0.96)), (0.6, (1, 1), "easeOut"), (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.26, 8, "easeOut"), (0.38, 9), (th + 0.03, -10), (0.6, -8), (d, 0, "easeInOut"))
    # đá cựa chân trước: kéo lùi lấy đà -> bật ra 3 khung -> khựng -> về
    key(a, "chan_p.rotate", (0, 0), (0.24, -16, "easeOut"), (0.36, -18, "snap"), (th, 86), (0.58, 82), (d, 0, "easeInOut"))
    key(a, "ban_p.rotate", (0, 0), (0.24, -18, "easeOut"), (0.36, -20, "snap"), (th, -14), (0.58, -12), (d, 0, "easeInOut"))
    key(a, "chan_p.scale", (0, (1, 1)), (0.36, (1, 1)), (th, (1.14, 0.94)), (th + 0.07, (1, 1), "easeOut"), (d, (1, 1)))
    # cẳng nhô ra trước + lên khỏi bụng lúc đá, vẽ TRƯỚC thân từ lúc bật tới lúc gần về (khoá thứ tự vẽ: bậc thang)
    TRK = (20, 34)
    key(a, "chan_p.translate", (0, (0, 0)), (0.36, (-4, 0), "snap"), (th, TRK), (0.58, (TRK[0] - 2, TRK[1] - 2)), (d, (0, 0), "easeInOut"))
    leg_front(a, 0.37, 0.82, 0.9)
    key(a, "chan_t.rotate", (0, 0), (0.24, 6, "easeOut"), (th, -6), (0.58, -5), (d, 0, "easeInOut"))
    # cánh dang lấy thăng bằng: giơ lúc lấy đà, đập xuống lúc đá
    key(a, "canh_gan.rotate", (0, 0), (0.24, -28, "easeOut"), (0.36, -30, "snap"), (th, 14), (0.6, 8), (d, 0, "easeInOut"))
    key(a, "canh_gan2.rotate", (0, 0), (0.28, -14, "easeOut"), (th + 0.03, 10), (0.6, 4), (d, 0, "easeInOut"))
    key(a, "canh_xa.rotate", (0, 0), (0.26, -24, "easeOut"), (0.38, -26, "snap"), (th + 0.02, 10), (0.6, 6), (d, 0, "easeInOut"))
    ops(f"event {a} {th} hit")
    follow(a, TR, d)
    flames(a, d, period=0.45)
    x, y = toe("p", 86, -14, tr=TRK)
    ops(f"bone.set fx_da1 x={x:.1f} y={y:.1f} world=true", f"bone.set fx_da1v x={x:.1f} y={y:.1f} world=true")
    kick_fx(a, th, "fx_da1", "fx_da1v")
    ops(f"vfx.shake {a} bone=than t={th:.3f} dur=0.14 amp=4 seed=3")      # rung giật lúc trúng (than không có khoá dời)
    return x, y


def cast():
    a, d, th = "cast", 1.0, 0.5
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.38, (-12, 2), "easeOut"), (0.44, (-13, 2), "snap"), (th, (12, 0)), (0.78, (10, 0)),
        (d, (0, 0), "easeInOut"))
    TR = [(0, 0), (0.38, 12), (0.44, 13), (th, -9), (0.78, -7), (d, 0)]
    key(a, "than.rotate", (0, 0), (0.38, 12, "easeOut"), (0.44, 13, "snap"), (th, -9), (0.78, -7), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.38, (1.04, 1.06), "easeOut"), (0.44, (1.05, 1.07), "snap"), (th, (0.97, 0.98)),
        (0.78, (0.98, 0.99)), (d, (1, 1), "easeInOut"))
    b0, b1 = fwd(-8, 4), fwd(16, -2)
    key(a, "dau.translate", (0, (0, 0)), (0.38, b0, "easeOut"), (0.44, b0, "snap"), (th, b1), (0.78, b1), (d, (0, 0), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.38, 16, "easeOut"), (0.44, 17, "snap"), (th, -8), (0.78, -6), (d, 0, "easeInOut"))
    key(a, "mo_duoi.rotate", (0, 0), (0.42, -4, "easeOut"), (0.47, -24), (0.78, -22), (0.9, 0, "easeIn"), (d, 0))
    key(a, "canh_gan.rotate", (0, 0), (0.38, -16, "easeOut"), (th, 10), (0.78, 8), (d, 0, "easeInOut"))
    key(a, "canh_xa.rotate", (0, 0), (0.4, -18, "easeOut"), (th + 0.02, 8), (0.78, 6), (d, 0, "easeInOut"))
    ops(f"event {a} {th} phun")
    follow(a, TR, d)
    flames(a, d, period=0.5)
    # lửa phun ra trước mỏ (nón quanh +x của phun_e), khói theo sau, chớp ở mỏ
    ops(f"vfx.ring {a} image=cham slot={a}_cham bone=m_vong t={th:.3f} dur=0.2 from=0.4 to=1.1 fade=0.12",
        f"vfx.burst {a} image=lua prefix={a}_l bone=phun_e count=10 t={th:.3f} dur=0.42 speed=700 spread=30 gravity=0 spin=60 "
        f"fade=0.5 scale=2.0 scaleEnd=4.2 seed=4",
        f"vfx.burst {a} image=tia prefix={a}_k bone=phun_e count=4 t={th + 0.04:.3f} dur=0.4 speed=720 spread=40 gravity=0 spin=120 "
        f"fade=0.4 scale=1.2 scaleEnd=0.5 seed=8",
        f"vfx.shake {a} bone=than t={th:.3f} dur=0.14 amp=3 seed=4")


def skill():
    a, d, h1, h2 = "skill", 1.8, 0.80, 1.10
    ops(f"anim.add {a} dur={d}")
    mv = [(0, (0, 0)), (0.32, (0, 0)), (0.36, (0, -6)), (0.56, (16, 96), "easeOut"), (h1, (26, 88)), (h2, (32, 74)),
          (1.28, (30, 62)), (1.42, (22, 0), "easeIn"), (1.48, (22, -6)), (1.62, (18, 0), "easeOut"), (d, (0, 0), "easeInOut")]
    key(a, "move.translate", *mv)
    # nhún lấy đà bật nhảy, ngả lưng trên không, chúi tới lúc đá; đáp nén
    key(a, "hip.translate", (0, (0, 0)), (0.3, (-8, -12), "easeOut"), (0.36, (-8, -14)), (0.5, (0, 4)), (1.42, (0, 0)),
        (1.48, (0, -12)), (1.62, (0, 2), "easeOut"), (d, (0, 0), "easeInOut"))
    TR = [(0, 0), (0.3, 8), (0.5, -4), (0.7, 12), (0.74, 13), (h1, -16), (0.9, -6), (1.02, 10), (h2, -18), (1.28, -10), (1.48, -6), (d, 0)]
    key(a, "than.rotate", (0, 0), (0.3, 8, "easeOut"), (0.5, -4), (0.7, 12, "easeOut"), (0.74, 13, "snap"), (h1, -16), (0.9, -6),
        (1.02, 10, "snap"), (h2, -18), (1.28, -10), (1.48, -6), (d, 0, "easeInOut"))
    key(a, "than.scale", (0, (1, 1)), (0.3, (0.92, 1.05)), (0.4, (1.08, 0.95)), (0.55, (1, 1), "easeOut"), (1.42, (1, 1)),
        (1.47, (0.88, 1.08)), (1.62, (1.03, 0.98), "easeOut"), (d, (1, 1), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.3, 6), (0.72, 10, "easeOut"), (h1 + 0.03, -10), (1.0, 6), (h2 + 0.03, -12), (1.3, -6),
        (1.47, -10), (d, 0, "easeInOut"))
    key(a, "mo_duoi.rotate", (0, 0), (0.7, 0), (h1, -14), (0.95, -4), (h2, -16), (1.3, -2), (1.5, 0))
    # cánh: giơ cao lấy đà, đập xuống lúc bật, vỗ nhanh giữ trên không, dang lúc đáp
    key(a, "canh_gan.rotate", (0, 0), (0.3, -46, "easeOut"), (0.4, 28), (0.52, -40, "easeOut"), (0.64, 22), (0.74, -36),
        (h1, 18), (0.92, -38), (1.02, 20), (h2, 14), (1.2, -34), (1.32, 16), (1.44, -20), (1.6, 6, "easeOut"), (d, 0, "easeInOut"))
    key(a, "canh_gan2.rotate", (0, 0), (0.32, -20, "easeOut"), (0.42, 14), (0.54, -18), (0.66, 12), (0.76, -16), (h1 + 0.02, 10),
        (0.94, -16), (1.04, 10), (1.22, -14), (1.34, 8), (1.46, -10), (d, 0, "easeInOut"))
    key(a, "canh_xa.rotate", (0, 0), (0.32, -38, "easeOut"), (0.42, 22), (0.54, -34, "easeOut"), (0.66, 18), (0.76, -30),
        (h1 + 0.02, 14), (0.94, -30), (1.04, 16), (1.22, -28), (1.34, 12), (1.46, -16), (d, 0, "easeInOut"))
    # chân trước: co lại trên không, đá cao 0,80, thu về, đá chéo xuống 1,10; chân sau co đối trọng
    key(a, "chan_p.rotate", (0, 0), (0.3, -10, "easeOut"), (0.36, -12), (0.56, 28, "easeOut"), (0.74, -20, "snap"), (h1, 82),
        (0.9, 70), (1.0, 6, "snap"), (h2, 52), (1.24, 46), (1.42, 0, "easeIn"), (d, 0))
    key(a, "ban_p.rotate", (0, 0), (0.56, 18, "easeOut"), (0.74, -24, "snap"), (h1, -12), (0.9, -10), (1.0, -26, "snap"), (h2, 8),
        (1.24, 6), (1.42, 0), (d, 0))
    key(a, "chan_p.scale", (0, (1, 1)), (0.74, (1, 1)), (h1, (1.15, 0.93)), (h1 + 0.07, (1, 1), "easeOut"), (1.0, (1, 1)),
        (h2, (1.12, 0.95)), (h2 + 0.07, (1, 1), "easeOut"), (d, (1, 1)))
    T1, T2 = (18, 24), (14, 14)
    key(a, "chan_p.translate", (0, (0, 0)), (0.56, (6, 10), "easeOut"), (0.74, (0, 4), "snap"), (h1, T1), (0.9, (T1[0] - 2, T1[1] - 2)),
        (1.0, (2, 6), "snap"), (h2, T2), (1.24, (12, 12)), (1.42, (0, 0), "easeIn"), (d, (0, 0)))
    leg_front(a, 0.58, 1.40, 1.48)
    key(a, "chan_t.rotate", (0, 0), (0.3, 8, "easeOut"), (0.56, 30, "easeOut"), (h1, 18), (h2, 24), (1.3, 20), (1.42, 0, "easeIn"),
        (1.48, -4), (d, 0, "easeInOut"))
    key(a, "ban_t.rotate", (0, 0), (0.56, 30, "easeOut"), (1.3, 26), (1.42, 0, "easeIn"), (d, 0))
    ops(f"event {a} {h1} hit", f"event {a} {h2} hit")
    follow(a, TR, d)
    flames(a, d, period=0.45)
    p1 = toe("p", 82, -12, tr=T1)          # điểm nổ là con của move: move dời theo cú nhảy tự cộng
    p2 = toe("p", 52, 8, tr=T2)
    ops(f"bone.set fx_da2 x={p2[0]:.1f} y={p2[1]:.1f} world=true", f"bone.set fx_da2v x={p2[0]:.1f} y={p2[1]:.1f} world=true")
    # cú 1 dùng điểm nổ riêng của skill (khác chỗ đòn đánh): dùng fx_da2 cho cú 2, cú 1 dùng xương skill riêng sk1 / sk1v
    ops(f"bone.add sk1 parent=move x={p1[0]:.1f} y={p1[1]:.1f} world=true", f"bone.add sk1v parent=move x={p1[0]:.1f} y={p1[1]:.1f} world=true")
    kick_fx(a, h1, "sk1", "sk1v", big=True, tag="a")
    kick_fx(a, h2, "fx_da2", "fx_da2v", big=True, tag="b")
    ops(f"vfx.shake {a} bone=than t={h1:.3f} dur=0.16 amp=5", f"vfx.shake {a} bone=hip t={h2:.3f} dur=0.16 amp=5 seed=2",
        f"vfx.ring {a} image=vong slot={a}_dat bone=dat_vong t=1.42 dur=0.34 from=0.4 to=2.4 fade=0.3")
    return p1, p2


def hit():
    a, d = "hit", 0.6
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-16, 4), "easeOut"), (0.25, (-10, 0)), (d, (0, 0), "easeInOut"))
    key(a, "than.rotate", (0, 0), (0.07, 14, "easeOut"), (0.3, 7), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.1, 14, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    hb = fwd(-10, 4)
    key(a, "dau.translate", (0, (0, 0)), (0.08, hb, "easeOut"), (0.3, (hb[0] * 0.3, hb[1] * 0.3)), (d, (0, 0), "easeInOut"))
    key(a, "mo_duoi.rotate", (0, 0), (0.07, -14, "easeOut"), (0.3, -4), (d, 0, "easeInOut"))
    key(a, "canh_gan.rotate", (0, 0), (0.07, -30, "easeOut"), (0.3, -10), (d, 0, "easeInOut"))
    key(a, "canh_xa.rotate", (0, 0), (0.09, -26, "easeOut"), (0.3, -8), (d, 0, "easeInOut"))
    key(a, "chan_p.rotate", (0, 0), (0.07, -6, "easeOut"), (0.3, -2), (d, 0, "easeInOut"))
    follow(a, [(0, 0), (0.07, 14), (0.3, 7), (d, 0)], d, k=0.8, lag=0.05)
    flames(a, d, period=0.3)
    ops(f"vfx.shake {a} bone=than t=0.0 dur=0.18 amp=4 freq=30", f"anim.reduce {a} tol=0.8")


def die():
    a, d = "die", 1.4
    ops(f"anim.add {a} dur={d}")
    # giật lùi 0,07 -> lảo đảo 0,1–0,5 (đầu ngoẹo, mỏ há) -> gục chúi về trước 0,5–0,9 -> nảy nhẹ -> mờ 1,05–1,4
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-14, 3), "easeOut"), (0.3, (-6, 0)), (0.5, (-2, 0)), (0.88, (14, -44), "easeIn"),
        (0.95, (14, -48)), (1.05, (14, -44), "easeOut"), (d, (14, -45)))
    dense(a, "than.rotate", lambda t: (12 * math.sin(math.pi * min(t, 0.14) / 0.14) if t < 0.14 else
                                        5 * math.sin(2 * math.pi * (t - 0.14) / 0.36) if t < 0.5 else
                                        -34 * ((t - 0.5) / 0.38) ** 2 if t < 0.88 else -34 + 3 * math.exp(-(t - 0.88) * 8) * math.sin((t - 0.88) * 30)), d)
    key(a, "than.scale", (0, (1, 1)), (0.88, (1, 1)), (0.93, (0.9, 1.06), "easeOut"), (1.1, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "dau.rotate", (0, 0), (0.1, 16), (0.3, -8), (0.45, 6), (0.6, -18), (0.88, -30, "easeIn"), (0.95, -24), (d, -26))
    key(a, "mo_duoi.rotate", (0, 0), (0.1, -18), (0.4, -10), (0.9, -20), (d, -20))
    key(a, "canh_gan.rotate", (0, 0), (0.07, -30), (0.4, -6, "easeOut"), (0.88, 30, "easeIn"), (0.95, 24), (d, 26))
    key(a, "canh_xa.rotate", (0, 0), (0.07, -24), (0.4, -4), (0.88, 24, "easeIn"), (d, 20))
    key(a, "chan_p.rotate", (0, 0), (0.5, 0), (0.9, 40, "easeIn"), (1.0, 34), (d, 36))
    key(a, "ban_p.rotate", (0, 0), (0.5, 0), (0.9, -20, "easeIn"), (d, -18))
    key(a, "chan_t.rotate", (0, 0), (0.5, 0), (0.9, -34, "easeIn"), (1.0, -28), (d, -30))
    follow(a, [(0, 0), (0.07, 10), (0.3, -3), (0.5, 0), (0.88, -34), (d, -34)], d, k=0.5, lag=0.1)
    flames(a, d, period=0.35)
    for sl in SLOTS:
        key(a, f"{sl}.alpha", (0, 1), (1.05, 1), (d, 0))


def appear():
    a, d = "appear", 0.8
    ops(f"anim.add {a} dur={d}")
    for s in SLOTS:
        key(a, f"{s}.alpha", (0, 0), (0.04, 1))
    key(a, "move.translate", (0, (0, 260)), (0.32, (0, 0), "easeIn"), (d, (0, 0)))
    key(a, "than.scale", (0, (1.05, 0.96)), (0.32, (1.05, 0.96)), (0.36, (0.86, 1.1)), (0.47, (1.04, 0.97), "easeOut"),
        (0.6, (1, 1), "easeInOut"), (d, (1, 1)))
    key(a, "hip.translate", (0, (0, 0)), (0.32, (0, 0)), (0.36, (0, -12)), (0.5, (0, 2), "easeOut"), (0.62, (0, 0)), (d, (0, 0)))
    # rơi: vỗ cánh nhanh, chân duỗi; đáp: nén, rồi ưỡn ngực gáy (ngẩng đầu, há mỏ, dang cánh)
    key(a, "canh_gan.rotate", (0, -40), (0.08, 20), (0.16, -40), (0.24, 20), (0.32, -36), (0.4, 10, "easeOut"), (0.52, -22),
        (0.7, -18), (d, 0, "easeInOut"))
    key(a, "canh_xa.rotate", (0, -30), (0.08, 16), (0.16, -30), (0.24, 16), (0.32, -28), (0.4, 8, "easeOut"), (0.52, -18),
        (0.7, -14), (d, 0, "easeInOut"))
    key(a, "chan_p.rotate", (0, 10), (0.32, 10), (0.36, -6), (0.5, 0, "easeOut"), (d, 0))
    key(a, "chan_t.rotate", (0, -10), (0.32, -10), (0.36, 6), (0.5, 0, "easeOut"), (d, 0))
    key(a, "than.rotate", (0, 0), (0.32, 0), (0.36, -6), (0.52, 8, "easeOut"), (0.7, 7), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, -6), (0.32, -6), (0.38, -10), (0.52, 18, "easeOut"), (0.7, 16), (d, 0, "easeInOut"))
    key(a, "mo_duoi.rotate", (0, 0), (0.48, 0), (0.54, -22), (0.7, -20), (0.78, 0, "easeIn"), (d, 0))
    follow(a, [(0, 0), (0.32, 0), (0.36, -6), (0.52, 8), (0.7, 7), (d, 0)], d)
    flames(a, d, period=0.4)
    ops(f"vfx.burst {a} image=bui prefix={a}_b bone=root count=6 t=0.32 dur=0.45 speed=320 spread=150 gravity=420 fade=0.4 "
        f"scale=1.8 scaleEnd=0.9 seed=5",
        f"vfx.ring {a} image=vong slot={a}_vong bone=dat_vong t=0.32 dur=0.4 from=0.4 to=2.6 fade=0.3")


def main():
    ops("# clip + hiệu ứng gà chọi lửa (quái lính đảo Hỏa) — sinh bởi ArtGen/Spine/quai_hoa_anim.py")
    vfx_art()
    idle()
    walk()
    pa = attack()
    cast()
    p1, p2 = skill()
    hit()
    die()
    appear()
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{len(L)} dòng -> {OUT}; mũi vuốt (thế giới, y lên): attack {pa[0]:.0f},{pa[1]:.0f}; skill {p1[0]:.0f},{p1[1]:.0f} / {p2[0]:.0f},{p2[1]:.0f}")


if __name__ == "__main__":
    main()
