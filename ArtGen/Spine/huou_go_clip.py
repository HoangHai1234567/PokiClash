# -*- coding: utf-8 -*-
"""Hươu gỗ cổ dài: clip RIÊNG theo ý người dùng (2026-11-12), dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3504 rồi để runtime Spine
thật nướng (cách của bach_tuoc_clip.py / tuong_da_clip.py; skill pokiclash-spine-rig mục 00 "CLIP MỚI trên rig gốc").

Người dùng:
- idle / walk: giống họ (idle_01, run_01).
- đánh thường: lao tới dùng sừng húc.
- chiêu mana: hơi cúi đầu, tụ một quả cầu năng lượng nhỏ ở giữa hai sừng rồi bắn một tia từ quả cầu đó vào đối thủ.
- chiêu cuối: đứng bằng hai chân, ngửa đầu há to mồm tụ một quả cầu siêu to, tụ xong gật đầu nện mạnh vào đối thủ.
- die: gục xuống (die_01).           - appear: mở một cánh cổng teleport kiểu rừng rồi con vật walk qua.

Rig gốc (con nhìn sang PHẢI, +x là phía trước):
  root > all > xy (dời cả con) > bone3 (hông / thân, góc gốc 90) > bone4 (lưng) > bone5 (ngực) > bone6a > bone6b > bone6b2 (cổ) > bone7 (đầu)
  đầu: gạc bone10-11-32, bone33-34, bone35-36, bone37-38-39; tai bone40.. / bone45..; bờm bone6b7 > bốn chuỗi
  chân trước: bone12 > bone13 > bone14 (IK SR1), bone17 > bone18 > bone19 (IK SL1); chân sau: bone22 > bone23 > bone70 (IK R1) > bone24
  (IK R2), bone28 > bone29 > bone71 (IK L1) > bone30 (IK L2); đuôi bone8 > bone9 > các chuỗi lá.
  Thứ tự IK trong mẫu khung: L1, L2, R1, R2, SL1, SR1.
Không có xương hàm: mồm há / ngậm là kênh riêng `ham` cho rig của MÌNH.

Kênh riêng (ghi <scan>/kenh_rieng.json): ham 0..1 (độ há mồm), cau = (bán kính đơn vị rig, x, y thế giới) quả cầu năng lượng (chỗ gắn
VFX), bay = cung dời xương move (đòn thường lao tới, appear đi vào), cong 0..1 (cánh cổng mở).

    huou_go_clip.py dung                 ghép, ghi <scan>/lam_clip/hg_extra.json
    huou_go_clip.py xem [clip,..|het] [n] [view|het] [t0] [t1]   tờ khung trên rig gốc → <scan>/lam_clip/khung/<clip>.jpg
    huou_go_clip.py song                 trang xem SỐNG (runtime Spine thật, 60 khung/giây) → <scan>/lam_clip/xem/xem.html
    huou_go_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (huou_go_rig.py đọc)
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
MON = "monster_3504"
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
PA = [b["parent"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]                 # L1, L2, R1, R2, SL1, SR1
ix = TEN.index
_S = None

CO = ["bone6a", "bone6b", "bone6b2", "bone7"]                              # cổ + đầu
CHUOI_DAU = ["root", "all", "xy", "bone3", "bone4", "bone5", "bone6a", "bone6b", "bone6b2", "bone7"]      # FK thuần tới đầu
# điểm trong hệ xương đầu (bone7), tính từ dáng gốc: đầu ở thế giới x 14..170, y 377..550 (tâm 98, 466); bone7 ở (101,6; 473,1) góc −52,4
TAM_SO = (98.0, 466.0)                             # tâm sọ
GIUA_SUNG = (96.0, 612.0)                          # giữa hai gạc, trên đỉnh đầu: chỗ tụ cầu nhỏ của chiêu mana
HUONG_MOM = (0.67, -0.74)                          # hướng mõm ở dáng gốc (chĩa xuống phải)
CAU_NHO, CAU_TO = 46.0, 175.0                      # bán kính cầu mana / cầu chiêu cuối (đơn vị rig)


def nhom(ds):
    m = np.zeros(len(TEN), bool)
    for n in ds:
        m[ix(n)] = True
    return m


def con_chau(goc):
    m = np.zeros(len(TEN), bool)
    m[ix(goc)] = True
    for i, p in enumerate(PA):                     # xương xếp cha trước con
        if p >= 0 and m[p]:
            m[i] = True
    return m


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k (6) độ trộn IK; ex = kênh riêng."""

    def __init__(self, u, k, ex=None):
        self.u, self.k = u, k
        self.ex = ex or dict(ham=0.0, cau=(0.0, 0.0, 0.0), cong=0.0)

    def chep(self):
        return Dang(self.u.copy(), self.k.copy(), dict(self.ex))

    def tron(self, B, w, mat_na=None):
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        return Dang(self.u + (B.u - self.u) * ww[:, None], self.k + (B.k - self.k) * (float(w) if mat_na is None else 0.0), dict(self.ex))

    def xoay(self, ten, do):
        self.u[ix(ten), 2] += do
        return self

    def doi(self, ten, dx, dy):
        self.u[ix(ten), 0] += dx
        self.u[ix(ten), 1] += dy
        return self


