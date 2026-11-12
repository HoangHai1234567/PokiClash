# -*- coding: utf-8 -*-
"""Bạch tuộc quái vật: clip RIÊNG theo ý người dùng (2026-11-12), dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3616 rồi để runtime
Spine thật nướng (cách của rong_vay_clip.py; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng: appear trồi lên từ hố đất (đưa các chân lên trước rồi kéo thân lên); đánh thường đấm (kéo dài xúc tu ra); chiêu mana bắn
một quả bóng mực (bóng mực là VFX, rig chỉ diễn thân + sự kiện); chiêu cuối như skill_04: giơ hai vòi ngoài lên uốn uốn kiểu triệu
hồi, bạch tuộc con hiện quanh thân, bò tới kẻ thù rồi nhảy vào; thêm walk.

Rig gốc điều khiển bằng: bone2 (dời cả con), bone3 (thân: dời, nghiêng), bone4/5/6 (đầu), ba xúc tu lớn có IK hai đốt gốc
  xúc tu 1 (sau cùng, to):     bone12 → 13 → 14 → 15 → 16 → 17, IK CJ3 trên (bone12, bone13)
  xúc tu 2 (móc, giữa thân):   bone7 → 8 → 9 → 10 → 11,         IK CJ1 trên (bone7, bone8)
  xúc tu 6 (trước, ĐẤM):       bone27 → 28 → 29 → 30 → 31,      IK CJ2 trên (bone27, bone28)
ba "ngón" nhỏ bone18–20, 21–23, 24–26; xích chạy trên đường cong. Con gốc nhìn PHẢI (+x là phía trước: mắt hướng về phía ba ngón
nhỏ; xúc tu 6 ở phía trước, xúc tu 1 và 2 to lộ mặt dưới ở phía sau). Bản đầu tôi đoán ngược (đấm bằng xúc tu 1 về −x), đã sửa.

    bach_tuoc_clip.py dung                 ghép, ghi <scan>/lam_clip/bt_extra.json
    bach_tuoc_clip.py xem [clip,..] [n] [view] [t0] [t1]   tờ khung trên rig gốc → <scan>/lam_clip/khung/<clip>.jpg
    bach_tuoc_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (bach_tuoc_rig.py đọc)
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
MON = "monster_3616"
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
TEN = [b["name"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]                 # CJ1, CJ2, CJ3
SLOT = [s["name"] for s in I["slots"]]
MAT = SLOT.index("P_yanjing1")
ix = TEN.index
_S = None

T1 = ["bone12", "bone13", "bone14", "bone15", "bone16", "bone17"]          # xúc tu 1 (đấm)
T2 = ["bone7", "bone8", "bone9", "bone10", "bone11"]
T6 = ["bone27", "bone28", "bone29", "bone30", "bone31"]
NGON = [["bone18", "bone19", "bone20"], ["bone21", "bone22", "bone23"], ["bone24", "bone25", "bone26"]]
K_CJ1, K_CJ2, K_CJ3 = 0, 1, 2


def nhom(ds):
    m = np.zeros(len(TEN), bool)
    for n in ds:
        m[ix(n)] = True
    return m


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k (3) độ trộn IK; mat = hình mắt."""

    def __init__(self, u, k, mat="P_yanjing1"):
        self.u, self.k, self.mat = u, k, mat

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), self.mat)

    def tron(self, B, w, mat_na=None):
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (float(w) if mat_na is None else 0.0),
                    B.mat if w > 0.5 and mat_na is None else self.mat)

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self

    def dai(self, ten, s):
        self.u[ix(ten), 3] *= s
        return self


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float), np.array([[q[0] for q in f["k"]] for f in v["frames"]], float),
                  [f["n"][MAT] for f in v["frames"]]) for c, v in S.items()}
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk, M = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w, M[i0] or "P_yanjing1")


def nghi():
    return dk("idle_01", 0.0)


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):
    x = min(1.0, max(0.0, x))
    return x ** k


