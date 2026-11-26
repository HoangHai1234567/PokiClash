# Clip chung của Lão Mực (GD_Claude/31 mục 4.1, mốc D2 bản 2): kiểu ống cao su đầu thập niên 1930. File này chỉ viết DÁNG theo
# giờ; phần "cao su" (tay sợi mì có sóng, thon khi giãn, lò xo tóc / lưỡi trai / nơ, chân ghim đất) do dong_co.py lo.
#
# Số đo lấy từ tư liệu người dùng ghi (ref/, chỉ học nhịp, không chép thiết kế):
#   * Steamboat Willie (mickeydance.mp4): nhún theo phách không phải sóng sin: dập xuống 1-2 hình, giữ thấp ~2 hình, bật lên 1 hình
#     có vượt quá, rồi "giữ có trôi" tới phách sau; tay bám vật thì đầu gần như đứng yên, phần dưới sa xuống ~3 % chiều cao; động
#     tác lớn: lấy đà 2 hình (nén) -> giãn 1-2 hình -> giữ dáng 3-4 hình -> vung 2 hình (khung nhòe) -> chạm, nén quá đà 2 hình ->
#     ổn định 3 hình; thân giãn / nén tới ±25 %.
#   * Cuphead (cupheadfinalboss.mp4): tay vươn ra ngoài khung rồi đập về: cuộn lấy đà 0,47 s (nhún vai, tay chữ W, đầu thụt) ->
#     bắn ra trong 3 khung (ống chùng lượn sóng -> căng, thon còn ~60 %) -> giữ ngoài khung -> đập vào trong 4 khung (ngón đi
#     trước) -> chạm: bàn tay bẹp ~55 % rồi nhả về 70 % trong 2 khung, giữ 0,33 s -> rút 3 khung (ngón rê) -> thu tay 3 khung thành
#     sóng chùng -> ổn định có vượt quá.
# Mọi clip dài bội số nửa giây (một phách 0,5 s) và hai đầu hoà vào idle giây 0.
# Chạy: py -3 -I hoat_anh.py [tên clip ...]   (không đối số: mọi clip)
import math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dong_co import *  # noqa

IDLE_DUR = 4.0
HT = {"t": (-212.0, TABLE_Y + 22.0), "p": (212.0, TABLE_Y + 22.0)}   # hai bàn tay tì mép bàn
SG = {"t": -1, "p": 1}
# Chỗ đồ trên bàn (thế giới rig). TẠM: D3 chốt bố cục bàn thật thì sửa hai mốc này rồi nướng lại (mọi đích tay tính từ đây).
CHIP = (0.0, 120.0)             # ô cược của người chơi (chồng chip cược)
TRAY_Y = TABLE_Y - 40.0         # khay chip của nhà cái, sát mép bàn phía Lão Mực
# Bàn tay (hình trong slot ban_tay_*): 1 xoè, 2 thả lỏng, 3 nắm nhìn trước, 4 chỉ, 5 kẹp, 6 xoè vẫy, 7 vốc, 8 giơ ngón cái,
# 9 úp (ngón cái ở mép trên), 10 nắm cần gạt, 11 MỞ DỰNG ĐỨNG nhìn nghiêng từ phía mu (ngón cái trên), 12 NẮM DỰNG NGHIÊNG (ngón
# cái trên). Luật hướng bàn tay trên mặt bàn: skill animation-humanoid mục 1.
HAND_BLADE = 11                 # gạt / quây chip: bàn tay dựng đứng, lòng tay quay về phía Lão Mực, camera thấy mu bàn tay
HAND_FIST_SIDE = 12             # nện bàn: cạnh ngón út chạm bàn, ngón cái ở trên, camera thấy mu nắm tay


def mir(s, x, y):
    """Điểm cho tay bên phải người xem; tay trái lấy đối xứng."""
    return (x * SG[s], y)


def on_table(s, lift=0.0, bow=27.0, tilt=0.0, hand=9, dx=0.0):
    return spec(s, to=(HT[s][0] + dx * SG[s], HT[s][1] + lift), bow=bow, k=0.46, inn=232, hand=hand, hrot=198, tilt=tilt, hs=1.0)


# ---------------------------------------------------------------- nhịp nền
def nhip(t, p, amt=1.0, sway=1.0, hands=True):
    """Nhịp nền của mọi clip: nhún theo phách (dập - giữ - bật vượt - trôi), đổi bên mỗi phách, bụng rung trễ, đầu trễ hơn thân và
    lắc ngược pha, hai tay tì bàn nên khuỷu bạnh ra lúc dập."""
    ph = t / BEAT
    d = pulse(ph)
    d1 = pulse(ph - 0.13)     # trễ ~2 khung
    d2 = pulse(ph - 0.24)
    sw = swing(t / (2 * BEAT))
    sw1 = swing((t - 0.08) / (2 * BEAT))
    p["my"] += -15.0 * d * amt
    p["sq"] += (0.060 * d if d > 0 else 0.11 * d) * amt
    p["wd"][1] += 0.075 * d1 * amt          # bụng phình trễ
    p["wd"][2] += -0.025 * d1 * amt
    p["wd"][3] += 0.03 * d * amt
    p["mx"] += 9.0 * sw * sway
    spine(p, lean=3.2 * sw * sway, arc=2.2 * sw1 * sway)
    # đầu: trễ hơn thân (còn ở trên lúc thân đã dập, còn ở dưới lúc thân đã bật), bẹp nhẹ khi "đáp", lắc ngược pha
    p["hy"] += 10.0 * (d - d1) * amt
    p["hsq"] += 0.035 * d2 * amt
    p["hr"] += -3.4 * sw1 * sway + 1.6 * (d1 - d2) * amt
    p["nr"] += -1.2 * sw * sway
    p["bow_d"] = (0.0, -2.5 * d1 * amt)
    for s in "tp":
        a = p["arm"][s]
        a["shr"] = (0.0, (-5.0 * d + 3.0 * max(0.0, -d1) * 3) * amt)
        if hands:
            a["mix"] = [(on_table(s, bow=25.0 + 15.0 * d1 * amt), 1.0)]
    return d


