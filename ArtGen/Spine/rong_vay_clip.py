# -*- coding: utf-8 -*-
"""Rồng vây: clip RIÊNG của mình, dựng ở TẦNG ĐIỀU KHIỂN của rig gốc (người dùng 2026-11-12: appear uốn lượn bay vào rồi gầm; đánh
thường quật đuôi mạnh; chiêu mana ngả người lấy đà cánh rồi quạt một phát mạnh; chiêu cuối biến tấu từ bản đang có).

Rig gốc (`monster_3458`) điều khiển thân sau bằng 5 điểm của một đường cong (xương `quxian*`, 8 đốt `H_shenti*` chạy trên đó bằng
path constraint), đuôi là chuỗi FK `weiba*`, cánh là các chuỗi `*chibang*`. Clip mới KHÔNG viết khoá cho từng đốt đã nướng (thân sẽ
gãy), mà ghép / co giãn thời gian / pha trộn / cộng thêm trên GIÁ TRỊ ĐIỀU KHIỂN của các clip của họ (trường `u`, `p` của
`mo_xe/chay.py sample`), rồi đưa lại cho runtime Spine thật nướng (extra.json) → lấy mẫu `l` → `rong_vay_rig.py` dùng như clip của họ.

    rong_vay_clip.py dung                 ghép, ghi <scan>/lam_clip/rv_extra.json
    rong_vay_clip.py xem [clip,..] [n]    tờ khung trên rig gốc bằng runtime thật → <scan>/lam_clip/khung/<clip>.jpg (xem nhịp, dáng)
    rong_vay_clip.py mau                  lấy mẫu 30 khung/giây → <scan>/sample_moi.json (rong_vay_rig.py đọc)
Chạy qua quai/khoa.py chrome (xem, mau mở Chrome ngầm)."""
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rong_vay_bo_cuc as BC  # noqa: E402

