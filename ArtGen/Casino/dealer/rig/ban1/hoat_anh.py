# Clip chung của Lão Mực (GD_Claude/31 mục 4.1, mốc D2). Viết bằng hàm thời gian, nướng 30 khung/giây, lược khoá thừa (RDP),
# ghi ../atom/ops/10_clip.ops rồi `atom do -f`.
# Tay ống cao su: mỗi khung tay là đường cong bậc hai từ vai tới đích (độ võng `bend`, dương = võng ra ngoài thân), chia đều 8 đốt
# theo độ dài cung; đốt dài ra khi với xa (dời xương con dọc trục cha, không dùng tỉ lệ để khỏi cộng dồn); bàn tay theo hướng đốt cuối
# + `tilt`. Đích tay cho bằng toạ độ thế giới (dáng gốc), đổi sang hệ ngực bằng động học thuận của root > move > hip > chest.
# Mặt: đổi hình `mat_XX` / `mieng_XX`; bàn tay: `tay_XX_t` / `tay_XX_p`.
# Chạy: py -3 -I hoat_anh.py [tên clip ...]   (không đối số: mọi clip)
import json, math, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
CLI = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
OX, OY = geo["origin"]
J = geo["J"]
FPS = 30
NSEG = 8


def W(name):
    px, py = J[name]
    return (px - OX, OY - py)


def angle(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


# ---------- dáng gốc (thế giới) ----------
HIP = W("hong")
CHEST = W("nguc")
HEAD = W("dau")
SH = {"t": W("vai_trai"), "p": W("vai_phai")}
WR = {"t": W("co_tay_trai"), "p": W("co_tay_phai")}
ARM_A = {s: angle(SH[s], WR[s]) for s in "tp"}
SEG = {s: math.dist(SH[s], WR[s]) / NSEG for s in "tp"}


# ma trận 2x3 [a b x; c d y]
def mat(x, y, rot, sx=1.0, sy=1.0):
    r = math.radians(rot)
    c, s = math.cos(r), math.sin(r)
    return (c * sx, -s * sy, x, s * sx, c * sy, y)


def mul(m, n):
    a, b, x, c, d, y = m
    a2, b2, x2, c2, d2, y2 = n
    return (a * a2 + b * c2, a * b2 + b * d2, a * x2 + b * y2 + x, c * a2 + d * c2, c * b2 + d * d2, c * x2 + d * y2 + y)


def apply(m, p):
    a, b, x, c, d, y = m
    return (a * p[0] + b * p[1] + x, c * p[0] + d * p[1] + y)


def inv(m):
    a, b, x, c, d, y = m
    det = a * d - b * c
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    return (ia, ib, -(ia * x + ib * y), ic, id_, -(ic * x + id_ * y))


def mang(m):
    return math.degrees(math.atan2(m[3], m[0]))


def local_of(child_w, child_rot, parent_w, parent_rot):
    r = math.radians(-parent_rot)
    dx, dy = child_w[0] - parent_w[0], child_w[1] - parent_w[1]
    return (dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)), child_rot - parent_rot


HIP_L, HIP_R = local_of(HIP, 90, (0, 0), 0)
CHEST_L, CHEST_R = local_of(CHEST, 90, HIP, 90)
T1_L = {s: local_of(SH[s], ARM_A[s], CHEST, 90) for s in "tp"}


def chest_world(p):
    """Ma trận thế giới của ngực theo khoá thân (move.translate, hip.rotate/scale, chest.rotate)."""
    m = mat(p["mx"], p["my"], 0)
    m = mul(m, mat(HIP_L[0], HIP_L[1], HIP_R + p["hr"], p["hsx"], p["hsy"]))
    m = mul(m, mat(CHEST_L[0], CHEST_L[1], CHEST_R + p["cr"], 1, 1))
    return m


def bez(a, c, b, t):
    u = 1 - t
    return (u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1])