def nap():
    global _S
    if _S is None:
        S = json.load(open(os.path.join(SCAN, "sample_dk.json"), encoding="utf-8"))
        _S = {}
        for c, v in S.items():
            U = np.array([f["u"] for f in v["frames"]], float)
            U[:, :, 2] = np.degrees(np.unwrap(np.radians(U[:, :, 2]), axis=0))          # bỏ bước nhảy 360 giữa hai khung
            U[:, :, 2] += 360.0 * np.round((B0[None, :, 2] - U[:1, :, 2]) / 360.0)      # khung đầu gần dáng gốc
            _S[c] = (float(v["dur"]), U, np.array([[q[0] for q in f["k"]] for f in v["frames"]], float))
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w)


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


def rung(t, t0, bien, tan=6.0, hz=5.0, pha=0.0):
    r = t - t0
    return bien * math.exp(-r * tan) * math.sin(2 * math.pi * hz * r + pha) if r > 0 else 0.0


def giat(t, bien, hz=19.0, pha=0.0):
    return bien * (math.sin(2 * math.pi * hz * t + pha) * 0.6 + math.sin(2 * math.pi * hz * 1.73 * t + 1.3 + pha) * 0.4)


def ma(x, y, rot, sx=1.0, sy=1.0):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0, 0, 1.0]])


def dau_tg(u):
    """ma trận thế giới của xương đầu (bone7): FK thuần dọc chuỗi (chuỗi này không có ràng buộc)."""
    M = np.eye(3)
    for n in CHUOI_DAU:
        M = M @ ma(*u[ix(n)])
    return M


def tg(u, ten):
    """ma trận thế giới của một xương theo FK thuần (chưa áp ràng buộc): dùng cho xương không bị IK lái, hoặc chân đang ở chế độ FK."""
    ch, i = [], ix(ten)
    while i >= 0:
        ch.append(i)
        i = PA[i]
    M = np.eye(3)
    for i in reversed(ch):
        M = M @ ma(*u[i])
    return M


DAI = {b["name"]: b["len"] for b in I["bones"]}
# (IK của khúc cuối, xương cuối của chân, xương đích, góc lệch của xương bàn chân so với xương cuối: ràng buộc transform của họ)
CHAN_IK = [("SR1", "bone14", "SR1", 12.658), ("SL1", "bone19", "SL1", 8.855), ("R2", "bone24", "R2", 18.431), ("L2", "bone30", "L2", 17.297)]


def chuan_ik(D):
    """DA khúc chân dưới bám một phần vào XƯƠNG BÀN CHÂN (bone15, bone20, bone25, bone31), xương này là con của ĐÍCH IK. Clip của họ khi
    chuyển chân sang FK (độ trộn IK = 0) thì bật ràng buộc transform cho bàn chân theo chân; mẫu khung của mình (u, k) KHÔNG mang độ
    trộn transform nên bàn chân nằm lại ở đích cũ → da chân bị kéo dài (người dùng 2026-11-12: "tôi vẫn thấy bị stretch"). Chuẩn hoá:
    chân nào IK < 1 thì dời ĐÍCH tới đúng đầu mút FK của chân (và xoay đích cho bàn chân đúng hướng), rồi đặt IK = 1."""
    A = np.linalg.inv(tg(D.u, "all"))
    for kn, cuoi, dich, off in CHAN_IK:
        j = IKS.index(kn)
        mix = float(D.k[j])
        if mix > 0.999:
            continue
        M = tg(D.u, cuoi)
        loc = A @ (M @ np.array([DAI[cuoi], 0.0, 1.0]))
        rot = math.degrees(math.atan2(M[1, 0], M[0, 0])) + off
        i, w = ix(dich), 1.0 - mix
        D.u[i, 0] += (loc[0] - D.u[i, 0]) * w
        D.u[i, 1] += (loc[1] - D.u[i, 1]) * w
        D.u[i, 2] += (((rot - D.u[i, 2] + 180.0) % 360.0) - 180.0) * w
        D.k[j] = 1.0
    for kn in ("R1", "L1"):
        D.k[IKS.index(kn)] = 1.0
    return D


