# Clip của máy quả "Háu Ăn" (rig ../atom, dựng bằng dung_rig.py). Kiểu hoạt hình ống cao su thập niên 1930: luôn nhún theo phách
# 0,5 s, lấy đà ngược chiều, nén giãn mạnh giữ thể tích, giữ dáng rồi bật, rung bằng hai dáng đổi nhau, phần ngọn trễ.
# File này viết DÁNG theo giờ (hàm c_<tên>(t) trả bảng tham số); phần "cao su" do bộ nướng ở cuối file lo:
#   * ba khối thân (hông, tấm khung cuộn, vòm đầu) nhận nén giãn và độ nghiêng TRỄ dần lên trên (0 / 0,035 / 0,075 s);
#   * hông hạ xuống khi nén, hai ống chân phình cong ra ngoài (dài ống giữ nguyên), giày ghim đất; rời đất thì giày treo theo lò xo;
#   * cần gạt và lò xo ăng ten: đầu mút là lò xo tắt dần đuổi theo dáng động học (trễ, vượt quá, rung dư).
# Nướng 30 khung/giây thành khoá AtomSpine (`key ...`), rồi `anim.reduce`. Mọi clip một lần kết thúc ở dáng nghỉ (= idle giây 0),
# trừ pull / stop_1 / stop_2 (nối vào spin) và tease / spin (lặp).
# Sự kiện: keo (cần bị giật), cach (cuộn dừng), nha_bi (nhả bi ở miệng), no / het_no (bi phun lúc jackpot), dap (đáp đất, rung màn),
#   mien_phi, chao.
# Chạy: py -3 -I hoat_anh.py [tên clip ...]   (không đối số: mọi clip)
import json, math, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
sys.path.insert(0, HERE)
from atom_cli import CLI  # noqa: E402
import dung_rig as R      # noqa: E402  (mốc px của rig)

FPS = 30
BEAT = 0.5
SUB = 4                       # bước con của lò xo mỗi khung
# ---- hình học dáng gốc (thế giới: x phải, y lên, gốc ở đất giữa hai chân) ----
HIP_Y = R.OY - R.Y_BOT        # 299
L_B = R.Y_BOT - R.Y_HT        # 187: hông -> tấm
L_P = R.Y_HT - R.Y_TD         # 400: tấm -> đầu
SOCK = {s: (R.Y_BOT - R.SOCKET_Y, -(R.LEG_X[s] - R.OX)) for s in ("t", "p")}    # gốc ống chân trong hệ hông (dọc, ngang)
ANK = {s: (R.LEG_X[s] - R.OX, R.OY - R.ANKLE_Y) for s in ("t", "p")}            # cổ chân lúc nghỉ
LEG_L = R.ANKLE_Y - R.SOCKET_Y
SEG = LEG_L / R.NLEG
SIDE = {"t": -1.0, "p": 1.0}
CAN_LOC = (R.Y_HT - R.CAN_PIVOT[1], -(R.CAN_PIVOT[0] - R.OX))                   # trục cần trong hệ tấm
CAN_A0 = R.ang(R.CAN_PIVOT, R.NUM)                                              # góc cần lúc nghỉ (thế giới)
CAN_L = R.dist(R.CAN_PIVOT, R.NUM)
LX_LOC = (R.Y_TD - R.LX[0][1], -(R.LX[0][0] - R.OX))                            # gốc lò xo trong hệ đầu
LX_L = R.LX[0][1] - R.LX[3][1]
LX_SEG = LX_L / 3
LAG = (0.0, 0.035, 0.075)     # trễ của ba khối
MOUTH = {"cuoi": 1, "nghien": 2, "rot_ham": 3, "o": 4, "meu": 5, "cuoi_to": 6}
EYE = {"thuong": 1, "xuong": 2, "loi": 3, "nham_chat": 4, "cuoi": 5, "chop": 6, "buon": 7, "sao": 8}


