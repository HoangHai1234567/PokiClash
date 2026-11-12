# -*- coding: utf-8 -*-
"""Tinh linh tượng đá cổ giữ rừng: clip RIÊNG theo ý người dùng (2026-11-12), dựng ở tầng điều khiển của rig gốc monster_3423 rồi để
runtime Spine thật nướng (cách của tinh_linh_clip.py / xuong_rong_clip.py; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng:
- idle: giống con gốc.                      - walk: giống họ (run_01).
- appear: từng bộ phận bay vào xếp thành hình.
- đánh thường: lao tới đấm vòng một phát.
- chiêu mana: đưa hai tay lên trước, bắn hai bàn tay vào đối thủ. Sửa cùng ngày sau khi xem rig: "bắn cả phần này nữa chứ không chỉ ngón tay"
  (ảnh chụp cả tảng cẳng tay + đai rễ + ngón) → thứ bay đi là CẢ TẢNG CẲNG TAY kèm bàn tay; ở lại chỉ còn tấm vai và mấy viên đá nhỏ.
- chiêu cuối: đưa hai tay lên trời, xoè bàn tay tụ một quả cầu năng lượng (VFX: gió / lá bị hút vào cầu), rồi hai tay đổ về trước ném.
- die: lõi tắt ngỏm, chân tay từ đó rụng rời.

Rig gốc: FK thuần (4 IK tay mặc định tắt, không dùng), MỌI mảnh cứng bám một xương:
  bone > bone31 > bone2 (THÂN: vòng ngực dưới + vỏ sau; con: ba chóp đá bone24-26, pha lê lõi bone27, khoá bone43)
  bone2 > bone3 > bone4 (ngực trên) > bone30 (vòng ngực trên), bone5 (quả cầu cổ) > bone6 (mào đầu), bone44 (đai vai)
  bone44 > bone7 > bone17 (bắp tay GẦN, vô hình; con: tấm vai bone28, ba pha lê nhỏ bone36-38) > bone18 (tảng cẳng tay + đai) > bone19
          (bàn tay) > ngón bone20, 21, 22 > bone23
  bone44 > bone9 > bone10 (bắp tay XA; tấm vai bone29, bốn pha lê nhỏ bone39-42) > bone11 (cẳng tay) > bone12 (bàn tay) > ngón bone13, 14,
          15 > bone16
Tay GẦN (R của họ) ở bên TRÁI người xem, vẽ trước thân; tay XA (L) ở bên phải, vẽ sau thân. Con nhìn sang PHẢI.
Bộ mảnh THỨ HAI (slot P_*2.., mặc định trống): mỗi mảnh / cụm mảnh một xương rời là con của `bone` (đặt cao hơn 811,4 đơn vị): họ dùng
cho die_01 (rã ra rơi thành đống). Mình dùng bộ này cho td_die và td_appear (đặt từng mảnh trong hệ thế giới).

Kênh riêng cho rig của MÌNH (rig gốc không có): loi 0..1 (lõi sáng / tắt), cau = (bán kính 0..1, x, y thế giới) quả cầu năng lượng,
ban = quãng bay 0..1 của hai tảng cẳng tay (game co theo khoảng cách đối thủ), bay = cung dời xương move.

    tuong_da_clip.py dung                 ghép, ghi <scan>/lam_clip/td_extra.json
    tuong_da_clip.py xem [clip,..] [n] [view] [t0] [t1]   tờ khung trên rig gốc → <scan>/lam_clip/khung/<clip>.jpg
    tuong_da_clip.py song                 trang xem SỐNG (runtime Spine thật, 60 khung/giây) → <scan>/lam_clip/xem/xem.html
    tuong_da_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (tuong_da_rig.py đọc)
Chạy qua quai/khoa.py chrome (xem, mau mở Chrome ngầm)."""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MON = "monster_3423"
FPS = 30.0


def sxs():
    for p in [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"D:\RefAnimation\SwordxStaff", r"E:\Ripper\SwordxStaff"]:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


SCAN = os.path.join(sxs(), "scan", MON)
RIG = os.path.join(sxs(), "web", "assets", "Monster", MON)
LAM = os.path.join(SCAN, "lam_clip")
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
A = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
TEN = [b["name"] for b in I["bones"]]
PA = [b["parent"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
SLOT = [s["name"] for s in I["slots"]]
ix = TEN.index
N = len(TEN)
DY2 = 811.385                                   # bộ mảnh thứ hai đặt cao hơn bộ chính chừng này
DAT = 6.0                                       # mặt đất (y thế giới): mảnh rơi nằm ở đây

TAY = {"R": dict(vai="bone17", tam="bone28", cang="bone18", ban="bone19", ngon=["bone20", "bone21", "bone22", "bone23"],
                 pl=["bone36", "bone37", "bone38"]),
       "L": dict(vai="bone10", tam="bone29", cang="bone11", ban="bone12", ngon=["bone13", "bone14", "bone15", "bone16"],
                 pl=["bone39", "bone40", "bone41", "bone42"])}


# ---------------------------------------------------------------- động học thuận
def ma(x, y, rot, sx=1.0, sy=1.0):
    r = math.radians(rot)
    c, s = math.cos(r), math.sin(r)
    return np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0, 0, 1.0]])


def fk(u):
    W = [None] * N
    for i in range(N):
        L = ma(*u[i])
        W[i] = L if PA[i] < 0 else W[PA[i]] @ L
    return W


def goc_cua(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def tach(M):
    sx = math.hypot(M[0, 0], M[1, 0])
    sy = math.hypot(M[0, 1], M[1, 1])
    if M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0] < 0:
        sy = -sy
    return [M[0, 2], M[1, 2], goc_cua(M), sx, sy]


