# -*- coding: utf-8 -*-
"""Quái đảo Thổ (dê đá húc): sinh lệnh AtomSpine cho clip + hiệu ứng -> quai_tho/atom/anim.ops.

    py -3 -I ArtGen/Spine/quai_tho_anim.py      # rồi: atom do -f anim.ops -p ArtGen/Spine/quai_tho/atom

Con NẶNG (skill animation-petclash): lấy đà dài, ít nảy, đất rung khi dậm. idle 2 s lặp (thở nặng, hông – ngực lệch pha, điểm
phá nhịp 1,25–1,7 s: hất đầu khịt mũi + cào móng trước), walk 2 s (2 chu kỳ, chân chéo cặp, móng bám đất bằng IK), attack 1,0 s
(lùi ngửa đầu lấy đà 0,32 s, giữ 4 khung, húc 0,5, khựng, về), cast 1,0 s (chồm hai chân trước, dậm 0,55: đá bật + vòng sóng
đất + rung), skill 1,8 s (cào móng hai lần, lấy đà, húc 1,0 và 1,25), hit 0,6 s (bật 0,07), die 1,4 s (giật, lả, khuỵu chân
gục, mờ 1,05–1,4), appear 0,8 s (rơi uỵch 0,32, nén, vòng bụi; khung đầu trống). Góc cộng vào dáng gốc (độ, CCW: dương = ngửa
đầu); dời cộng (px, y lên). Móng: đích IK `ik_*` dưới `move`.
"""
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "quai_tho", "atom", "anim.ops")
SLOTS = ["bom", "sung_xa", "chan_xa_sau", "chan_xa_truoc", "da1", "da2", "da3", "duoi", "chan_gan_sau", "chan_gan_truoc", "than",
         "tai_xa", "dau", "sung_gan"]
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