def arm_chain(S, H, bend, side):
    """Đường cong vai -> đích; trả góc thế giới và độ dài 8 đốt (đều theo cung). bend dương = khuỷu chìa ra xa thân
    (side −1 tay bên trái người xem, +1 bên phải); tay nằm ngang thì võng xuống."""
    mx, my = (S[0] + H[0]) / 2, (S[1] + H[1]) / 2
    dx, dy = H[0] - S[0], H[1] - S[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    if abs(nx) > 0.3:
        if nx * side < 0:
            nx, ny = -nx, -ny
    elif ny > 0:
        nx, ny = -nx, -ny
    C = (mx + nx * bend, my + ny * bend)
    pts = [bez(S, C, H, i / 200) for i in range(201)]
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.dist(pts[i - 1], pts[i]))
    tot = cum[-1]
    knots = []
    j = 0
    for k in range(NSEG + 1):
        target = tot * k / NSEG
        while j < len(cum) - 2 and cum[j + 1] < target:
            j += 1
        f = (target - cum[j]) / max(cum[j + 1] - cum[j], 1e-9)
        knots.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f))
    angs = [angle(knots[k], knots[k + 1]) for k in range(NSEG)]
    return angs, tot / NSEG


def unwrap(prev, a):
    while a - prev > 180:
        a -= 360
    while a - prev < -180:
        a += 360
    return a


# ---------- dáng ----------
REST = {"t": (WR["t"][0], WR["t"][1]), "p": (WR["p"][0], WR["p"][1])}


def base_pose():
    return {
        "mx": 0.0, "my": 0.0, "hr": 0.0, "hsx": 1.0, "hsy": 1.0, "cr": 0.0, "nr": 0.0, "dr": 0.0, "dsx": 1.0, "dsy": 1.0,
        "dx": 0.0, "dy": 0.0, "lr": 0.0, "lx": 0.0, "ly": 0.0, "msx": 1.0, "msy": 1.0,
        "arm": {"t": {"to": REST["t"], "bend": 0.0, "tilt": 0.0, "hand": 1}, "p": {"to": REST["p"], "bend": 0.0, "tilt": 0.0, "hand": 1}},
        "eye": 2, "mouth": 1,
    }


def lerp(a, b, t):
    return a + (b - a) * t