def gan(a, moc):
    """đưa góc a về gần góc mốc (cùng nhánh 360)."""
    return a - 360.0 * round((a - moc) / 360.0)


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y riêng; ex = kênh riêng của rig mình; tu_do = {xương bộ
    hai: (ma trận thế giới mong muốn, độ đậm)} khi dùng bộ mảnh thứ hai (None = bộ chính)."""

    def __init__(self, u, ex=None, tu_do=None):
        self.u = u
        self.ex = dict(loi=1.0, cau=(0.0, 0.0, 0.0), ban=(0.0, 0.0), ban_them=((0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 1.0, 0.0))) if ex is None else dict(ex)
        self.tu_do = tu_do

    def chep(self):
        return Dang(self.u.copy(), self.ex, self.tu_do)

    def W(self, ten):
        return fk(self.u)[ix(ten)]

    def vt(self, ten):
        M = self.W(ten)
        return np.array([M[0, 2], M[1, 2]])

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self

    def co(self, ten, sx, sy=None):
        self.u[ix(ten), 3] *= sx
        self.u[ix(ten), 4] *= sx if sy is None else sy
        return self

    def dat(self, ten, vt=None, goc=None):
        """đặt vị trí / góc THẾ GIỚI cho một xương (xương cha phải đặt xong trước)."""
        i = ix(ten)
        W = fk(self.u)
        Wp = W[PA[i]]
        if vt is not None:
            q = np.linalg.solve(Wp, np.array([vt[0], vt[1], 1.0]))
            self.u[i, 0], self.u[i, 1] = q[0], q[1]
        if goc is not None:
            self.u[i, 2] = gan(goc - goc_cua(Wp), self.u[i, 2])
        return self


_S = None


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float)) for c, v in S.items()}
    return _S


def dk(clip, t, lap=False):
    dur, U = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w)


def nghi():
    return dk("idle_01", 0.0)


# ---------------------------------------------------------------- đường cong
def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def thang(x):
    return min(1.0, max(0.0, x))


def vot(x, s=1.70158):
    """êm ra có vọt quá (back ease-out)."""
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def cong(moc, t, kieu=None):
    """nội suy theo các mốc (t, giá trị); giá trị là số hoặc bộ số; kieu[i] = hàm làm êm của đoạn i (mặc định em)."""
    if t <= moc[0][0]:
        return np.array(moc[0][1], float) if not np.isscalar(moc[0][1]) else moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            w = (kieu[i] if kieu and kieu[i] else em)(w)
            if np.isscalar(x):
                return x + (y - x) * w
            return np.array(x, float) + (np.array(y, float) - np.array(x, float)) * w
    return np.array(moc[-1][1], float) if not np.isscalar(moc[-1][1]) else moc[-1][1]


def rung(t, t0, bien, tan=0.25, hz=7.0, pha=0.0):
    """dao động tắt dần bắt đầu ở t0."""
    if t < t0:
        return 0.0
    x = t - t0
    return bien * math.exp(-x / tan) * math.sin(2 * math.pi * hz * x + pha)


def giat(t, bien, hz=22.0, pha=0.0):
    """rung giật đều (gồng, tụ lực)."""
    return bien * math.sin(2 * math.pi * hz * t + pha)


# ---------------------------------------------------------------- dáng nghỉ và các điểm mốc (thế giới, khung 0 idle)
D0 = nghi()
W0 = fk(D0.u)
NGUC0 = np.array([W0[ix("bone4")][0, 2], W0[ix("bone4")][1, 2]])
NGHI = {b: dict(vt=np.array([W0[ix(TAY[b]["cang"])][0, 2], W0[ix(TAY[b]["cang"])][1, 2]]) - NGUC0, goc=goc_cua(W0[ix(TAY[b]["cang"])]),
                vai=goc_cua(W0[ix(TAY[b]["vai"])])) for b in "RL"}
DAI_CANG = {"R": 181.8, "L": 168.1}             # gốc cẳng tay → bàn tay


def than(D, dx=0.0, dy=0.0, goc=0.0, dau=0.0, nguc=0.0):
    """cả con: dời (dx, dy) và nghiêng `goc` quanh tâm thân (bone2; dương = ngả ra sau / sang trái); `nguc` nghiêng thêm nửa trên
    (bone3: ngực, cổ, đầu, hai tay); `dau` nghiêng thêm riêng mào đầu."""
    D.doi("bone2", dx, dy)
    D.xoay("bone2", goc)
    D.xoay("bone3", nguc)
    D.xoay("bone6", dau)
    return D


def tay(D, ben, vt, goc, vai=0.6, tam=0.55, co=1.0):
    """đặt TẢNG CẲNG TAY trong hệ thế giới: gốc cẳng tay ở ngực + vt, trục cẳng tay (gốc → bàn tay) chĩa góc `goc`. Bắp tay (vô hình,
    mang tấm vai và pha lê nhỏ) quay `vai` phần về phía cẳng tay; tấm vai chỉ quay `tam` phần của bắp tay. Bàn tay, ngón đi theo."""
    T = TAY[ben]
    P = D.vt("bone4") + np.asarray(vt, float)
    iv = ix(T["vai"])
    Wv = fk(D.u)[iv]
    O = np.array([Wv[0, 2], Wv[1, 2]])
    a0 = goc_cua(Wv)
    at = math.degrees(math.atan2(P[1] - O[1], P[0] - O[0]))
    d = (gan(at, a0) - a0) * vai
    D.u[iv, 2] += d
    D.u[ix(T["tam"]), 2] -= d * (1 - tam)
    D.dat(T["cang"], P, goc)
    if co != 1.0:
        D.co(T["cang"], co)
    return D


def xoe(D, ben, v):
    """xoè bàn tay (v > 0: các ngón toả ra xa lòng bàn tay) hoặc nắm chặt (v < 0)."""
    T = TAY[ben]
    quat = [-24.0, 0.0, 26.0]
    for n, q in zip(T["ngon"][:3], quat):
        i = ix(n)
        D.u[i, 0] += B0[i, 0] * 0.34 * v
        D.u[i, 1] += B0[i, 1] * 0.34 * v
        D.u[i, 2] += q * v
    D.u[ix(T["ngon"][3]), 2] += 18.0 * v
    return D


def pha_le(D, ben, dx, dy, lech=0.0):
    """các mảnh pha lê nhỏ giữa vai và cẳng tay trôi thêm (dx, dy) thế giới, mỗi mảnh lệch pha một chút."""
    W = fk(D.u)
    for k, n in enumerate(TAY[ben]["pl"]):
        i = ix(n)
        f = 1.0 + lech * (k - 1)
        D.dat(n, (W[i][0, 2] + dx * f, W[i][1, 2] + dy * f))
    return D


def nhip_loi(D, t, chu_ky=1.0, bien=0.06):
    """nhịp đập của lõi (pha lê giữa ngực phồng nhẹ hai nhịp 'thình thịch' mỗi chu kỳ); bằng 0 ở t = 0."""
    x = (t % chu_ky) / chu_ky
    v = math.exp(-((x - 0.30) / 0.045) ** 2) + 0.6 * math.exp(-((x - 0.46) / 0.045) ** 2)
    D.co("bone27", 1 + bien * v)
    return D


# ---------------------------------------------------------------- idle (2 s, như họ) + nhịp lõi; walk = run_01; hit = hit_01
I_DUR = nap()["idle_01"][0]
W_DUR = nap()["run_01"][0]
H_DUR = nap()["hit_01"][0]


def idle(t):
    return nhip_loi(dk("idle_01", t, True), t, 1.0)


def walk(t):
    return nhip_loi(dk("run_01", t, True), t, W_DUR / 2)


def hit(t):
    return dk("hit_01", t)


# ---------------------------------------------------------------- đánh thường: lao tới, đấm vòng một phát bằng tay gần
A_DUR = 1.40
A_LAO0, A_LAO1 = 0.20, 0.46        # quãng lao
A_DAM, A_TRUNG = 0.46, 0.58        # vung đấm → trúng
A_VE0, A_VE1 = 0.78, 1.12          # lùi về
A_XA = 430.0                       # lao xa chừng này (đơn vị con gốc; game kéo tới đối thủ)


def attack_bay(t):
    x = cong([(0, 0.0), (A_LAO0, -26.0), (A_LAO1, A_XA * 0.86), (A_TRUNG, A_XA), (A_VE0, A_XA - 12), (A_VE1, 0.0), (A_DUR, 0.0)], t,
             [em, vao, ra, None, em, None])
    y = 36.0 * math.sin(math.pi * thang((t - A_VE0) / (A_VE1 - A_VE0))) if A_VE0 < t < A_VE1 else 0.0
    return x, y


def attack(t):
    D = nghi()
    R, L = NGHI["R"], NGHI["L"]
    # thân: thu người ngả sau lấy đà → chúi tới lúc lao → xoay theo cú đấm → khựng → về
    g = cong([(0, 0.0), (A_LAO0, 7.0), (A_LAO1, -11.0), (A_TRUNG, -19.0), (A_VE0, -13.0), (A_VE1, 3.0), (A_DUR, 0.0)], t,
             [em, em, ra, em, em, em])
    dy = cong([(0, 0.0), (A_LAO0, -16.0), (A_LAO1, -4.0), (A_TRUNG, -22.0), (A_VE0, -10.0), (A_VE1, 8.0), (A_DUR, 0.0)], t)
    dx = cong([(0, 0.0), (A_LAO0, -10.0), (A_TRUNG, 34.0), (A_VE0, 22.0), (A_VE1, 0.0)], t)
    kh = rung(t, A_TRUNG, 9.0, 0.07, 16.0)                                        # khựng lúc trúng
    than(D, dx + kh, dy, g, dau=-0.5 * g + rung(t, A_TRUNG, 5.0, 0.12, 9.0), nguc=0.35 * g)
    # tay GẦN: kéo ra sau lên cao (0–0.20), giữ lúc lao, quét VÒNG từ sau – xuống thấp trước thân – lên phía trước ngang ngực
    co_ = 1.0
    if t <= A_DAM:
        w = em(t / A_LAO0)
        vt = R["vt"] + (np.array([-92.0, 118.0]) - 0) * w + np.array([-14.0, 10.0]) * em((t - A_LAO0) / (A_DAM - A_LAO0))
        gc = R["goc"] + (-66.0) * w - 10.0 * em((t - A_LAO0) / (A_DAM - A_LAO0))
    elif t <= A_VE0:
        s = ra((t - A_DAM) / (A_TRUNG - A_DAM), 2.2)
        # cung móc: sau-trên → trái-dưới → trước-dưới → trước ngang ngực (toạ độ so với ngực)
        moc = [(0.0, R["vt"] + (-106.0, 128.0)), (0.34, (-300.0, -34.0)), (0.68, (-40.0, -112.0)), (1.0, (240.0, -60.0))]
        vt = cong(moc, s, [thang, thang, thang])
        gc = cong([(0.0, R["goc"] - 76.0), (0.34, -62.0), (0.68, -15.0), (1.0, 30.0)], s, [thang, thang, thang])
        co_ = 1.0 + 0.16 * math.sin(math.pi * min(1.0, s * 1.15))                # tới gần ống kính lúc vòng qua trước thân
        vt = vt + np.array([kh * 1.4, 0.0])
        if t > A_TRUNG:                                                          # dư lực: trôi thêm một chút rồi khựng
            f = em((t - A_TRUNG) / (A_VE0 - A_TRUNG))
            vt = vt + np.array([16.0, 14.0]) * f
            gc += 9.0 * f
    else:
        w = em((t - A_VE0) / (A_VE1 + 0.10 - A_VE0))
        vt = (np.array([256.0, -46.0]) * (1 - w) + R["vt"] * w) + np.array([0.0, -70.0]) * math.sin(math.pi * w)
        gc = 39.0 * (1 - w) + R["goc"] * w
    tay(D, "R", vt, gc, vai=0.62, tam=0.6, co=co_)
    xoe(D, "R", -0.5 * cong([(0, 0.0), (A_LAO0, 1.0), (A_VE0, 1.0), (A_VE1, 0.0)], t))
    # tay XA: thủ trước ngực lúc lấy đà, hất ra sau làm đối trọng lúc đấm
    w1 = cong([(0, 0.0), (A_LAO0, 1.0), (A_DAM, 1.0), (A_TRUNG, 0.0)], t)
    w2 = cong([(0, 0.0), (A_DAM, 0.0), (A_TRUNG, 1.0), (A_VE0, 1.0), (A_VE1 + 0.1, 0.0)], t, [None, ra, None, em])
    vt = L["vt"] + np.array([-58.0, 46.0]) * w1 + np.array([46.0, 36.0]) * w2
    gc = L["goc"] + 30.0 * w1 - 26.0 * w2
    tay(D, "L", vt, gc)
    pha_le(D, "R", -10.0 * w2, 8.0 * w2, 0.5)
    return nhip_loi(D, t, 0.7)


# ---------------------------------------------------------------- chiêu mana: hai tay đưa lên trước, bắn hai bàn tay vào đối thủ
C_DUR = 1.90
C_GIO = 0.36                       # hai tay đã chĩa tới
C_BAN = (0.56, 0.66)               # bàn tay gần / xa rời tay
C_TOI = 0.16                       # bay tới đích mất chừng này
C_GIU = 0.12                       # ghim ở đích
C_VE = 0.36                        # bay về
C_XA = 620.0                       # quãng bay xem thử trên rig gốc (game co theo khoảng cách đối thủ)
C_VT = {"R": (-112.0, -152.0), "L": (150.0, -46.0)}      # gốc cẳng tay lúc chĩa (so với ngực): tay gần thấp phía trước, tay xa cao phía sau
C_GOC = {"R": 7.0, "L": 3.0}


def ban_bay(t, k):
    """quãng bay 0..1 của bàn tay thứ k (0 gần, 1 xa) và độ nâng của đường về."""
    a = C_BAN[k]
    if t <= a:
        return 0.0, 0.0
    if t <= a + C_TOI:
        return ra((t - a) / C_TOI, 1.6), 0.0
    if t <= a + C_TOI + C_GIU:
        return 1.0, 0.0
    w = (t - a - C_TOI - C_GIU) / C_VE
    if w >= 1.0:
        return 0.0, 0.0
    return 1.0 - em(w) ** 1.25, math.sin(math.pi * w)


C_NANG = 120.0                     # đường về vồng cao chừng này
C_VE_R = C_BAN[0] + C_TOI + C_GIU + C_VE
C_VE_L = C_BAN[1] + C_TOI + C_GIU + C_VE


def cast(t):
    D = nghi()
    w = cong([(0, 0.0), (C_GIO, 1.0), (C_VE_L + 0.08, 1.0), (C_DUR - 0.12, 0.0)], t, [vot, None, em])
    gong = cong([(0, 0.0), (C_GIO, 0.0), (C_BAN[0], 1.0), (C_BAN[0] + 0.04, 0.0)], t, [None, em, None])            # gồng trước khi bắn
    # thân: ngả sau khi gồng, giật lùi mỗi phát bắn, đón tay về thì nảy
    giat_lui = sum(rung(t, C_BAN[k], 1.0, 0.09, 6.5, math.pi / 2) for k in (0, 1))
    don = rung(t, C_VE_R, 1.0, 0.10, 7.0) + rung(t, C_VE_L, 1.0, 0.10, 7.0)
    than(D, dx=-16.0 * w - 22.0 * gong - 12.0 * giat_lui + giat(t, 1.6 * gong), dy=-8.0 * w + 6.0 * don,
         goc=4.0 * w + 4.0 * gong + 3.0 * giat_lui, dau=3.0 * gong - 5.0 * giat_lui, nguc=2.0 * w)
    out, them = {}, {}
    for k, b in enumerate("RL"):
        Rg = NGHI[b]
        lui = -30.0 * gong - 40.0 * max(0.0, rung(t, C_BAN[k], 1.0, 0.08, 5.0, math.pi / 2)) - 16.0 * max(0.0, rung(t, (C_VE_R, C_VE_L)[k], 1.0, 0.07, 6.0, math.pi / 2))
        vt = Rg["vt"] + (np.array(C_VT[b]) - Rg["vt"]) * w + np.array([lui, giat(t, 2.2 * gong, 24.0, k * 2.0)]) * (1.0 if w > 0.5 else 0.0)
        # nâng tay theo cung (không quét ngang qua lõi): giữa đường nhô ra ngoài
        vt = vt + np.array([(-46.0 if b == "R" else 40.0), 30.0]) * math.sin(math.pi * min(1.0, w)) * (1.0 if t < C_GIO else 0.0)
        gc = Rg["goc"] + (C_GOC[b] - Rg["goc"]) * w
        tay(D, b, vt, gc, vai=0.5, tam=0.5)
        xoe(D, b, -0.6 * gong)
        f, nang = ban_bay(t, k)
        out[b] = f
        bay_ = C_BAN[k] < t < (C_VE_R, C_VE_L)[k]
        ve_ = t > C_BAN[k] + C_TOI + C_GIU
        xoay_ = (-360.0 * (1.0 - f) if ve_ else 0.0) * (1.0 if nang > 0 else 0.0) + rung(t, C_BAN[k] + C_TOI, 10.0, 0.05, 14.0)
        them[b] = (float(nang), float(xoay_) if bay_ else 0.0, float(1.0 + 0.16 * min(1.0, f * 3.0)), 1.0 if bay_ else 0.0)
        # tấm vai giật ngược lúc tảng tay rời đi, nảy lúc tảng tay lắp lại
        s_ = -1.0 if b == "R" else 1.0
        D.xoay(TAY[b]["tam"], s_ * (9.0 * rung(t, C_BAN[k], 1.0, 0.10, 5.5, math.pi / 2) - 6.0 * rung(t, (C_VE_R, C_VE_L)[k], 1.0, 0.09, 7.0)))
        if GIA_LAP and (f > 0 or nang > 0):          # xem thử trên rig gốc: dời thẳng xương CẲNG TAY (cả tảng + bàn tay); rig của mình dùng xương fly_*
            T = TAY[b]
            Wb = fk(D.u)[ix(T["cang"])]
            xa = C_XA + (0.0 if b == "R" else -40.0)
            D.dat(T["cang"], (Wb[0, 2] + f * xa, Wb[1, 2] + nang * C_NANG + (0.0 if b == "R" else -f * 60.0)))
            D.co(T["cang"], them[b][2])
            D.xoay(T["cang"], xoay_)
    D.ex["ban"] = (out["R"], out["L"])
    D.ex["ban_them"] = (them["R"], them["L"])      # mỗi tay: (độ nâng đường về 0..1, góc xoay thêm, tỉ lệ, đang bay 0 | 1)
    pha_le(D, "R", 0.0, 10.0 * gong, 0.6)
    pha_le(D, "L", 0.0, 10.0 * gong, 0.6)
    return nhip_loi(D, t, 0.5, 0.06 + 0.10 * gong)


# ---------------------------------------------------------------- chiêu cuối: hai tay giơ lên trời xoè ra, tụ cầu, đổ tay về trước ném
S_DUR = 2.80
S_GIO = 0.42                       # hai tay đã giơ, bàn tay xoè: bắt đầu tụ
S_DAY = 1.50                       # cầu đầy
S_NGA = 1.66                       # ngả ra sau hết cỡ
S_NEM = 1.80                       # tay đổ tới, cầu rời tay
S_TRUNG = 1.98                     # cầu tới đích (xem thử)
S_HOI = 2.20                       # bắt đầu thu về
S_TAY = {"R": ((-196.0, 204.0), 101.0), "L": ((226.0, 204.0), 79.0)}        # gốc cẳng tay lúc giơ (so với ngực), góc trục
S_NEM_TAY = {"R": ((-36.0, -96.0), -12.0), "L": ((96.0, 46.0), -14.0)}       # lúc đổ tới
S_CAU = (20.0, 505.0)              # tâm cầu lúc tụ, so với ngực


def skill(t):
    D = nghi()
    w = cong([(0, 0.0), (S_GIO, 1.0)], t, [vot])                                  # giơ tay
    tu = cong([(0, 0.0), (S_GIO, 0.0), (S_DAY, 1.0)], t, [None, lambda x: x])      # cầu lớn dần
    nga = cong([(0, 0.0), (S_DAY, 0.0), (S_NGA, 1.0), (S_NEM, 0.0)], t, [None, em, vao])
    nem = cong([(0, 0.0), (S_NGA, 0.0), (S_NEM, 1.0), (S_HOI, 1.0), (S_DUR - 0.10, 0.0)], t, [None, lambda x: vao(x, 2.4), None, em])
    hoi = cong([(0, 0.0), (S_HOI, 0.0), (S_DUR - 0.10, 1.0)], t, [None, em])
    cang = w * (1 - hoi)                                                          # còn đang giơ / vươn
    run_ = giat(t, 1.0 + 2.6 * tu, 21.0) * (1.0 if S_GIO < t < S_NGA else 0.0)
    du = rung(t, S_NEM, 1.0, 0.10, 7.5)
    than(D, dx=-8.0 * w * (1 - nem) - 26.0 * nga + 44.0 * nem * (1 - hoi) + run_ * 0.6 + 8.0 * du,
         dy=(22.0 * w - 20.0 * tu + 7.0 * math.sin(2 * math.pi * 1.7 * max(0.0, t - S_GIO)) * (1.0 if t < S_NGA else 0.0)) * (1 - nem) + 12.0 * nga
            - 30.0 * nem * (1 - hoi) + 5.0 * du,
         goc=(3.0 * w + 3.0 * tu) * (1 - nem) + 8.0 * nga - 17.0 * nem * (1 - hoi) - 3.0 * du,
         dau=(3.0 * w) * (1 - nem) + 4.0 * nga - 4.0 * nem * (1 - hoi),
         nguc=2.0 * w * (1 - nem) + 4.0 * nga - 5.0 * nem * (1 - hoi))
    for b in "RL":
        Rg = NGHI[b]
        (gx, gy), ggoc = S_TAY[b]
        (nx, ny), ngoc = S_NEM_TAY[b]
        s_ = -1.0 if b == "R" else 1.0
        # giơ: hai tay dang rộng dần theo cỡ cầu, hạ nhẹ vì nặng; ngả sau; đổ tới theo cung qua đỉnh đầu
        gio = np.array([gx + s_ * 26.0 * tu - 46.0 * nga, gy - 16.0 * tu + 24.0 * nga + run_])
        ggo = ggoc + s_ * 7.0 * tu + 15.0 * nga
        vt = Rg["vt"] + (gio - Rg["vt"]) * w + np.array([s_ * 70.0, 0.0]) * math.sin(math.pi * min(1.0, w)) * (1.0 if t < S_GIO else 0.0)
        gc = Rg["goc"] + (gan(ggo, Rg["goc"] + 180.0 * (1 if b == "R" else 1)) - Rg["goc"]) * w
        if nem > 0:
            dich = np.array([nx, ny])
            cung_ = np.array([60.0, 150.0]) * math.sin(math.pi * nem) * (1.0 if t < S_HOI else 0.0)
            vt = vt + (dich - vt) * nem + cung_
            gc = gc + (ngoc - gc) * nem
        if hoi > 0:
            vt = vt + (Rg["vt"] - vt) * hoi
            gc = gc + (Rg["goc"] - gc) * hoi
        tay(D, b, vt, gc, vai=0.62, tam=0.6)
        xoe(D, b, 1.0 * cang * (1 - 0.6 * nem) + 0.25 * tu * cang)
        # pha lê nhỏ bị hút lên phía cầu lúc tụ
        pha_le(D, b, -s_ * 10.0 * tu * (1 - nem), 34.0 * tu * (1 - nem) + giat(t, 3.0 * tu, 17.0) * (1 - nem), 0.5)
    # quả cầu: kênh riêng (bán kính 0..1, toạ độ thế giới); sau khi rời tay bay về phía đối thủ
    ng = D.vt("bone4")
    c = ng + np.array(S_CAU) + np.array([-40.0 * nga, 10.0 * nga + 14.0 * (1 - tu)])
    r = tu if t <= S_NEM else 1.0
    if t > S_NGA:
        f = vao((t - S_NGA) / (S_NEM - S_NGA), 2.0)
        c = c + (ng + np.array([330.0, 120.0]) - c) * min(1.0, f)
    if t > S_NEM:
        f = thang((t - S_NEM) / (S_TRUNG - S_NEM))
        c = c + np.array([640.0, -90.0]) * f
        r = 1.0 if f < 1 else 0.0
    D.ex["cau"] = (float(r), float(c[0]), float(c[1]))
    return nhip_loi(D, t, 0.5 if t < S_NEM else 0.8, 0.06 + 0.12 * tu * (1 - nem))


# ---------------------------------------------------------------- bộ mảnh thứ hai: từng mảnh đặt trong hệ thế giới (die, appear)
def _bo_hai():
    """{xương bộ hai: dict(x1 = xương bộ chính tương ứng, slots = [(slot bộ hai, hình, slot bộ chính)], cha = xương bộ hai cha | None,
    tam = tâm cụm ở khung 0 idle, P = đỉnh thế giới của cụm ở khung 0 idle)}"""
    B = [b["name"] for b in A["bones"]]
    chinh = {a["att"]: a for a in A["atts"] if a["cur"]}
    G = {}
    for a in A["atts"]:
        if a["cur"]:
            continue
        c = chinh[a["att"]]
        dem = {}
        for v in c["w"]:
            for bi, w_ in v:
                dem[bi] = dem.get(bi, 0.0) + w_
        x1 = B[max(dem, key=dem.get)]
        g = G.setdefault(a["bone"], dict(x1=None, slots=[], dt=0.0, P=[]))
        g["slots"].append((a["slot"], a["att"], c["slot"]))
        P = np.array(c["xy"], float).reshape(-1, 2)
        dt = np.ptp(P[:, 0]) * np.ptp(P[:, 1])
        g["P"].append(P)
        if dt > g["dt"]:
            g["dt"], g["x1"] = dt, x1
    Ws = fk(B0)
    for n, g in G.items():
        p = TEN[PA[ix(n)]]
        g["cha"] = p if p in G else None
        i1 = ix(g["x1"])
        g["M0"] = W0[i1] @ np.linalg.inv(Ws[i1])                                    # dáng gốc → khung 0 idle (mảnh cứng)
        P = np.concatenate(g["P"])
        P = (g["M0"] @ np.c_[P, np.ones(len(P))].T).T[:, :2]
        g["P"] = P
        g["tam"] = (P.min(0) + P.max(0)) / 2
        g["W2"] = ma(0, -DY2, 0) @ Ws[ix(n)]                                        # xương bộ hai kéo về chỗ bộ chính (dáng gốc)
    return G


G2 = _bo_hai()
THU_TU2 = sorted(G2, key=ix)


def roi_tu_do(D, dat_):
    """dat_ = {xương bộ hai: (dx, dy, góc quay quanh tâm cụm, tỉ lệ, độ đậm)} so với chỗ ở khung 0 idle → D.tu_do (ma trận thế giới)."""
    td = {}
    for n in THU_TU2:
        g = G2[n]
        dx, dy, gq, s, a = dat_.get(n, (0.0, 0.0, 0.0, 1.0, 1.0))
        c = g["tam"]
        M = ma(c[0] + dx, c[1] + dy, gq, s, s) @ ma(-c[0], -c[1], 0) @ g["M0"]
        td[n] = (M @ g["W2"], a)
    D.tu_do = td
    return D


def day_cum(n, gq):
    """nửa chiều cao của cụm sau khi quay gq độ quanh tâm (để đặt nằm trên đất)."""
    g = G2[n]
    r = math.radians(gq)
    y = (g["P"][:, 0] - g["tam"][0]) * math.sin(r) + (g["P"][:, 1] - g["tam"][1]) * math.cos(r)
    return -y.min()


# tên gọn của các cụm bộ hai
C2 = dict(dau="P_tou2", cau="P_qiu2", nguc_tren="P_tengwan06", nguc_duoi="P_shenti05", loi="P_shuijing2", khoa="P_zhuangshi2",
          chop1="P_shitou06", chop2="P_shitou05", chop3="P_shitou04", vai_g="P_tengwan05", vai_x="P_tengwan04",
          cang_g="P_shoubiR04", ban_g="P_shouR02", cang_x="P_shoubiL04", ban_x="P_shouL02",
          pl_g1="P_shuijing015", pl_g2="P_shuijing014", pl_g3="P_shuijing013",
          pl_x1="P_shuijing012", pl_x2="P_shuijing011", pl_x3="P_shuijing010", pl_x4="P_shuijing09",
          ng_g1="P_shouzhiR08", ng_g2="P_shouzhiR07", ng_g3="P_shouzhiR06", ng_g4="P_shouzhiR05",
          ng_x1="P_shouzhiL08", ng_x2="P_shouzhiL07", ng_x3="P_shouzhiL06", ng_x4="P_shouzhiL05")
assert set(C2.values()) == set(G2), sorted(set(G2) ^ set(C2.values()))

# ---------------------------------------------------------------- die: lõi tắt ngỏm, từ đó các mảnh mất lực rụng rời thành đống
X_DUR = 1.70
X_TAT = 0.34                       # lõi tắt hẳn
X_G = 5200.0                       # gia tốc rơi (đơn vị con gốc / s²)
# cụm: (giờ bắt đầu rơi, dời ngang lúc nằm, góc lúc nằm, kê cao thêm so với đất, nảy)
X_ROI = dict(
    chop2=(0.42, -22.0, -62.0, 0.0, 0.5), chop3=(0.44, 26.0, 55.0, 0.0, 0.5), chop1=(0.46, -30.0, 82.0, 0.0, 0.25),
    ng_g1=(0.42, -34.0, 70.0, 0.0, 0.7), ng_g2=(0.44, 18.0, -95.0, 0.0, 0.7), ng_g3=(0.45, 44.0, 130.0, 0.0, 0.7), ng_g4=(0.46, 62.0, -60.0, 0.0, 0.7),
    ng_x1=(0.43, -46.0, -80.0, 0.0, 0.7), ng_x2=(0.45, -8.0, 100.0, 0.0, 0.7), ng_x3=(0.46, 30.0, -120.0, 0.0, 0.7), ng_x4=(0.47, 52.0, 75.0, 0.0, 0.7),
    pl_g1=(0.48, 40.0, 84.0, 0.0, 0.5), pl_g2=(0.44, -20.0, -78.0, 0.0, 0.5), pl_g3=(0.46, 16.0, 96.0, 0.0, 0.5),
    pl_x1=(0.49, -44.0, -86.0, 0.0, 0.5), pl_x2=(0.47, -12.0, 80.0, 0.0, 0.5), pl_x3=(0.46, 22.0, -100.0, 0.0, 0.5), pl_x4=(0.48, 50.0, 88.0, 0.0, 0.5),
    ban_g=(0.50, -8.0, -38.0, 0.0, 0.3), ban_x=(0.53, 6.0, 34.0, 0.0, 0.3),
    cang_g=(0.55, -24.0, 78.0, 0.0, 0.14), cang_x=(0.59, 30.0, -74.0, 0.0, 0.14),
    khoa=(0.60, 44.0, 48.0, 0.0, 0.3),
    vai_g=(0.64, 34.0, -66.0, 26.0, 0.10), vai_x=(0.69, 6.0, 62.0, 22.0, 0.10),
    nguc_duoi=(0.72, 10.0, -14.0, 0.0, 0.10), loi=(0.75, -6.0, 80.0, 12.0, 0.12), nguc_tren=(0.78, 28.0, 24.0, 96.0, 0.10),
    cau=(0.80, 210.0, -560.0, 0.0, 0.45), dau=(0.84, 30.0, -17.0, 150.0, 0.08))
X_SU_KIEN = []


def _roi(n, t, ts, dxf, gf, ke, nay, khoi):
    """quỹ đạo rơi của một cụm: (dx, dy, góc). Trước ts: xệ dần (mất lực). Sau ts: rơi tự do tới chỗ nằm, nảy nhẹ, lắc tắt dần."""
    g = G2[n]
    y0 = g["tam"][1]
    yf = DAT + day_cum(n, gf) + ke
    xe = -(10.0 + 16.0 * khoi) * em((t - 0.10) / (ts - 0.10)) if t > 0.10 else 0.0   # xệ xuống trước khi rơi
    lac = giat(t, 1.5, 15.0, hash(n) % 7) * (1.0 if 0.12 < t < ts else 0.0)
    if t <= ts:
        return lac, xe, 0.0
    h = (y0 + xe) - yf if False else (y0 - (10.0 + 16.0 * khoi)) - yf
    tr = math.sqrt(max(1e-4, 2.0 * max(h, 1.0) / X_G))
    x = t - ts
    if x < tr:
        f = x / tr
        return dxf * f, -(10.0 + 16.0 * khoi) - 0.5 * X_G * x * x, gf * em(f)
    x2 = x - tr
    b = h * 0.16 * nay * abs(math.sin(math.pi * x2 / 0.17)) * math.exp(-x2 / 0.11)
    lan = (dxf * 0.12 * nay) * (1 - math.exp(-x2 / 0.12))
    return dxf + lan, (yf - y0) + b, gf + rung(t, ts + tr, 7.0 * (0.4 + nay), 0.10, 5.0)


def die(t):
    D = nghi()
    # giật ngửa lúc dính đòn cuối, lõi chập chờn rồi tắt
    D.ex["loi"] = float(cong([(0, 1.0), (0.08, 0.25), (0.13, 0.9), (0.19, 0.12), (0.25, 0.55), (X_TAT, 0.0)], t, [thang] * 5))
    giat_ = rung(t, 0.0, 1.0, 0.09, 4.0, math.pi / 2)
    dat_ = {}
    for ten, (ts, dxf, gf, ke, nay) in X_ROI.items():
        n = C2[ten]
        khoi = 1.0 if ten in ("dau", "vai_g", "vai_x", "cang_g", "cang_x", "nguc_tren", "nguc_duoi") else 0.4
        dx, dy, gq = _roi(n, t, ts, dxf, gf, ke, nay, khoi)
        c = G2[n]["tam"]
        # cú giật đầu clip: cả con bật lùi, mảnh ở cao bật nhiều hơn
        dx += -22.0 * giat_ * (0.5 + c[1] / 600.0)
        gq += 5.0 * giat_ * (1.0 if c[0] < 20 else -0.6)
        dat_[n] = (dx, dy, gq, 1.0, 1.0)
    # lõi: thu nhỏ một nhịp lúc tắt
    n = C2["loi"]
    dx, dy, gq, s, a = dat_[n]
    dat_[n] = (dx, dy, gq, 1.0 - 0.10 * math.exp(-((t - X_TAT) / 0.05) ** 2), a)
    # ngón, bàn tay là con của cẳng tay trong bộ hai: vẫn đặt theo thế giới (roi_tu_do tự tính riêng theo cha)
    return roi_tu_do(D, dat_)


# ---------------------------------------------------------------- appear: lõi hiện ra, từng mảnh bay vào xếp thành hình
P_DUR = 2.30
P_XONG = 1.52                      # ráp xong: đổi về bộ mảnh chính
# cụm: (giờ bắt đầu bay, bay bao lâu, từ đâu (dx, dy), góc lúc đầu)
P_BAY = dict(
    loi=(0.00, 0.34, (0.0, 250.0), 0.0),
    nguc_duoi=(0.26, 0.26, (-40.0, -330.0), -70.0), nguc_tren=(0.34, 0.26, (60.0, 330.0), 80.0), khoa=(0.44, 0.22, (300.0, -120.0), 160.0),
    chop1=(0.40, 0.24, (0.0, -300.0), 120.0), chop2=(0.46, 0.20, (-200.0, -220.0), -150.0), chop3=(0.50, 0.20, (220.0, -220.0), 150.0),
    cau=(0.56, 0.22, (330.0, 180.0), 360.0), dau=(0.62, 0.30, (0.0, 380.0), -24.0),
    vai_g=(0.74, 0.28, (-380.0, 120.0), 80.0), vai_x=(0.82, 0.28, (380.0, 120.0), -80.0),
    cang_g=(0.94, 0.28, (-330.0, -260.0), -120.0), cang_x=(1.00, 0.28, (330.0, -260.0), 120.0),
    ban_g=(1.08, 0.22, (-300.0, -160.0), 200.0), ban_x=(1.12, 0.22, (300.0, -160.0), -200.0),
    ng_g1=(1.16, 0.18, (-240.0, 60.0), 300.0), ng_g2=(1.19, 0.18, (-160.0, -180.0), -300.0), ng_g3=(1.22, 0.18, (200.0, -200.0), 300.0), ng_g4=(1.25, 0.18, (220.0, 80.0), -300.0),
    ng_x1=(1.18, 0.18, (-220.0, 60.0), -300.0), ng_x2=(1.21, 0.18, (-140.0, -180.0), 300.0), ng_x3=(1.24, 0.18, (220.0, -180.0), -300.0), ng_x4=(1.27, 0.18, (240.0, 80.0), 300.0),
    pl_g1=(1.26, 0.18, (-200.0, 200.0), 180.0), pl_g2=(1.30, 0.18, (-260.0, 0.0), -180.0), pl_g3=(1.34, 0.18, (-200.0, -200.0), 180.0),
    pl_x1=(1.28, 0.18, (200.0, 200.0), -180.0), pl_x2=(1.31, 0.18, (260.0, 60.0), 180.0), pl_x3=(1.33, 0.18, (240.0, -60.0), -180.0), pl_x4=(1.36, 0.18, (200.0, -200.0), 180.0))
P_NANG = [("dau", 16.0), ("vai_g", 9.0), ("vai_x", 9.0), ("cang_g", 8.0), ("cang_x", 8.0)]        # mảnh to tới nơi thì cả khối đã ráp dội nhẹ


def appear(t):
    D = nghi()
    dat_ = {}
    doi_khoi = 0.0
    for ten, bien in P_NANG:
        ts, td, _, _ = P_BAY[ten]
        doi_khoi += rung(t, ts + td * 0.82, bien, 0.09, 6.0)
    for ten, (ts, td, (ox, oy), g0) in P_BAY.items():
        n = C2[ten]
        if t < ts:
            dat_[n] = (ox, oy, g0, 0.6, 0.0)
            continue
        w = (t - ts) / td
        if ten == "loi":                                    # lõi hạ xuống chậm, xoay một vòng, đập mạnh dần
            f = em(w)
            s = 0.5 + 0.5 * f + (0.10 * math.sin(2 * math.pi * 3.0 * (t - ts)) * math.exp(-(t - ts) / 0.5) if w >= 1 else 0.0)
            dat_[n] = (ox * (1 - f), oy * (1 - f), 0.0, s, thang(w * 2.5))
            continue
        f = vot(w, 1.4)
        nay_ = rung(t, ts + td * 0.82, 0.08, 0.06, 9.0) if w > 0.8 else 0.0
        da_rap = 1.0 if w >= 1.0 else 0.0
        dat_[n] = (ox * (1 - f), oy * (1 - f) - doi_khoi * da_rap, g0 * (1 - em(min(1.0, w * 1.08))), (0.72 + 0.28 * thang(w * 1.6)) * (1 + nay_),
                   thang((t - ts) / 0.09))
    roi_tu_do(D, dat_)
    D.ex["loi"] = float(cong([(0, 0.0), (0.30, 0.55), (P_XONG - 0.06, 0.6), (P_XONG + 0.10, 1.0)], t, [None, None, vot]))
    # ráp xong: gồng một nhịp (hai tay bung ra, ngực ưỡn) rồi về dáng nghỉ: làm trên bộ mảnh chính
    if t >= P_XONG:
        D.tu_do = None
        g = cong([(P_XONG, 0.0), (P_XONG + 0.16, 1.0), (P_XONG + 0.34, 1.0), (P_DUR - 0.06, 0.0)], t, [vot, None, em])
        than(D, dy=20.0 * g, goc=2.0 * g, dau=6.0 * g)
        for b in "RL":
            s_ = -1.0 if b == "R" else 1.0
            Rg = NGHI[b]
            tay(D, b, Rg["vt"] + np.array([s_ * 64.0, 40.0]) * g, Rg["goc"] + s_ * 26.0 * g)
            xoe(D, b, 0.8 * g)
            pha_le(D, b, s_ * 8.0 * g, 10.0 * g, 0.5)
        D.co("bone27", 1 + 0.16 * g)
    return D


CLIP = {"td_idle": (I_DUR, idle), "td_walk": (W_DUR, walk), "td_attack": (A_DUR, attack), "td_cast": (C_DUR, cast), "td_skill": (S_DUR, skill),
        "td_appear": (P_DUR, appear), "td_hit": (H_DUR, hit), "td_die": (X_DUR, die)}
LAP = ("td_idle", "td_walk")
BAY = {"td_attack": attack_bay}                 # cung dời của xương move (đơn vị con gốc)
SU_KIEN = {"td_idle": [], "td_walk": [], "td_hit": [],
           "td_attack": [(A_TRUNG, "trung", "")],
           "td_cast": [(C_GIO, "tu", ""), (C_BAN[0], "phun", "g"), (C_BAN[1], "phun", "x"), (C_BAN[0] + C_TOI, "trung", "g"), (C_BAN[1] + C_TOI, "trung", "x"),
                       (C_VE_R, "ve", "g"), (C_VE_L, "ve", "x")],
           "td_skill": [(S_GIO, "tu", ""), (S_DAY, "day", ""), (S_NEM, "nem", ""), (S_TRUNG, "trung", "")],
           "td_appear": [(0.0, "loi", ""), (P_BAY["dau"][0] + P_BAY["dau"][1], "ghep", "dau"), (P_XONG, "xong", "")],
           "td_die": [(X_TAT, "tat", ""), (0.44, "roi", ""), (0.90, "cham_dat", ""), (1.26, "cham_dat", "dau")]}


def _goc_lien(a):
    """bỏ bước nhảy 360 giữa hai khung liền nhau."""
    return np.degrees(np.unwrap(np.radians(a)))


GIA_LAP = False                 # True: giả lập ngay trên rig gốc phần game / xương fly_* lo (bàn tay bay của chiêu mana)


def dung(xem=False):
    global GIA_LAP
    GIA_LAP = bool(xem)
    out = []
    rieng = {}
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        alpha = {}
        slots = {}
        co_td = [d.tu_do is not None for d in Ds]
        if any(co_td):
            # bộ mảnh thứ hai: tính biến đổi riêng của từng xương rời theo ma trận thế giới mong muốn
            for j, d in enumerate(Ds):
                if d.tu_do is None:
                    continue
                Wm = {}
                Wb = fk(d.u)[ix("bone")]
                for nm in THU_TU2:
                    M, a = d.tu_do[nm]
                    Wm[nm] = M
                    cha = G2[nm]["cha"]
                    L = np.linalg.solve(Wm[cha] if cha else Wb, M)
                    U[j, ix(nm)] = tach(L)
                    alpha.setdefault(nm, [1.0] * n)[j] = a
            for nm in THU_TU2:
                i = ix(nm)
                U[:, i, 2] = _goc_lien(U[:, i, 2])
                U[:, i, 2] += 360.0 * round((B0[i, 2] - U[[k for k in range(n) if co_td[k]][-1 if ten == "td_appear" else 0], i, 2]) / 360.0)
                for s2, att, s1 in G2[nm]["slots"]:
                    k2, k1 = [], []
                    for j, t in enumerate(ts):
                        v2, v1 = (att if co_td[j] else None), (None if co_td[j] else att)
                        if not k2 or k2[-1][1] != v2:
                            k2.append([round(t, 4), v2])
                            k1.append([round(t, 4), v1])
                    slots[s2] = {"attachment": k2}
                    slots[s1] = {"attachment": k1}
                    al = alpha[nm]
                    if min(al) < 0.999:
                        slots[s2]["alpha"] = [[round(t, 4), round(float(v), 3)] for t, v in zip(ts, al)]
            # khung không dùng bộ hai: để xương rời ở dáng gốc
            for j in range(n):
                if not co_td[j]:
                    for nm in THU_TU2:
                        U[j, ix(nm)] = U[max(0, j - 1), ix(nm)]
        if xem and ten in BAY:
            for j, t in enumerate(ts):
                U[j, ix("bone"), :2] += BAY[ten](t)
        bones = {}
        for i, nm in enumerate(TEN):
            d = U[:, i] - B0[i]
            o = {}
            if np.abs(d[:, 2]).max() > 1e-3:
                o["rotate"] = [[round(t, 4), round(float(v), 3)] for t, v in zip(ts, d[:, 2])]
            if np.abs(d[:, :2]).max() > 1e-3:
                o["translate"] = [[round(t, 4), round(float(x), 3), round(float(y), 3)] for t, (x, y) in zip(ts, d[:, :2])]
            sc = U[:, i, 3:] / np.where(np.abs(B0[i, 3:]) < 1e-6, 1.0, B0[i, 3:])
            if np.abs(sc - 1).max() > 1e-4:
                o["scale"] = [[round(t, 4), round(float(x), 4), round(float(y), 4)] for t, (x, y) in zip(ts, sc)]
            if o:
                bones[nm] = o
        out.append({"name": ten, "dur": dur, "bones": bones, "slots": slots})
        rieng[ten] = {"dur": dur, "loi": [float(d.ex["loi"]) for d in Ds], "cau": [list(d.ex["cau"]) for d in Ds],
                      "ban": [list(d.ex["ban"]) for d in Ds], "ban_them": [[list(x) for x in d.ex["ban_them"]] for d in Ds], "bay": [list(BAY[ten](t)) if ten in BAY else [0.0, 0.0] for t in ts],
                      "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, {len(slots)} slot đổi hình")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "td_extra.json"), "w", encoding="utf-8"))
    if not xem:
        json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "td_extra.json"))
    return rieng


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "0,330,1500,1000"
VIEW_RIENG = {"td_attack": "260,330,1900,1000", "td_cast": "330,330,1900,1000", "td_skill": "260,430,1900,1200", "td_appear": "0,360,1500,1100"}

TRANG = r"""<!doctype html><html><head><meta charset="utf-8"><title>tuong_da: clip trên rig gốc</title>
<style>body{background:#22252b;color:#ddd;font:14px sans-serif;margin:14px}button{background:#333842;color:#ddd;border:1px solid #555;
border-radius:6px;padding:6px 12px;margin:3px;font:14px sans-serif;cursor:pointer}button.on{background:#e8a33c;color:#111;border-color:#e8a33c}
#khung{position:relative;width:1100px;height:700px;margin-top:10px}canvas{position:absolute;left:0;top:0;border-radius:8px}#cv{background:#6b7079}
#st{color:#9ab}#mo{margin:6px 2px;max-width:1080px;line-height:1.45}</style></head><body>
<div><b>tuong_da</b>: clip dựng ở tầng điều khiển, chạy bằng runtime Spine thật trên RIG GỐC (hình của game tham khảo, chỉ xem nội bộ).
Quãng lao của đòn thường và quãng bay của bàn tay là giả lập phần code game lo. Vòng tròn lục = chỗ và cỡ quả cầu năng lượng (VFX làm
sau); dòng "lõi" = độ sáng lõi (rig của mình mới đổi được hình lõi). <span id="st">đang nạp</span></div>
<div id="nut"></div><div>tốc độ: <span id="td"></span> &nbsp; <label><input type="checkbox" id="lap" checked> phát lại liên tục</label></div>
<div id="mo"></div><div id="khung"><canvas id="cv" width="1100" height="700"></canvas><canvas id="ov" width="1100" height="700"></canvas></div>
<script src="__LIB__"></script>
<script>
const NAME="__MON__", SKEL="__SKEL__", ATLAS=__ATLAS__, PNG="__PNG__", EXTRA=__EXTRA__, INFO=__INFO__, KENH=__KENH__;
__ADDEXTRA__
function b64(s){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;}
const st=document.getElementById("st"), cv=document.getElementById("cv"), ov=document.getElementById("ov").getContext("2d");
let cur=null, t=0, speed=1, last=0, hold=0;
function kenh(c,ten,t){const k=KENH[c][ten];const x=Math.min(k.length-1,t*30),i=Math.floor(x),j=Math.min(k.length-1,i+1),w=x-i;
  return Array.isArray(k[i])?k[i].map((v,q)=>v*(1-w)+k[j][q]*w):k[i]*(1-w)+k[j]*w;}
async function main(){
  const ctx=new spine.ManagedWebGLRenderingContext(cv,{alpha:false});
  const am=new spine.AssetManager(ctx,"");
  am.setRawDataURI(NAME+".atlas","data:text/plain;base64,"+btoa(unescape(encodeURIComponent(ATLAS))));
  am.setRawDataURI(NAME+".png",PNG);
  am.loadTextureAtlas(NAME+".atlas");
  await new Promise(res=>{const w=()=>am.isLoadingComplete()?res():setTimeout(w,50);w();});
  if(am.hasErrors()){st.textContent="LOI "+JSON.stringify(am.getErrors());return;}
  const atlas=am.require(NAME+".atlas");
  const sd=new spine.SkeletonBinary(new spine.AtlasAttachmentLoader(atlas)).readSkeletonData(b64(SKEL));
  addExtra(sd,EXTRA);
  const renderer=new spine.SceneRenderer(cv,ctx);
  const sk=new spine.Skeleton(sd);
  const nut=document.getElementById("nut"), mo=document.getElementById("mo");
  function chon(c){cur=c;t=0;hold=0;[...nut.children].forEach(b=>b.classList.toggle("on",b.dataset.clip===c));
    const i=INFO[c];mo.textContent=c+" · "+i.dur.toFixed(2)+" s"+(i.lap?" · lặp":"")+(i.ev?" · sự kiện: "+i.ev:"")+" — "+i.mo;}
  for(const c of Object.keys(INFO)){const b=document.createElement("button");b.textContent=c.replace("td_","");b.dataset.clip=c;b.onclick=()=>chon(c);nut.appendChild(b);}
  const td=document.getElementById("td");
  for(const v of [1,0.5,0.25]){const b=document.createElement("button");b.textContent=v+"×";b.onclick=()=>{speed=v;[...td.children].forEach(x=>x.classList.toggle("on",x===b));};td.appendChild(b);if(v===1)b.classList.add("on");}
  chon(Object.keys(INFO)[0]);
  st.textContent="sẵn sàng";
  function ve(now){
    const dt=Math.min(0.05,(now-last)/1000||0);last=now;
    const i=INFO[cur], a=sd.findAnimation(cur);
    if(i.lap){t=(t+dt*speed)%i.dur;}
    else if(t<i.dur){t=Math.min(i.dur,t+dt*speed);}
    else{hold+=dt;if(hold>0.8&&document.getElementById("lap").checked){t=0;hold=0;}}
    sk.setToSetupPose();
    a.apply(sk,t,t,false,[],1,spine.MixBlend.setup,spine.MixDirection.mixIn);
    sk.updateWorldTransform(spine.Physics.update);
    const [vx,vy,vw,vh]=i.view, z=Math.max(vw/cv.width,vh/cv.height);
    ctx.gl.clearColor(0.42,0.44,0.48,1);ctx.gl.clear(ctx.gl.COLOR_BUFFER_BIT);
    renderer.camera.position.x=vx;renderer.camera.position.y=vy;renderer.camera.zoom=z;
    ctx.gl.viewport(0,0,cv.width,cv.height);renderer.camera.setViewport(cv.width,cv.height);renderer.camera.update();
    renderer.begin();renderer.drawSkeleton(sk,false);renderer.end();
    ov.clearRect(0,0,1100,700);
    const loi=kenh(cur,"loi",t), cau=kenh(cur,"cau",t), bay=kenh(cur,"bay",t);
    ov.strokeStyle="rgba(40,30,20,.35)";ov.beginPath();ov.moveTo(0,350+(vy-0)/z);ov.lineTo(1100,350+(vy-0)/z);ov.stroke();
    if(cau[0]>0.01){const x=550+(cau[1]+bay[0]-vx)/z, y=350-(cau[2]+bay[1]-vy)/z, r=118*cau[0]/z;
      ov.fillStyle="rgba(110,230,150,.55)";ov.strokeStyle="rgba(30,110,60,.9)";ov.lineWidth=3;ov.beginPath();ov.arc(x,y,r,0,6.2832);ov.fill();ov.stroke();}
    ov.fillStyle=loi>0.5?"#9f9":"#f99";ov.font="15px sans-serif";ov.fillText("lõi "+Math.round(loi*100)+"%   t = "+t.toFixed(2)+" s",14,24);
    requestAnimationFrame(ve);
  }
  requestAnimationFrame(ve);
}
main().catch(e=>{st.textContent="LOI "+e+" "+(e.stack||"");});
</script></body></html>"""

MO_TA = {"td_idle": "nguyên idle_01 của họ, thêm nhịp đập của lõi (pha lê giữa ngực phồng nhẹ hai nhịp mỗi giây)",
         "td_walk": "nguyên run_01 của họ (chúi tới, hai tay đánh so le); game lo dời ngang",
         "td_attack": "thu người kéo tay gần ra sau, LAO tới, tới nơi đấm VÒNG: tảng tay quét từ sau, xuống thấp qua trước thân, móc lên ngang ngực; khựng; nhảy lùi về",
         "td_cast": "hai tay đưa lên chĩa về trước, gồng rung, BẮN lần lượt hai TẢNG CẲNG TAY (tảng đá + đai rễ + bàn tay) bay tới đối thủ, tấm vai giật ngược; tảng tay lộn một vòng bay về lắp lại",
         "td_skill": "hai tay giơ lên trời, xoè ngón; tụ cầu (cầu lớn dần, người rung, pha lê nhỏ bị hút lên); ngả sau; đổ hai tay về trước NÉM cầu; dư lực; thu về",
         "td_appear": "lõi hạ xuống trước, rồi từng mảnh bay vào ráp: ngực, chóp đá, quả cầu cổ, mào đầu, hai vai, hai cẳng tay, bàn tay, ngón, pha lê nhỏ; ráp xong gồng một nhịp",
         "td_hit": "nguyên hit_01 của họ",
         "td_die": "giật ngửa, lõi chập chờn rồi TẮT (0,34 s); các mảnh xệ xuống, rồi rụng dần: ngón, pha lê, bàn tay, cẳng tay, vai, ngực, lõi, quả cầu lăn đi, mào đầu úp lên đống"}


def song():
    """trang xem SỐNG (runtime Spine thật, 60 khung/giây, mở bằng file://) trên rig gốc → <scan>/lam_clip/xem/xem.html."""
    import base64
    dung(xem=True)
    extra = open(os.path.join(LAM, "td_extra.json"), encoding="utf-8").read()
    rieng = dung()
    mo_xe = open(os.path.join(HERE, "mo_xe", "mo_xe.html"), encoding="utf-8").read()
    a = mo_xe.index("function addExtra(data, list) {")
    b = mo_xe.index("// lấy mẫu 30 khung/giây")
    b64 = lambda f: base64.b64encode(open(os.path.join(RIG, f), "rb").read()).decode()
    info = {c: {"dur": CLIP[c][0], "lap": c in LAP, "view": [float(x) for x in VIEW_RIENG.get(c, VIEW).split(",")], "mo": MO_TA.get(c, ""),
                "ev": ", ".join(f"{e}{' ' + s if s else ''} {x:.2f} s" for x, e, s in SU_KIEN.get(c, []))} for c in CLIP}
    kenh = {c: {k: rieng[c][k] for k in ("loi", "cau", "bay")} for c in CLIP}
    lib = "file:///" + os.path.join(HERE, "lib", "spine-player.js").replace(os.sep, "/")
    h = (TRANG.replace("__LIB__", lib).replace("__MON__", MON).replace("__SKEL__", b64(MON + ".skel"))
         .replace("__ATLAS__", json.dumps(open(os.path.join(RIG, MON + ".atlas"), encoding="utf-8").read()))
         .replace("__PNG__", "data:image/png;base64," + b64(MON + ".png")).replace("__EXTRA__", extra)
         .replace("__INFO__", json.dumps(info, ensure_ascii=False)).replace("__KENH__", json.dumps(kenh)).replace("__ADDEXTRA__", mo_xe[a:b]))
    ra_ = os.path.join(LAM, "xem")
    os.makedirs(ra_, exist_ok=True)
    open(os.path.join(ra_, "xem.html"), "w", encoding="utf-8").write(h)
    print(os.path.join(ra_, "xem.html"))


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    lenh = a[0] if a else "dung"
    if lenh == "dung":
        dung()
    elif lenh == "xem":
        dung(xem=True)
        cl = a[1] if len(a) > 1 and a[1] not in ("", "het") else ",".join(CLIP)       # PowerShell bỏ đối số rỗng: dùng "het"
        n = a[2] if len(a) > 2 else "16"
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        for c in cl.split(","):
            view = a[3] if len(a) > 3 and a[3] not in ("", "het") else VIEW_RIENG.get(c, VIEW)
            vw, vh = [float(x) for x in view.split(",")[2:]]
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=td_extra.json&n={n}&tw=380&th={int(round(380 * vh / vw))}&cols=8&view={view}{tt}")
        dung()
    elif lenh == "song":
        song()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "td_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