def cung(t, t0, t1, t2, t3):
    if t <= t0 or t >= t3:
        return 0.0
    if t < t1:
        return em((t - t0) / (t1 - t0))
    if t <= t2:
        return 1.0
    return 1.0 - em((t - t2) / (t3 - t2))


def cong(moc, t, kieu=None):
    if t <= moc[0][0]:
        return moc[0][1]
    for i in range(len(moc) - 1):
        (a, x), (b, y) = moc[i], moc[i + 1]
        if t <= b:
            w = (t - a) / (b - a)
            if kieu and kieu[i]:
                w = kieu[i](w)
            return x + (y - x) * w
    return moc[-1][1]


def dat(D, ten, goc, w):
    """kéo góc riêng của xương về giá trị tuyệt đối goc với trọng số w."""
    i = ix(ten)
    D.u[i, 2] += (goc - D.u[i, 2]) * w


def goc_the_gioi(D, ten):
    """góc thế giới (xấp xỉ FK, bỏ IK) của xương cha của ten: tổng góc riêng dọc chuỗi cha."""
    g, p = 0.0, I["bones"][ix(ten)]["parent"]
    while p >= 0:
        g += D.u[p, 2]
        p = I["bones"][p]["parent"]
    return g


# ---------------------------------------------------------------- attack: đấm, xúc tu 1 vươn dài
A_DA, A_TRUNG, A_GIU, A_DUR = 0.34, 0.44, 0.54, 1.15
AT_DA = (122.0, -58.0, -66.0, -52.0, -40.0)       # dáng lấy đà của xúc tu 6: góc thế giới của bone27, rồi góc riêng bone28..31
AT_DAM = (23.0, -3.0, -2.0, 2.0, 22.0)            # dáng đấm: bone27 chĩa ra trước chếch lên 23°, các đốt sau thẳng hàng, mút gập nhẹ


def attack(t):
    """ĐÒN THƯỜNG 1,15 s, đấm về phía TRƯỚC (+x) bằng xúc tu trước (xúc tu 6, bone27..31; ở skill_03 họ cũng duỗi nó ra trước).
    Lấy đà 0 → 0,34: thân ngả về sau, xúc tu 6 co lên cao ra sau như nắm đấm; đấm 0,34 → 0,44: duỗi thẳng ra trước, chếch lên, VƯƠN
    DÀI khoảng gấp đôi (tỉ lệ ở xương gốc khi chuỗi đã thẳng), thân chúi theo, sự kiện trung 0,44; giữ tới 0,54; rút về, thân nảy lại.
    Thân và các xúc tu khác: skill_03 co giãn thời gian; cú quét ra sau của xúc tu 1 giảm còn 35%."""
    R = nghi()
    tau = cong([(0.0, 0.0), (0.22, 0.52), (A_DA, 0.75), (A_TRUNG, 0.90), (A_GIU, 0.97), (A_DUR, 1.9)], t,
               [em, None, lambda w: vao(w, 1.6), None, em])
    D = dk("skill_03", tau)
    D.k[K_CJ2] = 0.0
    m1 = nhom(T1)
    D.u[m1] = R.tron(D, 0.35).u[m1]
    g = goc_the_gioi(D, "bone27")
    w0 = cung(t, 0.03, 0.22, A_DA - 0.05, A_DA + 0.03)     # lấy đà: co lên cao, ra sau
    dat(D, "bone27", AT_DA[0] - g, w0)
    for b, a in zip(T6[1:], AT_DA[1:]):
        dat(D, b, a, w0)
    w = cung(t, A_DA - 0.03, A_TRUNG - 0.01, A_GIU, 0.80)  # đấm: cả chuỗi thẳng ra trước, chếch lên
    dat(D, "bone27", AT_DAM[0] - g, w)
    for b, a in zip(T6[1:], AT_DAM[1:]):
        dat(D, b, a, w)
    s = cung(t, A_DA + 0.045, A_TRUNG - 0.005, A_GIU - 0.02, 0.74)      # vươn dài SAU khi đã chĩa đúng hướng (kẻo quét vòng qua đầu)
    # tỉ lệ xương CỘNG DỒN xuống con cháu: chỉ kéo ở gốc (cả chuỗi đang thẳng hàng nên dài đều), thêm một nấc ở giữa cho ngọn vút hơn
    D.dai("bone27", 1.0 + 0.95 * s)
    D.dai("bone29", 1.0 + 0.30 * s)
    # nảy khi trúng: giật lùi 1 nhịp rồi rung tắt dần
    r = max(0.0, t - A_TRUNG)
    nay = math.exp(-r * 9.0) * math.sin(r * 34.0) if t >= A_TRUNG else 0.0
    D.doi("bone3", 70.0 * cung(t, A_DA, A_TRUNG, A_GIU, 0.85) - 26.0 * cung(t, 0.05, 0.26, A_DA, A_TRUNG) - 10.0 * nay, 0.0)
    D.xoay("bone3", -5.0 * cung(t, A_DA, A_TRUNG, A_GIU, 0.85) + 3.0 * cung(t, 0.05, 0.26, A_DA, A_TRUNG))
    D.mat = "P_yanjing2" if 0.1 < t < 0.85 else "P_yanjing1"
    return D