def blink(p, t, t0):
    k = int(round((t - t0) * FPS))
    if 0 <= k < 5:
        sy = (0.45, 0.10, 0.10, 0.35, 0.8)[k]
        p["eye_s"] = (p["eye_s"][0], p["eye_s"][1] * sy)


def steps(t, v0, *kv):
    """Giá trị đổi theo mốc giờ: steps(t, v0, t1, v1, t2, v2...) = v của mốc cuối cùng đã qua."""
    v = v0
    for i in range(0, len(kv), 2):
        if t >= kv[i]:
            v = kv[i + 1]
    return v


def shake(t, hz=15.0):
    """Rung hai dáng: đổi dấu mỗi 1/hz giây (giữ chiêu, gồng: hai dáng lệch nhau vài độ đổi nhau mỗi 2 khung)."""
    return 1.0 if int(t * hz) % 2 == 0 else -1.0


CLIPS = {}
EVENTS = {}


def clip(name, dur, loop=False, events=()):
    def deco(f):
        CLIPS[name] = (dur, loop, f)
        if events:
            EVENTS[name] = list(events)
        return f
    return deco


# ---------------------------------------------------------------- idle
@clip("idle", IDLE_DUR, loop=True)
def c_idle(t, p):
    nhip(t, p)
    # điểm phá nhịp: liếc trái rồi liếc phải (phách 3-4), chớp mắt, tay phải gõ bàn ba nhịp cuối vòng
    if 1.0 <= t < 1.5:
        p["eye"] = 10
        p["mouth"] = 10
        p["hr"] += 3.0 * hat(t, 1.0, 1.08, 1.42, 1.5)
    elif 1.5 <= t < 2.0:
        p["eye"] = 10
        p["eye_s"] = (-1.0, 1.0)
        p["mouth"] = 10
        p["hr"] += -3.0 * hat(t, 1.5, 1.58, 1.92, 2.0)
    blink(p, t, 0.55)
    blink(p, t, 2.62)
    # gõ ngón ba cái (đập xuống ở giây 2,5 / 3,0 / 3,5): nhấc lên ở nửa sau phách, đập xuống đúng phách (như bàn chân gõ nhịp
    # của tư liệu); nghỉ nửa giây cuối để giây 0 là dáng nghỉ
    if 2.0 <= t < 3.5:
        ph = (t / BEAT) % 1.0
        up = ease(clamp((ph - 0.36) / 0.30)) * (1 - ein(clamp((ph - 0.80) / 0.16)))
        a = p["arm"]["p"]
        d1 = pulse(t / BEAT - 0.13)
        a["mix"] = [(on_table("p", lift=32.0 * up, bow=25.0 + 15.0 * d1 + 10 * up, tilt=-28.0 * up), 1.0)]
        a["drag"] = 0.3


# ---------------------------------------------------------------- greet
@clip("greet", 2.0, events=[(0.42, "cham_mu")])
def c_greet(t, p):
    amt = 1.0 - 0.75 * hat(t, 0.0, 0.1, 1.45, 1.8, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.14, 0.2, 0.3, eout, ein)          # nhún lấy đà
    up = seg(t, 0.2, 0.36, back)                             # bật lên, tay tới vành lưỡi trai
    hold = up * (1 - seg(t, 1.1, 1.38, ease))
    p["my"] += -20.0 * antic + 12.0 * hold
    p["sq"] += 0.11 * antic - 0.075 * hold * (1 - 0.5 * seg(t, 0.45, 0.7))
    bowk = hat(t, 0.46, 0.66, 1.0, 1.25, ease, ease)         # cúi chào sau khi chạm mũ
    spine(p, lean=-7.0 * bowk, arc=-9.0 * bowk)
    p["hr"] += -12.0 * bowk + wob(t, 0.36, 0.4, 4.0, 3.0)
    p["hy"] += -10.0 * bowk
    p["my"] += -10.0 * bowk
    # tay phải: rời bàn -> vành lưỡi trai (bám theo đầu) -> vẫy nhẹ -> về bàn
    brim = spec("p", to=(262.0, 1196.0), space="h", bow=-40.0, k=0.5, hand=5, hrot=118, hs=1.0)
    flick = spec("p", to=(330.0, 1120.0), space="h", bow=-30.0, k=0.5, hand=6, hrot=70, hs=1.05)
    arm_seq(p, "p", on_table("p"),
            (brim, seg(t, 0.16, 0.38, back)),
            (flick, seg(t, 1.1, 1.24, eout)),
            (on_table("p"), seg(t, 1.36, 1.7, ease)))
    p["arm"]["p"]["whip"] = 1.4
    p["arm"]["p"]["hand"] = steps(t, 9, 0.12, 5, 1.1, 6, 1.6, 9)
    # nhấc lưỡi trai
    tip = hat(t, 0.42, 0.56, 1.0, 1.14, back, ein)
    p["lv_r"] += 15.0 * tip + wob(t, 1.14, 0.45, 5.0, 3.0)
    p["lv_d"] = (6.0 * tip, 20.0 * tip)
    p["lv2"] += 8.0 * tip
    p["eye"] = steps(t, 2, 0.2, 1, 0.46, 8, 1.2, 2)
    p["mouth"] = 1
    p["mouth_s"] = (1.0 + 0.12 * hold, 1.0 + 0.12 * hold)
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 20.0 * antic - 8 * hold), 1.0)]


