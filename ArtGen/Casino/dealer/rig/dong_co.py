# Động cơ hoạt hình ống cao su của Lão Mực (GD_Claude/31, D2 bản 2). hoat_anh.py viết DÁNG theo giờ (hàm thời gian, tay cho bằng
# đích bàn tay); file này lo phần "cao su" rồi nướng thành khoá xương 30 khung/giây:
#   1. Thân: 4 đốt sống (nghiêng, cong chữ C, chữ S), nén giãn bằng DỜI đốt + tỉ lệ ngang của "xương da" (không lây sang tay, đầu).
#   2. Tay: đường cong bậc ba vai -> bàn tay, giữ chiều dài khi chùng (phình cung ra), giãn khi với xa và THON lại theo độ giãn
#      (Cuphead: tay giãn hết cỡ chỉ còn ~60-75 % bề dày); mỗi nút dọc tay nhận chuyển động của vai / bàn tay TRỄ dần theo
#      khoảng cách (sóng chạy dọc ống) + lò xo nảy tắt dần; bàn tay rê theo đà (ngón kéo về sau).
#   3. Phần trễ: chỏm tóc 3 đốt, tóc mai, lưỡi trai + vành, hai cánh nơ là lò xo góc bị gia tốc của gốc xương kéo (không khoá tay).
#   4. Chân: IK hai đốt tính tại chỗ, bàn chân ghim đất, gối chìa ra ngoài (chân vòng kiềng kiểu ống cao su).
#   5. Clip một lần: chạy đà trước bằng idle cho lò xo vào nhịp, hai đầu hoà vào idle (khung đầu / cuối trùng idle giây 0).
# Toạ độ thế giới AtomSpine: x = px − 512, y = 1460 − py (y lên).
import json, math, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
CLI = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
OX, OY = geo["origin"]
J = geo["J"]
FPS = 30          # khoá xuất
SUB = 2           # bước mô phỏng mỗi khung (60 Hz)
DT = 1.0 / (FPS * SUB)
NSEG = 8
TABLE_Y = 500.0   # mép bàn sau (thế giới): bàn che từ đây xuống; game canh rig sao cho y này trùng mép bàn
BEAT = 0.5        # một phách (giây): 120 phách / phút
# Bản 3 (người dùng chê "cánh tay gần vai lỏng lẻo, giống sợi chỉ hơn là mềm mại"): tay là một ỐNG có bề dày.
ARM_THICK = 1.16  # bề dày ống so với ảnh gốc (ảnh gốc 49 px; tờ concept vẽ tay to hơn)
ARM_THIN_MIN = 0.82   # kéo căng chỉ thon tới 82 % (× ARM_THICK = 95 % ảnh gốc), không bao giờ thành sợi
ARM_FAT_MAX = 1.10    # bị dồn ngắn lại thì phình tới 110 %


def firm(u):
    """Độ "mềm" dọc ống (u = 0 vai, 1 cổ tay): 0 ở ba đốt đầu (bắp tay bám chắc theo vai, không trễ, không lượn), tăng dần về
    cẳng tay. Mọi sóng trễ và lò xo của ống đều nhân với hàm này."""
    t = clamp((u - 0.30) / 0.40)
    return t * t * (3 - 2 * t)


def Wp(name):
    px, py = J[name]
    return (px - OX, OY - py)