# ---------------------------------------------------------------- cast: phồng người rồi phụt bóng mực
C_PHUN, C_DUR = 0.62, 1.5


def cast(t):
    """CHIÊU MANA 1,5 s (nguồn: skill_01, "nhổm cao rồi dập xuống"): hít phồng 0 → 0,48 (nhổm lên, ngả sau, đầu phồng), phụt 0,62
    (dập người ra trước – xuống, đầu xẹp nhanh), giật lùi, về. Sự kiện phun 0,62. Bóng mực là VFX: rig có xương `mieng`."""
    tau = cong([(0.0, 0.0), (0.48, 0.44), (C_PHUN, 0.66), (0.85, 0.95), (C_DUR, 1.8333)], t, [em, lambda w: vao(w, 1.7), None, em])
    D = dk("skill_01", tau)
    p = cung(t, 0.06, 0.46, 0.53, C_PHUN + 0.02)            # phồng
    x = cung(t, C_PHUN - 0.05, C_PHUN + 0.03, C_PHUN + 0.08, 0.95)   # xẹp sau khi phụt
    i5 = ix("bone5")
    D.u[i5, 3] *= 1.0 + 0.10 * p - 0.10 * x
    D.u[i5, 4] *= 1.0 + 0.13 * p - 0.07 * x
    D.xoay("bone3", 4.0 * p - 6.0 * x)                     # con nhìn về +x: ngả sau = xoay dương, dời −x; phụt = chúi tới +x
    D.doi("bone3", -30.0 * p + 85.0 * x, 0.0)
    D.mat = "P_yanjing 3" if C_PHUN - 0.06 < t < C_PHUN + 0.12 else ("P_yanjing2" if 0.08 < t < 1.0 else "P_yanjing1")
    return D


# ---------------------------------------------------------------- skill: giơ hai vòi ngoài, uốn triệu hồi, bổ xuống ra lệnh
S_GIO, S_BO, S_DUR = 0.50, 1.65, 3.0
S_GOI = [0.62, 0.92, 1.22, 1.52]                  # mốc từng bạch tuộc con hiện ra
S_LENH = 1.77                                     # hai vòi bổ xuống: lệnh xông lên