# ---------------------------------------------------------------- talk
@clip("talk", 2.0, loop=True)
def c_talk(t, p):
    nhip(t, p, amt=0.7, sway=0.8)
    shapes = [9, 10, 3, 9, 1, 10, 9, 2, 9, 3, 10, 1, 9, 10, 9, 1, 3, 9, 10, 2, 9, 1, 10, 1]   # 12 hình / giây
    k = int(t * 12) % len(shapes)
    p["mouth"] = shapes[k]
    p["mouth_s"] = (1.0, 1.0 + 0.10 * (1 if k % 2 == 0 else -0.5))
    # đầu gật theo âm tiết, nghiêng theo câu
    p["hr"] += 4.0 * math.sin(t * 2 * math.pi / 2.0) + 2.0 * (1 if k % 4 < 2 else -1)
    p["hy"] += 4.0 * (1 if k % 2 == 0 else 0)
    p["eye"] = 1 if (0.5 <= t < 1.0) else 2
    blink(p, t, 1.4)
    # tay phải khua theo câu: vẽ số 8 trước ngực, đổi dáng xoè / chỉ
    u = t / 2.0 * 2 * math.pi
    gx = 268.0 + 40.0 * math.sin(u)
    gy = 842.0 + 34.0 * math.sin(2 * u + 0.6)
    g = spec("p", to=(gx, gy), space="v", out=-64, inn=82 + 10 * math.sin(u), k=0.5, hand=1, hrot=78 + 22 * math.sin(u + 1.0), hs=1.0)
    p["arm"]["p"]["mix"] = [(g, 1.0)]
    p["arm"]["p"]["hand"] = 4 if 0.75 <= t < 1.25 else 1


# ---------------------------------------------------------------- bet_watch
@clip("bet_watch", 2.0)
def c_bet(t, p):
    amt = 1.0 - 0.6 * hat(t, 0.0, 0.1, 1.5, 1.8, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    pop = hat(t, 0.0, 0.1, 0.16, 0.26, eout, ease)          # giật mình vươn lên nhìn
    look = hat(t, 0.2, 0.42, 1.42, 1.7, back, ease)         # chồm xuống ngó chip
    p["my"] += 14.0 * pop - 24.0 * look
    p["sq"] += -0.09 * pop + 0.07 * look
    p["hy"] += -16.0 * look
    p["hsq"] += -0.08 * pop
    spine(p, arc=-4.0 * look)
    rub = hat(t, 0.4, 0.5, 1.38, 1.5, ease, ease)
    w = math.sin(t * 2 * math.pi * 5.0) * rub               # xoa tay 5 lần / giây
    for s in "tp":
        tog = spec(s, to=mir(s, 30.0, 655.0 + 15.0 * w * SG[s]), bow=58.0, k=0.62, hand=2, hrot=140, hs=1.0)
        arm_seq(p, s, on_table(s), (tog, seg(t, 0.22, 0.46, back)), (on_table(s), seg(t, 1.45, 1.78, ease)))
        p["arm"][s]["shr"] = (0.0, 6.0 * look + 4.0 * w * SG[s])
        p["arm"][s]["drag"] = 0.2
    p["wd"][3] += 0.04 * abs(w)
    p["bow_r"] = 4.0 * w
    p["eye"] = steps(t, 2, 0.03, 4, 0.24, 3, 1.5, 2)
    p["eye_d"] = (0.0, -6.0 * look)
    p["mouth"] = steps(t, 1, 0.9, 7, 1.3, 1)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.22, 2, 1.62, 9)