TAM_VOI = 0.97 * (DAI["bone23"] + DAI["bone70"] + DAI["bone24"])     # tầm với của chân sau (hông → đích), chừa 6% cho khớp còn gập


def dung_len(e):
    """dáng ĐỨNG LÊN hai chân sau (e = 0..1), dựng từ dáng nghỉ, KHÔNG kéo dãn chân: xoay cả thân quanh hông (bone3), hạ hông cho
    hai chân sau (móng vẫn ghim trên đất) còn trong tầm với, hai chân trước thả theo ngực (FK), hơi co."""
    D = nghi()
    D.xoay("bone3", 30.0 * e)
    D.doi("bone3", -10.0 * e, 0.0)
    D.doi("L2", -34.0 * e, 0.0)                    # chân sau xa bước lùi vào dưới hông (hông đó bị nâng lên khi thân xoay)
    # đùi sau (bone22, bone28: FK, con của lưng) giữ nguyên hướng thế giới: không thì thân xoay kéo gối ra xa bàn chân, vòng hạ hông
    # bên dưới phải hạ rất sâu (bản trước: con vật ngồi xổm chứ không đứng lên)
    D.xoay("bone22", -30.0 * e)
    D.xoay("bone28", -30.0 * e)
    for kn in ("SR1", "SL1"):
        D.k[IKS.index(kn)] = 1.0 - e
    # hai chân trước: trả lại gần hết góc xoay của thân (buông xuống), gập gối
    D.xoay("bone12", -22.0 * e)
    D.xoay("bone13", -34.0 * e)
    D.xoay("bone14", 42.0 * e)
    D.xoay("bone17", -30.0 * e)
    D.xoay("bone18", -30.0 * e)
    D.xoay("bone19", 46.0 * e)
    A = tg(D.u, "all")
    for _ in range(4):                             # hạ hông tới khi cả hai chân sau trong tầm với
        thua = 0.0
        for hong, dich in (("bone23", "R2"), ("bone29", "L2")):
            h_ = tg(D.u, hong)[:2, 2]
            d_ = (A @ np.array([D.u[ix(dich), 0], D.u[ix(dich), 1], 1.0]))[:2]
            thua = max(thua, float(np.hypot(*(h_ - d_))) - TAM_VOI)
        if thua <= 0.5:
            break
        D.doi("bone3", 0.0, -thua)
    return D


_M0 = np.linalg.inv(dau_tg(B0))
L_SO = _M0 @ np.array([TAM_SO[0], TAM_SO[1], 1.0])
L_SUNG = _M0 @ np.array([GIUA_SUNG[0], GIUA_SUNG[1], 1.0])
L_MOM = _M0[:2, :2] @ np.array(HUONG_MOM)


def cui(D, c):
    """cúi cổ về trước (c > 0) hoặc ngửa ra sau (c < 0): chia góc dọc ngực → cổ → đầu. Con nhìn +x nên cúi = quay thuận kim (âm)."""
    D.xoay("bone5", -7.0 * c)
    D.xoay("bone6a", -20.0 * c)
    D.xoay("bone6b", -9.0 * c)
    D.xoay("bone6b2", -5.0 * c)
    D.xoay("bone7", -8.0 * c)
    return D


def cau_sung(D, r):
    p = dau_tg(D.u) @ L_SUNG
    D.ex["cau"] = (r, float(p[0]), float(p[1]))


def cau_mom(D, r, xa=1.0):
    """cầu trước mõm: tâm cách tâm sọ (150 + 40 + bán kính) theo hướng mõm."""
    M = dau_tg(D.u)
    h = M[:2, :2] @ L_MOM
    h = h / np.hypot(*h)
    p = (M @ L_SO)[:2] + h * (150.0 + 40.0 * xa + r)
    D.ex["cau"] = (r, float(p[0]), float(p[1]))


# ---------------------------------------------------------------- idle, walk, hit, die: nguyên của họ
def idle(t):
    return dk("idle_01", t, True)


def walk(t):
    return dk("run_01", t, True)


def hit(t):
    return dk("hit_01", t)


def die(t):
    return dk("die_01", t)


# ---------------------------------------------------------------- attack: lao tới, húc sừng
A_CHAY, A_DA, A_TRUNG, A_GIU, A_DUR = 0.34, 0.47, 0.58, 0.78, 1.40
A_XA = 430.0