def sstep(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def soft(anim, dur, amp=1.0, period=None):
    """phụ kiện lệch pha (lặp liền): đuôi vẫy, tai, ba tấm đá lưng rung trễ dần"""
    p = period or dur
    ops(f"anim.wave {anim} bones=duoi prop=rotate amp={6 * amp:.1f} period={p / 2:.3f} phase=0.2",
        f"anim.wave {anim} bones=tai_x prop=rotate amp={4 * amp:.1f} period={p:.3f} phase=0.35",
        f"anim.wave {anim} bones=da1 prop=rotate amp={1.5 * amp:.1f} period={p:.3f} phase=0.25",
        f"anim.wave {anim} bones=da2 prop=rotate amp={1.5 * amp:.1f} period={p:.3f} phase=0.18",
        f"anim.wave {anim} bones=da3 prop=rotate amp={1.5 * amp:.1f} period={p:.3f} phase=0.1")


FLOP = {"da1": (2.0, 0.03), "da2": (2.5, 0.02), "da3": (3.0, 0.01), "tai_x": (6.0, 0.02), "duoi": (4.0, 0.04)}


def springs(anim, pat, end):
    """phụ kiện trễ theo thân bằng khoá tay (lò xo nướng bị bật 40–60° ở khung snap): pat = [(t, hệ số)], mỗi phụ kiện
    nhân biên độ riêng và trễ riêng; hệ số dương = ngả về sau (lúc lấy đà), âm = hất tới (lúc trúng)"""
    for b, (amp, dl) in FLOP.items():
        ks = [(0, pat[0][1] * amp if pat[0][0] == 0 else 0)]
        for t, v in pat:
            if t == 0:
                continue
            tt = min(end, t + dl) if t < end else end
            ks.append((tt, v * amp, "easeOut"))
        if ks[-1][0] < end:
            ks.append((end, 0, "easeInOut"))
        key(anim, f"{b}.rotate", *ks)


def vfx_art():
    ops("vfx.art da kind=shard palette=earth size=96 seed=3",
        "vfx.art bui kind=puff palette=earth size=150 seed=5",
        "vfx.art khoi kind=smoke palette=earth size=170 seed=8",
        "vfx.art vong kind=shockwave palette=earth size=280 seed=2",
        "vfx.art cham kind=impact palette=earth size=240 seed=4")


def butt_fx(anim, t, big=False, tag="", end=9.0):
    """trúng húc ở trán: chớp va chạm + vòng sóng + bụi + đá vụn văng (vẽ trên cùng); hạt tắt trước cuối clip"""
    s = 1.3 if big else 1.0
    lim = end - t - 0.03
    ops(f"vfx.ring {anim} image=cham slot={anim}_cham{tag} bone=vong_dau t={t:.3f} dur={0.22 * s:.3f} from=0.3 to={0.95 * s:.2f} fade=0.15",
        f"vfx.ring {anim} image=vong slot={anim}_vong{tag} bone=vong_dau t={t + 0.02:.3f} dur={min(0.42 * s, lim - 0.02):.3f} from=0.15 to={1.4 * s:.2f} fade=0.3")
    if big or not tag:
        ops(f"vfx.burst {anim} image=bui prefix={anim}_b{tag} bone=mui count={3 if big else 2} t={t + 0.01:.3f} dur={min(0.55, lim - 0.01):.3f} "
            f"speed=150 spread=200 gravity=-40 fade=0.5 scale=0.7 scaleEnd=1.1 seed=11")
    ops(f"vfx.burst {anim} image=da prefix={anim}_d{tag} bone=mui count={8 if big else 6} t={t:.3f} dur={min(0.5 * s, lim):.3f} "
        f"speed={480 * s:.0f} spread=150 gravity=1300 spin=420 fade=0.35 scale=1.0 scaleEnd=0.7 seed={7 + len(tag)}")


# ---------------------------------------------------------------- clip
def idle():
    a, d = "idle", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    # thở nặng: hông lún – ngực trễ pha; điểm phá nhịp 1,25–1,7: hất đầu khịt mũi + cào móng trước gần
    dense(a, "hip.translate", lambda t: (0.0, -3.0 * (0.5 - 0.5 * math.cos(2 * math.pi * t / d))), d)
    dense(a, "nguc.rotate", lambda t: 1.2 * tw(t, d, 0.15) + bump(t, 1.25, 0.08, 0.1, 0.2, 2.5), d)
    dense(a, "dau.rotate", lambda t: 1.5 * tw(t, d, 0.3) + bump(t, 1.25, 0.07, 0.06, 0.25, 11) - bump(t, 1.58, 0.06, 0.02, 0.1, 3), d)
    dense(a, "ik_gt.translate", lambda t: (-16 * bump(t, 1.3, 0.12, 0.0, 0.12, 1.0) * (1 if t > 1.42 else 0.3),
                                           12 * bump(t, 1.3, 0.1, 0.04, 0.12, 1.0)), d)
    dense(a, "tai_x.rotate", lambda t: 4 * tw(t, d, 0.35) + bump(t, 1.28, 0.05, 0.05, 0.15, 14), d)
    ops(f"anim.wave {a} bones=duoi prop=rotate amp=6 period=1 phase=0.2",
        f"anim.wave {a} bones=da1 prop=rotate amp=1.5 period=2 phase=0.25",
        f"anim.wave {a} bones=da2 prop=rotate amp=1.5 period=2 phase=0.18",
        f"anim.wave {a} bones=da3 prop=rotate amp=1.5 period=2 phase=0.1")
    ops(f"anim.loopfix {a}", f"anim.reduce {a} tol=0.15")


def foot(p, stride, lift, duty=0.6):
    """quỹ đạo móng trong một chu kỳ (p 0..1): chạm đất trượt lùi, nhấc lên bước tới"""
    p %= 1.0
    if p < duty:
        return (stride / 2 - stride * p / duty, 0.0)
    u = (p - duty) / (1 - duty)
    return (-stride / 2 + stride * sstep(u), lift * math.sin(math.pi * u))


def walk():
    a, d = "walk", 2.0
    ops(f"anim.add {a} dur={d} loop=true")
    per = 1.0
    for ik, ph in (("ik_gs", 0.0), ("ik_xt", 0.0), ("ik_xs", 0.5), ("ik_gt", 0.5)):
        dense(a, f"{ik}.translate", lambda t, ph=ph: foot(t / per + ph, 34, 14), d)
    # thân nặng: lún mỗi lần đổi cặp chân, ngực lệch pha hông, đầu gật theo bước
    dense(a, "hip.translate", lambda t: (1.5 * tw(t, per / 2, 0.1), -3.0 * (0.5 - 0.5 * math.cos(4 * math.pi * t / per))), d)
    dense(a, "nguc.rotate", lambda t: 1.5 * tw(t, per / 2, 0.3), d)
    dense(a, "dau.rotate", lambda t: 2.0 * tw(t, per / 2, 0.45), d)
    soft(a, d, amp=1.3, period=per)
    ops(f"anim.loopfix {a}", f"anim.reduce {a} tol=0.15")


def attack():
    a, d, th = "attack", 1.0, 0.5
    ops(f"anim.add {a} dur={d}")
    # lấy đà dài 0–0,32 (lùi, ngửa đầu, ngực nhổm), giữ 4 khung run nhẹ, húc 0,42 -> 0,5 (snap), khựng, về
    key(a, "hip.translate", (0, (0, 0)), (0.32, (-24, 3), "easeOut"), (0.42, (-25, 3), "snap"), (th, (30, -6)), (0.64, (27, -6)),
        (d, (0, 0), "easeInOut"))
    key(a, "nguc.rotate", (0, 0), (0.32, 5, "easeOut"), (0.42, 6, "snap"), (th, -5), (0.64, -4), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.34, 15, "easeOut"), (0.42, 16, "snap"), (th, -16), (0.56, -18), (0.66, -13), (d, 0, "easeInOut"))
    key(a, "dau.scale", (0, (1, 1)), (0.42, (1, 1)), (th, (1.07, 0.95)), (0.58, (1, 1), "easeOut"), (d, (1, 1)))
    springs(a, [(0.32, 1.0), (0.42, 1.0), (0.5, -2.2), (0.58, 1.0), (0.7, -0.4), (1.0, 0)], d)
    ops(f"event {a} {th} hit")
    butt_fx(a, th, end=d)
    ops(f"vfx.shake {a} bone=move t={th} dur=0.18 amp=5")