# ---------------------------------------------------------------- take
@clip("take", 2.5, events=[(0.54, "cham_chip"), (1.3, "vo_xong")])
def c_take(t, p):
    """Bản 3 (người dùng: "hơi lố, vòng tay vừa thôi, không cần tràn ngoài cam"): giữ mạch chữ W lấy đà -> vươn -> chụp xuống chồng
    chip -> quơ về khay, nhưng hai tay luôn trong khung, vươn vừa đủ tới ô cược, vòng quơ vừa phải."""
    amt = 1.0 - hat(t, 0.0, 0.08, 2.0, 2.35, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    coil = hat(t, 0.02, 0.28, 0.42, 0.48, ease, ein)
    coil2 = hat(t, 0.26, 0.38, 0.42, 0.48, ease, ein)        # cuộn cao thêm một nấc ngay trước khi ra tay
    strike = seg(t, 0.42, 0.54, lambda u: clamp(u) ** 1.6)
    hit = hat(t, 0.54, 0.56, 0.78, 0.92, lin, ease)
    rake = seg(t, 0.84, 1.3, ease)
    back_ = seg(t, 1.3, 1.56, eout)
    dust = hat(t, 1.5, 1.6, 1.98, 2.1, ease, ease)
    lunge = hat(t, 0.44, 0.54, 0.8, 0.95, eout, ease)         # chồm theo tay
    p["sq"] += 0.09 * coil + 0.05 * coil2 + 0.08 * lunge + 0.08 * hat(t, 0.54, 0.57, 0.62, 0.78, lin, ease) \
        - 0.07 * hat(t, 0.9, 1.12, 1.3, 1.5, ease, ease)
    p["my"] += -7.0 * coil - 7.0 * coil2 - 22.0 * lunge + 10.0 * rake * (1 - back_)
    p["hy"] += -10.0 * coil - 7.0 * coil2 - 8.0 * lunge + wob(t, 0.54, 0.4, 7.0, 3.0)
    p["hr"] += wob(t, 0.54, 0.45, 5.0, 3.0)
    spine(p, arc=4.0 * rake * (1 - back_))
    p["hsq"] += 0.05 * hat(t, 0.54, 0.57, 0.62, 0.78, lin, ease) - 0.04 * rake * (1 - back_)
    for s in "tp":
        coil_a = spec(s, to=mir(s, 292.0, 944.0 + 40.0 * coil2), space="v", out=-56, inn=86, k=0.55, hand=1, hrot=72, hs=1.0)
        # vươn thành một cung ra ngoài rồi quặp vào hai bên chồng chip (đỉnh cung ~ x 360, khung nhìn ±480)
        # Bản 4: hai bàn tay DỰNG ĐỨNG (ngón cái ở trên, lòng tay quay về phía Lão Mực), đầu ngón chụm nhau ở phía người chơi
        # thành "mái nhà khép kín" quây lấy chồng chip, rồi kéo cả mái về khay. Nhìn từ phía Lão Mực là chữ Λ; trên màn hình
        # (camera ở ghế người chơi) cổ tay ở trên, đầu ngón chụm ở dưới, chồng chip nằm trong lòng mái.
        in_a = spec(s, to=mir(s, 215.0, CHIP[1] + 104.0), out=-14, inn=218, k=0.45, hand=HAND_BLADE, hrot=218, hs=1.2,
                    hsq=0.16 * hat(t, 0.54, 0.56, 0.6, 0.72, lin, ease))
        tray_a = spec(s, to=mir(s, 228.0, TRAY_Y + 70.0), out=-24, inn=200, k=0.6, hand=HAND_BLADE, hrot=200, hs=1.0)
        dust_a = spec(s, to=mir(s, 40.0, 668.0 + 24.0 * math.sin(t * 2 * math.pi * 4.0) * SG[s] * dust),
                      bow=56.0, k=0.6, hand=9, hrot=150, hs=1.0)
        arm_seq(p, s, on_table(s),
                (coil_a, seg(t, 0.02, 0.28, ease)),
                (in_a, strike),
                (tray_a, rake),
                (dust_a, seg(t, 1.32, 1.58, eout)),
                (on_table(s), seg(t, 2.0, 2.32, ease)))
        a = p["arm"][s]
        a["shr"] = (0.0, a["shr"][1] + 14.0 * coil + 7.0 * coil2 - 6.0 * hit)
        a["hand"] = steps(t, 9, 0.06, 1, 0.44, HAND_BLADE, 1.44, 9)
    p["eye"] = steps(t, 2, 0.04, 3, 0.54, 4, 0.62, 6, 1.5, 2)
    p["eye_d"] = (0.0, -6.0 * lunge)
    p["mouth"] = steps(t, 1, 0.3, 7, 0.54, 2, 1.5, 1)
    p["mouth_s"] = (1.0, 1.0 + 0.08 * shake(t, 10) * rake * (1 - back_))


# ---------------------------------------------------------------- pay
@clip("pay", 2.5, events=[(1.3, "tra_chip")])
def c_pay(t, p):
    amt = 1.0 - 0.8 * hat(t, 0.0, 0.1, 1.85, 2.2, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    reluct = hat(t, 0.0, 0.3, 1.3, 1.6, ease, ease)          # tiếc: ngả người né, quay mặt
    reach = seg(t, 0.34, 0.6, back)
    push = seg(t, 0.62, 1.3, lin)
    # đẩy ngập ngừng: hai lần khựng
    pk = 0.5 * ease(clamp(push / 0.38)) + 0.3 * ease(clamp((push - 0.5) / 0.3)) + 0.2 * ease(clamp((push - 0.88) / 0.12))
    flick = hat(t, 1.3, 1.36, 1.4, 1.5, eout, ease)
    ret = seg(t, 1.46, 1.8, eout)
    sigh = hat(t, 1.6, 1.85, 2.0, 2.3, ease, ease)
    spine(p, lean=6.0 * reluct, arc=5.0 * reluct)
    p["mx"] += -10.0 * reluct
    p["my"] += 5.0 * reluct - 14.0 * sigh
    p["sq"] += -0.03 * reluct + 0.08 * sigh
    p["hr"] += 9.0 * reluct + 1.3 * shake(t, 12) * push * (1 - ret) + 6.0 * sigh
    p["hy"] += -10.0 * sigh
    # Bản 4: gạt chip bằng BÀN TAY DỰNG ĐỨNG (ngón cái ở trên, lòng tay quay vào trong, camera thấy mu bàn tay), không còn một
    # ngón chỉ xuống đẩy. Bàn tay nằm ngang chĩa vào giữa, mép ngón út tì bàn ngay sau chồng chip, đẩy cả chồng về ô cược.
    curl = spec("p", to=(215.0, 700.0), bow=58.0, k=0.6, hand=HAND_BLADE, hrot=196, hs=1.0)
    chip = spec("p", to=(166.0, TRAY_Y + 77.0), out=-8, inn=186, k=0.62, hand=HAND_BLADE, hrot=184, hs=1.0)
    give = spec("p", to=(172.0 + 5.0 * shake(t, 12) * (1 - ret), CHIP[1] + 157.0 - 30.0 * flick), out=-6, inn=188, k=0.6,
                hand=HAND_BLADE, hrot=188, hs=1.2)
    arm_seq(p, "p", on_table("p"),
            (curl, seg(t, 0.06, 0.3, ease)),
            (chip, reach),
            (give, pk),
            (on_table("p"), ret))
    a = p["arm"]["p"]
    a["whip"] = 1.0 + 1.3 * hat(t, 1.46, 1.5, 1.8, 2.0)
    a["lag"] = 1.0 + 0.8 * hat(t, 1.46, 1.5, 1.8, 2.0)
    a["drag"] = 0.5
    a["hand"] = steps(t, 9, 0.08, HAND_BLADE, 1.72, 9)
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 14.0 * reluct), 1.0)]
    p["eye"] = steps(t, 2, 0.1, 7, 1.9, 2)
    p["eye_d"] = (0.0, -3.0 * reluct)
    if 0.7 <= t < 1.25:
        blink(p, t, 0.9)
    p["mouth"] = steps(t, 1, 0.1, 6, 1.6, 3, 2.0, 1)
    p["mouth_s"] = (1.0 + 0.06 * shake(t, 12) * reluct, 1.0 + 0.05 * shake(t + 0.04, 12) * reluct + 0.25 * sigh)
    p["lv_r"] += -5.0 * sigh


