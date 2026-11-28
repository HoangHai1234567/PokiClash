# Clip D3 của Lão Mực (GD_Claude/31 mục 4.2, lều Đêm Bài): chia bài cho người chơi / cho mình, nhìn trộm lá úp, lật lá úp, quá 21.
# hoat_anh.py nạp file này (đăng ký vào CLIPS bằng @clip) nên chạy như mọi clip khác: py -3 -I hoat_anh.py deal deal_self ...
#
# Bố cục bàn lều Đêm Bài (CasinoTablesMenu.BuildBlackjack; sân khấu 1080 x 1920, mép bàn sau ở y −1000, rig tỉ lệ 0,79, gốc rig ở
# y −1395): điểm sân khấu (x, y) <-> rig (x / 0,79, 500 − (−y − 1000) / 0,79). Đổi bố cục bàn thì sửa các mốc dưới rồi nướng lại.
import json
import math
import os
import sys

from dong_co import seg, hat, wob, ease, eout, ein, lin, back, clamp, spec, arm_seq, spine, ATOM

# hoat_anh.py nạp file này ở cuối phần clip; lấy đúng module đang chạy (chạy thẳng thì là __main__) để clip vào cùng bảng CLIPS
_H = sys.modules.get("hoat_anh") or sys.modules["__main__"]
clip, nhip, on_table, steps, shake, mir = _H.clip, _H.nhip, _H.on_table, _H.steps, _H.shake, _H.mir
HAND_BLADE = _H.HAND_BLADE

DECK = (418.0, 384.0)          # cỗ bài trên nỉ bên phải khay chip (sân khấu (330, −1092))
DROW_Y = 323.0                 # hàng bài của dealer (sân khấu y −1140)
HOLE = (42.0, DROW_Y)          # lá úp: ô thứ hai khi có hai lá (sân khấu x +33)
HAND_PINCH = 5                 # bàn tay kẹp (cầm lá)


@clip("deal", 1.0, events=[(0.36, "bung")])
def c_deal(t, p):
    """Chia một lá cho người chơi: nhón lá ở cỗ bài -> rút tay về sau vai lấy đà -> búng về phía người chơi (khung 0,36: lá rời
    tay, game cho lá bay tiếp tới ô) -> quá đà, bàn tay xoè -> về bàn. Thân nghiêng theo tay, mắt dõi theo lá."""
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.08, 0.7, 0.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    grab = seg(t, 0.02, 0.14, eout)
    coil = seg(t, 0.15, 0.27, eout)
    flick = seg(t, 0.28, 0.36, lambda u: clamp(u) ** 1.6)
    over = hat(t, 0.36, 0.41, 0.46, 0.6, eout, ease)
    ret = seg(t, 0.52, 0.86, ease)
    lean = -5.0 * grab * (1 - coil) - 3.0 * coil * (1 - flick) + 4.0 * flick * (1 - ret)
    spine(p, lean=lean, arc=-5.0 * flick * (1 - ret) + 2.0 * coil * (1 - flick))
    p["my"] += -5.0 * grab * (1 - coil) + 4.0 * coil * (1 - flick) - 10.0 * flick * (1 - ret)
    p["sq"] += 0.05 * coil * (1 - flick) - 0.05 * over
    p["hr"] += -7.0 * grab * (1 - coil) + 6.0 * flick * (1 - ret) + wob(t, 0.36, 0.3, 3.0, 4.0)
    p["hy"] += -6.0 * flick * (1 - ret)
    deck_a = spec("p", to=(DECK[0], DECK[1] + 26.0), bow=44.0, k=0.5, hand=HAND_PINCH, hrot=250, hs=1.0)
    coil_a = spec("p", to=(318.0, 640.0), bow=52.0, k=0.5, hand=HAND_PINCH, hrot=78, hs=1.0)
    rel_a = spec("p", to=(150.0, 262.0 - 30.0 * over), bow=-18.0, k=0.45, hand=1, hrot=258, hs=1.15)
    arm_seq(p, "p", on_table("p"), (deck_a, grab), (coil_a, coil), (rel_a, flick), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["whip"] = 1.0 + 0.8 * hat(t, 0.34, 0.38, 0.5, 0.62)
    a["drag"] = 0.5
    a["hand"] = steps(t, 9, 0.04, 1, 0.12, HAND_PINCH, 0.36, 1, 0.72, 9)
    p["card"] = "la_bai" if 0.12 <= t < 0.36 else None
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 10.0 * coil * (1 - ret)), 1.0)]
    p["eye"] = steps(t, 2, 0.1, 10, 0.3, 1, 0.5, 2)
    p["eye_d"] = (4.0 * grab * (1 - coil), -7.0 * flick * (1 - ret))
    p["mouth"] = steps(t, 1, 0.26, 10, 0.4, 1)


