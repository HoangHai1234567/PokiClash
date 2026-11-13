# -*- coding: utf-8 -*-
"""Clip riêng của boss cuối đảo Mộc (moc_vuong) dựng ở TẦNG ĐIỀU KHIỂN của rig gốc monster_3709 rồi để runtime Spine nướng (IK bốn chân).

Chỉ clip nào phải giải IK mới làm ở đây: `mv_walk` (đi bộ bốn chân tại chỗ: lái bốn đích bàn chân all43, all46, target2, target4 và
thân all2 trên nền idle_01 của họ). Các clip ghép từ dáng đã nướng (appear, fly, skill) làm thẳng trong moc_vuong_rig.py.

    py -3 -I ArtGen/Spine/moc_vuong_clip.py dung                    → <scan>/lam_clip/mv_extra.json
    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/moc_vuong_clip.py xem [clip] [số khung] [view]   → tờ khung trên rig GỐC
    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/moc_vuong_clip.py mau    → <scan>/sample_moi.json (rig của mình đọc)
"""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MON = "monster_3709"
FPS = 30.0
SXS = os.environ.get("SXS") or next((p for p in ("D:/RefAnimation/SwordxStaff", "D:/Ripper/SwordxStaff", "E:/Ripper/SwordxStaff")
                                      if os.path.isdir(p)), "D:/RefAnimation/SwordxStaff")
SCAN = os.path.join(SXS, "scan", MON)
RIG = os.path.join(SXS, "web", "assets", "Monster", MON)
LAM = os.path.join(SCAN, "lam_clip")
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
TEN = [b["name"] for b in I["bones"]]
B0 = np.array([[b["x"], b["y"], b["rot"], b["sx"], b["sy"]] for b in I["bones"]], float)
IKS = [k["name"] for k in I["ik"]]
IK_GAP = [k["bend"] for k in I["ik"]]
_S = None


def ix(n):
    return TEN.index(n)


class Dang:
    """một dáng ở tầng điều khiển: u (số xương, 5) = x, y, xoay, tỉ lệ x, y CHƯA áp ràng buộc; k (số IK) độ trộn IK."""

    def __init__(self, u, k):
        self.u, self.k = u, k

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
        _S = {c: (float(v["dur"]), np.array([f["u"] for f in v["frames"]], float), np.array([[q[0] for q in f["k"]] for f in v["frames"]], float))
              for c, v in S.items() if c in ("idle_01",)}
    return _S


def dk(clip, t, lap=False):
    dur, U, Kk = nap()[clip]
    x = ((t % dur) if lap else min(max(t, 0.0), dur)) * FPS
    i0 = min(int(x), len(U) - 1)
    i1 = min(i0 + 1, len(U) - 1)
    w = x - i0
    return Dang(U[i0] * (1 - w) + U[i1] * w, Kk[i0] * (1 - w) + Kk[i1] * w)


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- walk: đi bộ bốn chân tại chỗ (lặp)
# Bốn đích bàn chân (con của `all`, đứng trên đất): all43 chân trước GẦN, all46 chân trước XA, target2 chân sau GẦN, target4 chân sau XA.
# Kiểu đi chéo của thú bốn chân: (trước gần + sau xa) rồi (trước xa + sau gần); chân sau đi trước chân trước cùng cặp một chút.
# Mỗi bàn chân: 62 % chu kỳ bám đất trượt lùi (thân đang tiến), 38 % nhấc lên đưa tới theo cung. Thân nhún hai lần mỗi chu kỳ, lắc nhẹ.
W_DUR = 1.2
W_BUOC, W_NHAC, W_BAM = 230.0, 105.0, 0.60
W_CHAN = [("all43", 0.00, 1.0, 1.0), ("target4", 0.92, 0.85, 0.8), ("all46", 0.50, 0.85, 0.85), ("target2", 0.42, 1.0, 1.0)]   # (đích, pha, hệ số sải, hệ số nhấc)