# ---------------------------------------------------------------- react_win_small
@clip("react_win_small", 1.5)
def c_win_small(t, p):
    k = hat(t, 0.0, 0.1, 1.0, 1.3, ease, ease)
    nhip(t * (1 + 0.0), p, amt=1.0 - 0.3 * k, sway=1.0 - k)
    jolt = hat(t, 0.0, 0.07, 0.1, 0.2, eout, ease)
    pose = seg(t, 0.12, 0.3, back) * (1 - seg(t, 1.02, 1.3, ease))
    p["my"] += 12.0 * jolt
    p["sq"] += -0.07 * jolt + 0.03 * pose
    spine(p, lean=-5.0 * pose, ess=4.0 * pose)
    p["hr"] += -11.0 * pose + wob(t, 0.3, 0.4, 4.0, 3.0)
    for s in "tp":
        hip = spec(s, to=mir(s, 246.0, 604.0), bow=58.0, k=0.62, hand=3, hrot=186, hs=1.0)   # chống nạnh
        arm_seq(p, s, on_table(s), (hip, seg(t, 0.1, 0.3, back)), (on_table(s), seg(t, 1.02, 1.32, ease)))
        p["arm"][s]["shr"] = (0.0, p["arm"][s]["shr"][1] + 8.0 * pose)
    tsk = 1 if (0.5 <= t < 0.58 or 0.74 <= t < 0.82) else 0   # chép miệng hai cái
    p["eye"] = steps(t, 2, 0.03, 5, 0.12, 9, 0.5, 10, 1.1, 2)
    p["mouth"] = 3 if tsk else steps(t, 1, 0.12, 10, 1.15, 1)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.1, 3, 1.2, 9)
    p["mouth_r"] = -8.0 * pose
    p["hy"] += 5.0 * tsk


# ---------------------------------------------------------------- react_win_big
@clip("react_win_big", 2.5, events=[(0.1, "soc")])
def c_win_big(t, p):
    amt = 1.0 - hat(t, 0.0, 0.05, 1.9, 2.3, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.07, 0.09, 0.14, eout, ein)
    boom = seg(t, 0.1, 0.19, eout)
    shock = boom * (1 - seg(t, 0.85, 1.15, ease))
    sag = hat(t, 0.95, 1.25, 1.7, 2.1, ease, ease)
    sh = shake(t, 15) * shock * (1 - seg(t, 0.2, 0.85, lin) * 0.6)
    p["sq"] += 0.17 * antic - 0.14 * shock * (1 - 0.45 * seg(t, 0.22, 0.6)) + 0.09 * sag + 0.012 * sh
    p["my"] += -24.0 * antic + 14.0 * shock * (1 - 0.5 * seg(t, 0.22, 0.6)) - 16.0 * sag
    p["hsq"] += 0.10 * antic - 0.24 * shock * (1 - 0.25 * seg(t, 0.22, 0.6)) + 0.03 * sag
    p["hy"] += 8.0 * shock - 12.0 * sag
    p["hr"] += 1.5 * sh + 7.0 * sag * math.sin((t - 1.0) * 2 * math.pi * 1.4)   # choáng: lắc lư
    spine(p, lean=0.8 * sh, ess=5.0 * sag * math.sin((t - 1.0) * 2 * math.pi * 1.4))
    # lưỡi trai bật lên, xoay, rơi lại đầu rồi nảy
    fly = seg(t, 0.1, 0.34, eout) * (1 - seg(t, 0.48, 0.86, ein))
    p["lv_d"] = (18.0 * fly, 190.0 * fly + wob(t, 0.86, 0.3, 10.0, 3.0))
    p["lv_r"] += 34.0 * fly + wob(t, 0.86, 0.45, 9.0, 3.0)
    p["lv_free"] = 1.0 - fly
    p["hsq"] += 0.07 * hat(t, 0.86, 0.9, 0.93, 1.05, lin, ease)
    p["chom"] = [-10.0 * shock, -14.0 * shock, -18.0 * shock]            # tóc dựng
    for s in "tp":
        up = spec(s, to=mir(s, 356.0 + 10.0 * sh, 1190.0), bow=-22.0, k=0.45, hand=6, hrot=78, hs=1.15)
        # tay rũ: thả phịch xuống bàn, úp, vẫn chĩa vào giữa (ngón cái phía gần người), hai tay dạng rộng hơn dáng nghỉ
        limp = on_table(s, dx=58.0, bow=46.0, tilt=-8.0)
        arm_seq(p, s, on_table(s), (up, seg(t, 0.09, 0.2, back)), (limp, seg(t, 0.92, 1.2, ein)),
                (on_table(s), seg(t, 1.9, 2.25, ease)))
        a = p["arm"][s]
        a["whip"] = 1.6
        a["lag"] = 1.4
        a["shr"] = (0.0, a["shr"][1] + 18.0 * shock - 10.0 * sag)
    p["eye"] = steps(t, 2, 0.03, 6, 0.1, 5, 1.05, 7, 2.0, 2)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.09, 6, 1.0, 9)
    es = 1.0 + 0.30 * shock * (1 - 0.3 * seg(t, 0.2, 0.5)) + 0.05 * sh
    p["eye_s"] = (es, es)
    p["eye_d"] = (0.0, 34.0 * shock)
    p["mouth"] = steps(t, 1, 0.03, 5, 0.1, 4, 1.05, 6, 2.0, 1)
    ms = 1.0 + 0.04 * sh
    p["mouth_s"] = (ms, ms - 0.05 * shock)
    p["mouth_d"] = (0.0, 8.0 * shock)
    if 1.3 <= t < 1.9:
        blink(p, t, 1.5)
    p["bw"] = 22.0 * shock