FPS = 30.0
SCAN = os.path.join(BC.sxs(), "scan", BC.MON)
LAM = os.path.join(SCAN, "lam_clip")           # bản chép rig gốc (skel, atlas, png) + rv_extra.json
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
TEN = [b["name"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
PATHS = [p["name"] for p in I["path"]]
_S = None


def nhom(*dk):
    """mặt nạ xương theo điều kiện tên: chuỗi con hoặc hàm."""
    m = np.zeros(len(TEN), bool)
    for d in dk:
        m |= np.array([(d(n) if callable(d) else d in n) for n in TEN])
    return m


CANH = nhom("chibang")                                                     # mọi xương cánh (màng, sống, dải cạnh)
DUOI = nhom("weiba", lambda n: n in ("bone30", "bone31", "bone32", "bone33", "bone34"))
MO = nhom(lambda n: n in ("bone10", "bone11"))                             # mỏ trên, mỏ dưới
DC = nhom("quxian")                                                        # điểm điều khiển đường cong thân sau
ix = TEN.index


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; p (8) vị trí trên đường cong."""

    def __init__(self, u, p):
        self.u, self.p = u, p

    def chep(self):
        return Dang(self.u.copy(), self.p.copy())

    def tron(self, B, w, mat_na=None):
        """pha về dáng B: w vô hướng; mat_na chọn xương (đường cong p chỉ pha khi không có mặt nạ hoặc mặt nạ gồm điểm điều khiển)."""
        ww = np.full(len(TEN), float(w)) if mat_na is None else np.where(mat_na, float(w), 0.0)
        u = self.u + (B.u - self.u) * ww[:, None]
        p = self.p + (B.p - self.p) * (float(w) if (mat_na is None or mat_na[DC].any()) else 0.0)
        return Dang(u, p)

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
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float), np.array([f["p"] for f in v["frames"]], float))
              for c, v in S.items()}
    return _S


def dk(clip, t, lap=False):
    """dáng điều khiển của clip gốc ở giây t (nội suy thẳng giữa hai khung 30/giây)."""
    dur, U, P = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, P[i0] * (1 - w) + P[i1] * w)


def nghi():
    return dk("idle_01", 0.0)


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.0):                      # nhanh rồi chậm
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.0):                     # chậm rồi nhanh
    x = min(1.0, max(0.0, x))
    return x ** k


def cung(t, t0, t1, t2, t3):
    """0 → 1 (t0..t1) giữ → 0 (t2..t3), mép êm."""
    if t <= t0 or t >= t3:
        return 0.0
    if t < t1:
        return em((t - t0) / (t1 - t0))
    if t <= t2:
        return 1.0
    return 1.0 - em((t - t2) / (t3 - t2))


def cong(moc, t, kieu=None):
    """đường thời gian từng đoạn: moc = [(giây ra, giây nguồn), ...]; kieu[i] = hàm dịu của đoạn i (mặc định thẳng)."""
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


def ha_mo(D, w):
    """há mỏ w (0..1): như họ làm ở skill_02 (mỏ dưới xoay tới −36°, mỏ trên +3°); cộng lên dáng đang có nhưng không vượt mức đó."""
    D.u[ix("bone11"), 2] = min(D.u[ix("bone11"), 2], B0[ix("bone11"), 2] - 9.6) - 26.0 * w
    D.u[ix("bone10"), 2] += 3.0 * w
    return D


# ---------------------------------------------------------------- 4 clip
def cast(t):
    """CHIÊU MANA 1,60 s: ngả người lấy đà, cánh GIƠ CAO XOÈ HẲN MẶT (0,14 → 0,46, giữ tới 0,60), quạt một phát mạnh xuống – ra trước
    (0,60 → 0,76, sự kiện phun 0,72), dư lực, cánh êm về.
    Nguồn: skill_01 của họ ("giơ cánh chém": cánh giơ xoè ở 0,39 s, đập xuống ở 0,59 s, lướt ra trước ở 0,78 s). Bản đầu dựng trên
    skill_02 bị người dùng trả ("chiêu bắn chưa thấy quạt cánh"): ở skill_02 cánh "giơ" là lật nghiêng mỏng như vạch rồi đập về
    gần dáng nghỉ, mắt không thấy cung quạt. Thêm: ngả lưng +8° lúc lấy đà, chúi −7° lúc quạt, há mỏ lúc quạt, đuôi giảm còn 60%,
    bỏ nhịp thu cánh phụ ở cuối clip nguồn ("quạt MỘT phát")."""
    R = nghi()
    moc = [(0.0, 0.0), (0.14, 0.17), (0.46, 0.39), (0.62, 0.47), (0.76, 0.62), (0.98, 0.80), (1.60, 1.3667)]
    kieu = [em, em, None, None, lambda w: ra(w, 1.8), em]     # cú quạt chạy đúng tốc độ của clip nguồn (cánh họ đập trong ~0,1 s)
    tau = cong(moc, t, kieu)
    S = dk("skill_01", tau)
    D = S.chep()
    D.u[DUOI] = R.tron(S, 0.60).u[DUOI]
    # cú nhún chúi đầu mở màn của skill_01 (0 → 0,2 s) giảm còn 45%: người dùng tả "hơi ngả người lại", không cúi trước
    k0 = 1.0 - 0.55 * cung(t, 0.0, 0.10, 0.16, 0.34)
    if k0 < 1.0:
        D = R.tron(D, k0)
    if t > 0.90:        # sau cú quạt cánh giữ dáng vừa lướt ra trước rồi êm về dáng nghỉ (bỏ nhịp thu cánh lật mỏng của clip nguồn)
        Q = dk("skill_01", cong(moc, 0.90, kieu))
        D.u[CANH] = Q.tron(R, em((t - 0.98) / 0.50), CANH).u[CANH]
    nga = 8.0 * cung(t, 0.16, 0.46, 0.60, 0.68) - 7.0 * cung(t, 0.62, 0.74, 0.90, 1.30)
    D.xoay("zhixin", nga)
    D.doi("zhixin", -40.0 * cung(t, 0.16, 0.46, 0.60, 0.68) + 55.0 * cung(t, 0.62, 0.74, 0.92, 1.35), 0.0)
    ha_mo(D, 0.8 * cung(t, 0.58, 0.68, 0.92, 1.12))
    return D


def attack(t):
    """ĐÒN THƯỜNG 1,05 s: quật đuôi. Lấy đà 0 → 0,32 (thu người, đuôi vung lên quá lưng), quật 0,32 → 0,44 (đuôi bổ xuống phía
    trước, sự kiện trung 0,44), dư lực tới 0,62, về. Nguồn: phần đuôi + thân của skill_02 (đuôi của họ vung lên ở 0,37 rồi bổ xuống
    ở 0,57); cánh chỉ lấy 30% (giữ thăng bằng), để mắt người xem dồn vào đuôi; lúc quật thân chúi tới."""
    R = nghi()
    tau = cong([(0.0, 0.0), (0.32, 0.37), (0.44, 0.57), (0.62, 0.73), (1.05, 1.667)], t,
               [em, lambda w: vao(w, 1.5), lambda w: ra(w, 1.6), em])
    S = dk("skill_02", tau)
    D = S.chep()
    Dc = R.tron(S, 0.30)
    D.u[CANH] = Dc.u[CANH]
    k = cung(t, 0.34, 0.44, 0.60, 0.95)
    D.xoay("zhixin", -7.0 * k)
    D.doi("zhixin", 60.0 * k, -25.0 * k)
    # ngọn đuôi vút thêm lúc quật (trễ pha ra ngọn), rồi nảy lại
    for j, (b, a) in enumerate((("weiba3", 10.0), ("weiba4", 16.0), ("weiba5", 22.0))):
        D.xoay(b, -a * cung(t, 0.36 + 0.02 * j, 0.45 + 0.02 * j, 0.50 + 0.02 * j, 0.70 + 0.03 * j)
               + 0.45 * a * cung(t, 0.56 + 0.02 * j, 0.68 + 0.02 * j, 0.72 + 0.02 * j, 0.92))
    # khung quật: đuôi vươn dài thêm dọc xương (vệt nhoè chuyển động), co lại ngay sau khung trúng
    kd = cung(t, 0.37, 0.42, 0.46, 0.56)
    for b, a in (("weiba2", 0.10), ("weiba3", 0.18), ("weiba4", 0.24), ("weiba5", 0.24)):
        D.u[ix(b), 3] *= 1.0 + a * kd
    return D


def skill(t):
    """CHIÊU CUỐI 2,33 s (biến tấu skill_03 của họ: dựng thẳng người, xoè cánh, giữ, hạ): thêm HÁ MỎ GẦM suốt lúc giữ (họ ngậm
    mỏ), đầu rung, và cánh VỖ HAI NHỊP lúc giữ (lấy nhịp đập của skill_02 pha 55% lên dáng cánh đang xoè). Sự kiện gam 0,70,
    het_gam 1,50 giữ nguyên."""
    S = dk("skill_03", t)
    D = S.chep()
    g = cung(t, 0.55, 0.72, 1.48, 1.72)
    ha_mo(D, g)
    D.xoay("tou", g * 2.6 * math.sin(2 * math.pi * 11.0 * t))
    D.xoay("Q_shenti5", g * 1.6 * math.sin(2 * math.pi * 11.0 * t + 1.1))
    # hai nhịp vỗ: 0,74 → 1,12 và 1,12 → 1,50; mỗi nhịp chạy đoạn 0,40 → 0,92 của skill_02 (giơ, đập, dư lực)
    for a, b in ((0.74, 1.12), (1.12, 1.50)):
        if a <= t <= b:
            x = (t - a) / (b - a)
            V = dk("skill_02", 0.40 + 0.52 * x)
            D = D.tron(V, 0.55 * math.sin(math.pi * x) ** 0.8, CANH)
    return D


BAY = 1.05          # appear: bay vào tới giây này
GAM0, GAM1 = 1.38, 1.92


def appear(t):
    """APPEAR 2,45 s: uốn lượn bay vào (0 → 1,05: dáng bay run_01 của họ, cả con dời từ sau – trên vào chỗ theo đường lượn sóng,
    thân nghiêng theo dốc đường bay), hãm lại thu về dáng nghỉ, rồi GẦM (1,2 → 2,0: vươn người giơ cánh như dáng 0,40 s của
    skill_01, há mỏ, đầu rung), về dáng nghỉ."""
    R = nghi()
    F = dk("run_01", t * 1.0, lap=True)
    w_bay = 1.0 - em((t - (BAY - 0.30)) / 0.42)             # 1 = dáng bay, 0 = dáng nghỉ
    D = R.tron(F, w_bay)
    e = ra(t / BAY, 2.4)
    con = (1.0 - e)
    dx = -900.0 * con
    song = math.sin(2 * math.pi * 1.25 * t + 0.4)
    dy = 300.0 * con + 150.0 * song * con ** 0.6
    doc = (150.0 * 2 * math.pi * 1.25 * math.cos(2 * math.pi * 1.25 * t + 0.4) * con ** 0.6) / 900.0   # dốc tương đối của đường bay
    D.doi("all", dx, dy)
    D.xoay("zhixin", 16.0 * doc * con ** 0.3)
    # gầm
    # thân vươn theo dáng 0,40 s của skill_01 (pha 78%); CÁNH lấy trọn dáng xoè 0,42 s của skill_03: pha cánh nửa chừng giữa hai
    # mặt thì màng bị ép mỏng thành vạch (đã thử pha 62% cả con theo skill_03: cánh mỏng, đuôi cuộn tự đè)
    g = cung(t, 1.14, GAM0, GAM1, 2.40)
    D = D.tron(dk("skill_01", 0.40), 0.78 * g, ~CANH)
    D = D.tron(dk("skill_03", 0.42), g, CANH)
    gm = cung(t, GAM0 - 0.10, GAM0 + 0.04, GAM1, GAM1 + 0.20)
    ha_mo(D, gm)
    D.xoay("tou", gm * (-7.0 + 2.8 * math.sin(2 * math.pi * 12.0 * t)))
    D.xoay("Q_shenti5", gm * 1.7 * math.sin(2 * math.pi * 12.0 * t + 1.0))
    for n in (n for n, m in zip(TEN, CANH) if m and n in ("R_chibang11", "R_chibang15", "R_chibang18", "L_chibang", "L_chibang4", "L_chibang7")):
        D.xoay(n, gm * 2.2 * math.sin(2 * math.pi * 9.0 * t + 0.7))
    return D


CLIP = {"rv_appear": (2.45, appear), "rv_attack": (1.05, attack), "rv_cast": (1.60, cast), "rv_skill": (2.3333, skill)}
# sự kiện (rong_vay_rig.py đọc): giây của khung trúng / nhả / gầm
SU_KIEN = {"rv_attack": [(0.44, "trung", "")], "rv_cast": [(0.72, "phun", ""), (1.24, "het_phun", "")],
           "rv_skill": [(0.70, "gam", ""), (1.50, "het_gam", "")], "rv_appear": []}


def dung():
    out = []
    for ten, (dur, fn) in CLIP.items():
        n = int(round(dur * FPS)) + 1
        ts = [min(dur, i / FPS) for i in range(n)]
        Ds = [fn(t) for t in ts]
        U = np.array([d.u for d in Ds])
        P = np.array([d.p for d in Ds])
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
        paths = {pn: {"position": [[round(t, 4), round(float(v), 5)] for t, v in zip(ts, P[:, k])]} for k, pn in enumerate(PATHS)}
        out.append({"name": ten, "dur": dur, "bones": bones, "paths": paths})
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá")
    os.makedirs(LAM, exist_ok=True)
    json.dump(out, open(os.path.join(LAM, "rv_extra.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "rv_extra.json"))


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
        view = f"&view={a[3]}" if len(a) > 3 else ""
        _chay("sheet", LAM, BC.MON, os.path.join(LAM, "khung"), f"anims={cl}&extra=rv_extra.json&n={n}&tw=520&th=460&cols=6{view}")
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, BC.MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "rv_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