# ---------------------------------------------------------------- tiện ích nhịp
def clamp(x, a, b):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def kf(t, *keys):
    """Nội suy mềm giữa các khoá (t, v); ngoài khoảng thì giữ."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t < t1:
            return v0 + (v1 - v0) * ease((t - t0) / (t1 - t0))
    return keys[-1][1]


def hold(t, v0, *kv):
    """Giá trị bậc: v0 tới mốc đầu, rồi mỗi (t, v) giữ tới mốc sau."""
    v = v0
    for tk, vk in kv:
        if t >= tk - 1e-6:
            v = vk
    return v


def bump(x, c, r):
    """Gò cos² quanh c, bán kính r (bằng 0 ngoài khoảng)."""
    d = clamp((x - c) / r, -1.0, 1.0)
    return math.cos(d * math.pi / 2) ** 2


def flip(t, hz):
    """Hai dáng đổi nhau: +1 / −1, đổi hz lần mỗi giây."""
    return 1.0 if int(math.floor(t * hz + 1e-6)) % 2 == 0 else -1.0


def base():
    return dict(J=0.0, sq=1.0, lean=0.0, tilt=0.0, mx=0.0, drop=0.0, can=0.0, eye=1, mouth=1, eye_s=(1.0, 1.0), eye_xy=(0.0, 0.0),
                mouth_s=(1.0, 1.0), brow=0.0, brow_dy=0.0, den=(1.0, 0.0), foot_t=(0.0, 0.0, 0.0), foot_p=(0.0, 0.0, 0.0))


CLIPS = {}


def clip(name, dur, loop=False, events=()):
    def deco(f):
        CLIPS[name] = dict(name=name, dur=dur, loop=loop, fn=f, events=list(events))
        return f
    return deco


def bop(ph, amt=1.0):
    """Nhún một phách (ph 0..1): dập nhanh, bật vượt, về; bằng 0 ở hai đầu phách (ngoài 0,16..0,82)."""
    return 1.0 - 0.052 * amt * bump(ph, 0.30, 0.14) + 0.024 * amt * bump(ph, 0.62, 0.20)


# ---------------------------------------------------------------- clip
@clip("idle", 4.0, loop=True)
def c_idle(t):
    p = base()
    k = int(t / BEAT + 1e-6)
    ph = t / BEAT - k
    p["sq"] = bop(ph)
    p["lean"] = 3.0 * math.sin(2 * math.pi * t / 2.0)
    p["den"] = (1.0, 0.0) if k % 2 == 0 else (0.0, 1.0)
    # gõ mũi giày phải theo phách (phách 1, 2, 3, 5): nhấc mũi dần rồi dập đúng phách sau
    if k in (0, 1, 2, 4):
        p["foot_p"] = (0.0, 0.0, 15.0 * kf(ph, (0.35, 0), (0.80, 1), (0.93, 1), (1.0, 0)))
    # chớp mắt
    if 0.62 <= t < 0.72 or 2.20 <= t < 2.30:
        p["eye"] = EYE["chop"]
    # trò phá nhịp (giây 3,0 .. 3,6): nhìn xuống miệng, nhai bi bốn cái, mày nhướn
    if 2.92 <= t < 3.62:
        g = t - 3.0
        p["eye"] = EYE["xuong"] if g < 0 else EYE["cuoi"]
        p["brow"] = 9.0 * kf(t, (2.92, 0), (3.02, 1), (3.5, 1), (3.62, 0))
        if g >= 0:
            n = int(g / 0.125)
            p["mouth"] = MOUTH["nghien"] if n % 2 == 0 and n < 5 else MOUTH["cuoi"]
            f = (g / 0.125) % 1.0
            p["mouth_s"] = (1.0 + 0.05 * bump(f, 0.2, 0.3), 1.0 - 0.10 * bump(f, 0.2, 0.3)) if n < 5 else (1.0, 1.0)
            p["sq"] *= 1.0 - (0.018 * bump(f, 0.2, 0.3) if n < 5 else 0.0)
    return p


PULL_LEAD = 0.30   # = bo_cuc.json pull_lead: 0,3 s đầu Lão Mực với tay tới núm (clip sl_pull của Lão Mực chạy cùng lúc, cùng khung)


@clip("pull", 0.9, events=[(PULL_LEAD + 0.17, "keo")])
def c_pull(t):
    """Lão Mực giật cần. 0 .. 0,30: dõi bàn tay với tới núm, rụt nhẹ ra xa -> (từ đây như cũ, lùi 0,30 s) nghiêng ra xa cần -> bị
    giật về phía cần, bẹp -> bật lại quá đà -> về. Núm rời chỗ ở 0,37, tới đáy ở 0,47, được nhả ở 0,57."""
    p = base()
    u = t - PULL_LEAD
    watch = kf(t, (0, 0), (0.12, 1), (PULL_LEAD + 0.08, 1), (PULL_LEAD + 0.15, 0))
    p["sq"] = kf(u, (0, 1), (0.10, 1.045), (0.17, 0.83), (0.25, 0.85), (0.35, 1.09), (0.47, 1.0)) * (1.0 + 0.012 * watch)
    p["lean"] = kf(u, (0, 0), (0.10, -5.5), (0.17, 11), (0.25, 10), (0.35, -4.5), (0.47, 0)) - 2.2 * kf(t, (0, 0), (0.2, 1), (PULL_LEAD, 0))
    p["can"] = kf(u, (0.07, 0), (0.17, -105), (0.27, -100), (0.34, 0))
    p["eye"] = hold(u, EYE["loi"] if t > 0.06 else EYE["thuong"], (0.15, EYE["nham_chat"]), (0.36, EYE["xuong"]))
    p["eye_xy"] = (11.0 * watch, 7.0 * watch)
    p["mouth"] = hold(u, MOUTH["o"] if t > 0.06 else MOUTH["cuoi"], (0.15, MOUTH["nghien"]), (0.40, MOUTH["cuoi"]))
    p["brow"] = kf(u, (-0.24, 0), (-0.14, 10), (0.15, 10), (0.19, -8), (0.34, -8), (0.44, 4))
    p["brow_dy"] = kf(u, (-0.24, 0), (-0.14, 12), (0.15, 12), (0.19, -5), (0.36, 0))
    p["den"] = (1.0, 1.0) if 0.15 <= u < 0.30 else (1.0, 0.0)
    return p


@clip("spin", 0.5, loop=True)
def c_spin(t):
    """Cuộn đang chạy: lắc hai bên 2 lần mỗi giây, thân rung hai dáng, răng lập cập, mắt dõi xuống ô cuộn."""
    p = base()
    p["lean"] = 4.6 * math.sin(2 * math.pi * t / 0.5)
    p["tilt"] = 0.9 * flip(t, 16)
    p["sq"] = 1.0 + 0.026 * math.sin(2 * math.pi * t / 0.25)
    p["eye"] = EYE["xuong"]
    p["eye_xy"] = (7.0 * math.sin(2 * math.pi * t / 0.5), 0.0)
    p["brow"] = 4.0
    n = int(t / 0.125 + 1e-6)
    p["mouth"] = MOUTH["cuoi"] if n % 2 == 0 else MOUTH["nghien"]
    p["den"] = (1.0, 0.0) if n % 2 == 0 else (0.0, 1.0)
    p["can"] = 0.0
    return p


def stop_fn(dirn, amp, to_idle):
    def f(t):
        p = base()
        k = 1.0 if t < 0.066 else math.exp(-9 * (t - 0.066)) * math.cos(2 * math.pi * 4.2 * (t - 0.066))
        end = kf(t, (0.26 if not to_idle else 0.34, 1), (0.36 if not to_idle else 0.42, 0))   # tắt hẳn trước khi hết clip
        p["sq"] = 1.0 - 0.085 * amp * k * end
        p["lean"] = dirn * 6.5 * amp * math.exp(-7.5 * t) * math.cos(2 * math.pi * 3.4 * t) * end
        p["eye"] = hold(t, EYE["loi"], (0.12, EYE["xuong"]))
        p["eye_xy"] = (dirn * 10.0 * kf(t, (0, 1), (0.3, 1), (0.4, 0)) if not to_idle else 0.0, 0.0)
        p["mouth"] = hold(t, MOUTH["o"], (0.13, MOUTH["nghien"]), (0.30, MOUTH["cuoi"]))
        p["brow"] = kf(t, (0, 9), (0.12, 9), (0.25, 4))
        p["brow_dy"] = kf(t, (0, 10), (0.1, 10), (0.22, 0))
        p["den"] = (1.0, 1.0) if t < 0.1 else (1.0, 0.0)
        return p
    return f


CLIPS["stop_1"] = dict(name="stop_1", dur=0.4, loop=False, fn=stop_fn(-1.0, 0.8, False), events=[(0.0, "cach")])
CLIPS["stop_2"] = dict(name="stop_2", dur=0.4, loop=False, fn=stop_fn(1.0, 1.0, False), events=[(0.0, "cach")])
CLIPS["stop_3"] = dict(name="stop_3", dur=0.5, loop=False, fn=stop_fn(-1.0, 1.5, True), events=[(0.0, "cach")])


@clip("tease", 0.5, loop=True)
def c_tease(t):
    """Hai cuộn đầu đã khớp: nín thở, kiễng lên, run nhanh, mắt lồi dán vào cuộn cuối."""
    p = base()
    p["sq"] = 1.075 + 0.008 * flip(t, 16)
    p["tilt"] = 1.3 * flip(t, 16)
    p["eye"] = EYE["loi"]
    p["eye_s"] = (1.06, 1.06)
    p["eye_xy"] = (9.0, -4.0)
    p["brow"] = 12.0
    p["brow_dy"] = 12.0
    p["mouth"] = MOUTH["nghien"]
    n = int(t / 0.0625 + 1e-6)
    p["den"] = (1.0, 0.0) if n % 2 == 0 else (0.0, 1.0)
    return p


@clip("lose", 1.2)
def c_lose(t):
    """Trượt: nhổm lên hy vọng 3 khung -> xẹp, rũ sang một bên, thở dài -> về."""
    p = base()
    p["sq"] = kf(t, (0, 1), (0.10, 1.04), (0.30, 0.915), (0.60, 0.93), (0.85, 0.92), (1.05, 1.0))
    p["lean"] = kf(t, (0, 0), (0.12, 0), (0.34, 4.5), (0.85, 5.0), (1.05, 0))
    sad = 0.14 <= t < 0.98
    p["eye"] = EYE["loi"] if t < 0.14 else EYE["buon"] if sad else EYE["thuong"]
    p["mouth"] = MOUTH["o"] if t < 0.14 else MOUTH["meu"] if sad else MOUTH["cuoi"]
    p["brow"] = kf(t, (0, 8), (0.12, 8), (0.26, 16), (0.88, 16), (1.0, 0))
    p["brow_dy"] = kf(t, (0, 8), (0.12, 8), (0.26, -3), (0.88, -3), (1.0, 0))
    p["den"] = (0.0, 0.0) if sad else (1.0, 0.0)
    p["can"] = kf(t, (0.14, 0), (0.34, -14), (0.85, -16), (1.02, 0))     # cần rũ theo
    return p


def hop(h, amp, height):
    """Một cú nhảy (h giây kể từ lúc bắt đầu nén): trả (nén giãn, độ cao)."""
    sq = 1.0 + amp * (kf(h, (0, 1), (0.12, 0.83), (0.17, 0.83), (0.21, 1.16), (0.37, 1.02), (0.50, 1.08), (0.54, 0.83), (0.60, 0.85), (0.68, 1.05),
                         (0.76, 1.0)) - 1.0)
    j = amp * height * math.sin(math.pi * (h - 0.19) / 0.33) if 0.19 < h < 0.52 else 0.0
    return sq, j


@clip("win", 1.6, events=[(0.20, "nha_bi"), (0.84, "nha_bi")])
def c_win(t):
    """Trúng đường: nén -> nhảy hai cái (cái sau nhỏ hơn), cười to, đèn nháy."""
    p = base()
    for s0, a in ((0.0, 1.0), (0.64, 0.62)):
        h = t - s0
        if 0 <= h <= 0.76:
            sq, j = hop(h, a, 100.0)
            p["sq"] *= sq
            p["J"] += j
    on = t < 1.36
    p["eye"] = EYE["cuoi"] if on else EYE["thuong"]
    p["mouth"] = (MOUTH["nghien"] if (t < 0.17 or 0.64 <= t < 0.80) else MOUTH["cuoi_to"]) if on else MOUTH["cuoi"]
    p["brow"] = kf(t, (0, 0), (0.1, 8), (1.25, 8), (1.4, 0))
    p["brow_dy"] = kf(t, (0, 0), (0.1, 8), (1.25, 8), (1.4, 0))
    n = int(t / 0.0625 + 1e-6)
    p["den"] = ((1.0, 0.0) if n % 2 == 0 else (0.0, 1.0)) if on else (1.0, 0.0)
    p["can"] = kf(t, (0, 0), (0.19, 0), (0.30, -22), (0.50, 0), (0.83, 0), (0.94, -14), (1.1, 0))   # cần văng theo cú nhảy
    return p


@clip("jackpot", 4.0, events=[(0.56, "no"), (1.40, "het_no"), (1.50, "dap"), (2.0, "nha_bi")])
def c_jackpot(t):
    """Gồng bẹp run (0,5 s) -> vọt lên dài gầy -> treo trên không lắc 6 cái -> rơi bẹp rung màn -> nảy -> nhảy múa, vẫy cần -> về."""
    p = base()
    p["sq"] = kf(t, (0, 1), (0.10, 0.775), (0.50, 0.79), (0.56, 1.24), (0.85, 1.10), (1.30, 1.02), (1.47, 1.14), (1.50, 0.72), (1.62, 0.74),
                 (1.72, 1.13), (1.95, 1.0), (2.0, 0.88), (2.1, 1.0))
    if t < 0.5:                                    # gồng: run hai dáng
        p["tilt"] += 0.9 * flip(t, 16)
        p["lean"] += 1.2 * flip(t + 0.03, 16)
    if 0.52 < t < 1.5:
        p["J"] += kf(t, (0.52, 0), (0.85, 185), (1.05, 198), (1.30, 185), (1.5, 0))   # nhảy vừa tầm màn (máy cao gần hết màn)
    if 0.82 < t < 1.34:                            # treo trên không, lắc
        s = flip(t - 0.82, 8)
        e = kf(t, (0.82, 0), (0.86, 1), (1.30, 1), (1.34, 0))
        p["lean"] += 10.0 * s * e
        p["tilt"] += 6.0 * s * e
    if 1.72 < t < 2.0:
        p["J"] += 62.0 * math.sin(math.pi * (t - 1.72) / 0.28)
    dance = 2.1 < t < 3.6
    if dance:
        d = t - 2.1
        e = kf(t, (2.1, 0), (2.2, 1), (3.35, 1), (3.6, 0))
        p["lean"] += 9.0 * e * math.sin(2 * math.pi * 2 * d)
        p["sq"] *= 1.0 - 0.06 * e * abs(math.sin(2 * math.pi * 2 * d))
        p["J"] += 34.0 * e * abs(math.sin(2 * math.pi * 2 * d))
        p["can"] = e * (-28.0 + 24.0 * math.sin(2 * math.pi * 2 * d + 0.6))        # vẫy cần như vẫy tay
    # mặt
    p["eye"] = hold(t, EYE["nham_chat"], (0.52, EYE["loi"]), (0.84, EYE["sao"]), (1.48, EYE["nham_chat"]), (1.70, EYE["cuoi"]), (2.6, EYE["sao"]),
                    (3.1, EYE["cuoi"]), (3.62, EYE["thuong"]))
    p["mouth"] = hold(t, MOUTH["nghien"], (0.52, MOUTH["rot_ham"]), (1.48, MOUTH["nghien"]), (1.70, MOUTH["cuoi_to"]), (3.62, MOUTH["cuoi"]))
    p["eye_s"] = (kf(t, (0.5, 1), (0.56, 1.25), (0.84, 1.12), (1.45, 1.12), (1.5, 1)),) * 2
    p["brow"] = kf(t, (0, 0), (0.08, -9), (0.5, -9), (0.56, 12), (1.45, 12), (1.5, -6), (1.7, 8), (3.5, 8), (3.65, 0))
    p["brow_dy"] = kf(t, (0, 0), (0.08, -6), (0.5, -6), (0.56, 30), (1.45, 26), (1.5, -4), (1.7, 8), (3.5, 8), (3.65, 0))
    n = int(t / 0.0625 + 1e-6)
    if t < 0.5:
        p["den"] = (0.0, 0.0)
    elif t < 1.5:
        p["den"] = (1.0, 1.0) if n % 2 == 0 else (0.0, 0.0)
    elif t < 3.62:
        p["den"] = (1.0, 0.0) if (n // 2) % 2 == 0 else (0.0, 1.0)
    return p


@clip("free", 1.2, events=[(0.2, "mien_phi")])
def c_free(t):
    """Ba Rương: tự giật cần hai cái liền, mắt sao, cười to."""
    p = base()
    p["can"] = kf(t, (0.08, 0), (0.18, -85), (0.26, -80), (0.36, 0), (0.46, 0), (0.56, -85), (0.64, -80), (0.74, 0))
    p["lean"] = kf(t, (0, 0), (0.08, -4), (0.18, 9), (0.28, 8), (0.38, -4), (0.46, -3), (0.56, 9), (0.66, 8), (0.76, -3), (0.92, 0))
    p["sq"] = kf(t, (0, 1), (0.08, 1.04), (0.18, 0.87), (0.28, 0.89), (0.38, 1.07), (0.46, 1.03), (0.56, 0.87), (0.66, 0.89), (0.76, 1.07), (0.92, 1.0))
    on = t < 0.98
    p["eye"] = EYE["sao"] if on else EYE["thuong"]
    p["mouth"] = MOUTH["cuoi_to"] if on else MOUTH["cuoi"]
    p["brow"] = kf(t, (0, 0), (0.1, 8), (0.9, 8), (1.0, 0))
    p["brow_dy"] = kf(t, (0, 0), (0.1, 10), (0.9, 10), (1.0, 0))
    n = int(t / 0.0625 + 1e-6)
    p["den"] = ((1.0, 1.0) if n % 2 == 0 else (0.0, 0.0)) if on else (1.0, 0.0)
    return p


@clip("appear", 1.4, events=[(0.5, "chao")])
def c_appear(t):
    """Vào lều: đang ngủ gật (xẹp, nghiêng, ngáy) -> giật mình bật lên -> đáp, nhe răng cười."""
    p = base()
    sn = math.sin(2 * math.pi * t / 0.5)
    p["sq"] = kf(t, (0, 0.90 + 0.012 * sn), (0.44, 0.905 + 0.012 * sn), (0.50, 0.84), (0.56, 1.22), (0.78, 1.04), (0.86, 0.86), (0.92, 0.88),
                 (1.02, 1.05), (1.14, 1.0))
    p["lean"] = kf(t, (0, -6.5), (0.46, -6.5), (0.56, 2), (0.9, 0))
    if 0.52 < t < 0.86:
        p["J"] = 70.0 * math.sin(math.pi * (t - 0.52) / 0.34)
    p["eye"] = hold(t, EYE["chop"], (0.48, EYE["loi"]), (0.90, EYE["chop"]), (0.98, EYE["thuong"]))
    p["mouth"] = hold(t, MOUTH["o"], (0.88, MOUTH["nghien"]), (1.04, MOUTH["cuoi"]))
    p["mouth_s"] = ((0.8 + 0.12 * sn,) * 2) if t < 0.48 else (1.0, 1.0)
    p["brow"] = kf(t, (0, 12), (0.46, 12), (0.52, 10), (0.9, 6), (1.05, 0))
    p["brow_dy"] = kf(t, (0, -4), (0.46, -4), (0.52, 26), (0.86, 18), (1.0, 0))
    p["den"] = (0.0, 0.0) if t < 0.5 else (1.0, 1.0) if t < 0.9 else (1.0, 0.0)
    p["can"] = kf(t, (0, -12), (0.46, -12), (0.56, 10), (0.8, 0))
    return p


# ---------------------------------------------------------------- bộ nướng
def rot(a, x, y):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return c * x - s * y, s * x + c * y


def kin(c, t):
    """Dáng động học tại giờ t: tham số (có trễ theo khối) + toạ độ thế giới các điểm tựa của chân, cần, lò xo."""
    dur, fn = c["dur"], c["fn"]

    def at(tt):
        return fn(tt % dur) if c["loop"] else fn(clamp(tt, 0.0, dur))

    p = at(t)
    ps = [p, at(t - LAG[1]), at(t - LAG[2])]
    sv = [q["sq"] for q in ps]
    sh = [1.0 + (1.0 / s - 1.0) * 0.55 for s in sv]
    r = [-(p["tilt"] + 0.30 * p["lean"]), -0.35 * ps[1]["lean"], -0.35 * ps[2]["lean"]]
    hy = -p["drop"] - ((1.0 - sv[0]) * 260.0 if sv[0] < 1 else (1.0 - sv[0]) * 120.0)
    hx = HIP_Y * math.sin(math.radians(p["tilt"])) + p["mx"]
    hip = (hx, p["J"] + HIP_Y + hy)
    a0 = 90.0 + r[0]
    dx, dy = rot(a0, L_B * sv[0], 0.0)
    tam = (hip[0] + dx, hip[1] + dy)
    a1 = a0 + r[1]
    dx, dy = rot(a1, L_P * sv[1], 0.0)
    dau = (tam[0] + dx, tam[1] + dy)
    a2 = a1 + r[2]
    out = dict(p=p, sv=sv, sh=sh, r=r, hip=hip, a=(a0, a1, a2), move=(0.0, p["J"]), hip_t=(hx, hy))
    for s in ("t", "p"):
        dx, dy = rot(a0, SOCK[s][0] * sv[0], SOCK[s][1] * sh[0])
        out["sock_" + s] = (hip[0] + dx, hip[1] + dy)
    dx, dy = rot(a1, CAN_LOC[0] * sv[1], CAN_LOC[1] * sh[1])
    out["can_pivot"] = (tam[0] + dx, tam[1] + dy)
    out["can_ang"] = a1 + (CAN_A0 - 90.0) + p["can"]
    dx, dy = rot(a2, LX_LOC[0] * sv[2], LX_LOC[1] * sh[2])
    out["lx_base"] = (dau[0] + dx, dau[1] + dy)
    out["lx_ang"] = a2
    return out


class Tip:
    """Đầu mút lò xo tắt dần đuổi theo điểm đích."""

    def __init__(self, k, c):
        self.k, self.c, self.p, self.v = k, c, None, (0.0, 0.0)

    def step(self, q, dt):
        if self.p is None:
            self.p = q
            return
        ax = self.k * (q[0] - self.p[0]) - self.c * self.v[0]
        ay = self.k * (q[1] - self.p[1]) - self.c * self.v[1]
        self.v = (self.v[0] + ax * dt, self.v[1] + ay * dt)
        self.p = (self.p[0] + self.v[0] * dt, self.p[1] + self.v[1] * dt)

    def keep(self, base, ang, L, lo, hi):
        """Giữ đầu mút ở phía trước gốc: khoảng cách dọc trục trong [lo, hi] x L (gốc vọt qua đầu mút thì góc lật 180 độ)."""
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        dx, dy = self.p[0] - base[0], self.p[1] - base[1]
        a, l = dx * c + dy * s, -dx * s + dy * c
        a2 = clamp(a, lo * L, hi * L)
        if a2 != a:
            va = self.v[0] * c + self.v[1] * s
            vl = -self.v[0] * s + self.v[1] * c
            va = 0.0 if (a < a2) == (va < 0) else va
            self.v = (va * c - vl * s, va * s + vl * c)
            self.p = (base[0] + a2 * c - l * s, base[1] + a2 * s + l * c)


def wrap(a):
    return (a + 180.0) % 360.0 - 180.0


def leg_points(S, A, side):
    """Ống chân từ gốc S tới cổ chân A: thẳng nếu đủ xa, ngắn hơn độ dài ống thì phình cong ra ngoài (dài ống giữ nguyên)."""
    dx, dy = A[0] - S[0], A[1] - S[1]
    d = max(1.0, math.hypot(dx, dy))
    h = 0.0
    if d < LEG_L:
        h = min(0.62 * LEG_L, d * math.sqrt(0.375 * (LEG_L / d - 1.0)))
    nx, ny = -dy / d, dx / d
    if nx * side < 0:
        nx, ny = -nx, -ny
    cx, cy = (S[0] + A[0]) / 2 + nx * 2 * h, (S[1] + A[1]) / 2 + ny * 2 * h
    pts = []
    for i in range(R.NLEG + 1):
        u = i / R.NLEG
        pts.append(((1 - u) ** 2 * S[0] + 2 * u * (1 - u) * cx + u * u * A[0], (1 - u) ** 2 * S[1] + 2 * u * (1 - u) * cy + u * u * A[1]))
    return pts


def bake(name):
    c = CLIPS[name]
    dur = c["dur"]
    n = int(round(dur * FPS))
    dt = 1.0 / (FPS * SUB)
    pre = 2 * dur if c["loop"] else 0.5
    tip_can, tip_lx = Tip(1500.0, 22.0), Tip(760.0, 15.0)
    shoe = {s: dict(p=ANK[s], v=(0.0, 0.0)) for s in ("t", "p")}
    frames = []
    steps = int(round((pre + dur) * FPS * SUB))
    for i in range(steps + 1):
        t = -pre + i * dt
        tt = t if c["loop"] else max(t, 0.0)
        K = kin(c, tt)
        # cần, lò xo: đầu mút đuổi theo dáng động học
        qc = (K["can_pivot"][0] + CAN_L * math.cos(math.radians(K["can_ang"])), K["can_pivot"][1] + CAN_L * math.sin(math.radians(K["can_ang"])))
        ql = (K["lx_base"][0] + LX_L * math.cos(math.radians(K["lx_ang"])), K["lx_base"][1] + LX_L * math.sin(math.radians(K["lx_ang"])))
        tip_can.step(qc, dt)
        tip_lx.step(ql, dt)
        tip_can.keep(K["can_pivot"], K["can_ang"], CAN_L, 0.85, 1.1)
        tip_lx.keep(K["lx_base"], K["lx_ang"], LX_L, 0.6, 1.6)
        # giày: trên đất thì ghim; thân lên cao quá tầm ống chân thì treo theo gốc ống (lò xo)
        for s in ("t", "p"):
            S = K["sock_" + s]
            hang = (ANK[s][0] + (S[0] - (-SOCK[s][1])), S[1] - LEG_L - 2.0)
            st = shoe[s]
            if hang[1] <= ANK[s][1] + 0.5:
                st["p"], st["v"] = ANK[s], (0.0, 0.0)
            else:
                ax = 900.0 * (hang[0] - st["p"][0]) - 34.0 * st["v"][0]
                ay = 900.0 * (hang[1] - st["p"][1]) - 34.0 * st["v"][1]
                st["v"] = (st["v"][0] + ax * dt, st["v"][1] + ay * dt)
                st["p"] = (st["p"][0] + st["v"][0] * dt, max(ANK[s][1], st["p"][1] + st["v"][1] * dt))
                if st["p"][1] <= ANK[s][1] + 1e-6 and st["v"][1] < 0:
                    st["v"] = (0.0, 0.0)
        if i % SUB == 0 and t >= -1e-9:
            frames.append((round(t, 5), K, tip_can.p, tip_lx.p, {s: shoe[s]["p"] for s in ("t", "p")}))
    frames = frames[:n + 1]
    # ---- khoá ----
    T = {}       # (xương, prop) -> [(t, giá trị)]
    A = {}       # slot -> [(t, tên hình)]
    AL = {}      # slot -> [(t, alpha)]
    prev_ang = {}

    def add(b, prop, t, v):
        T.setdefault((b, prop), []).append((t, v))

    def add_rot(b, t, v):
        if b in prev_ang:
            v = prev_ang[b] + wrap(v - prev_ang[b])
        prev_ang[b] = v
        add(b, "rotate", t, v)

    c["num_path"] = []
    for t, K, pc, pl, sh_pos in frames:
        p, sv, sh, r = K["p"], K["sv"], K["sh"], K["r"]
        add("move", "translate", t, K["move"])
        add("hip", "translate", t, K["hip_t"])
        add_rot("hip", t, r[0])
        add("tam", "translate", t, ((sv[0] - 1.0) * L_B, 0.0))
        add_rot("tam", t, r[1])
        add("dau", "translate", t, ((sv[1] - 1.0) * L_P, 0.0))
        add_rot("dau", t, r[2])
        for b, k in (("hip_d", 0), ("tam_d", 1), ("dau_d", 2)):
            add(b, "scale", t, (sv[k], sh[k]))
        # mặt (xương con của xương da: hệ cha có trục x hướng lên, y hướng sang trái)
        add("mat", "translate", t, (p["eye_xy"][1], -p["eye_xy"][0]))
        add("mat", "scale", t, p["eye_s"])
        add("mieng", "scale", t, p["mouth_s"])
        add("may_t", "translate", t, (p["brow_dy"], 0.0))
        add("may_p", "translate", t, (p["brow_dy"], 0.0))
        add_rot("may_t", t, p["brow"])
        add_rot("may_p", t, -p["brow"])
        A.setdefault("mat", []).append((t, f"mat_{p['eye']:02d}"))
        A.setdefault("mieng", []).append((t, f"mieng_{p['mouth']:02d}"))
        for sl, v in (("den_a_d", p["den"][0]), ("den_a_h", p["den"][0]), ("den_b_d", p["den"][1]), ("den_b_h", p["den"][1])):
            AL.setdefault(sl, []).append((t, v))
        # cần: trục bám tấm đã co giãn; góc động học + độ uốn của lò xo chia cho ba đốt
        add("can1", "translate", t, ((sv[1] - 1.0) * CAN_LOC[0], (sh[1] - 1.0) * CAN_LOC[1]))
        flex = clamp(wrap(math.degrees(math.atan2(pc[1] - K["can_pivot"][1], pc[0] - K["can_pivot"][0])) - K["can_ang"]), -38.0, 38.0)
        add_rot("can1", t, p["can"] + 0.40 * flex)
        add_rot("can2", t, 0.75 * flex)
        add_rot("can3", t, 0.95 * flex)
        # tâm núm (thế giới) theo đúng ba đốt vừa đặt: cho tay Lão Mực bám (clip_d5.py)
        ca, kx, ky = K["can_ang"], K["can_pivot"][0], K["can_pivot"][1]
        for d_ in (0.40 * flex, 0.75 * flex, 0.95 * flex):
            ca += d_
            kx += CAN_L / 3 * math.cos(math.radians(ca))
            ky += CAN_L / 3 * math.sin(math.radians(ca))
        c["num_path"].append((t, round(kx, 2), round(ky, 2)))
        # lò xo ăng ten: uốn + co giãn
        add("lx1", "translate", t, ((sv[2] - 1.0) * LX_LOC[0], (sh[2] - 1.0) * LX_LOC[1]))
        vx, vy = pl[0] - K["lx_base"][0], pl[1] - K["lx_base"][1]
        flex = 42.0 * math.tanh(wrap(math.degrees(math.atan2(vy, vx)) - K["lx_ang"]) / 42.0)
        st = clamp(math.hypot(vx, vy) / LX_L, 0.55, 1.6)
        add_rot("lx1", t, 0.30 * flex)
        add_rot("lx2", t, 0.55 * flex)
        add_rot("lx3", t, 0.75 * flex)
        add_rot("sao", t, -0.6 * flex)
        for b in ("lx2", "lx3", "sao"):
            add(b, "translate", t, ((st - 1.0) * LX_SEG, 0.0))
        # chân + giày (toạ độ thế giới)
        for s in ("t", "p"):
            f = p["foot_" + s]
            Apos = (sh_pos[s][0] + f[0], sh_pos[s][1] + f[1])
            lift = Apos[1] - ANK[s][1]
            srot = f[2] + SIDE[s] * min(20.0, max(0.0, lift - f[1]) * 0.25) + (-p["tilt"] if lift > 2 else 0.0)   # rời đất: mũi giày (đầu ngoài) chúc xuống
            add("giay_" + s, "translate", t, (Apos[0] - ANK[s][0], lift))
            add_rot("giay_" + s, t, srot)
            pts = leg_points(K["sock_" + s], (Apos[0], Apos[1] + 6.0), SIDE[s])
            S0 = (-SOCK[s][1], HIP_Y + SOCK[s][0])
            add(f"chan_{s}1", "translate", t, (pts[0][0] - S0[0], pts[0][1] - S0[1]))
            pa = -90.0
            for k in range(R.NLEG):
                a = math.degrees(math.atan2(pts[k + 1][1] - pts[k][1], pts[k + 1][0] - pts[k][0]))
                add_rot(f"chan_{s}{k + 1}", t, wrap(a - pa))
                pa = a
                if k > 0:
                    ln = math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])
                    add(f"chan_{s}{k + 1}", "translate", t, (ln - SEG, 0.0))
    return c, T, A, AL


def fmt(v):
    if isinstance(v, tuple):
        return ",".join(f"{x:.3f}".rstrip("0").rstrip(".") for x in v)
    return f"{v:.3f}".rstrip("0").rstrip(".")


def atom(*args, check=True):
    r = subprocess.run(CLI + list(args) + ["-p", ATOM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        print(out[-1500:])
        raise SystemExit(f"atom {' '.join(args[:2])} lỗi")
    return out


def ops_for(name, report):
    c, T, A, AL = bake(name)
    L = [f"anim.add {name} dur={c['dur']} loop={'true' if c['loop'] else 'false'}"]
    worst = (0.0, "")
    for (b, prop), ks in T.items():
        dflt = (1.0, 1.0) if prop == "scale" else (0.0, 0.0) if prop == "translate" else 0.0
        if all((abs(v[0] - dflt[0]) < 1e-4 and abs(v[1] - dflt[1]) < 1e-4) if isinstance(v, tuple) else abs(v - dflt) < 1e-4 for _, v in ks):
            continue
        if prop == "rotate":
            for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
                if abs(v1 - v0) > worst[0]:
                    worst = (abs(v1 - v0), f"{b} t={t0:.2f}")
        L.append(f"key {name} {b}.{prop} " + " ".join(f"{t:.4f}:{fmt(v)}" for t, v in ks))
    for sl, ks in A.items():
        out = [ks[0]] + [k for k0, k in zip(ks, ks[1:]) if k[1] != k0[1]]
        L.append(f"key {name} {sl}.attachment " + " ".join(f"{t:.4f}:{a}" for t, a in out))
    for sl, ks in AL.items():
        out = [ks[0]]
        for k0, k in zip(ks, ks[1:]):
            if k[1] != k0[1]:
                if out[-1][0] != k0[0]:
                    out.append(k0)
                out.append(k)
        if out[-1][0] != ks[-1][0]:
            out.append(ks[-1])
        L.append(f"key {name} {sl}.alpha " + " ".join(f"{t:.4f}:{fmt(v)}:stepped" for t, v in out))
    for t, ev in c["events"]:
        L.append(f"event {name} {t} {ev}")
    L.append(f"anim.reduce {name} tol=0.08")
    report.append(f"{name:9s} dur {c['dur']:.1f}  bước xoay lớn nhất {worst[0]:5.1f} độ/khung ({worst[1]})")
    return L


def main():
    names = [a for a in sys.argv[1:] if a in CLIPS] or list(CLIPS)
    existing = atom("q", "anims", "--limit", "200", check=False)
    have_ev = atom("q", "events", check=False)
    L, report = [], []
    for ev in sorted({e for c in CLIPS.values() for _, e in c["events"]}):
        if ev not in have_ev.split():
            L.append(f"event.add {ev}")
    for n in names:
        if any(line.split()[0] == n for line in existing.splitlines() if line.strip()):
            L.append(f"anim.del {n}")
        L += ops_for(n, report)
    path = os.path.join(ATOM, "ops", "10_clip.ops")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(atom("do", "-f", path).splitlines()[-1][:200], "|", len(L), "dòng")
    print("\n".join(report))
    if "pull" in names:   # đường đi của núm cần trong clip pull (thế giới rig máy quả), 30 khung/giây
        json.dump({"fps": FPS, "lead": PULL_LEAD, "pull": CLIPS["pull"]["num_path"]}, open(os.path.join(ATOM, "duong_num.json"), "w"))


if __name__ == "__main__":
    main()
