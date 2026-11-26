# Clip D4 của Lão Mực (GD_Claude/31 mục 4.3, lều Vòng Xoay): mời đặt cửa, "hết đặt!", quất mâm + búng bi, dõi theo bi, chỉ ô ra.
# hoat_anh.py nạp file này (đăng ký vào CLIPS bằng @clip) nên chạy như mọi clip khác:
#   py -3 -I hoat_anh.py rl_invite rl_no_more rl_spin rl_watch rl_point
#
# Bố cục lều Vòng Xoay (KHÁC lều Đêm Bài): sân khấu 1080 x 1920, rig tỉ lệ 0,70, mép bàn sau ở y −650 (rig y 500):
#   sân khấu (x, y) <-> rig (x / 0,7, 500 − (−y − 650) / 0,7).
#   Bảng cược nỉ: sân khấu x ±450, y −775..−1250 (rig x ±643, y 321..−357).
#   Bánh xe nằm sát người chơi: tâm sân khấu (0, −1500) = rig (0, −714), bán kính vành ngoài 320 px sân khấu (rig 457), nhìn
#   nghiêng nên dẹt 0,6; điểm ở bán kính r (phần của vành ngoài), góc a, độ cao h: rig (457 r cos a, −714 + 457 (0,6 r sin a + 0,8 h)).
#   Mâm xoay bán kính 0,70 (rig rx 320, ry 192), mép xa (đỉnh elip, gần Lão Mực nhất) rig (0, −522). Mâm xoay NGƯỢC chiều kim đồng hồ
#   trên màn (ở mép xa mặt mâm chạy sang TRÁI); bi chạy THEO chiều kim đồng hồ, vào đường chạy ở góc 40° (phải, xa): rig (306, −520).
# Tay "p" là tay bên PHẢI màn (x dương), "t" bên trái. Đổi bố cục thì sửa các mốc dưới rồi nướng lại.
import math
import sys

from dong_co import seg, hat, wob, ease, eout, ein, lin, back, clamp, spec, arm_seq, spine

# hoat_anh.py nạp file này ở cuối phần clip; lấy đúng module đang chạy (chạy thẳng thì là __main__) để clip vào cùng bảng CLIPS
_H = sys.modules.get("hoat_anh") or sys.modules["__main__"]
clip, nhip, on_table, steps, shake, mir = _H.clip, _H.nhip, _H.on_table, _H.steps, _H.shake, _H.mir

F = 1.0 / 30.0
WHEEL = (0.0, -714.0)          # tâm mặt phẳng ô của bánh xe
WHEEL_R = 457.0                # bán kính vành ngoài (rig)
ROTOR_RX, ROTOR_RY = 0.70 * WHEEL_R, 0.70 * WHEEL_R * 0.6   # mâm xoay: 320 x 192
GRAB_X, WHIP_X = 140.0, -260.0  # bàn tay trái bám mép xa của mâm ở x 140, quất dọc mép tới x −260
GRAB_HS = 1.25                 # cỡ bàn tay lúc bám mâm
PALM = (-18.0, 130.0)          # cổ tay so với điểm lòng bàn tay chạm mâm (bàn tay chĩa xuống −82 độ, lòng cách cổ tay 105 x 1,25)
ENTRY = (306.0, -520.0)        # chỗ bi vào đường chạy (game lái đường bay của bi tới đây, rig không vẽ)
HAND_OPEN, HAND_POINT, HAND_PINCH, HAND_WAVE, HAND_FLAT = 1, 4, 5, 6, 9


def rotor_far(x):
    """Điểm trên mép xa của mâm xoay (nửa trên elip) ở hoành độ x."""
    return (x, WHEEL[1] + ROTOR_RY * math.sqrt(max(0.0, 1.0 - (x / ROTOR_RX) ** 2)))