def attack_bay(t):
    x = cong([(0.0, 0.0), (0.06, 0.0), (A_CHAY, 0.66 * A_XA), (A_DA, 0.80 * A_XA), (A_TRUNG, A_XA), (A_GIU, A_XA), (1.22, 0.0)], t,
             [None, lambda w: vao(w, 1.6), None, lambda w: vao(w, 1.5), None, em])
    y = 70.0 * math.sin(math.pi * (t - A_GIU) / (1.22 - A_GIU)) if A_GIU < t < 1.22 else 0.0          # nhảy lùi về
    return x - 14.0 * rung(t, A_TRUNG, 1.0, 9.0, 5.5), y


def attack(t):
    """ĐÒN THƯỜNG 1,40 s. Chạy lao tới 0,06 → 0,34 (run_01, đầu chúi dần); chồm lấy đà 0,34 → 0,47 (dựng hai chân trước, đầu ngẩng: nửa
    đầu skill_01_1); HÚC 0,47 → 0,58: bổ đầu xuống – tới, gạc quật ra trước (skill_01_1 0,39 → 0,65), sự kiện trung 0,58; khựng tới
    0,78; ngẩng lên, nhảy lùi về chỗ 1,22; hoà về nghỉ."""
    R = nghi()
    tau = cong([(A_CHAY - 0.06, 0.13), (A_DA, 0.39), (A_TRUNG, 0.65), (A_GIU, 0.80), (1.20, 1.1667)], t, [em, lambda w: vao(w, 1.7), None, em])
    D = dk("skill_01_1", tau)
    if t < A_CHAY + 0.06:                          # quãng chạy: run_01, hoà từ nghỉ vào và hoà sang cú chồm
        Rn = dk("run_01", (t - 0.04) * 1.15, True)
        cui(Rn, 0.55 * em(t / 0.2))
        Rn = R.tron(Rn, em(t / 0.10))
        D = Rn.tron(D, em((t - (A_CHAY - 0.06)) / 0.12))
    cui(D, 0.35 * cung(t, A_TRUNG - 0.04, A_TRUNG, A_GIU, A_GIU + 0.12))               # húc sâu thêm, giữ
    D.xoay("bone7", rung(t, A_TRUNG, 7.0, 8.0, 6.0))
    D.doi("bone3", 0.0, -rung(t, A_TRUNG, 10.0, 8.0, 6.0, 1.2))
    return D.tron(R, em((t - 1.20) / 0.20)) if t > 1.20 else D


# ---------------------------------------------------------------- cast: hơi cúi đầu, tụ cầu nhỏ giữa hai sừng, bắn tia
C_CUI, C_PHUN, C_HET, C_DUR = 0.36, 1.00, 1.94, 2.35
C_MUC = 0.45                                       # "hơi cúi đầu": 45% mức cúi của cú húc (bản đầu cúi 100% thành gập cổ)


def cast(t):
    """CHIÊU MANA 2,35 s, đứng tại chỗ. Cúi đầu 0 → 0,36 (hai gạc chĩa về trước, thân hạ nhẹ, lùi một chút); tụ cầu nhỏ giữa hai gạc
    0,36 → 1,00 (cầu lớn dần, đầu rung nhẹ mạnh dần); BẮN tia 1,00 (sự kiện phun): đầu giật ngược lên một nhịp, thân giật lùi, rồi
    ghìm giữ tia tới 1,94 (rung nhỏ; tia của game chảy 0,88 s sau phun); cầu tắt, ngẩng lên, lắc bờm, về nghỉ."""
    D = dk("idle_01", t, True)
    c = cong([(0.0, 0.0), (C_CUI, 1.0), (C_PHUN - 0.06, 1.12), (C_PHUN + 0.05, 0.72), (C_PHUN + 0.22, 0.90), (C_HET, 0.90), (C_DUR - 0.05, 0.0)], t,
             [em, em, lambda w: ra(w, 2.2), em, None, em])
    tu = cung(t, C_CUI, C_PHUN - 0.05, C_PHUN - 0.05, C_PHUN)                        # mức gồng lúc tụ
    giu = cung(t, C_PHUN, C_PHUN + 0.05, C_HET - 0.1, C_HET + 0.05)
    cui(D, C_MUC * c + 0.035 * giat(t, 1.0, 17.0) * (0.3 + 0.7 * tu) * (tu > 0) + 0.02 * giat(t, 1.0, 23.0, 0.8) * giu)
    lui = -16.0 * em(t / C_CUI) * (1 - em((t - C_HET) / 0.3)) - 30.0 * cung(t, C_PHUN - 0.01, C_PHUN + 0.05, C_PHUN + 0.12, C_PHUN + 0.5)
    D.doi("bone3", lui, -9.0 * cung(t, 0.0, C_CUI, C_HET, C_DUR - 0.05) + giat(t, 1.6, 21.0, 2.0) * giu)
    D.xoay("bone4", 2.0 * cung(t, C_PHUN, C_PHUN + 0.05, C_PHUN + 0.15, C_PHUN + 0.5))
    D.xoay("bone7", rung(t, C_HET + 0.12, 6.0, 5.0, 4.0))                              # lắc đầu sau khi ngẩng
    r = CAU_NHO * (cong([(C_CUI - 0.04, 0.0), (C_PHUN - 0.06, 0.92), (C_PHUN, 1.25), (C_PHUN + 0.1, 1.0), (C_HET - 0.08, 0.9), (C_HET + 0.06, 0.0)], t,
                        [lambda w: ra(w, 1.6), None, None, None, em]) + 0.05 * giat(t, 1.0, 13.0) * (tu > 0 or giu > 0))
    cau_sung(D, max(0.0, r))
    return D