def cast():
    a, d, th = "cast", 1.0, 0.55
    ops(f"anim.add {a} dur={d}")
    # chồm: thân ngả về sau quanh hông, hai móng trước nhấc cao; giữ đỉnh 0,40–0,48; dậm xuống 0,55 (snap), nén, rung, về
    key(a, "hip.rotate", (0, 0), (0.4, 15, "easeOut"), (0.48, 16, "snap"), (th, -3), (0.62, -1.5), (d, 0, "easeInOut"))
    key(a, "hip.translate", (0, (0, 0)), (0.4, (-8, 6), "easeOut"), (0.48, (-8, 7), "snap"), (th, (6, -8)), (0.64, (4, -5)),
        (d, (0, 0), "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.4, 10, "easeOut"), (0.48, 12, "snap"), (th, -12), (0.66, -8), (d, 0, "easeInOut"))
    for ik, dx in (("ik_gt", -6), ("ik_xt", -4)):
        key(a, f"{ik}.translate", (0, (0, 0)), (0.4, (dx, 80), "easeOut"), (0.48, (dx, 86), "snap"), (th, (0, 0)), (d, (0, 0)))
    springs(a, [(0.4, -1.2), (0.48, -1.3), (0.55, 2.6), (0.63, -1.2), (0.75, 0.5), (1.0, 0)], d)
    ops(f"event {a} {th} phun")
    # vòng sóng đất + khói trước, đá bật lên sau cùng (vẽ trên khói); rung sân
    ops(f"vfx.ring {a} image=vong slot={a}_vong bone=dat_truoc t={th:.3f} dur=0.42 from=0.2 to=1.8 fade=0.3",
        f"vfx.burst {a} image=khoi prefix={a}_k bone=dat_truoc count=3 t={th + 0.02:.3f} dur=0.4 speed=120 spread=160 "
        f"gravity=-60 fade=0.55 scale=0.7 scaleEnd=1.2 seed=6",
        f"vfx.burst {a} image=da prefix={a}_d bone=dat_truoc count=8 t={th:.3f} dur=0.42 speed=640 spread=110 gravity=1500 "
        f"spin=420 fade=0.35 scale=1.2 scaleEnd=0.8 seed=4",
        f"vfx.shake {a} bone=move t={th} dur=0.25 amp=8")


def skill():
    a, d, t1, t2 = "skill", 1.8, 1.0, 1.25
    ops(f"anim.add {a} dur={d}")

    def tremble(t):
        return (2.0 if int(t * 30) % 2 else -2.0) if 0.74 <= t <= 0.9 else 0.0

    # cào móng hai lần (0,08–0,30 và 0,32–0,54), đầu cúi, thân lùi; lấy đà 0,6–0,9 (lùi sâu, ngửa đầu, run); húc 1,0; giật lùi
    # lấy đà nhanh 1,06–1,16; húc mạnh 1,25; khựng tới 1,42; về
    def hx(t):
        pts = [(0, 0), (0.55, -10), (0.74, -28), (0.9, -29), (t1, 34), (1.08, 26), (1.16, 18), (t2, 44), (1.42, 41), (d, 0)]
        for (a0, v0), (a1, v1) in zip(pts, pts[1:]):
            if a0 <= t <= a1:
                u = (t - a0) / (a1 - a0)
                if a0 in (0, 0.55, 1.42, 1.0):
                    u = sstep(u)
                return v0 + (v1 - v0) * u
        return 0.0

    def hy(t):
        return -6 if (t1 <= t < 1.1 or t2 <= t < 1.45) else (4 if 0.74 <= t <= 0.9 else 0)

    dense(a, "hip.translate", lambda t: (hx(t), hy(t)), d)
    key(a, "dau.rotate", (0, 0), (0.1, -8, "easeOut"), (0.55, -8), (0.76, 16, "easeOut"), (0.9, 17, "snap"), (t1, -17),
        (1.08, -6), (1.16, 10, "snap"), (t2, -19), (1.32, -20), (1.42, -16), (d, 0, "easeInOut"))
    dense(a, "nguc.rotate", lambda t: (6 * sstep((t - 0.55) / 0.2) if t < 0.9 else -6 if t < 1.16 else -7 if t < 1.42 else
                                       -7 * (1 - sstep((t - 1.42) / 0.38))) + tremble(t), d)
    key(a, "dau.scale", (0, (1, 1)), (0.9, (1, 1)), (t1, (1.07, 0.95)), (1.08, (1, 1), "easeOut"), (1.16, (1, 1)),
        (t2, (1.1, 0.93)), (1.34, (1, 1), "easeOut"), (d, (1, 1)))
    # cào móng trước gần: nhấc, cào lùi trên đất
    def paw(t):
        for s in (0.08, 0.32):
            if s <= t <= s + 0.22:
                u = (t - s) / 0.22
                return (14 - 34 * sstep(u), 12 * math.sin(math.pi * min(1, u * 1.6)) if u < 0.62 else 0)
        return (0.0, 0.0)
    dense(a, "ik_gt.translate", paw, 0.6)
    springs(a, [(0.74, 1.0), (0.9, 1.0), (1.0, -2.0), (1.08, 0.8), (1.16, 1.0), (1.25, -2.5), (1.33, 1.2), (1.45, -0.5), (1.8, 0)], d)
    ops(f"event {a} {t1} hit", f"event {a} {t2} hit")
    butt_fx(a, t1, tag="a", end=d)
    butt_fx(a, t2, big=True, tag="b", end=d)
    ops(f"vfx.shake {a} bone=move t={t1} dur=0.2 amp=6", f"vfx.shake {a} bone=move t={t2} dur=0.3 amp=10 seed=2")


def hit():
    a, d = "hit", 0.6
    ops(f"anim.add {a} dur={d}")
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-18, 4), "easeOut"), (0.25, (-10, 1)), (d, (0, 0), "easeInOut"))
    key(a, "nguc.rotate", (0, 0), (0.07, 6, "easeOut"), (0.3, 2), (d, 0, "easeInOut"))
    key(a, "dau.rotate", (0, 0), (0.09, 15, "easeOut"), (0.3, 4), (d, 0, "easeInOut"))
    springs(a, [(0.07, 2.0), (0.17, -1.0), (0.3, 0.4), (0.6, 0)], d)
    ops(f"vfx.shake {a} bone=nguc t=0.0 dur=0.18 amp=4 freq=30", f"anim.reduce {a} tol=0.4")