def skill(t):
    """CHIÊU CUỐI 3,2 s (nguồn: skill_04): giơ hai vòi ngoài (xúc tu 1 và 6) 0 → 0,5; giữ trên cao và UỐN LƯỢN như múa gọi tới 2,2
    (sóng chạy từ gốc ra ngọn, hai vòi lệch pha, thân nhún theo); bổ hai vòi xuống 2,2 → 2,32 (lệnh); dư lực, về."""
    tau = cong([(0.0, 0.0), (S_GIO, 0.60), (S_BO, 0.66), (S_LENH, 0.89), (2.15, 1.15), (S_DUR, 2.0)], t,
               [em, None, lambda w: vao(w, 1.5), None, em])
    D = dk("skill_04", tau)
    g = cung(t, S_GIO - 0.2, S_GIO + 0.1, S_BO - 0.08, S_BO + 0.04)
    ph = 2 * math.pi * 1.55 * (t - S_GIO)
    # ở skill_04, vòi sau (xúc tu 6) giơ lộ ra bên kia thân ở 0,42 s rồi thu khuất sau vỏ: suốt lúc múa giữ dáng lộ đó
    m6 = nhom(T6)
    D.u[m6] = D.tron(dk("skill_04", 0.42), cung(t, 0.30, S_GIO, S_BO - 0.05, S_BO + 0.08), m6).u[m6]
    for j, (b, a) in enumerate((("bone13", 9.0), ("bone14", 15.0), ("bone15", 20.0), ("bone16", 24.0), ("bone17", 28.0))):
        D.xoay(b, g * a * math.sin(ph - 0.75 * j))
    for j, (b, a) in enumerate((("bone28", 9.0), ("bone29", 16.0), ("bone30", 22.0), ("bone31", 27.0))):
        D.xoay(b, -g * a * math.sin(ph - 0.75 * j + 2.2))
    D.dai("bone14", 1.0 + 0.30 * g)                         # hai vòi vươn cao hơn lúc múa (kéo ở đốt gốc của đoạn ngọn: hai đốt
    D.dai("bone29", 1.0 + 0.30 * g)                         # gốc gập vuông với nó, kéo ở đó thì ngọn bị xô dẹt)
    D.xoay("bone12", g * 7.0 * math.sin(ph + 0.6))
    D.xoay("bone27", -g * 7.0 * math.sin(ph + 2.8))
    D.doi("bone3", 0.0, g * 16.0 * math.sin(2 * ph + 0.5))
    D.xoay("bone3", g * 2.2 * math.sin(ph))
    for j, ch in enumerate(NGON):
        for q, b in enumerate(ch):
            D.xoay(b, g * (5.0 + 3.0 * q) * math.sin(2 * ph - 0.9 * j - 0.6 * q))
    D.mat = "P_yanjing 3" if S_GIO < t < S_BO - 0.1 else ("P_yanjing2" if 0.1 < t < 2.6 else "P_yanjing1")
    return D


# ---------------------------------------------------------------- walk: bò tại chỗ (game tự dời)
W_DUR = 1.2


def walk(t):
    """WALK 1,2 s lặp: ba xúc tu lớn lần lượt nhấc – vươn tới – bám – kéo (mục tiêu IK), thân nhô lên khi kéo, ba ngón nhỏ gợn sóng,
    ngọn các xúc tu trễ pha. Bò về phía trước (+x)."""
    D = nghi()
    u = (t / W_DUR) % 1.0

    def buoc(pha, dai_, cao):
        x = (u + pha) % 1.0
        if x < 0.35:                                  # nhấc, vươn tới
            s = x / 0.35
            return dai_ * (em(s) - 0.5), cao * math.sin(math.pi * s)
        s = (x - 0.35) / 0.65                         # bám đất, kéo về sau
        return dai_ * (0.5 - s), 0.0

    for cj, pha, dai_, cao in (("CJ2", 0.0, 110.0, 66.0), ("CJ1", 0.5, 105.0, 55.0), ("CJ3", 0.28, 105.0, 62.0)):
        dx, dy = buoc(pha, dai_, cao)
        D.doi(cj, dx, dy)
    a = 2 * math.pi * u
    D.doi("bone3", 6.0 * math.sin(a), 13.0 * math.sin(2 * a + 0.9))
    D.xoay("bone3", 2.4 * math.sin(a + 0.4))
    D.xoay("bone5", 1.6 * math.sin(2 * a + 2.0))
    for j, ch in enumerate(NGON):
        for q, b in enumerate(ch):
            D.xoay(b, (9.0 + 5.0 * q) * math.sin(a * 2 - 1.3 * j - 0.7 * q))
    for ch, pha in ((T1[2:], 0.0), (T2[2:], math.pi), (T6[2:], 1.8)):
        for q, b in enumerate(ch):
            D.xoay(b, (7.0 + 3.0 * q) * math.sin(a - pha - 0.6 * q - 0.8))
    return D


