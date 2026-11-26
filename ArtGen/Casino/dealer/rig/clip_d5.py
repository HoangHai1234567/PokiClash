# Clip D5 của Lão Mực (GD_Claude/31 mục 4.4, lều Hội Máy Quả): kéo cần máy quả.
# hoat_anh.py nạp file này (đăng ký vào CLIPS bằng @clip) nên chạy như mọi clip khác:
#   py -3 -I hoat_anh.py sl_pull
#
# Bố cục lều Máy Quả (ArtGen/Casino/may_qua/bo_cuc.json): sân khấu 1080 x 1920; Lão Mực đứng sau quầy bên phải, rig tỉ lệ 0,60, gốc
# rig ở sân khấu (350, 1437) nên mép quầy (rig y 500) rơi đúng y 1137; máy quả "Háu Ăn" (rig ArtGen/Casino/may_qua/atom) tỉ lệ 0,90,
# gốc ở (−160, 1452), đứng bên TRÁI Lão Mực (phía tay "t"). Điểm rig máy (x, y) -> rig Lão Mực:
#   X = (−160 + 0,9 x − 350) / 0,60 ;  Y = (1437 − (1452 − 0,9 y)) / 0,60.
# Núm cần của máy lúc nghỉ ở rig Lão Mực (−228, 1397) (bên trái, cao hơn đầu, không đè lên tóc), bị giật xuống tới (87, 617) (trước bụng).
# ĐƯỜNG ĐI CỦA NÚM lấy từ chính clip `pull` của máy (may_qua/atom/duong_num.json, 30 khung/giây, do may_qua/rig/hoat_anh.py ghi):
# hai clip dài bằng nhau phần đầu và game phát CÙNG MỘT KHUNG nên bàn tay nằm đúng trên núm suốt lúc giật (0,30 .. 0,57 s).
# Nướng lại clip `pull` của máy hoặc đổi bố cục thì nướng lại clip này.
import json
import math
import os
import sys

from dong_co import seg, hat, wob, ease, eout, lin, back, clamp, spec, arm_seq, spine

_H = sys.modules.get("hoat_anh") or sys.modules["__main__"]
clip, nhip, on_table, steps = _H.clip, _H.nhip, _H.on_table, _H.steps

HERE = os.path.dirname(os.path.abspath(__file__))
MQ = os.path.abspath(os.path.join(HERE, "..", "..", "may_qua"))
BC = json.load(open(os.path.join(MQ, "bo_cuc.json"), encoding="utf-8"))
NUM = json.load(open(os.path.join(MQ, "atom", "duong_num.json")))
FPS_N = NUM["fps"]
LEAD = NUM["lead"]                 # 0,30: núm bắt đầu bị giật ở LEAD + 0,07
HAND_OPEN, HAND_GRIP = 1, 10       # 10: nắm cần gạt (bàn tay chữ C, có lỗ giữa)
GRIP_HS = 1.4                      # cỡ bàn tay lúc nắm núm (núm to hơn bàn tay thường)
GRIP_D = 130.0                     # lòng nắm cách cổ tay (px ảnh tay_10) theo hướng bàn tay
SHOULDER = (-80.0, 894.0)          # khớp vai trái lúc nghỉ (thế giới rig)
T_REL = LEAD + 0.27                # nhả núm (máy cho cần bật về từ đây)


def to_dealer(x, y):
    m, d = BC["may"], BC["dealer"]
    sx, sy = m["x"] + m["scale"] * x, m["y"] - m["scale"] * y
    return ((sx - d["x"]) / d["scale"], (d["y"] - sy) / d["scale"])


PATH = [(t, *to_dealer(x, y)) for t, x, y in NUM["pull"]]


def knob(t):
    """Tâm núm cần (rig Lão Mực) ở giây t của clip pull của máy."""
    u = clamp(t * FPS_N, 0.0, len(PATH) - 1.0)
    i = min(len(PATH) - 2, int(u))
    f = u - i
    return (PATH[i][1] + (PATH[i + 1][1] - PATH[i][1]) * f, PATH[i][2] + (PATH[i + 1][2] - PATH[i][2]) * f)