def die():
    a, d = "die", 1.4
    ops(f"anim.add {a} dur={d}")
    # giật 0,07 -> lả, đầu rũ lắc 0,1–0,5 -> khuỵu chân trước rồi sau, gục xuống đất 0,5–0,9 -> nén -> mờ 1,05–1,4
    key(a, "hip.translate", (0, (0, 0)), (0.07, (-14, 4), "easeOut"), (0.3, (-6, 0)), (0.5, (-4, -2)), (0.9, (6, -46), "easeIn"),
        (0.95, (6, -50)), (1.05, (6, -47), "easeOut"), (d, (6, -48)))
    key(a, "hip.rotate", (0, 0), (0.07, 3), (0.5, 0), (0.75, -9, "easeIn"), (0.92, -4, "easeIn"), (1.0, -5), (d, -5))
    dense(a, "dau.rotate", lambda t: (16 * math.sin(math.pi * min(t, 0.14) / 0.14) if t < 0.14 else
                                      -6 + 5 * math.sin(2 * math.pi * (t - 0.14) / 0.36) if t < 0.5 else
                                      -6 - 16 * sstep((t - 0.5) / 0.4) if t < 0.9 else
                                      -22 + 3 * math.exp(-(t - 0.9) * 8) * math.sin((t - 0.9) * 30)), d)
    key(a, "nguc.rotate", (0, 0), (0.5, 0), (0.78, -8, "easeIn"), (0.9, -6), (d, -6))
    # móng trượt ra khi khuỵu (chân gập theo IK)
    for ik, v in (("ik_gs", -14), ("ik_xs", -8), ("ik_gt", 16), ("ik_xt", 22)):
        key(a, f"{ik}.translate", (0, (0, 0)), (0.5, (0, 0)), (0.9, (v, 0), "easeIn"), (d, (v, 0)))
    springs(a, [(0.07, 1.5), (0.2, -0.6), (0.5, 0.3), (0.9, -1.8), (0.98, 1.0), (1.1, -0.4), (1.4, -0.4)], d)
    for sl in SLOTS:
        key(a, f"{sl}.alpha", (0, 1), (1.05, 1), (d, 0))