def walk(t):
    D = dk("idle_01", t * 2.0 / W_DUR * 1.0, lap=True)          # nền: idle của họ chạy đúng một vòng mỗi chu kỳ bước (cánh, đuôi, bờm)
    p = (t / W_DUR) % 1.0
    for ten, pha, k_sai, k_nhac in W_CHAN:
        q = (p + pha) % 1.0
        S = W_BUOC * k_sai
        if q < W_BAM:
            x, y, r = S / 2 - S * (q / W_BAM), 0.0, 0.0
        else:
            u = (q - W_BAM) / (1 - W_BAM)
            x = -S / 2 + S * em(u)
            y = W_NHAC * k_nhac * math.sin(math.pi * u) ** 0.9
            r = -16.0 * math.sin(2 * math.pi * u) * (1.0 if u < 0.5 else 0.6)      # mũi bàn chân chúc xuống lúc nhấc, ngẩng lúc đặt
        D.doi(ten, x, y)
        D.xoay(ten, r)
    # thân: nhún xuống lúc mỗi cặp chân chạm đất (hai lần mỗi chu kỳ), đưa nhẹ tới lui, vai – hông lắc ngược nhau
    s2, s4 = math.sin(2 * math.pi * p), math.sin(4 * math.pi * (p - 0.04))
    D.doi("all2", 10.0 * math.sin(4 * math.pi * p), -16.0 - 18.0 * math.cos(4 * math.pi * (p - 0.04)))
    D.xoay("all2", 2.6 * s2)
    D.xoay("all3", -2.0 * s2)
    D.xoay("all5", 2.4 * math.sin(4 * math.pi * (p - 0.1)))       # cổ – đầu gật trễ theo nhịp bước
    D.xoay("all7", -2.0 * math.sin(4 * math.pi * (p - 0.16)))
    # con gốc che gần hết chân sau cánh dưới và đuôi: bước đi phải đọc được qua cả khối thân. Bốn gốc cánh nảy trễ theo nhịp nhún
    # (cánh trên ngược pha cánh dưới), hai gốc đuôi đung đưa theo nhịp bước
    k4 = math.sin(4 * math.pi * (p - 0.14))
    for ten, bd in (("all38", 4.5), ("all155", -4.5), ("all63", -6.0), ("all127", 6.0)):
        D.xoay(ten, bd * k4)
    D.xoay("all9", 4.0 * math.sin(2 * math.pi * (p - 0.1)))
    D.xoay("all16", -4.0 * math.sin(2 * math.pi * (p - 0.2)))
    del s4
    return D


CLIP = {"mv_walk": (W_DUR, walk)}


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
        iks = {kn: [[round(t, 4), round(float(v), 4), IK_GAP[j]] for t, v in zip(ts, Kk[:, j])] for j, kn in enumerate(IKS)
               if np.abs(Kk[:, j] - 1).max() > 1e-4}
        out.append({"name": ten, "dur": dur, "bones": bones, "iks": iks})
        print(f"  {ten}: {dur:.2f} s, {n} khung, {len(bones)} xương có khoá, IK {list(iks)}")
    os.makedirs(LAM, exist_ok=True)
    for f in (MON + ".skel", MON + ".atlas", MON + ".png"):
        if not os.path.exists(os.path.join(LAM, f)):
            shutil.copy(os.path.join(RIG, f), os.path.join(LAM, f))
    json.dump(out, open(os.path.join(LAM, "mv_extra.json"), "w", encoding="utf-8"))
    print(os.path.join(LAM, "mv_extra.json"))


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
        _chay("sheet", LAM, MON, os.path.join(LAM, "khung"), f"anims={cl}&extra=mv_extra.json&n={n}&tw=430&th=330&cols=6&loop=1{view}")
    elif lenh == "mau":
        dung()
        _chay("sample", LAM, MON, os.path.join(SCAN, "sample_moi.json"), ",".join(CLIP), "30", "mv_extra.json")


if __name__ == "__main__":
    main(sys.argv[1:])