def grip(t, s=1.0):
    """Dáng tay trái nắm núm ở giây t: cổ tay lùi GRIP_D x cỡ tay về phía vai, ống tay đi vào bàn tay theo hướng vai -> núm."""
    kx, ky = knob(t)
    dx, dy = kx - SHOULDER[0], ky - SHOULDER[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    a = math.degrees(math.atan2(uy, ux))
    hs = GRIP_HS * s
    return spec("t", to=(kx - ux * GRIP_D * hs, ky - uy * GRIP_D * hs), inn=180.0 - a, k=0.40, hand=HAND_GRIP, hs=hs)


@clip("sl_pull", 1.1, events=[(LEAD, "nam"), (LEAD + 0.17, "giat")])
def c_sl_pull(t, p):
    """Kéo cần máy quả. Liếc sang máy, nhún lấy đà (0 – 0,1) -> tay trái vươn dài lên núm (0,06 – 0,28), nắm (0,26) -> giật xuống
    chéo qua trước ngực (0,37 – 0,47, bàn tay bám núm theo đường núm của máy), thân ngả theo, gồng 3 khung -> nhả (0,57), tay bật
    lên theo đà rồi về quầy (– 0,95)."""
    amt = 1.0 - 0.75 * hat(t, 0.0, 0.08, 0.72, 1.0, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    reach = seg(t, 0.06, 0.28, back)
    yank = seg(t, LEAD + 0.07, LEAD + 0.17, lambda v: clamp(v) ** 1.6)
    held = yank * (1 - seg(t, T_REL, T_REL + 0.1, ease))
    rel = seg(t, T_REL, T_REL + 0.12, eout)
    ret = seg(t, T_REL + 0.10, 0.95, ease)
    # thân: ngả sang trái (về phía máy) lúc vươn, bị kéo ngả phải + lún lúc giật, bật lại lúc nhả
    lean = 6.0 * reach * (1 - yank) - 7.0 * held + 3.0 * hat(t, T_REL, T_REL + 0.08, T_REL + 0.14, T_REL + 0.3, eout, ease)
    spine(p, lean=lean, arc=3.0 * reach * (1 - yank) - 4.0 * held)
    p["mx"] += -10.0 * reach * (1 - yank) + 12.0 * held
    p["my"] += 10.0 * reach * (1 - yank) - 22.0 * held + 8.0 * hat(t, T_REL, T_REL + 0.06, T_REL + 0.1, T_REL + 0.26, eout, ease)
    p["sq"] += -0.04 * reach * (1 - yank) + 0.09 * held
    p["hr"] += 7.0 * reach * (1 - yank) - 6.0 * held + wob(t, T_REL, 0.4, 4.0, 3.0)
    p["hy"] += 6.0 * reach * (1 - yank) - 6.0 * held
    # tay trái: quầy -> núm (lúc nghỉ) -> bám núm theo đường núm -> buông, bật lên -> quầy
    kx, ky = knob(t)
    bx, by = knob(T_REL)
    up = spec("t", to=(bx - 70.0, by + 40.0 + 70.0 * rel), bow=20, k=0.42, hand=HAND_OPEN, hs=1.25)   # buông: tay ở lại chỗ nhả, xoè ra, nảy nhẹ lên (núm tự bật về)
    arm_seq(p, "t", on_table("t"), (grip(0.0, 0.92), reach), (grip(t), seg(t, 0.24, LEAD, lin)), (up, rel), (on_table("t"), ret))
    a = p["arm"]["t"]
    a["whip"] = 1.0 + 0.8 * hat(t, T_REL, T_REL + 0.05, T_REL + 0.2, T_REL + 0.36)
    a["drag"] = 0.5
    a["hrate"] = 14.0 if 0.2 <= t < T_REL + 0.05 else 6.5
    a["hand"] = steps(t, 9, 0.08, HAND_OPEN, 0.25, HAND_GRIP, T_REL + 0.01, HAND_OPEN, T_REL + 0.32, 9)
    p["arm"]["p"]["mix"] = [(on_table("p", bow=25.0 + 12.0 * held), 1.0)]
    # mặt: liếc sang máy, nhe răng lúc giật
    p["eye_d"] = (-6.0 * reach * (1 - ret), 3.0 * reach * (1 - yank) - 4.0 * held)
    p["mouth_s"] = (1.0 + 0.10 * held, 1.0 + 0.06 * held)