# ---------------------------------------------------------------- appear: trồi lên từ hố
P_SAU = 980.0             # thân nằm sâu chừng này dưới đất lúc đầu (đỉnh mào gai ở y ≈ 930; mũ của con gốc đã bỏ)
# mốc: vòi bắt đầu thò lên, bắt đầu vung xuống, NGỌN CHẠM ĐẤT, bắt đầu chống đẩy mạnh, thân lên cao nhất (nhả ngọn), hết clip
P_VOI, P_VUNG, P_BAM, P_KEO, P_LEN, P_DUR = 0.28, 0.86, 1.00, 1.20, 1.62, 2.75
# thu hai tay chống (người dùng 2026-11-12: "2 xúc tu thêm kia nên làm thêm 1 đoạn thu nó lại sau khi xuất hiện, thu vào trong sau đầu"):
# thân đáp xong thì ngọn nhấc khỏi đất (P_THU), rồi cả tay trượt vào sau đầu, khuất hẳn lúc P_THU_HET
P_THU, P_THU_HET = 1.86, 2.44
# P_THU_HET + trễ của tay (0,05) phải SỚM hơn P_DUR − 0,2: bộ xuất hoà 0,2 s cuối clip về khung 0 idle (khop_idle), tức kéo xương hai tay
# về tư thế gốc (duỗi thẳng ra ngoài). Tay còn hiện lúc đó thì thò ra mờ mờ sau đầu (người dùng báo "có mấy frame bị lỗi", 2026-11-12)
assert P_THU_HET + 0.05 < P_DUR - 0.2 - 0.03
# HAI TAY CHỐNG của appear là hai xúc tu DÀI riêng (dải lưới 10 đốt, bach_tuoc_rig.VOI), không phải xúc tu ngắn của thân: bản kéo dài
# xúc tu thân gấp 2,5 lần bị người dùng trả 2026-11-12 ("nhìn hơi xấu, bị gãy mesh nhiều": lưới của họ rất thưa và vẽ ở dáng cuộn).