# ---------------------------------------------------------------- rl_invite: mời đặt cửa
@clip("rl_invite", 2.0)
def c_rl_invite(t, p):
    """Mời đặt cửa: tay phải nhấc khỏi bàn, vắt sang trái (thân ngả theo) -> quạt một cung rộng trên bảng cược từ trái sang phải,
    bàn tay xoè ngón chĩa xuống bảng -> dừng ở bên phải, bàn tay ngửa "mời", nháy mắt, đầu nghiêng -> về bàn."""
    amt = 1.0 - 0.7 * hat(t, 0.0, 0.1, 1.5, 1.85, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    cross = seg(t, 0.08, 0.36, back)
    sweep = seg(t, 0.42, 0.82, ease)
    hold = sweep * (1 - seg(t, 1.38, 1.6, ease))
    ret = seg(t, 1.42, 1.76, ease)
    lean = 5.0 * cross * (1 - sweep) - 5.0 * hold
    spine(p, lean=lean, arc=3.0 * cross * (1 - sweep) - 3.0 * hold)
    p["mx"] += -8.0 * cross * (1 - sweep) + 8.0 * hold
    p["my"] += -8.0 * cross * (1 - ret) + 5.0 * hat(t, 0.82, 0.9, 0.94, 1.1, eout, ease)
    p["hr"] += 5.0 * cross * (1 - sweep) - 9.0 * hold + wob(t, 0.82, 0.4, 3.5, 3.0)
    p["hy"] += -5.0 * cross * (1 - ret)
    # cung quạt: từ (−170, 300) võng xuống giữa bảng rồi lên (400, 235)
    u = sweep
    sx = -170.0 + 570.0 * u
    sy = 300.0 - 65.0 * u - 90.0 * math.sin(math.pi * u)
    left_a = spec("p", to=(-170.0, 300.0), out=-65, inn=225, k=0.5, hand=HAND_OPEN, hrot=236, hs=1.2)
    fan_a = spec("p", to=(sx, sy + 8.0 * math.sin((t - 0.82) * 2 * math.pi * 2.0) * hold * (1 - seg(t, 1.2, 1.4))),
                 out=-65 - 15 * u, inn=225 + 95 * u, k=0.5, hand=HAND_OPEN, hrot=236 + 64 * u, hs=1.2 + 0.08 * u)
    arm_seq(p, "p", on_table("p"), (left_a, cross), (fan_a, seg(t, 0.4, 0.46, lin)), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["whip"] = 1.0 + 0.6 * hat(t, 0.78, 0.84, 1.0, 1.2)
    a["drag"] = 0.6
    a["hand"] = steps(t, 9, 0.1, HAND_OPEN, 1.66, 9)
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 12.0 * hold), 1.0)]
    # mắt dõi theo bàn tay quạt, rồi nháy một mắt với người chơi
    p["eye"] = steps(t, 2, 0.12, 10, 0.86, 8, 1.36, 2)
    p["eye_s"] = (-1.0 if 0.6 <= t < 0.86 else 1.0, 1.0)
    p["eye_d"] = (0.0, -5.0 * cross * (1 - hold) * (1 - ret))
    p["mouth"] = steps(t, 1, 0.12, 10, 0.86, 1, 1.5, 1)
    ms = 1.0 + 0.10 * hat(t, 0.86, 0.94, 1.3, 1.45)
    p["mouth_s"] = (ms, ms)


# ---------------------------------------------------------------- rl_no_more: hết đặt
@clip("rl_no_more", 1.0)
def c_rl_no_more(t, p):
    """"Hết đặt!": tay phải úp, rút sang trái lấy đà -> xua ngang một cái dứt khoát trên bảng cược từ trái sang phải (cổ tay đi
    trước, ngón rê sau) -> khựng, lắc tắt dần -> về bàn. Mặt nghiêm, miệng chu hô."""
    amt = 1.0 - 0.7 * hat(t, 0.0, 0.08, 0.66, 0.92, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    coil = seg(t, 0.04, 0.26, back)
    cut = seg(t, 0.3, 0.42, lambda v: clamp(v) ** 1.5)
    stop = hat(t, 0.42, 0.45, 0.52, 0.66, lin, ease)
    ret = seg(t, 0.62, 0.9, ease)
    spine(p, lean=5.0 * coil * (1 - cut) - 6.0 * cut * (1 - ret), arc=3.0 * coil * (1 - cut))
    p["mx"] += -7.0 * coil * (1 - cut) + 9.0 * cut * (1 - ret)
    p["my"] += 6.0 * coil * (1 - cut) - 12.0 * cut * (1 - ret) - 6.0 * stop
    p["sq"] += -0.03 * coil * (1 - cut) + 0.05 * stop
    p["hr"] += 5.0 * coil * (1 - cut) - 6.0 * cut * (1 - ret) + wob(t, 0.42, 0.34, 4.0, 3.0)
    p["hy"] += -5.0 * cut * (1 - ret)
    coil_a = spec("p", to=(-130.0, 215.0), out=-60, inn=215, k=0.5, hand=HAND_FLAT, hrot=200, hs=1.25)
    cut_a = spec("p", to=(440.0, 160.0), out=-80, inn=322, k=0.45, hand=HAND_FLAT, hrot=176, hs=1.3,
                 hsq=-0.10 * hat(t, 0.34, 0.4, 0.42, 0.5, lin, ease))
    arm_seq(p, "p", on_table("p"), (coil_a, coil), (cut_a, cut), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["whip"] = 1.0 + 0.9 * hat(t, 0.4, 0.44, 0.56, 0.72)
    a["drag"] = 0.7
    a["hrate"] = 12.0 if 0.28 <= t < 0.6 else 6.5
    a["hand"] = HAND_FLAT
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 12.0 * cut * (1 - ret)), 1.0)]
    p["eye"] = steps(t, 2, 0.06, 1, 0.3, 9, 0.7, 2)
    p["eye_d"] = (0.0, -5.0 * cut * (1 - ret))
    p["mouth"] = steps(t, 1, 0.06, 10, 0.3, 3, 0.62, 1)
    p["mouth_s"] = (1.0, 1.0 + 0.12 * stop)