# ---------------------------------------------------------------- react_lose (người chơi thua: Lão Mực cười)
@clip("react_lose", 2.0)
def c_lose(t, p):
    amt = 1.0 - hat(t, 0.0, 0.08, 1.5, 1.8, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.1, 0.13, 0.2, eout, ein)
    back_ = seg(t, 0.14, 0.3, back)
    laugh = back_ * (1 - seg(t, 1.42, 1.72, ease))
    ha = math.sin((t - 0.3) * 2 * math.pi * 4.5)             # "ha ha ha" 4,5 nhịp / giây
    ha_sq = clamp(ha * 1.25, -1.0, 1.0)
    p["sq"] += 0.12 * antic - 0.10 * laugh + 0.03 * ha_sq * laugh
    p["my"] += -16.0 * antic + 14.0 * laugh + 5.0 * ha_sq * laugh
    spine(p, lean=7.0 * laugh, arc=10.0 * laugh)
    p["hr"] += 15.0 * laugh + 2.5 * ha_sq * laugh
    p["hy"] += 8.0 * laugh
    p["hsq"] += -0.05 * laugh + 0.03 * ha_sq * laugh
    p["wd"][1] += 0.11 * ha_sq * laugh                        # bụng rung
    p["wd"][2] += -0.05 * ha_sq * laugh
    for s in "tp":
        belly = spec(s, to=mir(s, 176.0, 640.0 + 9.0 * ha_sq * laugh), space="b", bow=66.0, k=0.62, hand=2, hrot=214, hs=1.0)
        arm_seq(p, s, on_table(s), (belly, seg(t, 0.12, 0.32, back)), (on_table(s), seg(t, 1.45, 1.78, ease)))
        a = p["arm"][s]
        a["shr"] = (0.0, a["shr"][1] + (10.0 + 7.0 * ha_sq) * laugh)
        a["drag"] = 0.2
    p["eye"] = steps(t, 2, 0.03, 3, 0.14, 6, 1.55, 2)
    p["mouth"] = steps(t, 1, 0.14, 2, 1.5, 9, 1.65, 1)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.12, 2, 1.62, 9)
    p["mouth_s"] = (1.0 + 0.10 * laugh, 1.0 + 0.10 * laugh + 0.10 * ha_sq * laugh)
    p["bow_r"] = 3.0 * ha_sq * laugh
    p["bw"] = 8.0 * ha_sq * laugh


# ---------------------------------------------------------------- react_push (hoà)
@clip("react_push", 1.5)
def c_push(t, p):
    amt = 1.0 - 0.8 * hat(t, 0.0, 0.08, 0.95, 1.25, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.1, 0.12, 0.2, eout, ein)
    up = seg(t, 0.14, 0.3, back)
    shrug = up * (1 - seg(t, 0.8, 0.92, ein))
    drop = hat(t, 0.86, 0.94, 0.98, 1.2, lin, ease)
    p["sq"] += 0.07 * antic - 0.05 * shrug + 0.07 * drop
    p["my"] += -10.0 * antic + 8.0 * shrug - 10.0 * drop
    p["hy"] += -16.0 * shrug                                   # đầu thụt giữa hai vai
    p["hr"] += 9.0 * shrug + wob(t, 0.92, 0.35, 3.0, 3.0)
    spine(p, lean=2.0 * shrug)
    for s in "tp":
        palm = spec(s, to=mir(s, 262.0, 850.0), bow=-58.0, k=0.56, hand=1, hrot=44, hs=1.05)
        arm_seq(p, s, on_table(s), (palm, seg(t, 0.12, 0.3, back)), (on_table(s), seg(t, 0.82, 1.12, ease)))
        a = p["arm"][s]
        a["shr"] = (0.0, a["shr"][1] + 26.0 * shrug - 8.0 * drop)
        a["whip"] = 1.0
    p["eye"] = steps(t, 2, 0.1, 1, 0.5, 10, 0.95, 2)
    p["mouth"] = steps(t, 1, 0.1, 6, 0.55, 3, 0.95, 1)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.12, 1, 1.0, 9)
    p["mouth_r"] = 6.0 * shrug
    if 0.5 <= t < 0.7:
        blink(p, t, 0.5)