def lp(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def eout(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ein(t):
    t = max(0.0, min(1.0, t))
    return t ** 3


def back(t, k=1.8):
    t = max(0.0, min(1.0, t))
    return 1 + (k + 1) * (t - 1) ** 3 + k * (t - 1) ** 2


def seg(t, t0, t1, f=ease):
    return f((t - t0) / max(t1 - t0, 1e-9))


def wob(t, t0, dur, amp, freq=3.0):
    """Lắc tắt dần sau cú dừng (nảy quá đà kiểu ống cao su)."""
    if t < t0:
        return 0.0
    u = (t - t0) / dur
    if u > 1:
        return 0.0
    return amp * math.sin(u * math.pi * 2 * freq) * (1 - u) ** 2


def bob(t, period, amp, phase=0.0):
    return amp * math.sin((t / period + phase) * 2 * math.pi)


# ---------- clip ----------
CLIPS = {}


def clip(name, dur, loop=False):
    def deco(f):
        CLIPS[name] = (dur, loop, f)
        return f
    return deco


TABLE_Y = 420.0  # mặt bàn (thế giới) ngang thắt lưng khi đứng sau bàn


@clip("idle", 2.0, loop=True)
def c_idle(t, p):
    p["my"] = -abs(bob(t, 2.0, 7))          # nhún 2 phách
    p["hsx"] = 1 - abs(bob(t, 2.0, 0.025))  # nén khi xuống
    p["hsy"] = 1 + abs(bob(t, 2.0, 0.018))
    p["hr"] = bob(t, 2.0, 1.2, 0.25)
    p["dr"] = bob(t, 2.0, -2.5, 0.35)
    for s, sg in (("t", -1), ("p", 1)):
        a = p["arm"][s]
        a["to"] = (REST[s][0] + bob(t, 2.0, 6, 0.1 if s == "t" else 0.6), REST[s][1] + abs(bob(t, 2.0, 5)))
        a["bend"] = 18 + bob(t, 2.0, 10, 0.3 if s == "t" else 0.8)
    p["eye"] = 10 if 0.75 <= t < 1.15 else 2  # liếc ngang một nhịp
    p["mouth"] = 8 if 1.15 <= t < 1.5 else 1


@clip("greet", 1.5)
def c_greet(t, p):
    a = seg(t, 0.0, 0.18)         # lấy đà: nhún xuống
    b = seg(t, 0.18, 0.42, eout)  # bật lên, tay chạm lưỡi trai
    c = seg(t, 1.05, 1.45)        # về
    up = b * (1 - c)
    p["my"] = -14 * a * (1 - b) + 4 * up
    p["hsx"] = 1 - 0.06 * a * (1 - b) + 0.04 * up
    p["dr"] = -6 * up + wob(t, 0.42, 0.5, 3)
    p["cr"] = 3 * up
    r = p["arm"]["p"]
    tip = (222.0, 1238.0)  # mép phải vành lưỡi trai, ngoài mặt
    r["to"] = lp(REST["p"], tip, up)
    r["bend"] = lerp(18, 90, up)
    r["tilt"] = 70 * up
    r["hand"] = 5 if 0.3 <= t < 1.1 else 1
    p["lr"] = -9 * seg(t, 0.4, 0.55) * (1 - c) + wob(t, 0.55, 0.5, 4)
    p["ly"] = 6 * seg(t, 0.4, 0.55) * (1 - c)
    l = p["arm"]["t"]
    l["bend"] = 18
    p["eye"] = 1 if 0.2 <= t < 1.2 else 2
    p["mouth"] = 1


@clip("talk", 1.2, loop=True)
def c_talk(t, p):
    p["my"] = -abs(bob(t, 0.6, 4))
    p["dr"] = bob(t, 1.2, 3)
    shapes = [9, 10, 1, 9, 8, 10, 9, 1]
    p["mouth"] = shapes[int(t / 0.15) % len(shapes)]
    p["eye"] = 1 if t < 0.9 else 2
    r = p["arm"]["p"]
    g = 0.5 - 0.5 * math.cos(t / 1.2 * 2 * math.pi)
    r["to"] = (lerp(205, 255, g), lerp(760, 820, g))
    r["bend"] = 45
    r["tilt"] = lerp(60, 20, g)
    r["hand"] = 1 if g < 0.5 else 2
    p["arm"]["t"]["bend"] = 15


@clip("bet_watch", 1.6)
def c_bet(t, p):
    a = seg(t, 0.0, 0.3, eout)
    c = seg(t, 1.25, 1.6)
    k = a * (1 - c)
    rub = math.sin(t * 2 * math.pi * 4) * 14 * seg(t, 0.3, 0.45) * (1 - c)
    p["arm"]["t"]["to"] = lp(REST["t"], (-30 + rub, 870), k)
    p["arm"]["p"]["to"] = lp(REST["p"], (30 + rub, 870), k)
    p["arm"]["t"]["bend"] = lerp(18, 75, k)
    p["arm"]["p"]["bend"] = lerp(18, 75, k)
    p["arm"]["t"]["tilt"] = -40 * k
    p["arm"]["p"]["tilt"] = 40 * k
    p["arm"]["t"]["hand"] = p["arm"]["p"]["hand"] = 2 if k > 0.3 else 1
    p["cr"] = -2 * k
    p["dr"] = -4 * k
    p["dy"] = -6 * k
    p["eye"] = 3 if 0.2 <= t < 1.3 else 2
    p["mouth"] = 1


@clip("take", 1.6)
def c_take(t, p):
    a = seg(t, 0.0, 0.25, eout)      # lấy đà: hai tay dang rộng, ngả ra
    b = seg(t, 0.25, 0.42, eout)     # vươn dài xuống đống chip
    c = seg(t, 0.48, 0.95, ease)     # vơ về khay
    d = seg(t, 1.2, 1.6)             # về
    pile = {"t": (-150.0, 230.0), "p": (150.0, 230.0)}
    wide = {"t": (-430.0, 760.0), "p": (430.0, 760.0)}
    tray = {"t": (-60.0, 470.0), "p": (60.0, 470.0)}
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        pos = lp(REST[s], wide[s], a)
        pos = lp(pos, pile[s], b)
        pos = lp(pos, tray[s], c)
        pos = lp(pos, REST[s], d)
        r["to"] = pos
        r["bend"] = 20 + 90 * b * (1 - c) + 40 * c * (1 - d) + wob(t, 0.95, 0.45, 25)
        r["tilt"] = (-30 * c * (1 - d)) * sg
        r["hand"] = 1 if t < 0.3 else 7 if t < 0.95 else 9 if t < 1.25 else 1
    p["hsx"] = 1 + 0.06 * a * (1 - b) - 0.07 * b * (1 - c) + wob(t, 0.95, 0.4, 0.03)
    p["hsy"] = 1 - 0.04 * a * (1 - b) + 0.05 * b * (1 - c)
    p["my"] = -10 * b * (1 - c)
    p["cr"] = -3 * b * (1 - c)
    p["dr"] = 5 * a * (1 - b) - 4 * b * (1 - c)
    p["eye"] = 3 if t < 0.48 else 6 if t < 1.25 else 2
    p["mouth"] = 1 if t < 0.48 else 2 if t < 1.25 else 1


@clip("pay", 1.4)
def c_pay(t, p):
    a = seg(t, 0.1, 0.45, ease)
    b = seg(t, 0.45, 0.85, ease)   # đẩy chip chậm, tiếc
    c = seg(t, 0.95, 1.35)
    r = p["arm"]["p"]
    chip = (80.0, 300.0)
    give = (60.0, 140.0)
    pos = lp(REST["p"], chip, a)
    pos = lp(pos, give, b)
    pos = lp(pos, REST["p"], c)
    r["to"] = pos
    r["bend"] = 30 + 30 * a * (1 - c)
    r["hand"] = 4 if 0.15 <= t < 1.0 else 1
    r["tilt"] = -60 * a * (1 - c)
    p["hr"] = -2 * a * (1 - c)
    p["dr"] = 4 * b * (1 - c) + bob(t, 0.25, 1.2) * a * (1 - c)
    p["eye"] = 7 if 0.1 <= t < 1.1 else 2
    p["mouth"] = 6 if 0.1 <= t < 1.1 else 1


@clip("react_win_small", 1.2)
def c_win_small(t, p):
    a = seg(t, 0.0, 0.25, eout)
    c = seg(t, 0.85, 1.2)
    k = a * (1 - c)
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        r["to"] = lp(REST[s], (190 * sg, 560), k)
        r["bend"] = lerp(18, 90, k)
        r["tilt"] = -90 * sg * k
        r["hand"] = 3 if k > 0.4 else 1
    p["dr"] = math.sin(t * 2 * math.pi * 3) * 5 * k
    p["eye"] = 9 if 0.1 <= t < 1.0 else 2
    p["mouth"] = 8 if t < 0.5 else 6 if t < 1.0 else 1


@clip("react_win_big", 1.7)
def c_win_big(t, p):
    a = seg(t, 0.0, 0.12, eout)      # giật bắn
    b = seg(t, 0.12, 0.7, ease)      # giữ sốc, hạ dần
    c = seg(t, 1.25, 1.7)
    k = a * (1 - c)
    p["hsx"] = 1 + 0.2 * a * (1 - 0.6 * b) * (1 - c) + wob(t, 0.12, 0.6, 0.04)
    p["hsy"] = 1 - 0.12 * a * (1 - 0.6 * b) * (1 - c)
    p["my"] = 30 * a * (1 - b) * (1 - c)
    # lưỡi trai bay lên rồi rơi lại đầu
    fly = seg(t, 0.05, 0.3, eout) * (1 - seg(t, 0.3, 0.75, ein))
    p["ly"] = 150 * fly
    p["lr"] = 30 * fly + wob(t, 0.75, 0.4, 6)
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        r["to"] = lp(REST[s], (300 * sg, 1280), k * (1 - 0.35 * b))
        r["bend"] = 18 + 50 * k
        r["tilt"] = 0
        r["hand"] = 1
    p["msx"] = p["msy"] = 1 + 0.25 * a * (1 - c)
    p["eye"] = 5 if 0.04 <= t < 1.3 else 2
    p["mouth"] = 4 if 0.04 <= t < 1.0 else 6 if t < 1.35 else 1


@clip("react_lose", 1.6)
def c_lose(t, p):
    a = seg(t, 0.0, 0.25, eout)
    c = seg(t, 1.2, 1.6)
    k = a * (1 - c)
    shake = math.sin(t * 2 * math.pi * 6) * k
    p["hsx"] = 1 + 0.1 * k + 0.025 * shake
    p["hr"] = -3 * k
    p["dr"] = 12 * k + 2.5 * shake
    p["my"] = 3 * abs(shake)
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        r["to"] = lp(REST[s], (85 * sg, 560 + 6 * shake), k)
        r["bend"] = lerp(18, 80, k)
        r["tilt"] = 70 * sg * k
        r["hand"] = 2 if k > 0.3 else 1
    p["eye"] = 6 if 0.05 <= t < 1.3 else 2
    p["mouth"] = 2 if 0.05 <= t < 1.3 else 1


@clip("react_push", 1.1)
def c_push(t, p):
    a = seg(t, 0.0, 0.3, eout)
    c = seg(t, 0.7, 1.1)
    k = a * (1 - c)
    p["my"] = 8 * k
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        r["to"] = lp(REST[s], (330 * sg, 820), k)
        r["bend"] = lerp(18, 45, k)
        r["tilt"] = 80 * sg * k
        r["hand"] = 2 if k > 0.3 else 1
    p["dr"] = 6 * k
    p["eye"] = 1 if 0.1 <= t < 0.9 else 2
    p["mouth"] = 8


@clip("grumpy", 1.5)
def c_grumpy(t, p):
    a = seg(t, 0.0, 0.32, eout)      # giơ nắm tay
    b = seg(t, 0.32, 0.42, ein)      # đập xuống
    c = seg(t, 1.1, 1.5)
    hi = {"t": (-200.0, 1150.0), "p": (200.0, 1150.0)}
    hit = {"t": (-130.0, TABLE_Y), "p": (130.0, TABLE_Y)}
    for s, sg in (("t", -1), ("p", 1)):
        r = p["arm"][s]
        pos = lp(REST[s], hi[s], a)
        pos = lp(pos, hit[s], b)
        pos = lp(pos, REST[s], c)
        r["to"] = (pos[0], pos[1] + wob(t, 0.42, 0.35, 18))
        r["bend"] = lerp(18, 55, a) * (1 - c) + 18 * c
        r["hand"] = 3 if 0.1 <= t < 1.2 else 1
    squash = b * (1 - seg(t, 0.42, 0.75, eout))
    p["hsx"] = 1 + 0.08 * a * (1 - b) - 0.18 * squash
    p["hsy"] = 1 + 0.12 * squash
    p["my"] = 10 * a * (1 - b) - 12 * squash
    p["dr"] = wob(t, 0.42, 0.5, 4)
    p["eye"] = 9 if 0.05 <= t < 1.25 else 2
    p["mouth"] = 5 if 0.05 <= t < 1.25 else 1


@clip("sulk", 1.7)
def c_sulk(t, p):
    a = seg(t, 0.0, 0.4, ease)
    c = seg(t, 1.35, 1.7)
    k = a * (1 - c)
    p["my"] = -16 * k
    p["hsx"] = 1 - 0.05 * k
    p["dr"] = -8 * k
    p["lr"] = -14 * k
    p["lx"] = 10 * k
    p["ly"] = -12 * k
    r = p["arm"]["p"]
    wave = math.sin(seg(t, 0.5, 1.3, lambda u: u) * math.pi * 4) if 0.5 <= t < 1.3 else 0
    r["to"] = lp(REST["p"], (260 + 25 * wave, 900), seg(t, 0.4, 0.6) * (1 - seg(t, 1.2, 1.45)))
    r["bend"] = 35
    r["tilt"] = 30 + 20 * wave
    r["hand"] = 1
    p["arm"]["t"]["bend"] = 12
    p["eye"] = 7 if 0.1 <= t < 1.5 else 2
    p["mouth"] = 6 if 0.1 <= t < 1.5 else 1


EVENTS = {"take": [(0.42, "cham_chip"), (0.95, "vo_xong")], "grumpy": [(0.42, "dap_ban")], "react_win_big": [(0.05, "soc")],
          "pay": [(0.85, "tra_chip")], "greet": [(0.42, "cham_mu")]}


# ---------- nướng ----------
def bake(name):
    dur, loop, f = CLIPS[name]
    n = int(round(dur * FPS))
    ch = {}  # (bone, prop) -> list[(t, value tuple)]
    att = {}  # slot -> list[(t, name)]
    prev_ang = {}

    def put(bone, prop, t, v):
        ch.setdefault((bone, prop), []).append((t, v))

    for i in range(n + 1):
        t = min(i / FPS, dur)
        p = base_pose()
        f(t, p)
        put("move", "translate", t, (p["mx"], p["my"]))
        put("hip", "rotate", t, (p["hr"],))
        put("hip", "scale", t, (p["hsx"], p["hsy"]))
        put("chest", "rotate", t, (p["cr"],))
        put("neck", "rotate", t, (p["nr"],))
        put("head", "rotate", t, (p["dr"],))
        put("head", "scale", t, (p["dsx"], p["dsy"]))
        put("head", "translate", t, (p["dx"], p["dy"]))
        put("luoi", "rotate", t, (p["lr"],))
        put("luoi", "translate", t, (p["lx"], p["ly"]))
        put("mat", "scale", t, (1.0, 1.0))
        put("mieng", "scale", t, (p["msx"], p["msy"]))
        cm = chest_world(p)
        cang = mang(cm)
        for s in "tp":
            a = p["arm"][s]
            (lx, ly), lrot = T1_L[s]
            S = apply(cm, (lx, ly))
            angs, ln = arm_chain(S, a["to"], a["bend"], -1 if s == "t" else 1)
            # góc liền mạch theo thời gian
            for k in range(NSEG):
                key = (s, k)
                if key in prev_ang:
                    angs[k] = unwrap(prev_ang[key], angs[k])
                prev_ang[key] = angs[k]
            put(f"tay_{s}1", "rotate", t, (angs[0] - cang - lrot,))
            for k in range(1, NSEG):
                put(f"tay_{s}{k + 1}", "rotate", t, (angs[k] - angs[k - 1],))
                put(f"tay_{s}{k + 1}", "translate", t, (ln - SEG[s], 0.0))
            put(f"tay_{s}b", "rotate", t, (a["tilt"] + (angs[-1] - angs[-1]),))
            put(f"tay_{s}b", "translate", t, (ln - SEG[s], 0.0))
            slot = "ban_tay_trai" if s == "t" else "ban_tay_phai"
            att.setdefault(slot, []).append((t, f"tay_{a['hand']:02d}_{s}"))
        att.setdefault("mat", []).append((t, f"mat_{p['eye']:02d}"))
        att.setdefault("mieng", []).append((t, f"mieng_{p['mouth']:02d}"))
    return dur, loop, ch, att


def rdp(keys, tol):
    """Lược khoá: giữ khoá đầu cuối, bỏ khoá nằm trên đoạn thẳng nối hai khoá kề trong sai số."""
    if len(keys) <= 2:
        return keys
    out = [keys[0]]

    def rec(i0, i1):
        t0, v0 = keys[i0]
        t1, v1 = keys[i1]
        worst, wi = 0.0, -1
        for i in range(i0 + 1, i1):
            t, v = keys[i]
            f = (t - t0) / max(t1 - t0, 1e-9)
            e = max(abs(v[j] - (v0[j] + (v1[j] - v0[j]) * f)) for j in range(len(v)))
            if e > worst:
                worst, wi = e, i
        if worst > tol and wi > 0:
            rec(i0, wi)
            out.append(keys[wi])
            rec(wi, i1)

    rec(0, len(keys) - 1)
    out.append(keys[-1])
    return out


TOL = {"rotate": 0.25, "translate": 0.4, "scale": 0.003}


def fmt(v):
    return ",".join(f"{x:.3f}".rstrip("0").rstrip(".") if abs(x) > 1e-9 else "0" for x in v)


def ops_for(name):
    dur, loop, ch, att = bake(name)
    L = [f"anim.del {name}"] if False else []
    L.append(f"anim.add {name} dur={dur} loop={'true' if loop else 'false'}")
    for (bone, prop), keys in ch.items():
        if all(max(abs(x - (1.0 if prop == 'scale' else 0.0)) for x in v) < 1e-6 for _, v in keys):
            continue  # đứng yên ở dáng gốc
        ks = rdp(keys, TOL[prop])
        L.append(f"key {name} {bone}.{prop} " + " ".join(f"{t:.4f}:{fmt(v)}" for t, v in ks))
    for slot, seq in att.items():
        out = []
        for t, a in seq:
            if not out or out[-1][1] != a:
                out.append((t, a))
        L.append(f"key {name} {slot}.attachment " + " ".join(f"{t:.4f}:{a}" for t, a in out))
    for t, ev in EVENTS.get(name, []):
        L.append(f"event {name} {t} {ev}")
    return L


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out)
        raise SystemExit("atom lỗi")
    return out


def main():
    names = sys.argv[1:] or list(CLIPS)
    existing = atom("q", "anims", check=False)
    L = []
    evs = sorted({ev for n in names for _, ev in EVENTS.get(n, [])})
    have_ev = atom("q", "events", check=False)
    for ev in evs:
        if ev not in have_ev:
            L.append(f"event.add {ev}")
    for n in names:
        if n in existing.split():
            L.append(f"anim.del {n}")
        L += ops_for(n)
    path = os.path.join(ATOM, "ops", "10_clip.ops")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(atom("do", "-f", path).splitlines()[-1], "|", len(L), "dòng")


if __name__ == "__main__":
    main()