def ang(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


# ---------- ma trận 2x3 [a b x; c d y] ----------
def mat(x, y, rot, sx=1.0, sy=1.0):
    r = math.radians(rot)
    c, s = math.cos(r), math.sin(r)
    return (c * sx, -s * sy, x, s * sx, c * sy, y)


def mul(m, n):
    a, b, x, c, d, y = m
    a2, b2, x2, c2, d2, y2 = n
    return (a * a2 + b * c2, a * b2 + b * d2, a * x2 + b * y2 + x, c * a2 + d * c2, c * b2 + d * d2, c * x2 + d * y2 + y)


def apply(m, p):
    return (m[0] * p[0] + m[1] * p[1] + m[2], m[3] * p[0] + m[4] * p[1] + m[5])


def inv(m):
    a, b, x, c, d, y = m
    det = a * d - b * c
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    return (ia, ib, -(ia * x + ib * y), ic, id_, -(ic * x + id_ * y))


def mang(m):
    return math.degrees(math.atan2(m[3], m[0]))


def rot2(v, deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


# ---------- dáng gốc ----------
SETUP = {}  # tên -> (cha, vị trí thế giới, góc thế giới)


def _b(name, parent, pos, rot):
    SETUP[name] = (parent, pos, rot)


_b("root", None, (0, 0), 0)
_b("move", "root", (0, 0), 0)
_b("hip", "move", Wp("hong"), 90)
_b("bung", "hip", Wp("bung"), 90)
_b("nguc", "bung", Wp("nguc"), 90)
_b("vai", "nguc", Wp("vai"), 90)
for _n, _k in (("hip", "hong"), ("bung", "bung"), ("nguc", "nguc"), ("vai", "vai")):
    _b(_n + "_d", _n, Wp(_k), 90)
_b("neck", "vai", Wp("co"), 90)
_b("head", "neck", Wp("dau"), 90)
_b("chom1", "head", Wp("chom1"), ang(Wp("chom1"), Wp("chom2")))
_b("chom2", "chom1", Wp("chom2"), ang(Wp("chom2"), Wp("chom3")))
_b("chom3", "chom2", Wp("chom3"), ang(Wp("chom3"), Wp("chom4")))
_b("mai", "head", Wp("mai1"), ang(Wp("mai1"), Wp("mai2")))
_b("luoi", "head", Wp("luoi"), ang(Wp("luoi"), Wp("luoi2")))
_b("luoi2", "luoi", Wp("luoi2"), ang(Wp("luoi2"), Wp("luoi3")))
_b("mat", "head", Wp("mat"), 0)
_b("mieng", "head", Wp("mieng"), 0)
_b("no", "vai", Wp("no"), 0)
_b("no_t", "no", Wp("no_t"), ang(Wp("no_t"), Wp("no_t2")))
_b("no_p", "no", Wp("no_p"), ang(Wp("no_p"), Wp("no_p2")))
SH, WR, ARM_A, SEG = {}, {}, {}, {}
for _s, _n in (("t", "trai"), ("p", "phai")):
    _b(f"dui_{_s}", "hip", Wp(f"dui_{_n}"), ang(Wp(f"dui_{_n}"), Wp(f"goi_{_n}")))
    _b(f"ong_{_s}", f"dui_{_s}", Wp(f"goi_{_n}"), ang(Wp(f"goi_{_n}"), Wp(f"co_chan_{_n}")))
    _b(f"ban_{_s}", f"ong_{_s}", Wp(f"co_chan_{_n}"), ang(Wp(f"co_chan_{_n}"), Wp(f"ban_chan_{_n}")))
    SH[_s], WR[_s] = Wp(f"vai_{_n}"), Wp(f"co_tay_{_n}")
    ARM_A[_s] = ang(SH[_s], WR[_s])
    SEG[_s] = dist(SH[_s], WR[_s]) / NSEG
    _b(f"tay_{_s}1", "vai", SH[_s], ARM_A[_s])
ARM_L = {s: SEG[s] * NSEG for s in "tp"}
SPINE = ["hip", "bung", "nguc", "vai"]
SPINE_LEN = [Wp("bung")[1] - Wp("hong")[1], Wp("nguc")[1] - Wp("bung")[1], Wp("vai")[1] - Wp("nguc")[1], Wp("co")[1] - Wp("vai")[1]]
REST_HAND = {"t": WR["t"], "p": WR["p"]}


def setup_local(name):
    parent, pos, rot = SETUP[name]
    if parent is None:
        return pos, rot
    _, ppos, prot = SETUP[parent]
    d = (pos[0] - ppos[0], pos[1] - ppos[1])
    return rot2(d, -prot), rot - prot


# ---------- hàm nhịp ----------
def clamp(v, a=0.0, b=1.0):
    return a if v < a else b if v > b else v


def lerp(a, b, t):
    return a + (b - a) * t


def lp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def eout(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ein(t):
    t = clamp(t)
    return t ** 3


def lin(t):
    return clamp(t)


def back(t, k=1.3):
    """Vào dáng nhanh, vượt quá đích ~6 % rồi lùi về (overshoot). Đầu vào uốn t^1,4 để khung đầu không nhảy vọt: bản easeOutBack
    thuần đi được 56 % quãng đường trong 14 % thời gian đầu, soi khung xen 60 khung/giây thấy tay "dịch chuyển tức thời"."""
    t = clamp(t) ** 1.4
    return 1 + (k + 1) * (t - 1) ** 3 + k * (t - 1) ** 2


def seg(t, t0, t1, f=ease):
    return f((t - t0) / max(t1 - t0, 1e-9))


def hat(t, t0, t1, t2, t3, fin=eout, fout=ease):
    """0 trước t0, lên 1 trong t0..t1, giữ tới t2, về 0 ở t3."""
    return seg(t, t0, t1, fin) * (1 - seg(t, t2, t3, fout))


def wob(t, t0, dur, amp, freq=3.0):
    """Lắc tắt dần sau cú dừng."""
    if t < t0:
        return 0.0
    u = (t - t0) / dur
    if u > 1:
        return 0.0
    return amp * math.sin(u * math.pi * 2 * freq) * (1 - u) ** 2


def pulse(ph):
    """Nhịp nhún một phách (ph 0..1), đo từ tư liệu Steamboat Willie: KHÔNG phải sóng sin. Dập xuống rất nhanh đúng phách (1-2
    hình), giữ dáng thấp ~2 hình, bật lên trong 1-2 hình có vượt quá (giãn), rồi "giữ có trôi" tới phách sau.
    Trả 1 = thấp nhất, 0 = dáng nghỉ, âm = vươn quá."""
    ph = ph % 1.0
    if ph < 0.14:
        return ease(ph / 0.14)
    if ph < 0.30:
        return 1.0 - 0.10 * (ph - 0.14) / 0.16
    if ph < 0.46:
        return lerp(0.90, -0.26, ease((ph - 0.30) / 0.16))
    if ph < 0.80:
        return -0.26 * (1 - eout((ph - 0.46) / 0.34))
    return 0.0


def swing(x):
    """Sóng sin "bẹt đầu": đổi bên nhanh, giữ lâu ở hai đầu (dáng -> dáng thay vì trôi đều)."""
    s = math.sin(x * 2 * math.pi)
    return math.copysign(abs(s) ** 0.55, s)


class SOD:
    """Động lực bậc hai (lò xo theo đích): f Hz, z giảm chấn (<1 = nảy quá đà), r đáp ứng đầu (âm = lấy đà ngược)."""

    def __init__(self, f, z, r, x0):
        self.k1 = z / (math.pi * f)
        self.k2 = 1 / ((2 * math.pi * f) ** 2)
        self.k3 = r * z / (2 * math.pi * f)
        self.xp = list(x0)
        self.y = list(x0)
        self.yd = [0.0] * len(x0)

    def step(self, x, T=DT):
        k2 = max(self.k2, T * T / 2 + T * self.k1 / 2, T * self.k1)
        for i in range(len(x)):
            xd = (x[i] - self.xp[i]) / T
            self.xp[i] = x[i]
            self.y[i] += T * self.yd[i]
            self.yd[i] += T * (x[i] + self.k3 * xd - self.y[i] - self.k1 * self.yd[i]) / k2
        return tuple(self.y)


# ---------- dáng ----------
SPEC0 = {"to": None, "space": "w", "bow": 30.0, "k": 0.42, "out": None, "inn": None, "t0": None, "t1": None,
         "hand": 1, "hrot": None, "tilt": 0.0, "hs": None, "hsq": 0.0, "minlen": 0.80}


def spec(s, **kw):
    """Một dáng tay: đích bàn tay `to` + hình ống (bow, k, out, inn, t0, t1) + bàn tay (hand, hrot, tilt, hs, hsq)."""
    d = dict(SPEC0)
    d["to"] = REST_HAND[s]
    d.update(kw)
    return d


def new_arm(s):
    # mix: [(spec, trọng số), ...] — động cơ dựng đường cong của từng dáng rồi trộn ĐIỂM (không trộn thông số), nên đổi dáng nào
    # sang dáng nào cũng mượt. Phần còn lại là thông số động: shr dời khớp vai, lag độ trễ sóng, whip độ nảy, drag bàn tay rê,
    # sod (f, z, r) lọc lò xo cho đích bàn tay (None = bám thẳng), thin ép độ thon, hand ép hình bàn tay.
    # hrate: tần số (Hz) của lò xo xoay bàn tay; cú nện cần bàn tay xoay kịp đúng khung chạm thì tăng lên.
    return {"mix": [(spec(s), 1.0)], "shr": (0.0, 0.0), "lag": 1.0, "whip": 1.0, "drag": 1.0, "sod": None, "thin": None,
            "hand": None, "hrate": 6.5}


def arm_seq(p, s, first, *steps):
    """Chuỗi dáng tay: first rồi lần lượt (dáng, w) — w = 0 giữ dáng trước, 1 = sang hẳn dáng này."""
    mix = [(first, 1.0)]
    for sp, w in steps:
        w = clamp(w)
        if w <= 0:
            continue
        mix = [(a, k * (1 - w)) for a, k in mix if k * (1 - w) > 1e-5] + [(sp, w)]
    p["arm"][s]["mix"] = mix


def base_pose():
    return {
        "mx": 0.0, "my": 0.0,
        "sp": [0.0, 0.0, 0.0, 0.0],      # xoay thêm 4 đốt sống hip, bung, nguc, vai (độ, dương = ngả sang trái người xem)
        "sq": 0.0,                        # nén (+) / giãn (−) thân: dài × (1 − sq), ngang × (1 + 0,8 sq)
        "wd": [0.0, 0.0, 0.0, 0.0],      # phình ngang thêm từng đốt (hip, bung, nguc, vai)
        "nr": 0.0, "hr": 0.0, "hx": 0.0, "hy": 0.0, "hsq": 0.0, "hs": 1.0,
        "eye": 2, "eye_s": (1.0, 1.0), "eye_d": (0.0, 0.0), "mouth": 1, "mouth_s": (1.0, 1.0), "mouth_r": 0.0, "mouth_d": (0.0, 0.0),
        "lv_r": 0.0, "lv_d": (0.0, 0.0), "lv2": 0.0, "lv_free": 1.0,
        "chom": [0.0, 0.0, 0.0], "mai": 0.0,
        "bow_r": 0.0, "bow_s": (1.0, 1.0), "bow_d": (0.0, 0.0), "bw": 0.0,
        "arm": {"t": new_arm("t"), "p": new_arm("p")},
        "foot": {"t": (0.0, 0.0), "p": (0.0, 0.0)},
        "spring": 1.0,                    # hệ số chung cho phần trễ
    }


def spine(p, lean=0.0, arc=0.0, ess=0.0):
    """Cộng dáng sống lưng: lean nghiêng cả thân; arc cong chữ C (gốc ngả ngược, ngọn cuộn); ess chữ S."""
    wl = (0.34, 0.26, 0.22, 0.18)
    wa = (-0.45, -0.05, 0.40, 0.60)
    ws = (0.50, 0.35, -0.40, -0.45)
    for i in range(4):
        p["sp"][i] += lean * wl[i] + arc * wa[i] + ess * ws[i]


# ---------- động học thuận phần thân ----------
def body_fk(p):
    """Ma trận thế giới của move, hip, bung, nguc, vai, neck, head theo dáng p (chưa có phần trễ)."""
    M = {}
    M["move"] = mat(p["mx"], p["my"], 0)
    prev = "move"
    k_len = 1.0 - p["sq"]
    for i, b in enumerate(SPINE):
        (lx, ly), lr = setup_local(b)
        if i > 0:
            lx = lx * k_len                    # đốt con dời dọc trục cha (cha chĩa lên: trục x cục bộ)
        M[b] = mul(M[prev], mat(lx, ly, lr + p["sp"][i]))
        prev = b
    (lx, ly), lr = setup_local("neck")
    M["neck"] = mul(M["vai"], mat(lx * k_len, ly, lr + p["nr"]))
    (lx, ly), lr = setup_local("head")
    hd = rot2((p["hx"], p["hy"]), -mang(M["neck"]))
    sx = (1.0 - p["hsq"]) * p["hs"]
    sy = (1.0 + 0.8 * p["hsq"]) * p["hs"]
    M["head"] = mul(M["neck"], mat(lx + hd[0], ly + hd[1], lr + p["hr"], sx, sy))
    M["head_ns"] = mul(M["neck"], mat(lx + hd[0], ly + hd[1], lr + p["hr"]))
    return M


def to_world(M, frame, pt):
    """Điểm cho ở toạ độ dáng gốc, gắn vào khung xương `frame` -> thế giới theo dáng hiện tại."""
    _, pos, rot = SETUP[frame]
    m0 = mat(pos[0], pos[1], rot)
    key = "head_ns" if frame == "head" else frame
    return apply(mul(M[key], inv(m0)), pt)


# ---------- tay ----------
def bez3(P0, P1, P2, P3, t):
    u = 1 - t
    a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return (a * P0[0] + b * P1[0] + c * P2[0] + d * P3[0], a * P0[1] + b * P1[1] + c * P2[1] + d * P3[1])


def polyline_len(pts):
    return sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def resample(pts, n):
    """Chia đường gấp khúc thành n đoạn đều theo độ dài; trả n + 1 điểm."""
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + dist(pts[i - 1], pts[i]))
    tot = cum[-1] or 1e-6
    out = []
    j = 0
    for k in range(n + 1):
        target = tot * k / n
        while j < len(cum) - 2 and cum[j + 1] < target:
            j += 1
        f = (target - cum[j]) / max(cum[j + 1] - cum[j], 1e-9)
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f))
    return out, tot