@clip("deal_self", 1.0, events=[(0.38, "bung")])
def c_deal_self(t, p):
    """Chia một lá cho mình: nhón lá ở cỗ bài -> vòng tay đặt lá xuống hàng bài trước bụng (khung 0,38 lá rời tay, game cho lá
    trượt nốt vào ô) -> bàn tay úp vỗ nhẹ -> về bàn."""
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.08, 0.7, 0.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    grab = seg(t, 0.02, 0.14, eout)
    lift = seg(t, 0.16, 0.26, eout)
    lay = seg(t, 0.27, 0.38, ease)
    pat = hat(t, 0.38, 0.42, 0.46, 0.56, eout, ease)
    ret = seg(t, 0.56, 0.88, ease)
    spine(p, lean=-5.0 * grab * (1 - lay) + 1.5 * lay * (1 - ret), arc=-3.0 * lay * (1 - ret))
    p["my"] += -5.0 * grab * (1 - lift) - 8.0 * lay * (1 - ret) - 4.0 * pat
    p["sq"] += 0.03 * pat
    p["hr"] += -6.0 * grab * (1 - lift) + 3.0 * lay * (1 - ret)
    p["hy"] += -8.0 * lay * (1 - ret)
    deck_a = spec("p", to=(DECK[0], DECK[1] + 26.0), bow=44.0, k=0.5, hand=HAND_PINCH, hrot=250, hs=1.0)
    lift_a = spec("p", to=(260.0, 470.0), bow=40.0, k=0.5, hand=HAND_PINCH, hrot=200, hs=1.0)
    lay_a = spec("p", to=(96.0, DROW_Y + 58.0 - 10.0 * pat), out=-10, inn=196, k=0.55, hand=HAND_PINCH, hrot=205, hs=1.05)
    arm_seq(p, "p", on_table("p"), (deck_a, grab), (lift_a, lift), (lay_a, lay), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["drag"] = 0.4
    a["hand"] = steps(t, 9, 0.04, 1, 0.12, HAND_PINCH, 0.38, 9)
    p["card"] = "la_bai" if 0.12 <= t < 0.38 else None
    p["eye"] = steps(t, 2, 0.12, 10, 0.3, 7, 0.6, 2)
    p["eye_d"] = (3.0 * grab * (1 - lift), -6.0 * lay * (1 - ret))
    p["mouth"] = steps(t, 1, 0.3, 10, 0.62, 1)


@clip("peek", 1.5)
def c_peek(t, p):
    """Nhìn trộm lá úp (lá ngửa là A hoặc 10): chồm tới, tay phải nhấc góc lá (game nhấc lá theo, 0,35 – 0,95), một mắt to một mắt
    nheo, miệng méo hồi hộp; buông lá, ngồi lại. Có blackjack hay không do game nói bằng bong bóng ngay sau clip."""
    amt = 1.0 - 0.7 * hat(t, 0.0, 0.1, 1.2, 1.45, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    reach = seg(t, 0.06, 0.3, back)
    lean = hat(t, 0.1, 0.34, 0.95, 1.2, eout, ease)
    ret = seg(t, 0.98, 1.3, ease)
    spine(p, arc=-7.0 * lean, lean=2.0 * lean)
    p["my"] += -16.0 * lean
    p["hy"] += -14.0 * lean
    p["hr"] += -5.0 * lean + 1.2 * shake(t, 10) * hat(t, 0.4, 0.45, 0.85, 0.9)
    corner = spec("p", to=(HOLE[0] + 54.0, HOLE[1] + 40.0 + 18.0 * hat(t, 0.35, 0.45, 0.85, 0.95)), out=-8, inn=200, k=0.55,
                  hand=HAND_PINCH, hrot=210, hs=1.05)
    arm_seq(p, "p", on_table("p"), (corner, reach), (on_table("p"), ret))
    p["arm"]["p"]["drag"] = 0.3
    p["arm"]["p"]["hand"] = steps(t, 9, 0.06, 1, 0.28, HAND_PINCH, 1.0, 9)
    p["eye"] = steps(t, 2, 0.3, 8, 1.0, 2)
    p["eye_d"] = (0.0, -9.0 * lean)
    p["mouth"] = steps(t, 1, 0.3, 6, 1.0, 1)
    p["mouth_s"] = (1.0 + 0.05 * shake(t, 12) * lean, 1.0)


@clip("reveal", 1.0, events=[(0.38, "lat")])
def c_reveal(t, p):
    """Lật lá úp kiểu ảo thuật: tay tới lá, kẹp (0,28) -> xoay cổ tay hất lá (0,38: game lật lá) -> bàn tay xoè giơ lên "ta-da"
    -> về bàn."""
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.08, 0.72, 0.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    reach = seg(t, 0.04, 0.26, eout)
    flip = seg(t, 0.28, 0.38, lambda u: clamp(u) ** 1.4)
    tada = hat(t, 0.38, 0.46, 0.52, 0.68, back, ease)
    ret = seg(t, 0.52, 0.78, ease)
    spine(p, arc=-4.0 * reach * (1 - flip) + 3.0 * tada, lean=-3.0 * tada)
    p["my"] += -10.0 * reach * (1 - flip) + 10.0 * tada
    p["sq"] += -0.05 * tada
    p["hr"] += -6.0 * reach * (1 - flip) + 7.0 * tada + wob(t, 0.42, 0.3, 3.0, 4.0)
    at_card = spec("p", to=(HOLE[0] + 40.0, HOLE[1] + 48.0), out=-8, inn=200, k=0.55, hand=HAND_PINCH, hrot=215, hs=1.05)
    flip_a = spec("p", to=(150.0, 470.0), bow=40.0, k=0.5, hand=HAND_PINCH, hrot=125, hs=1.05)
    tada_a = spec("p", to=(300.0, 760.0), space="v", out=-60, inn=84, k=0.5, hand=1, hrot=70, hs=1.05)
    arm_seq(p, "p", on_table("p"), (at_card, reach), (flip_a, flip), (tada_a, seg(t, 0.38, 0.47, eout)), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["whip"] = 1.0 + 0.8 * hat(t, 0.36, 0.4, 0.5, 0.64)
    a["hand"] = steps(t, 9, 0.05, 1, 0.22, HAND_PINCH, 0.38, 6, 0.7, 9)
    p["eye"] = steps(t, 2, 0.2, 10, 0.38, 6, 0.7, 2)
    p["mouth"] = steps(t, 1, 0.38, 9, 0.7, 1)


@clip("bust_self", 2.0)
def c_bust(t, p):
    """Dealer quá 21: giật mình (mắt lồi, há hốc) -> hai tay ôm đầu, thân bẹp, lắc đầu -> thở hắt, buông tay về bàn."""
    amt = 1.0 - 0.8 * hat(t, 0.0, 0.08, 1.6, 1.9, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    jolt = hat(t, 0.0, 0.06, 0.1, 0.22, eout, ease)
    grab = seg(t, 0.12, 0.3, back)
    hold = grab * (1 - seg(t, 1.25, 1.55, ease))
    shake_h = hat(t, 0.32, 0.4, 1.0, 1.15)
    p["my"] += 16.0 * jolt - 5.0 * hold
    p["sq"] += -0.08 * jolt + 0.03 * hold
    p["hsq"] += -0.07 * jolt + 0.02 * hold
    p["hy"] += 6.0 * hold
    p["hr"] += 9.0 * math.sin((t - 0.32) * 2 * math.pi * 3.0) * shake_h
    spine(p, arc=-3.0 * hold)
    for s in "tp":
        # khuỷu chìa ngang ra ngoài rồi cẳng tay dựng lên: ống tay đi vòng ngoài đầu, không che mặt (vai nằm dưới đầu)
        head_a = spec(s, to=mir(s, 292.0, 1040.0), space="h", out=-14, inn=88, k=0.5, hand=1, hrot=100, hs=1.0)
        arm_seq(p, s, on_table(s), (head_a, grab), (on_table(s), seg(t, 1.3, 1.62, ease)))
        p["arm"][s]["shr"] = (0.0, p["arm"][s]["shr"][1] + 10.0 * hold)
        p["arm"][s]["hand"] = steps(t, 9, 0.12, 1, 1.45, 9)
    p["eye"] = steps(t, 2, 0.03, 5, 0.3, 3, 1.3, 7, 1.7, 2)
    p["mouth"] = steps(t, 1, 0.03, 4, 0.3, 6, 1.3, 3, 1.7, 1)
    p["mouth_s"] = (1.0 + 0.06 * shake(t, 12) * hold, 1.0)
    p["lv_r"] += 6.0 * jolt


# ---------------------------------------------------------------- D3 phần hai: xoè bài, tách, gấp đôi, rút hồi hộp
XAO_N = 7
SPRING_T0, SPRING_GAP, SPRING_FLY = 0.6, 0.08, 0.22   # lá i rời tay phải ở T0 + i * GAP, bay FLY giây sang tay trái
SPRING_ARC = 120.0             # độ vồng của dòng bài (thấp hơn miệng, không che mặt)
HAND_GRIP = 7                  # bàn tay cầm vật (chữ C): ngón trên, ngón cái dưới, miệng chữ C quay về phía đầu ngón
# Đáy và miệng chữ C của hình tay_07 (px ảnh, y xuống; đo trên ảnh). Cỗ bài cắm vào chữ C: mép lá thụt sau đáy GRIP_IN px (lòng
# bàn tay che), thân lá chĩa ra theo miệng chữ C; lá vẽ dưới bàn tay nên ngón trên và ngón cái đè lên hai mép lá.
GRIP_IMG, MOUTH_IMG = (118.0, 84.0), (176.0, 80.0)
CARD_LEN, GRIP_IN = 158.0, 26.0        # chiều dài hình la_bai
HOLD_ROT = 150.0               # góc bàn tay lúc cầm bài trước ngực: miệng chữ C hai tay gần như đối nhau (hơi chúc xuống)
_GEO = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))["parts"][f"tay_{HAND_GRIP:02d}"]


def _grip_local(s):
    """Đáy chữ C và hướng miệng chữ C trong hệ xương tay_<s>b (cùng phép đặt hình như dung_rig.parts_ops; tay phải lật ngang)."""
    f = -1.0 if s == "p" else 1.0
    dx, dy = _GEO["huong"]
    gx, gy = _GEO["goc"]
    rot = -math.atan2(-dy, dx * f)
    c, s_ = math.cos(rot), math.sin(rot)

    def loc(q):
        ux, uy = (q[0] - gx) * f, -(q[1] - gy)
        return (c * ux - s_ * uy - 8.0, s_ * ux + c * uy)
    g, m = loc(GRIP_IMG), loc(MOUTH_IMG)
    return g, math.degrees(math.atan2(m[1] - g[1], m[0] - g[0]))


GRIP = {s: _grip_local(s) for s in "tp"}


def grip(hw, s):
    """Cỗ bài cầm trong chữ C của bàn tay s (thế giới): (tâm lá, góc xoay lá). Lá đứng dọc theo trục y ảnh nên góc = miệng − 90."""
    (x, y), a = hw[s]
    (gx, gy), da = GRIP[s]
    r = math.radians(a)
    g = (x + gx * math.cos(r) - gy * math.sin(r), y + gx * math.sin(r) + gy * math.cos(r))
    o = math.radians(a + da)
    k = CARD_LEN / 2 - GRIP_IN
    return (g[0] + k * math.cos(o), g[1] + k * math.sin(o)), a + da - 90.0


def hand_to(s, center, hrot):
    """Đích cổ tay (spec `to`) để cỗ bài trong bàn tay s có tâm ở `center` khi tay đứng yên ở góc hrot (tay trái lật như spec)."""
    a = hrot if s == "p" else 180.0 - hrot
    c0, _ = grip({s: ((0.0, 0.0), a)}, s)
    return (center[0] - c0[0], center[1] - c0[1])


def turn180(a, b):
    """Hiệu góc ngắn nhất b − a theo chu kỳ 180 (lưng bài xoay nửa vòng trông như cũ)."""
    return (b - a + 90.0) % 180.0 - 90.0


def lerp2(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


@clip("shuffle", 2.5, events=[(0.26, "nhac_bai"), (1.66, "go_bai"), (2.05, "dat_bai")])
def c_shuffle(t, p):
    """Xoè bài đầu phiên: tay phải nhấc cỗ bài trên nỉ (0,26: game ẩn hình cỗ bài) -> hai tay nâng lên trước ngực, mỗi tay kẹp một
    đầu cỗ bài -> bài bắn thành vòng cung từ tay phải sang tay trái (lò xo, từng lá một) -> hai tay khép lại kẹp hai đầu, gõ cỗ bài
    xuống (1,66) -> tay phải đặt cỗ bài về chỗ cũ (2,05: game hiện lại hình cỗ bài) -> về bàn. Mắt dõi theo dòng bài, miệng cười
    đắc ý. Lá luôn nằm trong chữ C của bàn tay cầm (grip), không đặt theo cổ tay."""
    amt = 1.0 - 0.75 * hat(t, 0.0, 0.1, 2.05, 2.4, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    grab = seg(t, 0.06, 0.26, eout)
    rise = seg(t, 0.28, 0.55, ease)
    spread = seg(t, 0.58, 0.8, eout) * (1 - seg(t, 1.3, 1.5, ease))
    tog = seg(t, 1.3, 1.5, ease)
    tap = hat(t, 1.52, 1.66, 1.68, 1.78, ein, eout)
    carry = seg(t, 1.76, 2.05, ease)
    ret = seg(t, 2.08, 2.38, ease)
    # cổ tay đặt sao cho cỗ bài trong chữ C rơi đúng chỗ cần: cỗ bài trên nỉ lúc nhấc / đặt, giữa ngực lúc hai tay kẹp chung
    lift_to = hand_to("p", (DECK[0], DECK[1] + 8.0), 240.0)
    put_to = hand_to("p", (DECK[0], DECK[1] + 8.0), 230.0)
    hx = hand_to("p", (0.0, 0.0), HOLD_ROT)[0]       # cổ tay phải khi tâm cỗ bài ở giữa (x = 0)
    hold_x = (hx + 20.0 + 125.0 * spread) * (1 - tog) + (hx + 12.0) * tog   # khép: hai đầu ngón găng vừa chạm, chừa lưng bài
    # tay phải: cỗ bài -> trước ngực -> dang -> khép -> gõ -> đặt lại cỗ bài -> về bàn
    deck_a = spec("p", to=lift_to, bow=44.0, k=0.5, hand=HAND_GRIP, hrot=240, hs=1.0)
    hold_p = spec("p", to=(hold_x, 700.0 + 35.0 * spread - 135.0 * tap), bow=40.0, k=0.5, hand=HAND_GRIP, hrot=HOLD_ROT, hs=1.0)
    carry_p = spec("p", to=put_to, bow=40.0, k=0.5, hand=HAND_GRIP, hrot=230, hs=1.0)
    arm_seq(p, "p", on_table("p"), (deck_a, grab), (hold_p, rise), (carry_p, carry), (on_table("p"), ret))
    # tay trái: nâng lên kẹp đầu kia -> dang đón bài -> khép, gõ -> về bàn khi tay phải mang cỗ bài đi
    hold_t = spec("t", to=mir("t", hold_x, 700.0 - 5.0 * spread - 135.0 * tap), bow=40.0, k=0.5, hand=HAND_GRIP, hrot=HOLD_ROT,
                  hs=1.0)
    arm_seq(p, "t", on_table("t"), (hold_t, rise), (on_table("t"), seg(t, 1.8, 2.15, ease)))
    for s in "tp":
        p["arm"][s]["drag"] = 0.3
        p["arm"][s]["hand"] = HAND_GRIP if 0.2 <= t < (2.08 if s == "p" else 1.85) else 9
    spine(p, lean=-4.0 * grab * (1 - rise), arc=-2.0 * rise * (1 - carry))
    p["my"] += 8.0 * rise * (1 - carry) - 10.0 * tap
    p["sq"] += -0.03 * rise * (1 - carry) + 0.06 * tap
    p["hy"] += -6.0 * tap
    flow = seg(t, SPRING_T0, SPRING_T0 + XAO_N * SPRING_GAP + SPRING_FLY, lin)
    p["eye"] = steps(t, 2, 0.5, 10, 0.6, 1, 1.3, 2, 1.6, 3, 1.8, 2)
    p["eye_d"] = (8.0 - 16.0 * flow if 0.6 <= t < 1.3 else 0.0, -4.0 * tap)
    p["mouth"] = steps(t, 1, 0.55, 10, 1.3, 1)

    def cards(hw):
        (R, rR), (L, rL) = grip(hw, "p"), grip(hw, "t")
        # góc tay trái quy về bản gần góc tay phải nhất (lưng bài xoay nửa vòng trông như cũ): góc lá liền một mạch từ lúc rời tay
        # phải tới lúc đáp tay trái, không nhảy 180 độ giữa hai khung (game nội suy giữa hai khoá sẽ thấy lá quay vụt)
        rL = rR + turn180(rR, rL)
        # cỗ bài hai tay kẹp chung: tâm giữa hai chữ C, góc trung bình; tay trái thả ra (1,76 – 1,9) thì cỗ bài theo hẳn tay phải
        both, r_both = lerp2(L, R, 0.5), rL + (rR - rL) * 0.5
        go = seg(t, 1.76, 1.9, ease)
        vis = 0.26 <= t < 2.05               # ngoài khoảng này lá ẩn (hình cỗ bài trên nỉ hiện) nhưng vẫn đi liền theo tay phải
        out = []
        for i in range(XAO_N):
            up = 2.2 * i                    # bề dày cỗ bài: lá trên lệch lên một chút
            ts = SPRING_T0 + i * SPRING_GAP
            if t < ts:                       # còn trong cỗ bài ở tay phải
                pos, r = R, rR
            elif t < ts + SPRING_FLY:        # đang bay vòng cung sang tay trái
                u = ease((t - ts) / SPRING_FLY)
                b = lerp2(R, L, u)
                pos = (b[0], b[1] + SPRING_ARC * math.sin(math.pi * u))
                r = rR + (rL - rR) * u + 30.0 * math.sin(math.pi * u)
            else:                            # đã sang tay trái; khép (kẹp chung), gõ, rồi theo tay phải về chỗ cỗ bài
                pos = lerp2(L, both, tog)
                r = rL + (r_both - rL) * tog
                pos = lerp2(pos, R, go)
                r = r + (rR - r) * go
            out.append((pos[0], pos[1] + up, r, vis))
        return out

    p["xao"] = cards


@clip("split", 1.0, events=[(0.42, "tach")])
def c_split(t, p):
    """Tách: hai bàn tay dựng đứng chụm lại giữa bàn rồi gạt dạt ra hai bên (0,42: game cho hai lá dạt sang hai tay), mắt mở to."""
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.08, 0.72, 0.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    join = seg(t, 0.04, 0.24, eout)
    sweep = seg(t, 0.3, 0.42, lambda u: clamp(u) ** 1.4)
    ret = seg(t, 0.56, 0.86, ease)
    for s in "tp":
        mid_a = spec(s, to=mir(s, 44.0, 360.0), out=-14, inn=210, k=0.5, hand=HAND_BLADE, hrot=200, hs=1.05)
        out_a = spec(s, to=mir(s, 330.0, 345.0), out=-14, inn=200, k=0.5, hand=HAND_BLADE, hrot=190, hs=1.05)
        arm_seq(p, s, on_table(s), (mid_a, join), (out_a, sweep), (on_table(s), ret))
        p["arm"][s]["whip"] = 1.0 + 0.6 * hat(t, 0.38, 0.42, 0.52, 0.64)
        p["arm"][s]["hand"] = steps(t, 9, 0.06, HAND_BLADE, 0.7, 9)
    spine(p, arc=-4.0 * join * (1 - ret))
    p["my"] += -10.0 * join * (1 - ret) + 6.0 * hat(t, 0.42, 0.46, 0.5, 0.6)
    p["hr"] += wob(t, 0.42, 0.3, 3.0, 4.0)
    p["eye"] = steps(t, 2, 0.1, 4, 0.42, 1, 0.7, 2)
    p["mouth"] = steps(t, 1, 0.1, 3, 0.42, 2, 0.7, 1)


@clip("double", 1.0)
def c_double(t, p):
    """Gấp đôi: nhướn mắt tròn xoe nhìn chồng chip thêm, chồm tới, xoa tay nhanh, liếm mép ("chơi lớn hả?"), rồi về."""
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.08, 0.72, 0.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    pop = hat(t, 0.0, 0.08, 0.14, 0.22, eout, ease)
    lean = hat(t, 0.14, 0.3, 0.62, 0.8, back, ease)
    rub = hat(t, 0.24, 0.3, 0.6, 0.66, ease, ease)
    w = math.sin(t * 2 * math.pi * 6.0) * rub
    p["my"] += 14.0 * pop - 18.0 * lean
    p["sq"] += -0.08 * pop + 0.05 * lean
    p["hy"] += -12.0 * lean
    p["hsq"] += -0.07 * pop
    spine(p, arc=-4.0 * lean)
    for s in "tp":
        tog = spec(s, to=mir(s, 30.0, 655.0 + 15.0 * w * (1 if s == "p" else -1)), bow=58.0, k=0.62, hand=2, hrot=140, hs=1.0)
        arm_seq(p, s, on_table(s), (tog, seg(t, 0.16, 0.32, back)), (on_table(s), seg(t, 0.62, 0.86, ease)))
        p["arm"][s]["drag"] = 0.2
        p["arm"][s]["hand"] = steps(t, 9, 0.16, 2, 0.74, 9)
    p["eye"] = steps(t, 2, 0.02, 4, 0.3, 3, 0.7, 2)
    p["eye_d"] = (0.0, -7.0 * lean)
    p["mouth"] = steps(t, 1, 0.3, 7, 0.66, 1)


@clip("deal_self_tense", 1.0, events=[(0.38, "bung")])
def c_deal_self_tense(t, p):
    """Dealer rút khi tổng 12–16 (dễ quá 21): như deal_self nhưng run run, mắt lồi, miệng méo, hai giọt mồ hôi rịn ở thái dương rồi
    chảy xuống."""
    c_deal_self(t, p)
    p["eye"] = steps(t, 4, 0.3, 5, 0.62, 4)
    p["mouth"] = 6
    p["mouth_s"] = (1.0 + 0.05 * shake(t, 12), 1.0)
    p["hr"] += 1.4 * shake(t, 14)
    # giọt tắt trước đoạn hoà về idle (0,7 s cuối) để không bị kéo trôi ngược lên
    u1 = seg(t, 0.02, 0.64, lin)
    u2 = seg(t, 0.14, 0.68, lin)
    p["sweat"] = [(0.0, -46.0 * u1, 0.02 <= t < 0.66), (0.0, -34.0 * u2, 0.14 <= t < 0.69)]