# ---------------------------------------------------------------- skill: đứng hai chân, ngửa đầu há mồm tụ cầu to, gật đầu nện
S_DUNG, S_HA, S_DAY, S_NEN, S_TRUNG, S_GIU, S_DUR = 0.42, 0.60, 1.80, 1.96, 2.08, 2.50, 3.10
CHAN = ["bone12", "bone13", "bone14", "bone17", "bone18", "bone19", "bone22", "bone23", "bone70", "bone24", "bone28", "bone29", "bone71", "bone30"]
S_HA_THAN = -18.0                                  # hạ hông chừng này lúc dựng người để hai móng sau vẫn chạm đất khi chân không dãn
T_DUNG = 0.16                                      # dáng chồm hai chân sau lấy ở die_01 (0,11 → 0,22 s họ dựng thẳng người)


def skill(t):
    """CHIÊU CUỐI 3,10 s, đứng tại chỗ. Nhún rồi DỰNG người lên hai chân sau 0 → 0,42 (dáng chồm của họ ở die_01 0,16 s); ngửa đầu, HÁ
    to mồm 0,42 → 0,60; tụ cầu siêu to trước mõm tới 1,80 (cầu lớn dần, cả người rung mạnh dần, hai chân trước đạp nhẹ trong không
    khí, người ngả dần ra sau vì cầu nặng); 1,80 → 1,96 ngả hẳn ra sau lấy đà; GẬT đầu NỆN xuống 1,96 → 2,08 (về dáng bổ đầu của
    skill_01_1 0,65 s: hai chân trước dộng xuống đất, gạc và mõm quật ra trước), cầu rời mõm (sự kiện nem 2,02, trung 2,08); khựng,
    rung tới 2,50; ngậm mồm, ngẩng lên, về nghỉ."""
    R = nghi()
    Dg = dung_len(1.0)                             # dáng dựng hai chân (tự dựng, không kéo dãn chân; bản đầu lấy die_01 0,16 s của họ)
    Bo = dk("skill_01_1", 0.65)                    # dáng bổ đầu
    if t < S_NEN:
        nhun = cung(t, 0.0, 0.12, 0.14, 0.30)
        D = dung_len(cong([(0.10, 0.0), (S_DUNG, 1.0)], t, [lambda w: em(ra(w, 1.4))]))
        D.doi("bone3", 0.0, -16.0 * nhun)
    elif t < S_GIU:
        D = Dg.tron(Bo, cong([(S_NEN, 0.0), (S_TRUNG, 1.0)], t, [lambda w: vao(w, 2.2)]))
    else:
        D = dk("skill_01_1", cong([(S_GIU, 0.65), (S_DUR - 0.12, 1.1667)], t, [em]))
        D = D.tron(R, em((t - (S_DUR - 0.25)) / 0.25))
    # KHÔNG kéo dãn chân (người dùng 2026-11-12, xem rig dạng 2: "chiêu cuối dạng 2 không stretch chân trước và chân sau, làm nó đứng
    # lên thôi là được"): die_01 và skill_01_1 của họ có khoá tỉ lệ trên xương chân (tới 1,4 lần) → trả tỉ lệ mọi xương chân về dáng gốc
    for b_ in CHAN:
        D.u[ix(b_), 3:5] = B0[ix(b_), 3:5]
    tu = cung(t, S_HA, S_DAY, S_DAY, S_NEN)                                          # 0 → 1 trong lúc tụ
    nga = cong([(S_DUNG - 0.1, 0.0), (S_HA, 0.9), (S_DAY, 1.25), (S_NEN, 1.75), (S_NEN + 0.07, 0.0)], t, [em, None, em, lambda w: vao(w, 2.0)])
    cui(D, -nga * 0.40)                                                              # ngửa cổ, đầu
    D.xoay("bone7", 9.0 * nga)                                                       # mõm chĩa lên
    D.xoay("bone4", 3.0 * nga)
    lac = (0.25 + 0.75 * vao(tu, 1.5)) * (S_HA < t < S_NEN)
    D.xoay("bone7", giat(t, 1.6, 16.0) * lac)
    D.xoay("bone6a", giat(t, 1.1, 14.0, 1.0) * lac)
    D.doi("bone3", giat(t, 2.2, 15.0, 2.0) * lac - 18.0 * cung(t, S_DAY, S_NEN, S_NEN, S_NEN + 0.08), giat(t, 2.0, 18.0, 0.5) * lac)
    dap = cung(t, S_DUNG, S_HA, S_DAY, S_NEN)                                        # hai chân trước đạp nhẹ trong không khí (FK)
    D.xoay("bone13", 9.0 * dap * math.sin(2 * math.pi * 1.6 * t))
    D.xoay("bone18", 9.0 * dap * math.sin(2 * math.pi * 1.6 * t + 2.4))
    # nện xong: rung tắt dần
    D.xoay("bone7", rung(t, S_TRUNG, 9.0, 7.0, 6.0))
    D.doi("bone3", rung(t, S_TRUNG, 12.0, 8.0, 6.5), -rung(t, S_TRUNG, 12.0, 8.0, 6.5, 1.3))
    D.ex["ham"] = cong([(S_DUNG - 0.04, 0.0), (S_HA, 1.0), (S_GIU - 0.1, 1.0), (S_GIU + 0.18, 0.0)], t, [lambda w: ra(w, 2.0), None, em]) \
        * (1.0 + 0.04 * giat(t, 1.0, 12.0) * lac)
    r = CAU_TO * cong([(S_HA - 0.02, 0.0), (S_DAY, 1.0), (S_NEN + 0.06, 1.08), (S_NEN + 0.10, 0.0)], t, [lambda w: ra(w, 1.5), None, None])
    cau_mom(D, max(0.0, r * (1.0 + 0.03 * giat(t, 1.0, 11.0) * lac)))
    return D