def appear():
    a, d = "appear", 0.8
    ops(f"anim.add {a} dur={d}")
    for s in SLOTS:
        key(a, f"{s}.alpha", (0, 0), (0.04, 1))
    key(a, "move.translate", (0, (0, 240)), (0.32, (0, 0), "easeIn"), (d, (0, 0)))
    # rơi: chân duỗi thõng; chạm đất 0,32: nén nặng (thân lún, chân gập IK), bật nhẹ, hất đầu "chào"
    key(a, "hip.translate", (0, (0, 6)), (0.32, (0, 6)), (0.37, (0, -14)), (0.5, (0, 2), "easeOut"), (0.62, (0, 0)), (d, (0, 0)))
    for ik, v in (("ik_gs", -10), ("ik_xs", -6), ("ik_gt", 6), ("ik_xt", 10)):
        key(a, f"{ik}.translate", (0, (v, -8)), (0.32, (0, 0), "easeIn"), (d, (0, 0)))
    key(a, "dau.rotate", (0, 8), (0.32, 8), (0.38, -10), (0.55, 10, "easeOut"), (0.66, -2), (d, 0, "easeInOut"))
    springs(a, [(0, 1.0), (0.32, 1.0), (0.37, -2.4), (0.47, 1.2), (0.6, -0.4), (0.8, 0)], d)
    ops(f"vfx.burst {a} image=bui prefix={a}_b bone=move count=6 t=0.32 dur=0.45 speed=220 spread=160 gravity=-30 fade=0.45 "
        f"scale=0.8 scaleEnd=1.2 seed=5",
        f"vfx.ring {a} image=vong slot={a}_vong bone=dat_vong t=0.32 dur=0.45 from=0.2 to=1.8 fade=0.3")


def main():
    ops("# clip + hiệu ứng dê đá húc (quái đảo Thổ) — sinh bởi ArtGen/Spine/quai_tho_anim.py")
    vfx_art()
    for f in (idle, walk, attack, cast, skill, hit, die, appear):
        f()
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{len(L)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