# ---------------------------------------------------------------- grumpy
@clip("grumpy", 2.5, events=[(0.56, "dap_ban")])
def c_grumpy(t, p):
    amt = 1.0 - hat(t, 0.0, 0.08, 1.8, 2.2, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    antic = hat(t, 0.0, 0.08, 0.1, 0.16, eout, ein)
    raise_ = seg(t, 0.1, 0.34, back)
    top = raise_ * (1 - seg(t, 0.46, 0.56, ein))             # giơ nắm tay cao, giữ, run
    slam = seg(t, 0.46, 0.56, ein)
    hit = hat(t, 0.56, 0.58, 0.64, 0.86, lin, eout)           # thân bẹp
    reb = hat(t, 0.62, 0.72, 0.74, 0.84, eout, ein)           # nắm tay nảy lên rồi rơi lại
    fume = seg(t, 0.8, 0.95) * (1 - seg(t, 1.55, 1.85, ease))
    thump = hat(t, 1.16, 1.2, 1.22, 1.36, lin, eout)          # dằn thêm một cái
    sh = shake(t, 15)
    p["sq"] += 0.08 * antic - 0.13 * top + 0.24 * hit + 0.05 * fume + 0.08 * thump
    p["my"] += -10.0 * antic + 20.0 * top - 34.0 * hit - 8.0 * fume - 10.0 * thump
    p["hsq"] += -0.07 * top + 0.16 * hit + 0.05 * thump
    p["hy"] += 8.0 * top - 4.0 * hit - 8.0 * fume
    p["hr"] += 1.6 * sh * (top + fume) + wob(t, 0.58, 0.4, 5.0, 3.0)
    spine(p, lean=0.9 * sh * (top + fume))
    p["wd"][1] += 0.10 * hit
    p["lv_d"] = (0.0, 26.0 * hat(t, 0.57, 0.63, 0.66, 0.8, eout, ein))     # lưỡi trai nảy khỏi đầu
    p["lv_r"] += -6.0 * fume
    p["chom"] = [-6.0 * fume, -8.0 * fume, -10.0 * fume]
    for s in "tp":
        hi = spec(s, to=mir(s, 215.0 + 6.0 * sh * top, 1315.0), bow=-26.0, k=0.45, hand=HAND_FIST_SIDE, hrot=95, hs=1.15)
        fist = spec(s, to=mir(s, 286.0, TABLE_Y + 36.0 + 46.0 * reb + (24.0 * hat(t, 1.06, 1.16, 1.16, 1.2, eout, ein) if s == "p" else 0.0)),
                    out=-18, inn=186, k=0.62, hand=HAND_FIST_SIDE, hrot=182, hs=1.12,
                    hsq=-0.20 * hat(t, 0.56, 0.58, 0.6, 0.7, lin, ease) - (0.16 * thump if s == "p" else 0.0))
        hi["hrot"] = 95 + 87 * seg(t, 0.44, 0.52, ease)       # cổ tay xoay 90 độ ngay đầu cú nện
        arm_seq(p, s, on_table(s), (hi, seg(t, 0.08, 0.34, back)), (fist, slam), (on_table(s), seg(t, 1.85, 2.1, ease)))
        a = p["arm"][s]
        a["shr"] = (0.0, a["shr"][1] + 14.0 * top + 12.0 * fume - 10.0 * hit)
        a["hrate"] = 16.0 if 0.44 <= t < 0.9 else 6.5        # nắm tay xoay ngang kịp trước khung chạm
        a["drag"] = 0.0 if 0.44 <= t < 0.9 else 1.0
    p["eye"] = steps(t, 2, 0.05, 9, 1.8, 2)
    p["eye_s"] = (1.0 + 0.10 * fume, 1.0 + 0.10 * fume)
    p["mouth"] = steps(t, 1, 0.05, 5, 1.75, 3, 2.0, 1)
    for s in "tp":
        p["arm"][s]["hand"] = steps(t, 9, 0.08, HAND_FIST_SIDE, 1.98, 9)
    p["mouth_s"] = (1.0 + 0.05 * sh * fume, 1.0 + 0.08 * hit)


# ---------------------------------------------------------------- sulk
@clip("sulk", 2.5)
def c_sulk(t, p):
    amt = 1.0 - 0.85 * hat(t, 0.0, 0.2, 1.9, 2.25, ease, ease)
    nhip(t, p, amt=amt, sway=amt)
    droop = hat(t, 0.0, 0.5, 1.85, 2.2, ease, ease)
    sigh = hat(t, 0.5, 0.75, 0.95, 1.25, ease, ease)
    p["sq"] += 0.11 * droop + 0.04 * sigh
    p["my"] += -18.0 * droop - 6.0 * sigh
    spine(p, lean=5.0 * droop, arc=9.0 * droop)
    p["hr"] += 13.0 * droop
    p["hy"] += -12.0 * droop
    p["hsq"] += 0.04 * droop
    # lưỡi trai lệch có chủ ý nhưng phải BÁM đầu: xoay quanh chốt ở bên phải đầu nên xoay nhiều thì đầu đai bên trái (nút vàng)
    # nhấc khỏi đầu ~57 px (bản 2 xoay 17 độ: mũ trông như tuột ra). Chỉ xoay 7 độ, phần "xị" dồn vào vành cụp xuống.
    p["lv_r"] += -7.0 * droop + wob(t, 2.2, 0.3, 3.0, 3.0)
    p["lv_d"] = (-4.0 * droop, -5.0 * droop)
    p["lv2"] += -20.0 * droop
    p["chom"] = [-4.0 * droop, -6.0 * droop, -8.0 * droop]      # chỏm tóc rũ
    wave_k = hat(t, 0.7, 0.95, 1.75, 1.95, ease, ease)
    wv = math.sin((t - 0.9) * 2 * math.pi * 2.5)
    wave = spec("p", to=(280.0 + 16.0 * wv * wave_k, 848.0), space="v", out=-64, inn=84, k=0.5, hand=6,
                hrot=90 - 34 * wv * wave_k, hs=1.0)
    arm_seq(p, "p", on_table("p"), (wave, seg(t, 0.62, 0.95, ease)), (on_table("p"), seg(t, 1.8, 2.15, ease)))
    a = p["arm"]["p"]
    a["drag"] = 0.4
    p["arm"]["t"]["mix"] = [(on_table("t", bow=25.0 + 16.0 * droop), 1.0)]
    p["arm"]["t"]["shr"] = (0.0, -8.0 * droop)
    p["eye"] = steps(t, 2, 0.12, 7, 2.0, 2)
    p["mouth"] = steps(t, 1, 0.12, 6, 0.6, 3, 0.95, 6, 1.95, 1)
    a["hand"] = steps(t, 9, 0.66, 6, 2.0, 9)
    p["mouth_s"] = (1.0, 1.0 + 0.3 * sigh)
    if 1.2 <= t < 1.5:
        blink(p, t, 1.25)


# ---------------------------------------------------------------- D3: lều Đêm Bài (clip_d3.py: deal, deal_self, peek, reveal, bust_self)
import clip_d3  # noqa: E402,F401


# ---------------------------------------------------------------- D4: lều Vòng Xoay (clip_d4.py: rl_invite, rl_no_more, rl_spin, rl_watch, rl_point)
import clip_d4  # noqa: E402,F401


# ---------------------------------------------------------------- D5: lều Hội Máy Quả (clip_d5.py: sl_pull; máy quả ở ArtGen/Casino/may_qua)
import clip_d5  # noqa: E402,F401


# ---------------------------------------------------------------- nướng
def pose_of(fn, t):
    p = base_pose()
    fn(t, p)
    return p


def to_frames(out):
    """[(t, ch, att)] -> (danh sách t, {kênh: [giá trị theo khung]}, {slot: [tên theo khung]})."""
    ts = [o[0] for o in out]
    ch = {}
    for _, c, _ in out:
        for k in c:
            ch.setdefault(k, [])
    for _, c, _ in out:
        for k in ch:
            ch[k].append(tuple(c.get(k, DEFAULT[k[1]])))
    # góc: đưa cả kênh về nhánh có khung đầu nằm trong (−180, 180] (mọi clip mở đầu ở cùng dáng idle nên cùng nhánh; không thì
    # số có thể lệch nhau đúng 360 độ giữa hai clip dù hình trùng)
    for k, vals in ch.items():
        if k[1] == "rotate":
            off = 360.0 * round(vals[0][0] / 360.0)
            if off:
                ch[k] = [(v[0] - off,) for v in vals]
    att = {}
    for _, _, a in out:
        for k, v in a.items():
            att.setdefault(k, []).append(v)
    return ts, ch, att


_IDLE = None


def idle_frames():
    global _IDLE
    if _IDLE is None:
        f = CLIPS["idle"][2]
        _, out = simulate(lambda t: pose_of(f, t % IDLE_DUR), -2 * IDLE_DUR, IDLE_DUR)
        ts, ch, att = to_frames(out)
        close_loop(ts, ch, IDLE_DUR, "idle")
        _IDLE = (ts, ch, att)
    return _IDLE


def close_loop(ts, ch, dur, name):
    """Vòng lặp: khung cuối phải trùng khung đầu; sai số còn lại (lò xo chưa vào nhịp hẳn) dồn đều vào 0,25 s cuối."""
    worst = 0.0
    for k, vals in ch.items():
        d = tuple(vals[0][j] - vals[-1][j] for j in range(len(vals[0])))
        worst = max(worst, max(abs(x) for x in d))
        for i, t in enumerate(ts):
            w = ease((t - (dur - 0.25)) / 0.25)
            if w > 0:
                vals[i] = tuple(vals[i][j] + d[j] * w for j in range(len(d)))
    print(f"  {name}: lệch đầu / cuối vòng trước khi khép {worst:.2f}")


def bake(name):
    dur, loop, fn = CLIPS[name]
    if name == "idle":
        return idle_frames()
    if loop:
        _, out = simulate(lambda t: pose_of(fn, t % dur), -2 * dur, dur)
        ts, ch, att = to_frames(out)
        close_loop(ts, ch, dur, name)
        return ts, ch, att
    idle_fn = CLIPS["idle"][2]
    _, out = simulate(lambda t: pose_of(idle_fn, t % IDLE_DUR) if t < 0 else pose_of(fn, t), -2.0, dur)
    ts, ch, att = to_frames(out)
    its, ich, iatt = idle_frames()
    n_idle = len(its) - 1
    n = len(ts) - 1
    w0, w1 = 0.0, 0.0
    for k, vals in ch.items():
        iv = ich.get(k)
        for i, t in enumerate(ts):
            ws = 1.0 - ease(t / 0.1)                     # đầu clip: hoà từ idle giây 0
            we = ease((t - (dur - 0.3)) / 0.3)           # cuối clip: hoà về idle giây 0
            if ws <= 0 and we <= 0:
                continue
            def idle_at(j):
                return iv[j % n_idle] if iv else DEFAULT[k[1]]
            v = vals[i]
            # góc: hoà theo đường ngắn nhất (bàn tay có thể đã quay dư trọn một vòng so với idle sau một cú vung: hình trùng
            # nhưng số lệch 360; hoà thẳng số thì bàn tay quay tít một vòng ở cuối clip)
            dif = (lambda a_, b_: wrap180(b_ - a_)) if k[1] == "rotate" else (lambda a_, b_: b_ - a_)
            if ws > 0:
                b = idle_at(i)
                w0 = max(w0, max(abs(dif(v[j], b[j])) for j in range(len(v))) if i == 0 else 0)
                v = tuple(v[j] + dif(v[j], b[j]) * ws for j in range(len(v)))
            if we > 0:
                b = idle_at(i - n)
                if i == n - 5:
                    w1 = max(w1, max(abs(dif(v[j], b[j])) for j in range(len(v))))
                v = tuple(v[j] + dif(v[j], b[j]) * we for j in range(len(v)))
            vals[i] = v
    for slot, seq in att.items():
        seq[-1] = iatt[slot][0]
    print(f"  {name}: lệch so với idle ở khung 0: {w0:.2f}; ở 0,3 s cuối trước khi hoà: {w1:.2f}")
    return ts, ch, att


def ops_for(name):
    dur, loop, _ = CLIPS[name]
    ts, ch, att = bake(name)
    L = [f"anim.add {name} dur={dur} loop={'true' if loop else 'false'}"]
    nkeys = 0
    for (bone, prop), vals in ch.items():
        d = DEFAULT[prop]
        if all(max(abs(v[j] - d[j]) for j in range(len(v))) < 1e-4 for v in vals):
            continue
        ks = rdp(list(zip(ts, vals)), TOL[prop])
        nkeys += len(ks)
        L.append(f"key {name} {bone}.{prop} " + " ".join(f"{t:.4f}:{fmt(v)}" for t, v in ks))
    for slot, seq in att.items():
        out = []
        for t, a in zip(ts, seq):
            if not out or out[-1][1] != a:
                out.append((t, a))
        L.append(f"key {name} {slot}.attachment " + " ".join(f"{t:.4f}:{a}" for t, a in out))
    for t, ev in EVENTS.get(name, []):
        L.append(f"event {name} {t} {ev}")
    return L, nkeys


def main():
    names = sys.argv[1:] or list(CLIPS)
    existing = atom("q", "anims", "--limit", "200", check=False)
    have = {ln.split()[0] for ln in existing.splitlines() if ln.strip()}
    L = []
    evs = sorted({ev for n in names for _, ev in EVENTS.get(n, [])})
    have_ev = atom("q", "events", check=False)
    for ev in evs:
        if ev not in have_ev:
            L.append(f"event.add {ev}")
    for n in names:
        if n in have:
            L.append(f"anim.del {n}")
        ops, nk = ops_for(n)
        print(f"{n}: {nk} khoá")
        L += ops
    path = os.path.join(ATOM, "ops", "10_clip.ops")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(atom("do", "-f", path).splitlines()[-1][:200], "|", len(L), "dòng")


if __name__ == "__main__":
    main()
