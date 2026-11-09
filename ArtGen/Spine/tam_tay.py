# -*- coding: utf-8 -*-
"""Tám Tay vẽ lại thành tướng .atomik (2026-11-08): bạch tuộc chiến binh, pháo thủ bong bóng, 2 dạng. Hình là concept trọn con
LIỀN một ảnh (build_tam_tay.py, Codex), rig thẳng từ ảnh bằng bộ dựng một ảnh của Thủy Long (thuy_long_lien.py: vùng loang
từ hạt giống kẻ tay, nét mực là tường; ít lớp; lớp dưới vẽ bù phần bị che). Tên xương như Thủy Long nên dùng lại thở, trúng
đòn, tiến hóa; clip đánh, chiêu mana, chiêu cuối viết riêng cho pháo (đứng bắn, giật lùi, không lao).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tam_tay.py nhan <k> | rig <k> | all | show <k> <clip> t1,t2
Chân = hai xúc tu đứng (đầu xúc tu cuộn là bàn chân, IK), tay = hai xúc tu (đầu cuộn của tay sau như nắm tay), đuôi = hai
xúc tu ngắn sau lưng (một chuỗi lò xo), đầu = túi đầu (mantle) có mặt.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import longrig as L  # noqa: E402
import thuy_long as T  # noqa: E402
import thuy_long_lien as Q  # noqa: E402
from longrig import curve  # noqa: E402

H = T.H


def code(k):
    return f"tam_tay_{k}"


def base(k):
    return os.path.join(HERE, "inbox", code(k))


# ---------------------------------------------------------------- clip (pháo)
def idle(ctx):
    """đứng thủ pháo: thở, xúc tu tay sau cuộn mở, nòng pháo nhích; xúc tu sau lưng lượn nhờ lò xo."""
    D = 2.4

    def f(t, P):
        T.breathe(P, t, D)
        u = 2 * math.pi * t / D
        P.rot("fist_b", 6.0 * math.sin(2 * u))
        P.rot("arm_b2", 3.0 * math.sin(u + 0.6))
        P.rot("tail1", 5.0 * math.sin(u))
        P.rot("tail2", 6.0 * math.sin(u - 0.8))
        P.rot("hand_f", 1.5 * math.sin(2 * u))
        T.plant(P, ctx)
    return {"dur": D, "loop": True, "fn": f}


def muzzle_fx(P, t, c, h, big=1.0):
    """phát bắn: bong bóng nổ ở miệng nòng, tia nước phụt tới."""
    T.fx_on(P, "fx_tip", t, h - 0.03, h + 0.16, fade=0.12, amax=0.95)
    P.scale("fx_tip", c([(0, 0.35), (h - 0.03, 0.35 * big), (h + 0.12, 0.85 * big, "o"), (h + 1, 0.85 * big)]))
    T.fx_on(P, "fx_jet", t, h - 0.02, h + 0.24, fade=0.14)
    P.scale("fx_jet", c([(0, 0.3), (h - 0.02, 0.3), (h + 0.1, 1.05 * big, "o"), (h + 1, 1.1 * big)]),
            c([(0, 0.6), (h + 0.1, 0.9 * big, "o"), (h + 1, 0.9 * big)]))


def attack(ctx):
    """bắn pháo: hạ thấp người, chĩa nòng, bắn (giật lùi cả người, nòng hất lên), bong bóng nổ ở đầu nòng, tia nước tới; về."""
    D, h = 0.9, 0.38
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        kick = c([(0, 0), (h - 0.02, 0), (h + 0.05, 1, "o"), (h + 0.3, 0.25), (D, 0)])
        mx = c([(0, 0), (0.2, 6), (h, 8), (h + 0.06, -16, "o"), (0.7, -6), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.22, -12), (h, -12), (h + 0.06, -6, "o"), (0.7, -4), (D, 0)]))
        T.bend(P, c([(0, 0), (0.22, -5), (h, -6), (h + 0.06, 9, "o"), (0.66, 3), (D, 0)]))
        P.rot("head", c([(0, 0), (0.22, -3), (h, -4), (h + 0.06, 5, "o"), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.22, 12), (h, 14), (D, 0)]) + 10 * kick)
        P.rot("arm_f2", c([(0, 0), (0.22, -10), (h, -12), (D, 0)]) + 8 * kick)
        T.aim(P, ctx.R, c([(0, W0), (0.22, 3), (h, 1), (D, W0)]) + 5 * kick)  # nòng ngang: tia nước bay thẳng tới
        P.rot("arm_b1", c([(0, 0), (0.22, -10), (h + 0.06, 14, "o"), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.22, -14), (h + 0.06, 10, "o"), (D, 0)]))
        T.plant(P, ctx, fb=(mx * 0.6, 0), ff=(mx * 0.85, 0))
        muzzle_fx(P, t, c, h)
    return {"dur": D, "fn": f, "hit": h}


def cast(ctx):
    """chiêu mana: nâng nòng chếch lên, bong bóng tụ ở miệng nòng (xoáy, lấp lánh), hạ nòng ngang rồi bắn tia; trận bắn tia
    từ miệng nòng ở khung trúng."""
    D, h = 1.0, 0.56
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        kick = c([(0, 0), (h - 0.02, 0), (h + 0.05, 1, "o"), (h + 0.3, 0.2), (D, 0)])
        P.move("hip", 0, c([(0, 0), (0.3, -6), (h, -8), (h + 0.06, -3, "o"), (D, 0)]))
        T.bend(P, c([(0, 0), (0.3, 6), (h - 0.05, 7), (h + 0.06, 10, "o"), (0.8, 2), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.3, 36), (h - 0.05, 40), (h, 16, "o"), (D, 0)]) + 8 * kick)
        P.rot("arm_f2", c([(0, 0), (0.3, 10), (h, -8, "o"), (D, 0)]) + 6 * kick)
        T.aim(P, ctx.R, c([(0, W0), (0.3, 42), (h - 0.05, 45), (h, 2, "o"), (D, W0)]) + 5 * kick)
        P.rot("arm_b1", c([(0, 0), (0.3, 16), (h, -14, "o"), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.3, -22), (h, -16), (D, 0)]))
        P.rot("head", c([(0, 0), (0.3, 6), (h, -4, "o"), (D, 0)]))
        T.plant(P, ctx)
        T.fx_on(P, "fx_spark", t, 0.18, h + 0.04, rise=0.1, fade=0.1)
        P.scale("fx_spark", c([(0, 0.4), (0.4, 1.1, "o"), (h, 0.7)]))
        P.rot("fx_spark", c([(0, 0), (D, 140, "l")]))
        T.fx_on(P, "fx_tip", t, 0.12, h + 0.12, rise=0.18, fade=0.1, amax=0.95)
        P.scale("fx_tip", c([(0, 0.3), (0.12, 0.35), (h - 0.02, 1.2), (h + 0.1, 1.7, "o"), (D, 1.7)]))
        P.rot("fx_tip", c([(0, 0), (D, -220, "l")]))
    return {"dur": D, "fn": f, "hit": h}


def skill(ctx):
    """chiêu cuối: xúc tu bám chặt đất, nước xoáy quanh người, nòng chếch lên bắn liên tiếp 3 phát (mỗi phát giật lùi), phát
    cuối là quả bong bóng lớn nổ trước đối thủ: cột nước, vòng sóng, sóng thần."""
    D, h = 1.7, 1.02
    W0 = ctx.R.weapon_ang
    shots = (0.5, 0.74, h)

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        kick = sum(c([(0, 0), (s - 0.02, 0), (s + 0.04, 1 if s == h else 0.6, "o"), (s + 0.2, 0), (D, 0)]) for s in shots)
        mx = c([(0, 0), (0.4, 4), (h, 0), (D, 0)]) - 10 * kick
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.36, -16), (h + 0.2, -14), (D, 0)]) + 4 * kick)
        T.bend(P, c([(0, 0), (0.36, -4), (h + 0.2, -5), (D, 0)]) + 6 * kick)
        P.rot("head", c([(0, 0), (0.36, -4), (h + 0.1, 4, "o"), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.36, 26), (h + 0.2, 24), (D, 0)]) + 8 * kick)
        P.rot("arm_f2", c([(0, 0), (0.36, -6), (D, 0)]) + 6 * kick)
        T.aim(P, ctx.R, c([(0, W0), (0.36, 6), (0.74, 5), (h, 3), (h + 0.25, 4), (D, W0)]) + 5 * kick)
        P.rot("arm_b1", c([(0, 0), (0.36, -24), (h + 0.2, -20), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.36, -30), (h + 0.2, -24), (D, 0)]))
        P.rot("fist_b", c([(0, 0), (0.36, 20), (h + 0.2, 16), (D, 0)]))
        T.plant(P, ctx, fb=(mx * 0.5, 0), ff=(mx * 0.7, 0))
        T.skill_fx_charge(P, t, c, t_end=0.6)
        for i, s in enumerate(shots):
            big = 1.35 if s == h else 0.8
            if s - 0.03 <= t < s + 0.24 or (i == len(shots) - 1 and t >= s - 0.03):
                muzzle_fx(P, t, c, s, big)
        T.skill_fx_impact(P, t, c, h + 0.08, at=0.62 * H)
    return {"dur": D, "fn": f, "hit": h}


def hit(ctx):
    """trúng đòn như Thủy Long, nhưng nòng pháo chỉ hất nhẹ (không dựng đứng lên trời)."""
    base_ = T.hit(ctx)
    W0 = ctx.R.weapon_ang

    def f(t, P):
        base_["fn"](t, P)
        b = curve(t, [(0, 0), (0.07, 1, "o"), (0.22, 0.6), (base_["dur"], 0)])
        T.aim(P, ctx.R, W0 + 10 * b)
    return dict(base_, fn=f)


def clips_of(ctx):
    return {"idle": idle(ctx), "hit": hit(ctx), "attack": attack(ctx), "cast": cast(ctx), "skill": skill(ctx)}


# ---------------------------------------------------------------- cấu hình bộ dựng một ảnh
# hai xúc tu sau lưng: "cape" (xúc tu trên) và "tail" (xúc tu dưới), mỗi cái một chuỗi lò xo gắn ngực
LAYERS = {k: [("cape", ["cape"], 22), ("tail", ["tail"], 22), ("arm_b", ["arm_b", "fist_b"], 34),
              ("leg_b", ["leg_b", "foot_b"], 30), ("leg_f", ["leg_f", "foot_f"], 30), ("body", ["torso"], 44),
              ("head", ["head"], 0),  # râu xúc tu buông trước ngực: đầu là lớp riêng trên thân, lắc đầu không xé ngực
              ("arm_f", ["arm_f", "shoulder", "weapon", "hand_f"], 0)] for k in (1, 2)}
JD = {1: {"top": 95.0,  # đỉnh mũ nồi
          "bones": {"hip": (480, 950), "spine1": (480, 950), "spine2": (485, 820), "chest": (495, 690), "neck": (505, 560),
                    "head": (520, 440), "arm_b1": (320, 610), "arm_b2": (160, 730), "fist_b": (130, 862),
                    "arm_f1": (570, 790), "arm_f2": (680, 815), "hand_f": (752, 805), "weapon": (790, 800),
                    "leg_b1": (430, 975), "leg_b2": (250, 1140), "foot_b": (205, 1300),
                    "leg_f1": (530, 975), "leg_f2": (650, 1150), "foot_f": (705, 1300),
                    "tail1": (205, 640), "tail2": (155, 612), "tail3": (100, 595), "tail4": (62, 620),
                    "cape1": (250, 540), "cape2": (205, 490), "cape3": (155, 462), "cape4": (118, 482)},
          "tips": {"tail": (92, 662), "cape": (122, 520)},
          "tip": (970, 578), "axis": ((735, 690), (970, 578))},
      2: {"top": 45.0,  # đỉnh mũ trụ
          "bones": {"hip": (470, 1000), "spine1": (470, 1000), "spine2": (480, 860), "chest": (490, 710), "neck": (500, 570),
                    "head": (512, 455), "arm_b1": (355, 595), "arm_b2": (150, 700), "fist_b": (75, 862),
                    "arm_f1": (600, 650), "arm_f2": (700, 780), "hand_f": (775, 830), "weapon": (815, 815),
                    "leg_b1": (340, 1010), "leg_b2": (205, 1180), "foot_b": (190, 1335),
                    "leg_f1": (580, 1010), "leg_f2": (700, 1160), "foot_f": (722, 1325),
                    "tail1": (290, 600), "tail2": (200, 580), "tail3": (110, 556), "tail4": (52, 580),
                    "cape1": (320, 525), "cape2": (250, 488), "cape3": (170, 428), "cape4": (115, 440)},
          "tips": {"tail": (48, 612), "cape": (95, 468)},
          "tip": (960, 590), "axis": ((800, 640), (960, 590))}}
MARKD = {1: {  # hạt giống (toạ độ tam_tay_1/tai_ve/L1_lien.png)
    "cape": [("line", [(272, 562), (235, 525), (200, 485), (150, 462), (118, 485)], 12)],
    "tail": [("line", [(196, 634), (185, 628), (140, 605), (95, 598), (65, 625)], 12)],
    "arm_b": [("line", [(330, 600), (250, 620), (170, 690), (125, 780), (130, 850)], 18)],
    "fist_b": [("line", [(180, 900), (232, 910)], 26)],
    "leg_b": [("line", [(410, 970), (320, 1060), (240, 1150), (215, 1280)], 26)],
    "foot_b": [("line", [(200, 1322), (140, 1352), (110, 1332)], 14)],
    "leg_f": [("line", [(530, 980), (620, 1080), (660, 1200), (690, 1290)], 26)],
    "foot_f": [("line", [(722, 1340), (800, 1352), (830, 1322)], 14)],
    "torso": [("poly", [(430, 560), (560, 560), (560, 980), (450, 980)]), ("line", [(330, 850), (450, 760), (580, 600)], 20),
              ("line", [(360, 840), (440, 780), (520, 720)], 14)],
    "head": [("poly", [(260, 200), (400, 170), (480, 250), (620, 300), (640, 380), (560, 420), (420, 420), (280, 380)]),
             ("poly", [(380, 110), (560, 100), (690, 180), (690, 260), (560, 250), (420, 200)]),
             ("line", [(420, 420), (430, 520), (450, 600)], 12), ("line", [(560, 420), (600, 500), (640, 520)], 10),
             ("line", [(500, 420), (520, 560)], 10)],
    "arm_f": [("line", [(585, 792), (650, 810), (720, 810)], 18)],
    "weapon": [("poly", [(650, 560), (760, 500), (850, 560), (990, 470), (1000, 640), (860, 640), (840, 720), (760, 860),
                         (720, 880), (660, 760)])],
    "hand_f": [("line", [(772, 780), (832, 792)], 26)],
}, 2: {  # tay trước khuất sau pháo, chỉ lộ đầu xúc tu quấn tay cầm
    "cape": [("line", [(320, 525), (250, 490), (170, 425), (115, 440)], 12)],
    "tail": [("line", [(290, 600), (200, 580), (110, 555), (55, 580)], 12)],
    "arm_b": [("line", [(350, 600), (250, 640), (150, 690), (90, 770), (70, 850)], 18)],
    "fist_b": [("line", [(130, 920), (185, 930)], 26)],
    "leg_b": [("line", [(330, 1010), (250, 1100), (200, 1200), (190, 1320)], 28)],
    "foot_b": [("line", [(180, 1360), (120, 1400), (80, 1380)], 16)],
    "leg_f": [("line", [(580, 1010), (660, 1100), (700, 1200), (720, 1310)], 28)],
    "foot_f": [("line", [(730, 1370), (810, 1390), (850, 1360)], 16)],
    "torso": [("poly", [(460, 520), (560, 520), (580, 1000), (450, 1000)]), ("line", [(310, 790), (620, 790)], 18),
              ("line", [(340, 890), (560, 890)], 26)],
    "head": [("poly", [(360, 230), (640, 200), (680, 330), (640, 420), (400, 420), (350, 330)]),
             ("line", [(320, 180), (450, 120), (600, 150), (670, 260)], 14),
             ("line", [(300, 70), (200, 90), (160, 180), (200, 250)], 16),
             ("poly", [(190, 240), (300, 220), (310, 350), (210, 360)]),
             ("line", [(420, 430), (400, 520), (380, 580)], 12), ("line", [(500, 430), (500, 560)], 12),
             ("line", [(600, 430), (640, 520), (680, 560)], 12)],
    "weapon": [("poly", [(560, 540), (700, 500), (780, 560), (990, 490), (1005, 690), (800, 720), (800, 780), (740, 860),
                         (640, 870), (560, 800)])],
    "hand_f": [("line", [(800, 800), (850, 830)], 26)],
}}
OVERRIDE = {1: {"head": [[(600, 465), (665, 465), (665, 545), (600, 545)]]},  # đầu xúc tu râu bên phải (sát súng)
            2: {}}
CLAMP = {1: {}, 2: {}}


def setup():
    Q.CFG.update({"code": code, "base": base, "clips": clips_of, "evolve": lambda *a: T.evolve(*a),
                  "beam": {1: 0.85, 2: 1.1}, "src": lambda k: os.path.join(base(k), "tai_ve", "L1_lien.png"),
                  "game": {"lunge": []}})
    Q.LAYERS.clear()
    Q.LAYERS.update(LAYERS)
    Q.JD.clear()
    Q.JD.update(JD)
    Q.MARKD.clear()
    Q.MARKD.update(MARKD)
    Q.OVERRIDE.clear()
    Q.OVERRIDE.update(OVERRIDE)
    Q.CLAMP.clear()
    Q.CLAMP.update(CLAMP)
    Q.LINEAR_Y.clear()
    Q.FULL_SHEET.clear()
    Q.WARM_FIX.clear()
    Q.PARENT["tail1"] = "chest"  # xúc tu sau lưng gắn ngực
    Q.CHAINS["tail"] = (["tail1", "tail2", "tail3", "tail4"], "chest", 0.1, 0.12)
    Q.CHAINS["cape"] = (["cape1", "cape2", "cape3", "cape4"], "chest", 0.1, 0.12)


def main(argv):
    setup()
    step = argv[0]
    if step == "all":
        n2 = Q.build_form(2)
        Q.build_form(1, n2)
    else:
        Q.main(argv)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