# ---------------------------------------------------------------- appear: cổng rừng mở, con vật bước qua
P_MO, P_RA, P_TOI, P_DONG, P_DUR = 0.40, 0.46, 1.62, 2.10, 2.40
P_XA = 760.0                                       # lúc đầu đứng lùi sau chừng này (khuất hẳn sau mặt cổng)
P_CONG = -400.0                                    # mặt cổng ở x thế giới này (sau đuôi con vật khi đã tới chỗ)


def appear_bay(t):
    return -P_XA * (1.0 - cong([(P_RA, 0.0), (P_TOI, 1.0)], t, [lambda w: ra(w, 1.35)])), 0.0


def appear(t):
    """APPEAR 2,40 s. Cổng rừng mở 0 → 0,40 (rig của mình: vòng cổng lớn dần, xoay nhẹ; sự kiện cong_mo 0); con vật bước ra khỏi mặt
    cổng 0,46 → 1,62 (run_01 chậm 0,62 lần thành nhịp đi nước kiệu, đi chậm dần; phần chưa qua cổng bị mặt nạ cắt giấu); tới chỗ:
    dừng, ngẩng đầu, lắc bờm một nhịp; cổng khép 1,62 → 2,10 (cong_dong); hoà về nghỉ."""
    R = nghi()
    di = dk("run_01", (t - P_RA) * 0.62, True)
    cui(di, 0.25)
    w = 1.0 - em((t - (P_TOI - 0.22)) / 0.30)
    D = R.tron(di, w if t > P_RA - 0.05 else 0.0)
    ng = cung(t, P_TOI - 0.05, P_TOI + 0.20, P_TOI + 0.32, P_DUR - 0.08)
    cui(D, -0.5 * ng)
    D.xoay("bone7", rung(t, P_TOI + 0.22, 9.0, 4.0, 3.6))
    D.xoay("bone6b", rung(t, P_TOI + 0.22, 4.0, 4.0, 3.6, 0.7))
    D.ex["cong"] = cong([(0.0, 0.0), (P_MO, 1.0), (P_TOI + 0.04, 1.0), (P_DONG, 0.0)], t, [lambda w: ra(w, 2.2), None, lambda w: vao(w, 1.8)])
    return D


CLIP = {"hg_idle": (5.3333, idle), "hg_walk": (0.5333, walk), "hg_attack": (A_DUR, attack), "hg_cast": (C_DUR, cast),
        "hg_skill": (S_DUR, skill), "hg_appear": (P_DUR, appear), "hg_hit": (0.5, hit), "hg_die": (1.0, die)}