def arm_curve(S, H, a, side, nsamp=32):
    """Đường cong tay vai S -> bàn tay H theo thông số a. Trả các điểm mẫu.
    bow: độ cong (độ): hai tiếp tuyến lệch khỏi dây cung về cùng một phía; dương = phía "ngoài" khi tay buông (bên phải người xem:
    ngược chiều kim đồng hồ). out / inn: ép hẳn hướng rời vai / hướng đi vào bàn tay (góc thế giới của tay bên PHẢI người xem;
    tay trái tự lấy đối xứng). k: độ dài tiếp tuyến theo dây cung; t0 / t1: độ dài tiếp tuyến tính bằng px (vòng ra ngoài khung).
    Tay chùng (dây cung ngắn hơn chiều dài nghỉ) thì phình tiếp tuyến cho đủ dài: ống cao su không co ngắn lại, nó cong ra."""
    cx, cy = H[0] - S[0], H[1] - S[1]
    L = math.hypot(cx, cy) or 1e-6
    c = (cx / L, cy / L)
    bow = a["bow"] * side
    d0 = rot2(c, bow)
    d1 = rot2(c, -bow)
    if a["out"] is not None:
        o = a["out"] if side > 0 else 180 - a["out"]
        d0 = (math.cos(math.radians(o)), math.sin(math.radians(o)))
    if a["inn"] is not None:
        o = a["inn"] if side > 0 else 180 - a["inn"]
        d1 = (math.cos(math.radians(o)), math.sin(math.radians(o)))
    m0 = a["t0"] if a["t0"] is not None else a["k"] * L
    m1 = a["t1"] if a["t1"] is not None else a["k"] * L

    def build(mult):
        P1 = (S[0] + d0[0] * m0 * mult, S[1] + d0[1] * m0 * mult)
        P2 = (H[0] - d1[0] * m1 * mult, H[1] - d1[1] * m1 * mult)
        return [bez3(S, P1, P2, H, i / nsamp) for i in range(nsamp + 1)]

    pts = build(1.0)
    need = ARM_L["t"] * a["minlen"]
    if polyline_len(pts) < need:
        # thêm độ dài tiếp tuyến tối thiểu để dây cung rất ngắn vẫn phình được
        base0, base1 = max(m0, 40.0), max(m1, 40.0)
        m0, m1 = base0, base1
        lo, hi = 0.0, 1.0
        while polyline_len(build(hi)) < need and hi < 40:
            hi *= 1.7
        for _ in range(14):
            mid = (lo + hi) / 2
            if polyline_len(build(mid)) < need:
                lo = mid
            else:
                hi = mid
        pts = build(hi)
    return pts