# ---------------------------------------------------------------- rl_spin: quất mâm xoay, búng bi
T_HIT = 21 * F                 # 0,70: bàn tay trái đập xuống mép xa của mâm
T_QUAY = 23 * F                # 0,767: bắt đầu quất (sự kiện quay: game cho mâm quay)
T_WHIP1 = 26 * F               # 0,867: hết cú quất, tay văng khỏi mâm
T_THA = 45 * F                 # 1,50: bi rời tay phải (sự kiện tha_bi: game cho bi bay tới đường chạy)


@clip("rl_spin", 2.0, events=[(T_QUAY, "quay"), (T_THA, "tha_bi")])
def c_rl_spin(t, p):
    """Quay bánh xe. Tay phải kẹp viên bi giơ lên khoe (0,06 – 0,3), mặt nhếch -> xoắn người lấy đà, tay trái cuộn chữ W cao
    (0,24 – 0,6) -> tay trái BẮN DÀI xuống mép xa của mâm (0,60 – 0,70: ống chùng rồi căng), bàn tay xoè đập bẹp lên mâm, giữ 2 khung
    -> QUẤT dọc mép mâm sang trái (0,767 – 0,867, sự kiện quay ở khung đầu), tay văng ra ngoài rồi thu về thành sóng -> tay phải rút
    ra sau đầu lấy đà (1,16 – 1,38) -> ném chúi viên bi xuống dọc sườn phải (1,40 – 1,50; 1,50 bi rời tay: sự kiện tha_bi, slot bi
    tắt, bàn tay xoè) -> quá đà, về bàn. Game gối sang rl_watch ngay sau tha_bi."""
    amt = 1.0 - hat(t, 0.0, 0.08, 1.62, 1.95, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    show = seg(t, 0.04, 0.24, back)
    coil = hat(t, 0.24, 0.5, T_HIT - 0.1, T_HIT - 0.04, ease, ein)
    coil2 = hat(t, 0.46, 0.58, T_HIT - 0.1, T_HIT - 0.04, ease, ein)        # cuộn cao thêm một nấc ngay trước khi ra tay
    strike = seg(t, T_HIT - 0.1, T_HIT, lambda v: clamp(v) ** 1.6)
    press = hat(t, T_HIT, T_HIT + 0.02, T_QUAY, T_QUAY + 0.05, lin, ease)   # bàn tay bẹp trên mâm
    whipk = seg(t, T_QUAY, T_WHIP1, lambda v: clamp(v) ** 1.35)
    fling = seg(t, T_WHIP1, T_WHIP1 + 0.1, eout)
    ret_t = seg(t, 0.98, 1.28, ease)
    lunge = hat(t, T_HIT - 0.08, T_HIT, 0.9, 1.12, eout, ease)              # chồm theo tay trái
    wind = hat(t, 1.16, 1.38, 1.40, 1.44, ease, ein)
    throw = seg(t, 1.40, T_THA, lambda v: clamp(v) ** 1.6)
    over = hat(t, T_THA, T_THA + 0.05, T_THA + 0.08, 1.72, eout, ease)
    ret_p = seg(t, 1.6, 1.9, ease)
    dive = throw * (1 - ret_p)                                              # chồm theo cú ném
    # thân: lấy đà thì vươn cao, ngả về bên phải (ngược hướng quất); đập xuống thì chồm tới, bẹp; quất thì vặn sang trái
    p["sq"] += -0.07 * coil - 0.04 * coil2 + 0.09 * lunge + 0.07 * press - 0.05 * wind + 0.06 * dive
    p["my"] += 12.0 * coil + 8.0 * coil2 - 40.0 * lunge + 10.0 * wind - 24.0 * dive
    p["mx"] += 8.0 * coil - 16.0 * whipk * (1 - ret_t) - 6.0 * wind + 10.0 * dive
    spine(p, lean=-5.0 * coil + 9.0 * whipk * (1 - ret_t) + 5.0 * wind - 7.0 * dive,
          arc=-8.0 * lunge + 3.0 * coil - 4.0 * dive)
    p["hy"] += 6.0 * coil - 16.0 * lunge + 5.0 * wind - 10.0 * dive + wob(t, T_HIT, 0.3, 6.0, 3.0)
    p["hr"] += -4.0 * show * (1 - coil) * (1 - lunge) + 5.0 * whipk * (1 - ret_t) + wob(t, T_WHIP1, 0.4, 5.0, 3.0) \
        + 5.0 * wind - 7.0 * dive
    p["hsq"] += 0.05 * press
    # ---- tay trái: bàn → chữ W → mép xa của mâm → quất dọc mép → văng → về bàn
    gx = GRAB_X + (WHIP_X - GRAB_X) * whipk
    g = rotor_far(gx)
    coil_a = spec("t", to=mir("t", 292.0, 944.0 + 40.0 * coil2), space="v", out=-56, inn=86, k=0.55, hand=HAND_OPEN, hrot=72, hs=1.0)
    # đích cho ở CỔ TAY: lòng bàn tay (cách cổ tay ~105 px x cỡ bàn tay, dọc hướng ngón) nằm đúng trên mép mâm. Ống tay rời vai
    # chếch ra ngoài rồi vòng xuống thành một cung chữ C bên trái bảng cược (không đâm thẳng xuống giữa ngực).
    grab_a = spec("t", to=(g[0] + PALM[0], g[1] + PALM[1]), out=-38, inn=262 + 14.0 * whipk, t0=280.0, t1=420.0,
                  hand=HAND_OPEN, hrot=262, hs=GRAB_HS, hsq=0.16 * press)
    fling_a = spec("t", to=(-440.0, -420.0), out=-52, inn=295, k=0.4, hand=HAND_WAVE, hrot=208, hs=1.2)
    arm_seq(p, "t", on_table("t"),
            (coil_a, seg(t, 0.24, 0.5, ease)),
            (grab_a, strike),
            (fling_a, fling),
            (on_table("t"), ret_t))
    a = p["arm"]["t"]
    a["shr"] = (0.0, a["shr"][1] + 14.0 * coil + 7.0 * coil2 - 8.0 * lunge)
    a["whip"] = 1.0 + 0.9 * hat(t, T_WHIP1 - 0.02, T_WHIP1 + 0.03, 1.1, 1.3)
    a["lag"] = 1.0 + 0.6 * hat(t, T_WHIP1, T_WHIP1 + 0.05, 1.1, 1.3)
    a["drag"] = 0.0 if T_HIT - 0.02 <= t < T_QUAY else 0.7
    a["hrate"] = 14.0 if T_HIT - 0.12 <= t < 1.0 else 6.5
    a["hand"] = steps(t, 9, 0.26, HAND_OPEN, T_WHIP1, HAND_WAVE, 1.14, 9)
    # ---- tay phải: giơ bi khoe → giữ → rút ra sau đầu → ném chúi xuống sườn phải → về bàn
    tw = math.sin((t - 0.1) * 2 * math.pi * 3.0) * hat(t, 0.2, 0.3, 0.5, 0.6)      # xoay xoay cổ tay khoe viên bi
    show_a = spec("p", to=(296.0, 930.0 + 10.0 * coil), space="v", out=-64, inn=84, k=0.5, hand=HAND_PINCH,
                  hrot=78 + 12.0 * tw, hs=1.05)
    # cổ tay gập xuống ngay nửa đầu cú ném (ngón chĩa xuống trước khung bi rời tay). Bàn tay lật CÙNG CHIỀU với cẳng tay (cẳng tay
    # vung qua phía ngoài: lên -> phải -> xuống, tức xuôi chiều kim đồng hồ); để động cơ tự trộn 118 -> 264 thì nó đi đường ngắn
    # qua phía trái, ngược chiều cẳng tay, cổ tay bẻ ngược một khung. Hai dáng dùng chung một góc nên không còn chỗ chọn nhầm.
    hr_throw = 118.0 - 214.0 * seg(t, 1.40, 1.40 + 2 * F, ease)
    wind_a = spec("p", to=(436.0, 1004.0), space="v", out=-36, inn=100, k=0.5, hand=HAND_PINCH, hrot=hr_throw, hs=1.05)
    rel_a = spec("p", to=(318.0, 150.0 - 70.0 * over), out=-72, inn=268, k=0.4, hand=HAND_OPEN, hrot=hr_throw, hs=1.25)
    arm_seq(p, "p", on_table("p"),
            (show_a, show),
            (wind_a, seg(t, 1.16, 1.38, ease)),
            (rel_a, throw),
            (on_table("p"), ret_p))
    b = p["arm"]["p"]
    b["whip"] = 1.0 + 0.8 * hat(t, T_THA - 0.02, T_THA + 0.03, 1.66, 1.84)
    b["drag"] = 0.0 if 1.38 <= t < 1.62 else 0.5
    b["hrate"] = 22.0 if 1.38 <= t < 1.62 else 6.5
    b["hand"] = steps(t, 9, 0.06, HAND_PINCH, T_THA, HAND_OPEN, 1.8, 9)
    p["ball"] = 0.06 <= t < T_THA - 1e-6
    # ---- mặt: liếc viên bi, nhếch -> trợn nhìn xuống mâm, nghiến răng lúc quất -> chu miệng lấy đà -> mắt tròn dõi theo bi
    p["eye"] = steps(t, 2, 0.06, 10, 0.44, 1, T_HIT - 0.1, 9, 0.98, 10, 1.18, 1, T_THA, 4)
    p["eye_s"] = (-1.0 if (0.06 <= t < 0.44 or 0.98 <= t < 1.18) else 1.0, 1.0)
    p["eye_d"] = (4.0 * dive, -7.0 * lunge - 8.0 * dive)
    p["mouth"] = steps(t, 1, 0.06, 10, T_HIT - 0.1, 5, 0.98, 10, 1.18, 3, T_THA, 1)
    p["mouth_s"] = (1.0, 1.0 + 0.06 * shake(t, 15) * press)


# ---------------------------------------------------------------- rl_watch: dõi theo viên bi (game kéo thời gian theo góc bi)
WATCH_DUR = 2.0


@clip("rl_watch", WATCH_DUR, loop=True)
def c_rl_watch(t, p):
    """Dõi theo bi. KHÔNG phát theo giờ: game kéo thời gian theo góc viên bi, t ứng với bi ở góc a = 40° − 360° t / 2,0 (bi đi theo
    chiều kim đồng hồ khi t tăng; t = 0: bi ở phải, xa). Không nhún theo phách, mọi thứ là hàm tuần hoàn của góc nên khép kín.
    Chồm tới trên bàn, hai tay tì mép bàn dạng rộng, khuỷu bạnh; đầu, mắt, thân dõi theo bi: bi bên phải thì đầu dịch / nghiêng
    sang phải, mắt liếc phải; bi gần người chơi (270°) thì cúi sâu nhất, bi ở xa (90°) thì ngẩng hơn."""
    a = math.radians(40.0 - 360.0 * t / WATCH_DUR)
    cx, sy = math.cos(a), math.sin(a)
    deep = 0.5 * (1.0 - sy)            # 0 = bi ở xa, 1 = bi sát người chơi
    p["my"] += -18.0 - 22.0 * deep
    p["sq"] += 0.04 + 0.05 * deep
    p["mx"] += 18.0 * cx
    spine(p, lean=-6.0 * cx, arc=-4.0 - 4.0 * deep)
    p["hx"] += 24.0 * cx
    p["hy"] += -10.0 - 14.0 * deep
    p["hr"] += -9.0 * cx
    p["nr"] += -1.5 * cx
    p["hsq"] += 0.02 * deep
    p["wd"][1] += 0.04 + 0.02 * deep
    for s in "tp":
        side = 1.0 if s == "p" else -1.0
        near = 0.5 * (1.0 + side * cx)          # bi ở phía tay này: khuỷu tay đó bạnh thêm (dồn người sang)
        p["arm"][s]["mix"] = [(on_table(s, dx=44.0, bow=36.0 + 8.0 * deep + 8.0 * near), 1.0)]
        p["arm"][s]["shr"] = (0.0, -4.0 - 3.0 * deep)
        p["arm"][s]["hand"] = HAND_FLAT
        p["arm"][s]["drag"] = 0.0
    p["eye"] = 4
    p["eye_d"] = (11.0 * cx, -8.0 + 5.0 * sy)
    p["mouth"] = 1
    p["bow_d"] = (0.0, -2.0 - 1.5 * deep)
    p["lv2"] += -4.0 * deep


# ---------------------------------------------------------------- rl_point: chỉ ô ra
@clip("rl_point", 1.5, events=[(0.5, "chi")])
def c_rl_point(t, p):
    """Bi dừng: giơ ngón trỏ lên cạnh đầu ("a ha", 0,08 – 0,3) -> chĩa thẳng xuống bánh xe (0,36 – 0,5, sự kiện chi lúc ngón dừng),
    nhấn nhấn hai cái, mặt hí hửng "đấy, thấy chưa" -> thu tay về bàn. Ngón chỉ về phía tâm mâm, không chạm (tay vươn vừa phải)."""
    amt = 1.0 - 0.8 * hat(t, 0.0, 0.08, 1.05, 1.4, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.08, 0.1, 0.16, eout, ein)
    up = seg(t, 0.08, 0.3, back)
    top = up * (1 - seg(t, 0.36, 0.44, ein))
    jab = seg(t, 0.36, 0.5, lambda v: clamp(v) ** 1.5)
    hold = jab * (1 - seg(t, 1.0, 1.24, ease))
    ret = seg(t, 1.0, 1.32, ease)
    tap = hat(t, 0.62, 0.68, 0.7, 0.78, eout, ein) + hat(t, 0.82, 0.88, 0.9, 0.98, eout, ein)   # nhấn nhấn ngón
    p["sq"] += 0.06 * antic - 0.06 * top + 0.07 * hold
    p["my"] += -10.0 * antic + 12.0 * top - 28.0 * hold - 4.0 * tap
    spine(p, lean=3.0 * top - 2.0 * hold, arc=-6.0 * hold)
    p["hy"] += 5.0 * top - 13.0 * hold
    p["hr"] += 5.0 * top - 4.0 * hold + wob(t, 0.5, 0.36, 4.0, 3.0)
    # cổ tay gập xuống ngay nửa đầu cú chĩa (tới khung "chi" ngón đã chĩa thẳng xuống và đứng yên), lật cùng chiều với cẳng tay
    # (xuôi chiều kim đồng hồ, qua phía ngoài) như cú ném bi của rl_spin; hai dáng dùng chung một góc
    hr_pt = 86.0 - 182.0 * seg(t, 0.36, 0.44, ease)
    up_a = spec("p", to=(304.0, 1010.0), space="v", out=-56, inn=88, k=0.52, hand=HAND_POINT, hrot=hr_pt, hs=1.05)
    down_a = spec("p", to=(60.0, -150.0 - 16.0 * tap), out=-74, inn=264, k=0.36, hand=HAND_POINT, hrot=hr_pt, hs=1.4)
    arm_seq(p, "p", on_table("p"), (up_a, up), (down_a, jab), (on_table("p"), ret))
    a = p["arm"]["p"]
    a["shr"] = (0.0, a["shr"][1] + 12.0 * top - 6.0 * hold)
    a["whip"] = 1.0 + 0.7 * hat(t, 0.48, 0.52, 0.6, 0.76)
    a["drag"] = 0.0 if 0.34 <= t < 0.7 else 0.4
    a["hrate"] = 20.0 if 0.34 <= t < 0.7 else 6.5
    a["hand"] = steps(t, 9, 0.08, HAND_POINT, 1.26, 9)
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 14.0 * hold), 1.0)]
    p["eye"] = steps(t, 2, 0.04, 1, 0.38, 3, 1.2, 2)
    p["eye_d"] = (0.0, -8.0 * hold)
    p["mouth"] = steps(t, 1, 0.08, 10, 0.5, 1, 1.25, 1)
    ms = 1.0 + 0.10 * hold
    p["mouth_s"] = (ms, ms)