LAP = {"hg_idle", "hg_walk"}
BAY = {"hg_attack": attack_bay, "hg_appear": appear_bay}
SU_KIEN = {"hg_attack": [(A_TRUNG, "trung", "")],
           "hg_cast": [(C_CUI, "tu", ""), (C_PHUN, "phun", ""), (C_HET, "het_phun", "")],
           "hg_skill": [(S_HA, "tu", ""), (S_DAY, "day", ""), (S_NEN + 0.06, "nem", ""), (S_TRUNG, "trung", "")],
           "hg_appear": [(0.0, "cong_mo", ""), (P_RA, "buoc_ra", ""), (P_TOI + 0.04, "cong_dong", "")]}


def dung(xem=False):
    out = []
    rieng = {}
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [chuan_ik(fn(t)) for t in ts]
        U = np.array([d.u for d in Ds])
        Kk = np.array([d.k for d in Ds])
        bay = [list(BAY[ten](t)) if ten in BAY else [0.0, 0.0] for t in ts]
        if xem and ten in BAY:                     # giả lập ngay trên rig gốc phần xương move của rig mình lo
            U[:, ix("all"), :2] += np.array(bay)
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
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks, "slots": {}})
        rieng[ten] = {"dur": dur, "ham": [float(d.ex["ham"]) for d in Ds], "cau": [list(d.ex["cau"]) for d in Ds],
                      "cong": [float(d.ex["cong"]) for d in Ds], "bay": bay, "su_kien": SU_KIEN.get(ten, []), "lap": ten in LAP}
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "hg_extra.json"), "w", encoding="utf-8"))
    if not xem:
        json.dump(rieng, open(os.path.join(SCAN, "kenh_rieng.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "hg_extra.json"))
    return rieng


def _chay(*a):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "chay.py"), *a], capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace")[-900:])
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-1500:])
        sys.exit(1)


VIEW = "0,360,1500,1000"
VIEW_RIENG = {"hg_attack": "230,360,1800,1000", "hg_skill": "60,470,1800,1250", "hg_appear": "-300,360,1900,1000",
              "hg_cast": "60,400,1700,1050"}

TRANG = r"""<!doctype html><html><head><meta charset="utf-8"><title>huou_go: clip trên rig gốc</title>
<style>body{background:#22252b;color:#ddd;font:14px sans-serif;margin:14px}button{background:#333842;color:#ddd;border:1px solid #555;
border-radius:6px;padding:6px 12px;margin:3px;font:14px sans-serif;cursor:pointer}button.on{background:#e8a33c;color:#111;border-color:#e8a33c}
#khung{position:relative;width:1100px;height:700px;margin-top:10px}canvas{position:absolute;left:0;top:0;border-radius:8px}#cv{background:#6b7079}
#st{color:#9ab}#mo{margin:6px 2px;max-width:1080px;line-height:1.45}</style></head><body>
<div><b>huou_go</b>: clip dựng ở tầng điều khiển, chạy bằng runtime Spine thật trên RIG GỐC (hình của game tham khảo, chỉ xem nội bộ).
Quãng lao của đòn thường và quãng đi vào của appear là giả lập phần xương move lo. Vòng tròn = chỗ và cỡ quả cầu năng lượng (VFX làm
sau); "mồm" = độ há (rig gốc không có hàm, rig của mình mới há được); vòng bầu dục + mảng che = cánh cổng và phần bị mặt nạ giấu.
<span id="st">đang nạp</span></div>
<div id="nut"></div><div>tốc độ: <span id="td"></span> &nbsp; <label><input type="checkbox" id="lap" checked> phát lại liên tục</label></div>
<div id="mo"></div><div id="khung"><canvas id="cv" width="1100" height="700"></canvas><canvas id="ov" width="1100" height="700"></canvas></div>
<script src="__LIB__"></script>
<script>
const NAME="__MON__", SKEL="__SKEL__", ATLAS=__ATLAS__, PNG="__PNG__", EXTRA=__EXTRA__, INFO=__INFO__, KENH=__KENH__, XCONG=__XCONG__;
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
  for(const c of Object.keys(INFO)){const b=document.createElement("button");b.textContent=c.replace("hg_","");b.dataset.clip=c;b.onclick=()=>chon(c);nut.appendChild(b);}
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
    const X=x=>550+(x-vx)/z, Y=y=>350-(y-vy)/z;
    const ham=kenh(cur,"ham",t), cau=kenh(cur,"cau",t), bay=kenh(cur,"bay",t), cg=kenh(cur,"cong",t);
    ov.strokeStyle="rgba(40,30,20,.35)";ov.lineWidth=1;ov.beginPath();ov.moveTo(0,Y(0));ov.lineTo(1100,Y(0));ov.stroke();
    if(cur==="hg_appear"){ov.fillStyle="rgb(107,112,121)";ov.fillRect(0,0,X(XCONG),Y(0));
      if(cg>0.01){ov.strokeStyle="rgba(120,220,120,.95)";ov.fillStyle="rgba(60,150,90,.35)";ov.lineWidth=7;ov.beginPath();
        ov.ellipse(X(XCONG),Y(370),95*cg/z,390*cg/z,0,0,6.2832);ov.fill();ov.stroke();}}
    if(cau[0]>0.5){const x=X(cau[1]+bay[0]), y=Y(cau[2]+bay[1]), r=cau[0]/z;
      ov.fillStyle="rgba(110,230,150,.55)";ov.strokeStyle="rgba(30,110,60,.9)";ov.lineWidth=3;ov.beginPath();ov.arc(x,y,r,0,6.2832);ov.fill();ov.stroke();}
    ov.fillStyle=ham>0.05?"#fd8":"#bcd";ov.font="15px sans-serif";ov.fillText("mồm há "+Math.round(ham*100)+"%   t = "+t.toFixed(2)+" s",14,24);
    requestAnimationFrame(ve);
  }
  requestAnimationFrame(ve);
}
main().catch(e=>{st.textContent="LOI "+e+" "+(e.stack||"");});
</script></body></html>"""