def appear(t):
    """APPEAR 2,75 s, phần THÂN (người dùng: "phải để các xúc tu chạm đất nữa thì mới đẩy được cơ thể lên"). Hố mở 0 → 0,28; hai tay
    chống vươn lên 0,28 → 0,7, vung đập xuống đất hai bên miệng hố 0,86 → 1,00 (bam_dat); 1,00 → 1,20 gồng: thân nhích lên chậm, đầu
    bẹp nhẹ; 1,20 → 1,62 bị ĐẨY vọt lên khỏi hố, quá đà 120; rơi về chỗ, nhún tắt dần; 1,86 → 2,44 hai tay chống thu vào sau đầu. Thân giữ dáng nghỉ (các xúc tu của thân
    không kéo dài); hố, mặt nạ cắt và hai tay chống dựng ở bach_tuoc_rig.py theo đúng các mốc P_* ở đây."""
    R = nghi()
    D = R.chep()
    D.mat = "P_yanjing2" if P_BAM < t < P_LEN + 0.1 else "P_yanjing1"
    if t < P_BAM:
        dy = -P_SAU + 40.0 * cung(t, P_VOI, 0.7, P_BAM, P_BAM)
    elif t < P_KEO:
        dy = -P_SAU + 40.0 + 110.0 * em((t - P_BAM) / (P_KEO - P_BAM))
    elif t < P_LEN:
        dy = -P_SAU + 150.0 + (P_SAU - 150.0 + 120.0) * ra((t - P_KEO) / (P_LEN - P_KEO), 2.0)
    else:
        r = t - P_LEN
        dy = 120.0 * math.exp(-r * 6.5) * math.cos(r * 13.0)
    D.doi("bone2", 0.0, dy)
    r = t - P_LEN
    sq = (0.10 * cung(t, P_KEO, P_KEO + 0.2, P_LEN - 0.05, P_LEN + 0.1)
          - (0.12 * math.exp(-r * 6.0) * math.sin(r * 13.0 + 0.6) if r > 0 else 0.0)
          - 0.05 * cung(t, P_BAM, P_BAM + 0.1, P_KEO - 0.04, P_KEO + 0.06))          # gồng: đầu bẹp nhẹ trước khi bật
    i5 = ix("bone5")
    D.u[i5, 3] *= 1.0 + sq
    D.u[i5, 4] *= 1.0 - 0.6 * sq
    # các xúc tu của thân buông thõng lúc thân được nhấc lên rồi đung đưa tắt dần (ngọn trễ hơn gốc)
    k = cung(t, P_KEO, P_LEN, P_LEN, P_LEN + 0.5)
    for j, ch in enumerate(NGON):
        for q, b in enumerate(ch):
            D.xoay(b, (10.0 + 6.0 * q) * (k + (0.8 * math.exp(-r * 4.0) * math.sin(r * 11.0 - 0.7 * j - 0.5 * q) if r > 0 else 0.0)))
    for ch, s_ in ((T1[2:], 1.0), (T2[2:], 1.0), (T6[2:], -1.0)):
        for q, b in enumerate(ch):
            D.xoay(b, s_ * (5.0 + 3.0 * q) * (0.6 * k + (0.8 * math.exp(-r * 4.5) * math.sin(r * 10.0 - 0.6 * q) if r > 0 else 0.0)))
    return D


CLIP = {"bt_appear": (P_DUR, appear), "bt_attack": (A_DUR, attack), "bt_cast": (C_DUR, cast), "bt_skill": (S_DUR, skill),
        "bt_walk": (W_DUR, walk)}
SU_KIEN = {"bt_attack": [(A_TRUNG, "trung", "")], "bt_cast": [(C_PHUN, "phun", "")],
           "bt_skill": [(x, "trieu_hoi", str(i)) for i, x in enumerate(S_GOI)] + [(S_LENH, "lenh", "")],
           "bt_appear": [(0.0, "ho_mo", ""), (P_BAM, "bam_dat", ""), (P_KEO, "keo_len", ""), (P_LEN + 0.12, "cham_dat", "")],
           "bt_walk": []}


def dung():
    out = []
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        Kk = np.array([d.k for d in Ds])
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
        iks = {kn: [[round(t, 4), round(float(v), 4), -1] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS)
               if np.abs(Kk[:, j] - 1).max() > 1e-4}
        mat = []
        for t, d in zip(ts, Ds):
            if not mat or mat[-1][1] != d.mat:
                mat.append([round(t, 4), d.mat])
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": {"P_yanjing1": {"attachment": mat}}})
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "bt_extra.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "bt_extra.json"))


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-600:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    lenh = a[0] if a else "dung"
    if lenh == "dung":
        dung()
    elif lenh == "xem":
        dung()
        cl = a[1] if len(a) > 1 else ",".join(CLIP)
        n = a[2] if len(a) > 2 else "12"
        view = f"&view={a[3]}" if len(a) > 3 and a[3] else ""
        tt = (f"&t0={a[4]}" if len(a) > 4 else "") + (f"&t1={a[5]}" if len(a) > 5 else "")
        _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={cl}&extra=bt_extra.json&n={n}&tw=330&th=290&cols=8{view}{tt}")
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "bt_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