def leg_ik(hipj, ankle, l1, l2, side):
    """IK hai đốt: gối chìa ra ngoài (side −1 trái, +1 phải). Trả (góc đùi, góc ống, dài đùi, dài ống) thế giới; kéo dãn nếu xa."""
    dx, dy = ankle[0] - hipj[0], ankle[1] - hipj[1]
    d = math.hypot(dx, dy) or 1e-6
    tot = l1 + l2
    if d >= tot * 0.999:
        k = d / tot
        a = math.degrees(math.atan2(dy, dx))
        return a, a, l1 * k, l2 * k
    cosA = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)
    A = math.degrees(math.acos(cosA))
    base = math.degrees(math.atan2(dy, dx))
    th1 = base + A * side          # chân chĩa xuống: cộng góc (bên phải) thì gối sang phải
    kx, ky = hipj[0] + l1 * math.cos(math.radians(th1)), hipj[1] + l1 * math.sin(math.radians(th1))
    th2 = math.degrees(math.atan2(ankle[1] - ky, ankle[0] - kx))
    return th1, th2, l1, l2


def wrap180(a):
    return (a + 180.0) % 360.0 - 180.0


def unwrap(prev, a):
    while a - prev > 180:
        a -= 360
    while a - prev < -180:
        a += 360
    return a