MO_TA = {"hg_idle": "nguyên idle_01 của họ (thở, cổ đung đưa, tai và bờm lá lay, lá rơi)",
         "hg_walk": "nguyên run_01 của họ (phi nước kiệu); game lo dời ngang",
         "hg_attack": "chạy lao tới (đầu chúi), tới nơi chồm hai chân trước lấy đà rồi BỔ đầu húc gạc vào đối thủ; khựng; nhảy lùi về",
         "hg_cast": "hơi cúi đầu, tụ cầu nhỏ giữa hai gạc (đầu rung mạnh dần); BẮN tia: đầu giật lên, thân giật lùi, ghìm giữ tia; ngẩng lên, lắc đầu",
         "hg_skill": "nhún, DỰNG người lên hai chân sau, ngửa đầu HÁ to mồm, tụ cầu siêu to trước mõm (rung mạnh dần, chân trước đạp nhẹ); ngả sau lấy đà; GẬT đầu NỆN cầu xuống đối thủ, hai chân trước dộng đất; khựng; ngậm mồm, về nghỉ",
         "hg_appear": "cổng rừng mở phía sau, con vật bước nước kiệu ra khỏi cổng (phần chưa qua cổng bị giấu), tới chỗ thì ngẩng đầu lắc bờm; cổng khép",
         "hg_hit": "nguyên hit_01 của họ", "hg_die": "nguyên die_01 của họ: chồm lên rồi gục đổ nghiêng xuống đất"}


def song():
    """trang xem SỐNG (runtime Spine thật, 60 khung/giây, mở bằng file://) trên rig gốc → <scan>/lam_clip/xem/xem.html."""
    import base64
    dung(xem=True)
    extra = open(os.path.join(LAM, "hg_extra.json"), encoding="utf-8").read()
    rieng = dung()
    mo_xe = open(os.path.join(HERE, "mo_xe", "mo_xe.html"), encoding="utf-8").read()
    a = mo_xe.index("function addExtra(data, list) {")
    b = mo_xe.index("// lấy mẫu 30 khung/giây")
    b64 = lambda f: base64.b64encode(open(os.path.join(RIG, f), "rb").read()).decode()
    info = {c: {"dur": CLIP[c][0], "lap": c in LAP, "view": [float(x) for x in VIEW_RIENG.get(c, VIEW).split(",")], "mo": MO_TA.get(c, ""),
                "ev": ", ".join(f"{e}{' ' + s if s else ''} {x:.2f} s" for x, e, s in SU_KIEN.get(c, []))} for c in CLIP}
    kenh = {c: {k: rieng[c][k] for k in ("ham", "cau", "bay", "cong")} for c in CLIP}
    lib = "file:///" + os.path.join(HERE, "lib", "spine-player.js").replace(os.sep, "/")
    h = (TRANG.replace("__LIB__", lib).replace("__MON__", MON).replace("__SKEL__", b64(MON + ".skel"))
         .replace("__ATLAS__", json.dumps(open(os.path.join(RIG, MON + ".atlas"), encoding="utf-8").read()))
         .replace("__PNG__", "data:image/png;base64," + b64(MON + ".png")).replace("__EXTRA__", extra).replace("__XCONG__", str(P_CONG))
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
            _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={c}&extra=hg_extra.json&n={n}&tw=380&th={int(round(380 * vh / vw))}&cols=8&view={view}{tt}")
        dung()
    elif lenh == "song":
        song()
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "hg_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