# ---------- lò xo phần trễ ----------
# tên: (cha để lấy ma trận, tần số Hz, giảm chấn, độ nhạy, giới hạn độ)
DANGLY = {
    "chom1": (2.6, 0.30, 0.10, 14), "chom2": (2.3, 0.28, 0.14, 20), "chom3": (2.0, 0.26, 0.18, 28),
    "mai": (2.8, 0.28, 0.22, 30),
    "luoi": (3.6, 0.42, 0.04, 4), "luoi2": (2.9, 0.28, 0.26, 24),
    "no_t": (3.8, 0.30, 0.34, 32), "no_p": (3.8, 0.30, 0.34, 32),
}


class Spring1:
    def __init__(self, f, z):
        self.w = 2 * math.pi * f
        self.z = z
        self.x = 0.0
        self.v = 0.0

    def step(self, force, T=DT):
        # nửa ẩn: bền với bước 1/60
        a = force - self.w * self.w * self.x - 2 * self.z * self.w * self.v
        self.v += a * T
        self.x += self.v * T
        return self.x


# ---------- mô phỏng + nướng ----------
class Sim:
    """Chạy hàm dáng qua thời gian, cộng phần trễ, trả các kênh khoá theo khung."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.spr = {k: Spring1(v[0], v[1]) for k, v in DANGLY.items()}
        self.base_hist = {k: [] for k in DANGLY}
        self.hand = {}
        self.hsod = {}
        self.hand_rot = {}
        self.S_hist = {"t": [], "p": []}
        self.H_hist = {"t": [], "p": []}
        self.node_spr = {s: [Spring1(2.5, 0.30), Spring1(2.5, 0.30), Spring1(3.9, 0.32), Spring1(3.9, 0.32)] for s in "tp"}
        self.node_hist = {s: [] for s in "tp"}
        self.prev_ang = {}
        self.step_i = 0

    def frame(self, p):
        """Một bước mô phỏng với dáng p. Trả dict kênh -> giá trị (đã là số gia so với dáng gốc)."""
        ch = {}
        att = {}
        M = body_fk(p)
        ch[("move", "translate")] = (p["mx"], p["my"])
        k_len = 1.0 - p["sq"]
        for i, b in enumerate(SPINE):
            ch[(b, "rotate")] = (p["sp"][i],)
            if i > 0:
                ch[(b, "translate")] = (SPINE_LEN[i - 1] * (k_len - 1.0), 0.0)
            wdt = (1.0 + 0.8 * p["sq"]) * (1.0 + p["wd"][i])
            ch[(b + "_d", "scale")] = (1.0, wdt)
        ch[("neck", "translate")] = (SPINE_LEN[3] * (k_len - 1.0), 0.0)
        ch[("neck", "rotate")] = (p["nr"],)
        hd = rot2((p["hx"], p["hy"]), -mang(M["neck"]))
        ch[("head", "translate")] = hd
        ch[("head", "rotate")] = (p["hr"],)
        ch[("head", "scale")] = ((1.0 - p["hsq"]) * p["hs"], (1.0 + 0.8 * p["hsq"]) * p["hs"])
        # mặt
        ch[("mat", "scale")] = p["eye_s"]
        ch[("mat", "translate")] = rot2(p["eye_d"], -90)       # hệ đầu: x cục bộ = lên
        ch[("mieng", "scale")] = p["mouth_s"]
        ch[("mieng", "rotate")] = (p["mouth_r"],)
        ch[("mieng", "translate")] = rot2(p["mouth_d"], -90)
        att["mat"] = f"mat_{p['eye']:02d}"
        att["mieng"] = f"mieng_{p['mouth']:02d}"

        # ---- phần trễ: gia tốc gốc xương kéo lò xo góc ----
        H_ = M["head_ns"]
        Vm = M["vai"]
        extra = {}
        for name, (f, z, gain, lim) in DANGLY.items():
            parent, pos, rot = SETUP[name]
            frame = "head" if parent in ("head", "chom1", "chom2", "luoi") else "vai"
            Mf = H_ if frame == "head" else Vm
            _, fpos, frot = SETUP[frame]
            m0 = inv(mat(fpos[0], fpos[1], frot))
            base = apply(mul(Mf, m0), pos)
            dirw = rot2((1.0, 0.0), rot + (mang(Mf) - frot))
            hist = self.base_hist[name]
            hist.append(base)
            if len(hist) >= 5:
                # gia tốc trên cửa sổ 5 mẫu (làm mượt gai của cú dập 2 khung)
                ax = (hist[-1][0] - 2 * hist[-3][0] + hist[-5][0]) / (4 * DT * DT)
                ay = (hist[-1][1] - 2 * hist[-3][1] + hist[-5][1]) / (4 * DT * DT)
            else:
                ax = ay = 0.0
            if len(hist) > 6:
                del hist[0]
            ln = {"chom1": 100, "chom2": 80, "chom3": 55, "mai": 100, "luoi": 240, "luoi2": 130, "no_t": 72, "no_p": 72}[name]
            cross = ax * dirw[1] - ay * dirw[0]
            force = clamp(gain * cross / ln, -900, 900) * p["spring"]
            if name == "luoi":
                force *= p["lv_free"]
            x = self.spr[name].step(force)
            lim_r = math.radians(lim)
            if abs(x) > lim_r:
                self.spr[name].x = math.copysign(lim_r, x)
                self.spr[name].v *= 0.4
                x = self.spr[name].x
            extra[name] = math.degrees(x)
        for i, n in enumerate(("chom1", "chom2", "chom3")):
            ch[(n, "rotate")] = (p["chom"][i] + extra[n],)
        ch[("mai", "rotate")] = (p["mai"] + extra["mai"],)
        ch[("luoi", "rotate")] = (p["lv_r"] + extra["luoi"],)
        ch[("luoi", "translate")] = rot2(p["lv_d"], -90)
        ch[("luoi2", "rotate")] = (p["lv2"] + extra["luoi2"],)
        ch[("no", "rotate")] = (p["bow_r"],)
        ch[("no", "scale")] = p["bow_s"]
        ch[("no", "translate")] = rot2(p["bow_d"], -90)
        ch[("no_t", "rotate")] = (-p["bw"] + extra["no_t"],)
        ch[("no_p", "rotate")] = (p["bw"] + extra["no_p"],)

        # ---- tay ----
        vang = mang(M["vai"])
        for s in "tp":
            a = p["arm"][s]
            side = -1 if s == "t" else 1
            (lx, ly), lrot = setup_local(f"tay_{s}1")
            shr = rot2(a["shr"], -vang)
            S = apply(M["vai"], (lx + shr[0], ly + shr[1]))
            # trộn các dáng: điểm đường cong, đích bàn tay, góc bàn tay, cỡ bàn tay
            tw = sum(w_ for _, w_ in a["mix"]) or 1.0
            pts = None
            Ht = [0.0, 0.0]
            want = None
            ref_a = 0.0
            hs = 0.0
            hsq = 0.0
            best = None
            for sp_, w_ in a["mix"]:
                w_ = w_ / tw
                if sp_["space"] == "w":
                    H_i = sp_["to"]
                else:
                    H_i = to_world(M, {"v": "vai", "h": "head", "b": "hip"}[sp_["space"]], sp_["to"])
                c_i = arm_curve(S, H_i, sp_, side)
                if pts is None:
                    pts = [[0.0, 0.0] for _ in c_i]
                for q, c in zip(pts, c_i):
                    q[0] += c[0] * w_
                    q[1] += c[1] * w_
                Ht[0] += H_i[0] * w_
                Ht[1] += H_i[1] * w_
                if sp_["hrot"] is not None:
                    wa = sp_["hrot"] if side > 0 else 180 - sp_["hrot"]
                else:
                    wa = ang(c_i[-3], c_i[-1])
                wa += sp_["tilt"] * side
                if want is None:
                    ref_a = unwrap(self.prev_ang.get(("hand", s), ARM_A[s]), wa)
                    want = ref_a * w_
                else:
                    want += unwrap(ref_a, wa) * w_
                h_i = sp_["hs"]
                if h_i is None:
                    h_i = 1.0 + 0.6 * clamp((TABLE_Y - 40 - H_i[1]) / 360.0, 0.0, 1.4)   # với về phía người chơi: to dần
                hs += h_i * w_
                hsq += sp_["hsq"] * w_
                if best is None or w_ > best[0]:
                    best = (w_, sp_["hand"])
            Ht = (Ht[0], Ht[1])
            if a["sod"] is not None:
                key = ("sod", s)
                cur = self.hsod.get(key)
                if cur is None or cur[0] != a["sod"]:
                    f_, z_, r_ = a["sod"]
                    start = self.hand.get(s, Ht)
                    cur = (a["sod"], SOD(f_, z_, r_, start))
                    self.hsod[key] = cur
                Hf = cur[1].step(Ht)
                dxy = (Hf[0] - Ht[0], Hf[1] - Ht[1])
                n_ = len(pts) - 1
                for i_, q in enumerate(pts):          # kéo cả đường cong theo đích đã lọc (đầu vai giữ nguyên)
                    u_ = i_ / n_
                    q[0] += dxy[0] * u_
                    q[1] += dxy[1] * u_
                Ht = Hf
            else:
                self.hsod.pop(("sod", s), None)
            sh, hh = self.S_hist[s], self.H_hist[s]
            sh.append(S)
            hh.append(Ht)
            if len(sh) > 40:
                del sh[0]
                del hh[0]
            nodes, tot = resample(pts, NSEG)
            # sóng dọc ống: nút i thấy vai trễ i phần, thấy bàn tay trễ (8 − i) phần
            tau_s = 0.11 * a["lag"]
            tau_h = 0.09 * a["lag"]

            def delayed(hist, sec):
                k = sec / DT
                i0 = int(math.floor(k))
                f = k - i0
                n = len(hist)
                a_ = hist[max(0, n - 1 - i0)]
                b_ = hist[max(0, n - 2 - i0)]
                return (a_[0] + (b_[0] - a_[0]) * f, a_[1] + (b_[1] - a_[1]) * f)

            lagged = [nodes[0]]
            for i in range(1, NSEG):
                u = i / NSEG
                sd = delayed(sh, tau_s * u)
                hd_ = delayed(hh, tau_h * (1 - u))
                fm = firm(u)
                x = nodes[i][0] + fm * ((1 - u) * (sd[0] - S[0]) + u * (hd_[0] - Ht[0]))
                y = nodes[i][1] + fm * ((1 - u) * (sd[1] - S[1]) + u * (hd_[1] - Ht[1]))
                lagged.append((x, y))
            lagged.append(nodes[NSEG])
            # lò xo của ống: gia tốc các nút kéo ống lệch ngược rồi nảy tắt dần. Dùng HAI DẠNG SÓNG trơn cho cả ống (nửa sóng:
            # bụng ống phình; trọn sóng: chữ S) chứ không cho từng nút một lò xo riêng — lò xo riêng làm các nút kề giật ngược nhau,
            # ống thành lổn nhổn.
            nh = self.node_hist[s]
            nh.append(lagged)
            if len(nh) > 4:
                del nh[0]
            f1x = f1y = f2x = f2y = 0.0
            if len(nh) >= 3:
                n1 = n2 = 0.0
                for i in range(1, NSEG):
                    u = i / NSEG
                    ax = (nh[-1][i][0] - 2 * nh[-2][i][0] + nh[-3][i][0]) / (DT * DT)
                    ay = (nh[-1][i][1] - 2 * nh[-2][i][1] + nh[-3][i][1]) / (DT * DT)
                    s1, s2 = firm(u) * math.sin(math.pi * u), firm(u) * math.sin(2 * math.pi * u)
                    f1x += s1 * ax
                    f1y += s1 * ay
                    f2x += s2 * ax
                    f2y += s2 * ay
                    n1 += s1
                    n2 += abs(s2)
                f1x, f1y, f2x, f2y = f1x / n1, f1y / n1, f2x / n2, f2y / n2
            g = 0.34 * a["whip"]
            sp4 = self.node_spr[s]
            m1x = sp4[0].step(clamp(-g * f1x, -60000, 60000))
            m1y = sp4[1].step(clamp(-g * f1y, -60000, 60000))
            m2x = sp4[2].step(clamp(-g * f2x, -60000, 60000))
            m2y = sp4[3].step(clamp(-g * f2y, -60000, 60000))
            for q_, lim_ in ((sp4[0], 40.0), (sp4[1], 40.0), (sp4[2], 22.0), (sp4[3], 22.0)):
                lim_ *= a["whip"]
                if abs(q_.x) > lim_:
                    q_.x = math.copysign(lim_, q_.x)
                    q_.v *= 0.5
            m1x, m1y, m2x, m2y = sp4[0].x, sp4[1].x, sp4[2].x, sp4[3].x
            final = [lagged[0]]
            for i in range(1, NSEG):
                u = i / NSEG
                s1, s2 = firm(u) * math.sin(math.pi * u), firm(u) * math.sin(2 * math.pi * u)
                final.append((lagged[i][0] + m1x * s1 + m2x * s2, lagged[i][1] + m1y * s1 + m2y * s2))
            final.append(lagged[NSEG])
            knots, tot = resample(final, NSEG)
            # chống gập kẹp: lúc bàn tay đổi hướng gấp (rời bàn vung lên) ống tạo một nếp gập gần 180 độ chạy dọc tay; ống cao su
            # thì phải thành một vòng tròn trịa. Làm trơn các nút (giữ hai đầu) tới khi không còn khớp nào gập quá 62 độ.
            for _ in range(10):
                turn = max(abs(wrap180(ang(knots[k], knots[k + 1]) - ang(knots[k - 1], knots[k]))) for k in range(1, NSEG))
                if turn <= 62.0:
                    break
                sm = [knots[0]]
                for k in range(1, NSEG):
                    sm.append((knots[k][0] * 0.5 + (knots[k - 1][0] + knots[k + 1][0]) * 0.25,
                               knots[k][1] * 0.5 + (knots[k - 1][1] + knots[k + 1][1]) * 0.25))
                sm.append(knots[NSEG])
                knots, tot = resample(sm, NSEG)
            ln = tot / NSEG
            angs = [ang(knots[k], knots[k + 1]) for k in range(NSEG)]
            for k in range(NSEG):
                key = (s, k)
                if key in self.prev_ang:
                    angs[k] = unwrap(self.prev_ang[key], angs[k])
                else:
                    angs[k] = unwrap(ARM_A[s], angs[k])
                self.prev_ang[key] = angs[k]
            stretch = ln / SEG[s]
            thin = a["thin"] if a["thin"] is not None else ARM_THICK * clamp(stretch ** -0.25, ARM_THIN_MIN, ARM_FAT_MAX)
            r1 = unwrap(self.prev_ang.get(("r1", s), 0.0), wrap180(angs[0] - vang - lrot))
            self.prev_ang[("r1", s)] = r1
            ch[(f"tay_{s}1", "rotate")] = (r1,)
            ch[(f"tay_{s}1", "translate")] = shr
            w_last = vang + lrot + r1          # góc thế giới của đốt cuối ĐÚNG NHƯ chuỗi khoá cộng lại (liền theo giờ)
            for k in range(1, NSEG):
                dk = wrap180(angs[k] - angs[k - 1])
                w_last += dk
                ch[(f"tay_{s}{k + 1}", "rotate")] = (dk,)
                ch[(f"tay_{s}{k + 1}", "translate")] = (ln - SEG[s], 0.0)
            for k in range(NSEG + 1):
                ch[(f"tay_{s}{k + 1}d", "scale")] = (1.0, thin)
            ch[(f"tay_{s}9d", "translate")] = (ln - SEG[s], 0.0)
            # bàn tay: góc đã trộn + rê theo đà (ngón kéo về sau khi tay vung), lọc lò xo
            hprev = self.hand.get(s)
            vx = vy = 0.0
            if hprev is not None:
                vx, vy = (Ht[0] - hprev[0]) / DT, (Ht[1] - hprev[1]) / DT
            self.hand[s] = Ht
            self.prev_ang[("hand", s)] = want
            dh = (math.cos(math.radians(want)), math.sin(math.radians(want)))
            drag = clamp(-0.022 * (dh[0] * vy - dh[1] * vx), -38, 38) * a["drag"]
            cur = self.hand_rot.get(s)
            if cur is None:
                cur = (a["hrate"], SOD(a["hrate"], 0.6, 0.0, (want + drag,)))
            elif cur[0] != a["hrate"]:
                old = cur[1]
                new_ = SOD(a["hrate"], 0.6, 0.0, tuple(old.y))
                new_.yd = list(old.yd)
                new_.xp = list(old.xp)
                cur = (a["hrate"], new_)
            self.hand_rot[s] = cur
            hr = cur[1].step((want + drag,))[0]
            # góc cục bộ bàn tay = góc thế giới (liền) − góc đốt cuối theo chuỗi khoá (liền): hiệu hai hàm liền nên nội suy giữa
            # hai khoá không bao giờ quay ngược vòng; chỉ trừ một bội 360 cố định chọn ở khung đầu
            rh = hr - w_last
            if ("rh0", s) not in self.prev_ang:
                self.prev_ang[("rh0", s)] = round(rh / 360.0) * 360.0
            rh -= self.prev_ang[("rh0", s)]
            ch[(f"tay_{s}b", "rotate")] = (rh,)
            ch[(f"tay_{s}b", "translate")] = (ln - SEG[s], 0.0)
            ch[(f"tay_{s}b", "scale")] = (hs * (1.0 - hsq), hs * (1.0 + hsq))
            hand = a["hand"] if a["hand"] is not None else best[1]
            att["ban_tay_trai" if s == "t" else "ban_tay_phai"] = f"tay_{hand:02d}_{s}"

        # ---- chân: bàn chân ghim đất ----
        hang = mang(M["hip"])
        for s, n in (("t", "trai"), ("p", "phai")):
            side = -1 if s == "t" else 1
            (lx, ly), lrot = setup_local(f"dui_{s}")
            hj = apply(M["hip"], (lx, ly))
            ank0 = Wp(f"co_chan_{n}")
            ankle = (ank0[0] + p["foot"][s][0], ank0[1] + p["foot"][s][1])
            l1 = dist(Wp(f"dui_{n}"), Wp(f"goi_{n}"))
            l2 = dist(Wp(f"goi_{n}"), ank0)
            th1, th2, d1, d2 = leg_ik(hj, ankle, l1, l2, side)
            a1 = SETUP[f"dui_{s}"][2]
            a2 = SETUP[f"ong_{s}"][2]
            a3 = SETUP[f"ban_{s}"][2]
            th1 = unwrap(a1, th1)
            th2 = unwrap(a2, th2)
            ch[(f"dui_{s}", "rotate")] = ((th1 - hang) - (a1 - 90),)
            ch[(f"ong_{s}", "rotate")] = ((th2 - th1) - (a2 - a1),)
            ch[(f"ong_{s}", "translate")] = (d1 - l1, 0.0)
            ch[(f"ban_{s}", "rotate")] = ((a3 - th2) - (a3 - a2),)
            ch[(f"ban_{s}", "translate")] = (d2 - l2, 0.0)
        self.step_i += 1
        return ch, att


DEFAULT = {"rotate": (0.0,), "translate": (0.0, 0.0), "scale": (1.0, 1.0)}


def simulate(pose_fn, t0, t1, sim=None):
    """Chạy pose_fn(t) -> p từ t0 tới t1 (bước DT). Trả sim và danh sách (t, ch, att) ở các khung xuất có t >= 0."""
    sim = sim or Sim()
    out = []
    n0 = int(round(t0 / DT))
    n1 = int(round(t1 / DT))
    for i in range(n0, n1 + 1):
        t = i * DT
        p = pose_fn(t)
        ch, att = sim.frame(p)
        if i >= 0 and i % SUB == 0:
            out.append((t, ch, att))
    return sim, out


def rdp(keys, tol):
    """Lược khoá: bỏ khoá nằm trên đoạn thẳng nối hai khoá giữ lại trong sai số."""
    if len(keys) <= 2:
        return keys
    keep = [False] * len(keys)
    keep[0] = keep[-1] = True
    stack = [(0, len(keys) - 1)]
    while stack:
        i0, i1 = stack.pop()
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
            keep[wi] = True
            stack.append((i0, wi))
            stack.append((wi, i1))
    return [k for k, f in zip(keys, keep) if f]


TOL = {"rotate": 0.4, "translate": 0.6, "scale": 0.005}


def fmt(v):
    return ",".join((f"{x:.3f}".rstrip("0").rstrip(".") if abs(x) > 5e-4 else "0") for x in v)


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out[-1500:])
        raise SystemExit("atom lỗi")
    return out
